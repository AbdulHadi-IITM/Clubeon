import os

from flask import Flask, send_from_directory
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

    # Register models so Alembic can detect them
    from app.bookings import models

    # Register Blueprints (Controllers)
    from app.bookings.controllers import bookings_bp
    app.register_blueprint(bookings_bp)

    from app.auth.controllers import auth_bp
    app.register_blueprint(auth_bp)

    # 1. Route to serve the actual YAML file
    @app.route('/api/docs/openapi.yaml')
    def send_openapi_yaml():
        # Points to the api-docs folder one level above the backend
        yaml_dir = os.path.abspath(os.path.join(app.root_path, '../../api-docs'))
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