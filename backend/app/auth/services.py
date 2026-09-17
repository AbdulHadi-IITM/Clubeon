from app.extensions import db
from app.auth.models import User
from flask_jwt_extended import create_access_token
from datetime import timedelta


class AuthService:
    @staticmethod
    def generate_access_token(user):
        """Generate JWT token for a user."""
        additional_claims = {"role": user.role}
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims,
            expires_delta=timedelta(hours=24)
        )
        return access_token

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            access_token = AuthService.generate_access_token(user)
            return access_token, user, None

        return None, None, {"code": "UNAUTHORIZED", "message": "Invalid email or password"}

    @staticmethod
    def register(name, email, password, role='player'):
        """
        Registers a new user. Returns a tuple: (User Object, Error Dictionary)
        """
        if User.query.filter_by(email=email).first():
            return None, {
                "code": "CONFLICT",
                "message": "Email is already registered."
            }

        try:
            new_user = User(
                name=name,
                email=email,
                role=role
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.flush()

            if role == 'owner':
                from app.clubs.models import Club
                club = Club(
                    name=f"{name}'s Club",
                    address="Main Campus, Bengaluru",
                    owner_id=new_user.id
                )
                db.session.add(club)

            db.session.commit()
            return new_user, None

        except Exception as e:
            db.session.rollback()
            return None, {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred during registration."
            }

    @staticmethod
    def update_profile(user_id, name=None, email=None, phone=None, facility=None):
        user = User.query.get(user_id)
        if not user:
            return None, {"code": "NOT_FOUND", "message": "User not found"}

        if email and email.lower() != user.email.lower():
            existing = User.query.filter_by(email=email.lower()).first()
            if existing and existing.id != user.id:
                return None, {"code": "CONFLICT", "message": "Email is already taken by another account."}
            user.email = email.lower()

        if name:
            user.name = name.strip()

        if phone is not None:
            user.phone = phone.strip()

        if facility and user.role == 'owner':
            try:
                from app.clubs.models import Club
                club = Club.query.filter_by(owner_id=user.id).first()
                if club:
                    club.name = facility.strip()
                else:
                    new_club = Club(name=facility.strip(), owner_id=user.id, address="Main Campus")
                    db.session.add(new_club)
            except Exception as ce:
                print('Error updating club facility:', ce)

        try:
            db.session.commit()
            return user, None
        except Exception as e:
            db.session.rollback()
            return None, {"code": "INTERNAL_ERROR", "message": str(e)}