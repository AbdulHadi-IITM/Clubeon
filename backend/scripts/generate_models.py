import os

AUTH_MODELS = """from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='player', nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
"""

CLUBS_MODELS = """from app.extensions import db

class Club(db.Model):
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    open_time = db.Column(db.String(5), nullable=True) # HH:MM
    close_time = db.Column(db.String(5), nullable=True) # HH:MM
    slot_duration_minutes = db.Column(db.Integer, default=60)

    owner = db.relationship('User', backref='clubs')
    courts = db.relationship('Court', backref='club', cascade="all, delete-orphan", lazy=True)

class Court(db.Model):
    __tablename__ = 'courts'

    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    open_time_override = db.Column(db.String(5), nullable=True)
    close_time_override = db.Column(db.String(5), nullable=True)
    slot_duration_override = db.Column(db.Integer, nullable=True)
"""

BOOKINGS_MODELS = """from app.extensions import db
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from sqlalchemy import text

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    court_id = db.Column(db.Integer, db.ForeignKey('courts.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='active', nullable=False) # active, released, overridden
    is_peak_hour = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    user = db.relationship('User', backref='bookings', lazy=True)
    court = db.relationship('Court', backref='bookings', lazy=True)

    __table_args__ = (
        ExcludeConstraint(
            (court_id, '='),
            (booking_date, '='),
            (text("tsrange(booking_date + start_time, booking_date + end_time, '[)')"), '&&'),
            where=(status == 'active'),
            name='prevent_overlapping_bookings'
        ),
    )

class CourtBlock(db.Model):
    __tablename__ = 'court_blocks'
    
    id = db.Column(db.Integer, primary_key=True)
    court_id = db.Column(db.Integer, db.ForeignKey('courts.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    title = db.Column(db.String(200))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
"""

MEMBERSHIPS_MODELS = """from app.extensions import db

class MembershipPlan(db.Model):
    __tablename__ = 'membership_plans'

    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price_monthly = db.Column(db.Float, nullable=False)
    benefits = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)

class Membership(db.Model):
    __tablename__ = 'memberships'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('membership_plans.id'), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    status = db.Column(db.String(20), default='active')
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    auto_renew = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    plan = db.relationship('MembershipPlan', lazy=True)
"""

EVENTS_MODELS = """from app.extensions import db

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    max_attendees = db.Column(db.Integer, nullable=True)
    registration_fee = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='upcoming')
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class EventRegistration(db.Model):
    __tablename__ = 'event_registrations'

    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='registered')
    registered_at = db.Column(db.DateTime, server_default=db.func.now())

    __table_args__ = (
        db.UniqueConstraint('event_id', 'user_id', name='uq_event_user'),
    )
"""

PAYMENTS_MODELS = """from app.extensions import db

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='INR')
    payment_type = db.Column(db.String(30), nullable=False) # booking, membership, event
    reference_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')
    gateway_transaction_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
"""

ATTENDANCE_MODELS = """from app.extensions import db

class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)
    check_in_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    check_out_at = db.Column(db.DateTime, nullable=True)
    
    user = db.relationship('User', lazy=True)
"""

NOTIFICATIONS_MODELS = """from app.extensions import db

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(30), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
"""

files_to_write = {
    'app/auth/models.py': AUTH_MODELS,
    'app/clubs/models.py': CLUBS_MODELS,
    'app/bookings/models.py': BOOKINGS_MODELS,
    'app/memberships/models.py': MEMBERSHIPS_MODELS,
    'app/events/models.py': EVENTS_MODELS,
    'app/payments/models.py': PAYMENTS_MODELS,
    'app/attendance/models.py': ATTENDANCE_MODELS,
    'app/notifications/models.py': NOTIFICATIONS_MODELS
}

import os
for path, content in files_to_write.items():
    with open(f"/home/adduser/Harshita-Projects/MAY2026-Team-096/backend/{path}", 'w') as f:
        f.write(content)

print("Generated models")
