import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-32-bytes-minimum-for-security')
    # Database: Supports SQLite (sqlite:///...) and PostgreSQL (postgresql://...)
    _db_url = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
    if _db_url and _db_url.startswith('postgres://'):
        _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Cookie Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', os.environ.get('SECRET_KEY', 'jwt-dev-key-must-be-at-least-32-chars-long'))
    JWT_TOKEN_LOCATION = ['cookies', 'headers']
    JWT_COOKIE_SECURE = os.environ.get('JWT_COOKIE_SECURE', 'False') == 'True'
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_COOKIE_SAMESITE = 'Lax'
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_COOKIE_NAME = 'access_token_cookie'
    JWT_COOKIE_MAX_AGE = 24 * 60 * 60

    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5173').split(',')

    # Stripe
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
    # Default currency for Stripe charges (ISO 4217, lowercase for the Stripe API)
    STRIPE_DEFAULT_CURRENCY = os.environ.get('STRIPE_DEFAULT_CURRENCY', 'inr')
    # Flat fee charged for a court booking (no per-court pricing exists in the model yet)
    BOOKING_FEE = float(os.environ.get('BOOKING_FEE', '500'))

    # AI Assistant Model (<provider>/<model_name> loaded from .env)
    ASSISTANT_MODEL = os.environ.get('ASSISTANT_MODEL', 'google/gemini-2.0-flash-lite').strip()

    # Sync Google / Gemini API keys if set under either name
    if os.environ.get('GOOGLE_API_KEY') and not os.environ.get('GEMINI_API_KEY'):
        os.environ['GEMINI_API_KEY'] = os.environ['GOOGLE_API_KEY']
    elif os.environ.get('GEMINI_API_KEY') and not os.environ.get('GOOGLE_API_KEY'):
        os.environ['GOOGLE_API_KEY'] = os.environ['GEMINI_API_KEY']