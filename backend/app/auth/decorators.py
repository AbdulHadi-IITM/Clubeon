from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def role_required(*required_roles):
    """
    Restrict a route to one or more roles.

        @role_required('owner')                 # single role
        @role_required('front-desk', 'owner')   # any of these roles

    Returns 401 when unauthenticated (via verify_jwt_in_request) and 403 when
    the caller's role is not permitted.
    """
    if not required_roles:
        raise ValueError("role_required() needs at least one role")

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # 1. Ensure a valid JWT is present
            verify_jwt_in_request()

            # 2. Extract the claims
            claims = get_jwt()

            # 3. Check the caller's role is one of the permitted roles
            if claims.get("role") not in required_roles:
                if len(required_roles) == 1:
                    message = f"{required_roles[0].capitalize()} access required."
                else:
                    allowed = ", ".join(required_roles)
                    message = f"Access restricted to: {allowed}."
                return jsonify({"code": "FORBIDDEN", "message": message}), 403

            # 4. If everything passes, execute the actual controller function
            return fn(*args, **kwargs)
        return decorator
    return wrapper
