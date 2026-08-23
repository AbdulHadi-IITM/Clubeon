from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.auth.services import AuthService
from app.auth.profile_service import ProfileService
from app.auth.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


def _user_to_dict(user):
    """Helper to serialize user."""
    club_name = None
    if user.role == 'owner':
        try:
            from app.clubs.models import Club
            club = Club.query.filter_by(owner_id=user.id).first()
            if club:
                club_name = club.name
        except Exception:
            pass

    data = user.to_dict()
    # Preserve develop's contract: blank strings rather than null, plus the
    # owner's club name as "facility".
    data["phone"] = user.phone or ''
    data["facility"] = club_name or ''
    data["created_at"] = user.created_at.isoformat() if user.created_at else None
    return data


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"code": "VALIDATION_ERROR", "message": "Missing credentials"}), 400

    access_token, user, error = AuthService.login(data['email'], data['password'])

    if error:
        return jsonify(error), 401

    # Create response with user data
    response = jsonify({
        "message": "Login successful",
        "user": _user_to_dict(user)
    })

    # Set HttpOnly cookie (browser sends it automatically on subsequent requests)
    response.set_cookie(
        'access_token_cookie',
        access_token,
        max_age=24*60*60,  # 24 hours
        secure=False,  # Set to True in production with HTTPS
        httponly=True,  # Prevents JavaScript access
        samesite='Lax',  # CSRF protection
        path='/'
    )

    return response, 200


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    required_fields = ['name', 'email', 'password', 'role']
    if not data or not all(field in data for field in required_fields):
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": "Missing required fields (name, email, password, role)"
        }), 400

    allowed_roles = ['player', 'owner', 'front-desk']
    if data['role'] not in allowed_roles:
        return jsonify({
            "code": "VALIDATION_ERROR",
            "message": f"Invalid role. Must be one of: {', '.join(allowed_roles)}"
        }), 400

    user, error = AuthService.register(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        role=data['role']
    )

    if error:
        status_code = 409 if error['code'] == 'CONFLICT' else 500
        return jsonify(error), status_code

    # Generate token and set cookie
    access_token = AuthService.generate_access_token(user)

    response = jsonify({
        "message": "User registered successfully",
        "user": _user_to_dict(user)
    })

    response.set_cookie(
        'access_token_cookie',
        access_token,
        max_age=24*60*60,
        secure=False,  # Set to True in production with HTTPS
        httponly=True,
        samesite='Lax',
        path='/'
    )

    return response, 201


@auth_bp.route('/me', methods=['GET'])
@jwt_required(optional=True)
def get_current_user():
    """
    Restore authenticated user from cookie.
    Called on page load by frontend to rehydrate user state.
    """
    user_id = get_jwt_identity()

    if not user_id:
        return jsonify({"code": "UNAUTHORIZED", "message": "Not authenticated"}), 401

    user = User.query.get(int(user_id))

    if not user:
        return jsonify({"code": "NOT_FOUND", "message": "User not found"}), 404

    return jsonify({
        "user": _user_to_dict(user)
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Logout by clearing the HttpOnly cookie.
    """
    response = jsonify({
        "message": "Logged out successfully"
    })

    # Clear the cookie by setting max_age to 0
    response.set_cookie(
        'access_token_cookie',
        '',
        max_age=0,
        secure=False,
        httponly=True,
        samesite='Lax',
        path='/'
    )
    return response, 200


@auth_bp.route('/profile', methods=['PUT', 'PATCH'])
@jwt_required()
def update_profile():
    """
    Update logged-in user profile details (e.g. name, email).
    """
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"code": "UNAUTHORIZED", "message": "Not authenticated"}), 401

    data = request.get_json() or {}
    user, error = AuthService.update_profile(
        user_id=int(user_id),
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        facility=data.get('facility')
    )

    if error:
        status_code = 409 if error.get('code') == 'CONFLICT' else 400
        return jsonify(error), status_code

    return jsonify({
        "message": "Profile updated successfully",
        "user": _user_to_dict(user)
    }), 200


# ============================================================
# Profile & Account Settings
# ============================================================
# NOTE: PUT/PATCH /auth/profile above is the canonical profile update and is
# left untouched — the frontend depends on its name/email/phone/facility
# contract. The endpoints below are additive.
_PROFILE_STATUS = {'VALIDATION_ERROR': 400, 'UNAUTHORIZED': 401,
                   'INVALID_CREDENTIALS': 403, 'FORBIDDEN': 403,
                   'NOT_FOUND': 404}


@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Full profile incl. preferences — backs the Profile/Settings screens."""
    result, error = ProfileService.get_profile(int(get_jwt_identity()))
    if error:
        return jsonify(error), _PROFILE_STATUS.get(error['code'], 400)
    return jsonify({"user": result}), 200


@auth_bp.route('/profile/details', methods=['PUT'])
@jwt_required()
def update_profile_details():
    """
    Update the extended profile fields the Settings screen offers
    (dob, gender, address, avatar_url, plus name/phone).

    Email and role are intentionally not editable here.
    """
    data = request.get_json(silent=True) or {}
    result, error = ProfileService.update_profile(int(get_jwt_identity()), data)
    if error:
        return jsonify(error), _PROFILE_STATUS.get(error['code'], 400)
    return jsonify({"message": "Profile updated successfully", "user": result}), 200


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    data = request.get_json(silent=True) or {}
    result, error = ProfileService.change_password(
        int(get_jwt_identity()),
        data.get('current_password'),
        data.get('new_password'),
    )
    if error:
        return jsonify(error), _PROFILE_STATUS.get(error['code'], 400)
    return jsonify(result), 200


@auth_bp.route('/preferences', methods=['PUT'])
@jwt_required()
def update_preferences():
    """Notification and privacy preferences."""
    data = request.get_json(silent=True) or {}
    result, error = ProfileService.update_preferences(int(get_jwt_identity()), data)
    if error:
        return jsonify(error), _PROFILE_STATUS.get(error['code'], 400)
    return jsonify({"message": "Preferences updated successfully", "user": result}), 200
