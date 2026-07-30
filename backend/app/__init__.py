import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from app.config import Config
from app.extensions import db, migrate, jwt
from flask_swagger_ui import get_swaggerui_blueprint


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Enable CORS with credentials (allows cookies)
    CORS(app,
         resources={r"/api/*": {
             "origins": app.config.get('CORS_ORIGINS', ['http://localhost:5173']),
             "supports_credentials": True,
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "expose_headers": ["X-CSRF-Token"]
         }})

    # Register models so Alembic can detect them
    from app.auth import models
    from app.clubs import models
    from app.bookings import models
    from app.memberships import models
    from app.events import models
    from app.payments import models
    from app.attendance import models
    from app.notifications import models

    # Register Blueprints (Controllers)
    from app.bookings.controllers import bookings_bp
    app.register_blueprint(bookings_bp)

    from app.auth.controllers import auth_bp
    app.register_blueprint(auth_bp)

    from app.clubs.controllers import clubs_bp
    app.register_blueprint(clubs_bp)

    from app.availability.controllers import availability_bp
    app.register_blueprint(availability_bp)

    from app.admin.controllers import admin_bp
    app.register_blueprint(admin_bp)

    from app.memberships.controllers import memberships_bp
    app.register_blueprint(memberships_bp)

    from app.events.controllers import events_bp
    app.register_blueprint(events_bp)




    # 1. Route to serve the actual YAML file
    @app.route('/api/docs/openapi.yaml')
    def send_openapi_yaml():
        yaml_dir = os.path.abspath(os.path.join(app.root_path, '../docs/api-docs'))
        return send_from_directory(yaml_dir, 'openapi.yaml')

    # 2. Setup the Swagger UI blueprint
    SWAGGER_URL = '/api/docs'
    API_URL = '/api/docs/openapi.yaml'

    swaggerui_bp = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Club Booking SaaS Platform"}
    )

    app.register_blueprint(swaggerui_bp, url_prefix=SWAGGER_URL)

    @app.route('/health')
    def health_check():
        return {"status": "healthy", "service": "club-booking-api"}, 200

    return app