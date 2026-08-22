from datetime import datetime
from app.extensions import db
from app.events.models import Event, EventRegistration
from app.clubs.models import Club

class EventService:
    @staticmethod
    def get_events(club_id=None):
        query = Event.query.filter(Event.status == 'upcoming')
        if club_id:
            query = query.filter_by(club_id=club_id)
        return query.order_by(Event.event_date.asc(), Event.start_time.asc()).all()

    @staticmethod
    def get_all_events(club_id=None):
        query = Event.query
        if club_id:
            query = query.filter_by(club_id=club_id)
        return query.order_by(Event.event_date.desc(), Event.start_time.asc()).all()

    @staticmethod
    def get_event_by_id(event_id):
        return Event.query.get(event_id)

    @staticmethod
    def update_event(user_id, event_id, data):
        event = Event.query.get(event_id)
        if not event:
            return None, {"code": "NOT_FOUND", "message": "Event not found"}

        club = Club.query.get(event.club_id)
        if club and club.owner_id != user_id and event.created_by != user_id:
            user_club = Club.query.filter_by(owner_id=user_id).first()
            if not user_club:
                return None, {"code": "FORBIDDEN", "message": "Not authorized to update this event"}

        if 'title' in data:
            event.title = data['title']
        if 'description' in data:
            event.description = data['description']
        if 'event_date' in data and data['event_date']:
            try:
                event.event_date = datetime.strptime(data['event_date'], "%Y-%m-%d").date()
            except ValueError:
                return None, {"code": "VALIDATION_ERROR", "message": "Invalid date format. Use YYYY-MM-DD."}
        if 'start_time' in data and data['start_time']:
            try:
                event.start_time = datetime.strptime(data['start_time'], "%H:%M").time()
            except ValueError:
                return None, {"code": "VALIDATION_ERROR", "message": "Invalid start_time format. Use HH:MM."}
        if 'end_time' in data and data['end_time']:
            try:
                event.end_time = datetime.strptime(data['end_time'], "%H:%M").time()
            except ValueError:
                return None, {"code": "VALIDATION_ERROR", "message": "Invalid end_time format. Use HH:MM."}
        if 'max_attendees' in data:
            event.max_attendees = data['max_attendees']
        if 'registration_fee' in data:
            event.registration_fee = float(data['registration_fee'])
        was_not_cancelled = (event.status != 'cancelled')
        if 'status' in data:
            event.status = data['status']

        db.session.commit()

        if was_not_cancelled and event.status == 'cancelled':
            EventService._broadcast_event_cancellation_announcement(event)

        return event, None

    @staticmethod
    def _broadcast_event_cancellation_announcement(event):
        try:
            from app.notifications.models import Notification
            from app.clubs.models import Club

            # 1. Notify all registered users
            registrations = EventRegistration.query.filter_by(event_id=event.id).all()
            registered_user_ids = set()
            for reg in registrations:
                registered_user_ids.add(reg.user_id)
                notif = Notification(
                    user_id=reg.user_id,
                    title=f"Event Cancelled: {event.title}",
                    body=f"The event '{event.title}' scheduled for {event.event_date} ({str(event.start_time)[:5]} - {str(event.end_time)[:5]}) has been cancelled. Any fees paid will be credited according to club policies.",
                    type="Tournament"
                )
                db.session.add(notif)

            # 2. Notify the club owner / admin
            admin_id = event.created_by
            if event.club_id:
                club = Club.query.get(event.club_id)
                if club and club.owner_id:
                    admin_id = club.owner_id

            if admin_id and admin_id not in registered_user_ids:
                admin_notif = Notification(
                    user_id=admin_id,
                    title=f"Event Cancelled: {event.title}",
                    body=f"Event '{event.title}' scheduled for {event.event_date} was cancelled. Cancellation notices have been dispatched to all {len(registered_user_ids)} registered attendees.",
                    type="Tournament"
                )
                db.session.add(admin_notif)

            # 3. Global announcement broadcast for event cancellation
            global_announcement = Notification(
                user_id=admin_id or 1,
                title=f"Event Cancelled: {event.title}",
                body=f"Notice: The event '{event.title}' scheduled for {event.event_date} has been cancelled.",
                type="Tournament"
            )
            db.session.add(global_announcement)
            db.session.commit()
        except Exception as e:
            print(f"Error broadcasting event cancellation announcement: {e}")

    @staticmethod
    def delete_event(user_id, event_id):
        event = Event.query.get(event_id)
        if not event:
            return False, {"code": "NOT_FOUND", "message": "Event not found"}

        club = Club.query.get(event.club_id)
        if club and club.owner_id != user_id and event.created_by != user_id:
            user_club = Club.query.filter_by(owner_id=user_id).first()
            if not user_club:
                return False, {"code": "FORBIDDEN", "message": "Not authorized to cancel this event"}

        event.status = 'cancelled'
        db.session.commit()

        # Broadcast cancellation announcement to admin and all attendees
        EventService._broadcast_event_cancellation_announcement(event)
        return True, None

    @staticmethod
    def create_event(user_id, club_id, title, description, event_date_str, start_time_str, end_time_str, max_attendees, registration_fee):
        try:
            event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            end_time = datetime.strptime(end_time_str, "%H:%M").time()
        except ValueError:
            return None, {"code": "VALIDATION_ERROR", "message": "Invalid date or time format"}

        club = None
        if club_id:
            club = Club.query.get(club_id)
        if not club or club.owner_id != user_id:
            user_club = Club.query.filter_by(owner_id=user_id).first()
            if user_club:
                club = user_club
                club_id = club.id
            elif club and club.owner_id == user_id:
                pass
            elif not club:
                club = Club.query.first()
                if club:
                    club_id = club.id
                else:
                    return None, {"code": "NOT_FOUND", "message": "Club not found"}

        event = Event(
            club_id=club_id,
            created_by=user_id,
            title=title,
            description=description,
            event_date=event_date,
            start_time=start_time,
            end_time=end_time,
            max_attendees=max_attendees,
            registration_fee=registration_fee,
            status='upcoming'
        )
        db.session.add(event)
        db.session.commit()
        return event, None

    @staticmethod
    def register(user_id, event_id):
        event = Event.query.get(event_id)
        if not event:
            return None, {"code": "NOT_FOUND", "message": "Event not found"}
            
        if event.status != 'upcoming':
            return None, {"code": "VALIDATION_ERROR", "message": "Can only register for upcoming events"}

        # Check if already registered
        existing = EventRegistration.query.filter_by(event_id=event_id, user_id=user_id).first()
        if existing:
            if existing.status == 'registered':
                return None, {"code": "CONFLICT", "message": "Already registered for this event"}
            else:
                existing.status = 'registered'
                db.session.commit()
                return existing, None

        # Check capacity
        if event.max_attendees:
            current_count = EventRegistration.query.filter_by(event_id=event_id, status='registered').count()
            if current_count >= event.max_attendees:
                return None, {"code": "CONFLICT", "message": "Event is full"}

        registration = EventRegistration(
            event_id=event_id,
            user_id=user_id,
            status='registered'
        )
        db.session.add(registration)
        db.session.commit()
        return registration, None

    @staticmethod
    def cancel_registration(user_id, event_id):
        registration = EventRegistration.query.filter_by(event_id=event_id, user_id=user_id).first()
        if not registration:
            return False, {"code": "NOT_FOUND", "message": "Registration not found"}
            
        if registration.status == 'cancelled':
            return False, {"code": "VALIDATION_ERROR", "message": "Registration is already cancelled"}

        registration.status = 'cancelled'
        db.session.commit()
        return True, None
