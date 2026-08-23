import pytest
from datetime import date, time, timedelta, datetime
from app.bookings.models import Booking

def test_create_booking_success(client, auth_headers, sample_club, db_session):
    token = auth_headers()
    client.set_cookie('access_token_cookie', token)
    
    court_id = sample_club.courts[0].id
    future_start = datetime.combine(
        date.today() + timedelta(days=1),
        time(12, 0),
    )
    future_end = future_start + timedelta(hours=1)

    payload = {
        "court_id": court_id,
        "booking_date": future_start.strftime("%Y-%m-%d"),
        "start_time": future_start.strftime("%H:%M"),
        "end_time": future_end.strftime("%H:%M"),
    }
    
    response = client.post('/api/v1/bookings', json=payload)
    assert response.status_code == 201
    assert 'booking_id' in response.json

def test_create_booking_rejects_past_slot(client, auth_headers, sample_club, db_session):
    token = auth_headers()
    client.set_cookie('access_token_cookie', token)

    court_id = sample_club.courts[0].id
    past_start = (datetime.now() - timedelta(hours=2)).replace(second=0, microsecond=0)
    past_end = past_start + timedelta(hours=1)

    payload = {
        "court_id": court_id,
        "booking_date": past_start.strftime("%Y-%m-%d"),
        "start_time": past_start.strftime("%H:%M"),
        "end_time": past_end.strftime("%H:%M"),
    }

    response = client.post('/api/v1/bookings', json=payload)

    assert response.status_code == 400
    assert response.json['code'] == 'VALIDATION_ERROR'
    assert 'already passed' in response.json['message']


def test_create_booking_conflict(client, auth_headers, sample_club, db_session, make_player):
    # Setup an existing booking
    player1 = make_player(email="player1@test.com")
    court_id = sample_club.courts[0].id
    future_date = date.today() + timedelta(days=2)
    
    booking = Booking(
        user_id=player1.id,
        court_id=court_id,
        booking_date=future_date,
        start_time=time(14, 0),
        end_time=time(15, 0)
    )
    db_session.add(booking)
    db_session.commit()
    
    # Try to book same slot with player2
    token = auth_headers() # player2 since make_player in conftest creates a new one? 
    # Actually auth_headers creates a default user if none passed
    client.set_cookie('access_token_cookie', token)
    
    payload = {
        "court_id": court_id,
        "booking_date": future_date.strftime("%Y-%m-%d"),
        "start_time": "14:30",
        "end_time": "15:30"
    }
    
    response = client.post('/api/v1/bookings', json=payload)
    assert response.status_code == 409
    assert response.json['code'] == 'CONFLICT'

def test_get_my_bookings(client, auth_headers, sample_club, db_session, make_player):
    # We pass user to auth_headers to control the identity
    user = make_player(email="my_bookings@test.com")
    token = auth_headers(user)
    client.set_cookie('access_token_cookie', token)
    
    # Create booking for this user
    court_id = sample_club.courts[0].id
    booking = Booking(
        user_id=user.id,
        court_id=court_id,
        booking_date=date.today(),
        start_time=time(16, 0),
        end_time=time(17, 0)
    )
    db_session.add(booking)
    db_session.commit()
    
    response = client.get('/api/v1/bookings')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['status'] == 'active'
    assert response.json[0]['club_name'] == 'Ace Sports Club'

def test_release_booking_success(client, auth_headers, sample_club, db_session, make_player):
    user = make_player(email="release@test.com")
    token = auth_headers(user)
    client.set_cookie('access_token_cookie', token)
    
    booking = Booking(
        user_id=user.id,
        court_id=sample_club.courts[0].id,
        booking_date=date.today(),
        start_time=time(18, 0),
        end_time=time(19, 0)
    )
    db_session.add(booking)
    db_session.commit()
    
    response = client.post(f'/api/v1/bookings/{booking.id}/release')
    assert response.status_code == 200
    assert response.json['message'] == 'Booking released successfully'
    
    db_session.refresh(booking)
    assert booking.status == 'released'

def test_release_booking_forbidden(client, auth_headers, sample_club, db_session, make_player):
    user1 = make_player(email="user1@test.com")
    user2 = make_player(email="user2@test.com")
    
    booking = Booking(
        user_id=user1.id,
        court_id=sample_club.courts[0].id,
        booking_date=date.today(),
        start_time=time(19, 0),
        end_time=time(20, 0)
    )
    db_session.add(booking)
    db_session.commit()
    
    # Authenticate as user2
    token = auth_headers(user2)
    client.set_cookie('access_token_cookie', token)
    
    response = client.post(f'/api/v1/bookings/{booking.id}/release')
    assert response.status_code == 403
    assert response.json['code'] == 'FORBIDDEN'
