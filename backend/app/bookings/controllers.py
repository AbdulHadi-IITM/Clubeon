from flask import Blueprint, request, jsonify
from app.bookings.services import BookingService

# Define the blueprint and the base URL
bookings_bp = Blueprint('bookings', __name__, url_prefix='/api/v1/bookings')

@bookings_bp.route('', methods=['POST'])
def create_booking():
    data = request.get_json()

    # 1. Basic Payload Validation
    required_fields = ['user_id', 'court_id', 'booking_date', 'start_time', 'end_time']
    if not all(field in data for field in required_fields):
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "Missing required fields"
        }), 400

    # 2. Delegate to the Service Layer
    booking, error = BookingService.create_booking(
        user_id=data['user_id'],
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