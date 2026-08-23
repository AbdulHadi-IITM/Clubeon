"""
Stripe payment integration for the payments module, wired into the
booking / membership / event flows.

Flow:
  1. Client calls POST /api/v1/payments/stripe/create-payment-intent with just
     `payment_type` + `reference_id`. The **amount is resolved server-side** from
     the referenced entity (never trusted from the client):
       - booking     -> flat BOOKING_FEE (config); booking must belong to the
                        user and still be active
       - membership  -> MembershipPlan.price (plan must be active)
       - event       -> Event.registration_fee (must be > 0)
     We record a pending `Payment`, create a Stripe PaymentIntent, store its id
     as gateway_transaction_id, and return the `client_secret`.
  2. Stripe calls POST /api/v1/payments/stripe/webhook after the payment
     resolves. We verify the signature and flip the Payment to
     completed / failed.

Amounts are in major units (e.g. rupees) and converted to the smallest currency
unit (paise/cents) for Stripe.
"""
import stripe
from flask import current_app

from app.extensions import db
from app.payments.models import Payment
from app.payments.fulfillment import FulfillmentService
from app.bookings.models import Booking
from app.memberships.models import MembershipPlan, Membership
from app.events.models import Event

ALLOWED_PAYMENT_TYPES = {"booking", "membership", "event"}
# Currencies Stripe treats as zero-decimal (no *100 conversion).
ZERO_DECIMAL_CURRENCIES = {"jpy", "krw", "vnd", "clp", "bif", "djf", "gnf",
                           "kmf", "mga", "pyg", "rwf", "ugx", "vuv", "xaf",
                           "xof", "xpf"}


class StripeService:
    @staticmethod
    def _configure():
        """Set the Stripe API key from config. Returns an error dict if unset."""
        secret = current_app.config.get("STRIPE_SECRET_KEY")
        if not secret:
            return {"code": "CONFIG_ERROR",
                    "message": "Stripe is not configured (STRIPE_SECRET_KEY missing)."}
        stripe.api_key = secret
        return None

    @staticmethod
    def _to_minor_units(amount, currency):
        if currency.lower() in ZERO_DECIMAL_CURRENCIES:
            return int(round(amount))
        return int(round(amount * 100))

    @staticmethod
    def resolve_amount(user_id, payment_type, reference_id):
        if payment_type == "booking":
            booking = Booking.query.get(reference_id)
            if not booking:
                return None, {"code": "NOT_FOUND", "message": "Booking not found."}
            if booking.user_id != user_id:
                return None, {"code": "FORBIDDEN", "message": "You cannot pay for another user's booking."}
            if booking.status != "active":
                return None, {"code": "VALIDATION_ERROR", "message": f"Booking is '{booking.status}' and cannot be paid for."}

            base_fee = float(current_app.config.get("BOOKING_FEE", 500.0))

            # Check for active membership
            membership = Membership.query.filter_by(user_id=user_id, status='active').first()
            discount = membership.plan.discount_percentage if membership and membership.plan else 0
            amount = base_fee * (1 - discount / 100.0)

            # If discounted to zero, still return zero; the caller handles free payments
            return float(amount), None

        # For membership plans
        if payment_type == "membership":
            plan = MembershipPlan.query.get(reference_id)
            if not plan or not plan.is_active:
                return None, {"code": "NOT_FOUND", "message": "Membership plan not found or inactive."}
            return float(plan.price), None

        # For events
        if payment_type == "event":
            event = Event.query.get(reference_id)
            if not event:
                return None, {"code": "NOT_FOUND", "message": "Event not found."}
            fee = float(event.registration_fee or 0)
            if fee <= 0:
                return None, {"code": "VALIDATION_ERROR", "message": "This event is free; no payment required."}
            return fee, None

        return None, {"code": "VALIDATION_ERROR", "message": "Invalid payment_type"}

    @staticmethod
    def create_payment_intent(user_id, payment_type, reference_id, currency=None):
        """
        Create a Stripe PaymentIntent for a booking / membership / event.

        Returns (result_dict, None) on success or (None, error_dict) on failure.
        """
        # --- basic validation ---
        if payment_type not in ALLOWED_PAYMENT_TYPES:
            return None, {"code": "VALIDATION_ERROR",
                          "message": "payment_type must be one of: "
                                     + ", ".join(sorted(ALLOWED_PAYMENT_TYPES))}
        if reference_id is None:
            return None, {"code": "VALIDATION_ERROR",
                          "message": "reference_id is required."}

        err = StripeService._configure()
        if err:
            return None, err

        # Normalize currency (default to 'inr' if not provided)
        currency = (currency or current_app.config.get("STRIPE_DEFAULT_CURRENCY", "inr")).lower()
        currency_code = currency.upper()

        # Already paid for? Don't let the user be charged twice.
        already_paid = Payment.query.filter_by(
            user_id=user_id, payment_type=payment_type,
            reference_id=reference_id, status="completed").first()
        if already_paid:
            return None, {"code": "ALREADY_PAID",
                          "message": "This item has already been paid for."}

        # --- amount resolved server-side from the referenced entity ---
        amount, err = StripeService.resolve_amount(user_id, payment_type, reference_id)
        if err:
            return None, err

        if amount <= 0:
            # Free purchase – skip Stripe, directly mark payment and fulfil
            payment = Payment(
                user_id=user_id,
                amount=0,
                currency=currency_code,
                payment_type=payment_type,
                reference_id=reference_id,
                status="completed"
            )
            db.session.add(payment)
            db.session.commit()
            # Fulfil the membership/event/booking
            FulfillmentService.mark_paid_and_fulfill(payment)
            return {
                "payment_id": payment.id,
                "client_secret": None,
                "amount": 0,
                "currency": currency,
                "payment_type": payment_type,
                "reference_id": reference_id,
                "status": "completed",
            }, None

        # ===== Normal case: amount > 0, we need to create a Stripe PaymentIntent =====

        # Create a pending Payment record first
        payment = Payment(
            user_id=user_id,
            amount=amount,
            currency=currency_code,
            payment_type=payment_type,
            reference_id=reference_id,
            status="pending"
        )
        db.session.add(payment)
        db.session.commit()

        # Create the Stripe PaymentIntent
        try:
            intent = stripe.PaymentIntent.create(
                amount=StripeService._to_minor_units(amount, currency),
                currency=currency,
                automatic_payment_methods={"enabled": True},
                metadata={
                    "payment_id": payment.id,
                    "user_id": user_id,
                    "payment_type": payment_type,
                    "reference_id": reference_id,
                },
            )
        except stripe.StripeError as e:
            # Mark the payment as failed if Stripe rejects it
            payment.status = "failed"
            db.session.commit()
            message = getattr(e, "user_message", None) or str(e)
            return None, {"code": "PAYMENT_GATEWAY_ERROR", "message": message}

        # Store the Stripe PaymentIntent ID and commit
        payment.gateway_transaction_id = intent.id
        db.session.commit()

        return {
            "payment_id": payment.id,
            "client_secret": intent.client_secret,
            "amount": amount,
            "currency": currency,
            "payment_type": payment_type,
            "reference_id": reference_id,
            "status": payment.status,
            "publishable_key": current_app.config.get("STRIPE_PUBLISHABLE_KEY"),
        }, None

    @staticmethod
    def handle_webhook(payload, signature_header):
        """
        Verify a Stripe webhook and update the matching Payment.

        `payload` must be the raw request body (bytes). Returns
        (result_dict, None) or (None, error_dict).
        """
        err = StripeService._configure()
        if err:
            return None, err

        secret = current_app.config.get("STRIPE_WEBHOOK_SECRET")
        if not secret:
            return None, {"code": "CONFIG_ERROR",
                          "message": "Stripe webhook secret not configured."}

        try:
            event = stripe.Webhook.construct_event(payload, signature_header, secret)
        except ValueError:
            return None, {"code": "VALIDATION_ERROR", "message": "Invalid payload."}
        except stripe.SignatureVerificationError:
            return None, {"code": "INVALID_SIGNATURE", "message": "Invalid signature."}

        event_type = event["type"]
        obj = event["data"]["object"]
        intent_id = obj.get("id")

        payment = None
        if intent_id:
            payment = Payment.query.filter_by(gateway_transaction_id=intent_id).first()
        if payment is None:
            payment_id = (obj.get("metadata") or {}).get("payment_id")
            if payment_id:
                payment = Payment.query.get(int(payment_id))

        if payment is None:
            # Unknown/irrelevant event — acknowledge so Stripe stops retrying.
            return {"received": True, "type": event_type,
                    "fulfilment": "no_matching_payment"}, None

        if intent_id and not payment.gateway_transaction_id:
            payment.gateway_transaction_id = intent_id

        fulfilment = "ignored"
        if event_type == "payment_intent.succeeded":
            # Marks the payment completed AND delivers what was paid for
            # (activate membership / confirm event registration / confirm
            # booking). Idempotent across Stripe's webhook retries.
            fulfilment, _ = FulfillmentService.mark_paid_and_fulfill(payment)
        elif event_type in ("payment_intent.payment_failed",
                            "payment_intent.canceled"):
            fulfilment, _ = FulfillmentService.mark_failed(payment)
        else:
            db.session.commit()

        return {"received": True, "type": event_type,
                "payment_id": payment.id, "fulfilment": fulfilment}, None