from app.extensions import db
from app.bookings.models import User
from flask_jwt_extended import create_access_token
from datetime import timedelta

class AuthService:
    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Inject claims into the JWT payload
            additional_claims = {"role": user.role}

            # Mint the token (expires in 24 hours)
            access_token = create_access_token(
                identity=str(user.id),
                additional_claims=additional_claims,
                expires_delta=timedelta(hours=24)
            )
            return access_token, user, None

        return None, None, {"code": "UNAUTHORIZED", "message": "Invalid email or password"}

    @staticmethod
    def register(name, email, password, role='player'):
        """
        Registers a new user. Returns a tuple: (User Object, Error Dictionary)
        """
        # 1. Check for existing user to prevent database IntegrityErrors on the unique email constraint
        if User.query.filter_by(email=email).first():
            return None, {
                "code": "CONFLICT",
                "message": "Email is already registered."
            }

        try:

            # 2. Create the user entity
            new_user = User(
                name=name,
                email=email,
                role=role
            )

            # 3. Hash the password before staging it
            new_user.set_password(password)

            # 4. Commit to database
            db.session.add(new_user)
            db.session.commit()

            return new_user, None

        except Exception as e:
            db.session.rollback()
            return None, {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred during registration."
            }