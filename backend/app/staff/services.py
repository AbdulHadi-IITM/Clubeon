from datetime import date, datetime
from app.extensions import db
from app.auth.models import User
from app.clubs.models import Club, Court
from app.bookings.models import Booking
from app.attendance.models import AttendanceRecord
from app.events.models import Event, EventRegistration
from app.memberships.models import Membership


class StaffService:
    @staticmethod
    def get_club(club_id):
        return Club.query.get(club_id)

    @staticmethod
    def list_bookings(club_id, booking_date=None):
        query = Booking.query.join(Court).filter(Court.club_id == club_id)
        if booking_date:
            try:
                parsed = datetime.strptime(booking_date, '%Y-%m-%d').date()
            except ValueError:
                return None, {'code': 'VALIDATION_ERROR', 'message': 'Invalid date format. Use YYYY-MM-DD.'}
            query = query.filter(Booking.booking_date == parsed)
        return query.order_by(Booking.booking_date.desc(), Booking.start_time.asc()).all(), None

    @staticmethod
    def get_booking(club_id, booking_id):
        return (
            Booking.query.join(Court)
            .filter(Booking.id == booking_id, Court.club_id == club_id)
            .first()
        )

    @staticmethod
    def list_members(club_id):
        rows = (
            db.session.query(User, db.func.count(Booking.id).label('booking_count'))
            .join(Booking, Booking.user_id == User.id)
            .join(Court, Booking.court_id == Court.id)
            .filter(Court.club_id == club_id, User.role == 'player')
            .group_by(User.id)
            .order_by(User.name.asc())
            .all()
        )
        return rows

    @staticmethod
    def get_member(club_id, user_id):
        has_club_booking = (
            db.session.query(Booking.id)
            .join(Court)
            .filter(Booking.user_id == user_id, Court.club_id == club_id)
            .first()
        )
        if not has_club_booking:
            return None
        return User.query.filter_by(id=user_id, role='player').first()

    @staticmethod
    def member_detail(club_id, user_id):
        user = StaffService.get_member(club_id, user_id)
        if not user:
            return None

        bookings = (
            Booking.query.join(Court)
            .filter(Booking.user_id == user_id, Court.club_id == club_id)
            .order_by(Booking.booking_date.desc(), Booking.start_time.desc())
            .limit(10)
            .all()
        )
        memberships = (
            Membership.query
            .filter_by(user_id=user_id, club_id=club_id)
            .order_by(Membership.created_at.desc())
            .all()
        )
        active_membership = next((m for m in memberships if m.status == 'active'), None)
        attendance_count = (
            AttendanceRecord.query
            .join(Booking, AttendanceRecord.booking_id == Booking.id)
            .join(Court, Booking.court_id == Court.id)
            .filter(AttendanceRecord.user_id == user_id, Court.club_id == club_id)
            .count()
        )
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'created_at': str(user.created_at) if user.created_at else None,
            'booking_count': Booking.query.join(Court).filter(Booking.user_id == user_id, Court.club_id == club_id).count(),
            'attendance_count': attendance_count,
            'active_membership': {
                'id': active_membership.id,
                'plan_name': active_membership.plan.name if active_membership.plan else None,
                'status': active_membership.status,
                'start_date': str(active_membership.start_date),
                'end_date': str(active_membership.end_date),
                'auto_renew': active_membership.auto_renew,
            } if active_membership else None,
            'bookings': [
                {
                    'id': b.id,
                    'date': str(b.booking_date),
                    'start_time': str(b.start_time),
                    'end_time': str(b.end_time),
                    'court_name': b.court.name,
                    'status': b.status,
                }
                for b in bookings
            ],
        }

    @staticmethod
    def expected_attendance(club_id, attendance_date=None):
        target_date = date.today()
        if attendance_date:
            try:
                target_date = datetime.strptime(attendance_date, '%Y-%m-%d').date()
            except ValueError:
                return None, {'code': 'VALIDATION_ERROR', 'message': 'Invalid date format. Use YYYY-MM-DD.'}

        bookings = (
            Booking.query.join(Court)
            .filter(
                Court.club_id == club_id,
                Booking.booking_date == target_date,
                Booking.status == 'active',
            )
            .order_by(Booking.start_time.asc())
            .all()
        )

        booking_ids = [b.id for b in bookings]
        records = (
            AttendanceRecord.query
            .filter(AttendanceRecord.booking_id.in_(booking_ids))
            .order_by(AttendanceRecord.check_in_at.desc())
            .all()
            if booking_ids else []
        )
        by_booking = {}
        for record in records:
            by_booking.setdefault(record.booking_id, record)

        result = []
        for booking in bookings:
            record = by_booking.get(booking.id)
            status = 'checked-in' if record and not record.check_out_at else 'checked-out' if record else 'expected'
            result.append({
                'id': booking.id,
                'user_id': booking.user_id,
                'user_name': booking.user.name,
                'user_email': booking.user.email,
                'booking_id': booking.id,
                'court_name': booking.court.name,
                'booking_date': str(booking.booking_date),
                'start_time': str(booking.start_time),
                'end_time': str(booking.end_time),
                'attendance_status': status,
                'attendance_id': record.id if record else None,
            })
        return result, None

    @staticmethod
    def list_attendance(club_id, attendance_date=None):
        query = (
            AttendanceRecord.query
            .join(Booking, AttendanceRecord.booking_id == Booking.id)
            .join(Court, Booking.court_id == Court.id)
            .filter(Court.club_id == club_id)
        )
        if attendance_date:
            try:
                parsed_d = datetime.strptime(attendance_date, '%Y-%m-%d').date()
                query = query.filter(Booking.booking_date == parsed_d)
            except ValueError:
                pass
        return query.order_by(AttendanceRecord.check_in_at.desc()).all()


    @staticmethod
    def check_in_booking(booking_id, club_id=None):
        booking = Booking.query.get(booking_id)
        if not booking:
            return None, {'code': 'NOT_FOUND', 'message': 'Booking not found.'}
        if club_id is not None and booking.court.club_id != club_id:
            return None, {'code': 'FORBIDDEN', 'message': 'Booking does not belong to this club.'}
        if booking.status != 'active':
            return None, {'code': 'VALIDATION_ERROR', 'message': f'Booking is {booking.status}.'}
        existing = AttendanceRecord.query.filter_by(booking_id=booking.id, check_out_at=None).first()
        if existing:
            return None, {'code': 'CONFLICT', 'message': 'Member is already checked in for this booking.'}
        record = AttendanceRecord(user_id=booking.user_id, booking_id=booking.id, check_in_at=datetime.utcnow())
        db.session.add(record)
        db.session.commit()
        return record, None

    @staticmethod
    def check_out(attendance_id, club_id=None):
        record = AttendanceRecord.query.get(attendance_id)
        if not record:
            return None, {'code': 'NOT_FOUND', 'message': 'Attendance record not found.'}
        if club_id is not None and (not record.booking or record.booking.court.club_id != club_id):
            return None, {'code': 'FORBIDDEN', 'message': 'Attendance record does not belong to this club.'}
        if record.check_out_at:
            return None, {'code': 'VALIDATION_ERROR', 'message': 'Member is already checked out.'}
        record.check_out_at = datetime.utcnow()
        db.session.commit()
        return record, None

    @staticmethod
    def dashboard(club_id):
        today = date.today()
        courts = Court.query.filter_by(club_id=club_id).all()
        bookings = (
            Booking.query.join(Court)
            .filter(Court.club_id == club_id, Booking.booking_date == today)
            .order_by(Booking.start_time.asc()).all()
        )
        booking_ids = [b.id for b in bookings]
        attendance = AttendanceRecord.query.filter(AttendanceRecord.booking_id.in_(booking_ids)).all() if booking_ids else []
        active_attendance = [r for r in attendance if r.check_out_at is None]
        return {
            'date': str(today),
            'total_courts': len(courts),
            'active_courts': sum(1 for c in courts if c.is_active),
            'today_bookings': len(bookings),
            'active_bookings': sum(1 for b in bookings if b.status == 'active'),
            'checked_in': len(active_attendance),
            'pending_arrivals': max(0, sum(1 for b in bookings if b.status == 'active') - len(active_attendance)),
            'bookings': bookings,
        }

    @staticmethod
    def list_events(club_id, event_date=None):
        query = Event.query.filter_by(club_id=club_id).order_by(Event.event_date.asc(), Event.start_time.asc())
        if event_date:
            try:
                parsed = datetime.strptime(event_date, '%Y-%m-%d').date()
            except ValueError:
                return None, {'code': 'VALIDATION_ERROR', 'message': 'Invalid date format. Use YYYY-MM-DD.'}
            query = query.filter(Event.event_date == parsed)
        return query.all(), None

    @staticmethod
    def get_event(club_id, event_id):
        return Event.query.filter_by(id=event_id, club_id=club_id).first()

    @staticmethod
    def event_detail(club_id, event_id):
        event = StaffService.get_event(club_id, event_id)
        if not event:
            return None
        registrations = (
            EventRegistration.query
            .filter_by(event_id=event_id, status='registered')
            .order_by(EventRegistration.registered_at.asc())
            .all()
        )
        users = {u.id: u for u in User.query.filter(User.id.in_([r.user_id for r in registrations])).all()} if registrations else {}
        attendances = {a.user_id: a for a in AttendanceRecord.query.filter_by(event_id=event_id).all()}
        return {
            'id': event.id,
            'club_id': event.club_id,
            'title': event.title,
            'description': event.description,
            'date': str(event.event_date),
            'start_time': str(event.start_time),
            'end_time': str(event.end_time),
            'max_attendees': event.max_attendees,
            'registration_fee': event.registration_fee,
            'status': event.status,
            'registered_count': len(registrations),
            'participants': [
                {
                    'registration_id': r.id,
                    'user_id': r.user_id,
                    'name': users[r.user_id].name if r.user_id in users else 'Member',
                    'email': users[r.user_id].email if r.user_id in users else '',
                    'registered_at': str(r.registered_at) if r.registered_at else None,
                    'is_checked_in': r.user_id in attendances,
                    'check_in_at': str(attendances[r.user_id].check_in_at) if r.user_id in attendances else None,
                }
                for r in registrations
            ],
        }

    @staticmethod
    def check_in_event(event_id, user_id):
        event = Event.query.get(event_id)
        if not event:
            return None, {'code': 'NOT_FOUND', 'message': 'Event not found'}

        registration = EventRegistration.query.filter_by(event_id=event_id, user_id=user_id, status='registered').first()
        if not registration:
            return None, {'code': 'NOT_FOUND', 'message': 'Participant registration not found'}

        existing = AttendanceRecord.query.filter_by(event_id=event_id, user_id=user_id).first()
        if existing:
            return existing, None

        record = AttendanceRecord(user_id=user_id, event_id=event_id)
        db.session.add(record)
        db.session.commit()
        return record, None
