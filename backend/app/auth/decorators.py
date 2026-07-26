from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # 1. Ensure a valid JWT is present in the request header
            verify_jwt_in_request()

            # 2. Extract the claims
            claims = get_jwt()

            # 3. Check if the user's role matches the required role
            if claims.get("role") != required_role:
                return jsonify({
                    "code": "FORBIDDEN",
                    "message": f"{required_role.capitalize()} access required."
                }), 403

            # 4. If everything passes, execute the actual controller function
            return fn(*args, **kwargs)
        return decorator
    return wrapper