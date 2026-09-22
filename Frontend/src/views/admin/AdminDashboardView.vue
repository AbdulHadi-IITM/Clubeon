<template>
  <div class="space-y-6">
    <!-- Content Container -->
    <div class="content-container space-y-6">
      <!-- TAB 1: DASHBOARD (MAIN OVERVIEW) -->
      <!-- MODULAR ADMIN TABS -->
      <OverviewTab v-if="activeNav === 'Dashboard'" />
      <MembersTab v-else-if="activeNav === 'Members'" />
      <CourtsTab v-else-if="activeNav === 'Courts'" />
      <BookingsTab v-else-if="activeNav === 'Bookings'" />
      <EventsTab v-else-if="activeNav === 'Events'" />
      <AnnouncementsTab v-else-if="activeNav === 'Announcements'" />
      <AnalyticsTab v-else-if="activeNav === 'Analytics'" />
      <SettingsTab v-else-if="activeNav === 'Settings'" />
    </div>

      <!-- ALL ADMIN POPUP MODALS -->

          <!-- ADD COURT MODAL -->
          <div v-if="showAddCourtModal" class="modal-overlay" role="dialog" aria-modal="true">
            <div class="modal-card">
              <div class="modal-header">
                <h3>
                  {{
                    courtStore.courts.length === 0
                      ? 'Setup Your Club & First Court'
                      : 'Create New Court'
                  }}
                </h3>
                <button @click="closeAddCourtModal" class="close-btn">×</button>
              </div>
              <form @submit.prevent="handleCreateCourt" class="modal-form">
                <div class="form-row">
                  <div class="form-group">
                    <label>Court Name</label>
                    <input
                      type="text"
                      v-model="courtForm.court_name"
                      placeholder="e.g. Tennis Court 1"
                      required
                    />
                  </div>
                </div>

                <div class="form-row">
                  <div class="form-group">
                    <label>Sport / Court Type</label>
                    <select v-model="courtForm.sport_type" required>
                      <option v-for="sport in courtStore.sportsTypes" :key="sport.value" :value="sport.value">
                        {{ sport.icon }} {{ sport.label }}
                      </option>
                    </select>
                  </div>
                </div>

                <!-- Show Club setup fields only if this is the first court (courts array is empty) -->
                <div v-if="!courtStore.club" class="form-row">
                  <div class="form-group">
                    <label>Club Name</label>
                    <input
                      type="text"
                      v-model="courtForm.club_name"
                      placeholder="e.g. Apex Sports Arena"
                      required
                    />
                  </div>
                  <div class="form-group">
                    <label>Club Address</label>
                    <input
                      type="text"
                      v-model="courtForm.club_address"
                      placeholder="Full physical address"
                      required
                    />
                  </div>
                </div>

                <div class="modal-actions">
                  <button type="button" @click="closeAddCourtModal" class="cancel-modal-btn">
                    Cancel
                  </button>
                  <button type="submit" class="submit-modal-btn">Create Court</button>
                </div>
              </form>
            </div>
          </div>

          <!-- EDIT COURT MODAL -->
          <div v-if="showEditCourtModal" class="modal-overlay" role="dialog" aria-modal="true">
            <div class="modal-card">
              <div class="modal-header">
                <h3>Edit Court</h3>
                <button @click="closeEditCourtModal" class="close-btn">×</button>
              </div>
              <form @submit.prevent="handleUpdateCourt" class="modal-form">
                <div class="form-row">
                  <div class="form-group">
                    <label>Court Name</label>
                    <input type="text" v-model="courtForm.court_name" required />
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label>Sport / Court Type</label>
                    <select v-model="courtForm.sport_type" required>
                      <option v-for="sport in courtStore.sportsTypes" :key="sport.value" :value="sport.value">
                        {{ sport.icon }} {{ sport.label }}
                      </option>
                    </select>
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label>Status</label>
                    <select v-model="courtForm.is_active">
                      <option :value="true">Active</option>
                      <option :value="false">Inactive</option>
                    </select>
                  </div>
                </div>

                <!-- Toggle: Use Defaults or Custom -->
                <div class="toggle-section">
                  <label class="toggle-label">Operating Hours & Slot Duration</label>
                  <div class="toggle-group">
                    <button
                      type="button"
                      class="toggle-btn"
                      :class="{ active: courtForm.use_defaults }"
                      @click="courtForm.use_defaults = true"
                    >
                      Use Club Defaults
                    </button>
                    <button
                      type="button"
                      class="toggle-btn"
                      :class="{ active: !courtForm.use_defaults }"
                      @click="courtForm.use_defaults = false"
                    >
                      Custom Settings
                    </button>
                  </div>
                </div>

                <!-- Override inputs – enabled only when custom is selected -->
                <div class="form-row" :class="{ 'disabled-section': courtForm.use_defaults }">
                  <div class="form-group">
                    <label>Open Time</label>
                    <input
                      type="time"
                      v-model="courtForm.open_time_override"
                      :disabled="courtForm.use_defaults"
                    />
                  </div>
                  <div class="form-group">
                    <label>Close Time</label>
                    <input
                      type="time"
                      v-model="courtForm.close_time_override"
                      :disabled="courtForm.use_defaults"
                    />
                  </div>
                </div>
                <div class="form-row" :class="{ 'disabled-section': courtForm.use_defaults }">
                  <div class="form-group">
                    <label>Slot Duration (minutes)</label>
                    <input
                      type="number"
                      v-model="courtForm.slot_duration_override"
                      :disabled="courtForm.use_defaults"
                      min="15"
                      step="15"
                      placeholder="e.g. 60"
                    />
                  </div>
                </div>

                <div class="modal-actions">
                  <button type="button" @click="closeEditCourtModal" class="cancel-modal-btn">
                    Cancel
                  </button>
                  <button type="submit" class="submit-modal-btn">Save Changes</button>
                </div>
              </form>
            </div>
          </div>

        <!-- BOOKING DETAILS MODAL -->
        <div v-if="showBookingDetailsModal && selectedBooking" class="modal-overlay" @click.self="closeBookingDetailsModal">
          <div class="modal-card booking-detail-modal">
            <div class="modal-header">
              <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
                <h2 style="margin: 0;">Booking Details</h2>
                <span class="booking-ref-tag large">{{ selectedBooking.id }}</span>
                <span class="booking-status-badge" :class="'bstatus-' + selectedBooking.status.toLowerCase()">
                  {{ selectedBooking.status }}
                </span>
              </div>
              <button class="close-modal-btn" @click="closeBookingDetailsModal">✕</button>
            </div>

            <div class="modal-body booking-detail-body">
              <!-- Player Profile Section -->
              <div class="detail-section-card">
                <h4>Player Information</h4>
                <div class="detail-grid">
                  <div class="detail-item">
                    <span class="detail-label">Player Name</span>
                    <span class="detail-val font-bold">{{ selectedBooking.player }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Email Address</span>
                    <span class="detail-val">{{ selectedBooking.email }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Phone</span>
                    <span class="detail-val">{{ selectedBooking.phone }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">User Tier</span>
                    <span class="detail-val">{{ selectedBooking.userType }}</span>
                  </div>
                </div>
              </div>

              <!-- Reservation Details Section -->
              <div class="detail-section-card">
                <h4>Reservation & Schedule</h4>
                <div class="detail-grid">
                  <div class="detail-item">
                    <span class="detail-label">Facility / Court</span>
                    <span class="detail-val font-bold">{{ selectedBooking.facility }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Sport Category</span>
                    <span class="detail-val">{{ selectedBooking.sport }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Scheduled Date</span>
                    <span class="detail-val">{{ selectedBooking.dateDisplay }} ({{ selectedBooking.date }})</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Time Slot</span>
                    <span class="detail-val">{{ selectedBooking.time }} ({{ selectedBooking.duration }})</span>
                  </div>
                </div>
              </div>

              <!-- Payment & Fee Section -->
              <div class="detail-section-card">
                <h4>Payment & Billing</h4>
                <div class="detail-grid">
                  <div class="detail-item">
                    <span class="detail-label">Booking Fee</span>
                    <span class="detail-val font-bold" style="color: #2563eb; font-size: 1.1rem;">₹{{ selectedBooking.amount }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Payment Status</span>
                    <span class="pay-status-tag" :class="'pay-' + selectedBooking.paymentStatus.toLowerCase()">{{ selectedBooking.paymentStatus }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Payment Method</span>
                    <span class="detail-val">{{ selectedBooking.paymentMethod }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Created At</span>
                    <span class="detail-val">{{ selectedBooking.createdAt }}</span>
                  </div>
                </div>
              </div>

              <!-- Notes Section -->
              <div v-if="selectedBooking.notes" class="detail-section-card">
                <h4>Notes & Comments</h4>
                <p class="notes-text">{{ selectedBooking.notes }}</p>
              </div>
            </div>

            <div class="modal-footer">
              <div style="display: flex; gap: 0.75rem;">
                <button
                  v-if="selectedBooking.status === 'Confirmed' || selectedBooking.status === 'Pending'"
                  class="cancel-modal-btn danger-btn"
                  @click="requestCancelBooking(selectedBooking)"
                >
                  ✕ Cancel Booking
                </button>
                <button
                  v-if="selectedBooking.status === 'Confirmed'"
                  class="submit-modal-btn success-btn"
                  @click="markBookingCompleted(selectedBooking)"
                >
                  ✓ Mark Completed
                </button>
              </div>
              <button class="cancel-modal-btn" @click="closeBookingDetailsModal">Close</button>
            </div>
          </div>
        </div>

        <!-- CANCEL BOOKING CONFIRMATION MODAL -->
        <div v-if="showCancelConfirmModal && bookingToCancel" class="modal-overlay" @click.self="showCancelConfirmModal = false">
          <div class="modal-card small-confirm-modal">
            <div class="modal-header">
              <h3 style="color: #ef4444; margin: 0;">Cancel Booking</h3>
              <button class="close-modal-btn" @click="showCancelConfirmModal = false">✕</button>
            </div>
            <div class="modal-body" style="padding: 1.5rem 0;">
              <p>Are you sure you want to cancel booking <strong>{{ bookingToCancel.id }}</strong> for <strong>{{ bookingToCancel.player }}</strong>?</p>
              <p style="font-size: 0.85rem; color: #64748b; margin-top: 0.5rem;">This action will change the status to Cancelled and initiate a refund for ₹{{ bookingToCancel.amount }}.</p>
            </div>
            <div class="modal-footer">
              <button class="cancel-modal-btn" @click="showCancelConfirmModal = false">Keep Booking</button>
              <button class="submit-modal-btn danger-btn" @click="confirmCancelBooking">Confirm Cancellation</button>
            </div>
          </div>
        </div>

        <!-- CREATE NEW BOOKING MODAL -->
        <div v-if="showNewBookingModal" class="modal-overlay" @click.self="closeNewBookingModal">
          <div class="modal-card">
            <div class="modal-header">
              <h2>Add New Court Reservation</h2>
              <button class="close-modal-btn" @click="closeNewBookingModal">✕</button>
            </div>
            <form @submit.prevent="handleCreateNewBooking" class="modal-form">
              <div class="form-row">
                <div class="form-group">
                  <label>Player Name *</label>
                  <input type="text" v-model="newBookingForm.player" required placeholder="e.g. Alex Smith" />
                </div>
                <div class="form-group">
                  <label>Player Email *</label>
                  <input type="email" v-model="newBookingForm.email" required placeholder="alex@example.com" />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Phone Number</label>
                  <input type="text" v-model="newBookingForm.phone" placeholder="+1 (555) 000-0000" />
                </div>
                <div class="form-group">
                  <label>User Type</label>
                  <select v-model="newBookingForm.userType">
                    <option value="Member (VIP)">Member (VIP)</option>
                    <option value="Member (Standard)">Member (Standard)</option>
                    <option value="Casual Player">Casual Player</option>
                    <option value="Guest">Guest</option>
                  </select>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Facility / Court *</label>
                  <select v-model="newBookingForm.facility" @change="newBookingForm.sport = newBookingForm.facility.includes('Tennis') ? 'Tennis' : newBookingForm.facility.includes('Badminton') ? 'Badminton' : newBookingForm.facility.includes('Squash') ? 'Squash' : 'Swimming'">
                    <option value="Tennis Court 1">Tennis Court 1</option>
                    <option value="Tennis Court 2">Tennis Court 2</option>
                    <option value="Badminton Arena A">Badminton Arena A</option>
                    <option value="Badminton Arena B">Badminton Arena B</option>
                    <option value="Squash Court 1">Squash Court 1</option>
                    <option value="Squash Court 2">Squash Court 2</option>
                    <option value="Swimming Lane 1">Swimming Lane 1</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Date *</label>
                  <input type="date" v-model="newBookingForm.date" required />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Time Slot *</label>
                  <input type="text" v-model="newBookingForm.time" required placeholder="e.g. 05:00 PM - 07:00 PM" />
                </div>
                <div class="form-group">
                  <label>Duration</label>
                  <input type="text" v-model="newBookingForm.duration" placeholder="e.g. 2.0 hrs" />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Booking Fee (₹)</label>
                  <input type="number" v-model="newBookingForm.amount" min="0" step="5" />
                </div>
                <div class="form-group">
                  <label>Payment Status</label>
                  <select v-model="newBookingForm.paymentStatus">
                    <option value="Paid">Paid</option>
                    <option value="Pending">Pending</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label>Notes / Special Requests</label>
                <textarea v-model="newBookingForm.notes" rows="2" placeholder="Add any special instructions or equipment requests..."></textarea>
              </div>

              <div class="modal-actions">
                <button type="button" class="cancel-modal-btn" @click="closeNewBookingModal">Cancel</button>
                <button type="submit" class="submit-modal-btn">Create Reservation</button>
              </div>
            </form>
          </div>
        </div>

        <!-- CREATE EVENT MODAL -->
        <div v-if="showCreateEventModal" class="modal-overlay" @click.self="closeCreateEventModal">
          <div class="modal-card">
            <div class="modal-header">
              <h3>+ Create New Event</h3>
              <button class="close-modal-btn" @click="closeCreateEventModal">✕</button>
            </div>
            <form @submit.prevent="handleCreateEvent" class="modal-form">
              <div class="form-group">
                <label>Event Title *</label>
                <input type="text" v-model="eventForm.title" required placeholder="e.g. Apex Summer Tennis Open 2026" />
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Sport Category *</label>
                  <select v-model="eventForm.sport" required>
                    <option value="Tennis">Tennis</option>
                    <option value="Badminton">Badminton</option>
                    <option value="Squash">Squash</option>
                    <option value="Swimming">Swimming</option>
                    <option value="Social">Social / General</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Event Type *</label>
                  <select v-model="eventForm.type" required>
                    <option value="Tournament">Tournament</option>
                    <option value="Coaching Clinic">Coaching Clinic</option>
                    <option value="Social League">Social League</option>
                    <option value="Exhibition">Exhibition / Match</option>
                  </select>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Event Date *</label>
                  <input type="date" v-model="eventForm.date" required />
                </div>
                <div class="form-group">
                  <label>Time Slot *</label>
                  <input type="text" v-model="eventForm.time" required placeholder="e.g. 10:00 AM - 04:00 PM" />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Venue / Court Location *</label>
                  <input type="text" v-model="eventForm.venue" required placeholder="e.g. Tennis Courts 1 & 2" />
                </div>
                <div class="form-group">
                  <label>Max Player Capacity *</label>
                  <input type="number" v-model="eventForm.capacity" min="1" required />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Entry Fee (₹)</label>
                  <input type="number" v-model="eventForm.fee" min="0" step="50" placeholder="0 for Free" />
                </div>
                <div class="form-group">
                  <label>Event Status</label>
                  <select v-model="eventForm.status">
                    <option value="Upcoming">Upcoming</option>
                    <option value="Ongoing">Ongoing</option>
                    <option value="Completed">Completed</option>
                    <option value="Cancelled">Cancelled</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label>Organizer Name</label>
                <input type="text" v-model="eventForm.organizer" placeholder="e.g. Head Coach David" />
              </div>

              <div class="form-group">
                <label>Description & Rules</label>
                <textarea v-model="eventForm.description" rows="3" placeholder="Describe event details, prizes, eligibility, or equipment guidelines..."></textarea>
              </div>

              <div class="modal-actions">
                <button type="button" class="cancel-modal-btn" @click="closeCreateEventModal">Cancel</button>
                <button type="submit" class="submit-modal-btn">Publish Event</button>
              </div>
            </form>
          </div>
        </div>

        <!-- EDIT EVENT MODAL -->
        <div v-if="showEditEventModal && editingEvent" class="modal-overlay" @click.self="closeEditEventModal">
          <div class="modal-card">
            <div class="modal-header">
              <h3>✎ Edit Event: {{ editingEvent.title }}</h3>
              <button class="close-modal-btn" @click="closeEditEventModal">✕</button>
            </div>
            <form @submit.prevent="handleUpdateEvent" class="modal-form">
              <div class="form-group">
                <label>Event Title *</label>
                <input type="text" v-model="editEventForm.title" required />
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Sport Category</label>
                  <select v-model="editEventForm.sport">
                    <option value="Tennis">Tennis</option>
                    <option value="Badminton">Badminton</option>
                    <option value="Squash">Squash</option>
                    <option value="Swimming">Swimming</option>
                    <option value="Social">Social</option>
                  </select>
                </div>
                <div class="form-group">
                  <label>Event Type</label>
                  <select v-model="editEventForm.type">
                    <option value="Tournament">Tournament</option>
                    <option value="Coaching Clinic">Coaching Clinic</option>
                    <option value="Social League">Social League</option>
                  </select>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Event Date</label>
                  <input type="date" v-model="editEventForm.date" />
                </div>
                <div class="form-group">
                  <label>Time Slot</label>
                  <input type="text" v-model="editEventForm.time" />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Venue / Location</label>
                  <input type="text" v-model="editEventForm.venue" />
                </div>
                <div class="form-group">
                  <label>Capacity</label>
                  <input type="number" v-model="editEventForm.capacity" min="1" />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>Entry Fee (₹)</label>
                  <input type="number" v-model="editEventForm.fee" min="0" />
                </div>
                <div class="form-group">
                  <label>Event Status</label>
                  <select v-model="editEventForm.status">
                    <option value="Upcoming">Upcoming</option>
                    <option value="Ongoing">Ongoing</option>
                    <option value="Completed">Completed</option>
                    <option value="Cancelled">Cancelled</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label>Description</label>
                <textarea v-model="editEventForm.description" rows="3"></textarea>
              </div>

              <div class="modal-actions">
                <button type="button" class="cancel-modal-btn" @click="closeEditEventModal">Cancel</button>
                <button type="submit" class="submit-modal-btn">Save Changes</button>
              </div>
            </form>
          </div>
        </div>

        <!-- VIEW EVENT DETAILS & PARTICIPANTS MODAL -->
        <div v-if="showEventDetailsModal && selectedEvent" class="modal-overlay" @click.self="closeEventDetailsModal">
          <div class="modal-card booking-detail-modal">
            <div class="modal-header">
              <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
                <h2 style="margin: 0;">{{ selectedEvent.title }}</h2>
                <span class="sport-badge-pill" :class="'sport-' + selectedEvent.sport.toLowerCase()">{{ selectedEvent.sport }}</span>
                <span class="booking-status-badge" :class="'estatus-' + selectedEvent.status.toLowerCase()">{{ selectedEvent.status }}</span>
              </div>
              <button class="close-modal-btn" @click="closeEventDetailsModal">✕</button>
            </div>

            <div class="modal-body booking-detail-body">
              <div class="detail-section-card">
                <h4>Event Overview</h4>
                <div class="detail-grid">
                  <div class="detail-item">
                    <span class="detail-label">Event Category</span>
                    <span class="detail-val font-semibold">{{ selectedEvent.type }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Scheduled Date</span>
                    <span class="detail-val font-semibold">{{ selectedEvent.dateDisplay }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Time & Slot</span>
                    <span class="detail-val">{{ selectedEvent.time }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Venue Location</span>
                    <span class="detail-val">{{ selectedEvent.venue }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Organizer / Host</span>
                    <span class="detail-val">{{ selectedEvent.organizer }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Entry Fee</span>
                    <span class="detail-val font-bold" style="color: #2563eb;">{{ selectedEvent.fee > 0 ? '₹' + selectedEvent.fee : 'Free Entry' }}</span>
                  </div>
                </div>
              </div>

              <div class="detail-section-card">
                <h4>Event Description</h4>
                <p class="notes-text">{{ selectedEvent.description }}</p>
              </div>

              <div class="detail-section-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                  <h4 style="margin: 0; border: none; padding: 0;">Registered Participants ({{ selectedEvent.registered }} / {{ selectedEvent.capacity }})</h4>
                  <button class="export-csv-btn" style="padding: 0.35rem 0.75rem; font-size: 0.78rem;" @click="addSampleParticipant(selectedEvent)">+ Register Player</button>
                </div>

                <div v-if="!selectedEvent.participants || selectedEvent.participants.length === 0" style="color: #64748b; font-size: 0.85rem; font-style: italic;">
                  No players registered yet.
                </div>
                <div v-else class="participants-tags-list">
                  <div v-for="(p, idx) in selectedEvent.participants" :key="idx" class="participant-pill-item">
                    <span>👤 {{ p }}</span>
                    <button class="remove-participant-btn" @click="removeParticipant(selectedEvent, idx)" title="Remove">×</button>
                  </div>
                </div>
              </div>
            </div>

            <div class="modal-footer">
              <div style="display: flex; gap: 0.75rem;">
                <button class="action-icon-btn complete-btn" @click="openEditEventModal(selectedEvent)">✎ Edit Event</button>
                <button class="action-icon-btn cancel-btn" @click="requestDeleteEvent(selectedEvent)" style="display: inline-flex; align-items: center; gap: 0.4rem;">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" style="width: 14px; height: 14px;">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  <span>Delete Event</span>
                </button>
              </div>
              <button class="cancel-modal-btn" @click="closeEventDetailsModal">Close</button>
            </div>
          </div>
        </div>

        <!-- DELETE EVENT CONFIRMATION MODAL -->
        <div v-if="showDeleteEventModal && eventToDelete" class="modal-overlay" @click.self="showDeleteEventModal = false">
          <div class="modal-card small-confirm-modal" style="max-width: 460px; width: 92vw; padding: 1.5rem; border-radius: 1.25rem; box-shadow: 0 20px 45px rgba(15, 23, 42, 0.22); overflow: hidden;">
            <div class="modal-header" style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #f1f5f9; padding-bottom: 0.85rem;">
              <div style="display: flex; align-items: center; gap: 0.55rem;">
                <div style="width: 32px; height: 32px; border-radius: 8px; background: #fee2e2; color: #ef4444; display: grid; place-items: center; font-size: 1rem;">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" style="width: 16px; height: 16px;">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </div>
                <h3 style="color: #0f172a; margin: 0; font-size: 1.1rem; font-weight: 800;">Cancel & Delete Event</h3>
              </div>
              <button class="close-modal-btn" @click="showDeleteEventModal = false">✕</button>
            </div>
            <div class="modal-body" style="padding: 1.25rem 0; overflow-wrap: break-word; word-break: break-word; white-space: normal;">
              <p style="font-size: 0.95rem; color: #334155; line-height: 1.5; margin: 0;">
                Are you sure you want to delete event <strong style="color: #0f172a;">"{{ eventToDelete.title }}"</strong>?
              </p>
              <div style="margin-top: 0.85rem; padding: 0.75rem 0.95rem; background: #fef2f2; border: 1px solid #fecaca; border-radius: 0.75rem; color: #b91c1c; font-size: 0.82rem; line-height: 1.5; overflow-wrap: break-word; word-break: break-word;">
                📢 This action will cancel the event and automatically broadcast an announcement notice to all {{ eventToDelete.registered || 0 }} registered attendees.
              </div>
            </div>
            <div class="modal-footer" style="display: flex; justify-content: flex-end; gap: 0.75rem; border-top: 1px solid #f1f5f9; padding-top: 0.85rem; margin-top: 0.25rem;">
              <button class="cancel-modal-btn" @click="showDeleteEventModal = false">Keep Event</button>
              <button class="submit-modal-btn danger-btn" @click="confirmDeleteEvent" style="background: linear-gradient(135deg, #ef4444, #dc2626); color: #ffffff; padding: 0.55rem 1.2rem; border-radius: 0.6rem; font-weight: 700; border: none; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25);">Confirm Delete</button>
            </div>
          </div>
        </div>

        <!-- MEMBER DETAILS MODAL -->
        <div v-if="showMemberModal && selectedMemberForModal" class="modal-overlay" @click.self="showMemberModal = false">
          <div class="modal-card">
            <div class="modal-header">
              <h3>Member Profile Details</h3>
              <button class="close-modal-btn" @click="showMemberModal = false">✕</button>
            </div>
            <div class="modal-body" style="padding: 1.25rem 1.5rem;">
              <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.25rem; background: #f8fafc; padding: 1rem; border-radius: 0.75rem; border: 1px solid #e2e8f0;">
                <div class="user-avatar-sm" style="width: 48px; height: 48px; font-size: 1.1rem; background: linear-gradient(135deg, #2563eb, #4f46e5); color: #fff; font-weight: 700; display: grid; place-items: center; border-radius: 999px;">
                  {{ selectedMemberForModal.initials }}
                </div>
                <div>
                  <h4 style="font-size: 1.1rem; font-weight: 700; color: #0f172a; margin: 0;">{{ selectedMemberForModal.name }}</h4>
                  <span style="font-size: 0.85rem; color: #64748b;">{{ selectedMemberForModal.email }}</span>
                </div>
              </div>

              <div class="setting-row">
                <span class="setting-label">Membership Plan</span>
                <span style="font-weight: 700; color: #2563eb;">{{ selectedMemberForModal.plan }}</span>
              </div>
              <div class="setting-row">
                <span class="setting-label">Date Joined</span>
                <span class="setting-val">{{ selectedMemberForModal.dateJoined }}</span>
              </div>
              <div class="setting-row">
                <span class="setting-label">Total Facility Bookings</span>
                <span class="setting-val">{{ selectedMemberForModal.totalBookings }} bookings</span>
              </div>
              <div class="setting-row">
                <span class="setting-label">Contact Phone</span>
                <span class="setting-val">{{ selectedMemberForModal.phone }}</span>
              </div>
              <div class="setting-row">
                <span class="setting-label">Account Status</span>
                <span class="status-badge-chip status-active">Active & Verified</span>
              </div>
            </div>
            <div class="modal-footer">
              <button class="cancel-modal-btn" @click="showMemberModal = false">Close</button>
            </div>
          </div>
        </div>

        <!-- CREATE ANNOUNCEMENT MODAL -->
        <div v-if="showCreateAnnouncementModal" class="modal-overlay" @click.self="closeCreateAnnouncementModal">
          <div class="modal-card" style="max-width: 640px; width: 95vw; max-height: 90vh; overflow-y: auto;">
            <!-- Modern Header -->
            <div class="modal-header" style="background: linear-gradient(135deg, #1e293b, #0f172a); color: #ffffff; border-radius: 1rem 1rem 0 0; padding: 1.25rem 1.5rem;">
              <div style="display: flex; align-items: center; gap: 0.85rem;">
                <div style="width: 42px; height: 42px; border-radius: 12px; background: linear-gradient(135deg, #3b82f6, #6366f1); display: grid; place-items: center; font-size: 1.35rem; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);">
                  📢
                </div>
                <div>
                  <h3 style="margin: 0; font-size: 1.2rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;">Broadcast New Announcement</h3>
                  <span style="font-size: 0.82rem; color: #94a3b8;">Publish facility updates, tournament alerts, and court maintenance notices</span>
                </div>
              </div>
              <button class="close-modal-btn" @click="closeCreateAnnouncementModal" style="color: #94a3b8; background: rgba(255,255,255,0.08); border-radius: 999px; width: 32px; height: 32px; display: grid; place-items: center; border: none; font-size: 1rem;">✕</button>
            </div>

            <!-- Quick Template Bar -->
            <div style="background: #f8fafc; border-bottom: 1px solid #e2e8f0; padding: 0.75rem 1.5rem; display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
              <span style="font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em;">Quick Starters:</span>
              <button type="button" class="quick-template-btn" @click="applyAnnouncementTemplate('maintenance')">
                🛠️ Maintenance
              </button>
              <button type="button" class="quick-template-btn" @click="applyAnnouncementTemplate('tournament')">
                🏆 Tournament
              </button>
              <button type="button" class="quick-template-btn" @click="applyAnnouncementTemplate('policy')">
                📜 Policy
              </button>
              <button type="button" class="quick-template-btn" @click="applyAnnouncementTemplate('broadcast')">
                📣 Hours Flash
              </button>
            </div>

            <div class="modal-body" style="padding: 1.5rem;">
              <!-- Title Input -->
              <div class="form-group" style="margin-bottom: 1.25rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                  <label class="form-label font-bold" style="font-size: 0.85rem; color: #1e293b; margin: 0;">
                    Announcement Title / Headline <span style="color: #ef4444;">*</span>
                  </label>
                  <span style="font-size: 0.75rem; color: #94a3b8;">{{ announcementForm.title.length }}/100</span>
                </div>
                <input
                  v-model="announcementForm.title"
                  type="text"
                  maxlength="100"
                  class="form-control broadcast-input"
                  placeholder="e.g., Scheduled Synthetic Court Resurfacing & Lighting Upgrade"
                  required
                />
              </div>

              <!-- Category Selector Cards -->
              <div class="form-group" style="margin-bottom: 1.25rem;">
                <label class="form-label font-bold" style="display: block; font-size: 0.85rem; color: #1e293b; margin-bottom: 0.5rem;">
                  Category
                </label>
                <div class="category-selector-grid">
                  <button
                    v-for="cat in [
                      { name: 'General', icon: '📢', color: 'blue' },
                      { name: 'Broadcast', icon: '📣', color: 'purple' },
                      { name: 'Tournament', icon: '🏆', color: 'emerald' },
                      { name: 'Policy', icon: '📜', color: 'orange' },
                      { name: 'Maintenance', icon: '🛠️', color: 'rose' }
                    ]"
                    :key="cat.name"
                    type="button"
                    class="category-card-btn"
                    :class="[{ active: announcementForm.category === cat.name }, 'cat-' + cat.color]"
                    @click="announcementForm.category = cat.name"
                    style="justify-content: center; padding: 0.65rem 0.5rem;"
                  >
                    <span class="cat-icon">{{ cat.icon }}</span>
                    <span class="cat-name">{{ cat.name }}</span>
                  </button>
                </div>
              </div>

              <!-- Message / Body Textarea -->
              <div class="form-group">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                  <label class="form-label font-bold" style="font-size: 0.85rem; color: #1e293b; margin: 0;">
                    Announcement Message Content <span style="color: #ef4444;">*</span>
                  </label>
                  <span style="font-size: 0.75rem; color: #94a3b8;">{{ announcementForm.body.length }}/500</span>
                </div>
                <textarea
                  v-model="announcementForm.body"
                  rows="5"
                  maxlength="500"
                  class="form-control broadcast-textarea"
                  placeholder="Provide comprehensive details, operational timings, affected courts, or rules..."
                  required
                ></textarea>
              </div>
            </div>

            <!-- Modal Footer -->
            <div class="modal-footer" style="display: flex; justify-content: flex-end; align-items: center; gap: 0.85rem; padding: 1.25rem 1.5rem; background: #f8fafc; border-top: 1px solid #e2e8f0; border-radius: 0 0 1rem 1rem;">
              <button type="button" class="cancel-modal-btn" @click="closeCreateAnnouncementModal">Cancel</button>
              <button
                type="button"
                class="submit-modal-btn broadcast-submit-btn"
                :disabled="isSubmittingAnnouncement"
                @click="submitCreateAnnouncement"
              >
                <span v-if="isSubmittingAnnouncement" class="spinner-xs"></span>
                <span v-else style="font-size: 1rem;">🚀</span>
                <span>{{ isSubmittingAnnouncement ? 'Publishing...' : 'Publish Announcement' }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- ANNOUNCEMENT DETAILS MODAL -->
        <div v-if="showAnnouncementDetailsModal && selectedAnnouncement" class="modal-overlay" @click.self="closeAnnouncementDetails">
          <div class="modal-card modal-card-details" style="max-width: 580px; width: 95vw;">
            <div class="modal-header" style="background: linear-gradient(135deg, #1e293b, #0f172a); color: #ffffff; border-radius: 1rem 1rem 0 0; padding: 1.25rem 1.5rem;">
              <div style="display: flex; align-items: center; gap: 0.6rem;">
                <span class="announcement-badge" :class="selectedAnnouncement.categoryClass" style="font-size: 0.82rem; padding: 0.35rem 0.75rem;">
                  {{ selectedAnnouncement.icon || '📢' }} {{ selectedAnnouncement.category }}
                </span>
                <span style="font-size: 0.82rem; color: #94a3b8;">
                  {{ selectedAnnouncement.date }}
                </span>
              </div>
              <button class="close-modal-btn" @click="closeAnnouncementDetails" style="color: #94a3b8; background: rgba(255,255,255,0.08); border-radius: 999px; width: 32px; height: 32px; display: grid; place-items: center; border: none; font-size: 1rem;">✕</button>
            </div>

            <div class="modal-body" style="padding: 1.5rem;">
              <h3 style="font-size: 1.25rem; font-weight: 800; color: #0f172a; margin: 0 0 1rem; line-height: 1.35; letter-spacing: -0.01em;">
                {{ selectedAnnouncement.title }}
              </h3>

              <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 0.85rem; padding: 1.25rem; margin-bottom: 1.25rem;">
                <h5 style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin: 0 0 0.5rem; font-weight: 700;">Announcement Details</h5>
                <p style="font-size: 0.95rem; color: #334155; line-height: 1.65; white-space: pre-wrap; margin: 0;">
                  {{ selectedAnnouncement.body || 'No detailed message description provided.' }}
                </p>
              </div>

              <div class="announcement-meta-grid" style="grid-template-columns: 1fr 1fr;">
                <div class="meta-card">
                  <span class="meta-label">Category</span>
                  <span class="meta-val font-bold">{{ selectedAnnouncement.category }}</span>
                </div>
                <div class="meta-card">
                  <span class="meta-label">Date Published</span>
                  <span class="meta-val">{{ selectedAnnouncement.date }}</span>
                </div>
              </div>
            </div>

            <div class="modal-footer" style="display: flex; justify-content: space-between; align-items: center; gap: 0.75rem; padding: 1.25rem 1.5rem; background: #f8fafc; border-top: 1px solid #e2e8f0; border-radius: 0 0 1rem 1rem;">
              <button
                type="button"
                class="cancel-modal-btn danger-btn"
                style="background: #fef2f2; color: #ef4444; border: 1px solid #fecaca; display: inline-flex; align-items: center; gap: 0.35rem;"
                @click="handleDeleteAnnouncement(selectedAnnouncement)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="15" height="15">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                <span>Delete Announcement</span>
              </button>
              <button type="button" class="cancel-modal-btn" @click="closeAnnouncementDetails">Close</button>
            </div>
          </div>
        </div>

        <!-- Edit Admin Profile Modal -->
        <div v-if="showEditProfileModal" class="modal-overlay" @click.self="closeEditProfileModal">
          <div class="modal-card" style="max-width: 520px; width: 95vw; max-height: 90vh; overflow-y: auto;">
            <!-- Modal Header -->
            <div class="modal-header" style="background: linear-gradient(135deg, #1e293b, #0f172a); color: #ffffff; border-radius: 1rem 1rem 0 0; padding: 1.25rem 1.5rem; display: flex; justify-content: space-between; align-items: center;">
              <div style="display: flex; align-items: center; gap: 0.85rem;">
                <div style="width: 42px; height: 42px; border-radius: 12px; background: linear-gradient(135deg, #3b82f6, #6366f1); display: grid; place-items: center; font-size: 1.35rem; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);">
                  👤
                </div>
                <div>
                  <h3 style="margin: 0; font-size: 1.2rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;">Edit Admin Profile</h3>
                  <span style="font-size: 0.82rem; color: #94a3b8;">Update your administrative contact details and credentials</span>
                </div>
              </div>
              <button type="button" class="close-modal-btn" @click="closeEditProfileModal" style="color: #94a3b8; background: rgba(255,255,255,0.08); border-radius: 999px; width: 32px; height: 32px; display: grid; place-items: center; border: none; font-size: 1rem; cursor: pointer;">✕</button>
            </div>

            <!-- Modal Body Form -->
            <form @submit.prevent="saveAdminProfile" class="modal-body" style="padding: 1.5rem;">
              <!-- Avatar Preview & Change -->
              <div style="display: flex; align-items: center; gap: 1.25rem; margin-bottom: 1.5rem; padding: 1rem; background: #f8fafc; border-radius: 0.85rem; border: 1px solid #e2e8f0;">
                <div style="position: relative; width: 64px; height: 64px; border-radius: 50%; background: linear-gradient(135deg, #2563eb, #4f46e5); color: #ffffff; display: grid; place-items: center; font-size: 1.3rem; font-weight: 800; overflow: hidden; flex-shrink: 0; box-shadow: 0 4px 12px rgba(37,99,235,0.3);">
                  <img v-if="editProfileForm.avatarUrl" :src="editProfileForm.avatarUrl" alt="Avatar preview" style="width: 100%; height: 100%; object-fit: cover;" />
                  <span v-else>{{ getInitials(editProfileForm.name || adminProfile.name) }}</span>
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.4rem; flex: 1;">
                  <span style="font-size: 0.85rem; font-weight: 700; color: #1e293b;">Profile Avatar</span>
                  <div style="display: flex; align-items: center; gap: 0.5rem; flex-wrap: wrap;">
                    <label class="modal-upload-btn" style="background: #2563eb; color: #ffffff; font-size: 0.78rem; font-weight: 600; padding: 0.4rem 0.85rem; border-radius: 0.5rem; cursor: pointer; display: inline-flex; align-items: center; gap: 0.35rem; transition: background 0.2s ease;">
                      📷 Choose Photo
                      <input type="file" accept="image/*" @change="handleEditAvatarUpload" style="display: none;" />
                    </label>
                    <button v-if="editProfileForm.avatarUrl" type="button" @click="removeEditAvatar" style="background: #fee2e2; color: #dc2626; border: 1px solid #fecaca; font-size: 0.78rem; font-weight: 600; padding: 0.4rem 0.85rem; border-radius: 0.5rem; cursor: pointer;">
                      Remove
                    </button>
                  </div>
                </div>
              </div>

              <!-- Full Name Field -->
              <div class="form-group" style="margin-bottom: 1.15rem;">
                <label class="form-label" style="display: block; font-size: 0.82rem; font-weight: 700; color: #334155; margin-bottom: 0.35rem;">
                  Full Name <span style="color: #ef4444;">*</span>
                </label>
                <input
                  v-model="editProfileForm.name"
                  type="text"
                  required
                  placeholder="e.g. Alex Morgan"
                  class="form-control"
                  style="width: 100%; padding: 0.65rem 0.85rem; border: 1.5px solid #cbd5e1; border-radius: 0.6rem; font-size: 0.9rem;"
                />
              </div>

              <!-- Email Field -->
              <div class="form-group" style="margin-bottom: 1.15rem;">
                <label class="form-label" style="display: block; font-size: 0.82rem; font-weight: 700; color: #334155; margin-bottom: 0.35rem;">
                  Email Address <span style="color: #ef4444;">*</span>
                </label>
                <input
                  v-model="editProfileForm.email"
                  type="email"
                  required
                  placeholder="e.g. alex.morgan@clubeon.com"
                  class="form-control"
                  style="width: 100%; padding: 0.65rem 0.85rem; border: 1.5px solid #cbd5e1; border-radius: 0.6rem; font-size: 0.9rem;"
                />
              </div>

              <!-- Phone Field -->
              <div class="form-group" style="margin-bottom: 1.15rem;">
                <label class="form-label" style="display: block; font-size: 0.82rem; font-weight: 700; color: #334155; margin-bottom: 0.35rem;">
                  Phone Number
                </label>
                <input
                  v-model="editProfileForm.phone"
                  type="text"
                  placeholder="e.g. +91 98765 43210"
                  class="form-control"
                  style="width: 100%; padding: 0.65rem 0.85rem; border: 1.5px solid #cbd5e1; border-radius: 0.6rem; font-size: 0.9rem;"
                />
              </div>

              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.15rem;">
                <!-- Role is set by the server and is not client-editable -->
                <div class="form-group">
                  <label class="form-label" style="display: block; font-size: 0.82rem; font-weight: 700; color: #334155; margin-bottom: 0.35rem;">
                    Role <span style="font-size: 0.72rem; color: #64748b; font-weight: 500;">(fixed)</span>
                  </label>
                  <input
                    :value="adminProfile.role"
                    type="text"
                    disabled
                    class="form-control"
                    style="width: 100%; padding: 0.65rem 0.85rem; border: 1.5px solid #e2e8f0; background: #f8fafc; color: #64748b; font-weight: 600; border-radius: 0.6rem; font-size: 0.9rem; cursor: not-allowed;"
                  />
                </div>

                <!-- Club name -->
                <div class="form-group">
                  <label class="form-label" style="display: block; font-size: 0.82rem; font-weight: 700; color: #334155; margin-bottom: 0.35rem;">
                    Club Name
                  </label>
                  <input
                    v-model="editProfileForm.facility"
                    type="text"
                    placeholder="e.g. Ace Sports Club"
                    class="form-control"
                    style="width: 100%; padding: 0.65rem 0.85rem; border: 1.5px solid #cbd5e1; border-radius: 0.6rem; font-size: 0.9rem;"
                  />
                </div>
              </div>

              <!-- Modal Footer -->
              <div class="modal-footer" style="display: flex; justify-content: flex-end; align-items: center; gap: 0.75rem; padding-top: 1.25rem; border-top: 1px solid #e2e8f0; margin-top: 1.5rem;">
                <button type="button" class="cancel-modal-btn" @click="closeEditProfileModal" style="background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; font-weight: 600; padding: 0.65rem 1.25rem; border-radius: 0.6rem; cursor: pointer;">
                  Cancel
                </button>
                <button type="submit" :disabled="isSavingAdminProfile" class="submit-modal-btn" style="background: linear-gradient(135deg, #2563eb, #4f46e5); color: #ffffff; font-weight: 700; padding: 0.65rem 1.4rem; border-radius: 0.6rem; border: none; cursor: pointer; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35); display: inline-flex; align-items: center; gap: 0.4rem;">
                  <span>{{ isSavingAdminProfile ? 'Saving…' : 'Save Changes' }}</span>
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="16" height="16">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                  </svg>
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- First-Time Admin Phone Setup Modal -->
        <div v-if="showFirstTimePhoneModal" class="modal-overlay" style="z-index: 500;">
          <div class="modal-card" style="max-width: 440px; width: 95vw; border-radius: 1.25rem; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);">
            <!-- Modal Header -->
            <div style="background: linear-gradient(135deg, #1e293b, #0f172a); color: #ffffff; padding: 1.5rem; text-align: center; position: relative;">
              <div style="width: 52px; height: 52px; border-radius: 16px; background: linear-gradient(135deg, #2563eb, #4f46e5); display: grid; place-items: center; font-size: 1.6rem; margin: 0 auto 0.75rem; box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);">
                📱
              </div>
              <h3 style="margin: 0 0 0.35rem; font-size: 1.25rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;">Welcome to Clubeon</h3>
              <p style="margin: 0; font-size: 0.85rem; color: #94a3b8; line-height: 1.4;">
                Please provide your contact phone number to complete your administrator setup.
              </p>
            </div>

            <!-- Modal Body Form -->
            <form @submit.prevent="submitFirstTimePhone" style="padding: 1.5rem; background: #ffffff;">
              <div class="form-group" style="margin-bottom: 1.25rem;">
                <label class="form-label" style="display: block; font-size: 0.85rem; font-weight: 700; color: #1e293b; margin-bottom: 0.45rem;">
                  Admin Phone Number <span style="color: #ef4444;">*</span>
                </label>
                <input
                  v-model="firstTimePhoneInput"
                  type="tel"
                  required
                  placeholder="e.g. +91 98765 43210"
                  class="form-control"
                  style="width: 100%; padding: 0.75rem 0.95rem; border: 1.5px solid #cbd5e1; border-radius: 0.65rem; font-size: 0.95rem;"
                  autofocus
                />
                <span style="display: block; font-size: 0.75rem; color: #64748b; margin-top: 0.4rem;">
                  🔒 You will only be asked for this once upon your first login.
                </span>
              </div>

              <div style="display: flex; gap: 0.75rem; justify-content: flex-end; align-items: center; margin-top: 1.5rem;">
                <button
                  type="button"
                  @click="skipFirstTimePhone"
                  style="background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; font-weight: 600; padding: 0.65rem 1.15rem; border-radius: 0.6rem; cursor: pointer; font-size: 0.85rem;"
                >
                  Skip for Now
                </button>
                <button
                  type="submit"
                  style="background: linear-gradient(135deg, #2563eb, #4f46e5); color: #ffffff; font-weight: 700; padding: 0.65rem 1.4rem; border-radius: 0.6rem; border: none; cursor: pointer; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35); font-size: 0.85rem;"
                >
                  Save & Continue
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
</template>


<script setup>
import { ref, computed, onMounted, inject, watch, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCourtStore } from '@/stores/courts'
import { useNotificationStore } from '@/stores/notifications'
import api from '@/api/axios'
import { getSportImage } from '@/utils/sportImages'
import BrandMark from '@/components/BrandMark.vue'
import OverviewTab from './tabs/OverviewTab.vue'
import MembersTab from './tabs/MembersTab.vue'
import CourtsTab from './tabs/CourtsTab.vue'
import BookingsTab from './tabs/BookingsTab.vue'
import EventsTab from './tabs/EventsTab.vue'
import AnnouncementsTab from './tabs/AnnouncementsTab.vue'
import AnalyticsTab from './tabs/AnalyticsTab.vue'
import SettingsTab from './tabs/SettingsTab.vue'
import { provide } from 'vue'


const props = defineProps({
  initialTab: {
    type: String,
    default: 'Dashboard',
  },
})

const route = useRoute()
const router = useRouter()
const toast = inject('toast')
const courtStore = useCourtStore()
const notificationStore = useNotificationStore()
const showAddCourtModal = ref(false)
const showEditCourtModal = ref(false)
const currentEditCourt = ref(null)
const auth = useAuthStore()
const isMobileSidebarOpen = ref(false)
const activeNav = ref(props.initialTab || route.query.tab || 'Dashboard')

watch(
  () => props.initialTab,
  (newTab) => {
    if (newTab) {
      activeNav.value = newTab
    }
  },
  { immediate: true },
)

const currentDate = ref(
  new Date().toLocaleDateString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }),
)

// =========================================================
// COURTS STATE
// =========================================================
const totalCourts = computed(() => courtStore.courts.length)
const activeCourtsCount = computed(() => courtStore.courts.filter((c) => c.is_active).length)
const inactiveCourtsCount = computed(() => courtStore.courts.filter((c) => !c.is_active).length)

const clubForm = ref({
  name: '',
  address: '',
  open_time: '',
  close_time: '',
  slot_duration_minutes: 60,
})

const courtForm = ref({
  court_name: '',
  sport_type: 'tennis',
  is_active: true,
  use_defaults: true,
  open_time_override: '',
  close_time_override: '',
  slot_duration_override: '',
})

// =========================================================
// MEMBERS STATE (REAL DATA)
// =========================================================
const memberSearchQuery = ref('')
const selectedMemberPlanFilter = ref('All')
const selectedMemberForModal = ref(null)
const showMemberModal = ref(false)
const members = ref([])

// Fetch members from backend
async function fetchMembers() {
  try {
    const res = await api.get('/admin/members')
    members.value = Array.isArray(res.data) ? res.data : []
  } catch (err) {
    console.error('Failed to fetch members:', err)
    if (toast) toast.error('Unable to load members')
  }
}

// Watch activeNav to fetch when Members tab is opened
watch(activeNav, (newTab) => {
  if (newTab === 'Members') fetchMembers()
})

// Map real backend data to display fields
const filteredMembersList = computed(() => {
  let list = members.value.map(m => ({
    id: m.id,
    name: m.name,
    email: m.email,
    initials: (m.name || 'M').charAt(0).toUpperCase(),
    plan: m.membership_plan || 'No Plan',
    dateJoined: m.created_at
      ? new Date(m.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
      : '—',
    totalBookings: m.booking_count || 0,
    phone: m.phone || '—',
    membership_status: m.membership_status || 'none'
  }))

  const q = memberSearchQuery.value.toLowerCase().trim()
  if (q) {
    list = list.filter(m =>
      (m.name && m.name.toLowerCase().includes(q)) ||
      (m.email && m.email.toLowerCase().includes(q)) ||
      (m.plan && m.plan.toLowerCase().includes(q))
    )
  }

  if (selectedMemberPlanFilter.value !== 'All') {
    list = list.filter(m => m.plan === selectedMemberPlanFilter.value)
  }
  return list
})

// KPI real values
const totalMembers = computed(() => members.value.length)
const activeMembers = computed(() => members.value.filter(m => m.membership_status === 'active').length)
const totalBookingsAll = computed(() => members.value.reduce((sum, m) => sum + (m.booking_count || 0), 0))

// =========================================================
// COURTS & CLUB ACTIONS
// =========================================================
// Fetch data on mount
// ---------------------------------------------------------------
// Live backend data (replaces the placeholder figures below)
// ---------------------------------------------------------------
const analyticsLoading = ref(false)
const analyticsError = ref('')
const adminAnalytics = ref(null)

const inr = (n) => `₹${Number(n || 0).toLocaleString('en-IN')}`

/** Pull real KPIs from /analytics/admin and map them onto the dashboard. */
async function loadAdminAnalytics() {
  analyticsLoading.value = true
  analyticsError.value = ''
  try {
    const days = parseInt(analyticsTimeframe.value, 10) || 30
    const { data } = await api.get('/analytics/admin', { params: { days } })
    adminAnalytics.value = data

    kpiCards.value = [
      {
        title: 'Total Members', value: String(data.members.total),
        icon: 'members', colorClass: 'blue',
        trend: `${data.members.active} active`, trendType: 'neutral',
      },
      {
        title: 'Active Courts',
        value: `${data.courts.active} / ${data.courts.total}`,
        icon: 'courts', colorClass: 'emerald',
        trend: `${data.courts.utilisation_percent}% utilisation`, trendType: 'neutral',
      },
      {
        title: 'Upcoming Bookings', value: String(data.bookings.upcoming),
        icon: 'bookings', colorClass: 'purple',
        trend: `${data.bookings.total} all-time`, trendType: 'neutral',
      },
      {
        title: 'Revenue', value: inr(data.revenue.total),
        icon: 'events', colorClass: 'orange',
        trend: `${data.revenue.pending_payments} pending`, trendType: 'neutral',
      },
    ]

    // Real per-court booking distribution
    const palette = ['bar-blue', 'bar-emerald', 'bar-orange', 'bar-purple']
    bookingTrends.value = data.courts.breakdown.map((c, i) => ({
      sport: c.court_name,
      count: c.bookings,
      percentage: c.percentage,
      colorClass: palette[i % palette.length],
    }))

    courtUtilization.value = [{
      period: `Overall (last ${data.window_days} days)`,
      rate: data.courts.utilisation_percent,
      colorClass: 'bar-blue',
    }]

    // --- Revenue split by what was paid for (real completed payments) ---
    const typeColors = { booking: '#2563eb', membership: '#059669', event: '#ea580c' }
    const revenueTotal = data.revenue.total || 0
    sportRevenueBreakdown.value = Object.entries(data.revenue.by_type || {}).map(
      ([type, amount]) => ({
        sport: type.charAt(0).toUpperCase() + type.slice(1),
        revenue: amount,
        percentage: revenueTotal ? Math.round((amount / revenueTotal) * 100) : 0,
        color: typeColors[type] || '#64748b',
      }),
    )

    // --- Bookings by hour of day ---
    hourlyOccupancyData.value = (data.hourly_occupancy || []).map((h) => ({
      hour: h.hour,
      rate: h.rate,
      bookings: h.bookings,
    }))

    // --- Court performance (bookings in the selected window) ---
    topPerformingFacilities.value = data.courts.breakdown.map((c) => ({
      id: c.court_id,
      name: c.court_name,
      sport: 'Court',
      hoursBooked: c.bookings,
      occupancy: `${c.percentage}%`,
      status: c.is_active ? 'Active' : 'Inactive',
    }))

    financialSummary.value = {
      grossRevenue: inr(revenueTotal),
      completedPayments: inr(revenueTotal),
      pendingPayments: data.revenue.pending_payments,
    }

    // Stripe is the only configured gateway, so the split is not a guess.
    paymentMethodBreakdown.value = revenueTotal
      ? [{ method: 'Stripe', percentage: 100, color: '#2563eb', val: inr(revenueTotal) }]
      : []
  } catch (err) {
    analyticsError.value =
      err?.response?.data?.message || 'Could not load analytics.'
  } finally {
    analyticsLoading.value = false
  }
}

/** Real bookings for this club (owners previously could not see any). */
const BOOKING_STATUS_LABELS = {
  active: 'Confirmed',
  released: 'Cancelled',
  overridden: 'Cancelled',
}
const PAYMENT_STATUS_LABELS = {
  completed: 'Paid',
  pending: 'Pending',
  failed: 'Failed',
  unpaid: 'Unpaid',
}

function titleCase(value) {
  if (!value) return ''
  return value.charAt(0).toUpperCase() + value.slice(1)
}

function durationLabel(start, end) {
  const toMinutes = (v) => {
    const [h, m] = String(v || '').split(':')
    return Number(h) * 60 + Number(m || 0)
  }
  const mins = toMinutes(end) - toMinutes(start)
  if (!Number.isFinite(mins) || mins <= 0) return ''
  const hrs = mins / 60
  return `${hrs % 1 === 0 ? hrs : hrs.toFixed(1)} hr${hrs === 1 ? '' : 's'}`
}

async function loadClubBookings() {
  bookingsLoading.value = true
  try {
    const { data } = await api.get('/bookings/club')
    bookingsList.value = (data.bookings || []).map((b) => {
      const initials = (b.member_name || '?')
        .split(' ').map((w) => w[0]).slice(0, 2).join('').toUpperCase()
      return {
        id: `BK-${b.id}`,
        bookingId: b.id,
        player: b.member_name || 'Unknown',
        email: b.member_email || '',
        phone: b.member_phone || '',
        facility: b.court_name,
        sport: titleCase(b.sport_type) || 'Multi-purpose',
        date: b.date,
        dateDisplay: b.date,
        time: `${String(b.start_time).slice(0, 5)} - ${String(b.end_time).slice(0, 5)}`,
        duration: durationLabel(b.start_time, b.end_time),
        amount: b.payment_amount ?? 0,
        paymentStatus: PAYMENT_STATUS_LABELS[b.payment_status] || 'Unpaid',
        paymentMethod: b.payment_status === 'completed' ? 'Stripe' : '',
        status: BOOKING_STATUS_LABELS[b.status] || titleCase(b.status),
        initials,
        userType: 'Member',
        createdAt: b.created_at || '',
        notes: '',
      }
    })
  } catch (err) {
    analyticsError.value =
      err?.response?.data?.message || 'Could not load bookings.'
  } finally {
    bookingsLoading.value = false
  }
}

function reloadAdminData() {
  loadAdminAnalytics()
  loadClubBookings()
}

onMounted(async () => {
  if (!auth.initialized || !auth.user) {
    try {
      await auth.restoreUser()
    } catch {
      // The route guard sends an unauthenticated user to the login screen.
    }
  }
  syncProfileWithAuthUser(auth.user)
  checkFirstTimePhoneSetup(auth.user)
  courtStore.fetchCourts()
  notificationStore.fetchAnnouncements()
  loadAdminAnalytics()
  loadClubBookings()
})


watch(
  () => courtStore.club,
  (newClub) => {
    if (newClub) {
      clubForm.value = {
        name: newClub.name,
        address: newClub.address || '',
        open_time: newClub.open_time || '',
        close_time: newClub.close_time || '',
        slot_duration_minutes: newClub.slot_duration_minutes || 60,
      }
    } else {
      clubForm.value = {
        name: '',
        address: '',
        open_time: '',
        close_time: '',
        slot_duration_minutes: 60,
      }
    }
  },
  { immediate: true },
)

const openAddCourtModal = () => {
  showEditCourtModal.value = false
  currentEditCourt.value = null
  courtForm.value = {
    court_name: '',
    sport_type: 'tennis',
    is_active: true,
    use_defaults: true,
    open_time_override: '',
    close_time_override: '',
    slot_duration_override: '',
  }
  showAddCourtModal.value = true
}

const closeAddCourtModal = () => {
  showAddCourtModal.value = false
}

const handleCreateCourt = async () => {
  const result = await courtStore.createCourt(courtForm.value)
  if (result.success) {
    closeAddCourtModal()
    toast.success('Court created successfully! 🎾')
  } else {
    toast.error(result.error || 'Failed to create court')
  }
}

const closeEditCourtModal = () => {
  showEditCourtModal.value = false
  currentEditCourt.value = null
}

const handleUpdateCourt = async () => {
  const payload = {
    court_name: courtForm.value.court_name,
    sport_type: courtForm.value.sport_type,
    is_active: courtForm.value.is_active,
    open_time_override: courtForm.value.use_defaults
      ? null
      : courtForm.value.open_time_override || null,
    close_time_override: courtForm.value.use_defaults
      ? null
      : courtForm.value.close_time_override || null,
    slot_duration_override: courtForm.value.use_defaults
      ? null
      : courtForm.value.slot_duration_override
        ? Number(courtForm.value.slot_duration_override)
        : null,
  }
  const result = await courtStore.updateCourt(currentEditCourt.value.id, payload)
  if (result.success) {
    closeEditCourtModal()
    toast.success('Court updated successfully! ✨')
  } else {
    toast.error(result.error || 'Failed to update court')
  }
}

const handleDeleteCourt = async (courtId) => {
  if (confirm('Are you sure you want to delete this court?')) {
    const result = await courtStore.deleteCourt(courtId)
    if (result.success) {
      toast.success('Court deleted successfully.')
    } else {
      toast.error(result.error || 'Failed to delete court')
    }
  }
}

const saveOrCreateClub = async () => {
  if (courtStore.club) {
    const result = await courtStore.updateClubSettings({
      name: clubForm.value.name,
      address: clubForm.value.address,
      open_time: clubForm.value.open_time || null,
      close_time: clubForm.value.close_time || null,
      slot_duration_minutes: clubForm.value.slot_duration_minutes || null,
    })
    if (result.success) {
      toast.success('Club settings updated successfully!')
    } else {
      toast.error(result.error || 'Failed to update club settings')
    }
  } else {
    if (!clubForm.value.name || !clubForm.value.address) {
      toast.error('Please provide a Club Name and Address')
      return
    }
    const result = await courtStore.createClub({
      name: clubForm.value.name,
      address: clubForm.value.address,
      open_time: clubForm.value.open_time || null,
      close_time: clubForm.value.close_time || null,
      slot_duration_minutes: clubForm.value.slot_duration_minutes || null,
    })
    if (result.success) {
      toast.success('Club created successfully! 🏛️')
    } else {
      toast.error(result.error || 'Failed to create club')
    }
  }
}

const openEditCourtModal = (court) => {
  showAddCourtModal.value = false
  currentEditCourt.value = court
  const hasOverrides =
    court.open_time_override || court.close_time_override || court.slot_duration_override
  courtForm.value = {
    court_name: court.name,
    sport_type: court.sport_type || 'multi-purpose',
    is_active: court.is_active,
    use_defaults: !hasOverrides,
    open_time_override: court.open_time_override || '',
    close_time_override: court.close_time_override || '',
    slot_duration_override: court.slot_duration_override || '',
  }
  showEditCourtModal.value = true
}

const sportLabel = (value) => {
  const sport = courtStore.sportsTypes.find((item) => item.value === value)
  return sport ? `${sport.icon} ${sport.label}` : '🏟️ Multi-purpose'
}

// =========================================================
// HEADER & NAVIGATION
// =========================================================
const headerTitle = computed(() => {
  switch (activeNav.value) {
    case 'Members': return 'Members Management'
    case 'Courts': return 'Facility & Courts'
    case 'Bookings': return 'Bookings & Reservations'
    case 'Events': return 'Events & Tournaments'
    case 'Announcements': return 'Announcements & Broadcasts'
    case 'Analytics': return 'Performance & Analytics'
    case 'Settings': return 'System Settings'
    default: return 'Admin Dashboard'
  }
})

const headerSubtitle = computed(() => {
  switch (activeNav.value) {
    case 'Members': return 'Overview of registered club members, pending requests, and player accounts.'
    case 'Courts': return 'Monitor court availability, status, and maintenance schedules.'
    case 'Bookings': return 'Track active reservations, upcoming court slots, and cancellations.'
    case 'Events': return 'Organize tournaments, coaching sessions, and social club activities.'
    case 'Announcements': return 'Broadcast facility notices, schedule updates, and tournament alerts.'
    case 'Analytics': return 'Detailed statistics on booking trends, peak hours, and membership growth.'
    case 'Settings': return 'Configure club information, operating hours, and notification preferences.'
    default: return `Welcome back${adminProfile.name ? ', ' + adminProfile.name.split(' ')[0] : ''} • Monitor club operations and analytics.`
  }
})

const primaryNavItems = ref([
  { name: 'Dashboard', icon: 'dashboard' },
  { name: 'Members', icon: 'members' },
  { name: 'Courts', icon: 'courts' },
  { name: 'Bookings', icon: 'bookings' },
  { name: 'Events', icon: 'events' },
  { name: 'Announcements', icon: 'announcements' },
  { name: 'Analytics', icon: 'analytics' },
  { name: 'Settings', icon: 'settings' },
])

const setActiveNav = (navName, push = true) => {
  activeNav.value = navName
  isMobileSidebarOpen.value = false
  if (push) {
    const slugMap = {
      'Dashboard': 'dashboard',
      'Members': 'members',
      'Courts': 'courts',
      'Bookings': 'bookings',
      'Events': 'events',
      'Announcements': 'announcements',
      'Analytics': 'analytics',
      'Settings': 'settings',
    }
    const slug = slugMap[navName] || 'dashboard'
    if (route.name !== `admin-${slug}`) {
      router.push({ name: `admin-${slug}` })
    }
  }
}

const handleLogout = async () => {
  await auth.logout()
  router.push({ name: 'login' })
}

// =========================================================
// DASHBOARD MOCK DATA (keep as is if needed, but can be dynamic)
// =========================================================
// Populated from /analytics/admin on mount.
const kpiCards = ref([])

// =========================================================
// BOOKINGS STATE
// =========================================================
// Real club bookings, loaded from /bookings/club. Starts empty so the table
// never shows figures that were not returned by the API.
const bookingsList = ref([])
const bookingsLoading = ref(true)

const bookingSearchQuery = ref('')
const bookingStatusFilter = ref('All')
const bookingFacilityFilter = ref('All')
const bookingDateFilter = ref('All')
const bookingSortBy = ref('newest')

const showBookingDetailsModal = ref(false)
const selectedBooking = ref(null)
const showNewBookingModal = ref(false)
const showCancelConfirmModal = ref(false)
const bookingToCancel = ref(null)

const newBookingForm = reactive({
  player: '',
  email: '',
  phone: '',
  facility: 'Tennis Court 1',
  sport: 'Tennis',
  date: new Date().toISOString().split('T')[0],
  time: '10:00 AM - 11:00 AM',
  duration: '1.0 hr',
  amount: 40,
  paymentStatus: 'Paid',
  status: 'Confirmed',
  userType: 'Casual Player',
  notes: ''
})

function isTimeCompleted(booking) {
  if (!booking || booking.status === 'Cancelled' || booking.status === 'Completed') return false
  const today = new Date().toISOString().split('T')[0]
  if (booking.date < today) return true
  return false
}

function getEffectiveStatus(booking) {
  if (!booking) return 'Confirmed'
  if (booking.status === 'Cancelled') return 'Cancelled'
  if (booking.status === 'Completed') return 'Completed'
  if (isTimeCompleted(booking)) return 'Completed'
  return booking.status
}

function resetBookingFilters() {
  bookingSearchQuery.value = ''
  bookingStatusFilter.value = 'All'
  bookingFacilityFilter.value = 'All'
  bookingDateFilter.value = 'All'
  bookingSortBy.value = 'newest'
}

const filteredBookings = computed(() => {
  return bookingsList.value.filter(b => {
    const q = bookingSearchQuery.value.trim().toLowerCase()
    const matchesSearch = !q ||
      b.id.toLowerCase().includes(q) ||
      b.player.toLowerCase().includes(q) ||
      b.email.toLowerCase().includes(q) ||
      b.facility.toLowerCase().includes(q)

    const effStatus = getEffectiveStatus(b)
    const matchesStatus = bookingStatusFilter.value === 'All' || effStatus.toLowerCase() === bookingStatusFilter.value.toLowerCase()
    const matchesFacility = bookingFacilityFilter.value === 'All' ||
      b.sport.toLowerCase() === bookingFacilityFilter.value.toLowerCase() ||
      b.facility.toLowerCase().includes(bookingFacilityFilter.value.toLowerCase())

    let matchesDate = true
    if (bookingDateFilter.value === 'Today') {
      matchesDate = b.dateDisplay === 'Today' || b.date === new Date().toISOString().split('T')[0]
    } else if (bookingDateFilter.value === 'Upcoming') {
      matchesDate = effStatus === 'Confirmed' || effStatus === 'Pending'
    } else if (bookingDateFilter.value === 'Past') {
      matchesDate = effStatus === 'Completed' || effStatus === 'Cancelled'
    }

    return matchesSearch && matchesStatus && matchesFacility && matchesDate
  }).sort((a, b) => {
    if (bookingSortBy.value === 'newest') return b.id.localeCompare(a.id)
    if (bookingSortBy.value === 'oldest') return a.id.localeCompare(b.id)
    if (bookingSortBy.value === 'name') return a.player.localeCompare(b.player)
    if (bookingSortBy.value === 'amount') return b.amount - a.amount
    return 0
  })
})

const bookingKpis = computed(() => {
  const total = bookingsList.value.length
  const confirmed = bookingsList.value.filter(b => getEffectiveStatus(b) === 'Confirmed').length
  const completed = bookingsList.value.filter(b => getEffectiveStatus(b) === 'Completed').length
  const autoCompleted = bookingsList.value.filter(b => isTimeCompleted(b)).length
  const cancelled = bookingsList.value.filter(b => b.status === 'Cancelled').length
  return { total, confirmed, completed, autoCompleted, cancelled }
})

function openBookingDetails(booking) {
  selectedBooking.value = booking
  showBookingDetailsModal.value = true
}

function closeBookingDetailsModal() {
  showBookingDetailsModal.value = false
  selectedBooking.value = null
}

function requestCancelBooking(booking) {
  showBookingDetailsModal.value = false
  selectedBooking.value = null
  bookingToCancel.value = booking
  showCancelConfirmModal.value = true
}

function confirmCancelBooking() {
  if (!bookingToCancel.value) return
  const target = bookingsList.value.find(b => b.id === bookingToCancel.value.id)
  if (target) {
    target.status = 'Cancelled'
    target.paymentStatus = 'Refunded'
  }
  if (selectedBooking.value && selectedBooking.value.id === bookingToCancel.value.id) {
    selectedBooking.value.status = 'Cancelled'
    selectedBooking.value.paymentStatus = 'Refunded'
  }
  showCancelConfirmModal.value = false
  bookingToCancel.value = null
  if (toast) toast.success('Booking cancelled successfully!')
}

function markBookingCompleted(booking) {
  const target = bookingsList.value.find(b => b.id === booking.id)
  if (target) target.status = 'Completed'
  if (selectedBooking.value && selectedBooking.value.id === booking.id) selectedBooking.value.status = 'Completed'
  if (toast) toast.success(`Booking ${booking.id} marked as Completed!`)
}

function openNewBookingModal() {
  newBookingForm.player = ''
  newBookingForm.email = ''
  newBookingForm.phone = ''
  newBookingForm.notes = ''
  showNewBookingModal.value = true
}

function closeNewBookingModal() {
  showNewBookingModal.value = false
}

function handleCreateNewBooking() {
  if (!newBookingForm.player || !newBookingForm.email) {
    if (toast) toast.error('Please enter player name and email.')
    return
  }
  const newId = `BK-${100 + bookingsList.value.length + 1}`
  const initials = newBookingForm.player.split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2) || 'BK'

  const createdBooking = {
    id: newId,
    player: newBookingForm.player,
    email: newBookingForm.email,
    phone: newBookingForm.phone || '+1 (555) 000-0000',
    facility: newBookingForm.facility,
    sport: newBookingForm.sport,
    date: newBookingForm.date,
    dateDisplay: newBookingForm.date,
    time: newBookingForm.time,
    duration: newBookingForm.duration || '1.0 hr',
    amount: Number(newBookingForm.amount) || 0,
    paymentStatus: newBookingForm.paymentStatus,
    paymentMethod: 'Admin Manual Entry',
    status: newBookingForm.status,
    initials: initials,
    userType: newBookingForm.userType,
    createdAt: new Date().toLocaleString(),
    notes: newBookingForm.notes || 'Created manually by Admin'
  }

  bookingsList.value.unshift(createdBooking)
  showNewBookingModal.value = false
  if (toast) toast.success(`New booking ${newId} created successfully!`)
}

function exportBookingsCSV() {
  const headers = ['Booking ID', 'Player', 'Email', 'Facility', 'Sport', 'Date', 'Time', 'Amount', 'Payment Status', 'Booking Status']
  const rows = filteredBookings.value.map(b => [
    b.id,
    `"${b.player}"`,
    `"${b.email}"`,
    `"${b.facility}"`,
    b.sport,
    b.date,
    `"${b.time}"`,
    b.amount,
    b.paymentStatus,
    b.status
  ])

  const csvContent = [headers.join(','), ...rows.map(e => e.join(','))].join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', `clubeon_bookings_${new Date().toISOString().split('T')[0]}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  if (toast) toast.success('Bookings exported to CSV!')
}

// =========================================================
// ANALYTICS DATA (MOCK)
// =========================================================
// Populated from /analytics/admin on mount.
const bookingTrends = ref([])

// Populated from /analytics/admin on mount.
const courtUtilization = ref([])

// =========================================================
// ANNOUNCEMENTS STATE
// =========================================================
const announcementsSearchQuery = ref('')
const announcementsCategoryFilter = ref('All')
const showCreateAnnouncementModal = ref(false)
const showAnnouncementDetailsModal = ref(false)
const selectedAnnouncement = ref(null)
const isSubmittingAnnouncement = ref(false)

const announcementForm = ref({
  title: '',
  category: 'General',
  body: '',
})

const announcements = computed(() => notificationStore.announcements)

const filteredAnnouncements = computed(() => {
  let list = announcements.value
  if (announcementsCategoryFilter.value !== 'All') {
    list = list.filter(item => item.category.toLowerCase() === announcementsCategoryFilter.value.toLowerCase())
  }
  if (announcementsSearchQuery.value.trim()) {
    const q = announcementsSearchQuery.value.toLowerCase()
    list = list.filter(item =>
      (item.title && item.title.toLowerCase().includes(q)) ||
      (item.body && item.body.toLowerCase().includes(q))
    )
  }
  return list
})

const openCreateAnnouncementModal = () => {
  showAnnouncementDetailsModal.value = false
  selectedAnnouncement.value = null
  announcementForm.value = {
    title: '',
    category: 'General',
    body: '',
  }
  showCreateAnnouncementModal.value = true
}

const applyAnnouncementTemplate = (templateType) => {
  if (templateType === 'maintenance') {
    announcementForm.value = {
      title: 'Scheduled Court Maintenance & Surface Care',
      category: 'Maintenance',
      body: 'Courts 1 and 2 will be temporarily unavailable on Thursday from 08:00 AM to 02:00 PM for deep surface cleaning and line recoating. Regular reservations resume at 02:30 PM.',
    }
  } else if (templateType === 'tournament') {
    announcementForm.value = {
      title: 'Registrations Open: Club Summer Grand Slam 2026',
      category: 'Tournament',
      body: 'Sign-ups are officially live for our annual summer championship! Singles and doubles brackets available with trophies, medal awards, and ₹50,000 cash prize pool.',
    }
  } else if (templateType === 'policy') {
    announcementForm.value = {
      title: 'Updated Court Booking Rules & Footwear Guidelines',
      category: 'Policy',
      body: 'All players are kindly reminded to check in with front desk reception prior to slot start time. Strict non-marking sports shoes are required on all indoor synthetic courts.',
    }
  } else if (templateType === 'broadcast') {
    announcementForm.value = {
      title: 'Flash Alert: Evening Facility Hours Extended',
      category: 'Broadcast',
      body: 'Due to overwhelming demand, court floodlight operating hours are extended until 11:00 PM throughout this weekend. Slots are now open on the booking calendar.',
    }
  }
  if (toast) {
    toast.success('Template loaded!')
  }
}

const handleCreateAnnouncement = () => {
  openCreateAnnouncementModal()
}

const closeCreateAnnouncementModal = () => {
  showCreateAnnouncementModal.value = false
}

const submitCreateAnnouncement = async () => {
  if (!announcementForm.value.title.trim()) {
    if (toast) {
      toast.error('Please enter an announcement title')
    } else {
      alert('Please enter an announcement title')
    }
    return
  }
  if (!announcementForm.value.body.trim()) {
    if (toast) {
      toast.error('Please enter announcement message content')
    } else {
      alert('Please enter announcement message content')
    }
    return
  }
  isSubmittingAnnouncement.value = true
  const result = await notificationStore.createAnnouncement({
    title: announcementForm.value.title.trim(),
    body: announcementForm.value.body.trim(),
    category: announcementForm.value.category,
  })
  isSubmittingAnnouncement.value = false

  if (result.success) {
    closeCreateAnnouncementModal()
    if (toast) {
      toast.success('Announcement broadcasted successfully! 📢')
    } else {
      alert('Announcement broadcasted!')
    }
  } else {
    if (toast) {
      toast.error(result.error || 'Failed to broadcast announcement')
    } else {
      alert(result.error || 'Failed to broadcast')
    }
  }
}

const openAnnouncementDetails = (item) => {
  showCreateAnnouncementModal.value = false
  selectedAnnouncement.value = item
  showAnnouncementDetailsModal.value = true
  if (!item.is_read) notificationStore.markAsRead(item.id)
}

const closeAnnouncementDetails = () => {
  showAnnouncementDetailsModal.value = false
  selectedAnnouncement.value = null
}

const refreshAnnouncements = async () => {
  await notificationStore.fetchAnnouncements()
  if (notificationStore.error) {
    if (toast) {
      toast.error(notificationStore.error)
    }
  } else {
    if (toast) {
      toast.success('Announcements refreshed')
    }
  }
}

const handleDeleteAnnouncement = async (item) => {
  if (!item) return
  if (!confirm(`Are you sure you want to delete "${item.title}"?`)) return

  const result = await notificationStore.deleteAnnouncement(item.id)
  if (!result.success) {
    if (toast) {
      toast.error(result.error)
    } else {
      alert(result.error)
    }
    return
  }
  if (selectedAnnouncement.value && selectedAnnouncement.value.id === item.id) {
    closeAnnouncementDetails()
  }
  if (toast) {
    toast.success('Announcement removed')
  }
}

// =========================================================
// EVENTS STATE
// =========================================================
const eventViewMode = ref('grid')
const eventSearchQuery = ref('')
const eventStatusFilter = ref('All')
const eventSportFilter = ref('All')
const eventTypeFilter = ref('All')
const eventSortBy = ref('date')

const showCreateEventModal = ref(false)
const showEditEventModal = ref(false)
const showEventDetailsModal = ref(false)
const showDeleteEventModal = ref(false)

const selectedEvent = ref(null)
const editingEvent = ref(null)
const eventToDelete = ref(null)

const eventsList = ref([])

async function loadEvents() {
  try {
    const clubId = courtStore.club?.id || (courtStore.courts && courtStore.courts[0]?.club_id) || ''
    const url = clubId ? `/events?club_id=${clubId}&status=all` : '/events?status=all'
    const res = await api.get(url)
    eventsList.value = (res.data || []).map(e => ({
      id: e.id,
      title: e.title,
      // The Event model carries no type or sport, so labelling everything a
      // "Tournament" mislabelled coaching clinics and open days.
      type: e.type || 'Event',
      sport: e.sport || '',
      date: e.date,
      dateDisplay: new Date(e.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
      time: `${(e.start_time || '09:00').substring(0, 5)} - ${(e.end_time || '18:00').substring(0, 5)}`,
      start_time: (e.start_time || '09:00').substring(0, 5),
      end_time: (e.end_time || '18:00').substring(0, 5),
      venue: e.venue || (courtStore.club?.name || 'Main Arena'),
      capacity: e.max_attendees || 30,
      registered: e.registered_count || 0,
      fee: e.registration_fee || 0,
      status: e.status ? (e.status.charAt(0).toUpperCase() + e.status.slice(1)) : 'Upcoming',
      organizer: 'Club Owner',
      description: e.description || '',
      participants: []
    }))
  } catch (error) {
    console.error('Failed to load events:', error)
  }
}

onMounted(loadEvents)

watch(() => courtStore.club, loadEvents)

const upcomingEvents = computed(() => {
  return eventsList.value.map(e => ({
    id: e.id,
    title: e.title,
    type: e.type,
    date: e.dateDisplay,
    info: `${e.registered} / ${e.capacity} Registered Players`,
    status: e.status,
    chipClass: e.sport === 'Tennis' ? 'chip-blue' : e.sport === 'Badminton' ? 'chip-emerald' : 'chip-orange',
    statusClass: e.status === 'Upcoming' ? 'status-open' : 'status-confirmed'
  }))
})

const eventForm = reactive({
  title: '', sport: 'Tennis', type: 'Tournament',
  date: new Date().toISOString().split('T')[0],
  time: '10:00 - 16:00',
  venue: 'Tennis Court 1',
  capacity: 16,
  fee: 0,
  status: 'Upcoming',
  organizer: 'Club Staff',
  description: ''
})

const editEventForm = reactive({
  id: '', title: '', sport: 'Tennis', type: 'Tournament', date: '',
  time: '', venue: '', capacity: 16, fee: 0, status: 'Upcoming', description: ''
})

const filteredEvents = computed(() => {
  return eventsList.value.filter(e => {
    const q = eventSearchQuery.value.trim().toLowerCase()
    const matchesSearch = !q ||
      e.title.toLowerCase().includes(q) ||
      e.venue.toLowerCase().includes(q) ||
      e.organizer.toLowerCase().includes(q)
    const matchesStatus = eventStatusFilter.value === 'All' || e.status.toLowerCase() === eventStatusFilter.value.toLowerCase()
    const matchesSport = eventSportFilter.value === 'All' || e.sport.toLowerCase() === eventSportFilter.value.toLowerCase()
    const matchesType = eventTypeFilter.value === 'All' || e.type.toLowerCase() === eventTypeFilter.value.toLowerCase()
    return matchesSearch && matchesStatus && matchesSport && matchesType
  }).sort((a, b) => {
    if (eventSortBy.value === 'date') return a.date.localeCompare(b.date)
    if (eventSortBy.value === 'title') return a.title.localeCompare(b.title)
    if (eventSortBy.value === 'registered') return b.registered - a.registered
    if (eventSortBy.value === 'fee') return b.fee - a.fee
    return 0
  })
})

const eventsKpis = computed(() => {
  const total = eventsList.value.length
  const upcoming = eventsList.value.filter(e => e.status === 'Upcoming' || e.status === 'Ongoing').length
  const totalRegistered = eventsList.value.reduce((sum, e) => sum + e.registered, 0)
  const totalCapacity = eventsList.value.reduce((sum, e) => sum + e.capacity, 0)
  const totalRevenue = eventsList.value.reduce((sum, e) => sum + (e.registered * e.fee), 0)
  return { total, upcoming, totalRegistered, totalCapacity, totalRevenue }
})

function resetEventFilters() {
  eventSearchQuery.value = ''
  eventStatusFilter.value = 'All'
  eventSportFilter.value = 'All'
  eventTypeFilter.value = 'All'
  eventSortBy.value = 'date'
}

function openCreateEventModal() {
  eventForm.title = ''
  eventForm.description = ''
  showCreateEventModal.value = true
}

function closeCreateEventModal() {
  showCreateEventModal.value = false
}

function _parseTimeString(t, defaultTime = '10:00') {
  if (!t) return defaultTime
  const raw = t.trim()
  if (raw.includes(':')) {
    const parts = raw.replace(/(am|pm)/i, '').trim().split(':')
    let h = parseInt(parts[0])
    if (/pm/i.test(raw) && h < 12) h += 12
    return `${h.toString().padStart(2, '0')}:${(parts[1] || '00').padStart(2, '0')}`
  }
  return defaultTime
}

async function handleCreateEvent() {
  if (!eventForm.title) {
    if (toast) toast.error('Please fill in event title.')
    return
  }
  const clubId = courtStore.club?.id || (courtStore.courts && courtStore.courts[0]?.club_id) || undefined
  let [startTimeStr, endTimeStr] = ['10:00', '16:00']
  if (eventForm.time && eventForm.time.includes('-')) {
    const parts = eventForm.time.split('-')
    startTimeStr = parts[0].trim()
    endTimeStr = parts[1].trim()
  }

  const payload = {
    club_id: clubId,
    title: eventForm.title,
    description: eventForm.description || '',
    event_date: eventForm.date || new Date().toISOString().split('T')[0],
    start_time: _parseTimeString(startTimeStr, '10:00'),
    end_time: _parseTimeString(endTimeStr, '16:00'),
    max_attendees: Number(eventForm.capacity) || 20,
    registration_fee: Number(eventForm.fee) || 0
  }

  try {
    await api.post('/events', payload)
    showCreateEventModal.value = false
    await loadEvents()
    if (toast) toast.success(`Event "${payload.title}" created successfully!`)
  } catch (err) {
    if (toast) toast.error(err.response?.data?.message || 'Failed to create event.')
  }
}

function openEventDetails(event) {
  selectedEvent.value = event
  showEventDetailsModal.value = true
}

function closeEventDetailsModal() {
  showEventDetailsModal.value = false
  selectedEvent.value = null
}

function openEditEventModal(event) {
  showEventDetailsModal.value = false
  selectedEvent.value = null
  editingEvent.value = event
  editEventForm.id = event.id
  editEventForm.title = event.title
  editEventForm.sport = event.sport
  editEventForm.type = event.type
  editEventForm.date = event.date
  editEventForm.time = event.time
  editEventForm.venue = event.venue
  editEventForm.capacity = event.capacity
  editEventForm.fee = event.fee
  editEventForm.status = event.status
  editEventForm.description = event.description
  showEditEventModal.value = true
}

function closeEditEventModal() {
  showEditEventModal.value = false
  editingEvent.value = null
}

async function handleUpdateEvent() {
  if (!editingEvent.value) return
  let [startTimeStr, endTimeStr] = [editingEvent.value.start_time || '10:00', editingEvent.value.end_time || '16:00']
  if (editEventForm.time && editEventForm.time.includes('-')) {
    const parts = editEventForm.time.split('-')
    startTimeStr = parts[0].trim()
    endTimeStr = parts[1].trim()
  }

  const payload = {
    title: editEventForm.title,
    description: editEventForm.description,
    event_date: editEventForm.date,
    start_time: _parseTimeString(startTimeStr, '10:00'),
    end_time: _parseTimeString(endTimeStr, '16:00'),
    max_attendees: Number(editEventForm.capacity) || 20,
    registration_fee: Number(editEventForm.fee) || 0,
    status: (editEventForm.status || 'upcoming').toLowerCase()
  }

  try {
    await api.put(`/events/${editingEvent.value.id}`, payload)
    showEditEventModal.value = false
    editingEvent.value = null
    await loadEvents()
    if (toast) toast.success('Event details updated successfully!')
  } catch (err) {
    if (toast) toast.error(err.response?.data?.message || 'Failed to update event.')
  }
}

function requestDeleteEvent(event) {
  showEventDetailsModal.value = false
  selectedEvent.value = null
  eventToDelete.value = event
  showDeleteEventModal.value = true
}

async function confirmDeleteEvent() {
  if (!eventToDelete.value) return
  try {
    await api.delete(`/events/${eventToDelete.value.id}`)
    showDeleteEventModal.value = false
    if (showEventDetailsModal.value) showEventDetailsModal.value = false
    if (toast) toast.success(`Event "${eventToDelete.value.title}" cancelled.`)
    eventToDelete.value = null
    await loadEvents()
  } catch (err) {
    if (toast) toast.error(err.response?.data?.message || 'Failed to cancel event.')
  }
}

function addSampleParticipant(event) {
  const sampleNames = ['Alex Morgan', 'Carlos Alcaraz', 'Coco Gauff', 'Novak D.', 'Iga Swiatek', 'Jannik Sinner']
  const randomName = sampleNames[Math.floor(Math.random() * sampleNames.length)]
  if (event.registered < event.capacity) {
    event.participants = event.participants || []
    event.participants.push(randomName)
    event.registered += 1
    if (toast) toast.success(`Registered ${randomName} to event!`)
  } else {
    if (toast) toast.error('Event is already at full capacity!')
  }
}

function removeParticipant(event, index) {
  if (event.participants && event.participants[index]) {
    const removedName = event.participants[index]
    event.participants.splice(index, 1)
    event.registered = Math.max(0, event.registered - 1)
    if (toast) toast.success(`Removed ${removedName} from event.`)
  }
}

// =========================================================
// ANALYTICS TAB REACTIVE STATE & EXPORT
// =========================================================
const analyticsTimeframe = ref('30 Days')

// Membership split, from the live /analytics/admin payload.
const membershipOverview = computed(() => {
  const m = adminAnalytics.value?.members
  if (!m) return { total: 0, permanent: 0, permanentPct: 0, publicPlayers: 0, publicPct: 0 }
  const permanent = m.active
  const publicPlayers = m.public_players ?? 0
  const total = permanent + publicPlayers
  const pct = (n) => (total ? Math.round((n / total) * 1000) / 10 : 0)
  return { total, permanent, permanentPct: pct(permanent),
           publicPlayers, publicPct: pct(publicPlayers) }
})

// Analytics-tab KPIs, derived from the live /analytics/admin payload.
const analyticsKpis = computed(() => {
  const d = adminAnalytics.value
  if (!d) {
    return { revenue: '—', window: '', peakHour: '—', peakBookings: '',
             activeMembers: '—', totalMembers: 0, utilisation: '—', bookingsInWindow: 0 }
  }
  const peak = (d.hourly_occupancy || []).reduce(
    (best, h) => (best && best.bookings >= h.bookings ? best : h), null)
  return {
    revenue: inr(d.revenue.total),
    window: `Last ${d.window_days} days`,
    peakHour: peak && peak.bookings ? peak.hour : 'No bookings yet',
    peakBookings: peak && peak.bookings ? `${peak.bookings} bookings` : '',
    activeMembers: String(d.members.active),
    totalMembers: d.members.total,
    utilisation: `${d.courts.utilisation_percent}%`,
    bookingsInWindow: d.bookings.in_window,
  }
})
// Re-fetch real analytics when the timeframe selector changes
watch(analyticsTimeframe, () => loadAdminAnalytics())
const activeChartMetric = ref('revenue')

// Populated from /analytics/admin on mount.
const sportRevenueBreakdown = ref([])

// Donut geometry derived from the live revenue split. The chart used to be a
// fixed 45/30/15/10 pie with a "₹4.82L" total painted into the markup, so it
// contradicted the legend rendered right beside it.
const DONUT_CIRCUMFERENCE = 2 * Math.PI * 38

const donutSegments = computed(() => {
  const total = sportRevenueBreakdown.value.reduce((sum, i) => sum + (i.revenue || 0), 0)
  if (!total) return []

  let consumed = 0
  return sportRevenueBreakdown.value.map((item) => {
    const length = (item.revenue / total) * DONUT_CIRCUMFERENCE
    const segment = {
      sport: item.sport,
      color: item.color,
      dashArray: `${length.toFixed(2)} ${(DONUT_CIRCUMFERENCE - length).toFixed(2)}`,
      dashOffset: (-consumed).toFixed(2),
    }
    consumed += length
    return segment
  })
})

// Monthly growth chart, from /analytics/admin `monthly`. The bars used to be a
// literal array of invented figures (₹2.45L … ₹4.82L, 320–648 bookings) that
// stayed on screen no matter what the club had actually taken.
const growthChart = computed(() => {
  const rows = adminAnalytics.value?.monthly || []
  const metric = activeChartMetric.value === 'revenue' ? 'revenue' : 'bookings'
  const values = rows.map((r) => Number(r[metric]) || 0)
  const peak = Math.max(...values, 0)

  const compact = (n) => {
    if (metric === 'bookings') return String(Math.round(n))
    if (n >= 100000) return `₹${(n / 100000).toFixed(2)}L`
    if (n >= 1000) return `₹${(n / 1000).toFixed(1)}K`
    return `₹${Math.round(n)}`
  }

  // Three gridline labels at 100%, 70% and 40% of the peak.
  const axis = peak
    ? [compact(peak), compact(peak * 0.7), compact(peak * 0.4)]
    : ['', '', '']

  const trackHeight = 155
  const baseline = 185
  const slot = rows.length ? 630 / rows.length : 0

  const bars = rows.map((row, i) => {
    const value = Number(row[metric]) || 0
    const h = peak ? Math.max((value / peak) * trackHeight, value > 0 ? 3 : 0) : 0
    const w = Math.min(38, Math.max(slot - 42, 14))
    return {
      month: row.month,
      x: 55 + i * slot,
      w,
      h,
      y: baseline - h,
      label: value ? compact(value) : '',
    }
  })

  return { bars, axis }
})

const revenueTotalLabel = computed(() => {
  const total = sportRevenueBreakdown.value.reduce((sum, i) => sum + (i.revenue || 0), 0)
  if (total >= 100000) return `₹${(total / 100000).toFixed(2)}L`
  return inr(total)
})

// Populated from /analytics/admin on mount.
const hourlyOccupancyData = ref([])

// Populated from /analytics/admin on mount.
const topPerformingFacilities = ref([])

// Populated from /analytics/admin on mount.
const paymentMethodBreakdown = ref([])

// Populated from /analytics/admin. Costs and profit are not modelled anywhere
// in the backend, so they are not shown rather than invented.
const financialSummary = ref({
  grossRevenue: '—', completedPayments: '—', pendingPayments: 0,
})

function exportAnalyticsCSV() {
  const data = adminAnalytics.value
  if (!data) {
    if (toast) toast.error('Analytics are still loading. Please try again.')
    return
  }

  const headers = ['Report Metric / Category', 'Value / Details', 'Timeframe / Period']
  const window = `Last ${data.window_days} days`
  const rows = [
    ['Report Title', `${data.club.name} — Analytics Report`, `Generated: ${new Date().toLocaleDateString()}`],
    ['Selected Timeframe', analyticsTimeframe.value, ''],
    ['Total Revenue', `INR ${Number(data.revenue.total).toLocaleString('en-IN')}`, window],
    ['Pending Payments', data.revenue.pending_payments, ''],
    ['Failed Payments', data.revenue.failed_payments, ''],
    ['Total Bookings', data.bookings.total, 'All time'],
    ['Bookings In Window', data.bookings.in_window, window],
    ['Upcoming Bookings', data.bookings.upcoming, ''],
    ['Cancelled / Released', data.bookings.released + data.bookings.overridden, ''],
    ['Members', data.members.total, `${data.members.active} active`],
    ['Courts', data.courts.total, `${data.courts.active} active`],
    ['Court Utilisation', `${data.courts.utilisation_percent}%`, window],
    ['Events', data.events.total, `${data.events.registrations} registrations`],
    ['---', '---', '---'],
    ['Revenue By Type', 'Amount (INR)', 'Share'],
    ...Object.entries(data.revenue.by_type || {}).map(([type, amount]) => [
      type.charAt(0).toUpperCase() + type.slice(1),
      Number(amount).toLocaleString('en-IN'),
      data.revenue.total ? `${Math.round((amount / data.revenue.total) * 100)}%` : '0%',
    ]),
    ['---', '---', '---'],
    ['Bookings By Court', 'Bookings', 'Share'],
    ...data.courts.breakdown.map((c) => [c.court_name, c.bookings, `${c.percentage}%`]),
    ['---', '---', '---'],
    ['Bookings By Hour', 'Bookings', 'Relative Occupancy'],
    ...(data.hourly_occupancy || []).map((h) => [h.hour, h.bookings, `${h.rate}%`]),
    ['---', '---', '---'],
    ['Daily Booking Trend', 'Date', 'Bookings'],
    ...(data.trend || []).map((t) => ['', t.date, t.bookings]),
  ]
  const csvContent = [headers.join(','), ...rows.map(e => e.map(cell => `"${cell}"`).join(','))].join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', `clubeon_analytics_report_${new Date().toISOString().split('T')[0]}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  if (toast) toast.success('Analytics report downloaded successfully! 📊')
}

// =========================================================
// MEMBER DETAILS & EXPORT (UPDATED)
// =========================================================
function viewMemberDetails(member) {
  selectedMemberForModal.value = member
  showMemberModal.value = true
}

function exportMembersCSV() {
  const headers = ['Name', 'Email', 'Membership Plan', 'Booking Count', 'Status']
  const rows = filteredMembersList.value.map(m => [
    m.name,
    m.email,
    m.plan,
    m.totalBookings,
    m.membership_status
  ])
  const csv = [headers, ...rows].map(r => r.join(',')).join('\n')
  const blob = new Blob([csv], { type: 'text/csv' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = 'club_members.csv'
  link.click()
}

// --- REAL-TIME ADMIN PROFILE STATE ---
const showProfilePopover = ref(false)
const showEditProfileModal = ref(false)
const isSavingAdminProfile = ref(false)
const showFirstTimePhoneModal = ref(false)
const firstTimePhoneInput = ref('')

// Placeholders are blank so the UI never shows a name, role or club the
// server did not return; syncProfileWithAuthUser fills them in.
const adminProfile = reactive({
  name: '',
  role: '',
  email: '',
  phone: '',
  facility: '',
  memberSince: '',
  initials: '',
  avatarUrl: null
})

const editProfileForm = reactive({
  name: '',
  email: '',
  phone: '',
  role: '',
  facility: '',
  avatarUrl: null
})

// The system has three roles: owner, front-desk and player. There is no
// "Super Admin"; labelling the club owner as one overstated their scope.
function formatRole(role) {
  if (!role) return ''
  const key = role.toLowerCase()
  if (key === 'owner') return 'Club Owner'
  if (key === 'front-desk') return 'Front Desk'
  if (key === 'player') return 'Member'
  return role.charAt(0).toUpperCase() + role.slice(1)
}

function formatMemberSince(createdAt) {
  if (!createdAt) return 'Recent'
  try {
    const d = new Date(createdAt)
    if (isNaN(d.getTime())) return 'Recent'
    return d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
  } catch {
    return 'Recent'
  }
}

function getInitials(name) {
  if (!name) return 'AD'
  const parts = name.trim().split(' ').filter(Boolean)
  if (parts.length >= 2) {
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
  } else if (parts.length === 1 && parts[0].length > 0) {
    return parts[0].slice(0, 2).toUpperCase()
  }
  return 'AD'
}

function checkFirstTimePhoneSetup(u) {
  if (!u) return
  const userKey = `phone_prompt_done_${u.id || u.email}`
  const alreadyPrompted = localStorage.getItem(userKey)
  // If user has no phone in db and has not completed initial prompt
  if (!u.phone && !alreadyPrompted) {
    firstTimePhoneInput.value = ''
    showFirstTimePhoneModal.value = true
  }
}

async function submitFirstTimePhone() {
  const phoneVal = firstTimePhoneInput.value.trim()
  if (!phoneVal) {
    if (toast) toast.error('Please enter a valid phone number.')
    return
  }

  try {
    if (auth.isAuthenticated()) {
      await auth.updateProfile({ phone: phoneVal })
    } else if (auth.user) {
      auth.user.phone = phoneVal
    }
  } catch (err) {
    console.warn('Error saving initial phone:', err)
  }

  adminProfile.phone = phoneVal
  const userKey = `phone_prompt_done_${auth.user?.id || auth.user?.email || 'default'}`
  localStorage.setItem(userKey, 'true')

  showFirstTimePhoneModal.value = false
  if (toast) toast.success('Phone number saved successfully! 📱')
}

function skipFirstTimePhone() {
  const userKey = `phone_prompt_done_${auth.user?.id || auth.user?.email || 'default'}`
  localStorage.setItem(userKey, 'true')
  showFirstTimePhoneModal.value = false
}

// The profile is server state. It used to be mirrored into localStorage, which
// meant the avatar and phone number only existed in one browser, and the
// no-user branch dereferenced `u` and threw.
function syncProfileWithAuthUser(u) {
  if (!u) {
    adminProfile.name = ''
    adminProfile.email = ''
    adminProfile.role = ''
    adminProfile.phone = ''
    adminProfile.facility = ''
    adminProfile.memberSince = ''
    adminProfile.initials = ''
    adminProfile.avatarUrl = null
    return
  }

  adminProfile.name = u.name || ''
  adminProfile.email = u.email || ''
  adminProfile.role = formatRole(u.role)
  adminProfile.initials = getInitials(adminProfile.name)
  adminProfile.phone = u.phone || ''
  // `facility` is the owner's club name, resolved by the API.
  adminProfile.facility = u.facility || ''
  adminProfile.memberSince = formatMemberSince(u.created_at)
  adminProfile.avatarUrl = u.avatar_url || null
}

// Reactively watch for auth.user changes
watch(
  () => auth.user,
  (newUser) => {
    syncProfileWithAuthUser(newUser)
    if (newUser) {
      checkFirstTimePhoneSetup(newUser)
    }
  },
  { immediate: true, deep: true }
)

function toggleProfilePopover() {
  showProfilePopover.value = !showProfilePopover.value
}

function openEditProfileModal() {
  editProfileForm.name = adminProfile.name
  editProfileForm.email = adminProfile.email
  editProfileForm.phone = adminProfile.phone
  editProfileForm.role = adminProfile.role
  editProfileForm.facility = adminProfile.facility
  editProfileForm.avatarUrl = adminProfile.avatarUrl
  showEditProfileModal.value = true
}

function closeEditProfileModal() {
  showEditProfileModal.value = false
}

async function handleEditAvatarUpload(event) {
  const file = event.target.files && event.target.files[0]
  event.target.value = ''
  if (!file) return
  if (!file.type.startsWith('image/')) {
    if (toast) toast.error('Please choose an image file.')
    return
  }
  try {
    editProfileForm.avatarUrl = await downscaleImage(file)
  } catch (err) {
    if (toast) toast.error(err.message || 'Could not read that image.')
  }
}

function removeEditAvatar() {
  editProfileForm.avatarUrl = null
}

async function saveAdminProfile() {
  if (!editProfileForm.name || !editProfileForm.name.trim()) {
    if (toast) toast.error('Please enter a valid full name.')
    return
  }
  if (!editProfileForm.email || !editProfileForm.email.trim()) {
    if (toast) toast.error('Please enter a valid email address.')
    return
  }

  const newName = editProfileForm.name.trim()
  const newEmail = editProfileForm.email.trim()
  const newPhone = editProfileForm.phone.trim()

  isSavingAdminProfile.value = true
  try {
    // name / email / phone, plus the club rename that `facility` performs.
    await auth.updateProfile({
      name: newName,
      email: newEmail,
      phone: newPhone,
      facility: editProfileForm.facility.trim(),
    })

    // The avatar lives on a different endpoint.
    if ((editProfileForm.avatarUrl || null) !== (adminProfile.avatarUrl || null)) {
      const { data } = await api.put('/auth/profile/details', {
        avatar_url: editProfileForm.avatarUrl || '',
      })
      auth.user = { ...auth.user, avatar_url: data.user?.avatar_url || null }
    }

    syncProfileWithAuthUser(auth.user)
    courtStore.fetchCourts()
    showEditProfileModal.value = false
    if (toast) toast.success('Profile updated.')
  } catch (err) {
    // Never report success for a save the server rejected.
    if (toast) {
      toast.error(err?.response?.data?.message || 'Could not save your profile.')
    }
  } finally {
    isSavingAdminProfile.value = false
  }
}

// Avatars are stored as a data: URL on the user row, so the source image is
// downscaled first to keep that row small.
const AVATAR_MAX_PX = 320
const AVATAR_QUALITY = 0.82

function downscaleImage(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onerror = () => reject(new Error('Could not read that file.'))
    reader.onload = () => {
      const img = new Image()
      img.onerror = () => reject(new Error('That file is not a readable image.'))
      img.onload = () => {
        const scale = Math.min(1, AVATAR_MAX_PX / Math.max(img.width, img.height))
        const canvas = document.createElement('canvas')
        canvas.width = Math.round(img.width * scale)
        canvas.height = Math.round(img.height * scale)
        canvas.getContext('2d').drawImage(img, 0, 0, canvas.width, canvas.height)
        resolve(canvas.toDataURL('image/jpeg', AVATAR_QUALITY))
      }
      img.src = reader.result
    }
    reader.readAsDataURL(file)
  })
}

async function handleAvatarUpload(event) {
  const file = event.target.files && event.target.files[0]
  event.target.value = ''
  if (!file) return
  if (!file.type.startsWith('image/')) {
    if (toast) toast.error('Please choose an image file.')
    return
  }
  try {
    const dataUrl = await downscaleImage(file)
    const { data } = await api.put('/auth/profile/details', { avatar_url: dataUrl })
    adminProfile.avatarUrl = data.user?.avatar_url || dataUrl
    auth.user = { ...auth.user, avatar_url: adminProfile.avatarUrl }
    if (toast) toast.success('Profile picture updated.')
  } catch (err) {
    if (toast) toast.error(err?.response?.data?.message || 'Could not update your photo.')
  }
}


// Provide admin context to modular tab components
provide('adminContext', {
  activeChartMetric,
  activeCourtsCount,
  activeMembers,
  activeNav,
  adminProfile,
  analyticsError,
  analyticsKpis,
  analyticsLoading,
  analyticsTimeframe,
  announcements,
  announcementsCategoryFilter,
  announcementsSearchQuery,
  bookingDateFilter,
  bookingFacilityFilter,
  bookingKpis,
  bookingSearchQuery,
  bookingSortBy,
  bookingStatusFilter,
  bookingTrends,
  bookingsList,
  bookingsLoading,
  clubForm,
  courtStore,
  courtUtilization,
  donutSegments,
  eventSearchQuery,
  eventSortBy,
  eventSportFilter,
  eventStatusFilter,
  eventTypeFilter,
  eventViewMode,
  eventsKpis,
  exportAnalyticsCSV,
  exportBookingsCSV,
  exportMembersCSV,
  filteredAnnouncements,
  filteredBookings,
  filteredEvents,
  filteredMembersList,
  financialSummary,
  getEffectiveStatus,
  growthChart,
  handleCreateAnnouncement,
  handleDeleteAnnouncement,
  handleDeleteCourt,
  hourlyOccupancyData,
  inactiveCourtsCount,
  isTimeCompleted,
  kpiCards,
  markBookingCompleted,
  memberSearchQuery,
  members,
  membershipOverview,
  notificationStore,
  openAddCourtModal,
  openAnnouncementDetails,
  openBookingDetails,
  openCreateEventModal,
  openEditCourtModal,
  openEditEventModal,
  openEventDetails,
  openNewBookingModal,
  paymentMethodBreakdown,
  refreshAnnouncements,
  reloadAdminData,
  requestCancelBooking,
  requestDeleteEvent,
  resetBookingFilters,
  resetEventFilters,
  revenueTotalLabel,
  saveOrCreateClub,
  selectedMemberPlanFilter,
  sportLabel,
  sportRevenueBreakdown,
  topPerformingFacilities,
  totalBookingsAll,
  totalCapacity,
  totalCourts,
  totalMembers,
  totalRegistered,
  totalRevenue,
  upcomingEvents,
  viewMemberDetails
})

</script>

<style>
@import './admin.css';
</style>
