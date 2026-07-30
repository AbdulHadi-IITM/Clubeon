# Backend Implementation Checklist

## Project Setup & Data Layer
- [x] Create project structure (domain modules)
- [x] Define `User` model (Auth)
- [x] Define `Club` and `Court` models (Clubs)
- [x] Define `Booking` and `CourtBlock` models (Bookings)
- [x] Define `MembershipPlan` and `Membership` models (Memberships)
- [x] Define `Event` and `EventRegistration` models (Events)
- [x] Define `Payment` model (Payments)
- [x] Define `AttendanceRecord` model (Attendance)
- [x] Define `Notification` model (Notifications)

## API Modules (Controllers & Services)
- [x] Implement Auth Module (`register`, `login`, `logout`, `me`)
- [x] Implement Clubs Module (`get clubs`, `get courts`)
- [x] Implement Availability Module (`get availability matrix`)
- [x] Implement Bookings Module (`create`, `get my bookings`, `release`)
- [x] Implement Admin Actions Module (`override`, `block court`)
- [x] Implement Memberships Module (`plans`, `subscribe`, `my memberships`, `cancel`)
- [x] Implement Events Module (`list`, `create`, `register`, `cancel`)
- [ ] Implement Payments Module (`my payments`, `webhook`)
- [ ] Implement Attendance Module (`check-in`, `check-out`, `admin view`)
- [ ] Implement Notifications Module (`get`, `read`, `read-all`)

## Application Configuration
- [ ] Update `app/__init__.py` to register all module blueprints
- [ ] Resolve cross-module dependencies using Services

## Testing (`pytest`)
- [x] Setup `conftest.py` (fixtures for app, db, auth_headers, mock data)
- [x] Write tests for Auth
- [x] Write tests for Clubs
- [x] Write tests for Availability
- [x] Write tests for Bookings
- [x] Write tests for Admin Actions
- [x] Write tests for Memberships
- [x] Write tests for Events
- [ ] Write tests for Payments
- [ ] Write tests for Attendance
- [ ] Write tests for Notifications

## Documentation
- [ ] Update `api-docs/openapi.yaml` with logged deviations
