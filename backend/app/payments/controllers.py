from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.payments.services import PaymentService

payments_bp = Blueprint('payments', __name__, url_prefix='/api/v1/payments')

@payments_bp.route('/my-payments', methods=['GET'])
@jwt_required()
def get_my_payments():
    user_id = int(get_jwt_identity())
    payments = PaymentService.get_my_payments(user_id)
    
    result = []
    for p in payments:
        result.append({
            "id": p.id,
            "amount": p.amount,
            "currency": p.currency,
            "payment_type": p.payment_type,
            "reference_id": p.reference_id,
            "status": p.status,
            "transaction_id": p.gateway_transaction_id,
            "created_at": str(p.created_at)
        })
    return jsonify(result), 200

@payments_bp.route('/webhook', methods=['POST'])
def webhook():
    # Mock webhook from a payment provider
    data = request.get_json()
    if not data:
        return jsonify({"code": "VALIDATION_ERROR", "message": "Invalid payload"}), 400
        
    transaction_id = data.get('transaction_id', 'mock_txn_123')
    status = data.get('status', 'completed')
    reference_id = data.get('reference_id')
    payment_type = data.get('payment_type', 'unknown')
    
    PaymentService.handle_webhook(transaction_id, status, reference_id, payment_type)
    
    return jsonify({"message": "Webhook processed successfully"}), 200
