"""
Payment lookups and the settlement check that gates paid fulfilment.

The client-side checkout confirms a card with Stripe and then asks the server
to grant the thing that was paid for. The server must not take the client's
word for that, so `settle` is the single place that answers "has this user
actually paid for this item?".

Settlement order:
  1. A `completed` Payment already exists -> yes.
  2. A `pending` Payment exists -> ask Stripe for the PaymentIntent's real
     status and reconcile. This closes the window between the shopper
     finishing checkout and Stripe's webhook arriving, and means the flow also
     works in environments with no webhook configured at all.
  3. Otherwise -> not paid.
"""
from app.extensions import db
from app.payments.models import Payment


class PaymentService:
    @staticmethod
    def get_my_payments(user_id):
        return Payment.query.filter_by(user_id=user_id).order_by(
            Payment.created_at.desc()).all()

    @staticmethod
    def find_completed(user_id, payment_type, reference_id):
        return Payment.query.filter_by(
            user_id=user_id,
            payment_type=payment_type,
            reference_id=reference_id,
            status="completed",
        ).first()

    @staticmethod
    def settle(user_id, payment_type, reference_id):
        """
        Return True if `reference_id` has been paid for by `user_id`.

        Reconciles a pending Stripe PaymentIntent as a side effect, so a
        payment that succeeded at the card step counts even if the webhook has
        not landed yet.
        """
        if PaymentService.find_completed(user_id, payment_type, reference_id):
            return True

        pending = Payment.query.filter_by(
            user_id=user_id,
            payment_type=payment_type,
            reference_id=reference_id,
            status="pending",
        ).order_by(Payment.created_at.desc()).first()

        if pending is None or not pending.gateway_transaction_id:
            return False

        return PaymentService._reconcile_with_stripe(pending)

    @staticmethod
    def _reconcile_with_stripe(payment):
        """Ask Stripe for the intent's status and apply it. Best effort."""
        import stripe
        from flask import current_app
        from app.payments.fulfillment import FulfillmentService

        secret = current_app.config.get("STRIPE_SECRET_KEY")
        if not secret:
            return False
        stripe.api_key = secret

        try:
            intent = stripe.PaymentIntent.retrieve(payment.gateway_transaction_id)
        except Exception:
            current_app.logger.exception(
                "Could not retrieve PaymentIntent %s for payment %s",
                payment.gateway_transaction_id, payment.id)
            return False

        status = getattr(intent, "status", None)
        if status == "succeeded":
            FulfillmentService.mark_paid_and_fulfill(payment)
            return True
        if status in ("canceled", "requires_payment_method"):
            # `requires_payment_method` after a confirm attempt means the card
            # was declined. Leave it pending otherwise; the shopper may still
            # be mid-checkout.
            if status == "canceled":
                FulfillmentService.mark_failed(payment)
        db.session.rollback()
        return False
