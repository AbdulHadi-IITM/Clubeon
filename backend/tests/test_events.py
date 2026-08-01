import pytest
from datetime import date, time
from app.events.models import Event, EventRegistration

def test_create_event_success(client, auth_headers, sample_club, db_session):
    owner = sample_club.owner
    token = auth_headers(owner)
    client.set_cookie('access_token_cookie', token)
    
    payload = {
        "club_id": sample_club.id,
        "title": "Summer Tournament",
        "description": "Annual summer tennis tournament",
        "event_date": "2026-08-15",
        "start_time": "09:00",
        "end_time": "17:00",
        "max_attendees": 32,
        "registration_fee": 50.0
    }
    
    response = client.post('/api/v1/events', json=payload)
    assert response.status_code == 201
    assert 'event_id' in response.json

def test_create_event_forbidden(client, auth_headers, sample_club, db_session, make_player):
    player = make_player(email="not_owner@test.com")
    token = auth_headers(player)
    client.set_cookie('access_token_cookie', token)
    
    payload = {
        "club_id": sample_club.id,
        "title": "Summer Tournament",
        "event_date": "2026-08-15",
        "start_time": "09:00",
        "end_time": "17:00"
    }
    
    response = client.post('/api/v1/events', json=payload)
    assert response.status_code == 403

def test_get_events(client, sample_club, db_session):
    event = Event(
        club_id=sample_club.id,
        created_by=sample_club.owner_id,
        title="Test Event",
        event_date=date(2026, 9, 1),
        start_time=time(10, 0),
        end_time=time(12, 0)
    )
    db_session.add(event)
    db_session.commit()
    
    response = client.get('/api/v1/events')
    assert response.status_code == 200
    assert len(response.json) >= 1
    assert response.json[0]['title'] == 'Test Event'

def test_register_event_success(client, auth_headers, sample_club, db_session, make_player):
    event = Event(
        club_id=sample_club.id,
        created_by=sample_club.owner_id,
        title="Register Event",
        event_date=date(2026, 9, 1),
        start_time=time(10, 0),
        end_time=time(12, 0)
    )
    db_session.add(event)
    db_session.commit()
    
    user = make_player(email="event_reg@test.com")
    token = auth_headers(user)
    client.set_cookie('access_token_cookie', token)
    
    response = client.post(f'/api/v1/events/{event.id}/register')
    assert response.status_code == 200
    assert 'registration_id' in response.json

def test_register_event_full(client, auth_headers, sample_club, db_session, make_player):
    event = Event(
        club_id=sample_club.id,
        created_by=sample_club.owner_id,
        title="Full Event",
        event_date=date(2026, 9, 1),
        start_time=time(10, 0),
        end_time=time(12, 0),
        max_attendees=1
    )
    db_session.add(event)
    db_session.commit()
    
    user1 = make_player(email="reg1@test.com")
    reg1 = EventRegistration(event_id=event.id, user_id=user1.id, status='registered')
    db_session.add(reg1)
    db_session.commit()
    
    user2 = make_player(email="reg2@test.com")
    token = auth_headers(user2)
    client.set_cookie('access_token_cookie', token)
    
    response = client.post(f'/api/v1/events/{event.id}/register')
    assert response.status_code == 409
    assert response.json['code'] == 'CONFLICT'

def test_cancel_event_registration(client, auth_headers, sample_club, db_session, make_player):
    event = Event(
        club_id=sample_club.id,
        created_by=sample_club.owner_id,
        title="Cancel Event",
        event_date=date(2026, 9, 1),
        start_time=time(10, 0),
        end_time=time(12, 0)
    )
    db_session.add(event)
    db_session.commit()
    
    user = make_player(email="cancel_reg@test.com")
    reg = EventRegistration(event_id=event.id, user_id=user.id, status='registered')
    db_session.add(reg)
    db_session.commit()
    
    token = auth_headers(user)
    client.set_cookie('access_token_cookie', token)
    
    response = client.post(f'/api/v1/events/{event.id}/cancel')
    assert response.status_code == 200
    
    db_session.refresh(reg)
    assert reg.status == 'cancelled'
