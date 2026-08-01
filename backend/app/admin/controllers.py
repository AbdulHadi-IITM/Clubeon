from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.auth.decorators import role_required
from app.admin.services import AdminService

admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')

@admin_bp.route('/bookings/<int:booking_id>/override', methods=['POST'])
@role_required('owner')
def override_booking(booking_id):
    owner_id = int(get_jwt_identity())
    success, error = AdminService.override_booking(owner_id, booking_id)
    
    if error:
        status_code = 400
        if error['code'] == 'FORBIDDEN': status_code = 403
        elif error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code
        
    return jsonify({"message": "Booking overridden successfully"}), 200

@admin_bp.route('/courts/block', methods=['POST'])
@role_required('owner')
def block_court():
    owner_id = int(get_jwt_identity())
    data = request.get_json()
    
    court_id = data.get('court_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    title = data.get('title', 'Admin Block')
    
    if not all([court_id, start_date, end_date]):
        return jsonify({"code": "VALIDATION_ERROR", "message": "Missing required fields"}), 400
        
    block, error = AdminService.block_court(owner_id, court_id, start_date, end_date, title)
    
    if error:
        status_code = 400
        if error['code'] == 'FORBIDDEN': status_code = 403
        elif error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code
        
    return jsonify({
        "message": "Court blocked successfully",
        "block_id": block.id
    }), 201
