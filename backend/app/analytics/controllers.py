from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.auth.decorators import role_required
from app.analytics.services import AnalyticsService

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/v1/analytics')

_STATUS = {'NOT_FOUND': 404, 'FORBIDDEN': 403, 'VALIDATION_ERROR': 400}


@analytics_bp.route('/admin', methods=['GET'])
@role_required('owner')
def admin_analytics():
    """KPIs for the club owner's dashboard (real data, not mocks)."""
    owner_id = int(get_jwt_identity())
    days = request.args.get('days', default=30, type=int)
    if days is None or days < 1 or days > 365:
        return jsonify({"code": "VALIDATION_ERROR",
                        "message": "days must be between 1 and 365."}), 400

    result, error = AnalyticsService.admin_overview(owner_id, days)
    if error:
        return jsonify(error), _STATUS.get(error['code'], 400)
    return jsonify(result), 200


@analytics_bp.route('/member', methods=['GET'])
@jwt_required()
def member_analytics():
    """Stats for the signed-in member's dashboard."""
    user_id = int(get_jwt_identity())
    result, error = AnalyticsService.member_overview(user_id)
    if error:
        return jsonify(error), _STATUS.get(error['code'], 400)
    return jsonify(result), 200


@analytics_bp.route('/staff', methods=['GET'])
@role_required('front-desk', 'owner')
def staff_analytics():
    """Today's operational snapshot for the front desk."""
    club_id = request.args.get('club_id', type=int)
    result, error = AnalyticsService.staff_overview(club_id)
    if error:
        return jsonify(error), _STATUS.get(error['code'], 400)
    return jsonify(result), 200
