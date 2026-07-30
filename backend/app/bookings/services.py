from datetime import datetime
from app.extensions import db
from app.bookings.models import Booking
from app.clubs.models import Court

class BookingService:
    @staticmethod
    def create_booking(user_id, court_id, booking_date_str, start_time_str, end_time_str):
        try:
            booking_date = datetime.strptime(booking_date_str, "%Y-%m-%d").date()
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            end_time = datetime.strptime(end_time_str, "%H:%M").time()
        except ValueError:
            return None, {"code": "VALIDATION_ERROR", "message": "Invalid date or time format."}

        if start_time >= end_time:
            return None, {"code": "VALIDATION_ERROR", "message": "Start time must be before end time."}

        court = Court.query.get(court_id)
        if not court or not court.is_active:
            return None, {"code": "NOT_FOUND", "message": "Court not found or inactive."}

        # Check for overlapping active bookings (Application-level lock)
        # In a real high-concurrency environment without ExcludeConstraint, we'd use SELECT FOR UPDATE or similar
        # Since SQLite doesn't have GiST, we do a manual check.
        overlapping = Booking.query.filter(
            Booking.court_id == court_id,
            Booking.booking_date == booking_date,
            Booking.status == 'active',
            Booking.start_time < end_time,
            Booking.end_time > start_time
        ).first()

        if overlapping:
            return None, {"code": "CONFLICT", "message": "This time slot is already booked."}

        new_booking = Booking(
            user_id=user_id,
            court_id=court_id,
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time,
            status='active'
        )
        db.session.add(new_booking)
        db.session.commit()
        return new_booking, None

    @staticmethod
    def get_my_bookings(user_id):
        return Booking.query.filter_by(user_id=user_id).order_by(Booking.booking_date.desc(), Booking.start_time.desc()).all()

    @staticmethod
    def release_booking(user_id, booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return False, {"code": "NOT_FOUND", "message": "Booking not found"}
        
        if booking.user_id != user_id:
            return False, {"code": "FORBIDDEN", "message": "Not authorized to release this booking"}

        if booking.status != 'active':
            return False, {"code": "VALIDATION_ERROR", "message": f"Booking is already {booking.status}"}

        booking.status = 'released'
        db.session.commit()
        return True, None