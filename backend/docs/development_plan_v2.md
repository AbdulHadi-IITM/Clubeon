# Development Plan v2 — Backend (Flask REST API)
## Sports Facility Booking & Club Management System

> **Scope**: Backend only. No frontend code. This document is written to be consumed by both the backend engineering team and the UI/frontend team as the authoritative source on what every API does, what it expects, and what it returns.
>
> **Excluded** (teammate's scope): Club/court creation by owners, court-level availability/slot customisation, and pure player user stories.
>
> **API Contract**: All endpoints must conform to `api-docs/openapi.yaml`. Any implementation deviation must be reflected back in that file before the PR is merged.
>
> **Base URL**: `http://127.0.0.1:5000/api/v1`
>
> **Auth mechanism**: JWT stored in an **HttpOnly cookie** (`access_token_cookie`). The frontend does **not** need to manage tokens manually — the browser attaches the cookie automatically on every request. All protected routes verify the cookie via Flask-JWT-Extended.

---

## Table of Contents

1. [Project Structure](#1-project-structure)
2. [Database Models](#2-database-models)
3. [Module: Authentication (`auth`)](#3-module-authentication-auth)
4. [Module: Clubs & Courts (`clubs`)](#4-module-clubs--courts-clubs)
5. [Module: Availability (`availability`)](#5-module-availability-availability)
6. [Module: Bookings (`bookings`)](#6-module-bookings-bookings)
7. [Module: Admin Actions (`admin`)](#7-module-admin-actions-admin)
8. [Module: Memberships (`memberships`)](#8-module-memberships-memberships)
9. [Module: Events & Tournaments (`events`)](#9-module-events--tournaments-events)
10. [Module: Payments (`payments`)](#10-module-payments-payments)
11. [Module: Attendance (`attendance`)](#11-module-attendance-attendance)
12. [Module: Notifications (`notifications`)](#12-module-notifications-notifications)
13. [Cross-Cutting Concerns](#13-cross-cutting-concerns)
14. [Tests Directory Layout](#14-tests-directory-layout)
15. [OpenAPI Deviations Log](#15-openapi-deviations-log)

---

## 1. Project Structure

The backend follows a **domain-first Modular Monolith** — each business capability lives in its own Python package. No app-wide `controllers/` or `services/` folders.

```
backend/
├── run.py                        # Entry point
├── requirements.txt
├── .env
├── migrations/                   # Alembic DB migrations
├── tests/                        # ALL test cases live here
│   ├── conftest.py               # Pytest fixtures (app, db, auth headers)
│   ├── test_auth.py
│   ├── test_clubs.py
│   ├── test_availability.py
│   ├── test_bookings.py
│   ├── test_admin.py
│   ├── test_memberships.py
│   ├── test_events.py
│   ├── test_payments.py
│   ├── test_attendance.py
│   └── test_notifications.py
└── app/
    ├── __init__.py               # App factory — registers all blueprints
    ├── config.py
    ├── extensions.py             # db, jwt, migrate singletons
    ├── auth/
    │   ├── controllers.py        # Route handlers (Blueprint)
    │   ├── services.py           # Business logic
    │   ├── decorators.py         # @role_required, @owner_required
    │   └── models.py             # User model (if extracted from bookings)
    ├── clubs/
    │   ├── controllers.py
    │   ├── services.py
    │   └── models.py             # Club, Court, OperatingHours
    ├── bookings/
    │   ├── controllers.py
    │   ├── services.py
    │   └── models.py             # Booking, CourtBlock
    ├── memberships/
    │   ├── controllers.py
    │   ├── services.py
    │   └── models.py             # MembershipPlan, Membership
    ├── events/
    │   ├── controllers.py
    │   ├── services.py
    │   └── models.py             # Event, EventRegistration
    ├── payments/
    │   ├── controllers.py
    │   ├── services.py
    │   └── models.py             # Payment, Invoice
    ├── attendance/
    │   ├── controllers.py
    │   ├── services.py
    │   └── models.py             # AttendanceRecord
    └── notifications/
        ├── controllers.py
        ├── services.py
        └── models.py             # Notification, Announcement
```

---

## 2. Database Models

All models are SQLAlchemy ORM classes. Alembic migrations are auto-generated via `flask db migrate`.

### 2.1 `User` *(existing — `app/bookings/models.py`, to be moved to `app/auth/models.py`)*

| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | |
| `name` | String(100) | NOT NULL |
| `email` | String(100) | UNIQUE, NOT NULL |
| `password_hash` | String(255) | Stored via Werkzeug |
| `role` | String(20) | `player`, `owner`, `front-desk` |
| `created_at` | DateTime | server default |

### 2.2 `Club` *(existing — `app/bookings/models.py`, to be moved to `app/clubs/models.py`)*

| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | |
| `name` | String(100) | NOT NULL |
| `address` | String(255) | |
| `owner_id` | FK → `users.id` | NOT NULL |
| `open_time` | String(5) | `HH:MM` format |
| `close_time` | String(5) | `HH:MM` format |
| `slot_duration_minutes` | Integer | Default: 60 |

> **Change from current model**: `OperatingHours` is embedded as flat columns on `Club` (and `Court`) rather than a nested sub-object. The API response will still serialise them as a nested `operating_hours` object to match the OpenAPI schema.

### 2.3 `Court` *(existing — `app/bookings/models.py`, to be moved to `app/clubs/models.py`)*

| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | |
| `club_id` | FK → `clubs.id` | NOT NULL, cascade delete |
| `name` | String(50) | NOT NULL |
| `is_active` | Boolean | Default: True |
| `open_time_override` | String(5) | Nullable — overrides club hours |
| `close_time_override` | String(5) | Nullable |
| `slot_duration_override` | Integer | Nullable |

### 2.4 `Booking` *(existing — `app/bookings/models.py`)*

| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | |
| `user_id` | FK → `users.id` | NOT NULL |
| `court_id` | FK → `courts.id` | NOT NULL |
| `booking_date` | Date | NOT NULL |
| `start_time` | Time | NOT NULL |
| `end_time` | Time | NOT NULL |
| `status` | String(20) | `active`, `released`, `overridden` |
| `is_peak_hour` | Boolean | Default: False |
| `created_at` | DateTime | server default |

**Constraint**: PostgreSQL GiST `ExcludeConstraint` on `(court_id =, booking_date =, tsrange &&)` where `status = 'active'`. This is the database-level double-booking guard.

### 2.5 `CourtBlock` *(new)*

| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | |
| `court_id` | FK → `courts.id` | NOT NULL |
| `start_date` | Date | NOT NULL |
| `end_date` | Date | NOT NULL |
| `title` | String(200) | e.g. "Maintenance", "Tournament" |
| `created_by` | FK → `users.id` | The owner who created the block |
| `created_at` | DateTime | server default |

### 2.6 `MembershipPlan` *(new)*

| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | |
| `club_id` | FK → `clubs.id` | Plan is scoped per club |
| `name` | String(100) | e.g. "Gold", "Silver" |
| `price_monthly` | Float | |
| `benefits` | Text | JSON string or free text describing perks |
| `is_active` | Boolean | Default: True |

### 2.7 `Membership` *(new)*

| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | |
| `user_id` | FK → `users.id` | |
| `plan_id` | FK → `membership_plans.id` | |
| `club_id` | FK → `clubs.id` | Denormalised for fast lookup |
| `status` | String(20) | `active`, `paused`, `expired`, `cancelled` |
| `start_date` | Date | |
| `end_date` | Date | |
| `auto_renew` | Boolean | Default: False |
| `created_at` | DateTime | |

### 2.8 `Event` *(new)*

| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | |
| `club_id` | FK → `clubs.id` | |
| `created_by` | FK → `users.id` | Organizer or owner |
| `title` | String(200) | |
| `description` | Text | |
| `event_date` | Date | |
| `start_time` | Time | |
| `end_time` | Time | |
| `max_attendees` | Integer | Nullable = unlimited |
| `registration_fee` | Float | 0.0 = free |
| `status` | String(20) | `upcoming`, `ongoing`, `completed`, `cancelled` |
| `created_at` | DateTime | |

### 2.9 `EventRegistration` *(new)*

| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | |
| `event_id` | FK → `events.id` | |
| `user_id` | FK → `users.id` | |
| `status` | String(20) | `registered`, `cancelled` |
| `registered_at` | DateTime | |

**Constraint**: UNIQUE on `(event_id, user_id)` — a user can only register once per event.

### 2.10 `Payment` *(new)*

| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | |
| `user_id` | FK → `users.id` | |
| `amount` | Float | |
| `currency` | String(3) | Default: `INR` |
| `payment_type` | String(30) | `booking`, `membership`, `event` |
| `reference_id` | Integer | The booking/membership/event ID |
| `status` | String(20) | `pending`, `completed`, `failed`, `refunded` |
| `gateway_transaction_id` | String(100) | From Razorpay/Stripe |
| `created_at` | DateTime | |

### 2.11 `AttendanceRecord` *(new)*

| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | |
| `user_id` | FK → `users.id` | |
| `booking_id` | FK → `bookings.id` | Nullable (walk-ins may not have a booking) |
| `event_id` | FK → `events.id` | Nullable |
| `check_in_at` | DateTime | |
| `check_out_at` | DateTime | Nullable |

### 2.12 `Notification` *(new)*

| Column | Type | Notes |
|---|---|---|
| `id` | Integer PK | |
| `user_id` | FK → `users.id` | Recipient |
| `title` | String(200) | |
| `body` | Text | |
| `type` | String(30) | `booking`, `event`, `payment`, `announcement` |
| `is_read` | Boolean | Default: False |
| `created_at` | DateTime | |

---

## 3. Module: Authentication (`auth`)

**Blueprint prefix**: `/api/v1/auth`

### 3.1 `POST /auth/register`

**Auth**: None (public)

**Purpose**: Create a new user account. On success, immediately issues a JWT so the user is logged in.

**Request Body**:
```json
{
  "name": "Harshita",
  "email": "harshita@example.com",
  "password": "SecurePass123!",
  "role": "player"
}
```

**Validation Logic** (in `AuthService.register`):
1. All four fields (`name`, `email`, `password`, `role`) must be present → 400 `VALIDATION_ERROR`.
2. `role` must be one of `["player", "owner", "front-desk"]` → 400 `VALIDATION_ERROR`.
3. Query `users` table for existing email → 409 `CONFLICT` if found.
4. Hash password with Werkzeug `generate_password_hash`, persist `User` row.
5. Call `AuthService.generate_access_token(user)` — encodes `user.id` as identity, `user.role` as additional claim, 24h expiry.
6. Set HttpOnly cookie `access_token_cookie` (SameSite=Lax, Secure=False in dev).

**Success Response** `201`:
```json
{
  "message": "User registered successfully",
  "user": { "id": 1, "name": "Harshita", "email": "harshita@example.com", "role": "player" }
}
```

**Error Responses**:
| Code | HTTP | Condition |
|---|---|---|
| `VALIDATION_ERROR` | 400 | Missing or invalid fields |
| `CONFLICT` | 409 | Email already registered |
| `INTERNAL_ERROR` | 500 | DB failure |

---

### 3.2 `POST /auth/login`

**Auth**: None (public)

**Purpose**: Authenticate a user with email + password. Issues a JWT cookie on success.

**Request Body**:
```json
{ "email": "harshita@example.com", "password": "SecurePass123!" }
```

**Logic** (in `AuthService.login`):
1. Validate both fields present → 400 if missing.
2. Query `users` by email.
3. Call `user.check_password(password)` (Werkzeug `check_password_hash`).
4. If match: generate token, set cookie, return user data.
5. If no match: return 401 (do NOT reveal whether email or password was wrong).

**Success Response** `200`:
```json
{
  "message": "Login successful",
  "user": { "id": 1, "name": "Harshita", "email": "harshita@example.com", "role": "player" }
}
```

**Error Responses**:
| Code | HTTP | Condition |
|---|---|---|
| `VALIDATION_ERROR` | 400 | Missing email/password |
| `UNAUTHORIZED` | 401 | Invalid credentials |

---

### 3.3 `GET /auth/me`

**Auth**: Optional JWT (cookie). If valid cookie present, returns user data.

**Purpose**: Used by the frontend on page load to rehydrate user session state without forcing a re-login.

**Logic**:
1. Flask-JWT-Extended reads cookie, extracts `user_id` from identity.
2. If no valid JWT → 401.
3. Query `User` by `user_id` → 404 if not found.
4. Return user data.

**Success Response** `200`:
```json
{ "user": { "id": 1, "name": "Harshita", "email": "harshita@example.com", "role": "player" } }
```

---

### 3.4 `POST /auth/logout`

**Auth**: None required (clearing the cookie is idempotent).

**Purpose**: Invalidate the session by clearing the HttpOnly cookie.

**Logic**: Set `access_token_cookie` with `max_age=0` to expire it immediately.

**Success Response** `200`:
```json
{ "message": "Logged out successfully" }
```

> **Note for UI team**: After calling this endpoint, the browser will no longer send the auth cookie. Redirect the user to the login page immediately.

---

### 3.5 `@role_required(role)` Decorator

Located in `app/auth/decorators.py`. Applied to any protected route.

**Logic**:
1. Calls `verify_jwt_in_request()` — reads the HttpOnly cookie.
2. Extracts `claims = get_jwt()`.
3. Checks `claims['role'] == required_role`. If not → 403 `FORBIDDEN`.

**Current roles**: `player`, `owner`, `front-desk`.

---

## 4. Module: Clubs & Courts (`clubs`)

**Blueprint prefix**: `/api/v1`

> This module's **create/update club/court** endpoints are the teammate's responsibility. This section documents the **read/discovery** endpoints that your scope covers.

### 4.1 `GET /clubs`

**Auth**: Public (no JWT required)

**Purpose**: Returns all active clubs. Primary use case is the public discovery page where players browse available clubs to book at.

**Logic** (in `ClubService.list_clubs`):
1. Query all `Club` rows.
2. Optionally filter by name/location via query params (`?search=badminton`).
3. Serialise `operating_hours` as nested object: `{ open_time, close_time, slot_duration_minutes }`.

**Success Response** `200`:
```json
[
  {
    "id": 1,
    "name": "Ace Sports Club",
    "address": "123 MG Road, Bengaluru",
    "owner_id": 5,
    "operating_hours": {
      "open_time": "06:00",
      "close_time": "22:00",
      "slot_duration_minutes": 60
    }
  }
]
```

---

### 4.2 `GET /clubs/{clubId}/courts`

**Auth**: Public

**Purpose**: Returns all active courts for a given club. Used by the frontend when a player selects a club and wants to see its courts before checking availability.

**Logic**:
1. Validate `clubId` exists → 404 if not.
2. Query all `Court` rows where `club_id = clubId` and `is_active = True`.
3. Serialise `operating_hours_override` as nested object (nullable).

**Success Response** `200`:
```json
[
  {
    "id": 3,
    "club_id": 1,
    "name": "Court 1 - Clay",
    "is_active": true,
    "operating_hours_override": null
  }
]
```

---

## 5. Module: Availability (`availability`)

**Blueprint prefix**: `/api/v1`

### 5.1 `GET /clubs/{clubId}/availability?date=YYYY-MM-DD`

**Auth**: Public

**Purpose**: The core discovery endpoint. Returns a matrix of every active court in the club, and for each court, a list of time slots for the given date. Each slot is marked `available`, `booked`, or `blocked`. The UI uses this to render the booking calendar grid.

**Query Parameters**:
| Param | Type | Required | Notes |
|---|---|---|---|
| `date` | `YYYY-MM-DD` | Yes | The date to check availability for |

**Logic** (in `AvailabilityService.get_availability`):
1. Validate `date` is a valid date string and not in the past → 400 if invalid.
2. Fetch the club and all its active courts (`is_active = True`).
3. For each court:
   a. Determine effective `open_time`, `close_time`, `slot_duration_minutes` — use court-level override if set, else fall back to club-level defaults.
   b. Generate all time slots by iterating from `open_time` to `close_time` in `slot_duration_minutes` increments. E.g., for 06:00–22:00 at 60 min, this produces 16 slots.
   c. Query all `Booking` rows where `court_id = court.id`, `booking_date = date`, `status = 'active'`. Mark overlapping generated slots as `booked`.
   d. Query all `CourtBlock` rows where `court_id = court.id`, `start_date <= date <= end_date`. Mark ALL slots for that court as `blocked`.
4. Return the full matrix.

**Success Response** `200`:
```json
[
  {
    "court_id": 3,
    "court_name": "Court 1 - Clay",
    "slots": [
      { "start_time": "06:00", "end_time": "07:00", "status": "available" },
      { "start_time": "07:00", "end_time": "08:00", "status": "booked" },
      { "start_time": "08:00", "end_time": "09:00", "status": "blocked" }
    ]
  }
]
```

**Error Responses**:
| Code | HTTP | Condition |
|---|---|---|
| `VALIDATION_ERROR` | 400 | Invalid/missing date |
| `NOT_FOUND` | 404 | Club not found |

> **Note for UI team**: Always call this endpoint before showing the booking form. Use the `status` field to disable already-booked or blocked slots in the UI. Do not rely on client-side state to track availability — always fetch fresh from this endpoint.

---

## 6. Module: Bookings (`bookings`)

**Blueprint prefix**: `/api/v1`

### 6.1 `POST /bookings`

**Auth**: JWT required. Role: `player` (enforced by `@role_required('player')`).

**Purpose**: A player books a specific slot on a specific court. This is the primary transactional endpoint.

**Request Body**:
```json
{
  "court_id": 3,
  "booking_date": "2026-08-15",
  "start_time": "09:00",
  "end_time": "10:00"
}
```

**Logic** (in `BookingService.create_booking`):
1. Validate all required fields present and correctly typed → 400.
2. Validate `start_time < end_time` → 400.
3. Validate `booking_date` is not in the past → 400.
4. Validate the slot aligns with the court's configured `slot_duration_minutes` (e.g. a 90-min booking is invalid if court uses 60-min slots).
5. Check no active `CourtBlock` covers this court on `booking_date` → 409 `COURT_BLOCKED`.
6. Attempt DB insert. The PostgreSQL GiST `ExcludeConstraint` (on `court_id`, `booking_date`, `tsrange`) will raise `IntegrityError` on any overlap → catch and return 409 `CONCURRENCY_CONFLICT`.
7. On success, trigger a `Notification` record for the user (booking confirmation).

**Success Response** `201`:
```json
{ "message": "Booking successful", "booking_id": 42 }
```

**Error Responses**:
| Code | HTTP | Condition |
|---|---|---|
| `VALIDATION_ERROR` | 400 | Bad payload |
| `COURT_BLOCKED` | 409 | Court is blocked for maintenance/event |
| `CONCURRENCY_CONFLICT` | 409 | Slot was taken by another user simultaneously |
| `INTERNAL_ERROR` | 500 | Unexpected DB error |

---

### 6.2 `GET /bookings/my`

**Auth**: JWT required. Any role.

**Purpose**: Returns all bookings made by the currently authenticated user. The UI uses this to render "My Bookings" page.

**Logic**:
1. Extract `user_id` from JWT.
2. Query `Booking` where `user_id = current_user`, ordered by `booking_date DESC, start_time ASC`.
3. Optionally support `?status=active` filter.

**Success Response** `200`:
```json
[
  {
    "id": 42,
    "court_id": 3,
    "court_name": "Court 1 - Clay",
    "club_name": "Ace Sports Club",
    "booking_date": "2026-08-15",
    "start_time": "09:00",
    "end_time": "10:00",
    "status": "active",
    "created_at": "2026-07-30T10:00:00"
  }
]
```

---

### 6.3 `PATCH /bookings/{bookingId}/release`

**Auth**: JWT required. Any role (but ownership enforced in logic).

**Purpose**: A player voluntarily releases/cancels their booked slot. Sets `status = 'released'` so the slot becomes available again.

**Logic** (in `BookingService.release_booking`):
1. Fetch `Booking` by `bookingId` → 404 if not found.
2. Verify `booking.user_id == current_user_id` → 403 if not the owner.
3. Verify `booking.status == 'active'` → 409 if already released/overridden.
4. Optionally: enforce a **cancellation window** (e.g. cannot cancel < 1 hour before start).
5. Set `booking.status = 'released'`, commit.
6. Trigger a `Notification` to the user confirming cancellation.

**Success Response** `200`:
```json
{ "message": "Slot released successfully", "booking_id": 42 }
```

---

## 7. Module: Admin Actions (`admin`)

**Blueprint prefix**: `/api/v1/admin`

### 7.1 `POST /admin/overrides`

**Auth**: JWT required. Role: `owner`.

**Purpose**: An owner forcefully overrides (cancels) an existing player booking — e.g. due to an emergency or court reassignment. A reason is mandatory and logged for accountability.

**Request Body**:
```json
{
  "booking_id": 42,
  "reason": "Emergency court closure due to flood damage in the facility."
}
```

**Logic** (in `AdminService.override_booking`):
1. Validate `booking_id` and `reason` present; `reason` must be ≥ 20 characters → 400.
2. Fetch `Booking` → 404 if not found.
3. Verify the booking's court belongs to the calling owner's club via `AuthorizationService.verify_court_ownership(court_id, owner_id)` → 403 if not.
4. Check booking `status == 'active'` → 409 if already resolved.
5. Set `booking.status = 'overridden'`, commit.
6. Trigger a `Notification` to the affected player with the override reason.

**Success Response** `201`:
```json
{ "message": "Override initiated", "booking_id": 42 }
```

---

### 7.2 `POST /admin/blocks`

**Auth**: JWT required. Role: `owner`.

**Purpose**: Block a court for a date range. Prevents any new bookings during that period. Existing bookings on those dates are NOT automatically cancelled (that requires separate override calls), but the availability endpoint will show slots as `blocked`.

**Request Body**:
```json
{
  "court_id": 3,
  "start_date": "2026-08-20",
  "end_date": "2026-08-22",
  "title": "Annual Maintenance"
}
```

**Logic** (in `AdminService.block_court`):
1. Validate all fields present, `start_date <= end_date` → 400.
2. Verify court ownership via `AuthorizationService.verify_court_ownership` → 403.
3. Insert `CourtBlock` row with `created_by = owner_id`.

**Success Response** `201`:
```json
{ "message": "Court blocked successfully", "block_id": 7 }
```

---

## 8. Module: Memberships (`memberships`)

**Blueprint prefix**: `/api/v1`

### 8.1 `GET /clubs/{clubId}/membership-plans`

**Auth**: Public

**Purpose**: Returns all active membership plans for a given club. Used by the UI to display the pricing/benefits page.

**Logic**:
1. Validate `clubId` exists → 404.
2. Query `MembershipPlan` where `club_id = clubId` and `is_active = True`.

**Success Response** `200`:
```json
[
  {
    "id": 1,
    "name": "Gold",
    "price_monthly": 2500.0,
    "benefits": "Unlimited bookings, priority slots, guest passes",
    "is_active": true
  }
]
```

---

### 8.2 `POST /memberships`

**Auth**: JWT required. Any role.

**Purpose**: Subscribe a user to a membership plan for a club.

**Request Body**:
```json
{
  "plan_id": 1,
  "auto_renew": true
}
```

**Logic** (in `MembershipService.subscribe`):
1. Validate `plan_id` exists and is active → 404/400.
2. Check if the user already has an `active` membership at this club → 409 `ALREADY_MEMBER`.
3. Compute `start_date = today`, `end_date = today + 30 days`.
4. Insert `Membership` row with `status = 'active'`.
5. Create a `Payment` record (`payment_type = 'membership'`, `status = 'pending'`).
6. Trigger `Notification` to user confirming subscription.

**Success Response** `201`:
```json
{ "message": "Membership activated", "membership_id": 5, "payment_id": 12 }
```

---

### 8.3 `GET /memberships/my`

**Auth**: JWT required. Any role.

**Purpose**: Returns the current user's active (and past) memberships. Used by UI to display membership status and renewal date.

**Logic**:
1. Query `Membership` joined with `MembershipPlan` and `Club` where `user_id = current_user`.
2. Order by `created_at DESC`.

**Success Response** `200`:
```json
[
  {
    "id": 5,
    "plan_name": "Gold",
    "club_name": "Ace Sports Club",
    "status": "active",
    "start_date": "2026-07-30",
    "end_date": "2026-08-29",
    "auto_renew": true
  }
]
```

---

### 8.4 `PATCH /memberships/{membershipId}/cancel`

**Auth**: JWT required. Ownership enforced.

**Purpose**: A user cancels their own membership. Sets `status = 'cancelled'`.

**Logic**:
1. Fetch `Membership` → 404 if not found.
2. Verify `membership.user_id == current_user_id` → 403.
3. Verify `status == 'active'` → 409 if already cancelled/expired.
4. Set `status = 'cancelled'`, commit.
5. Trigger cancellation `Notification`.

---

### 8.5 Internal: `MembershipService.is_active_member(user_id, club_id)`

**Purpose**: A service-layer function (not an API endpoint) called by other modules (e.g. `bookings`) to check if a user has an active membership at a club — to apply discounts or allow priority bookings.

**Returns**: `True / False`

---

## 9. Module: Events & Tournaments (`events`)

**Blueprint prefix**: `/api/v1`

### 9.1 `GET /clubs/{clubId}/events`

**Auth**: Public

**Purpose**: Returns all upcoming events at a given club. Used by UI to display the events/tournaments discovery page.

**Logic**:
1. Query `Event` where `club_id = clubId` and `status IN ('upcoming', 'ongoing')` and `event_date >= today`.
2. Return with registration count and whether the user is registered (if JWT present).

**Success Response** `200`:
```json
[
  {
    "id": 1,
    "title": "Summer Badminton Tournament",
    "event_date": "2026-08-10",
    "start_time": "08:00",
    "end_time": "18:00",
    "registration_fee": 500.0,
    "max_attendees": 64,
    "current_registrations": 23,
    "status": "upcoming"
  }
]
```

---

### 9.2 `POST /events` *(Owner/Organizer only)*

**Auth**: JWT required. Role: `owner`.

**Purpose**: Create a new event or tournament at a club owned by the requester.

**Request Body**:
```json
{
  "club_id": 1,
  "title": "Summer Badminton Tournament",
  "description": "Open singles tournament, all skill levels welcome.",
  "event_date": "2026-08-10",
  "start_time": "08:00",
  "end_time": "18:00",
  "max_attendees": 64,
  "registration_fee": 500.0
}
```

**Logic** (in `EventService.create_event`):
1. Validate all required fields present → 400.
2. Verify the owner owns `club_id` → 403.
3. Validate `event_date` is in the future → 400.
4. Validate `start_time < end_time` → 400.
5. Insert `Event` row with `status = 'upcoming'`, `created_by = current_user_id`.

**Success Response** `201`:
```json
{ "message": "Event created", "event_id": 1 }
```

---

### 9.3 `POST /events/{eventId}/register`

**Auth**: JWT required. Any role.

**Purpose**: Register the current user for an event and initiate payment if a fee applies.

**Logic** (in `EventService.register`):
1. Fetch `Event` → 404 if not found.
2. Verify `event.status == 'upcoming'` → 409 if registration closed.
3. Check `max_attendees` — count existing `registered` registrations. If at capacity → 409 `EVENT_FULL`.
4. Check no existing `EventRegistration` for `(event_id, user_id)` → 409 `ALREADY_REGISTERED`.
5. Insert `EventRegistration` with `status = 'registered'`.
6. If `registration_fee > 0`: create `Payment` record with `status = 'pending'`, `payment_type = 'event'`.
7. Trigger `Notification` to user confirming registration.

**Success Response** `201`:
```json
{ "message": "Registered for event", "registration_id": 8, "payment_id": 15 }
```

---

### 9.4 `DELETE /events/{eventId}/register`

**Auth**: JWT required. Any role.

**Purpose**: Cancel a user's event registration.

**Logic**:
1. Fetch `EventRegistration` for `(event_id, current_user_id)` → 404 if not found.
2. Verify `registration.status == 'registered'` → 409 if already cancelled.
3. Set `status = 'cancelled'`, commit.
4. If payment was made, create a refund `Payment` record (handled by Payments module).

---

## 10. Module: Payments (`payments`)

**Blueprint prefix**: `/api/v1`

### 10.1 `GET /payments/my`

**Auth**: JWT required. Any role.

**Purpose**: Returns all payment records for the current user. Used by UI to display billing history.

**Logic**:
1. Query `Payment` where `user_id = current_user`, ordered `created_at DESC`.

**Success Response** `200`:
```json
[
  {
    "id": 12,
    "amount": 2500.0,
    "currency": "INR",
    "payment_type": "membership",
    "reference_id": 5,
    "status": "completed",
    "gateway_transaction_id": "pay_Razorpay123",
    "created_at": "2026-07-30T10:00:00"
  }
]
```

---

### 10.2 `POST /payments/webhook` *(Razorpay/Stripe Callback)*

**Auth**: None (but validated via HMAC signature in headers)

**Purpose**: Receives payment confirmation/failure events from the payment gateway. Updates `Payment.status` accordingly and triggers downstream actions.

**Logic** (in `PaymentService.handle_webhook`):
1. Validate HMAC signature using `RAZORPAY_WEBHOOK_SECRET` from env → 400 if invalid.
2. Parse event type from payload (`payment.captured`, `payment.failed`, `refund.processed`).
3. Match `gateway_transaction_id` to a `Payment` row → log and ignore if not found.
4. Update `Payment.status` → `'completed'` / `'failed'` / `'refunded'`.
5. If `completed`: trigger `Notification` (receipt) to the user.
6. If `refunded`: update the related booking/membership/event accordingly.

---

### 10.3 Internal: `PaymentService.create_payment(user_id, amount, payment_type, reference_id)`

Service function called by other modules (Bookings, Memberships, Events). Creates a `Payment` record in `pending` state and returns the `payment_id` + gateway order object for the frontend to complete the payment flow.

---

## 11. Module: Attendance (`attendance`)

**Blueprint prefix**: `/api/v1`

### 11.1 `POST /attendance/check-in`

**Auth**: JWT required. Role: `front-desk` or `owner`.

**Purpose**: Front-desk staff records a user's check-in against a booking or event.

**Request Body**:
```json
{ "user_id": 10, "booking_id": 42 }
```

**Logic**:
1. Validate `user_id` and at least one of `booking_id` or `event_id` present → 400.
2. If `booking_id` provided: verify booking exists, belongs to `user_id`, and is `active` → 404/409.
3. Check no existing open `AttendanceRecord` (i.e., `check_out_at IS NULL`) for this user+booking → 409 `ALREADY_CHECKED_IN`.
4. Insert `AttendanceRecord` with `check_in_at = now()`.

**Success Response** `201`:
```json
{ "message": "Check-in recorded", "attendance_id": 3 }
```

---

### 11.2 `PATCH /attendance/{attendanceId}/check-out`

**Auth**: JWT required. Role: `front-desk` or `owner`.

**Purpose**: Records the check-out time for an open attendance record.

**Logic**:
1. Fetch `AttendanceRecord` → 404 if not found.
2. Verify `check_out_at IS NULL` → 409 if already checked out.
3. Set `check_out_at = now()`, commit.

**Success Response** `200`:
```json
{ "message": "Check-out recorded", "duration_minutes": 55 }
```

---

### 11.3 `GET /admin/attendance`

**Auth**: JWT required. Role: `owner`.

**Purpose**: Owner views all attendance records across their clubs. Used for operations dashboards.

**Query Parameters**: `?club_id=1&date=2026-07-30`

**Logic**:
1. Verify owner owns `club_id` → 403.
2. Query `AttendanceRecord` joined with `User`, `Booking`, `Court`, `Club` filtered by club and date.

---

## 12. Module: Notifications (`notifications`)

**Blueprint prefix**: `/api/v1`

### 12.1 `GET /notifications`

**Auth**: JWT required. Any role.

**Purpose**: Returns all in-app notifications for the current user, ordered newest-first. Used by the UI notification bell/panel.

**Logic**:
1. Query `Notification` where `user_id = current_user`, `ORDER BY created_at DESC`.
2. Return with `unread_count` in the response envelope.

**Success Response** `200`:
```json
{
  "unread_count": 3,
  "notifications": [
    {
      "id": 1,
      "title": "Booking Confirmed",
      "body": "Court 1 - Clay on 2026-08-15 at 09:00 is confirmed.",
      "type": "booking",
      "is_read": false,
      "created_at": "2026-07-30T10:00:00"
    }
  ]
}
```

---

### 12.2 `PATCH /notifications/{notificationId}/read`

**Auth**: JWT required. Ownership enforced.

**Purpose**: Mark a single notification as read.

**Logic**:
1. Fetch `Notification` → 404.
2. Verify `notification.user_id == current_user_id` → 403.
3. Set `is_read = True`, commit.

---

### 12.3 `PATCH /notifications/read-all`

**Auth**: JWT required.

**Purpose**: Mark all of the current user's notifications as read (e.g. "clear all" button).

**Logic**: Bulk update `Notification` where `user_id = current_user` and `is_read = False`.

---

### 12.4 Internal: `NotificationService.send(user_id, title, body, type)`

Internal service function — not a public API endpoint. Called by other modules after significant events (booking created, membership activated, override issued, etc.). 

**Behaviour**:
1. Inserts a `Notification` DB record (always — for in-app display).
2. Optionally dispatches Email via SendGrid (configurable per notification type).
3. Optionally dispatches SMS via Twilio (for critical events like overrides).

---

## 13. Cross-Cutting Concerns

### 13.1 Error Response Shape

All error responses must use the `ErrorResponse` schema defined in `openapi.yaml`:
```json
{ "code": "ERROR_CODE_SNAKE_CASE", "message": "Human-readable description." }
```

Never expose internal stack traces or DB error messages to the client.

### 13.2 JWT Strategy

- Token lives in `HttpOnly`, `SameSite=Lax` cookie named `access_token_cookie`.
- Flask-JWT-Extended is configured to read from cookies (via `JWT_TOKEN_LOCATION = ['cookies']`).
- The UI **does not** need to store or manage the token. The browser handles it automatically.
- Token expiry: **24 hours**. There is no refresh token in v1 — user must re-login after expiry.

### 13.3 Multi-Tenant Isolation

Every owner-scoped action must call `AuthorizationService.verify_court_ownership(court_id, owner_id)` or an equivalent club-level check before proceeding. This prevents Owner A from modifying Owner B's courts or bookings.

### 13.4 `app/__init__.py` — Blueprint Registration

As new modules are added, each module's `controllers.py` must be registered in the app factory:
```python
from app.clubs.controllers import clubs_bp
app.register_blueprint(clubs_bp)
# ... and so on for each new module
```

---

## 14. Tests Directory Layout

All test files live in `backend/tests/`. Run with `pytest` from the `backend/` directory.

```
tests/
├── conftest.py               # Shared fixtures
├── test_auth.py
├── test_clubs.py
├── test_availability.py
├── test_bookings.py
├── test_admin.py
├── test_memberships.py
├── test_events.py
├── test_payments.py
├── test_attendance.py
└── test_notifications.py
```

### 14.1 `conftest.py` — Fixtures

Must provide:
- `app` fixture: creates a Flask test app with a fresh in-memory SQLite DB.
- `client` fixture: Flask test client.
- `db_session` fixture: DB session with rollback after each test.
- `auth_headers(role)` fixture: returns a dict with a valid JWT cookie for a given role (registers + logs in a test user).
- Helper functions: `make_player()`, `make_owner()`, `make_club(owner_id)`, `make_court(club_id)`.

### 14.2 `test_auth.py`

| Test | Description |
|---|---|
| `test_register_success` | Valid payload → 201, user in DB, cookie set |
| `test_register_duplicate_email` | Same email twice → 409 |
| `test_register_invalid_role` | Role = "superadmin" → 400 |
| `test_register_missing_fields` | Missing `name` → 400 |
| `test_login_success` | Valid credentials → 200, cookie set |
| `test_login_wrong_password` | Wrong password → 401 |
| `test_login_nonexistent_email` | Unknown email → 401 |
| `test_me_authenticated` | Valid cookie → 200 with user data |
| `test_me_unauthenticated` | No cookie → 401 |
| `test_logout` | Clears cookie → 200 |

### 14.3 `test_clubs.py`

| Test | Description |
|---|---|
| `test_list_clubs_public` | No auth, returns list → 200 |
| `test_list_clubs_empty` | No clubs in DB → empty array |
| `test_get_courts_for_club` | Valid clubId → 200 with courts |
| `test_get_courts_invalid_club` | clubId = 9999 → 404 |

### 14.4 `test_availability.py`

| Test | Description |
|---|---|
| `test_availability_no_bookings` | All slots = `available` |
| `test_availability_with_booking` | Booked slot shows `booked` |
| `test_availability_blocked_court` | Active block → all slots `blocked` |
| `test_availability_missing_date` | No `?date=` → 400 |
| `test_availability_past_date` | Past date → 400 |
| `test_availability_invalid_club` | clubId 9999 → 404 |
| `test_slot_generation` | Verify correct number of slots for open/close times |

### 14.5 `test_bookings.py`

| Test | Description |
|---|---|
| `test_create_booking_success` | Valid booking → 201 |
| `test_create_booking_overlap` | Two players book same slot simultaneously → 409 `CONCURRENCY_CONFLICT` |
| `test_create_booking_past_date` | Past date → 400 |
| `test_create_booking_blocked_court` | Court blocked on that date → 409 `COURT_BLOCKED` |
| `test_create_booking_invalid_time` | `start_time >= end_time` → 400 |
| `test_create_booking_player_only` | Owner JWT → 403 |
| `test_create_booking_unauthenticated` | No cookie → 401 |
| `test_get_my_bookings` | Returns only current user's bookings |
| `test_release_booking_success` | Release own active booking → 200 |
| `test_release_booking_wrong_user` | Release another user's booking → 403 |
| `test_release_booking_already_released` | Re-release → 409 |

### 14.6 `test_admin.py`

| Test | Description |
|---|---|
| `test_override_booking_success` | Owner overrides a booking at their court → 201 |
| `test_override_booking_wrong_owner` | Owner tries to override booking at another's court → 403 |
| `test_override_booking_short_reason` | Reason < 20 chars → 400 |
| `test_override_booking_not_found` | Invalid booking_id → 404 |
| `test_block_court_success` | Valid block → 201 |
| `test_block_court_wrong_owner` | Blocking another owner's court → 403 |
| `test_block_court_invalid_dates` | `start_date > end_date` → 400 |
| `test_block_court_player_forbidden` | Player tries to block → 403 |

### 14.7 `test_memberships.py`

| Test | Description |
|---|---|
| `test_list_plans_public` | No auth → 200 with plans |
| `test_list_plans_empty` | No plans for club → empty list |
| `test_subscribe_success` | Valid plan → 201 |
| `test_subscribe_already_member` | Already active membership → 409 |
| `test_subscribe_invalid_plan` | plan_id 9999 → 404 |
| `test_get_my_memberships` | Returns current user's memberships |
| `test_cancel_membership_success` | Own active membership → 200 |
| `test_cancel_membership_wrong_user` | Another user's membership → 403 |
| `test_cancel_membership_already_cancelled` | Re-cancel → 409 |

### 14.8 `test_events.py`

| Test | Description |
|---|---|
| `test_list_events_public` | No auth, returns upcoming events |
| `test_create_event_owner` | Owner creates event at their club → 201 |
| `test_create_event_wrong_owner` | Owner at another's club → 403 |
| `test_create_event_past_date` | Past date → 400 |
| `test_create_event_player_forbidden` | Player tries to create → 403 |
| `test_register_for_event` | Valid registration → 201 |
| `test_register_duplicate` | Same user registers twice → 409 |
| `test_register_event_full` | Registration at capacity → 409 `EVENT_FULL` |
| `test_cancel_registration_success` | Cancel own registration → 200 |
| `test_cancel_registration_not_found` | No registration exists → 404 |

### 14.9 `test_payments.py`

| Test | Description |
|---|---|
| `test_get_my_payments` | Returns current user's payment history |
| `test_webhook_valid_signature` | Valid HMAC, `payment.captured` → updates status to `completed` |
| `test_webhook_invalid_signature` | Bad HMAC → 400 |
| `test_webhook_unknown_transaction` | Unknown `gateway_transaction_id` → logs and returns 200 (idempotent) |

### 14.10 `test_attendance.py`

| Test | Description |
|---|---|
| `test_check_in_success` | Front-desk records check-in → 201 |
| `test_check_in_already_checked_in` | Duplicate check-in → 409 |
| `test_check_in_invalid_booking` | Booking not found → 404 |
| `test_check_in_wrong_user` | Booking belongs to different user → 409 |
| `test_check_out_success` | Records check-out, returns duration → 200 |
| `test_check_out_already_done` | Re-checkout → 409 |
| `test_get_admin_attendance` | Owner views records for their club → 200 |
| `test_get_admin_attendance_wrong_owner` | Owner views another's club → 403 |
| `test_check_in_player_forbidden` | Player role tries to check in → 403 |

### 14.11 `test_notifications.py`

| Test | Description |
|---|---|
| `test_get_notifications` | Returns user's notifications with unread count |
| `test_get_notifications_unauthenticated` | No cookie → 401 |
| `test_mark_notification_read` | Sets `is_read = True` → 200 |
| `test_mark_notification_wrong_user` | Another user's notification → 403 |
| `test_mark_all_read` | All unread → all set to read |
| `test_notification_created_on_booking` | Creating a booking inserts a `Notification` row |
| `test_notification_created_on_override` | Override triggers notification to affected player |

---

## 15. OpenAPI Deviations Log

The table below tracks places where the implementation deviates from the original `api-docs/openapi.yaml`. Each deviation must be reflected back in the YAML before the relevant PR is merged.

| # | Endpoint | Deviation | Status |
|---|---|---|---|
| 1 | `POST /auth/login` | OpenAPI specifies `Authorization: Bearer` header; implementation uses HttpOnly cookie. Cookie approach is more secure for browser clients. OpenAPI spec must add `Cookie` security scheme. | ⏳ Pending |
| 2 | `POST /auth/register` | OpenAPI allows only `player` and `owner` roles. Implementation also supports `front-desk`. Spec must be updated to include this. | ⏳ Pending |
| 3 | `PATCH /bookings/{bookingId}/release` | OpenAPI lists this as `PATCH`. Response should include the updated booking object, not just a message. Spec can be extended. | ⏳ Pending |
| 4 | New endpoints | `GET /auth/me`, `POST /auth/logout`, `GET /bookings/my`, `GET /clubs/{clubId}/courts`, all membership/event/payment/attendance/notification routes — **not yet in `openapi.yaml`**. Must be added. | ⏳ Pending |
| 5 | `Club` schema | OpenAPI `Club` schema lacks flat `open_time`, `close_time`, `slot_duration_minutes` columns. Spec shows `OperatingHours` as a nested object — implementation will serialise it this way too (no schema change needed, but DB stores flat). | ✅ Aligned |
