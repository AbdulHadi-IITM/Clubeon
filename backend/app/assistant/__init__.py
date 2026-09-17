from flask import Blueprint

assistant_bp = Blueprint('assistant', __name__, url_prefix='/api/v1/assistant')

# Import controllers to register routes
from app.assistant import controllers
