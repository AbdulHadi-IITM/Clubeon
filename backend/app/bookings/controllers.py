from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.bookings.services import BookingService, AuthorizationService, CourtService
from app.auth.decorators import role_required

# Define the blueprint and the base URL
bookings_bp = Blueprint('bookings', __name__, url_prefix='/api/v1/bookings')

@bookings_bp.route('', methods=['POST'])
@role_required('player')
def create_booking():
    user_id = get_jwt_identity()
    data = request.get_json()

    # 1. Basic Payload Validation
    required_fields = ['court_id', 'booking_date', 'start_time', 'end_time']
    if not all(field in data for field in required_fields):
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "Missing required fields"
        }), 400

    # 2. Delegate to the Service Layer
    booking, error = BookingService.create_booking(
        user_id=user_id,
        court_id=data['court_id'],
        booking_date=data['booking_date'],
        start_time=data['start_time'],
        end_time=data['end_time']
    )

    # 3. Handle specific errors returned by the service
    if error:
        status_code = 409 if error['code'] == 'CONCURRENCY_CONFLICT' else 500
        return jsonify(error), status_code

    # 4. Success Response
    return jsonify({
        "message": "Booking successful",
        "booking_id": booking.id
    }), 201

@bookings_bp.route('/admin/blocks', methods=['POST'])
@role_required('owner')
def block_court():
    data = request.get_json()
    current_admin_id = get_jwt_identity()
    court_id = data.get('court_id')

    # 1. Enforce Multi-Tenant Isolation
    is_authorized = AuthorizationService.verify_court_ownership(court_id, current_admin_id)
    if not is_authorized:
        return jsonify({
            "code": "FORBIDDEN",
            "message": "You do not own the facility housing this court."
        }), 403

    # TODO Proceed with blocking logic...
    return jsonify({"message": "Court blocked successfully"}), 201

@bookings_bp.route('/courts', methods=['GET'])
@role_required('owner')
def list_courts():
    user_id = get_jwt_identity()
    courts = CourtService.get_courts_for_owner(int(user_id))
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "is_active": c.is_active
    } for c in courts]), 200

@bookings_bp.route('/courts', methods=['POST'])
@role_required('owner')
def create_court():
    user_id = get_jwt_identity()
    data = request.get_json()

    court_name = data.get('court_name')
    if not court_name:
        return jsonify({"code": "VALIDATION_ERROR", "message": "Court name is required"}), 400

    court, error = CourtService.create_court(
        owner_id=int(user_id),
        court_name=court_name,
        club_name=data.get('club_name'),
        club_address=data.get('club_address')
    )
    if error:
        return jsonify(error), 400 if error['code'] == 'CLUB_REQUIRED' else 500

    return jsonify({"message": "Court created successfully", "court": {
        "id": court.id,
        "name": court.name,
        "is_active": court.is_active
    }}), 201

@bookings_bp.route('/courts/<int:court_id>', methods=['PUT'])
@role_required('owner')
def update_court(court_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    court_name = data.get('court_name')
    if not court_name:
        return jsonify({"code": "VALIDATION_ERROR", "message": "Court name is required"}), 400

    court, error = CourtService.update_court(
        court_id=court_id,
        owner_id=int(user_id),
        court_name=court_name,
        is_active=data.get('is_active', True)
    )
    if error:
        return jsonify(error), 404 if error['code'] == 'NOT_FOUND' else 500

    return jsonify({"message": "Court updated successfully"}), 200

@bookings_bp.route('/courts/<int:court_id>', methods=['DELETE'])
@role_required('owner')
def delete_court(court_id):
    user_id = get_jwt_identity()
    success, error = CourtService.delete_court(
        court_id=court_id,
        owner_id=int(user_id)
    )
    if error:
        return jsonify(error), 404 if error['code'] == 'NOT_FOUND' else 500

    return jsonify({"message": "Court deleted successfully"}), 200
