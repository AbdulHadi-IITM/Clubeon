from flask import Blueprint, request, jsonify
from app.clubs.services import ClubService

clubs_bp = Blueprint('clubs', __name__, url_prefix='/api/v1/clubs')

@clubs_bp.route('', methods=['GET'])
def list_clubs():
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

@clubs_bp.route('/<int:club_id>/courts', methods=['GET'])
def get_courts(club_id):
    courts, error = ClubService.get_courts(club_id)
    if error:
        return jsonify(error), 404
        
    result = []
    for court in courts:
        result.append({
            "id": court.id,
            "club_id": court.club_id,
            "name": court.name,
            "is_active": court.is_active,
            "operating_hours_override": {
                "open_time": court.open_time_override,
                "close_time": court.close_time_override,
                "slot_duration_minutes": court.slot_duration_override
            } if court.open_time_override else None
        })
        
    return jsonify(result), 200
