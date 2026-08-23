"""
Analytics for the Admin, Member and Staff dashboards.

Every figure here is computed from real rows — these endpoints replace the
hard-coded numbers the dashboards previously displayed.
"""
from datetime import date, timedelta

from sqlalchemy import func

from app.extensions import db
from app.auth.models import User
from app.clubs.models import Club, Court
from app.bookings.models import Booking, CourtBlock
from app.memberships.models import Membership, MembershipPlan
from app.events.models import Event, EventRegistration
from app.payments.models import Payment
from app.attendance.models import AttendanceRecord


def _owner_club(owner_id):
    return Club.query.filter_by(owner_id=owner_id).first()


class AnalyticsService:
    # ------------------------------------------------------------------
    # ADMIN / OWNER
    # ------------------------------------------------------------------
    @staticmethod
    def admin_overview(owner_id, days=30):
        """KPIs for the club owner's dashboard."""
        club = _owner_club(owner_id)
        if not club:
            return None, {"code": "NOT_FOUND",
                          "message": "You do not own a club yet."}

        court_ids = [c.id for c in Court.query.filter_by(club_id=club.id).all()]
        today = date.today()
        since = today - timedelta(days=days)

        base = Booking.query.filter(Booking.court_id.in_(court_ids)) if court_ids \
            else Booking.query.filter(db.false())

        total_bookings = base.count()
        active_bookings = base.filter(Booking.status == "active").count()
        released_bookings = base.filter(Booking.status == "released").count()
        overridden_bookings = base.filter(Booking.status == "overridden").count()
        upcoming_bookings = base.filter(Booking.booking_date >= today,
                                        Booking.status == "active").count()
        recent_bookings = base.filter(Booking.booking_date >= since).count()

        # --- members ---
        total_members = Membership.query.filter_by(club_id=club.id).count()
        active_members = Membership.query.filter_by(club_id=club.id,
                                                    status="active").count()

        # --- revenue (completed payments only) ---
        revenue_rows = db.session.query(
            Payment.payment_type, func.coalesce(func.sum(Payment.amount), 0.0)
        ).filter(Payment.status == "completed").group_by(Payment.payment_type).all()
        revenue_by_type = {t: float(a or 0) for t, a in revenue_rows}
        total_revenue = round(sum(revenue_by_type.values()), 2)

        pending_payments = Payment.query.filter_by(status="pending").count()
        failed_payments = Payment.query.filter_by(status="failed").count()

        # --- utilisation: booked slots vs bookable slots over the window ---
        slot_minutes = club.slot_duration_minutes or 60
        try:
            open_h, open_m = (int(x) for x in (club.open_time or "06:00").split(":"))
            close_h, close_m = (int(x) for x in (club.close_time or "22:00").split(":"))
            minutes_open = (close_h * 60 + close_m) - (open_h * 60 + open_m)
        except (ValueError, AttributeError):
            minutes_open = 16 * 60
        slots_per_court_per_day = max(minutes_open // slot_minutes, 0)
        capacity = slots_per_court_per_day * max(len(court_ids), 0) * days
        utilisation = round((recent_bookings / capacity) * 100, 1) if capacity else 0.0

        # --- per-court breakdown ---
        per_court = []
        for court in Court.query.filter_by(club_id=club.id).all():
            cnt = Booking.query.filter_by(court_id=court.id).filter(
                Booking.booking_date >= since).count()
            per_court.append({
                "court_id": court.id,
                "court_name": court.name,
                "is_active": court.is_active,
                "bookings": cnt,
                "percentage": round((cnt / recent_bookings) * 100, 1) if recent_bookings else 0.0,
            })

        # --- bookings per day (trend) ---
        trend_rows = db.session.query(
            Booking.booking_date, func.count(Booking.id)
        ).filter(Booking.court_id.in_(court_ids) if court_ids else db.false(),
                 Booking.booking_date >= since).group_by(
            Booking.booking_date).order_by(Booking.booking_date).all()
        trend = [{"date": d.isoformat(), "bookings": c} for d, c in trend_rows]

        # --- events ---
        events_q = Event.query.filter_by(club_id=club.id)
        event_ids = [e.id for e in events_q.all()]
        registrations = EventRegistration.query.filter(
            EventRegistration.event_id.in_(event_ids),
            EventRegistration.status == "registered").count() if event_ids else 0

        return {
            "club": {"id": club.id, "name": club.name},
            "window_days": days,
            "bookings": {
                "total": total_bookings,
                "active": active_bookings,
                "released": released_bookings,
                "overridden": overridden_bookings,
                "upcoming": upcoming_bookings,
                "in_window": recent_bookings,
            },
            "members": {"total": total_members, "active": active_members},
            "revenue": {
                "total": total_revenue,
                "by_type": revenue_by_type,
                "pending_payments": pending_payments,
                "failed_payments": failed_payments,
            },
            "courts": {
                "total": len(court_ids),
                "active": sum(1 for c in per_court if c["is_active"]),
                "blocked_now": CourtBlock.query.filter(
                    CourtBlock.court_id.in_(court_ids),
                    CourtBlock.start_date <= today,
                    CourtBlock.end_date >= today).count() if court_ids else 0,
                "utilisation_percent": utilisation,
                "breakdown": per_court,
            },
            "events": {"total": len(event_ids), "registrations": registrations},
            "trend": trend,
        }, None

    # ------------------------------------------------------------------
    # MEMBER
    # ------------------------------------------------------------------
    @staticmethod
    def member_overview(user_id):
        today = date.today()
        base = Booking.query.filter_by(user_id=user_id)

        total = base.count()
        upcoming = base.filter(Booking.booking_date >= today,
                               Booking.status == "active").count()
        completed = base.filter(Booking.booking_date < today,
                                Booking.status == "active").count()
        cancelled = base.filter(Booking.status.in_(["released", "overridden"])).count()

        membership = Membership.query.filter_by(
            user_id=user_id, status="active").order_by(Membership.end_date.desc()).first()
        membership_info = None
        if membership:
            plan = MembershipPlan.query.get(membership.plan_id)
            membership_info = {
                "membership_id": membership.id,
                "plan_name": plan.name if plan else None,
                "status": membership.status,
                "start_date": membership.start_date.isoformat(),
                "end_date": membership.end_date.isoformat(),
                "days_left": max((membership.end_date - today).days, 0),
                "auto_renew": membership.auto_renew,
            }

        spend = db.session.query(
            func.coalesce(func.sum(Payment.amount), 0.0)
        ).filter(Payment.user_id == user_id,
                 Payment.status == "completed").scalar()

        registrations = EventRegistration.query.filter_by(
            user_id=user_id, status="registered").count()

        attendance = AttendanceRecord.query.filter_by(user_id=user_id).count()

        next_booking = base.filter(Booking.booking_date >= today,
                                   Booking.status == "active").order_by(
            Booking.booking_date, Booking.start_time).first()
        next_info = None
        if next_booking:
            next_info = {
                "booking_id": next_booking.id,
                "date": next_booking.booking_date.isoformat(),
                "start_time": str(next_booking.start_time),
                "end_time": str(next_booking.end_time),
                "court_name": next_booking.court.name,
                "club_name": next_booking.court.club.name,
            }

        return {
            "bookings": {"total": total, "upcoming": upcoming,
                         "completed": completed, "cancelled": cancelled},
            "membership": membership_info,
            "total_spend": round(float(spend or 0), 2),
            "event_registrations": registrations,
            "attendance_count": attendance,
            "next_booking": next_info,
        }, None

    # ------------------------------------------------------------------
    # STAFF / FRONT DESK
    # ------------------------------------------------------------------
    @staticmethod
    def staff_overview(club_id=None):
        """Operational snapshot for today — front-desk view."""
        today = date.today()

        club = Club.query.get(club_id) if club_id else Club.query.first()
        if not club:
            return None, {"code": "NOT_FOUND", "message": "No club found."}

        court_ids = [c.id for c in Court.query.filter_by(club_id=club.id).all()]
        day_q = Booking.query.filter(
            Booking.court_id.in_(court_ids) if court_ids else db.false(),
            Booking.booking_date == today)

        checked_in = AttendanceRecord.query.filter(
            func.date(AttendanceRecord.check_in_at) == today).count()
        checked_out = AttendanceRecord.query.filter(
            AttendanceRecord.check_out_at.isnot(None),
            func.date(AttendanceRecord.check_out_at) == today).count()

        todays = []
        for b in day_q.order_by(Booking.start_time).all():
            todays.append({
                "booking_id": b.id,
                "member": b.user.name if b.user else None,
                "court_name": b.court.name if b.court else None,
                "start_time": str(b.start_time),
                "end_time": str(b.end_time),
                "status": b.status,
            })

        return {
            "club": {"id": club.id, "name": club.name},
            "date": today.isoformat(),
            "today": {
                "total_bookings": day_q.count(),
                "active": day_q.filter(Booking.status == "active").count(),
                "released": day_q.filter(Booking.status == "released").count(),
                "checked_in": checked_in,
                "checked_out": checked_out,
                "currently_inside": max(checked_in - checked_out, 0),
            },
            "bookings": todays,
        }, None
