import pytest
from app.notifications.models import Notification

def test_get_my_notifications(client, auth_headers, db_session, make_player):
    user = make_player(email="notif@test.com")
    
    n1 = Notification(user_id=user.id, title="Test 1", body="Body 1", type="system")
    n2 = Notification(user_id=user.id, title="Test 2", body="Body 2", type="alert", is_read=True)
    db_session.add_all([n1, n2])
    db_session.commit()
    
    token = auth_headers(user)
    client.set_cookie('access_token_cookie', token)
    
    response = client.get('/api/v1/notifications')
    assert response.status_code == 200
    assert len(response.json) == 2

def test_mark_read(client, auth_headers, db_session, make_player):
    user = make_player(email="mark@test.com")
    
    n1 = Notification(user_id=user.id, title="Test 1", body="Body 1", type="system")
    db_session.add(n1)
    db_session.commit()
    
    token = auth_headers(user)
    client.set_cookie('access_token_cookie', token)
    
    response = client.post(f'/api/v1/notifications/{n1.id}/read')
    assert response.status_code == 200
    
    db_session.refresh(n1)
    assert n1.is_read is True

def test_mark_all_read(client, auth_headers, db_session, make_player):
    user = make_player(email="markall@test.com")
    
    n1 = Notification(user_id=user.id, title="Test 1", body="Body 1", type="system")
    n2 = Notification(user_id=user.id, title="Test 2", body="Body 2", type="system")
    db_session.add_all([n1, n2])
    db_session.commit()
    
    token = auth_headers(user)
    client.set_cookie('access_token_cookie', token)
    
    response = client.post('/api/v1/notifications/read-all')
    assert response.status_code == 200
    
    db_session.refresh(n1)
    db_session.refresh(n2)
    assert n1.is_read is True
    assert n2.is_read is True
