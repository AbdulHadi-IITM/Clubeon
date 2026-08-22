import math
from app.clubs.models import Club, Court
from app.availability.services import AvailabilityService
from datetime import date as dt_date

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance between two points on the Earth in kilometers."""
    R = 6371.0  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    return c * R

class RecommendationService:
    @staticmethod
    def find_clubs_by_criteria(criteria: dict) -> list[dict]:
        """
        Search for clubs and courts by multiple criteria.
        Criteria keys (all optional):
          sport_type   : str   e.g. "swimming", "badminton", "tennis"
          amenities    : list  e.g. ["chlorine-free", "heated", "parking"]
          tags         : list  e.g. ["kid-friendly", "indoor"]
          user_lat     : float
          user_lon     : float
          distance_km  : float e.g. 5.0
          date         : str   YYYY-MM-DD
        """
        sport_type = criteria.get("sport_type")
        amenities = criteria.get("amenities") or []
        if isinstance(amenities, str):
            amenities = [a.strip().lower() for a in amenities.split(",") if a.strip()]
        else:
            amenities = [str(a).strip().lower() for a in amenities if str(a).strip()]

        tags = criteria.get("tags") or []
        if isinstance(tags, str):
            tags = [t.strip().lower() for t in tags.split(",") if t.strip()]
        else:
            tags = [str(t).strip().lower() for t in tags if str(t).strip()]

        user_lat = criteria.get("user_lat")
        user_lon = criteria.get("user_lon")
        distance_km = criteria.get("distance_km")
        if distance_km is not None:
            try:
                distance_km = float(distance_km)
            except (ValueError, TypeError):
                distance_km = None

        query = Court.query.join(Club).filter(Court.is_active == True)

        if sport_type and str(sport_type).strip():
            st = str(sport_type).strip().lower()
            query = query.filter(Court.sport_type.ilike(f"%{st}%"))

        courts = query.all()
        results = []

        for court in courts:
            club = court.club
            if not club:
                continue

            court_amenities = [str(a).lower() for a in (court.amenities or [])]
            court_tags = [str(t).lower() for t in (court.tags or [])]
            club_amenities = [str(a).lower() for a in (club.amenities or [])]
            club_tags = [str(t).lower() for t in (club.tags or [])]

            combined_amenities = set(court_amenities + club_amenities)
            combined_tags = set(court_tags + club_tags)

            # Match amenities
            if amenities:
                if not any(
                    any(req in am for am in combined_amenities)
                    for req in amenities
                ):
                    continue

            # Match tags
            if tags:
                if not any(
                    any(req in tg for tg in combined_tags)
                    for req in tags
                ):
                    continue

            # Geolocation calculation
            dist = None
            if user_lat is not None and user_lon is not None and club.latitude is not None and club.longitude is not None:
                try:
                    dist = haversine_km(float(user_lat), float(user_lon), float(club.latitude), float(club.longitude))
                    if distance_km and distance_km > 0 and dist > distance_km:
                        continue
                except (ValueError, TypeError):
                    dist = None

            results.append({
                "club_id": club.id,
                "club_name": club.name,
                "court_id": court.id,
                "court_name": court.name,
                "sport_type": court.sport_type,
                "address": club.address or "Address not specified",
                "distance_km": round(dist, 1) if dist is not None else None,
                "amenities": list(combined_amenities),
                "tags": list(combined_tags),
                "open_time": str(club.open_time or "06:00"),
                "close_time": str(club.close_time or "22:00")
            })

        # Sort by distance (if available) or club name
        results.sort(key=lambda r: (r["distance_km"] if r["distance_km"] is not None else 9999, r["club_name"]))
        return results
