from datetime import datetime

from app.auth.models import User
from app.extensions import db
from app.bookings.models import Booking, CourtBlock
from app.clubs.models import Court, Club
from app.memberships.models import Membership


class AdminService:
    @staticmethod
    def override_booking(owner_id, booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return False, {"code": "NOT_FOUND", "message": "Booking not found"}
        
        # Verify ownership (The owner of the club that owns the court)
        if booking.court.club.owner_id != owner_id:
            return False, {"code": "FORBIDDEN", "message": "Not authorized to override bookings for this club"}

        if booking.status not in ('active', 'pending'):
            return False, {"code": "VALIDATION_ERROR", "message": f"Booking is already {booking.status}"}

        booking.status = 'overridden'
        db.session.commit()
        return True, None

    @staticmethod
    def cancel_booking(owner_id, booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return False, {"code": "NOT_FOUND", "message": "Booking not found"}
        
        # Verify ownership
        if booking.court.club.owner_id != owner_id:
            return False, {"code": "FORBIDDEN", "message": "Not authorized to cancel bookings for this club"}

        if booking.status in ('cancelled', 'overridden'):
            return False, {"code": "VALIDATION_ERROR", "message": f"Booking is already {booking.status}"}

        booking.status = 'cancelled'
        db.session.commit()
        return True, None

    @staticmethod
    def complete_booking(owner_id, booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return False, {"code": "NOT_FOUND", "message": "Booking not found"}
        
        # Verify ownership
        if booking.court.club.owner_id != owner_id:
            return False, {"code": "FORBIDDEN", "message": "Not authorized to complete bookings for this club"}

        booking.status = 'completed'
        db.session.commit()
        return True, None

    @staticmethod
    def get_bookings(owner_id, member_id=None, status=None, court_id=None, date_str=None, search=None):
        """Return bookings belonging to clubs owned by this admin.

        If member_id is supplied, only that member's bookings are returned.
        Supports filtering by status, court_id, date, and search term.
        """
        from app.bookings.models import Booking
        from app.clubs.models import Court, Club
        from app.auth.models import User

        query = (
            Booking.query
            .join(Booking.court)
            .join(Court.club)
            .filter(Club.owner_id == owner_id)
        )

        if member_id is not None:
            query = query.filter(Booking.user_id == member_id)
        if status and status.lower() != 'all':
            if status.lower() in ('confirmed', 'active'):
                query = query.filter(Booking.status.in_(['active', 'confirmed']))
            elif status.lower() in ('cancelled', 'overridden', 'released'):
                query = query.filter(Booking.status.in_(['cancelled', 'overridden', 'released']))
            else:
                query = query.filter(Booking.status.ilike(status))
        if court_id is not None:
            query = query.filter(Booking.court_id == court_id)
        if date_str:
            try:
                parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                query = query.filter(Booking.booking_date == parsed_date)
            except ValueError:
                pass
        if search and search.strip():
            search_term = f"%{search.strip()}%"
            query = query.join(Booking.user).filter(
                db.or_(
                    User.name.ilike(search_term),
                    User.email.ilike(search_term),
                    Court.name.ilike(search_term)
                )
            )

        return query.order_by(
            Booking.booking_date.desc(),
            Booking.start_time.desc(),
            Booking.id.desc(),
        ).all()


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
    def get_members(owner_id):
        from app.auth.models import User
        from app.bookings.models import Booking
        from app.clubs.models import Court, Club
        from app.memberships.models import Membership

        users = User.query.filter(User.role.in_(['player', 'member', 'front-desk', 'owner'])).all()
        result = []
        for u in users:
            b_count = (
                Booking.query
                .join(Booking.court)
                .join(Court.club)
                .filter(Club.owner_id == owner_id, Booking.user_id == u.id)
                .count()
            )
            active_m = Membership.query.filter_by(user_id=u.id, status='active').first()
            plan_name = active_m.plan.name if active_m and active_m.plan else ('VIP Pass' if u.role == 'owner' else 'Standard Member')
            
            result.append({
                'id': u.id,
                'name': u.name,
                'email': u.email,
                'role': u.role,
                'status': 'Active' if u.is_active else 'Suspended',
                'plan': plan_name,
                'bookings_count': b_count,
                'phone': '+1 (555) 234-5678',
                'date_joined': u.created_at.strftime('%b %d, %Y') if u.created_at else 'Jan 15, 2026',
            })
        return result

    @staticmethod
    def list_club_members(owner_id):
        return AdminService.get_members(owner_id), None

    @staticmethod
    def get_events(owner_id):
        from app.events.models import Event, EventRegistration
        from app.clubs.models import Club

        clubs = Club.query.filter_by(owner_id=owner_id).all()
        club_ids = [c.id for c in clubs]

        events = Event.query.filter(Event.club_id.in_(club_ids)).order_by(Event.event_date.desc()).all() if club_ids else []
        result = []
        for e in events:
            reg_count = EventRegistration.query.filter_by(event_id=e.id, status='registered').count()
            result.append({
                'id': e.id,
                'title': e.title,
                'description': e.description or '',
                'club_id': e.club_id,
                'sport': 'Tennis' if 'tennis' in e.title.lower() else 'General',
                'event_date': str(e.event_date),
                'start_time': str(e.start_time)[:5] if e.start_time else '',
                'end_time': str(e.end_time)[:5] if e.end_time else '',
                'max_attendees': e.max_attendees or 50,
                'registered_count': reg_count,
                'registration_fee': float(e.registration_fee or 0.0),
                'status': e.status or 'upcoming',
            })
        return result

    @staticmethod
    def get_analytics(owner_id):
        from app.bookings.models import Booking
        from app.clubs.models import Court, Club

        bookings = (
            Booking.query
            .join(Booking.court)
            .join(Court.club)
            .filter(Club.owner_id == owner_id)
            .all()
        )

        total_bookings = len(bookings)
        completed_bookings = len([b for b in bookings if b.status == 'completed'])
        active_bookings = len([b for b in bookings if b.status in ('active', 'confirmed')])
        cancelled_bookings = len([b for b in bookings if b.status in ('cancelled', 'overridden', 'released')])

        sport_counts = {}
        for b in bookings:
            sport = b.court.sport_type if b.court else 'Other'
            sport_counts[sport] = sport_counts.get(sport, 0) + 1

        total_revenue = sum([40 for b in bookings if b.status in ('active', 'completed')])

        return {
            'total_bookings': total_bookings,
            'active_bookings': active_bookings,
            'completed_bookings': completed_bookings,
            'cancelled_bookings': cancelled_bookings,
            'total_revenue': total_revenue,
            'sport_breakdown': sport_counts,
        }

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
        
        db.session.delete(announcement)
        db.session.commit()
        return True, None


