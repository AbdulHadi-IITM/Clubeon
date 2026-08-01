from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.auth.decorators import role_required
from app.events.services import EventService

events_bp = Blueprint('events', __name__, url_prefix='/api/v1/events')

@events_bp.route('', methods=['GET'])
def get_events():
    club_id = request.args.get('club_id', type=int)
    events = EventService.get_events(club_id)
    
    result = []
    for e in events:
        result.append({
            "id": e.id,
            "club_id": e.club_id,
            "title": e.title,
            "description": e.description,
            "date": str(e.event_date),
            "start_time": str(e.start_time),
            "end_time": str(e.end_time),
            "max_attendees": e.max_attendees,
            "registration_fee": e.registration_fee,
            "status": e.status
        })
    return jsonify(result), 200

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
    
    if not all([club_id, title, event_date, start_time, end_time]):
        return jsonify({"code": "VALIDATION_ERROR", "message": "Missing required fields"}), 400
        
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
