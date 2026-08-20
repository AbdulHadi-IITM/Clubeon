"""
Tests for profile & account settings (/api/v1/auth/profile, /change-password,
/preferences).

These back the Settings screens. Before this feature the profile fields
(phone, dob, gender, address) did not exist on the model at all, so the UI
could show them but never save them.
"""
from datetime import timedelta

import pytest
from flask_jwt_extended import create_access_token

from app.auth.models import User

PROFILE = "/api/v1/auth/profile"
# develop owns PUT /auth/profile (name/email/phone/facility); the extended
# settings fields live on /auth/profile/details.
PROFILE_DETAILS = "/api/v1/auth/profile/details"


def _login(client, app, user):
    with app.app_context():
        token = create_access_token(identity=str(user.id),
                                    additional_claims={"role": user.role},
                                    expires_delta=timedelta(hours=1))
    client.set_cookie("access_token_cookie", token)


# ---------------- read ----------------
def test_get_profile_returns_all_fields(client, app, make_player):
    user = make_player(email="p1@test.com")
    _login(client, app, user)
    r = client.get(PROFILE)
    assert r.status_code == 200
    u = r.json["user"]
    for field in ("id", "name", "email", "role", "phone", "dob",
                  "gender", "address", "avatar_url", "preferences"):
        assert field in u
    assert set(u["preferences"]) == {"notify_email", "notify_sms",
                                     "notify_push", "profile_public"}


def test_profile_requires_auth(client):
    assert client.get(PROFILE).status_code == 401


# ---------------- phone (the reported problem) ----------------
def test_phone_number_can_be_updated(client, app, make_player):
    user = make_player(email="phone@test.com")
    _login(client, app, user)

    r = client.put(PROFILE_DETAILS, json={"phone": "+91 98765 43210"})
    assert r.status_code == 200
    assert r.json["user"]["phone"] == "+919876543210"

    with app.app_context():
        assert User.query.get(user.id).phone == "+919876543210"


def test_phone_can_be_cleared(client, app, make_player):
    user = make_player(email="phoneclear@test.com")
    _login(client, app, user)
    client.put(PROFILE_DETAILS, json={"phone": "9876543210"})
    r = client.put(PROFILE_DETAILS, json={"phone": ""})
    assert r.status_code == 200
    assert r.json["user"]["phone"] is None


@pytest.mark.parametrize("bad", ["abcd", "12", "1" * 20, "98765-abc"])
def test_invalid_phone_rejected(client, app, make_player, bad):
    user = make_player(email=f"badphone{abs(hash(bad))}@test.com")
    _login(client, app, user)
    r = client.put(PROFILE_DETAILS, json={"phone": bad})
    assert r.status_code == 400
    assert r.json["code"] == "VALIDATION_ERROR"


# ---------------- other profile fields ----------------
def test_update_full_profile(client, app, make_player):
    user = make_player(email="full@test.com")
    _login(client, app, user)
    r = client.put(PROFILE_DETAILS, json={
        "name": "Varun Karthik", "phone": "9876543210",
        "dob": "2000-06-15", "gender": "Male",
        "address": "123 Playmaker Avenue, Chennai",
    })
    assert r.status_code == 200
    u = r.json["user"]
    assert u["name"] == "Varun Karthik"
    assert u["dob"] == "2000-06-15"
    assert u["gender"] == "Male"
    assert u["address"].startswith("123 Playmaker")


def test_partial_update_leaves_other_fields(client, app, make_player):
    user = make_player(email="partial@test.com")
    _login(client, app, user)
    client.put(PROFILE_DETAILS, json={"phone": "9876543210", "gender": "Other"})
    r = client.put(PROFILE_DETAILS, json={"address": "New Street"})
    assert r.json["user"]["phone"] == "9876543210"
    assert r.json["user"]["gender"] == "Other"
    assert r.json["user"]["address"] == "New Street"


def test_future_dob_rejected(client, app, make_player):
    user = make_player(email="dob@test.com")
    _login(client, app, user)
    r = client.put(PROFILE_DETAILS, json={"dob": "299-01-01".replace("299", "2999")})
    assert r.status_code == 400


def test_invalid_gender_rejected(client, app, make_player):
    user = make_player(email="gender@test.com")
    _login(client, app, user)
    r = client.put(PROFILE_DETAILS, json={"gender": "Robot"})
    assert r.status_code == 400


def test_empty_name_rejected(client, app, make_player):
    user = make_player(email="emptyname@test.com")
    _login(client, app, user)
    r = client.put(PROFILE_DETAILS, json={"name": "   "})
    assert r.status_code == 400


# ---------------- protected fields ----------------
@pytest.mark.parametrize("field,value", [("email", "new@test.com"),
                                         ("role", "owner"),
                                         ("password", "hacked")])
def test_protected_fields_cannot_be_changed(client, app, make_player, field, value):
    user = make_player(email=f"prot_{field}@test.com")
    _login(client, app, user)
    r = client.put(PROFILE_DETAILS, json={field: value})
    assert r.status_code == 400
    with app.app_context():
        fresh = User.query.get(user.id)
        assert fresh.role == "player"
        assert fresh.email == f"prot_{field}@test.com"


def test_unknown_field_rejected(client, app, make_player):
    user = make_player(email="unknown@test.com")
    _login(client, app, user)
    r = client.put(PROFILE_DETAILS, json={"is_admin": True})
    assert r.status_code == 400


# ---------------- change password ----------------
def test_change_password_success(client, app, make_player):
    user = make_player(email="pw@test.com", password="OldPassword1!")
    _login(client, app, user)
    r = client.post("/api/v1/auth/change-password", json={
        "current_password": "OldPassword1!", "new_password": "BrandNewPass2!"})
    assert r.status_code == 200

    client.post("/api/v1/auth/logout")
    ok = client.post("/api/v1/auth/login", json={
        "email": "pw@test.com", "password": "BrandNewPass2!"})
    assert ok.status_code == 200


def test_change_password_wrong_current(client, app, make_player):
    user = make_player(email="pw2@test.com", password="OldPassword1!")
    _login(client, app, user)
    r = client.post("/api/v1/auth/change-password", json={
        "current_password": "WrongOne!", "new_password": "BrandNewPass2!"})
    # Must NOT be 401: the session is valid, only the password is wrong.
    # A 401 would trip the frontend interceptor and log the user out.
    assert r.status_code == 403
    assert r.json["code"] == "INVALID_CREDENTIALS"


def test_change_password_too_short(client, app, make_player):
    user = make_player(email="pw3@test.com", password="OldPassword1!")
    _login(client, app, user)
    r = client.post("/api/v1/auth/change-password", json={
        "current_password": "OldPassword1!", "new_password": "short"})
    assert r.status_code == 400


def test_change_password_must_differ(client, app, make_player):
    user = make_player(email="pw4@test.com", password="OldPassword1!")
    _login(client, app, user)
    r = client.post("/api/v1/auth/change-password", json={
        "current_password": "OldPassword1!", "new_password": "OldPassword1!"})
    assert r.status_code == 400


# ---------------- preferences ----------------
def test_update_preferences(client, app, make_player):
    user = make_player(email="prefs@test.com")
    _login(client, app, user)
    r = client.put("/api/v1/auth/preferences", json={
        "notify_email": False, "notify_sms": True, "profile_public": True})
    assert r.status_code == 200
    prefs = r.json["user"]["preferences"]
    assert prefs["notify_email"] is False
    assert prefs["notify_sms"] is True
    assert prefs["profile_public"] is True
    assert prefs["notify_push"] is True  # untouched


def test_preferences_must_be_boolean(client, app, make_player):
    user = make_player(email="prefsbad@test.com")
    _login(client, app, user)
    r = client.put("/api/v1/auth/preferences", json={"notify_email": "yes"})
    assert r.status_code == 400
