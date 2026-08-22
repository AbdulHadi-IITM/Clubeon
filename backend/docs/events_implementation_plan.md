# End-to-End Implementation Plan for Events

**Objective:**
Complete the end-to-end implementation of the Events feature across Member, Staff, and Admin (Owner) portals. This includes finalizing API endpoints for event management, fetching single events, and recording attendance, as well as replacing static mock data in the frontend with real API integrations.

## 1. Backend Implementation (API & Services)

**A. Events Module (`backend/app/events/`)**
- **GET Single Event:** Create `GET /api/v1/events/<int:event_id>` to allow members/users to fetch the details of a specific event without retrieving the entire list.
- **Admin Event Listing:** Create or update an endpoint (e.g. `GET /api/v1/admin/events`) to support fetching *all* events for a club, including past and cancelled ones. Currently, `GET /api/v1/events` only returns `upcoming` events.
- **Update Event:** Add `PUT /api/v1/events/<int:event_id>` (protected by `@role_required('owner')`) to allow updating event details (title, description, time, fee, capacity).
- **Delete/Cancel Event:** Add `DELETE /api/v1/events/<int:event_id>` (protected by `@role_required('owner')`) to allow admins to cancel an event. Update the event status to `cancelled` and optionally refund/notify registered members.

**B. Staff Module (`backend/app/staff/`)**
- **Event Attendance Check-in:** Create `POST /api/v1/staff/events/attendance/check-in` which takes `event_id` and `user_id`. It will create an `AttendanceRecord` linking `event_id` and `user_id`.
- **Participant Check-in Status:** Update `StaffService.event_detail` to return the `check_in_at` timestamp for each registered participant by joining with `AttendanceRecord`.

## 2. Frontend Implementation (Vue.js)

**A. Admin Portal (`Frontend/src/views/AdminDashboardView.vue`)**
The Admin Dashboard currently relies on static mock data (`eventsList`) for its Events tab.
- **Fetch Real Events:** Implement `loadEvents()` to call the admin events endpoint and replace the static array.
- **Dynamic KPIs:** Compute `eventsKpis` dynamically using the fetched API data.
- **Create Event Integration:** Hook `handleCreateEvent()` to post form data to `POST /api/v1/events` instead of modifying the static array.
- **Edit/Delete Actions:** Add functional "Edit" and "Cancel" buttons on the event cards in the Admin view, triggering the respective `PUT` and `DELETE` endpoints and refreshing the list.

**B. Member Portal (`Frontend/src/views/member/EventDetails.vue`)**
- **Single Event Fetch:** Refactor `member/EventDetails.vue` to fetch the specific event via `api.get('/events/${eventId}')` rather than fetching all events and filtering locally.
- **My Registrations View:** Create a dedicated view or section for members to easily see events they have registered for (utilizing `/api/v1/events/my-registrations`).

**C. Staff Portal (`Frontend/src/views/staff/EventDetails.vue`)**
- **Participant Check-In UI:** Add a "Check-in" button next to each participant in the registered members table.
- **Check-In Integration:** Call the new `POST /api/v1/staff/events/attendance/check-in` when staff clicks the button, and update the UI to reflect the checked-in state.

## 3. Database & Migrations
- Since `AttendanceRecord` already contains `event_id`, no complex database migrations are required.
- Add `attendances = db.relationship('AttendanceRecord', backref='event', lazy=True)` in the `Event` model for easier querying.
