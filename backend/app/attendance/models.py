from app.extensions import db

class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)
    check_in_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    check_out_at = db.Column(db.DateTime, nullable=True)
    
    user = db.relationship('User', lazy=True)
