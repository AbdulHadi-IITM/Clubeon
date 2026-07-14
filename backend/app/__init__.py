from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt

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

    @app.route('/health')
    def health_check():
        return {"status": "healthy", "service": "club-booking-api"}, 200

    return app