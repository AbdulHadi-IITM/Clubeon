import pytest
from datetime import date, time
from app.attendance.models import AttendanceRecord
from app.bookings.models import Booking

def test_check_in_success(client, auth_headers, sample_club, db_session, make_player):
    user = make_player(email="checkin@test.com")
    
    # Create a booking
    booking = Booking(
        user_id=user.id,
        court_id=sample_club.courts[0].id,
        booking_date=date.today(),
        start_time=time(14, 0),
        end_time=time(15, 0)
    )
    db_session.add(booking)
    db_session.commit()
    
    token = auth_headers(user)
    client.set_cookie('access_token_cookie', token)
    
    payload = {
        "booking_id": booking.id
    }
    
    response = client.post('/api/v1/attendance/check-in', json=payload)
    assert response.status_code == 201
    assert 'attendance_id' in response.json

def test_check_in_conflict(client, auth_headers, sample_club, db_session, make_player):
    user = make_player(email="checkin2@test.com")
    
    booking = Booking(
        user_id=user.id,
        court_id=sample_club.courts[0].id,
        booking_date=date.today(),
        start_time=time(15, 0),
        end_time=time(16, 0)
    )
    db_session.add(booking)
    db_session.commit()
    
    # Already checked in
    record = AttendanceRecord(
        user_id=user.id,
        booking_id=booking.id
    )
    db_session.add(record)
    db_session.commit()
    
    token = auth_headers(user)
    client.set_cookie('access_token_cookie', token)
    
    response = client.post('/api/v1/attendance/check-in', json={"booking_id": booking.id})
    assert response.status_code == 409
    assert response.json['code'] == 'CONFLICT'

def test_check_out_success(client, auth_headers, sample_club, db_session, make_player):
    user = make_player(email="checkout@test.com")
    
    record = AttendanceRecord(
        user_id=user.id
    )
    db_session.add(record)
    db_session.commit()
    
    token = auth_headers(user)
    client.set_cookie('access_token_cookie', token)
    
    response = client.post('/api/v1/attendance/check-out', json={"attendance_id": record.id})
    assert response.status_code == 200
    
    db_session.refresh(record)
    assert record.check_out_at is not None

def test_admin_view_attendance(client, auth_headers, sample_club, db_session, make_player):
    owner = sample_club.owner
    token = auth_headers(owner)
    client.set_cookie('access_token_cookie', token)
    
    # Create booking for club and an attendance record
    user = make_player(email="view@test.com")
    booking = Booking(
        user_id=user.id,
        court_id=sample_club.courts[0].id,
        booking_date=date.today(),
        start_time=time(16, 0),
        end_time=time(17, 0)
    )
    db_session.add(booking)
    db_session.commit()
    
    record = AttendanceRecord(
        user_id=user.id,
        booking_id=booking.id
    )
    db_session.add(record)
    db_session.commit()
    
    response = client.get(f'/api/v1/attendance/admin/view?club_id={sample_club.id}')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['user_email'] == 'view@test.com'
