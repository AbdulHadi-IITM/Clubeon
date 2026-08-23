from app.bookings.services import BookingService
from app.events.services import EventService
from app.availability.services import AvailabilityService
from app.memberships.services import MembershipService
from app.clubs.models import Club, Court
from app.bookings.models import Booking, BookingIntent
from app.attendance.models import AttendanceRecord
from datetime import date, datetime, timedelta
from flask import g
import json
import re
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
    checked_in = AttendanceRecord.query.filter(AttendanceRecord.check_out_at == None).count()
    
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
            "check_in": str(r.check_in_at) if r.check_in_at else None,
            "check_out": str(r.check_out_at) if r.check_out_at else None
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
    dt_str = _parse_human_date(target_date_str) if target_date_str else str(date.today())
    matrix = AvailabilityService.get_availability_matrix(club_id, dt_str)
    if isinstance(matrix, tuple) and matrix[1]:
        return json.dumps(matrix[1])
    
    data = matrix[0] if isinstance(matrix, tuple) else matrix
    summary = {}
    for court in (data or {}).get("courts", []):
        c_name = court.get("court_name") or court.get("name", "Court")
        available_slots = [
            f"{s.get('start_time')} - {s.get('end_time')}"
            for s in court.get("slots", [])
            if s.get("status") == "available"
        ]
        summary[c_name] = available_slots
    return json.dumps({"date": dt_str, "available_slots_by_court": summary})

@llm.tool
def get_court_status(target_date_str: str = "") -> str:
    """Get court availability summary and occupancy count."""
    club_id = _get_current_club_id()
    dt_str = _parse_human_date(target_date_str) if target_date_str else str(date.today())
    matrix = AvailabilityService.get_availability_matrix(club_id, dt_str)
    if isinstance(matrix, tuple) and matrix[1]:
        return json.dumps(matrix[1])
    
    matrix_data = matrix[0] if isinstance(matrix, tuple) else matrix
    summary = {}
    for court in (matrix_data or {}).get('courts', []):
        c_name = court.get('court_name') or court.get('name', 'Court')
        available = sum(1 for slot in court.get('slots', []) if slot['status'] == 'available')
        booked = sum(1 for slot in court.get('slots', []) if slot['status'] == 'booked')
        blocked = sum(1 for slot in court.get('slots', []) if slot['status'] == 'blocked')
        summary[c_name] = {
            "available": available,
            "booked": booked,
            "blocked": blocked
        }
    return json.dumps(summary)

def _parse_human_date(date_str: str) -> str:
    if not date_str:
        return str(date.today())
    raw = date_str.strip().lower()
    today = date.today()
    
    # Common slang and abbreviations
    if raw in ["today", "tdy", "tod"]:
        return str(today)
    if raw in ["tomorrow", "tmrw", "tmr", "tom", "tomm", "next day"]:
        return str(today + timedelta(days=1))
    if raw in ["day after tomorrow", "day after tmrw"]:
        return str(today + timedelta(days=2))
    if raw in ["yesterday"]:
        return str(today - timedelta(days=1))

    # Day of week (e.g. "monday", "next tuesday", "this friday")
    weekdays = {
        "monday": 0, "mon": 0,
        "tuesday": 1, "tue": 1, "tues": 1,
        "wednesday": 2, "wed": 2,
        "thursday": 3, "thu": 3, "thur": 3, "thurs": 3,
        "friday": 4, "fri": 4,
        "saturday": 5, "sat": 5,
        "sunday": 6, "sun": 6,
    }
    for day_name, target_weekday in weekdays.items():
        if day_name in raw:
            days_ahead = target_weekday - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            if "next" in raw and days_ahead < 7:
                days_ahead += 7
            return str(today + timedelta(days=days_ahead))

    # Match YYYY-MM-DD
    ymd_match = re.search(r"(\d{4})[./\-](\d{1,2})[./\-](\d{1,2})", raw)
    if ymd_match:
        y, m, d = int(ymd_match.group(1)), int(ymd_match.group(2)), int(ymd_match.group(3))
        try:
            return str(date(y, m, d))
        except ValueError:
            pass

    # Match DD-MM-YYYY or DD/MM/YYYY
    dmy_match = re.search(r"(\d{1,2})[./\-](\d{1,2})[./\-](\d{4})", raw)
    if dmy_match:
        d, m, y = int(dmy_match.group(1)), int(dmy_match.group(2)), int(dmy_match.group(3))
        try:
            return str(date(y, m, d))
        except ValueError:
            pass

    # Match named months (e.g., "24 Aug", "Aug 24", "24th August")
    months = {
        "jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3,
        "apr": 4, "april": 4, "may": 5, "jun": 6, "june": 6, "jul": 7, "july": 7,
        "aug": 8, "august": 8, "sep": 9, "september": 9, "oct": 10, "october": 10,
        "nov": 11, "november": 11, "dec": 12, "december": 12
    }
    for m_name, m_num in months.items():
        if m_name in raw:
            d_match = re.search(r"\b(\d{1,2})(?:st|nd|rd|th)?\b", raw)
            if d_match:
                d = int(d_match.group(1))
                y = today.year
                y_match = re.search(r"\b(20\d{2})\b", raw)
                if y_match:
                    y = int(y_match.group(1))
                try:
                    return str(date(y, m_num, d))
                except ValueError:
                    pass

    return str(today)

def _parse_human_time(time_str: str) -> tuple[str, str]:
    """Parse time string into (start_time_HH:MM, end_time_HH:MM)."""
    if not time_str:
        return "06:00", "07:00"
    raw = time_str.strip().lower()

    parts = None
    for sep in [" to ", " - ", "-", "–", "—", " until ", " till "]:
        if sep in raw:
            split_parts = [p.strip() for p in raw.split(sep, 1)]
            if len(split_parts) == 2 and split_parts[0] and split_parts[1]:
                parts = split_parts
                break

    def _parse_single_time(t_str: str, fallback_am_pm: str = None) -> tuple[int, int]:
        s = t_str.strip().lower()
        is_pm = any(k in s for k in ["pm", "p.m.", "evening", "night", "afternoon"])
        is_am = any(k in s for k in ["am", "a.m.", "morning"])
        
        if not is_pm and not is_am and fallback_am_pm:
            is_pm = (fallback_am_pm == "pm")
            is_am = (fallback_am_pm == "am")

        clean = re.sub(r"[^\d:]", "", s)
        if ":" in clean:
            h_str, m_str = clean.split(":", 1)
            hour = int(h_str) if h_str else 6
            minute = int(m_str) if m_str else 0
        elif clean.isdigit():
            hour = int(clean)
            minute = 0
        else:
            return 6, 0

        if is_pm and hour < 12:
            hour += 12
        elif is_am and hour == 12:
            hour = 0

        return hour, minute

    if parts:
        second_part = parts[1]
        shared_period = "pm" if ("pm" in second_part or "evening" in second_part) else ("am" if "am" in second_part else None)
        
        s_h, s_m = _parse_single_time(parts[0], fallback_am_pm=shared_period)
        e_h, e_m = _parse_single_time(parts[1], fallback_am_pm=shared_period)
        
        if (e_h, e_m) <= (s_h, s_m):
            e_h = (s_h + 1) % 24
        
        return f"{s_h:02d}:{s_m:02d}", f"{e_h:02d}:{e_m:02d}"
    else:
        s_h, s_m = _parse_single_time(raw)
        e_h = (s_h + 1) % 24
        return f"{s_h:02d}:{s_m:02d}", f"{e_h:02d}:{e_m:02d}"

@llm.tool
def prepare_court_booking(court_name: str = "", court_id: int = 0, target_date: str = "", start_time: str = "") -> str:
    """Prepare a temporary 5-minute booking draft hold for a court. Does NOT finalize without user confirmation. Provide court name or id, date (supports 'today', 'tomorrow', 'tmrw', 'YYYY-MM-DD', weekday names), and start time ('6 PM', '18:00', '6am to 7am'). Returns draft details or available alternatives if unavailable."""
    user_id = _get_current_user_id()
    c_id = court_id
    court_obj = None

    if c_id:
        court_obj = Court.query.get(c_id)
    elif court_name:
        court_obj = Court.query.filter(Court.name.ilike(f"%{court_name.strip()}%"), Court.is_active == True).first()
        if not court_obj:
            clean_name = court_name.lower().replace("court", "").strip()
            court_obj = Court.query.filter(Court.name.ilike(f"%{clean_name}%"), Court.is_active == True).first()
        if not court_obj:
            court_obj = Court.query.filter(Court.sport_type.ilike(f"%{court_name.strip()}%"), Court.is_active == True).first()

    if not court_obj:
        court_obj = Court.query.filter_by(is_active=True).first()

    c_id = court_obj.id if court_obj else 1
    dt_str = _parse_human_date(target_date)
    st_str, et_str = _parse_human_time(start_time)

    intent, error = BookingService.prepare_intent(
        user_id=user_id,
        court_id=c_id,
        booking_date_str=dt_str,
        start_time_str=st_str,
        end_time_str=et_str
    )

    if error:
        # Get alternative available slots on this court for the user
        matrix_res = AvailabilityService.get_availability_matrix(court_obj.club_id if court_obj else 1, dt_str)
        data = matrix_res[0] if isinstance(matrix_res, tuple) else matrix_res
        available_slots = []
        for c in (data or {}).get("courts", []):
            is_matching_court = (
                c.get("court_id") == c_id or 
                c.get("id") == c_id or 
                (court_obj and c.get("court_name", "").lower() == court_obj.name.lower())
            )
            if is_matching_court:
                available_slots = [
                    f"{s.get('start_time')} - {s.get('end_time')}"
                    for s in c.get("slots", [])
                    if s.get("status") == "available"
                ]
                break

        return json.dumps({
            "status": "unavailable",
            "error": error.get("message", "This slot is unavailable."),
            "court_name": court_obj.name if court_obj else "Court",
            "date": dt_str,
            "requested_time": f"{st_str} - {et_str}",
            "available_slots": available_slots,
            "requires_confirmation": False
        })

    court = intent.court
    return json.dumps({
        "status": "draft_prepared",
        "intent_id": intent.id,
        "court_id": court.id,
        "court_name": court.name,
        "club_name": court.club.name if court.club else "ClubDash Arena",
        "booking_date": str(intent.booking_date),
        "start_time": str(intent.start_time),
        "end_time": str(intent.end_time),
        "expires_in_minutes": 5,
        "requires_confirmation": True
    })

@llm.tool
def confirm_court_booking(intent_id: str = "") -> str:
    """Confirm and finalize a booking draft. If intent_id is empty or unknown, leave it empty—the system will automatically confirm the user's latest active hold."""
    user_id = _get_current_user_id()
    intent_to_confirm = intent_id.strip() if intent_id else ""
    if not intent_to_confirm:
        # Check if user has an active pending intent
        latest_intent = BookingIntent.query.filter_by(user_id=user_id, status='pending').order_by(BookingIntent.created_at.desc()).first()
        if latest_intent:
            intent_to_confirm = latest_intent.id
        else:
            # Check if already confirmed recently
            recent_confirmed = BookingIntent.query.filter_by(user_id=user_id, status='confirmed').order_by(BookingIntent.created_at.desc()).first()
            if recent_confirmed:
                intent_to_confirm = recent_confirmed.id
            else:
                return json.dumps({"error": "No active booking hold found to confirm. Please specify what you would like to book first."})

    booking, error = BookingService.confirm_intent(user_id=user_id, intent_id=intent_to_confirm)
    if error:
        return json.dumps({"error": error.get("message", "Failed to confirm booking")})

    return json.dumps({
        "status": "confirmed",
        "booking_id": booking.id,
        "court_name": booking.court.name,
        "club_name": booking.court.club.name if booking.court.club else "ClubDash Arena",
        "booking_date": str(booking.booking_date),
        "start_time": str(booking.start_time),
        "end_time": str(booking.end_time),
        "message": f"Successfully confirmed booking #{booking.id} on {booking.court.name} for {booking.booking_date} from {booking.start_time} to {booking.end_time}!"
    })

@llm.tool
def cancel_my_booking(booking_id: int = 0) -> str:
    """Cancel one of the authenticated user's confirmed bookings."""
    user_id = _get_current_user_id()
    if not booking_id:
        return json.dumps({"error": "Please provide the booking ID you wish to cancel."})

    success, error = BookingService.release_booking(user_id=user_id, booking_id=booking_id)
    if error:
        return json.dumps({"error": error.get("message", "Unable to cancel booking")})

    return json.dumps({
        "status": "cancelled",
        "booking_id": booking_id,
        "message": f"Booking #{booking_id} has been cancelled successfully."
    })




