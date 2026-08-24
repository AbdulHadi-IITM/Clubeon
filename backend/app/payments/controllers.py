from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.payments.services import PaymentService
from app.payments.stripe_service import StripeService
from app.payments.fulfillment import PaymentStatusService

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


# ============================================================
# Stripe Payment API
# ============================================================

@payments_bp.route('/stripe/create-payment-intent', methods=['POST'])
@jwt_required()
def stripe_create_payment_intent():
    """Create a Stripe PaymentIntent for the authenticated user."""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json(silent=True) or {}

        # Amount is derived server-side from the referenced entity, never trusted
        # from the client.
        result, error = StripeService.create_payment_intent(
            user_id=user_id,
            payment_type=data.get('payment_type'),
            reference_id=data.get('reference_id'),
            currency=data.get('currency'),
        )

        if error:
            status_map = {
                'VALIDATION_ERROR': 400,
                'NOT_FOUND': 404,
                'FORBIDDEN': 403,
                'ALREADY_PAID': 409,
                'CONFIG_ERROR': 503,
                'PAYMENT_GATEWAY_ERROR': 502,
            }
            return jsonify(error), status_map.get(error['code'], 400)

        return jsonify(result), 201
    except Exception as exc:
        return jsonify({"code": "PAYMENT_GATEWAY_ERROR", "message": str(exc)}), 502


@payments_bp.route('/stripe/webhook', methods=['POST'])
def stripe_webhook():
    """Stripe webhook endpoint. Verifies the signature on the raw body."""
    payload = request.get_data()  # raw bytes required for signature verification
    signature = request.headers.get('Stripe-Signature', '')

    result, error = StripeService.handle_webhook(payload, signature)

    if error:
        status_map = {
            'VALIDATION_ERROR': 400,
            'INVALID_SIGNATURE': 400,   # Stripe expects a 4xx to retry/flag
            'CONFIG_ERROR': 503,
        }
        return jsonify(error), status_map.get(error['code'], 400)

    return jsonify(result), 200


@payments_bp.route('/stripe/status/<int:payment_id>', methods=['GET'])
@jwt_required()
def stripe_payment_status(payment_id):
    """
    Poll a payment's status after confirming the card on the client.

    Once the webhook has been processed the status becomes `completed` and,
    for memberships/events, the resulting membership_id / registration_status
    is included so the client can route the user onward.
    """
    user_id = int(get_jwt_identity())
    result, error = PaymentStatusService.get_status(user_id, payment_id)

    if error:
        status_map = {'NOT_FOUND': 404, 'FORBIDDEN': 403}
        return jsonify(error), status_map.get(error['code'], 400)

    return jsonify(result), 200
