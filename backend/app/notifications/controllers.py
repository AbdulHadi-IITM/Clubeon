from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.notifications.services import NotificationService

notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/v1/notifications')

@notifications_bp.route('', methods=['GET'])
@jwt_required()
def get_my_notifications():
    user_id = int(get_jwt_identity())
    notifications = NotificationService.get_my_notifications(user_id)
    
    result = []
    for n in notifications:
        result.append({
            "id": n.id,
            "title": n.title,
            "body": n.body,
            "type": n.type,
            "is_read": n.is_read,
            "created_at": str(n.created_at)
        })
    return jsonify(result), 200

@notifications_bp.route('/<int:notification_id>/read', methods=['POST'])
@jwt_required()
def mark_read(notification_id):
    user_id = int(get_jwt_identity())
    success, error = NotificationService.mark_read(user_id, notification_id)
    
    if error:
        status_code = 400
        if error['code'] == 'FORBIDDEN': status_code = 403
        elif error['code'] == 'NOT_FOUND': status_code = 404
        return jsonify(error), status_code
        
    return jsonify({"message": "Notification marked as read"}), 200

@notifications_bp.route('/read-all', methods=['POST'])
@jwt_required()
def mark_all_read():
    user_id = int(get_jwt_identity())
    NotificationService.mark_all_read(user_id)
    return jsonify({"message": "All notifications marked as read"}), 200
