from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from app.auth.decorators import role_required
from app.admin.services import AdminService

admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')


def serialize_admin_booking(b):
    user_name = b.user.name if b.user else 'Unknown member'
    user_email = b.user.email if b.user else '—'
    court_name = b.court.name if b.court else 'Court'
    sport_type = b.court.sport_type if b.court else 'Other'
    start_t = str(b.start_time)[:5] if b.start_time else ''
    end_t = str(b.end_time)[:5] if b.end_time else ''

    return {
        'id': b.id,
        'user_id': b.user_id,
        'player': user_name,
        'email': user_email,
        'member': {
            'id': b.user.id if b.user else None,
            'name': user_name,
            'email': user_email,
        },
        'court_id': b.court_id,
        'court_name': court_name,
        'facility': court_name,
        'sport': sport_type,
        'sport_type': sport_type,
        'club_id': b.court.club.id if b.court and b.court.club else None,
        'club_name': b.court.club.name if b.court and b.court.club else '',
        'date': str(b.booking_date),
        'start_time': start_t,
        'end_time': end_t,
        'time': f"{start_t} - {end_t}",
        'duration': '1.0 hr',
        'amount': 40,
        'paymentStatus': 'Paid',
        'status': b.status,
        'is_peak_hour': bool(b.is_peak_hour),
        'created_at': b.created_at.isoformat() if b.created_at else None,
    }


@admin_bp.route('/bookings', methods=['GET'])
@role_required('owner')
def get_admin_bookings():
    """Return all bookings for the admin's clubs, optionally filtered by member, court, status, date, or search."""
    owner_id = int(get_jwt_identity())

    member_id = request.args.get('member_id', type=int)
    court_id = request.args.get('court_id', type=int)
    status = request.args.get('status', type=str)
    date_str = request.args.get('date', type=str)
    search = request.args.get('search', type=str)

    bookings = AdminService.get_bookings(
        owner_id=owner_id,
        member_id=member_id,
        status=status,
        court_id=court_id,
        date_str=date_str,
        search=search,
    )

    return jsonify([serialize_admin_booking(b) for b in bookings]), 200


@admin_bp.route('/members/<int:member_id>/bookings', methods=['GET'])
@role_required('owner')
def get_member_bookings(member_id):
    """Return every booking for one member within the admin's clubs."""
    owner_id = int(get_jwt_identity())

    bookings = AdminService.get_bookings(
        owner_id=owner_id,
        member_id=member_id,
    )

    return jsonify([serialize_admin_booking(b) for b in bookings]), 200


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


@admin_bp.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
@role_required('owner')
def cancel_booking(booking_id):
    owner_id = int(get_jwt_identity())
    success, error = AdminService.cancel_booking(owner_id, booking_id)
    
    if error:
        status_code = 400
        if error['code'] == 'FORBIDDEN': status_code = 403
        elif error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code
        
    return jsonify({"message": "Booking cancelled successfully"}), 200


@admin_bp.route('/bookings/<int:booking_id>/complete', methods=['POST'])
@role_required('owner')
def complete_booking(booking_id):
    owner_id = int(get_jwt_identity())
    success, error = AdminService.complete_booking(owner_id, booking_id)
    
    if error:
        status_code = 400
        if error['code'] == 'FORBIDDEN': status_code = 403
        elif error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code
        
    return jsonify({"message": "Booking marked as completed"}), 200


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


@admin_bp.route('/members', methods=['GET'])
@role_required('owner')
def get_admin_members():
    """Return all members registered or active in owner's clubs."""
    owner_id = int(get_jwt_identity())
    members = AdminService.get_members(owner_id)
    return jsonify(members), 200


@admin_bp.route('/events', methods=['GET'])
@role_required('owner')
def get_admin_events():
    """Return all events belonging to the owner's clubs."""
    owner_id = int(get_jwt_identity())
    events = AdminService.get_events(owner_id)
    return jsonify(events), 200


@admin_bp.route('/analytics', methods=['GET'])
@role_required('owner')
def get_admin_analytics():
    """Return dynamic booking and utilization analytics for the owner's clubs."""
    owner_id = int(get_jwt_identity())
    stats = AdminService.get_analytics(owner_id)
    return jsonify(stats), 200

