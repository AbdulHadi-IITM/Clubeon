import pytest
from datetime import date, time, timedelta
from app.bookings.models import Booking, CourtBlock
from app.auth.models import User

def test_override_booking_success(client, auth_headers, sample_club, db_session, make_player):
    # Create booking for a normal player
    player = make_player(email="player_admin@test.com")
    court_id = sample_club.courts[0].id
    
    booking = Booking(
        user_id=player.id,
        court_id=court_id,
        booking_date=date.today(),
        start_time=time(14, 0),
        end_time=time(15, 0)
    )
    db_session.add(booking)
    db_session.commit()
    
    # Authenticate as the club owner
    owner = sample_club.owner
    token = auth_headers(owner)
    client.set_cookie('access_token_cookie', token)
    
    response = client.post(f'/api/v1/admin/bookings/{booking.id}/override')
    assert response.status_code == 200
    assert response.json['message'] == 'Booking overridden successfully'
    
    db_session.refresh(booking)
    assert booking.status == 'overridden'

def test_override_booking_forbidden(client, auth_headers, sample_club, db_session, make_player):
    player = make_player(email="player_admin2@test.com")
    court_id = sample_club.courts[0].id
    
    booking = Booking(
        user_id=player.id,
        court_id=court_id,
        booking_date=date.today(),
        start_time=time(14, 0),
        end_time=time(15, 0)
    )
    db_session.add(booking)
    db_session.commit()
    
    # Authenticate as some other owner
    other_owner = make_player(email="other_owner@test.com", role="owner")
    token = auth_headers(other_owner)
    client.set_cookie('access_token_cookie', token)
    
    response = client.post(f'/api/v1/admin/bookings/{booking.id}/override')
    assert response.status_code == 403
    assert response.json['code'] == 'FORBIDDEN'

def test_block_court_success(client, auth_headers, sample_club, db_session, make_player):
    owner = sample_club.owner
    token = auth_headers(owner)
    client.set_cookie('access_token_cookie', token)
    
    court_id = sample_club.courts[0].id
    target_date = date.today()
    
    # Add an active booking in the block range to see if it gets overridden
    player = make_player(email="victim@test.com")
    booking = Booking(
        user_id=player.id,
        court_id=court_id,
        booking_date=target_date,
        start_time=time(10, 0),
        end_time=time(11, 0)
    )
    db_session.add(booking)
    db_session.commit()
    
    payload = {
        "court_id": court_id,
        "start_date": target_date.strftime("%Y-%m-%d"),
        "end_date": target_date.strftime("%Y-%m-%d"),
        "title": "Maintenance"
    }
    
    response = client.post('/api/v1/admin/courts/block', json=payload)
    assert response.status_code == 201
    assert 'block_id' in response.json
    
    # Check if booking was overridden
    db_session.refresh(booking)
    assert booking.status == 'overridden'
    
    # Check if CourtBlock was created
    block = CourtBlock.query.get(response.json['block_id'])
    assert block is not None
    assert block.title == "Maintenance"
