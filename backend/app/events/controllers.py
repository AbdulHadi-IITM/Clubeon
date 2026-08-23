from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from app.auth.decorators import role_required
from app.events.services import EventService
from app.events.models import EventRegistration

events_bp = Blueprint('events', __name__, url_prefix='/api/v1/events')

def _serialize_event(e, user_id=None):
    return {
        "id": e.id,
        "club_id": e.club_id,
        "title": e.title,
        "description": e.description,
        "date": str(e.event_date),
        "start_time": str(e.start_time),
        "end_time": str(e.end_time),
        "max_attendees": e.max_attendees,
        "registration_fee": e.registration_fee,
        "status": e.status,
        "registered_count": EventRegistration.query.filter_by(event_id=e.id, status='registered').count(),
        "my_registration_status": (
            (EventRegistration.query.filter_by(event_id=e.id, user_id=user_id).first().status
             if EventRegistration.query.filter_by(event_id=e.id, user_id=user_id).first() else None)
            if user_id else None
        )
    }

@events_bp.route('', methods=['GET'])
@jwt_required(optional=True)
def get_events():
    club_id = request.args.get('club_id', type=int)
    status_filter = request.args.get('status', 'upcoming')
    
    if status_filter == 'all':
        events = EventService.get_all_events(club_id)
    else:
        events = EventService.get_events(club_id)

    identity = get_jwt_identity()
    user_id = int(identity) if identity is not None else None
    
    return jsonify([_serialize_event(e, user_id) for e in events]), 200

@events_bp.route('/<int:event_id>', methods=['GET'])
@jwt_required(optional=True)
def get_single_event(event_id):
    event = EventService.get_event_by_id(event_id)
    if not event:
        return jsonify({"code": "NOT_FOUND", "message": "Event not found"}), 404

    identity = get_jwt_identity()
    user_id = int(identity) if identity is not None else None
    return jsonify(_serialize_event(event, user_id)), 200

@events_bp.route('/<int:event_id>', methods=['PUT'])
@role_required('owner')
def update_event(event_id):
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}
    event, error = EventService.update_event(user_id, event_id, data)
    if error:
        status_code = 400
        if error['code'] == 'FORBIDDEN': status_code = 403
        elif error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code
    return jsonify({"message": "Event updated successfully", "event": _serialize_event(event, user_id)}), 200

@events_bp.route('/<int:event_id>', methods=['DELETE'])
@role_required('owner')
def delete_event(event_id):
    user_id = int(get_jwt_identity())
    success, error = EventService.delete_event(user_id, event_id)
    if error:
        status_code = 400
        if error['code'] == 'FORBIDDEN': status_code = 403
        elif error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code
    return jsonify({"message": "Event cancelled successfully"}), 200

@events_bp.route('', methods=['POST'])
@role_required('owner')
def create_event():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    club_id = data.get('club_id')
    title = data.get('title')
    description = data.get('description', '')
    event_date = data.get('event_date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    max_attendees = data.get('max_attendees')
    registration_fee = data.get('registration_fee', 0.0)
    
    if not all([title, event_date, start_time, end_time]):
        return jsonify({"code": "VALIDATION_ERROR", "message": "Missing required fields: title, event_date, start_time, end_time"}), 400
        
    event, error = EventService.create_event(
        user_id, club_id, title, description, 
        event_date, start_time, end_time, 
        max_attendees, registration_fee
    )
    
    if error:
        status_code = 400
        if error['code'] == 'FORBIDDEN': status_code = 403
        elif error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code
        
    return jsonify({
        "message": "Event created successfully",
        "event_id": event.id
    }), 201

@events_bp.route('/<int:event_id>/register', methods=['POST'])
@jwt_required()
def register_event(event_id):
    user_id = int(get_jwt_identity())
    registration, error = EventService.register(user_id, event_id)
    
    if error:
        status_code = 400
        if error['code'] == 'CONFLICT': status_code = 409
        elif error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code
        
    return jsonify({
        "message": "Registered successfully",
        "registration_id": registration.id
    }), 200

@events_bp.route('/<int:event_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_registration(event_id):
    user_id = int(get_jwt_identity())
    success, error = EventService.cancel_registration(user_id, event_id)
    
    if error:
        status_code = 400
        if error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code
        
    return jsonify({"message": "Registration cancelled successfully"}), 200


@events_bp.route('/my-registrations', methods=['GET'])
@jwt_required()
def my_registrations():
    user_id = int(get_jwt_identity())
    rows = EventRegistration.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': r.id, 'event_id': r.event_id, 'status': r.status,
        'registered_at': str(r.registered_at) if r.registered_at else None
    } for r in rows]), 200
