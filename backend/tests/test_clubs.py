import pytest
from app.clubs.models import Club, Court

def test_list_clubs_public(client, sample_club):
    response = client.get('/api/v1/clubs')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['name'] == 'Ace Sports Club'
    assert response.json[0]['operating_hours']['open_time'] == '06:00'

def test_list_clubs_empty(client):
    response = client.get('/api/v1/clubs')
    assert response.status_code == 200
    assert len(response.json) == 0

def test_list_clubs_search(client, sample_club):
    response = client.get('/api/v1/clubs?search=ace')
    assert response.status_code == 200
    assert len(response.json) == 1
    
    response2 = client.get('/api/v1/clubs?search=badminton')
    assert response2.status_code == 200
    assert len(response2.json) == 0

def test_get_courts_for_club(client, sample_club):
    response = client.get(f'/api/v1/clubs/{sample_club.id}/courts')
    assert response.status_code == 200
    assert len(response.json) == 1 # Only active courts should be returned
    assert response.json[0]['name'] == 'Court 1 - Clay'
    assert response.json[0]['operating_hours_override'] is None

def test_get_courts_invalid_club(client):
    response = client.get('/api/v1/clubs/9999/courts')
    assert response.status_code == 404
    assert response.json['code'] == 'NOT_FOUND'
