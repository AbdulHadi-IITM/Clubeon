from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.bookings.models import Booking

class BookingService:

    @staticmethod
    def create_booking(user_id, court_id, booking_date, start_time, end_time):
        """
        Creates a new booking. Returns a tuple: (Booking Object, Error Dictionary)
        """
        try:
            new_booking = Booking(
                user_id=user_id,
                court_id=court_id,
                booking_date=booking_date,
                start_time=start_time,
                end_time=end_time
            )
            db.session.add(new_booking)
            db.session.commit()

            return new_booking, None

        except IntegrityError:
            # This triggers if the GiST overlap constraint fails
            db.session.rollback()
            return None, {
                "code": "CONCURRENCY_CONFLICT",
                "message": "This slot was just booked by another member."
            }
        except Exception as e:
            db.session.rollback()
            return None, {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred."
            }