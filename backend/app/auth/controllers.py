from flask import Blueprint, request, jsonify
from app.auth.services import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"code": "VALIDATION_ERROR", "message": "Missing credentials"}), 400

    access_token, user, error = AuthService.login(data['email'], data['password'])

    if error:
        return jsonify(error), 401

    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # 1. Basic Payload Validation
    required_fields = ['name', 'email', 'password', 'role']
    if not data or not all(field in data for field in required_fields):
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "Missing required fields (name, email, password, role)"
        }), 400

    # 2. Enum Validation
    allowed_roles = ['player', 'owner']
    if data['role'] not in allowed_roles:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": f"Invalid role. Must be one of: {', '.join(allowed_roles)}"
        }), 400

    # 3. Delegate to the Service Layer
    user, error = AuthService.register(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        role=data['role']
    )

    # 4. Handle specific errors
    if error:
        status_code = 409 if error['code'] == 'CONFLICT' else 500
        return jsonify(error), status_code

    # 5. Success Response
    return jsonify({
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 201