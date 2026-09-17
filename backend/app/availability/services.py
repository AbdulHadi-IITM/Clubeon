from datetime import datetime, date, time, timedelta
from app.clubs.models import Club, Court
from app.bookings.models import Booking, CourtBlock

def _parse_time(t_val, default_time_str):
    if not t_val:
        t_val = default_time_str
    if isinstance(t_val, time):
        return t_val
    t_str = str(t_val).strip()[:5]
    try:
        return datetime.strptime(t_str, "%H:%M").time()
    except Exception:
        return datetime.strptime(default_time_str, "%H:%M").time()

class AvailabilityService:
    @staticmethod
    def get_availability_matrix(club_id, target_date_str):
        try:
            target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
        except ValueError:
            return None, {"code": "VALIDATION_ERROR", "message": "Invalid date format. Use YYYY-MM-DD"}
            
        club = Club.query.get(club_id)
        if not club:
            return None, {"code": "NOT_FOUND", "message": "Club not found"}
            
        courts = Court.query.filter_by(club_id=club_id, is_active=True).all()
        if not courts:
            return {"date": str(target_date), "courts": []}, None
            
        court_ids = [c.id for c in courts]
        
        # Fetch bookings and blocks
        bookings = Booking.query.filter(
            Booking.court_id.in_(court_ids),
            Booking.booking_date == target_date,
            Booking.status != 'released'
        ).all()
        
        blocks = CourtBlock.query.filter(
            CourtBlock.court_id.in_(court_ids),
            CourtBlock.start_date <= target_date,
            CourtBlock.end_date >= target_date
        ).all()
        
        result = {"date": str(target_date), "courts": []}
        
        for court in courts:
            open_time_val = court.open_time_override or club.open_time or "06:00"
            close_time_val = court.close_time_override or club.close_time or "22:00"
            open_time = _parse_time(open_time_val, "06:00")
            close_time = _parse_time(close_time_val, "22:00")
            slot_duration = court.slot_duration_override or club.slot_duration_minutes or 60
            if slot_duration <= 0:
                slot_duration = 60
            
            # Generate slots
            slots = []
            current_time = datetime.combine(target_date, open_time)
            end_datetime = datetime.combine(target_date, close_time)
            
            # Filter bookings and blocks for this court
            court_bookings = [b for b in bookings if b.court_id == court.id]
            court_blocks = [b for b in blocks if b.court_id == court.id]
            
            while current_time < end_datetime:
                slot_start = current_time.time()
                slot_end = (current_time + timedelta(minutes=slot_duration)).time()
                
                status = "available"
                reason = None
                
                # Check for blocks
                is_blocked = len(court_blocks) > 0
                
                if is_blocked:
                    status = "blocked"
                    reason = "admin_block"
                else:
                    # Check for bookings
                    is_booked = any(
                        b.start_time <= slot_start and b.end_time >= slot_end
                        for b in court_bookings
                    )
                    if is_booked:
                        status = "booked"
                        
                slots.append({
                    "start_time": str(slot_start),
                    "end_time": str(slot_end),
                    "status": status,
                    "reason": reason
                })
                
                current_time += timedelta(minutes=slot_duration)
                
            result["courts"].append({
                "court_id": court.id,
                "court_name": court.name,
                "slots": slots
            })
            
        return result, None
