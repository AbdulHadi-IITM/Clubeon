from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.bookings.models import Booking, Court, Club

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

class AuthorizationService:

    @staticmethod
    def verify_court_ownership(court_id, owner_id):
        """
        Validates that the provided owner_id is the actual owner of the court's club.
        """
        # We join Court and Club to check ownership in a single, efficient query
        court = Court.query.join(Club).filter(
            Court.id == court_id,
            Club.owner_id == owner_id
        ).first()

        return court is not None

class CourtService:
    @staticmethod
    def get_courts_for_owner(owner_id):
        """Get all courts belonging to the owner's club."""
        return Court.query.join(Club).filter(Club.owner_id == owner_id).all()

    @staticmethod
    def create_court(owner_id, court_name, club_name=None, club_address=None):
        """
        Creates a new court. If the owner doesn't have a club yet, creates the club first.
        Returns: (Court Object, Error Dictionary)
        """
        # 1. Check if the owner already has a club
        club = Club.query.filter_by(owner_id=owner_id).first()

        if not club:
            # 2. If no club exists, require club details to create one
            if not club_name or not club_address:
                return None, {
                    "code": "CLUB_REQUIRED",
                    "message": "First time setup: Please provide a club name and address to create your facility."
                }
            club = Club(name=club_name, address=club_address, owner_id=owner_id)
            db.session.add(club)
            db.session.flush()  # Generates club.id without committing the full transaction yet

        try:
            new_court = Court(name=court_name, club_id=club.id, is_active=True)
            db.session.add(new_court)
            db.session.commit()
            return new_court, None
        except Exception as e:
            db.session.rollback()
            return None, {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred while creating the court."
            }

    @staticmethod
    def update_court(court_id, owner_id, court_name, is_active):
        court = Court.query.join(Club).filter(Court.id == court_id, Club.owner_id == owner_id).first()
        if not court:
            return None, {"code": "NOT_FOUND", "message": "Court not found or you do not own it."}

        court.name = court_name
        court.is_active = is_active
        db.session.commit()
        return court, None

    @staticmethod
    def delete_court(court_id, owner_id):
        court = Court.query.join(Club).filter(Court.id == court_id, Club.owner_id == owner_id).first()
        if not court:
            return None, {"code": "NOT_FOUND", "message": "Court not found or you do not own it."}

        db.session.delete(court)
        db.session.commit()
        return True, None