"""
Tests for the analytics endpoints that back the Admin / Member / Staff
dashboards, and for club-booking visibility.

Before this feature the dashboards displayed hard-coded numbers and there was
no endpoint for an owner or front-desk user to see bookings at all
(GET /bookings is player-only).
"""
from datetime import date, time, timedelta

from flask_jwt_extended import create_access_token

from app.clubs.models import Club, Court
from app.bookings.models import Booking
from app.memberships.models import MembershipPlan, Membership
from app.payments.models import Payment

ADMIN = "/api/v1/analytics/admin"
MEMBER = "/api/v1/analytics/member"
STAFF = "/api/v1/analytics/staff"
CLUB_BOOKINGS = "/api/v1/bookings/club"


def _login(client, app, user):
    with app.app_context():
        token = create_access_token(identity=str(user.id),
                                    additional_claims={"role": user.role},
                                    expires_delta=timedelta(hours=1))
    client.set_cookie("access_token_cookie", token)


def _club_with_courts(db_session, owner):
    club = Club(name="Ace Sports Club", address="12 Baseline Rd",
                owner_id=owner.id, open_time="06:00", close_time="22:00",
                slot_duration_minutes=60)
    db_session.add(club)
    db_session.commit()
    c1 = Court(club_id=club.id, name="Court 1", is_active=True)
    c2 = Court(club_id=club.id, name="Court 2", is_active=True)
    db_session.add_all([c1, c2])
    db_session.commit()
    return club, c1, c2


# ---------------- admin analytics ----------------
def test_admin_analytics_uses_real_data(client, app, db_session, make_player):
    owner = make_player(email="an_owner@test.com", role="owner")
    player = make_player(email="an_player@test.com")
    club, court1, _ = _club_with_courts(db_session, owner)

    today = date.today()
    db_session.add_all([
        Booking(user_id=player.id, court_id=court1.id, booking_date=today,
                start_time=time(10, 0), end_time=time(11, 0), status="active"),
        Booking(user_id=player.id, court_id=court1.id, booking_date=today,
                start_time=time(12, 0), end_time=time(13, 0), status="released"),
    ])
    db_session.add(Payment(user_id=player.id, amount=500.0, currency="INR",
                           payment_type="booking", reference_id=1,
                           status="completed"))
    db_session.commit()

    _login(client, app, owner)
    r = client.get(ADMIN)
    assert r.status_code == 200
    d = r.json
    assert d["club"]["name"] == "Ace Sports Club"
    assert d["bookings"]["total"] == 2
    assert d["bookings"]["active"] == 1
    assert d["bookings"]["released"] == 1
    assert d["revenue"]["total"] == 500.0
    assert d["courts"]["total"] == 2
    assert len(d["courts"]["breakdown"]) == 2
    assert isinstance(d["trend"], list)


def test_admin_analytics_is_owner_only(client, app, make_player):
    player = make_player(email="an_notowner@test.com")
    _login(client, app, player)
    r = client.get(ADMIN)
    assert r.status_code == 403
    assert r.json["code"] == "FORBIDDEN"


def test_admin_analytics_requires_auth(client):
    assert client.get(ADMIN).status_code == 401


def test_admin_analytics_without_club(client, app, make_player):
    owner = make_player(email="an_noclub@test.com", role="owner")
    _login(client, app, owner)
    r = client.get(ADMIN)
    assert r.status_code == 404


def test_admin_analytics_rejects_bad_window(client, app, db_session, make_player):
    owner = make_player(email="an_badwin@test.com", role="owner")
    _club_with_courts(db_session, owner)
    _login(client, app, owner)
    assert client.get(f"{ADMIN}?days=0").status_code == 400
    assert client.get(f"{ADMIN}?days=999").status_code == 400


def test_admin_analytics_is_scoped_to_own_club(client, app, db_session, make_player):
    """An owner must never see another club's bookings."""
    owner_a = make_player(email="an_a@test.com", role="owner")
    owner_b = make_player(email="an_b@test.com", role="owner")
    player = make_player(email="an_p2@test.com")
    club_a, court_a, _ = _club_with_courts(db_session, owner_a)

    club_b = Club(name="Other Club", address="x", owner_id=owner_b.id,
                  open_time="06:00", close_time="22:00", slot_duration_minutes=60)
    db_session.add(club_b)
    db_session.commit()
    court_b = Court(club_id=club_b.id, name="B1", is_active=True)
    db_session.add(court_b)
    db_session.commit()
    db_session.add(Booking(user_id=player.id, court_id=court_b.id,
                           booking_date=date.today(), start_time=time(9, 0),
                           end_time=time(10, 0), status="active"))
    db_session.commit()

    _login(client, app, owner_a)
    assert client.get(ADMIN).json["bookings"]["total"] == 0


# ---------------- member analytics ----------------
def test_member_analytics(client, app, db_session, make_player):
    owner = make_player(email="mem_owner@test.com", role="owner")
    player = make_player(email="mem_p@test.com")
    club, court1, _ = _club_with_courts(db_session, owner)

    future = date.today() + timedelta(days=3)
    plan = MembershipPlan(club_id=club.id, name="Gold", duration_months=1, price=999.0,
                          is_active=True)
    db_session.add(plan)
    db_session.commit()
    db_session.add_all([
        Booking(user_id=player.id, court_id=court1.id, booking_date=future,
                start_time=time(10, 0), end_time=time(11, 0), status="active"),
        Membership(user_id=player.id, plan_id=plan.id, club_id=club.id,
                   status="active", start_date=date.today(),
                   end_date=date.today() + timedelta(days=30)),
        Payment(user_id=player.id, amount=999.0, currency="INR",
                payment_type="membership", reference_id=plan.id,
                status="completed"),
    ])
    db_session.commit()

    _login(client, app, player)
    r = client.get(MEMBER)
    assert r.status_code == 200
    d = r.json
    assert d["bookings"]["total"] == 1
    assert d["bookings"]["upcoming"] == 1
    assert d["membership"]["plan_name"] == "Gold"
    assert d["membership"]["days_left"] >= 0
    assert d["total_spend"] == 999.0
    assert d["next_booking"]["court_name"] == "Court 1"


def test_member_analytics_empty_state(client, app, make_player):
    player = make_player(email="mem_empty@test.com")
    _login(client, app, player)
    d = client.get(MEMBER).json
    assert d["bookings"]["total"] == 0
    assert d["membership"] is None
    assert d["next_booking"] is None
    assert d["total_spend"] == 0


def test_member_analytics_requires_auth(client):
    assert client.get(MEMBER).status_code == 401


# ---------------- staff analytics ----------------
def test_staff_analytics(client, app, db_session, make_player):
    owner = make_player(email="st_owner@test.com", role="owner")
    staff = make_player(email="st_staff@test.com", role="front-desk")
    player = make_player(email="st_p@test.com")
    club, court1, _ = _club_with_courts(db_session, owner)

    db_session.add(Booking(user_id=player.id, court_id=court1.id,
                           booking_date=date.today(), start_time=time(10, 0),
                           end_time=time(11, 0), status="active"))
    db_session.commit()

    _login(client, app, staff)
    r = client.get(STAFF)
    assert r.status_code == 200
    d = r.json
    assert d["today"]["total_bookings"] == 1
    assert d["today"]["active"] == 1
    assert d["bookings"][0]["member"] == "Player"


def test_staff_analytics_forbidden_for_player(client, app, make_player):
    player = make_player(email="st_player@test.com")
    _login(client, app, player)
    assert client.get(STAFF).status_code == 403


# ---------------- club bookings visibility (the bug) ----------------
def test_owner_can_see_club_bookings(client, app, db_session, make_player):
    owner = make_player(email="cb_owner@test.com", role="owner")
    player = make_player(email="cb_p@test.com")
    club, court1, _ = _club_with_courts(db_session, owner)
    db_session.add(Booking(user_id=player.id, court_id=court1.id,
                           booking_date=date.today(), start_time=time(10, 0),
                           end_time=time(11, 0), status="active"))
    db_session.commit()

    _login(client, app, owner)
    r = client.get(CLUB_BOOKINGS)
    assert r.status_code == 200, "owners could not see bookings"
    assert r.json["count"] == 1
    b = r.json["bookings"][0]
    assert b["member_name"] == "Player"
    assert b["court_name"] == "Court 1"


def test_front_desk_can_see_club_bookings(client, app, db_session, make_player):
    owner = make_player(email="cb_owner2@test.com", role="owner")
    staff = make_player(email="cb_staff@test.com", role="front-desk")
    player = make_player(email="cb_p2@test.com")
    club, court1, _ = _club_with_courts(db_session, owner)
    db_session.add(Booking(user_id=player.id, court_id=court1.id,
                           booking_date=date.today(), start_time=time(14, 0),
                           end_time=time(15, 0), status="active"))
    db_session.commit()

    _login(client, app, staff)
    r = client.get(CLUB_BOOKINGS)
    assert r.status_code == 200
    assert r.json["count"] == 1


def test_club_bookings_filters(client, app, db_session, make_player):
    owner = make_player(email="cb_filter@test.com", role="owner")
    player = make_player(email="cb_pf@test.com")
    club, court1, court2 = _club_with_courts(db_session, owner)
    today = date.today()
    db_session.add_all([
        Booking(user_id=player.id, court_id=court1.id, booking_date=today,
                start_time=time(10, 0), end_time=time(11, 0), status="active"),
        Booking(user_id=player.id, court_id=court2.id, booking_date=today,
                start_time=time(11, 0), end_time=time(12, 0), status="released"),
    ])
    db_session.commit()

    _login(client, app, owner)
    assert client.get(f"{CLUB_BOOKINGS}?status=active").json["count"] == 1
    assert client.get(f"{CLUB_BOOKINGS}?court_id={court1.id}").json["count"] == 1
    assert client.get(f"{CLUB_BOOKINGS}?date={today.isoformat()}").json["count"] == 2
    assert client.get(f"{CLUB_BOOKINGS}?date=not-a-date").status_code == 400


def test_club_bookings_forbidden_for_player(client, app, make_player):
    player = make_player(email="cb_player@test.com")
    _login(client, app, player)
    assert client.get(CLUB_BOOKINGS).status_code == 403


def test_owner_cannot_see_other_clubs_bookings(client, app, db_session, make_player):
    owner_a = make_player(email="cb_a@test.com", role="owner")
    owner_b = make_player(email="cb_b@test.com", role="owner")
    player = make_player(email="cb_p3@test.com")
    _club_with_courts(db_session, owner_a)

    club_b = Club(name="Club B", address="y", owner_id=owner_b.id,
                  open_time="06:00", close_time="22:00", slot_duration_minutes=60)
    db_session.add(club_b)
    db_session.commit()
    court_b = Court(club_id=club_b.id, name="B1", is_active=True)
    db_session.add(court_b)
    db_session.commit()
    db_session.add(Booking(user_id=player.id, court_id=court_b.id,
                           booking_date=date.today(), start_time=time(9, 0),
                           end_time=time(10, 0), status="active"))
    db_session.commit()

    _login(client, app, owner_a)
    assert client.get(CLUB_BOOKINGS).json["count"] == 0
