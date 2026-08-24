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

def test_unauthenticated_mock_webhook_is_gone(client):
    """
    The old POST /payments/webhook took an unsigned JSON body and marked any
    payment completed, so anyone could grant themselves a paid membership.
    Settlement now goes through the signature-verified Stripe webhook only.
    """
    response = client.post('/api/v1/payments/webhook', json={
        "transaction_id": "mock_txn_456",
        "status": "completed",
        "reference_id": 99,
        "payment_type": "event",
    })
    assert response.status_code == 404
    assert Payment.query.filter_by(reference_id=99, payment_type="event").first() is None
