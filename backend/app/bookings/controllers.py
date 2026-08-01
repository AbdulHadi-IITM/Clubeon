from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.bookings.services import BookingService

bookings_bp = Blueprint('bookings', __name__, url_prefix='/api/v1/bookings')

@bookings_bp.route('', methods=['POST'])
@jwt_required()
def create_booking():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    court_id = data.get('court_id')
    booking_date = data.get('booking_date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    
    if not all([court_id, booking_date, start_time, end_time]):
        return jsonify({"code": "VALIDATION_ERROR", "message": "Missing required fields"}), 400
        
    booking, error = BookingService.create_booking(user_id, court_id, booking_date, start_time, end_time)
    if error:
        status_code = 400
        if error['code'] == 'CONFLICT': status_code = 409
        elif error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code
        
    return jsonify({
        "message": "Booking created successfully",
        "booking_id": booking.id
    }), 201

@bookings_bp.route('', methods=['GET'])
@jwt_required()
def get_my_bookings():
    user_id = int(get_jwt_identity())
    bookings = BookingService.get_my_bookings(user_id)
    
    result = []
    for b in bookings:
        result.append({
            "id": b.id,
            "court_id": b.court_id,
            "date": str(b.booking_date),
            "start_time": str(b.start_time),
            "end_time": str(b.end_time),
            "status": b.status,
            "court_name": b.court.name,
            "club_name": b.court.club.name
        })
    return jsonify(result), 200

@bookings_bp.route('/<int:booking_id>/release', methods=['POST'])
@jwt_required()
def release_booking(booking_id):
    user_id = int(get_jwt_identity())
    success, error = BookingService.release_booking(user_id, booking_id)
    
    if error:
        status_code = 400
        if error['code'] == 'FORBIDDEN': status_code = 403
        elif error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code
        
    return jsonify({"message": "Booking released successfully"}), 200
