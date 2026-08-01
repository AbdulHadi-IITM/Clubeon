from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.auth.decorators import role_required
from app.attendance.services import AttendanceService

attendance_bp = Blueprint('attendance', __name__, url_prefix='/api/v1/attendance')

@attendance_bp.route('/check-in', methods=['POST'])
@jwt_required()
def check_in():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    booking_id = data.get('booking_id')
    event_id = data.get('event_id')
    
    record, error = AttendanceService.check_in(user_id, booking_id, event_id)
    
    if error:
        status_code = 400
        if error['code'] == 'CONFLICT': status_code = 409
        elif error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code
        
    return jsonify({
        "message": "Checked in successfully",
        "attendance_id": record.id
    }), 201

@attendance_bp.route('/check-out', methods=['POST'])
@jwt_required()
def check_out():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    attendance_id = data.get('attendance_id')
    if not attendance_id:
        return jsonify({"code": "VALIDATION_ERROR", "message": "attendance_id is required"}), 400
        
    success, error = AttendanceService.check_out(user_id, attendance_id)
    
    if error:
        status_code = 400
        if error['code'] == 'FORBIDDEN': status_code = 403
        elif error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code
        
    return jsonify({"message": "Checked out successfully"}), 200

@attendance_bp.route('/admin/view', methods=['GET'])
@role_required('owner')
def view_attendance():
    owner_id = int(get_jwt_identity())
    club_id = request.args.get('club_id', type=int)
    
    if not club_id:
        return jsonify({"code": "VALIDATION_ERROR", "message": "club_id is required"}), 400
        
    records, error = AttendanceService.get_club_attendance(owner_id, club_id)
    
    if error:
        return jsonify(error), 403
        
    result = []
    for r in records:
        result.append({
            "id": r.id,
            "user_id": r.user_id,
            "user_email": r.user.email,
            "booking_id": r.booking_id,
            "event_id": r.event_id,
            "check_in_at": str(r.check_in_at),
            "check_out_at": str(r.check_out_at) if r.check_out_at else None
        })
    return jsonify(result), 200
