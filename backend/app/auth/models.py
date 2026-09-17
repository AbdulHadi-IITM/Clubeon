from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='player', nullable=False)
    phone = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # --- Profile (editable from the Settings / Profile screens) ---
    dob = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    # Text, not String(500): the profile screen stores a downscaled avatar as a
    # data: URL, which does not fit in 500 characters. Size is capped in
    # ProfileService.update_profile.
    avatar_url = db.Column(db.Text, nullable=True)

    # --- Preferences (Settings -> Notifications / Privacy) ---
    notify_email = db.Column(db.Boolean, default=True, nullable=False)
    notify_sms = db.Column(db.Boolean, default=False, nullable=False)
    notify_push = db.Column(db.Boolean, default=True, nullable=False)
    profile_public = db.Column(db.Boolean, default=False, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_preferences=False):
        """Serialise the user for API responses."""
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
            "dob": self.dob.isoformat() if self.dob else None,
            "gender": self.gender,
            "address": self.address,
            "avatar_url": self.avatar_url,
            "created_at": str(self.created_at) if self.created_at else None,
        }
        if include_preferences:
            data["preferences"] = {
                "notify_email": self.notify_email,
                "notify_sms": self.notify_sms,
                "notify_push": self.notify_push,
                "profile_public": self.profile_public,
            }
        return data
