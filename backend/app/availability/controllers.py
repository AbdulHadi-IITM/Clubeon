from flask import Blueprint, request, jsonify
from app.availability.services import AvailabilityService
from datetime import date

availability_bp = Blueprint('availability', __name__, url_prefix='/api/v1/availability')

@availability_bp.route('/matrix', methods=['GET'])
def get_availability_matrix():
    club_id = request.args.get('club_id', type=int)
    target_date = request.args.get('date')
    
    if not club_id:
        return jsonify({"code": "VALIDATION_ERROR", "message": "club_id is required"}), 400
        
    if not target_date:
        target_date = str(date.today())
        
    matrix, error = AvailabilityService.get_availability_matrix(club_id, target_date)
    
    if error:
        return jsonify(error), 400 if error['code'] == 'VALIDATION_ERROR' else 404
        
    return jsonify(matrix), 200
