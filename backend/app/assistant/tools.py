from app.bookings.services import BookingService
from app.events.services import EventService
from app.availability.services import AvailabilityService
from app.memberships.services import MembershipService
from app.clubs.models import Club, Court
from app.bookings.models import Booking
from app.attendance.models import AttendanceRecord
from datetime import date, datetime
from flask import g
import json
from mirascope import llm

def _get_current_user_id() -> int:
    return getattr(g, "assistant_user_id", 1)

def _get_current_club_id() -> int:
    return getattr(g, "assistant_club_id", 1)

@llm.tool
def get_my_bookings() -> str:
    """Get upcoming bookings for the authenticated user."""
    user_id = _get_current_user_id()
    bookings = BookingService.get_my_bookings(user_id)
    result = []
    for b in bookings:
        result.append({
            "date": str(b.booking_date),
            "start_time": str(b.start_time),
            "end_time": str(b.end_time),
            "status": b.status,
            "court": b.court.name,
            "club": b.court.club.name
        })
    return json.dumps(result)

@llm.tool
def get_events(club_id: int = 1) -> str:
    """Get upcoming events and registration status for a club."""
    events = EventService.get_events(club_id or _get_current_club_id())
    result = []
    for e in events:
        result.append({
            "title": e.title,
            "date": str(e.event_date),
            "time": f"{e.start_time} - {e.end_time}",
            "registered": len(e.registrations),
            "max": e.max_attendees,
            "status": e.status
        })
    return json.dumps(result)

@llm.tool
def get_availability(target_date_str: str = "") -> str:
    """Get live court availability for a specific date (format YYYY-MM-DD). If not provided, defaults to today."""
    club_id = _get_current_club_id()
    dt_str = target_date_str if target_date_str else str(date.today())
    matrix = AvailabilityService.get_availability_matrix(club_id, dt_str)
    if isinstance(matrix, tuple):
        return json.dumps(matrix[1]) if matrix[1] else json.dumps(matrix[0])
    return json.dumps(matrix)

@llm.tool
def get_my_membership() -> str:
    """Get membership and plan information for the authenticated user."""
    user_id = _get_current_user_id()
    memberships = MembershipService.get_my_memberships(user_id)
    result = []
    for m in memberships:
        result.append({
            "plan": m.plan.name,
            "status": m.status,
            "start_date": str(m.start_date),
            "end_date": str(m.end_date)
        })
    return json.dumps(result)

@llm.tool
def get_club_information(club_id: int = 1) -> str:
    """Get club details, operating hours, and active courts."""
    c_id = club_id or _get_current_club_id()
    club = Club.query.get(c_id)
    if not club:
        return json.dumps({"error": "Club not found"})
    courts = Court.query.filter_by(club_id=c_id, is_active=True).count()
    return json.dumps({
        "name": club.name,
        "address": club.address,
        "open_time": str(club.open_time),
        "close_time": str(club.close_time),
        "slot_duration": getattr(club, "slot_duration_minutes", 60),
        "active_courts": courts
    })

@llm.tool
def get_staff_dashboard(target_date_str: str = "") -> str:
    """Get today's operational summary and court dashboard for staff."""
    club_id = _get_current_club_id()
    dt_str = target_date_str if target_date_str else str(date.today())
    target_date = datetime.strptime(dt_str, "%Y-%m-%d").date() if "-" in dt_str else date.today()
    
    total_courts = Court.query.filter_by(club_id=club_id).count()
    active_courts = Court.query.filter_by(club_id=club_id, is_active=True).count()
    bookings_today = Booking.query.join(Court).filter(Court.club_id == club_id, Booking.booking_date == target_date).all()
    active_bookings = len([b for b in bookings_today if b.status == 'confirmed'])
    checked_in = AttendanceRecord.query.filter(AttendanceRecord.check_out_time == None).count()
    
    return json.dumps({
        "total_courts": total_courts,
        "active_courts": active_courts,
        "total_bookings_today": len(bookings_today),
        "active_bookings": active_bookings,
        "checked_in_members": checked_in,
        "pending_arrivals": max(0, active_bookings - checked_in)
    })

@llm.tool
def get_staff_bookings(target_date_str: str = "") -> str:
    """Search staff booking information and player schedules for a date (YYYY-MM-DD)."""
    club_id = _get_current_club_id()
    dt_str = target_date_str if target_date_str else str(date.today())
    target_date = datetime.strptime(dt_str, "%Y-%m-%d").date() if "-" in dt_str else date.today()
    bookings = Booking.query.join(Court).filter(Court.club_id == club_id, Booking.booking_date == target_date).all()
    result = []
    for b in bookings:
        result.append({
            "id": b.id,
            "user": b.user.name if b.user else "Unknown",
            "email": b.user.email if b.user else "Unknown",
            "court": b.court.name,
            "time": f"{b.start_time} - {b.end_time}",
            "status": b.status
        })
    return json.dumps(result)

@llm.tool
def get_staff_attendance() -> str:
    """Get member attendance and check-in records."""
    records = AttendanceRecord.query.all()
    result = []
    for r in records:
        result.append({
            "user": r.user.name if getattr(r, "user", None) else "Unknown",
            "check_in": str(r.check_in_time),
            "check_out": str(r.check_out_time) if r.check_out_time else None
        })
    return json.dumps(result)

@llm.tool
def find_facilities(sport_type: str = "", amenities: str = "", tags: str = "", distance_km: float = 0.0, date: str = "") -> str:
    """Search for clubs and courts by sport type, amenities (e.g. chlorine-free, heated), tags (e.g. kid-friendly, indoor), and max distance in km. Returns ranked results with distance, highlights, and hours."""
    from app.assistant.recommendation_service import RecommendationService
    criteria = {
        "sport_type": sport_type,
        "amenities": amenities,
        "tags": tags,
        "user_lat": getattr(g, "assistant_user_lat", None),
        "user_lon": getattr(g, "assistant_user_lon", None),
        "distance_km": distance_km if distance_km > 0 else None,
        "date": date
    }
    results = RecommendationService.find_clubs_by_criteria(criteria)
    return json.dumps(results)

@llm.tool
def get_club_details(club_id: int = 1) -> str:
    """Get full details of a specific club: amenities, court list, address, and operating hours."""
    club = Club.query.get(club_id)
    if not club:
        return json.dumps({"error": "Club not found"})
    courts = Court.query.filter_by(club_id=club_id, is_active=True).all()
    return json.dumps({
        "club_id": club.id,
        "name": club.name,
        "address": club.address,
        "open_time": str(club.open_time),
        "close_time": str(club.close_time),
        "amenities": club.amenities or [],
        "tags": club.tags or [],
        "courts": [
            {
                "id": c.id,
                "name": c.name,
                "sport_type": c.sport_type,
                "amenities": c.amenities or [],
                "tags": c.tags or []
            }
            for c in courts
        ]
    })

@llm.tool
def get_available_slots_for_club(club_id: int = 1, target_date_str: str = "") -> str:
    """Get all available booking slots grouped by court for a specific club on a given date (YYYY-MM-DD)."""
    dt_str = target_date_str if target_date_str else str(date.today())
    matrix = AvailabilityService.get_availability_matrix(club_id, dt_str)
    if isinstance(matrix, tuple) and matrix[1]:
        return json.dumps(matrix[1])
    
    data = matrix[0] if isinstance(matrix, tuple) else matrix
    summary = {}
    for court in (data or {}).get("courts", []):
        available_slots = [s["time"] for s in court.get("slots", []) if s.get("status") == "available"]
        summary[court["name"]] = available_slots
    return json.dumps({"date": dt_str, "available_slots_by_court": summary})

@llm.tool
def get_court_status(target_date_str: str = "") -> str:
    """Get court availability summary and occupancy count."""
    club_id = _get_current_club_id()
    dt_str = target_date_str if target_date_str else str(date.today())
    matrix = AvailabilityService.get_availability_matrix(club_id, dt_str)
    if isinstance(matrix, tuple) and matrix[1]:
        return json.dumps(matrix[1])
    
    matrix_data = matrix[0] if isinstance(matrix, tuple) else matrix
    summary = {}
    for court in (matrix_data or {}).get('courts', []):
        available = sum(1 for slot in court.get('slots', []) if slot['status'] == 'available')
        booked = sum(1 for slot in court.get('slots', []) if slot['status'] == 'booked')
        blocked = sum(1 for slot in court.get('slots', []) if slot['status'] == 'blocked')
        summary[court['name']] = {
            "available": available,
            "booked": booked,
            "blocked": blocked
        }
    return json.dumps(summary)



