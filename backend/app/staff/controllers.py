from datetime import datetime
from flask import Blueprint, jsonify, request
from app.auth.decorators import role_required
from app.staff.services import StaffService
from app.events.models import EventRegistration

staff_bp = Blueprint('staff', __name__, url_prefix='/api/v1/staff')


def booking_json(b):
    return {
        'id': b.id,
        'user_id': b.user_id,
        'user_name': b.user.name,
        'user_email': b.user.email,
        'court_id': b.court_id,
        'court_name': b.court.name,
        'club_id': b.court.club_id,
        'club_name': b.court.club.name,
        'date': str(b.booking_date),
        'start_time': str(b.start_time),
        'end_time': str(b.end_time),
        'status': b.status,
    }


@staff_bp.route('/dashboard', methods=['GET'])
@role_required('front-desk')
def dashboard():
    club_id = request.args.get('club_id', type=int)
    if not club_id or not StaffService.get_club(club_id):
        return jsonify({'code': 'VALIDATION_ERROR', 'message': 'A valid club_id is required.'}), 400
    data = StaffService.dashboard(club_id)
    data['bookings'] = [booking_json(b) for b in data['bookings']]
    return jsonify(data), 200


@staff_bp.route('/bookings', methods=['GET'])
@role_required('front-desk')
def bookings():
    club_id = request.args.get('club_id', type=int)
    if not club_id or not StaffService.get_club(club_id):
        return jsonify({'code': 'VALIDATION_ERROR', 'message': 'A valid club_id is required.'}), 400
    rows, error = StaffService.list_bookings(club_id, request.args.get('date'))
    if error:
        return jsonify(error), 400
    return jsonify([booking_json(b) for b in rows]), 200


@staff_bp.route('/members', methods=['GET'])
@role_required('front-desk')
def members():
    club_id = request.args.get('club_id', type=int)
    if not club_id or not StaffService.get_club(club_id):
        return jsonify({'code': 'VALIDATION_ERROR', 'message': 'A valid club_id is required.'}), 400
    rows = StaffService.list_members(club_id)
    return jsonify([{
        'id': user.id, 'name': user.name, 'email': user.email,
        'role': user.role, 'booking_count': booking_count,
    } for user, booking_count in rows]), 200


@staff_bp.route('/bookings/<int:booking_id>', methods=['GET'])
@role_required('front-desk')
def booking_detail(booking_id):
    club_id = request.args.get('club_id', type=int)
    if not club_id or not StaffService.get_club(club_id):
        return jsonify({'code': 'VALIDATION_ERROR', 'message': 'A valid club_id is required.'}), 400
    booking = StaffService.get_booking(club_id, booking_id)
    if not booking:
        return jsonify({'code': 'NOT_FOUND', 'message': 'Booking not found for this club.'}), 404
    return jsonify(booking_json(booking)), 200


@staff_bp.route('/members/<int:user_id>', methods=['GET'])
@role_required('front-desk')
def member_detail(user_id):
    club_id = request.args.get('club_id', type=int)
    if not club_id or not StaffService.get_club(club_id):
        return jsonify({'code': 'VALIDATION_ERROR', 'message': 'A valid club_id is required.'}), 400
    data = StaffService.member_detail(club_id, user_id)
    if not data:
        return jsonify({'code': 'NOT_FOUND', 'message': 'Member not found for this club.'}), 404
    return jsonify(data), 200


@staff_bp.route('/events', methods=['GET'])
@role_required('front-desk')
def events():
    club_id = request.args.get('club_id', type=int)
    if not club_id or not StaffService.get_club(club_id):
        return jsonify({'code': 'VALIDATION_ERROR', 'message': 'A valid club_id is required.'}), 400
    rows, error = StaffService.list_events(club_id, request.args.get('date'))
    if error:
        return jsonify(error), 400
    result = []
    for event in rows:
        registered_count = EventRegistration.query.filter_by(event_id=event.id, status='registered').count()
        result.append({
            'id': event.id,
            'club_id': event.club_id,
            'title': event.title,
            'description': event.description,
            'date': str(event.event_date),
            'start_time': str(event.start_time),
            'end_time': str(event.end_time),
            'max_attendees': event.max_attendees,
            'registration_fee': event.registration_fee,
            'status': event.status,
            'registered_count': registered_count,
        })
    return jsonify(result), 200


@staff_bp.route('/events/<int:event_id>', methods=['GET'])
@role_required('front-desk')
def event_detail(event_id):
    club_id = request.args.get('club_id', type=int)
    if not club_id or not StaffService.get_club(club_id):
        return jsonify({'code': 'VALIDATION_ERROR', 'message': 'A valid club_id is required.'}), 400
    data = StaffService.event_detail(club_id, event_id)
    if not data:
        return jsonify({'code': 'NOT_FOUND', 'message': 'Event not found for this club.'}), 404
    return jsonify(data), 200


@staff_bp.route('/attendance/expected', methods=['GET'])
@role_required('front-desk')
def expected_attendance():
    club_id = request.args.get('club_id', type=int)
    attendance_date = request.args.get('date')
    if not club_id or not StaffService.get_club(club_id):
        return jsonify({'code': 'VALIDATION_ERROR', 'message': 'A valid club_id is required.'}), 400
    rows, error = StaffService.expected_attendance(club_id, attendance_date)
    if error:
        return jsonify(error), 400
    return jsonify(rows), 200


@staff_bp.route('/attendance', methods=['GET'])
@role_required('front-desk')
def attendance():
    club_id = request.args.get('club_id', type=int)
    attendance_date = request.args.get('date')
    if not club_id or not StaffService.get_club(club_id):
        return jsonify({'code': 'VALIDATION_ERROR', 'message': 'A valid club_id is required.'}), 400
    rows = StaffService.list_attendance(club_id, attendance_date)
    return jsonify([{
        'id': r.id,
        'user_id': r.user_id,
        'user_name': r.user.name,
        'user_email': r.user.email,
        'booking_id': r.booking_id,
        'court_name': r.booking.court.name if r.booking else None,
        'booking_date': str(r.booking.booking_date) if r.booking else None,
        'start_time': str(r.booking.start_time) if r.booking else None,
        'end_time': str(r.booking.end_time) if r.booking else None,
        'check_in_at': str(r.check_in_at),
        'check_out_at': str(r.check_out_at) if r.check_out_at else None,
    } for r in rows]), 200




@staff_bp.route('/attendance/check-in', methods=['POST'])
@role_required('front-desk')
def check_in():
    data = request.get_json() or {}
    booking_id = data.get('booking_id')
    club_id = data.get('club_id')
    if not booking_id:
        return jsonify({'code': 'VALIDATION_ERROR', 'message': 'booking_id is required.'}), 400
    if not club_id:
        from app.bookings.models import Booking
        b = Booking.query.get(booking_id)
        if b and b.court:
            club_id = b.court.club_id
    if not club_id or not StaffService.get_club(int(club_id)):
        return jsonify({'code': 'VALIDATION_ERROR', 'message': 'A valid club_id is required.'}), 400
    record, error = StaffService.check_in_booking(booking_id, int(club_id))
    if error:
        return jsonify(error), 409 if error['code'] == 'CONFLICT' else 404 if error['code'] == 'NOT_FOUND' else 400
    return jsonify({'message': 'Member checked in successfully.', 'attendance_id': record.id}), 201


@staff_bp.route('/attendance/<int:attendance_id>/check-out', methods=['POST'])
@role_required('front-desk')
def check_out(attendance_id):
    club_id = request.args.get('club_id', type=int)
    if not club_id:
        from app.attendance.models import AttendanceRecord
        r = AttendanceRecord.query.get(attendance_id)
        if r and r.booking and r.booking.court:
            club_id = r.booking.court.club_id
    if not club_id or not StaffService.get_club(club_id):
        return jsonify({'code': 'VALIDATION_ERROR', 'message': 'A valid club_id is required.'}), 400
    record, error = StaffService.check_out(attendance_id, club_id)
    if error:
        return jsonify(error), 403 if error['code'] == 'FORBIDDEN' else 404 if error['code'] == 'NOT_FOUND' else 400
    return jsonify({'message': 'Member checked out successfully.'}), 200


@staff_bp.route('/events/attendance/check-in', methods=['POST'])
@role_required('front-desk')
def check_in_event():
    data = request.get_json() or {}
    event_id = data.get('event_id')
    user_id = data.get('user_id')
    if not event_id or not user_id:
        return jsonify({'code': 'VALIDATION_ERROR', 'message': 'event_id and user_id are required.'}), 400
    record, error = StaffService.check_in_event(event_id, user_id)
    if error:
        return jsonify(error), 404 if error['code'] == 'NOT_FOUND' else 400
    return jsonify({'message': 'Participant checked in successfully.', 'attendance_id': record.id}), 201
