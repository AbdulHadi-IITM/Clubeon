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
- [ ] Implement Auth Module (`register`, `login`, `logout`, `me`)
- [ ] Implement Clubs Module (`get clubs`, `get courts`)
- [ ] Implement Availability Module (`get availability matrix`)
- [ ] Implement Bookings Module (`create`, `get my bookings`, `release`)
- [ ] Implement Admin Actions Module (`override`, `block court`)
- [ ] Implement Memberships Module (`plans`, `subscribe`, `my memberships`, `cancel`)
- [ ] Implement Events Module (`list`, `create`, `register`, `cancel`)
- [ ] Implement Payments Module (`my payments`, `webhook`)
- [ ] Implement Attendance Module (`check-in`, `check-out`, `admin view`)
- [ ] Implement Notifications Module (`get`, `read`, `read-all`)

## Application Configuration
- [ ] Update `app/__init__.py` to register all module blueprints
- [ ] Resolve cross-module dependencies using Services

## Testing (`pytest`)
- [ ] Setup `conftest.py` (fixtures for app, db, auth_headers, mock data)
- [ ] Write tests for Auth
- [ ] Write tests for Clubs
- [ ] Write tests for Availability
- [ ] Write tests for Bookings
- [ ] Write tests for Admin Actions
- [ ] Write tests for Memberships
- [ ] Write tests for Events
- [ ] Write tests for Payments
- [ ] Write tests for Attendance
- [ ] Write tests for Notifications

## Documentation
- [ ] Update `api-docs/openapi.yaml` with logged deviations
