from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.auth.decorators import role_required
from app.clubs.services import ClubService, CourtService

clubs_bp = Blueprint('clubs', __name__, url_prefix='/api/v1/clubs')

@clubs_bp.route('', methods=['GET'])
@jwt_required(optional=True)
def list_clubs():
    """
    Public club directory.

    Anonymous access is deliberate: the landing page's court-availability view
    and the club picker both need this before a visitor signs in, and the
    payload is club metadata only — no personal data.
    """
    search = request.args.get('search')
    clubs = ClubService.list_clubs(search)
    
    result = []
    for club in clubs:
        result.append({
            "id": club.id,
            "name": club.name,
            "address": club.address,
            "owner_id": club.owner_id,
            "operating_hours": {
                "open_time": club.open_time,
                "close_time": club.close_time,
                "slot_duration_minutes": club.slot_duration_minutes
            }
        })
    
    return jsonify(result), 200

@clubs_bp.route('', methods=['POST'])
@role_required('owner')
def create_club():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    name = data.get('name')
    address = data.get('address')
    if not name or not address:
        return jsonify({"code": "VALIDATION_ERROR", "message": "Club name and address are required"}), 400

    club, error = ClubService.create_club(
        owner_id=user_id,
        name=name,
        address=address,
        open_time=data.get('open_time'),
        close_time=data.get('close_time'),
        slot_duration=data.get('slot_duration_minutes')
    )
    if error:
        return jsonify(error), 409 if error['code'] == 'CONFLICT' else 500

    return jsonify({"message": "Club created successfully", "club": {"id": club.id, "name": club.name}}), 201

@clubs_bp.route('/<int:club_id>/courts', methods=['GET'])
@jwt_required(optional=True)
def get_courts(club_id):
    """Public court list for a club. Court metadata only, no personal data."""
    courts, error = ClubService.get_courts(club_id)
    if error:
        return jsonify(error), 404
        
    result = []
    for court in courts:
        result.append({
            "id": court.id,
            "club_id": court.club_id,
            "name": court.name,
            "sport_type": court.sport_type,
            "is_active": court.is_active,
            "operating_hours_override": {
                "open_time": court.open_time_override,
                "close_time": court.close_time_override,
                "slot_duration_minutes": court.slot_duration_override
            } if court.open_time_override else None
        })
        
    return jsonify(result), 200

@clubs_bp.route('/courts', methods=['GET'])
@role_required('owner')
def list_courts():
    user_id = int(get_jwt_identity())
    courts, club = CourtService.get_courts_and_club_for_owner(user_id)

    return jsonify({
        "club": {
            "id": club.id,
            "name": club.name,
            "address": club.address,
            "open_time": club.open_time,
            "close_time": club.close_time,
            "slot_duration_minutes": club.slot_duration_minutes
        } if club else None,
        "courts": [{
            "id": c.id,
            "name": c.name,
            "sport_type": c.sport_type,
            "is_active": c.is_active,
            "open_time_override": c.open_time_override,
            "close_time_override": c.close_time_override,
            "slot_duration_override": c.slot_duration_override
        } for c in courts]
    }), 200

@clubs_bp.route('/courts', methods=['POST'])
@role_required('owner')
def create_court():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    court_name = data.get('court_name')
    if not court_name:
        return jsonify({"code": "VALIDATION_ERROR", "message": "Court name is required"}), 400
    court, error = CourtService.create_court(
        owner_id=user_id,
        court_name=court_name,
        club_name=data.get('club_name'),
        club_address=data.get('club_address'),
        sport_type=data.get('sport_type', 'multi-purpose')
    )
    if error:
        return jsonify(error), 400 if error['code'] in ('CLUB_REQUIRED', 'VALIDATION_ERROR') else 500
    return jsonify({"message": "Court created", "court": {"id": court.id, "name": court.name, "sport_type": court.sport_type, "is_active": court.is_active}}), 201

@clubs_bp.route('/courts/<int:court_id>', methods=['PUT'])
@role_required('owner')
def update_court(court_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()
    court_name = data.get('court_name')
    if not court_name:
        return jsonify({"code": "VALIDATION_ERROR", "message": "Court name is required"}), 400

    court, error = CourtService.update_court(
        court_id=court_id,
        owner_id=user_id,
        court_name=court_name,
        is_active=data.get('is_active', True),
        sport_type=data.get('sport_type', 'multi-purpose'),
        open_time_override=data.get('open_time_override'),
        close_time_override=data.get('close_time_override'),
        slot_duration_override=data.get('slot_duration_override')
    )
    if error:
        return jsonify(error), 404 if error['code'] == 'NOT_FOUND' else 400 if error['code'] == 'VALIDATION_ERROR' else 500
    return jsonify({"message": "Court updated successfully"}), 200

@clubs_bp.route('/courts/<int:court_id>', methods=['DELETE'])
@role_required('owner')
def delete_court(court_id):
    user_id = int(get_jwt_identity())
    success, error = CourtService.delete_court(court_id, user_id)
    if error:
        return jsonify(error), 404 if error['code'] == 'NOT_FOUND' else 500
    return jsonify({"message": "Court deleted"}), 200

@clubs_bp.route('/my-club', methods=['GET'])
@role_required('owner')
def get_my_club():
    user_id = int(get_jwt_identity())
    club = ClubService.get_club_by_owner(user_id)
    if not club:
        return jsonify({"message": "No club found"}), 404
    return jsonify({
        "id": club.id,
        "name": club.name,
        "address": club.address,
        "open_time": club.open_time,
        "close_time": club.close_time,
        "slot_duration_minutes": club.slot_duration_minutes
    }), 200

@clubs_bp.route('/<int:club_id>', methods=['PUT'])
@role_required('owner')
def update_club(club_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()

    club, error = ClubService.update_club(
        owner_id=user_id,
        club_id=club_id,
        name=data.get('name'),
        address=data.get('address'),
        open_time=data.get('open_time'),
        close_time=data.get('close_time'),
        slot_duration=data.get('slot_duration_minutes')
    )
    if error:
        return jsonify(error), 403

    return jsonify({"message": "Club settings updated successfully"}), 200

@clubs_bp.route('/<int:club_id>/metadata', methods=['PATCH', 'PUT'])
@role_required('owner')
def update_club_metadata(club_id):
    user_id = int(get_jwt_identity())
    data = request.get_json() or {}

    club, error = ClubService.update_metadata(
        owner_id=user_id,
        club_id=club_id,
        latitude=data.get('latitude'),
        longitude=data.get('longitude'),
        amenities=data.get('amenities'),
        tags=data.get('tags')
    )
    if error:
        return jsonify(error), 403

    return jsonify({
        "message": "Club metadata updated successfully",
        "club": {
            "id": club.id,
            "latitude": club.latitude,
            "longitude": club.longitude,
            "amenities": club.amenities,
            "tags": club.tags
        }
    }), 200

