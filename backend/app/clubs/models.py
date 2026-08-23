from app.extensions import db

class Club(db.Model):
    __tablename__ = 'clubs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    open_time = db.Column(db.String(5), nullable=True) # HH:MM
    close_time = db.Column(db.String(5), nullable=True) # HH:MM
    slot_duration_minutes = db.Column(db.Integer, default=60)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    amenities = db.Column(db.JSON, default=list)
    tags = db.Column(db.JSON, default=list)

    owner = db.relationship('User', backref='clubs')
    courts = db.relationship('Court', backref='club', cascade="all, delete-orphan", lazy=True)

class Court(db.Model):
    __tablename__ = 'courts'

    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    sport_type = db.Column(db.String(30), nullable=False, default='multi-purpose')
    is_active = db.Column(db.Boolean, default=True)
    open_time_override = db.Column(db.String(5), nullable=True)
    close_time_override = db.Column(db.String(5), nullable=True)
    slot_duration_override = db.Column(db.Integer, nullable=True)
    amenities = db.Column(db.JSON, default=list)
    tags = db.Column(db.JSON, default=list)

