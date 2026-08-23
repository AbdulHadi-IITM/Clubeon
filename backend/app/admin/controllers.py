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

@admin_bp.route('/announcements', methods=['POST'])
@role_required('owner')
def create_announcement():
    owner_id = int(get_jwt_identity())
    data = request.get_json() or {}
    
    title = data.get('title')
    body = data.get('body') or data.get('message', '')
    category = data.get('category', 'General')
    target_audience = data.get('target_audience', 'all')
    
    if not title or not body:
        return jsonify({"code": "VALIDATION_ERROR", "message": "Title and body are required"}), 400
        
    announcement, error = AdminService.create_announcement(owner_id, title, body, category.lower(), target_audience)
    if error:
        return jsonify(error), 400
        
    return jsonify({
        "message": "Announcement broadcasted successfully",
        "announcement": announcement
    }), 201

@admin_bp.route('/announcements', methods=['GET'])
@role_required('owner')
def get_announcements():
    owner_id = int(get_jwt_identity())
    announcements, error = AdminService.get_announcements(owner_id)
    if error:
        return jsonify(error), 400
    return jsonify(announcements), 200

@admin_bp.route('/announcements/<int:announcement_id>', methods=['DELETE'])
@role_required('owner')
def delete_announcement(announcement_id):
    owner_id = int(get_jwt_identity())
    success, error = AdminService.delete_announcement(owner_id, announcement_id)
    if error:
        return jsonify(error), 400
    return jsonify({"message": "Announcement deleted successfully"}), 200

@admin_bp.route('/members', methods=['GET'])
@role_required('owner')
def list_members():
    owner_id = int(get_jwt_identity())
    members, error = AdminService.list_club_members(owner_id)
    if error:
        return jsonify(error), 400
    return jsonify(members), 200

