"""
Post-payment fulfilment.

Recording a Payment as `completed` is only half of a payment workflow — the
thing the user paid for still has to be delivered. This module performs that
second half, and is invoked from the Stripe webhook once a PaymentIntent
succeeds:

    membership  -> create/activate the Membership for the paid plan
    event       -> confirm the user's EventRegistration
    booking     -> confirm the booking is active

A notification is raised for the user in every case.

**Idempotency:** Stripe retries webhooks (and may deliver the same event more
than once), so `fulfill` must be safe to call repeatedly. It is driven off the
`pending -> completed` transition: the caller flips the status only via
`mark_paid_and_fulfill`, which returns early if the Payment is already
`completed`. Each handler is additionally written to be a no-op when the
entity is already in its fulfilled state.
"""
from datetime import date

from dateutil.relativedelta import relativedelta

from app.extensions import db
from app.payments.models import Payment
from app.bookings.models import Booking
from app.memberships.models import MembershipPlan, Membership
from app.events.models import Event, EventRegistration
from app.notifications.models import Notification


def _notify(user_id, title, body, type_):
    db.session.add(Notification(user_id=user_id, title=title, body=body, type=type_))


class FulfillmentService:
    # ------------------------------------------------------------------
    # entry point
    # ------------------------------------------------------------------
    @staticmethod
    def mark_paid_and_fulfill(payment):
        """
        Flip a Payment to 'completed' and deliver what was paid for.

        Idempotent: returns ("already_completed", None) if the payment has
        already been fulfilled. Returns (result_str, error_dict).
        """
        if payment.status == "completed":
            return "already_completed", None

        payment.status = "completed"

        handler = {
            "membership": FulfillmentService._fulfill_membership,
            "event": FulfillmentService._fulfill_event,
            "booking": FulfillmentService._fulfill_booking,
        }.get(payment.payment_type)

        if handler is None:
            db.session.commit()
            return "no_handler", None

        result, error = handler(payment)
        db.session.commit()
        return result, error

    @staticmethod
    def mark_failed(payment):
        """Mark a Payment failed. Idempotent; performs no fulfilment."""
        if payment.status == "completed":
            # A completed payment must never be downgraded by a late/duplicate
            # failure event.
            return "already_completed", None
        if payment.status == "failed":
            return "already_failed", None
        payment.status = "failed"
        _notify(payment.user_id, "Payment failed",
                f"Your {payment.payment_type} payment of "
                f"{payment.currency} {payment.amount:.2f} could not be completed.",
                "payment")
        db.session.commit()
        return "failed", None

    # ------------------------------------------------------------------
    # per-type handlers
    # ------------------------------------------------------------------
    @staticmethod
    def _fulfill_membership(payment):
        """`reference_id` is the MembershipPlan id that was paid for."""
        plan = MembershipPlan.query.get(payment.reference_id)
        if not plan:
            return "plan_missing", {"code": "NOT_FOUND",
                                    "message": "Membership plan no longer exists."}

        # Already active for this club (e.g. duplicate webhook, or the user
        # subscribed by another route) -> nothing to do.
        existing = Membership.query.filter_by(
            user_id=payment.user_id, club_id=plan.club_id, status="active"
        ).first()
        if existing:
            return "membership_already_active", None

        start_date = date.today()
        membership = Membership(
            user_id=payment.user_id,
            plan_id=plan.id,
            club_id=plan.club_id,
            status="active",
            start_date=start_date,
            end_date=start_date + relativedelta(months=plan.duration_months or 1),
            auto_renew=False,
        )
        db.session.add(membership)
        _notify(payment.user_id, "Membership activated",
                f"Your '{plan.name}' membership is now active until "
                f"{membership.end_date.isoformat()}.",
                "payment")
        return "membership_activated", None

    @staticmethod
    def _fulfill_event(payment):
        """`reference_id` is the Event id that was paid for."""
        event = Event.query.get(payment.reference_id)
        if not event:
            return "event_missing", {"code": "NOT_FOUND",
                                     "message": "Event no longer exists."}

        registration = EventRegistration.query.filter_by(
            event_id=event.id, user_id=payment.user_id
        ).first()

        if registration is not None:
            if registration.status == "registered":
                return "registration_already_confirmed", None
            registration.status = "registered"
        else:
            # Respect capacity even at fulfilment time.
            if event.max_attendees:
                taken = EventRegistration.query.filter_by(
                    event_id=event.id, status="registered").count()
                if taken >= event.max_attendees:
                    _notify(payment.user_id, "Event is full",
                            f"'{event.title}' filled up before your payment "
                            "completed. Your payment is eligible for a refund.",
                            "event")
                    return "event_full", {"code": "CONFLICT",
                                          "message": "Event is full."}
            registration = EventRegistration(
                event_id=event.id, user_id=payment.user_id, status="registered")
            db.session.add(registration)

        _notify(payment.user_id, "Event registration confirmed",
                f"You are registered for '{event.title}' on "
                f"{event.event_date.isoformat()}.",
                "event")
        return "registration_confirmed", None

    @staticmethod
    def _fulfill_booking(payment):
        """`reference_id` is the Booking id that was paid for."""
        booking = Booking.query.get(payment.reference_id)
        if not booking:
            return "booking_missing", {"code": "NOT_FOUND",
                                       "message": "Booking no longer exists."}

        if booking.status != "active":
            # Released/overridden before the payment landed.
            _notify(payment.user_id, "Booking no longer held",
                    "Your payment succeeded but the booking is "
                    f"'{booking.status}'. It is eligible for a refund.",
                    "booking")
            return "booking_inactive", {"code": "CONFLICT",
                                        "message": f"Booking is {booking.status}."}

        _notify(payment.user_id, "Booking confirmed",
                f"Your court booking on {booking.booking_date.isoformat()} "
                f"({str(booking.start_time)[:5]}–{str(booking.end_time)[:5]}) is confirmed.",
                "booking")
        return "booking_confirmed", None


class PaymentStatusService:
    """Read helpers used by the payment-status endpoint."""

    @staticmethod
    def get_status(user_id, payment_id):
        payment = Payment.query.get(payment_id)
        if not payment:
            return None, {"code": "NOT_FOUND", "message": "Payment not found."}
        if payment.user_id != user_id:
            return None, {"code": "FORBIDDEN",
                          "message": "Not authorized to view this payment."}

        if payment.status == "pending" and payment.gateway_transaction_id:
            from app.payments.services import PaymentService
            PaymentService._reconcile_with_stripe(payment)
            db.session.refresh(payment)

        data = {
            "payment_id": payment.id,
            "status": payment.status,
            "amount": payment.amount,
            "currency": payment.currency,
            "payment_type": payment.payment_type,
            "reference_id": payment.reference_id,
            "transaction_id": payment.gateway_transaction_id,
            "created_at": str(payment.created_at),
        }

        # Surface what the payment unlocked, so the client can route the user.
        if payment.status == "completed" and payment.payment_type == "membership":
            plan = MembershipPlan.query.get(payment.reference_id)
            if plan:
                membership = Membership.query.filter_by(
                    user_id=payment.user_id, club_id=plan.club_id,
                    status="active").first()
                data["membership_id"] = membership.id if membership else None
        if payment.status == "completed" and payment.payment_type == "event":
            reg = EventRegistration.query.filter_by(
                event_id=payment.reference_id, user_id=payment.user_id).first()
            data["registration_status"] = reg.status if reg else None

        return data, None
