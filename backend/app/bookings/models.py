from app.extensions import db
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='player', nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Establish a relationship for easy querying later
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Court(db.Model):
    __tablename__ = 'courts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    bookings = db.relationship('Booking', backref='court', lazy=True)

class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    court_id = db.Column(db.Integer, db.ForeignKey('courts.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), default='active', nullable=False)
    is_peak_hour = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # The PostgreSQL GiST Exclusion Constraint to prevent time overlaps
    __table_args__ = (
        ExcludeConstraint(
            (court_id, '='),
            (booking_date, '='),
            (text("tsrange(booking_date + start_time, booking_date + end_time, '[)')"), '&&'),
            where=(status == 'active'),
            name='prevent_overlapping_bookings'
        ),
    )