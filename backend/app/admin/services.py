from datetime import datetime
from app.extensions import db
from app.bookings.models import Booking, CourtBlock
from app.clubs.models import Court

class AdminService:
    @staticmethod
    def override_booking(owner_id, booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return False, {"code": "NOT_FOUND", "message": "Booking not found"}
        
        # Verify ownership (The owner of the club that owns the court)
        if booking.court.club.owner_id != owner_id:
            return False, {"code": "FORBIDDEN", "message": "Not authorized to override bookings for this club"}

        if booking.status != 'active':
            return False, {"code": "VALIDATION_ERROR", "message": f"Booking is already {booking.status}"}

        booking.status = 'overridden'
        db.session.commit()
        return True, None

    @staticmethod
    def block_court(owner_id, court_id, start_date_str, end_date_str, title):
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            return None, {"code": "VALIDATION_ERROR", "message": "Invalid date format"}

        court = Court.query.get(court_id)
        if not court:
            return None, {"code": "NOT_FOUND", "message": "Court not found"}
            
        if court.club.owner_id != owner_id:
            return None, {"code": "FORBIDDEN", "message": "Not authorized to block courts for this club"}

        if start_date > end_date:
            return None, {"code": "VALIDATION_ERROR", "message": "Start date must be before or equal to end date"}

        # Cancel any active bookings in this range
        bookings_to_cancel = Booking.query.filter(
            Booking.court_id == court_id,
            Booking.booking_date >= start_date,
            Booking.booking_date <= end_date,
            Booking.status == 'active'
        ).all()

        for b in bookings_to_cancel:
            b.status = 'overridden'

        block = CourtBlock(
            court_id=court_id,
            start_date=start_date,
            end_date=end_date,
            title=title,
            created_by=owner_id
        )
        db.session.add(block)
        db.session.commit()
        
        return block, None

    @staticmethod
    def create_announcement(owner_id, title, body, announcement_type='general', target_audience='all'):
        from app.notifications.models import Notification
        from app.auth.models import User
        
        notification = Notification(
            user_id=owner_id,
            title=title,
            body=body,
            type=announcement_type,
            is_read=False
        )
        db.session.add(notification)

        users = User.query.filter(User.id != owner_id).all()
        for u in users:
            db.session.add(Notification(
                user_id=u.id,
                title=title,
                body=body,
                type=announcement_type,
                is_read=False
            ))
        
        db.session.commit()
        return {
            "id": notification.id,
            "title": notification.title,
            "body": notification.body,
            "type": notification.type,
            "is_read": notification.is_read,
            "created_at": str(notification.created_at)
        }, None

    @staticmethod
    def get_announcements(owner_id):
        from app.notifications.models import Notification
        announcements = Notification.query.filter_by(user_id=owner_id).order_by(Notification.created_at.desc()).all()
        result = []
        for a in announcements:
            result.append({
                "id": a.id,
                "title": a.title,
                "body": a.body,
                "type": a.type,
                "is_read": a.is_read,
                "created_at": str(a.created_at)
            })
        return result, None

    @staticmethod
    def delete_announcement(owner_id, announcement_id):
        from app.notifications.models import Notification
        announcement = Notification.query.get(announcement_id)
        if not announcement:
            return False, {"code": "NOT_FOUND", "message": "Announcement not found"}
        
        # Delete related notifications with the same title if desired, or just this one
        db.session.delete(announcement)
        db.session.commit()
        return True, None

