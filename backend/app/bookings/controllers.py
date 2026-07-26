from app.auth.decorators import role_required
from flask import Blueprint, request, jsonify
from app.bookings.services import BookingService, AuthorizationService
from flask_jwt_extended import get_jwt_identity

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

# TODO Enable owners/admins to create their clubs and add courts
# TODO Get all the available clubs/courts (for the players)
# TODO Owners/admins should be able to customize the court availablity/ slots or even the club availability
