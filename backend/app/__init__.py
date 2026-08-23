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

    return app