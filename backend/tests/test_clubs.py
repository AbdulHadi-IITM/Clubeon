import pytest
from app.clubs.models import Club, Court

# --- CLUB CRUD TESTS ---
def test_create_club_success(client, db_session, make_player, auth_headers):
    """Owner successfully creates a new club."""
    owner = make_player(email="owner.create@test.com", role="owner")
    token = auth_headers(owner)
    client.set_cookie('access_token_cookie', token)

    payload = {
        "name": "Apex Sports Arena",
        "address": "123 Champion Street",
        "open_time": "06:00",
        "close_time": "22:00",
        "slot_duration_minutes": 60
    }
    response = client.post('/api/v1/clubs', json=payload)

    assert response.status_code == 201
    assert response.json['message'] == 'Club created successfully'
    club = Club.query.filter_by(name="Apex Sports Arena").first()
    assert club is not None
    assert club.owner_id == owner.id
    assert club.open_time == "06:00"
    assert club.close_time == "22:00"
    assert club.slot_duration_minutes == 60

def test_create_club_duplicate(client, db_session, make_player, auth_headers, sample_club):
    """Owner cannot create a second club (409 CONFLICT)."""
    owner = sample_club.owner
    token = auth_headers(owner)
    client.set_cookie('access_token_cookie', token)

    payload = {"name": "Second Club", "address": "456 Street"}
    response = client.post('/api/v1/clubs', json=payload)
    assert response.status_code == 409
    assert response.json['code'] == 'CONFLICT'

def test_update_club_success(client, db_session, make_player, auth_headers, sample_club):
    """Owner updates club details and operating hours."""
    owner = sample_club.owner
    token = auth_headers(owner)
    client.set_cookie('access_token_cookie', token)

    payload = {
        "name": "Updated Club Name",
        "address": "456 New Address",
        "open_time": "07:00",
        "close_time": "23:00",
        "slot_duration_minutes": 30
    }
    response = client.put(f'/api/v1/clubs/{sample_club.id}', json=payload)
    assert response.status_code == 200
    assert response.json['message'] == 'Club settings updated successfully'

    db_session.refresh(sample_club)
    assert sample_club.name == "Updated Club Name"
    assert sample_club.address == "456 New Address"
    assert sample_club.open_time == "07:00"
    assert sample_club.close_time == "23:00"
    assert sample_club.slot_duration_minutes == 30

def test_update_club_forbidden(client, db_session, make_player, auth_headers, sample_club):
    """Another owner cannot update this club (403 FORBIDDEN)."""
    other_owner = make_player(email="other.owner@test.com", role="owner")
    token = auth_headers(other_owner)
    client.set_cookie('access_token_cookie', token)

    response = client.put(f'/api/v1/clubs/{sample_club.id}', json={"name": "Hack"})
    assert response.status_code == 403
    assert response.json['code'] == 'FORBIDDEN'


# --- COURT CRUD TESTS ---
def test_create_court_first_time(client, db_session, make_player, auth_headers):
    """Owner creates a court + club simultaneously when they don't have a club yet."""
    owner = make_player(email="owner.firstcourt@test.com", role="owner")
    token = auth_headers(owner)
    client.set_cookie('access_token_cookie', token)

    payload = {
        "court_name": "Squash Court 1",
        "club_name": "My New Club",
        "club_address": "789 Avenue"
    }
    response = client.post('/api/v1/clubs/courts', json=payload)
    assert response.status_code == 201
    assert response.json['message'] == 'Court created'

    court = Court.query.filter_by(name="Squash Court 1").first()
    assert court is not None
    club = Club.query.filter_by(name="My New Club").first()
    assert club is not None
    assert court.club_id == club.id
    assert club.owner_id == owner.id
    # Verify default hours are set automatically
    assert club.open_time == "06:00"
    assert club.close_time == "22:00"
    assert club.slot_duration_minutes == 60

def test_create_court_with_existing_club(client, db_session, make_player, auth_headers, sample_club):
    """Owner creates a court when they already own a club."""
    owner = sample_club.owner
    token = auth_headers(owner)
    client.set_cookie('access_token_cookie', token)

    payload = {"court_name": "New Court 3"}
    response = client.post('/api/v1/clubs/courts', json=payload)
    assert response.status_code == 201
    court = Court.query.filter_by(name="New Court 3").first()
    assert court is not None
    assert court.club_id == sample_club.id

def test_update_court_with_overrides(client, db_session, make_player, auth_headers, sample_club):
    """Owner updates a court with custom overrides (open/close/duration)."""
    owner = sample_club.owner
    token = auth_headers(owner)
    client.set_cookie('access_token_cookie', token)

    court = sample_club.courts[0]
    payload = {
        "court_name": "Renovated Court",
        "is_active": False,
        "open_time_override": "09:00",
        "close_time_override": "21:00",
        "slot_duration_override": 45
    }
    response = client.put(f'/api/v1/clubs/courts/{court.id}', json=payload)
    assert response.status_code == 200

    db_session.refresh(court)
    assert court.name == "Renovated Court"
    assert court.is_active is False
    assert court.open_time_override == "09:00"
    assert court.close_time_override == "21:00"
    assert court.slot_duration_override == 45

def test_update_court_clear_overrides(client, db_session, make_player, auth_headers, sample_club):
    """Owner clears overrides to revert to club default hours (toggles to 'Default')."""
    owner = sample_club.owner
    token = auth_headers(owner)
    client.set_cookie('access_token_cookie', token)

    court = sample_club.courts[0]
    # Set an override first
    court.open_time_override = "10:00"
    court.slot_duration_override = 90
    db_session.commit()

    # Now send null values to clear them
    payload = {
        "court_name": court.name,
        "is_active": True,
        "open_time_override": None,
        "close_time_override": None,
        "slot_duration_override": None
    }
    response = client.put(f'/api/v1/clubs/courts/{court.id}', json=payload)
    assert response.status_code == 200

    db_session.refresh(court)
    assert court.open_time_override is None
    assert court.close_time_override is None
    assert court.slot_duration_override is None

def test_update_court_forbidden(client, db_session, make_player, auth_headers, sample_club):
    """Another owner cannot update this court (403 FORBIDDEN)."""
    other_owner = make_player(email="other.courtowner@test.com", role="owner")
    token = auth_headers(other_owner)
    client.set_cookie('access_token_cookie', token)

    court = sample_club.courts[0]
    response = client.put(f'/api/v1/clubs/courts/{court.id}', json={"court_name": "Hack"})
    assert response.status_code == 404
    assert response.json['code'] == 'NOT_FOUND'

def test_delete_court_success(client, db_session, make_player, auth_headers, sample_club):
    """Owner successfully deletes a court."""
    owner = sample_club.owner
    token = auth_headers(owner)
    client.set_cookie('access_token_cookie', token)

    court = sample_club.courts[0]
    response = client.delete(f'/api/v1/clubs/courts/{court.id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Court deleted'

    # Verify it's gone
    court = Court.query.get(court.id)
    assert court is None

def test_delete_court_forbidden(client, db_session, make_player, auth_headers, sample_club):
    """Another owner cannot delete this court (404 NOT_FOUND)."""
    other_owner = make_player(email="other.delete@test.com", role="owner")
    token = auth_headers(other_owner)
    client.set_cookie('access_token_cookie', token)

    court = sample_club.courts[0]
    response = client.delete(f'/api/v1/clubs/courts/{court.id}')
    assert response.status_code == 404
    assert response.json['code'] == 'NOT_FOUND'