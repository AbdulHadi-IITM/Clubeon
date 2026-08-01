import pytest
from app.auth.models import User

def test_register_success(client, db_session):
    payload = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "password": "Password123!",
        "role": "player"
    }
    response = client.post('/api/v1/auth/register', json=payload)
    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully'
    assert 'user' in response.json
    
    # Verify DB
    user = User.query.filter_by(email="jane@example.com").first()
    assert user is not None
    assert user.name == "Jane Doe"
    
    # Verify cookie is set
    cookies = response.headers.get_all('Set-Cookie')
    assert any('access_token_cookie' in c for c in cookies)

def test_register_duplicate_email(client, make_player):
    make_player(email="duplicate@example.com")
    payload = {
        "name": "Another Person",
        "email": "duplicate@example.com",
        "password": "Password123!",
        "role": "player"
    }
    response = client.post('/api/v1/auth/register', json=payload)
    assert response.status_code == 409
    assert response.json['code'] == 'CONFLICT'

def test_register_invalid_role(client):
    payload = {
        "name": "Jane Doe",
        "email": "jane2@example.com",
        "password": "Password123!",
        "role": "superadmin"
    }
    response = client.post('/api/v1/auth/register', json=payload)
    assert response.status_code == 400
    assert response.json['code'] == 'VALIDATION_ERROR'

def test_login_success(client, make_player):
    make_player(email="login@example.com", password="Password123!")
    payload = {
        "email": "login@example.com",
        "password": "Password123!"
    }
    response = client.post('/api/v1/auth/login', json=payload)
    assert response.status_code == 200
    assert response.json['message'] == 'Login successful'
    
    cookies = response.headers.get_all('Set-Cookie')
    assert any('access_token_cookie' in c for c in cookies)

def test_login_wrong_password(client, make_player):
    make_player(email="login2@example.com", password="Password123!")
    payload = {
        "email": "login2@example.com",
        "password": "WrongPassword!"
    }
    response = client.post('/api/v1/auth/login', json=payload)
    assert response.status_code == 401
    assert response.json['code'] == 'UNAUTHORIZED'

def test_me_authenticated(client, auth_headers):
    token = auth_headers()
    client.set_cookie('access_token_cookie', token)
    response = client.get('/api/v1/auth/me')
    assert response.status_code == 200
    assert 'user' in response.json

def test_me_unauthenticated(client):
    response = client.get('/api/v1/auth/me')
    assert response.status_code == 401

def test_logout(client, auth_headers):
    token = auth_headers()
    client.set_cookie('access_token_cookie', token)
    response = client.post('/api/v1/auth/logout')
    assert response.status_code == 200
    
    # Cookie should be cleared (max-age 0 or empty)
    cookies = response.headers.get_all('Set-Cookie')
    assert any('access_token_cookie=' in c for c in cookies)
