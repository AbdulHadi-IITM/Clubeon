from datetime import datetime
from app.extensions import db
from app.attendance.models import AttendanceRecord
from app.bookings.models import Booking
from app.events.models import Event
from app.clubs.models import Club

class AttendanceService:
    @staticmethod
    def check_in(user_id, booking_id=None, event_id=None):
        if not booking_id and not event_id:
            return None, {"code": "VALIDATION_ERROR", "message": "Must provide booking_id or event_id"}

        if booking_id:
            booking = Booking.query.get(booking_id)
            if not booking or booking.user_id != user_id:
                return None, {"code": "NOT_FOUND", "message": "Booking not found or not owned by user"}
                
        if event_id:
            # Optionally check if user is registered for the event
            # For simplicity, we just check if event exists
            event = Event.query.get(event_id)
            if not event:
                return None, {"code": "NOT_FOUND", "message": "Event not found"}

        # Check if already checked in (active session)
        existing = AttendanceRecord.query.filter_by(
            user_id=user_id,
            booking_id=booking_id,
            event_id=event_id,
            check_out_at=None
        ).first()

        if existing:
            return None, {"code": "CONFLICT", "message": "Already checked in"}

        record = AttendanceRecord(
            user_id=user_id,
            booking_id=booking_id,
            event_id=event_id,
            check_in_at=datetime.utcnow()
        )
        db.session.add(record)
        db.session.commit()
        return record, None

    @staticmethod
    def check_out(user_id, attendance_id):
        record = AttendanceRecord.query.get(attendance_id)
        if not record:
            return False, {"code": "NOT_FOUND", "message": "Attendance record not found"}
            
        if record.user_id != user_id:
            return False, {"code": "FORBIDDEN", "message": "Not authorized"}
            
        if record.check_out_at is not None:
            return False, {"code": "VALIDATION_ERROR", "message": "Already checked out"}

        record.check_out_at = datetime.utcnow()
        db.session.commit()
        return True, None

    @staticmethod
    def get_club_attendance(owner_id, club_id):
        club = Club.query.get(club_id)
        if not club or club.owner_id != owner_id:
            return None, {"code": "FORBIDDEN", "message": "Not authorized to view this club's attendance"}

        # To keep it simple, we fetch all records and filter in python (or use complex joins)
        # For small scale, python filter is fine, or two queries.
        # Let's do two queries to be efficient enough.
        
        # Bookings for this club
        booking_records = AttendanceRecord.query.join(Booking).filter(Booking.court.has(club_id=club_id)).all()
        
        # Events for this club
        event_records = AttendanceRecord.query.join(Event).filter(Event.club_id == club_id).all()
        
        all_records = list(set(booking_records + event_records))
        all_records.sort(key=lambda x: x.check_in_at, reverse=True)
        return all_records, None
