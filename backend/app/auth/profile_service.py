"""
Profile & account-settings operations.

Backs the Settings / Profile screens: viewing and editing profile details
(name, phone, date of birth, gender, address, avatar), changing the password,
and updating notification/privacy preferences.

Email is deliberately NOT editable here — it is the login identity and changing
it needs a verification flow. Role is never client-editable (privilege
escalation).
"""
from datetime import datetime

from app.extensions import db
from app.auth.models import User

# Fields a user may change about themselves.
EDITABLE_FIELDS = {"name", "phone", "dob", "gender", "address", "avatar_url"}
PREFERENCE_FIELDS = {"notify_email", "notify_sms", "notify_push", "profile_public"}
ALLOWED_GENDERS = {"Male", "Female", "Other", "Prefer not to say"}


def _clean_phone(value):
    """Accept common phone formats; store digits with an optional leading +."""
    raw = str(value).strip()
    compact = raw.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if compact.startswith("+"):
        digits, prefix = compact[1:], "+"
    else:
        digits, prefix = compact, ""
    if not digits.isdigit():
        return None, "Phone number may only contain digits, spaces, -, () and a leading +."
    if not (7 <= len(digits) <= 15):
        return None, "Phone number must be between 7 and 15 digits."
    return prefix + digits, None


class ProfileService:
    @staticmethod
    def get_profile(user_id):
        user = User.query.get(user_id)
        if not user:
            return None, {"code": "NOT_FOUND", "message": "User not found"}
        return user.to_dict(include_preferences=True), None

    @staticmethod
    def update_profile(user_id, data):
        """Partial update — only the provided editable fields are changed."""
        user = User.query.get(user_id)
        if not user:
            return None, {"code": "NOT_FOUND", "message": "User not found"}

        if not isinstance(data, dict) or not data:
            return None, {"code": "VALIDATION_ERROR", "message": "No fields provided."}

        # Reject attempts to change protected fields outright, so the client
        # never believes a change was applied when it was not.
        for protected in ("email", "role", "id", "password", "password_hash"):
            if protected in data:
                return None, {"code": "VALIDATION_ERROR",
                              "message": f"'{protected}' cannot be changed here."}

        unknown = set(data) - EDITABLE_FIELDS
        if unknown:
            return None, {"code": "VALIDATION_ERROR",
                          "message": "Unknown field(s): " + ", ".join(sorted(unknown))}

        if "name" in data:
            name = str(data["name"] or "").strip()
            if not name:
                return None, {"code": "VALIDATION_ERROR", "message": "Name cannot be empty."}
            if len(name) > 100:
                return None, {"code": "VALIDATION_ERROR", "message": "Name is too long (max 100)."}
            user.name = name

        if "phone" in data:
            if data["phone"] in (None, ""):
                user.phone = None
            else:
                phone, err = _clean_phone(data["phone"])
                if err:
                    return None, {"code": "VALIDATION_ERROR", "message": err}
                user.phone = phone

        if "dob" in data:
            if data["dob"] in (None, ""):
                user.dob = None
            else:
                try:
                    parsed = datetime.strptime(str(data["dob"]), "%Y-%m-%d").date()
                except ValueError:
                    return None, {"code": "VALIDATION_ERROR",
                                  "message": "dob must be in YYYY-MM-DD format."}
                if parsed > datetime.utcnow().date():
                    return None, {"code": "VALIDATION_ERROR",
                                  "message": "Date of birth cannot be in the future."}
                user.dob = parsed

        if "gender" in data:
            if data["gender"] in (None, ""):
                user.gender = None
            elif data["gender"] not in ALLOWED_GENDERS:
                return None, {"code": "VALIDATION_ERROR",
                              "message": "gender must be one of: " + ", ".join(sorted(ALLOWED_GENDERS))}
            else:
                user.gender = data["gender"]

        if "address" in data:
            address = (data["address"] or "").strip() or None
            if address and len(address) > 255:
                return None, {"code": "VALIDATION_ERROR", "message": "Address is too long (max 255)."}
            user.address = address

        if "avatar_url" in data:
            user.avatar_url = (data["avatar_url"] or "").strip() or None

        db.session.commit()
        return user.to_dict(include_preferences=True), None

    @staticmethod
    def change_password(user_id, current_password, new_password):
        user = User.query.get(user_id)
        if not user:
            return None, {"code": "NOT_FOUND", "message": "User not found"}

        if not current_password or not new_password:
            return None, {"code": "VALIDATION_ERROR",
                          "message": "current_password and new_password are required."}

        if not user.check_password(current_password):
            # NOTE: deliberately not 401 — the session is valid, only the
            # supplied password is wrong. A 401 would trip the frontend's
            # global "unauthorized" interceptor and log the user out.
            return None, {"code": "INVALID_CREDENTIALS",
                          "message": "Current password is incorrect."}

        if len(new_password) < 8:
            return None, {"code": "VALIDATION_ERROR",
                          "message": "New password must be at least 8 characters."}

        if current_password == new_password:
            return None, {"code": "VALIDATION_ERROR",
                          "message": "New password must be different from the current password."}

        user.set_password(new_password)
        db.session.commit()
        return {"message": "Password changed successfully"}, None

    @staticmethod
    def update_preferences(user_id, data):
        user = User.query.get(user_id)
        if not user:
            return None, {"code": "NOT_FOUND", "message": "User not found"}

        if not isinstance(data, dict) or not data:
            return None, {"code": "VALIDATION_ERROR", "message": "No preferences provided."}

        unknown = set(data) - PREFERENCE_FIELDS
        if unknown:
            return None, {"code": "VALIDATION_ERROR",
                          "message": "Unknown preference(s): " + ", ".join(sorted(unknown))}

        for field in PREFERENCE_FIELDS:
            if field in data:
                if not isinstance(data[field], bool):
                    return None, {"code": "VALIDATION_ERROR",
                                  "message": f"'{field}' must be true or false."}
                setattr(user, field, data[field])

        db.session.commit()
        return user.to_dict(include_preferences=True), None
