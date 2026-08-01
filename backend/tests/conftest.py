import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import create_app
from app.extensions import db
from app.auth.models import User
from flask_jwt_extended import create_access_token
from datetime import timedelta

class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test-secret'
    JWT_SECRET_KEY = 'test-jwt-secret'
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_COOKIE_CSRF_PROTECT = False

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db.session

@pytest.fixture
def make_player(db_session):
    def _make_player(email="player@example.com", name="Player", password="Password123!", role='player'):
        user = User(name=name, email=email, role=role)
        user.set_password(password)
        db_session.add(user)
        db_session.commit()
        return user
    return _make_player

@pytest.fixture
def auth_headers(app, make_player):
    def _auth_headers(user=None):
        if user is None:
            user = make_player()
        with app.app_context():
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={"role": user.role},
                expires_delta=timedelta(hours=24)
            )
        # Instead of headers, we need to set the cookie in the client
        return access_token
    return _auth_headers

from app.clubs.models import Club, Court
@pytest.fixture
def sample_club(db_session, make_player):
    owner = make_player(email="owner_conftest@example.com", role="owner")
    club = Club(name="Ace Sports Club", address="123 Road", owner_id=owner.id, open_time="06:00", close_time="22:00", slot_duration_minutes=60)
    db_session.add(club)
    db_session.commit()
    
    court1 = Court(club_id=club.id, name="Court 1 - Clay", is_active=True)
    court2 = Court(club_id=club.id, name="Court 2 - Hard", is_active=False)
    db_session.add_all([court1, court2])
    db_session.commit()
    
    return club
