from app.extensions import db
from app.notifications.models import Notification
from sqlalchemy import or_

class NotificationService:
    @staticmethod
    def get_my_notifications(user_id):
        # Fetch notifications specific to this user, plus all global announcements
        # Deduplicate announcements by title if needed
        notifications = Notification.query.filter(
            or_(
                Notification.user_id == user_id,
                Notification.type.in_(['announcement', 'General', 'Broadcast', 'Tournament', 'Policy', 'Maintenance'])
            )
        ).order_by(Notification.created_at.desc()).all()

        # Deduplicate announcements by title and created date to avoid repeats
        seen_keys = set()
        deduped = []
        for n in notifications:
            key = (n.title, str(n.created_at)[:10])
            if key not in seen_keys:
                seen_keys.add(key)
                deduped.append(n)
        return deduped

    @staticmethod
    def mark_read(user_id, notification_id):
        notification = Notification.query.get(notification_id)
        if not notification:
            return False, {"code": "NOT_FOUND", "message": "Notification not found"}
            
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
