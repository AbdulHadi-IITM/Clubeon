from app.clubs.models import Club, Court
from app.extensions import db

class ClubService:

    @staticmethod
    def create_club(owner_id, name, address, open_time=None, close_time=None, slot_duration=None):
        existing = Club.query.filter_by(owner_id=owner_id).first()
        if existing:
            return None, {"code": "CONFLICT", "message": "You already own a club."}

        # Set defaults if not provided
        club = Club(
            owner_id=owner_id,
            name=name,
            address=address,
            open_time=open_time or "06:00",
            close_time=close_time or "22:00",
            slot_duration_minutes=slot_duration or 60
        )
        db.session.add(club)
        db.session.commit()
        return club, None

    @staticmethod
    def list_clubs(search=None):
        query = Club.query
        if search:
            query = query.filter(Club.name.ilike(f"%{search}%"))
        return query.all()

    @staticmethod
    def get_courts(club_id):
        club = Club.query.get(club_id)
        if not club:
            return None, {"code": "NOT_FOUND", "message": "Club not found"}
        
        courts = Court.query.filter_by(club_id=club_id, is_active=True).all()
        return courts, None

    @staticmethod
    def get_club_by_owner(owner_id):
        return Club.query.filter_by(owner_id=owner_id).first()

    @staticmethod
    def update_club(owner_id, club_id, name=None, address=None, open_time=None, close_time=None, slot_duration=None):
        club = Club.query.get(club_id)
        if not club or club.owner_id != owner_id:
            return None, {"code": "FORBIDDEN", "message": "Not authorized"}

        if name is not None: club.name = name
        if address is not None: club.address = address
        if open_time is not None: club.open_time = open_time if open_time != '' else None
        if close_time is not None: club.close_time = close_time if close_time != '' else None
        if slot_duration is not None:
            if slot_duration != '':
                try:
                    club.slot_duration_minutes = int(slot_duration)
                except ValueError:
                    return None, {"code": "VALIDATION_ERROR", "message": "Slot duration must be a number"}
            else:
                club.slot_duration_minutes = None
        db.session.commit()
        return club, None

class CourtService:
    @staticmethod
    def get_courts_for_owner(owner_id):
        return Court.query.join(Club).filter(Club.owner_id == owner_id).all()

    @staticmethod
    def create_court(owner_id, court_name, club_name=None, club_address=None):
        club = Club.query.filter_by(owner_id=owner_id).first()
        if not club:
            if not club_name or not club_address:
                return None, {"code": "CLUB_REQUIRED", "message": "First time setup: Provide club name and address."}
            # Set default operating hours and slot duration
            club = Club(
                name=club_name,
                address=club_address,
                owner_id=owner_id,
                open_time="06:00",          # default open time
                close_time="22:00",         # default close time
                slot_duration_minutes=60    # default slot length
            )
            db.session.add(club)
            db.session.flush()
        try:
            new_court = Court(name=court_name, club_id=club.id, is_active=True)
            db.session.add(new_court)
            db.session.commit()
            return new_court, None
        except Exception:
            db.session.rollback()
            return None, {"code": "INTERNAL_ERROR", "message": "Failed to create court."}

    @staticmethod
    def delete_court(court_id, owner_id):
        court = Court.query.join(Club).filter(Court.id == court_id, Club.owner_id == owner_id).first()
        if not court:
            return None, {"code": "NOT_FOUND", "message": "Court not found or not owned."}
        db.session.delete(court)
        db.session.commit()
        return True, None

    @staticmethod
    def get_courts_and_club_for_owner(owner_id):
        club = Club.query.filter_by(owner_id=owner_id).first()
        if not club:
            return [], None
        courts = Court.query.filter_by(club_id=club.id).all()
        return courts, club

    @staticmethod
    def update_court(court_id, owner_id, court_name, is_active, open_time_override=None, close_time_override=None, slot_duration_override=None):
        court = Court.query.join(Club).filter(Court.id == court_id, Club.owner_id == owner_id).first()
        if not court:
            return None, {"code": "NOT_FOUND", "message": "Court not found or you do not own it."}

        court.name = court_name
        court.is_active = is_active

        # Always set the override field – if input is None or empty, set to None (clear the override)
        court.open_time_override = None if open_time_override in (None, '') else open_time_override
        court.close_time_override = None if close_time_override in (None, '') else close_time_override

        # Handle slot_duration_override separately (must be int or None)
        if slot_duration_override in (None, ''):
            court.slot_duration_override = None
        else:
            try:
                court.slot_duration_override = int(slot_duration_override)
            except ValueError:
                return None, {"code": "VALIDATION_ERROR", "message": "Slot duration must be a number"}

        db.session.commit()
        return court, None
