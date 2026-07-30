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
    def create_event(user_id, club_id, title, description, event_date_str, start_time_str, end_time_str, max_attendees, registration_fee):
        try:
            event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            end_time = datetime.strptime(end_time_str, "%H:%M").time()
        except ValueError:
            return None, {"code": "VALIDATION_ERROR", "message": "Invalid date or time format"}

        club = Club.query.get(club_id)
        if not club:
            return None, {"code": "NOT_FOUND", "message": "Club not found"}
            
        if club.owner_id != user_id:
            return None, {"code": "FORBIDDEN", "message": "Not authorized to create events for this club"}

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
