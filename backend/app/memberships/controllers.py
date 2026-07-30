from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.memberships.services import MembershipService

memberships_bp = Blueprint('memberships', __name__, url_prefix='/api/v1/memberships')

@memberships_bp.route('/plans', methods=['GET'])
def get_plans():
    club_id = request.args.get('club_id', type=int)
    plans = MembershipService.get_plans(club_id)
    
    result = []
    for p in plans:
        result.append({
            "id": p.id,
            "club_id": p.club_id,
            "name": p.name,
            "price_monthly": p.price_monthly,
            "benefits": p.benefits
        })
    return jsonify(result), 200

@memberships_bp.route('/subscribe', methods=['POST'])
@jwt_required()
def subscribe():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    plan_id = data.get('plan_id')
    auto_renew = data.get('auto_renew', False)
    
    if not plan_id:
        return jsonify({"code": "VALIDATION_ERROR", "message": "plan_id is required"}), 400
        
    membership, error = MembershipService.subscribe(user_id, plan_id, auto_renew)
    
    if error:
        status_code = 400
        if error['code'] == 'CONFLICT': status_code = 409
        elif error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code
        
    return jsonify({
        "message": "Subscribed successfully",
        "membership_id": membership.id
    }), 201

@memberships_bp.route('/my-memberships', methods=['GET'])
@jwt_required()
def get_my_memberships():
    user_id = int(get_jwt_identity())
    memberships = MembershipService.get_my_memberships(user_id)
    
    result = []
    for m in memberships:
        result.append({
            "id": m.id,
            "plan_id": m.plan_id,
            "club_id": m.club_id,
            "plan_name": m.plan.name,
            "status": m.status,
            "start_date": str(m.start_date),
            "end_date": str(m.end_date),
            "auto_renew": m.auto_renew
        })
    return jsonify(result), 200

@memberships_bp.route('/<int:membership_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_membership(membership_id):
    user_id = int(get_jwt_identity())
    success, error = MembershipService.cancel_membership(user_id, membership_id)
    
    if error:
        status_code = 400
        if error['code'] == 'FORBIDDEN': status_code = 403
        elif error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code
        
    return jsonify({"message": "Membership cancelled successfully"}), 200
