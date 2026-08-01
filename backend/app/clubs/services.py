from app.clubs.models import Club, Court

class ClubService:
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
