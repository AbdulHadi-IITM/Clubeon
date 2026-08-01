# API Endpoints cURL Cheatsheet

Since the application uses `flask-jwt-extended` with `set_access_cookies` (HttpOnly cookies), make sure to save the cookies during login (`-c cookies.txt`) and pass them to all subsequent authenticated requests (`-b cookies.txt`).

---

## 1. Auth

### Register
```bash
curl -X POST http://127.0.0.1:5000/api/v1/auth/register \
-H "Content-Type: application/json" \
-d '{"name": "Test Owner", "email": "owner@example.com", "password": "password123", "role": "owner"}'
```

### Login
```bash
curl -c cookies.txt -X POST http://127.0.0.1:5000/api/v1/auth/login \
-H "Content-Type: application/json" \
-d '{"email": "owner@example.com", "password": "password123"}'
```

### Get Current User (Me)
```bash
curl -b cookies.txt -X GET http://127.0.0.1:5000/api/v1/auth/me
```

---

## 2. Clubs

### Get All Clubs
```bash
curl -X GET http://127.0.0.1:5000/api/v1/clubs
```

### Create Club (Owner Role required)
```bash
curl -b cookies.txt -X POST http://127.0.0.1:5000/api/v1/clubs \
-H "Content-Type: application/json" \
-d '{"name": "My Tennis Club", "address": "123 Court St", "open_time": "06:00", "close_time": "22:00", "slot_duration_minutes": 60}'
```

### Add Court to Club (Owner Role required)
```bash
curl -b cookies.txt -X POST http://127.0.0.1:5000/api/v1/clubs/1/courts \
-H "Content-Type: application/json" \
-d '{"name": "Court 1", "is_active": true}'
```

### Get Availability Matrix
```bash
curl -X GET 'http://127.0.0.1:5000/api/v1/availability/matrix?club_id=1&date=2026-07-20'
```

---

## 3. Bookings

### Create Booking
```bash
curl -b cookies.txt -X POST http://127.0.0.1:5000/api/v1/bookings \
-H "Content-Type: application/json" \
-d '{"court_id": 1, "booking_date": "2026-07-20", "start_time": "10:00", "end_time": "11:00"}'
```

### Get My Bookings
```bash
curl -b cookies.txt -X GET http://127.0.0.1:5000/api/v1/bookings
```

### Release Booking
```bash
curl -b cookies.txt -X POST http://127.0.0.1:5000/api/v1/bookings/1/release
```

---

## 4. Admin Actions

### Override Booking
```bash
curl -b cookies.txt -X POST http://127.0.0.1:5000/api/v1/admin/overrides \
-H "Content-Type: application/json" \
-d '{"booking_id": 1, "reason": "Emergency maintenance needed"}'
```

### Block Court
```bash
curl -b cookies.txt -X POST http://127.0.0.1:5000/api/v1/admin/blocks \
-H "Content-Type: application/json" \
-d '{"court_id": 1, "start_date": "2026-08-01", "end_date": "2026-08-05", "title": "Tournament"}'
```

---

## 5. Memberships

### Get Plans
```bash
curl -X GET http://127.0.0.1:5000/api/v1/memberships/plans
```

### Subscribe to Plan
```bash
curl -b cookies.txt -X POST http://127.0.0.1:5000/api/v1/memberships/subscribe \
-H "Content-Type: application/json" \
-d '{"plan_id": 1}'
```

### Get My Memberships
```bash
curl -b cookies.txt -X GET http://127.0.0.1:5000/api/v1/memberships/my-memberships
```

### Cancel Membership
```bash
curl -b cookies.txt -X POST http://127.0.0.1:5000/api/v1/memberships/1/cancel
```

---

## 6. Events

### Get Events
```bash
curl -X GET 'http://127.0.0.1:5000/api/v1/events?club_id=1'
```

### Create Event
```bash
curl -b cookies.txt -X POST http://127.0.0.1:5000/api/v1/events \
-H "Content-Type: application/json" \
-d '{"club_id": 1, "title": "Summer Cup", "description": "Annual tennis cup", "event_date": "2026-09-01", "start_time": "10:00", "end_time": "14:00", "max_attendees": 30, "registration_fee": 100.0}'
```

### Register for Event
```bash
curl -b cookies.txt -X POST http://127.0.0.1:5000/api/v1/events/1/register
```

### Cancel Registration
```bash
curl -b cookies.txt -X POST http://127.0.0.1:5000/api/v1/events/1/cancel
```

---

## 7. Payments

### Get My Payments
```bash
curl -b cookies.txt -X GET http://127.0.0.1:5000/api/v1/payments/my-payments
```

### Webhook
```bash
curl -X POST http://127.0.0.1:5000/api/v1/payments/webhook \
-H "Content-Type: application/json" \
-d '{"transaction_id": "txn_12345", "status": "completed", "reference_id": 1, "payment_type": "event"}'
```

---

## 8. Attendance

### Check-in (Booking)
```bash
curl -b cookies.txt -X POST http://127.0.0.1:5000/api/v1/attendance/check-in \
-H "Content-Type: application/json" \
-d '{"booking_id": 1}'
```

### Check-out
```bash
curl -b cookies.txt -X POST http://127.0.0.1:5000/api/v1/attendance/check-out \
-H "Content-Type: application/json" \
-d '{"attendance_id": 1}'
```

### View Attendance (Admin)
```bash
curl -b cookies.txt -X GET 'http://127.0.0.1:5000/api/v1/attendance/admin/view?club_id=1'
```

---

## 9. Notifications

### Get My Notifications
```bash
curl -b cookies.txt -X GET http://127.0.0.1:5000/api/v1/notifications
```

### Mark Notification as Read
```bash
curl -b cookies.txt -X POST http://127.0.0.1:5000/api/v1/notifications/1/read
```

### Mark All Notifications as Read
```bash
curl -b cookies.txt -X POST http://127.0.0.1:5000/api/v1/notifications/read-all
```
