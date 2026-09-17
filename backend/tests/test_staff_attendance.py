"""
Tests for the front-desk attendance screens.

/staff/attendance/expected backs the "Today's expected members" list; it was the
one endpoint the merged staff UI called that the backend did not implement.
"""
from datetime import date, time, timedelta

from flask_jwt_extended import create_access_token

from app.bookings.models import Booking
from app.attendance.models import AttendanceRecord

EXPECTED = "/api/v1/staff/attendance/expected"


def _login(client, app, user):
    with app.app_context():
        token = create_access_token(identity=str(user.id),
                                    additional_claims={"role": user.role},
                                    expires_delta=timedelta(hours=1))
    client.set_cookie("access_token_cookie", token)


def _booking(db_session, user, court, start=time(10, 0), end=time(11, 0), day=None):
    b = Booking(user_id=user.id, court_id=court.id,
                booking_date=day or date.today(),
                start_time=start, end_time=end, status="active")
    db_session.add(b)
    db_session.commit()
    return b


def test_expected_lists_todays_bookings(client, app, db_session, make_player, sample_club):
    staff = make_player(email="fd1@test.com", role="front-desk")
    player = make_player(email="p1@test.com")
    booking = _booking(db_session, player, sample_club.courts[0])

    _login(client, app, staff)
    r = client.get(EXPECTED, query_string={"club_id": sample_club.id})
    assert r.status_code == 200
    assert len(r.json) == 1
    row = r.json[0]
    assert row["id"] == booking.id
    assert row["user_name"] == player.name
    assert row["court_name"] == sample_club.courts[0].name
    assert row["attendance_status"] == "expected"


def test_status_tracks_check_in_and_check_out(client, app, db_session, make_player, sample_club):
    staff = make_player(email="fd2@test.com", role="front-desk")
    player = make_player(email="p2@test.com")
    booking = _booking(db_session, player, sample_club.courts[0])
    _login(client, app, staff)

    client.post("/api/v1/staff/attendance/check-in", json={"booking_id": booking.id})
    assert client.get(EXPECTED, query_string={"club_id": sample_club.id}
                      ).json[0]["attendance_status"] == "checked_in"

    with app.app_context():
        record = AttendanceRecord.query.filter_by(booking_id=booking.id).first()
    client.post(f"/api/v1/staff/attendance/{record.id}/check-out")
    assert client.get(EXPECTED, query_string={"club_id": sample_club.id}
                      ).json[0]["attendance_status"] == "checked_out"


def test_other_days_are_excluded(client, app, db_session, make_player, sample_club):
    staff = make_player(email="fd3@test.com", role="front-desk")
    player = make_player(email="p3@test.com")
    _booking(db_session, player, sample_club.courts[0],
             day=date.today() + timedelta(days=1))

    _login(client, app, staff)
    assert client.get(EXPECTED, query_string={"club_id": sample_club.id}).json == []


def test_explicit_date_is_honoured(client, app, db_session, make_player, sample_club):
    staff = make_player(email="fd4@test.com", role="front-desk")
    player = make_player(email="p4@test.com")
    tomorrow = date.today() + timedelta(days=1)
    _booking(db_session, player, sample_club.courts[0], day=tomorrow)

    _login(client, app, staff)
    r = client.get(EXPECTED, query_string={"club_id": sample_club.id,
                                           "date": tomorrow.isoformat()})
    assert len(r.json) == 1


def test_bad_date_is_rejected(client, app, make_player, sample_club):
    staff = make_player(email="fd5@test.com", role="front-desk")
    _login(client, app, staff)
    r = client.get(EXPECTED, query_string={"club_id": sample_club.id, "date": "nope"})
    assert r.status_code == 400


def test_club_id_is_required(client, app, make_player):
    staff = make_player(email="fd6@test.com", role="front-desk")
    _login(client, app, staff)
    assert client.get(EXPECTED).status_code == 400


def test_players_cannot_read_the_front_desk_list(client, app, make_player, sample_club):
    player = make_player(email="p5@test.com")
    _login(client, app, player)
    assert client.get(EXPECTED, query_string={"club_id": sample_club.id}).status_code == 403


def test_requires_authentication(client, sample_club):
    assert client.get(EXPECTED, query_string={"club_id": sample_club.id}).status_code == 401
