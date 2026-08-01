import pytest
from app.payments.models import Payment

def test_get_my_payments(client, auth_headers, db_session, make_player):
    user = make_player(email="pay@test.com")
    payment = Payment(
        user_id=user.id,
        amount=150.0,
        currency='INR',
        payment_type='booking',
        reference_id=1,
        status='completed',
        gateway_transaction_id='txn_123'
    )
    db_session.add(payment)
    db_session.commit()
    
    token = auth_headers(user)
    client.set_cookie('access_token_cookie', token)
    
    response = client.get('/api/v1/payments/my-payments')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['amount'] == 150.0
    assert response.json[0]['status'] == 'completed'

def test_webhook(client, db_session):
    payload = {
        "transaction_id": "mock_txn_456",
        "status": "completed",
        "reference_id": 99,
        "payment_type": "event"
    }
    
    response = client.post('/api/v1/payments/webhook', json=payload)
    assert response.status_code == 200
    assert response.json['message'] == 'Webhook processed successfully'
    
    payment = Payment.query.filter_by(reference_id=99, payment_type="event").first()
    assert payment is not None
    assert payment.status == 'completed'
    assert payment.gateway_transaction_id == 'mock_txn_456'
