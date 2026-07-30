import pytest
from datetime import date, time, timedelta, datetime
from app.bookings.models import Booking, CourtBlock

@pytest.fixture
def sample_availability_data(sample_club, db_session, make_player):
    player = make_player(email="player2@example.com")
    target_date = date.today()
    
    # We know sample_club has 2 courts, Court 1 (active) and Court 2 (inactive)
    courts = sample_club.courts
    active_court = [c for c in courts if c.name == 'Court 1 - Clay'][0]
    
    # Add a booking from 07:00 to 08:00
    booking = Booking(
        user_id=player.id, 
        court_id=active_court.id, 
        booking_date=target_date, 
        start_time=time(7, 0), 
        end_time=time(8, 0),
        status='active'
    )
    
    # Add a court block for the day
    block = CourtBlock(
        court_id=active_court.id,
        start_date=target_date,
        end_date=target_date,
        title="Maintenance",
        created_by=player.id
    )
    
    db_session.add_all([booking, block])
    db_session.commit()
    
    return sample_club, active_court, target_date

def test_get_availability_matrix_success(client, sample_availability_data):
    club, active_court, target_date = sample_availability_data
    
    response = client.get(f'/api/v1/availability/matrix?club_id={club.id}&date={target_date}')
    
    assert response.status_code == 200
    data = response.json
    assert data['date'] == str(target_date)
    assert len(data['courts']) == 1 # Only active court
    
    court_data = data['courts'][0]
    assert court_data['court_id'] == active_court.id
    
    # Verify slots
    slots = court_data['slots']
    assert len(slots) > 0
    
    # Check 06:00 to 07:00 is blocked (due to day-long block)
    assert slots[0]['start_time'] == '06:00:00'
    assert slots[0]['end_time'] == '07:00:00'
    assert slots[0]['status'] == 'blocked'
    assert slots[0]['reason'] == 'admin_block'
    
    # Check 07:00 to 08:00 is blocked too
    assert slots[1]['start_time'] == '07:00:00'
    assert slots[1]['status'] == 'blocked'

def test_get_availability_matrix_missing_club(client):
    response = client.get('/api/v1/availability/matrix?date=2024-01-01')
    assert response.status_code == 400
    assert response.json['code'] == 'VALIDATION_ERROR'

def test_get_availability_matrix_invalid_date(client, sample_club):
    response = client.get(f'/api/v1/availability/matrix?club_id={sample_club.id}&date=invalid-date')
    assert response.status_code == 400
    assert response.json['code'] == 'VALIDATION_ERROR'
