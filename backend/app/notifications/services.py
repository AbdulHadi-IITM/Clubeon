from app.extensions import db
from app.notifications.models import Notification

class NotificationService:
    @staticmethod
    def get_my_notifications(user_id):
        return Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()

    @staticmethod
    def mark_read(user_id, notification_id):
        notification = Notification.query.get(notification_id)
        if not notification:
            return False, {"code": "NOT_FOUND", "message": "Notification not found"}
            
        if notification.user_id != user_id:
            return False, {"code": "FORBIDDEN", "message": "Not authorized"}

        notification.is_read = True
        db.session.commit()
        return True, None

    @staticmethod
    def mark_all_read(user_id):
        notifications = Notification.query.filter_by(user_id=user_id, is_read=False).all()
        for n in notifications:
            n.is_read = True
        db.session.commit()
        return True, None
