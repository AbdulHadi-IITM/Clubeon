"""
End-to-end tests for the payment workflow: pay -> webhook -> fulfilment.

Covers the gap these tests were written for: a successful Stripe payment must
actually *deliver* what was bought (activate the membership, confirm the event
registration, confirm the booking), be idempotent across Stripe's webhook
retries, and be observable via the payment-status endpoint.

The Stripe SDK is monkeypatched so everything runs offline.
"""
from datetime import date, time, timedelta
from types import SimpleNamespace

import pytest
import stripe
from flask_jwt_extended import create_access_token

from app.payments.models import Payment
from app.bookings.models import Booking
from app.memberships.models import MembershipPlan, Membership
from app.events.models import Event, EventRegistration
from app.notifications.models import Notification

CREATE = "/api/v1/payments/stripe/create-payment-intent"
WEBHOOK = "/api/v1/payments/stripe/webhook"


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _token(app, user):
    with app.app_context():
        return create_access_token(identity=str(user.id),
                                   additional_claims={"role": user.role},
                                   expires_delta=timedelta(hours=1))


def _login(client, app, user):
    client.set_cookie("access_token_cookie", _token(app, user))


def _stub_intent(monkeypatch, intent_id="pi_test"):
    monkeypatch.setattr(
        stripe.PaymentIntent, "create",
        staticmethod(lambda **kw: SimpleNamespace(
            id=intent_id, client_secret=f"{intent_id}_secret")))


def _send_webhook(client, monkeypatch, intent_id="pi_test",
                  event_type="payment_intent.succeeded", payment_id=None):
    """Deliver a Stripe event with a stubbed (valid) signature."""
    obj = {"id": intent_id, "metadata": {}}
    if payment_id is not None:
        obj["metadata"]["payment_id"] = payment_id
    monkeypatch.setattr(
        stripe.Webhook, "construct_event",
        staticmethod(lambda payload, sig, secret: {
            "type": event_type, "data": {"object": obj}}))
    return client.post(WEBHOOK, data=b"{}",
                       headers={"Stripe-Signature": "t=1,v1=ok"})


@pytest.fixture
def stripe_cfg(app):
    app.config["STRIPE_SECRET_KEY"] = "sk_test_dummy"
    app.config["STRIPE_WEBHOOK_SECRET"] = "whsec_dummy"
    app.config["BOOKING_FEE"] = 500.0
    return app


# --------------------------------------------------------------------------
# MEMBERSHIP — the reported bug: payment did not activate the membership
# --------------------------------------------------------------------------
def test_membership_is_activated_on_successful_payment(
        client, stripe_cfg, db_session, make_player, sample_club, monkeypatch):
    app = stripe_cfg
    user = make_player(email="mem_activate@test.com")
    plan = MembershipPlan(club_id=sample_club.id, name="Gold",
                          price_monthly=999.0, is_active=True)
    db_session.add(plan)
    db_session.commit()
    plan_id, club_id = plan.id, sample_club.id

    _stub_intent(monkeypatch, "pi_mem")
    _login(client, app, user)
    resp = client.post(CREATE, json={"payment_type": "membership",
                                     "reference_id": plan_id})
    assert resp.status_code == 201
    payment_id = resp.json["payment_id"]

    # Before the webhook: no membership yet.
    with app.app_context():
        assert Membership.query.filter_by(user_id=user.id).count() == 0

    hook = _send_webhook(client, monkeypatch, "pi_mem", payment_id=payment_id)
    assert hook.status_code == 200
    assert hook.json["fulfilment"] == "membership_activated"

    with app.app_context():
        assert Payment.query.get(payment_id).status == "completed"
        m = Membership.query.filter_by(user_id=user.id, club_id=club_id).first()
        assert m is not None, "membership was not created by payment fulfilment"
        assert m.status == "active"
        assert m.plan_id == plan_id
        assert m.start_date == date.today()
        assert m.end_date > m.start_date
        # user is told about it
        assert Notification.query.filter_by(user_id=user.id).count() >= 1


def test_membership_fulfilment_is_idempotent(
        client, stripe_cfg, db_session, make_player, sample_club, monkeypatch):
    """Stripe retries webhooks — a duplicate event must not double-activate."""
    app = stripe_cfg
    user = make_player(email="mem_idem@test.com")
    plan = MembershipPlan(club_id=sample_club.id, name="Silver",
                          price_monthly=499.0, is_active=True)
    db_session.add(plan)
    db_session.commit()

    _stub_intent(monkeypatch, "pi_idem")
    _login(client, app, user)
    payment_id = client.post(CREATE, json={"payment_type": "membership",
                                           "reference_id": plan.id}).json["payment_id"]

    first = _send_webhook(client, monkeypatch, "pi_idem", payment_id=payment_id)
    second = _send_webhook(client, monkeypatch, "pi_idem", payment_id=payment_id)

    assert first.json["fulfilment"] == "membership_activated"
    assert second.json["fulfilment"] == "already_completed"
    with app.app_context():
        assert Membership.query.filter_by(user_id=user.id).count() == 1


# --------------------------------------------------------------------------
# EVENT
# --------------------------------------------------------------------------
def test_event_registration_confirmed_on_payment(
        client, stripe_cfg, db_session, make_player, sample_club, monkeypatch):
    app = stripe_cfg
    user = make_player(email="ev_fulfil@test.com")
    event = Event(club_id=sample_club.id, created_by=sample_club.owner_id,
                  title="Championship", event_date=date(2026, 9, 1),
                  start_time=time(9, 0), end_time=time(12, 0),
                  registration_fee=200.0, status="upcoming")
    db_session.add(event)
    db_session.commit()
    event_id = event.id

    _stub_intent(monkeypatch, "pi_ev")
    _login(client, app, user)
    payment_id = client.post(CREATE, json={"payment_type": "event",
                                           "reference_id": event_id}).json["payment_id"]

    with app.app_context():
        assert EventRegistration.query.filter_by(event_id=event_id).count() == 0

    hook = _send_webhook(client, monkeypatch, "pi_ev", payment_id=payment_id)
    assert hook.json["fulfilment"] == "registration_confirmed"

    with app.app_context():
        reg = EventRegistration.query.filter_by(event_id=event_id,
                                                user_id=user.id).first()
        assert reg is not None, "registration was not created by fulfilment"
        assert reg.status == "registered"


def test_event_full_at_fulfilment_is_flagged(
        client, stripe_cfg, db_session, make_player, sample_club, monkeypatch):
    """Capacity is still enforced if the event fills up mid-payment."""
    app = stripe_cfg
    payer = make_player(email="ev_late@test.com")
    other = make_player(email="ev_first@test.com")
    event = Event(club_id=sample_club.id, created_by=sample_club.owner_id,
                  title="Tiny", event_date=date(2026, 9, 1),
                  start_time=time(9, 0), end_time=time(12, 0),
                  registration_fee=100.0, max_attendees=1, status="upcoming")
    db_session.add(event)
    db_session.commit()

    _stub_intent(monkeypatch, "pi_full")
    _login(client, app, payer)
    payment_id = client.post(CREATE, json={"payment_type": "event",
                                           "reference_id": event.id}).json["payment_id"]

    # someone else takes the last seat before the webhook arrives
    db_session.add(EventRegistration(event_id=event.id, user_id=other.id,
                                     status="registered"))
    db_session.commit()

    hook = _send_webhook(client, monkeypatch, "pi_full", payment_id=payment_id)
    assert hook.json["fulfilment"] == "event_full"
    with app.app_context():
        # payment still recorded as completed (money was taken -> refundable)
        assert Payment.query.get(payment_id).status == "completed"
        assert EventRegistration.query.filter_by(
            event_id=event.id, user_id=payer.id).count() == 0


# --------------------------------------------------------------------------
# BOOKING
# --------------------------------------------------------------------------
def test_booking_confirmed_on_payment(
        client, stripe_cfg, db_session, make_player, sample_club, monkeypatch):
    app = stripe_cfg
    user = make_player(email="bk_fulfil@test.com")
    booking = Booking(user_id=user.id, court_id=sample_club.courts[0].id,
                      booking_date=date(2026, 9, 1), start_time=time(10, 0),
                      end_time=time(11, 0), status="active")
    db_session.add(booking)
    db_session.commit()

    _stub_intent(monkeypatch, "pi_bk")
    _login(client, app, user)
    payment_id = client.post(CREATE, json={"payment_type": "booking",
                                           "reference_id": booking.id}).json["payment_id"]

    hook = _send_webhook(client, monkeypatch, "pi_bk", payment_id=payment_id)
    assert hook.json["fulfilment"] == "booking_confirmed"
    with app.app_context():
        assert Payment.query.get(payment_id).status == "completed"
        assert Notification.query.filter_by(user_id=user.id).count() >= 1


def test_released_booking_is_flagged_at_fulfilment(
        client, stripe_cfg, db_session, make_player, sample_club, monkeypatch):
    app = stripe_cfg
    user = make_player(email="bk_released@test.com")
    booking = Booking(user_id=user.id, court_id=sample_club.courts[0].id,
                      booking_date=date(2026, 9, 2), start_time=time(10, 0),
                      end_time=time(11, 0), status="active")
    db_session.add(booking)
    db_session.commit()

    _stub_intent(monkeypatch, "pi_rel")
    _login(client, app, user)
    payment_id = client.post(CREATE, json={"payment_type": "booking",
                                           "reference_id": booking.id}).json["payment_id"]

    booking.status = "released"
    db_session.commit()

    hook = _send_webhook(client, monkeypatch, "pi_rel", payment_id=payment_id)
    assert hook.json["fulfilment"] == "booking_inactive"


# --------------------------------------------------------------------------
# FAILURE PATH
# --------------------------------------------------------------------------
def test_failed_payment_does_not_fulfil(
        client, stripe_cfg, db_session, make_player, sample_club, monkeypatch):
    app = stripe_cfg
    user = make_player(email="mem_fail@test.com")
    plan = MembershipPlan(club_id=sample_club.id, name="Bronze",
                          price_monthly=199.0, is_active=True)
    db_session.add(plan)
    db_session.commit()

    _stub_intent(monkeypatch, "pi_fail")
    _login(client, app, user)
    payment_id = client.post(CREATE, json={"payment_type": "membership",
                                           "reference_id": plan.id}).json["payment_id"]

    hook = _send_webhook(client, monkeypatch, "pi_fail", payment_id=payment_id,
                         event_type="payment_intent.payment_failed")
    assert hook.json["fulfilment"] == "failed"
    with app.app_context():
        assert Payment.query.get(payment_id).status == "failed"
        assert Membership.query.filter_by(user_id=user.id).count() == 0


def test_late_failure_cannot_downgrade_completed_payment(
        client, stripe_cfg, db_session, make_player, sample_club, monkeypatch):
    app = stripe_cfg
    user = make_player(email="mem_late_fail@test.com")
    plan = MembershipPlan(club_id=sample_club.id, name="Plat",
                          price_monthly=1299.0, is_active=True)
    db_session.add(plan)
    db_session.commit()

    _stub_intent(monkeypatch, "pi_late")
    _login(client, app, user)
    payment_id = client.post(CREATE, json={"payment_type": "membership",
                                           "reference_id": plan.id}).json["payment_id"]

    _send_webhook(client, monkeypatch, "pi_late", payment_id=payment_id)
    late = _send_webhook(client, monkeypatch, "pi_late", payment_id=payment_id,
                         event_type="payment_intent.payment_failed")
    assert late.json["fulfilment"] == "already_completed"
    with app.app_context():
        assert Payment.query.get(payment_id).status == "completed"


# --------------------------------------------------------------------------
# DOUBLE-CHARGE GUARD + STATUS ENDPOINT
# --------------------------------------------------------------------------
def test_cannot_pay_twice_for_same_item(
        client, stripe_cfg, db_session, make_player, sample_club, monkeypatch):
    app = stripe_cfg
    user = make_player(email="dbl@test.com")
    plan = MembershipPlan(club_id=sample_club.id, name="Once",
                          price_monthly=299.0, is_active=True)
    db_session.add(plan)
    db_session.commit()

    _stub_intent(monkeypatch, "pi_once")
    _login(client, app, user)
    payment_id = client.post(CREATE, json={"payment_type": "membership",
                                           "reference_id": plan.id}).json["payment_id"]
    _send_webhook(client, monkeypatch, "pi_once", payment_id=payment_id)

    again = client.post(CREATE, json={"payment_type": "membership",
                                      "reference_id": plan.id})
    assert again.status_code == 409
    assert again.json["code"] == "ALREADY_PAID"


def test_payment_status_endpoint_reports_fulfilment(
        client, stripe_cfg, db_session, make_player, sample_club, monkeypatch):
    app = stripe_cfg
    user = make_player(email="status@test.com")
    plan = MembershipPlan(club_id=sample_club.id, name="Status",
                          price_monthly=350.0, is_active=True)
    db_session.add(plan)
    db_session.commit()

    _stub_intent(monkeypatch, "pi_status")
    _login(client, app, user)
    payment_id = client.post(CREATE, json={"payment_type": "membership",
                                           "reference_id": plan.id}).json["payment_id"]

    pending = client.get(f"/api/v1/payments/stripe/status/{payment_id}")
    assert pending.status_code == 200
    assert pending.json["status"] == "pending"

    _send_webhook(client, monkeypatch, "pi_status", payment_id=payment_id)

    done = client.get(f"/api/v1/payments/stripe/status/{payment_id}")
    assert done.json["status"] == "completed"
    assert done.json["membership_id"] is not None


def test_payment_status_is_private_to_owner(
        client, stripe_cfg, db_session, make_player, sample_club, monkeypatch):
    app = stripe_cfg
    owner_user = make_player(email="priv_owner@test.com")
    intruder = make_player(email="priv_intruder@test.com")
    plan = MembershipPlan(club_id=sample_club.id, name="Priv",
                          price_monthly=100.0, is_active=True)
    db_session.add(plan)
    db_session.commit()

    _stub_intent(monkeypatch, "pi_priv")
    _login(client, app, owner_user)
    payment_id = client.post(CREATE, json={"payment_type": "membership",
                                           "reference_id": plan.id}).json["payment_id"]

    _login(client, app, intruder)
    resp = client.get(f"/api/v1/payments/stripe/status/{payment_id}")
    assert resp.status_code == 403


def test_webhook_for_unknown_payment_is_acknowledged(
        client, stripe_cfg, monkeypatch):
    """Unknown events must return 200 so Stripe stops retrying."""
    hook = _send_webhook(client, monkeypatch, "pi_does_not_exist")
    assert hook.status_code == 200
    assert hook.json["fulfilment"] == "no_matching_payment"
