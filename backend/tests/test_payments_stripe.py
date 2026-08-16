"""
Tests for the Stripe payment API (/api/v1/payments/stripe/*), including its
integration with the booking / membership / event flows.

The Stripe SDK is monkeypatched so these tests run fully offline (no network,
no real API keys) — consistent with the rest of the suite.
"""
from datetime import date, time
from types import SimpleNamespace

import stripe

from app.payments.models import Payment
from app.bookings.models import Booking
from app.memberships.models import MembershipPlan
from app.events.models import Event

ENDPOINT = "/api/v1/payments/stripe/create-payment-intent"


def _login(client, auth_headers, user=None):
    client.set_cookie("access_token_cookie", auth_headers(user))


# ---------- booking integration ----------

def test_booking_payment_success(client, app, db_session, make_player,
                                 sample_club, auth_headers, monkeypatch):
    app.config["STRIPE_SECRET_KEY"] = "sk_test_dummy"
    app.config["BOOKING_FEE"] = 500.0

    user = make_player(email="payer@test.com")
    booking = Booking(user_id=user.id, court_id=sample_club.courts[0].id,
                      booking_date=date(2026, 9, 1), start_time=time(10, 0),
                      end_time=time(11, 0), status="active")
    db_session.add(booking)
    db_session.commit()
    booking_id = booking.id

    def fake_create(**kwargs):
        assert kwargs["amount"] == 50000            # 500.00 -> paise
        assert kwargs["metadata"]["payment_type"] == "booking"
        assert kwargs["metadata"]["reference_id"] == booking_id
        return SimpleNamespace(id="pi_book", client_secret="pi_book_secret")

    monkeypatch.setattr(stripe.PaymentIntent, "create", staticmethod(fake_create))
    _login(client, auth_headers, user)

    resp = client.post(ENDPOINT, json={"payment_type": "booking",
                                       "reference_id": booking_id})
    assert resp.status_code == 201
    assert resp.json["amount"] == 500.0
    assert resp.json["client_secret"] == "pi_book_secret"

    with app.app_context():
        p = Payment.query.get(resp.json["payment_id"])
        assert p.status == "pending"
        assert p.payment_type == "booking"
        assert p.reference_id == booking_id
        assert p.gateway_transaction_id == "pi_book"


def test_booking_payment_forbidden_for_other_user(client, app, db_session,
                                                  make_player, sample_club, auth_headers):
    app.config["STRIPE_SECRET_KEY"] = "sk_test_dummy"
    owner_of_booking = make_player(email="owner_b@test.com")
    booking = Booking(user_id=owner_of_booking.id, court_id=sample_club.courts[0].id,
                      booking_date=date(2026, 9, 1), start_time=time(10, 0),
                      end_time=time(11, 0), status="active")
    db_session.add(booking)
    db_session.commit()

    other = make_player(email="intruder@test.com")
    _login(client, auth_headers, other)
    resp = client.post(ENDPOINT, json={"payment_type": "booking",
                                       "reference_id": booking.id})
    assert resp.status_code == 403
    assert resp.json["code"] == "FORBIDDEN"


def test_booking_payment_not_found(client, app, make_player, auth_headers):
    app.config["STRIPE_SECRET_KEY"] = "sk_test_dummy"
    _login(client, auth_headers, make_player(email="nf@test.com"))
    resp = client.post(ENDPOINT, json={"payment_type": "booking", "reference_id": 99999})
    assert resp.status_code == 404
    assert resp.json["code"] == "NOT_FOUND"


# ---------- membership integration ----------

def test_membership_payment_uses_plan_price(client, app, db_session, make_player,
                                            sample_club, auth_headers, monkeypatch):
    app.config["STRIPE_SECRET_KEY"] = "sk_test_dummy"
    plan = MembershipPlan(club_id=sample_club.id, name="Gold",
                          price_monthly=999.0, is_active=True)
    db_session.add(plan)
    db_session.commit()

    def fake_create(**kwargs):
        assert kwargs["amount"] == 99900            # 999.00 -> paise
        return SimpleNamespace(id="pi_mem", client_secret="pi_mem_secret")

    monkeypatch.setattr(stripe.PaymentIntent, "create", staticmethod(fake_create))
    _login(client, auth_headers, make_player(email="mem@test.com"))

    resp = client.post(ENDPOINT, json={"payment_type": "membership",
                                       "reference_id": plan.id})
    assert resp.status_code == 201
    assert resp.json["amount"] == 999.0


# ---------- event integration ----------

def test_event_payment_uses_registration_fee(client, app, db_session, make_player,
                                             sample_club, auth_headers, monkeypatch):
    app.config["STRIPE_SECRET_KEY"] = "sk_test_dummy"
    event = Event(club_id=sample_club.id, created_by=sample_club.owner_id,
                  title="Championship", event_date=date(2026, 9, 1),
                  start_time=time(9, 0), end_time=time(12, 0), registration_fee=200.0)
    db_session.add(event)
    db_session.commit()

    def fake_create(**kwargs):
        assert kwargs["amount"] == 20000
        return SimpleNamespace(id="pi_ev", client_secret="pi_ev_secret")

    monkeypatch.setattr(stripe.PaymentIntent, "create", staticmethod(fake_create))
    _login(client, auth_headers, make_player(email="ev@test.com"))

    resp = client.post(ENDPOINT, json={"payment_type": "event", "reference_id": event.id})
    assert resp.status_code == 201
    assert resp.json["amount"] == 200.0


def test_event_free_is_rejected(client, app, db_session, make_player,
                                sample_club, auth_headers):
    app.config["STRIPE_SECRET_KEY"] = "sk_test_dummy"
    event = Event(club_id=sample_club.id, created_by=sample_club.owner_id,
                  title="Free Meetup", event_date=date(2026, 9, 1),
                  start_time=time(9, 0), end_time=time(12, 0), registration_fee=0.0)
    db_session.add(event)
    db_session.commit()

    _login(client, auth_headers, make_player(email="free@test.com"))
    resp = client.post(ENDPOINT, json={"payment_type": "event", "reference_id": event.id})
    assert resp.status_code == 400
    assert resp.json["code"] == "VALIDATION_ERROR"


# ---------- generic guards ----------

def test_requires_auth(client):
    resp = client.post(ENDPOINT, json={"payment_type": "booking", "reference_id": 1})
    assert resp.status_code == 401


def test_invalid_payment_type(client, app, make_player, auth_headers):
    app.config["STRIPE_SECRET_KEY"] = "sk_test_dummy"
    _login(client, auth_headers, make_player(email="bad@test.com"))
    resp = client.post(ENDPOINT, json={"payment_type": "not-a-type", "reference_id": 1})
    assert resp.status_code == 400
    assert resp.json["code"] == "VALIDATION_ERROR"


def test_not_configured_returns_503(client, make_player, auth_headers):
    # STRIPE_SECRET_KEY intentionally not set
    _login(client, auth_headers, make_player(email="cfg@test.com"))
    resp = client.post(ENDPOINT, json={"payment_type": "booking", "reference_id": 1})
    assert resp.status_code == 503
    assert resp.json["code"] == "CONFIG_ERROR"


# ---------- webhook ----------

def test_webhook_marks_payment_completed(client, app, db_session, make_player, monkeypatch):
    app.config["STRIPE_SECRET_KEY"] = "sk_test_dummy"
    app.config["STRIPE_WEBHOOK_SECRET"] = "whsec_dummy"

    user = make_player(email="hook@test.com")
    payment = Payment(user_id=user.id, amount=500, currency="INR",
                      payment_type="booking", reference_id=1, status="pending",
                      gateway_transaction_id="pi_hook_1")
    db_session.add(payment)
    db_session.commit()
    payment_id = payment.id

    def fake_construct(payload, sig_header, secret):
        return {"type": "payment_intent.succeeded",
                "data": {"object": {"id": "pi_hook_1",
                                    "metadata": {"payment_id": payment_id}}}}

    monkeypatch.setattr(stripe.Webhook, "construct_event", staticmethod(fake_construct))

    resp = client.post("/api/v1/payments/stripe/webhook", data=b"{}",
                       headers={"Stripe-Signature": "t=1,v1=sig"})
    assert resp.status_code == 200
    assert resp.json["type"] == "payment_intent.succeeded"
    with app.app_context():
        assert Payment.query.get(payment_id).status == "completed"


def test_webhook_invalid_signature(client, app, monkeypatch):
    app.config["STRIPE_SECRET_KEY"] = "sk_test_dummy"
    app.config["STRIPE_WEBHOOK_SECRET"] = "whsec_dummy"

    def fake_construct(payload, sig_header, secret):
        raise stripe.SignatureVerificationError("bad sig", sig_header)

    monkeypatch.setattr(stripe.Webhook, "construct_event", staticmethod(fake_construct))
    resp = client.post("/api/v1/payments/stripe/webhook", data=b"{}",
                       headers={"Stripe-Signature": "bad"})
    assert resp.status_code == 400
    assert resp.json["code"] == "INVALID_SIGNATURE"
