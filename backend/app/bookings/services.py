from datetime import datetime, timedelta, date as dt_date, time as dt_time
import uuid
from app.extensions import db
from app.bookings.models import Booking, BookingIntent
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

        booking_start = datetime.combine(booking_date, start_time)
        if booking_start <= datetime.now():
            return None, {
                "code": "VALIDATION_ERROR",
                "message": "This time slot has already passed. Please choose a future slot.",
            }

        court = Court.query.get(court_id)
        if not court or not court.is_active:
            return None, {"code": "NOT_FOUND", "message": "Court not found or inactive."}

        # Check for overlapping active bookings
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
    def prepare_intent(user_id, court_id, booking_date_str, start_time_str, end_time_str=None):
        """Prepare a 5-minute temporary hold and booking preview draft."""
        try:
            booking_date = datetime.strptime(booking_date_str, "%Y-%m-%d").date()
            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            if end_time_str:
                end_time = datetime.strptime(end_time_str, "%H:%M").time()
            else:
                end_hour = (start_time.hour + 1) % 24
                end_time = dt_time(end_hour, start_time.minute)
        except ValueError:
            return None, {"code": "VALIDATION_ERROR", "message": "Invalid date (YYYY-MM-DD) or time (HH:MM) format."}

        booking_start = datetime.combine(booking_date, start_time)
        if booking_start <= datetime.now():
            return None, {
                "code": "VALIDATION_ERROR",
                "message": "This time slot has already passed. Please select a future time.",
            }

        court = Court.query.get(court_id)
        if not court or not court.is_active:
            return None, {"code": "NOT_FOUND", "message": "Court not found or inactive."}

        # Check for overlapping active bookings
        overlapping = Booking.query.filter(
            Booking.court_id == court_id,
            Booking.booking_date == booking_date,
            Booking.status == 'active',
            Booking.start_time < end_time,
            Booking.end_time > start_time
        ).first()

        if overlapping:
            return None, {"code": "CONFLICT", "message": f"Slot {start_time_str} - {end_time.strftime('%H:%M')} on {court.name} is already booked."}

        # Clear any prior stale pending intents for this user
        BookingIntent.query.filter_by(user_id=user_id, status='pending').update({'status': 'expired'})
        db.session.commit()

        intent_id = f"int_{uuid.uuid4().hex[:12]}"
        expires_at = datetime.now() + timedelta(minutes=10)

        intent = BookingIntent(
            id=intent_id,
            user_id=user_id,
            court_id=court_id,
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time,
            status='pending',
            expires_at=expires_at
        )
        db.session.add(intent)
        db.session.commit()
        return intent, None

    @staticmethod
    def confirm_intent(user_id, intent_id):
        """Atomically confirm a pending booking intent into an active booking."""
        intent = BookingIntent.query.get(intent_id)
        if not intent:
            return None, {"code": "NOT_FOUND", "message": "Booking intent draft not found."}

        if intent.user_id != user_id:
            return None, {"code": "FORBIDDEN", "message": "Not authorized to confirm this booking."}

        if intent.status == 'confirmed':
            existing = Booking.query.filter_by(
                user_id=user_id,
                court_id=intent.court_id,
                booking_date=intent.booking_date,
                start_time=intent.start_time
            ).first()
            if existing:
                return existing, None

        if intent.status != 'pending':
            return None, {"code": "VALIDATION_ERROR", "message": f"This booking draft has already been {intent.status}."}

        if intent.expires_at < (datetime.now() - timedelta(minutes=1)):
            intent.status = 'expired'
            db.session.commit()
            return None, {"code": "EXPIRED", "message": "This booking hold has expired. Please start a new booking."}

        # Re-verify no conflicts
        overlapping = Booking.query.filter(
            Booking.court_id == intent.court_id,
            Booking.booking_date == intent.booking_date,
            Booking.status == 'active',
            Booking.start_time < intent.end_time,
            Booking.end_time > intent.start_time
        ).first()

        if overlapping:
            intent.status = 'expired'
            db.session.commit()
            return None, {"code": "CONFLICT", "message": "This slot was just booked by another player. Please select another slot."}

        new_booking = Booking(
            user_id=intent.user_id,
            court_id=intent.court_id,
            booking_date=intent.booking_date,
            start_time=intent.start_time,
            end_time=intent.end_time,
            status='active'
        )
        intent.status = 'confirmed'
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