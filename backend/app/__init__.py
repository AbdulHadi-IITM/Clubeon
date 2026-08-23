import os

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from app.config import Config
from app.extensions import db, migrate, jwt


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # =========================================================
    # Initialize Flask Extensions
    # =========================================================

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # =========================================================
    # CORS
    # =========================================================

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": app.config.get(
                    "CORS_ORIGINS",
                    ["http://localhost:5173"],
                ),
                "supports_credentials": True,
                "methods": [
                    "GET",
                    "POST",
                    "PUT",
                    "PATCH",
                    "DELETE",
                    "OPTIONS",
                ],
                "allow_headers": [
                    "Content-Type",
                    "Authorization",
                ],
                "expose_headers": [
                    "X-CSRF-Token",
                ],
            }
        },
    )

    # =========================================================
    # Register Models
    #
    # Import models so SQLAlchemy/Alembic can discover them.
    # =========================================================

    from app.auth import models as auth_models
    from app.clubs import models as club_models
    from app.bookings import models as booking_models
    from app.memberships import models as membership_models
    from app.events import models as event_models
    from app.payments import models as payment_models
    from app.attendance import models as attendance_models
    from app.notifications import models as notification_models

    # The aliases above intentionally keep the modules imported.
    # They also prevent ambiguous repeated `models` names.

    # =========================================================
    # Register Blueprints
    # =========================================================

    # Authentication
    from app.auth.controllers import auth_bp
    app.register_blueprint(auth_bp)

    # Clubs / Courts
    from app.clubs.controllers import clubs_bp
    app.register_blueprint(clubs_bp)

    # Availability
    from app.availability.controllers import availability_bp
    app.register_blueprint(availability_bp)

    # Bookings
    from app.bookings.controllers import bookings_bp
    app.register_blueprint(bookings_bp)

    # Admin / Owner
    from app.admin.controllers import admin_bp
    app.register_blueprint(admin_bp)

    # =========================================================
    # Front Desk / Staff
    # =========================================================

    from app.staff.controllers import staff_bp
    app.register_blueprint(staff_bp)

    # Memberships
    from app.memberships.controllers import memberships_bp
    app.register_blueprint(memberships_bp)

    # Events
    from app.events.controllers import events_bp
    app.register_blueprint(events_bp)

    # Payments
    from app.payments.controllers import payments_bp
    app.register_blueprint(payments_bp)

    # Attendance
    from app.attendance.controllers import attendance_bp
    app.register_blueprint(attendance_bp)

    # Notifications
    from app.notifications.controllers import notifications_bp
    app.register_blueprint(notifications_bp)

    # Assistant
    from app.assistant.controllers import assistant_bp
    app.register_blueprint(assistant_bp)

    from app.analytics.controllers import analytics_bp
    app.register_blueprint(analytics_bp)

    with app.app_context():
        from app.memberships.services import MembershipService
        MembershipService.seed_default_plans()

    # =========================================================
    # OpenAPI YAML
    # =========================================================

    @app.route("/api/docs/openapi.yaml")
    def send_openapi_yaml():
        yaml_dir = os.path.abspath(
            os.path.join(
                app.root_path,
                "../docs/api-docs",
            )
        )

        return send_from_directory(
            yaml_dir,
            "openapi.yaml",
        )

    # =========================================================
    # Swagger UI
    # =========================================================

    SWAGGER_URL = "/api/docs"
    API_URL = "/api/docs/openapi.yaml"

    swaggerui_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            "app_name": "Club Booking SaaS Platform"
        },
    )

    app.register_blueprint(
        swaggerui_bp,
        url_prefix=SWAGGER_URL,
    )

    # =========================================================
    # Health Check
    # =========================================================

    @app.route("/health")
    def health_check():
        return {
            "status": "healthy",
            "service": "club-booking-api",
        }, 200

    # Auto-create tables & enrich recommendation metadata
    # Demo/bootstrap data. Skipped under TESTING: it calls db.create_all() and
    # seeds a demo club owned by user id 1, which lands in the test database and
    # makes the first user created by a test "already own a club".
    if not app.config.get('TESTING'):
        with app.app_context():
            try:
                from sqlalchemy import text, inspect
                db.create_all()

                # Ensure new columns exist on existing tables in SQLite/Postgres
                inspector = inspect(db.engine)
                if inspector.has_table('clubs'):
                    existing_club_cols = [c['name'] for c in inspector.get_columns('clubs')]
                    if 'latitude' not in existing_club_cols:
                        db.session.execute(text("ALTER TABLE clubs ADD COLUMN latitude FLOAT"))
                    if 'longitude' not in existing_club_cols:
                        db.session.execute(text("ALTER TABLE clubs ADD COLUMN longitude FLOAT"))
                    if 'amenities' not in existing_club_cols:
                        db.session.execute(text("ALTER TABLE clubs ADD COLUMN amenities JSON"))
                    if 'tags' not in existing_club_cols:
                        db.session.execute(text("ALTER TABLE clubs ADD COLUMN tags JSON"))

                if inspector.has_table('courts'):
                    existing_court_cols = [c['name'] for c in inspector.get_columns('courts')]
                    if 'amenities' not in existing_court_cols:
                        db.session.execute(text("ALTER TABLE courts ADD COLUMN amenities JSON"))
                    if 'tags' not in existing_court_cols:
                        db.session.execute(text("ALTER TABLE courts ADD COLUMN tags JSON"))

                db.session.commit()

                from app.clubs.models import Club, Court
                club1 = Club.query.get(1)
                if club1:
                    if club1.latitude is None:
                        club1.latitude = 12.9716
                        club1.longitude = 77.5946
                        club1.amenities = ["parking", "cafe", "locker-room", "pro-shop", "wifi"]
                        club1.tags = ["family-friendly", "indoor", "air-conditioned"]
                    for court in club1.courts:
                        if not court.amenities:
                            court.amenities = ["indoor", "wooden-flooring", "led-lighting", "parking"]
                        if not court.tags:
                            court.tags = ["kid-friendly", "all-weather"]

                # Ensure an AquaFit Swimming center exists for chlorine-free / kid-friendly queries
                aqua = Club.query.filter(Club.name.ilike("%AquaFit%")).first()
                if not aqua:
                    aqua = Club(
                        name="AquaFit Olympic & Wellness Club",
                        address="12 Lake View Rd, Indiranagar",
                        owner_id=club1.owner_id if club1 else 1,
                        open_time="06:00",
                        close_time="22:00",
                        latitude=12.9784,
                        longitude=77.6408,
                        amenities=["chlorine-free", "heated", "parking", "cafe", "showers", "sauna"],
                        tags=["kid-friendly", "family-friendly", "women-only-hours", "wellness"]
                    )
                    db.session.add(aqua)
                    db.session.flush()
                    pool1 = Court(
                        club_id=aqua.id,
                        name="Olympic Lap Pool (50m)",
                        sport_type="swimming",
                        is_active=True,
                        amenities=["chlorine-free", "heated", "salt-water", "lane-dividers"],
                        tags=["kid-friendly", "pro-training"]
                    )
                    pool2 = Court(
                        club_id=aqua.id,
                        name="Learners & Kids Splash Pool",
                        sport_type="swimming",
                        is_active=True,
                        amenities=["chlorine-free", "heated", "shallow-depth", "lifeguard-on-duty"],
                        tags=["kid-friendly", "family-friendly"]
                    )
                    db.session.add_all([pool1, pool2])

                db.session.commit()
            except Exception:
                db.session.rollback()

    return app