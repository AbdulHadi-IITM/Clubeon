import pytest
from datetime import datetime


def test_basic_health_endpoint(client):
    """Test the basic /health probe returns 200 OK."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'clubeon-api'


def test_api_health_endpoint(client):
    """Test /api/health returns database connectivity and timestamp."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'clubeon-api'
    assert data['database'] == 'connected'
    assert 'timestamp' in data
    # Verify timestamp parses as valid ISO format
    parsed_time = datetime.fromisoformat(data['timestamp'])
    assert parsed_time is not None


def test_api_status_endpoint(client):
    """Test /api/status returns service metadata, version, and feature flags."""
    response = client.get('/api/status')
    assert response.status_code == 200
    data = response.get_json()
    assert data['service'] == 'Clubeon Sports Management API'
    assert data['version'] == '1.0.0'
    assert 'features' in data
    assert isinstance(data['features'], dict)
    assert 'swagger_docs' in data['features']
    assert data['features']['swagger_docs'] is True
    assert 'environment' in data
    assert 'timestamp' in data
