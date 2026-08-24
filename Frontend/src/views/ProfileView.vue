<template>
  <div class="player-profile-view">
    <p v-if="loadError" class="profile-alert" role="alert">
      {{ loadError }}
      <button type="button" class="profile-alert-retry" @click="reload">Retry</button>
    </p>

    <!-- 1. Hero Profile Banner -->
    <section class="profile-hero-card">
      <div class="hero-cover-pattern"></div>
      <div class="hero-inner">
        <div class="avatar-col">
          <div class="avatar-box">
            <img
              v-if="userState.avatarUrl"
              :src="userState.avatarUrl"
              :alt="userState.name"
              class="avatar-image"
            />
            <div v-else class="avatar-initials">
              {{ getInitials(userState.name) }}
            </div>
            <button
              @click="triggerAvatarUpload"
              class="avatar-camera-btn"
              title="Change Profile Photo"
              aria-label="Change profile photo"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="15" height="15">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
          </div>
        </div>

        <div class="hero-info-col">
          <div class="name-row">
            <h1 class="user-display-name">{{ userState.name || 'Member' }}</h1>
            <span class="role-pill">{{ roleLabel }}</span>
            <span v-if="activeMembership" class="status-pill live">
              {{ activeMembership.plan_name || 'Member' }}
            </span>
          </div>
          <p class="user-email-text">{{ userState.email }}</p>

          <!-- Quick Metrics Bar -->
          <div class="metrics-bar">
            <div class="metric-item">
              <div class="metric-icon-wrap blue">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="16" height="16">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <div>
                <span class="metric-num">{{ bookingsCount }}</span>
                <span class="metric-lbl">Total Bookings</span>
              </div>
            </div>

            <div class="metric-divider"></div>

            <div class="metric-item">
              <div class="metric-icon-wrap emerald">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="16" height="16">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <div>
                <span class="metric-num">{{ homeFacility || 'Not set' }}</span>
                <span class="metric-lbl">Home Facility</span>
              </div>
            </div>

            <div class="metric-divider"></div>

            <div class="metric-item">
              <div class="metric-icon-wrap violet">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="16" height="16">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <span class="metric-num">{{ userState.memberSince || '—' }}</span>
                <span class="metric-lbl">Member Since</span>
              </div>
            </div>
          </div>
        </div>

        <div class="hero-actions-col">
          <button @click="openEditProfileModal" class="btn-edit-hero">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="16" height="16">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
            </svg>
            <span>Edit Profile</span>
          </button>
        </div>
      </div>
    </section>

    <!-- 2. Clean 2-Column Dashboard Grid -->
    <div class="profile-content-grid">
      <!-- Left Column: Personal Information & Contact Details -->
      <div class="grid-left-col">
        <div class="card-panel">
          <div class="panel-header">
            <div class="panel-title-wrap">
              <div class="panel-icon-box">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="18" height="18">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <div>
                <h3 class="panel-title">Personal Information</h3>
                <p class="panel-sub">Account credentials & contact info</p>
              </div>
            </div>
            <button @click="openEditProfileModal" class="panel-action-btn">
              Edit
            </button>
          </div>

          <div class="info-rows-list">
            <div class="info-row">
              <span class="info-label">Full Name</span>
              <span class="info-value font-semibold">{{ userState.name || 'Not provided' }}</span>
            </div>

            <div class="info-row">
              <span class="info-label">Email Address</span>
              <span class="info-value">{{ userState.email || 'Not provided' }}</span>
            </div>

            <div class="info-row">
              <span class="info-label">Phone Number</span>
              <span class="info-value" :class="{ 'text-muted': !userState.phone }">
                {{ userState.phone || 'Not provided' }}
              </span>
            </div>

            <div class="info-row">
              <span class="info-label">Date of Birth</span>
              <span class="info-value" :class="{ 'text-muted': !userState.dob }">
                {{ formatDate(userState.dob) || 'Not provided' }}
              </span>
            </div>

            <div class="info-row">
              <span class="info-label">Gender</span>
              <span class="info-value" :class="{ 'text-muted': !userState.gender }">
                {{ userState.gender || 'Not provided' }}
              </span>
            </div>

            <div class="info-row">
              <span class="info-label">Address</span>
              <span class="info-value" :class="{ 'text-muted': !userState.address }">
                {{ userState.address || 'Not provided' }}
              </span>
            </div>

            <div class="info-row">
              <span class="info-label">Home Facility</span>
              <span v-if="homeFacility" class="info-value badge-facility">{{ homeFacility }}</span>
              <span v-else class="info-value text-muted">No bookings yet</span>
            </div>

            <div class="info-row">
              <span class="info-label">Member Since</span>
              <span class="info-value">{{ userState.memberSince || '—' }}</span>
            </div>

            <div class="info-row">
              <span class="info-label">Account Role</span>
              <span class="info-value capitalize">{{ roleLabel }}</span>
            </div>
          </div>
        </div>

        <!-- Account settings -->
        <div class="card-panel">
          <div class="panel-header">
            <div class="panel-title-wrap">
              <div class="panel-icon-box slate">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="18" height="18">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <div>
                <h3 class="panel-title">Account & Notifications</h3>
                <p class="panel-sub">Security and what we contact you about</p>
              </div>
            </div>
          </div>

          <div class="settings-list">
            <div class="settings-row">
              <div class="settings-copy">
                <span class="settings-title">Password</span>
                <span class="settings-hint">Change the password you sign in with.</span>
              </div>
              <button type="button" class="panel-action-btn" @click="openPasswordModal">
                Change
              </button>
            </div>

            <div v-for="row in PREFERENCE_ROWS" :key="row.key" class="settings-row">
              <div class="settings-copy">
                <span class="settings-title">{{ row.label }}</span>
                <span class="settings-hint">{{ row.hint }}</span>
              </div>
              <label class="switch">
                <input
                  type="checkbox"
                  :checked="preferences[row.key]"
                  :aria-label="row.label"
                  @change="updatePreference(row.key, $event.target.checked)"
                />
                <span class="switch-track"><span class="switch-thumb"></span></span>
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Membership Tier & Recent Reservations -->
      <div class="grid-right-col">
        <!-- Membership Card -->
        <div class="card-panel membership-highlight-panel">
          <div class="panel-header">
            <div class="panel-title-wrap">
              <div class="panel-icon-box gold">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="18" height="18">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                </svg>
              </div>
              <div>
                <h3 class="panel-title">Membership Status</h3>
                <p class="panel-sub">
                  {{ activeMembership ? 'Your current plan' : 'No active plan' }}
                </p>
              </div>
            </div>
            <span v-if="activeMembership" class="badge-plan-active">Active</span>
          </div>

          <div class="membership-box-inner">
            <template v-if="activeMembership">
              <div class="plan-hero">
                <div class="plan-type">{{ activeMembership.plan_name || 'Membership' }}</div>
                <p class="plan-desc">
                  {{ activeMembership.plan_benefits || 'Member privileges on court bookings.' }}
                </p>
              </div>
              <div class="plan-perks-list">
                <div v-if="activeMembership.plan_discount_percentage" class="perk-item">
                  <span class="perk-check">✓</span>
                  <span>{{ activeMembership.plan_discount_percentage }}% off every court booking</span>
                </div>
                <div class="perk-item">
                  <span class="perk-check">✓</span>
                  <span>Started {{ formatDate(activeMembership.start_date) }}</span>
                </div>
                <div class="perk-item">
                  <span class="perk-check">✓</span>
                  <span>Renews or expires {{ formatDate(activeMembership.end_date) }}</span>
                </div>
              </div>
            </template>

            <div v-else class="plan-hero">
              <div class="plan-type">Pay as you go</div>
              <p class="plan-desc">
                You book courts at the standard rate. A membership adds a booking
                discount and guaranteed slots.
              </p>
            </div>

            <div class="plan-footer-actions">
              <router-link to="/member/membership" class="btn-plan-action">
                {{ activeMembership ? 'Manage membership' : 'View membership plans' }}
              </router-link>
            </div>
          </div>
        </div>

        <!-- Recent Bookings Overview -->
        <div class="card-panel">
          <div class="panel-header">
            <div class="panel-title-wrap">
              <div class="panel-icon-box purple">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="18" height="18">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
              <div>
                <h3 class="panel-title">Your Reservations</h3>
                <p class="panel-sub">Recent court bookings</p>
              </div>
            </div>
            <router-link to="/member/my-bookings" class="panel-action-btn">
              View All
            </router-link>
          </div>

          <div v-if="bookingsState.length === 0" class="empty-bookings-box">
            <span class="empty-icon">🎾</span>
            <p class="empty-title">No upcoming reservations</p>
            <p class="empty-sub">Ready for a game? Reserve a court in seconds.</p>
            <router-link to="/member/book-court" class="btn-quick-book">
              Book a Court
            </router-link>
          </div>

          <div v-else class="compact-bookings-list">
            <div
              v-for="b in bookingsState.slice(0, 3)"
              :key="b.id"
              class="compact-booking-card"
            >
              <div class="booking-card-left">
                <span class="court-title">{{ b.courtName }}</span>
                <span class="time-title">{{ b.dateLabel }} • {{ b.timeSlot }}</span>
              </div>
              <span class="badge-booking-status" :class="(b.status || 'confirmed').toLowerCase()">
                {{ b.status }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. Edit Profile Modal -->
    <div v-if="isEditProfileOpen" class="modal-backdrop" @click.self="closeEditProfileModal">
      <div class="modal-card">
        <div class="modal-card-header">
          <div>
            <h3 class="modal-title">Edit Profile Details</h3>
            <p class="modal-sub">Update your account information</p>
          </div>
          <button @click="closeEditProfileModal" class="modal-close-btn" aria-label="Close">
            ✕
          </button>
        </div>

        <form @submit.prevent="saveProfile" class="modal-form">
          <div class="form-group">
            <label class="form-label">Full Name <span class="req">*</span></label>
            <input
              v-model="editForm.name"
              type="text"
              required
              placeholder="e.g. Alex Morgan"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Email Address <span class="req">*</span></label>
            <input
              v-model="editForm.email"
              type="email"
              required
              placeholder="e.g. alex@example.com"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Phone Number</label>
            <input
              v-model="editForm.phone"
              type="tel"
              placeholder="e.g. +91 98765 43210"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="pf-dob">Date of Birth</label>
            <input id="pf-dob" v-model="editForm.dob" type="date" class="form-input" />
          </div>

          <div class="form-group">
            <label class="form-label" for="pf-gender">Gender</label>
            <select id="pf-gender" v-model="editForm.gender" class="form-input">
              <option value="">Prefer not to say</option>
              <option v-for="g in GENDERS" :key="g" :value="g">{{ g }}</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label" for="pf-address">Address</label>
            <input
              id="pf-address"
              v-model="editForm.address"
              type="text"
              placeholder="e.g. 12 Lake View Rd, Indiranagar"
              class="form-input"
            />
          </div>

          <div class="modal-footer">
            <button type="button" @click="closeEditProfileModal" class="btn-cancel">
              Cancel
            </button>
            <button type="submit" class="btn-save" :disabled="isSaving">
              <span v-if="isSaving">Saving...</span>
              <span v-else>Save Changes</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 4. Change Password Modal -->
    <div v-if="isPasswordOpen" class="modal-backdrop" @click.self="closePasswordModal">
      <div class="modal-card">
        <div class="modal-card-header">
          <div>
            <h3 class="modal-title">Change Password</h3>
            <p class="modal-sub">You will stay signed in on this device</p>
          </div>
          <button @click="closePasswordModal" class="modal-close-btn" aria-label="Close">✕</button>
        </div>

        <form @submit.prevent="submitPasswordChange" class="modal-form">
          <div class="form-group">
            <label class="form-label" for="pw-current">
              Current Password <span class="req">*</span>
            </label>
            <input
              id="pw-current"
              v-model="passwordForm.current"
              type="password"
              required
              autocomplete="current-password"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label class="form-label" for="pw-next">New Password <span class="req">*</span></label>
            <input
              id="pw-next"
              v-model="passwordForm.next"
              type="password"
              required
              minlength="8"
              autocomplete="new-password"
              class="form-input"
            />
            <p class="form-hint">At least 8 characters, and different from the current one.</p>
          </div>

          <div class="form-group">
            <label class="form-label" for="pw-confirm">
              Confirm New Password <span class="req">*</span>
            </label>
            <input
              id="pw-confirm"
              v-model="passwordForm.confirm"
              type="password"
              required
              autocomplete="new-password"
              class="form-input"
            />
          </div>

          <div class="modal-footer">
            <button type="button" @click="closePasswordModal" class="btn-cancel">Cancel</button>
            <button type="submit" class="btn-save" :disabled="isSavingPassword">
              {{ isSavingPassword ? 'Saving…' : 'Update Password' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Hidden file input for avatar upload -->
    <input
      type="file"
      ref="fileInput"
      class="hidden"
      accept="image/*"
      @change="onAvatarSelected"
    />
  </div>
</template>

<script setup>
/**
 * Member / front-desk profile.
 *
 * Everything on this screen is server state. It previously kept the phone
 * number and the avatar in localStorage, so both silently vanished on another
 * browser, and it read booking fields (`booking_date`, `court.name`) that
 * GET /bookings does not return, so every reservation rendered with today's
 * date. Profile details, preferences and the password now go through the
 * /auth/profile* endpoints.
 */
import { computed, inject, onMounted, reactive, ref, watch } from 'vue'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const toast = inject('toast', null)

const fileInput = ref(null)
const isSaving = ref(false)
const isSavingPassword = ref(false)
const loadError = ref('')

const GENDERS = ['Male', 'Female', 'Other', 'Prefer not to say']

// Avatars are stored as a data: URL on the user row, so the source image is
// downscaled to keep that row small (see MAX_AVATAR_CHARS on the server).
const AVATAR_MAX_PX = 320
const AVATAR_QUALITY = 0.82

const userState = ref({
  name: '',
  email: '',
  phone: '',
  role: 'player',
  memberSince: '',
  avatarUrl: '',
  dob: '',
  gender: '',
  address: '',
})

const preferences = reactive({
  notify_email: true,
  notify_sms: false,
  notify_push: true,
  profile_public: false,
})

const bookingsState = ref([])
const memberships = ref([])

// ---------------------------------------------------------------- helpers

function getInitials(name) {
  if (!name) return '—'
  const parts = name.trim().split(/\s+/).filter(Boolean)
  if (parts.length >= 2) return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase()
  return '—'
}

function formatMemberSince(createdAt) {
  if (!createdAt) return ''
  const d = new Date(createdAt)
  if (Number.isNaN(d.getTime())) return ''
  return d.toLocaleDateString('en-IN', { month: 'short', year: 'numeric' })
}

function formatDate(value) {
  if (!value) return ''
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return String(value)
  return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}

function apiMessage(err, fallback) {
  return err?.response?.data?.message || err?.message || fallback
}

const bookingsCount = computed(() => bookingsState.value.length)
const roleLabel = computed(() =>
  userState.value.role === 'front-desk' ? 'Staff Member' : 'Player',
)

/** The club this member actually plays at, taken from their bookings. */
const homeFacility = computed(() => {
  const names = bookingsState.value.map((b) => b.clubName).filter(Boolean)
  if (!names.length) return ''
  const tally = names.reduce((acc, n) => ({ ...acc, [n]: (acc[n] || 0) + 1 }), {})
  return Object.entries(tally).sort((a, b) => b[1] - a[1])[0][0]
})

const activeMembership = computed(
  () => memberships.value.find((m) => m.status === 'active') || null,
)

// ---------------------------------------------------------------- loading

function applyProfile(u) {
  if (!u) return
  userState.value = {
    name: u.name || '',
    email: u.email || '',
    phone: u.phone || '',
    role: u.role || 'player',
    memberSince: formatMemberSince(u.created_at),
    avatarUrl: u.avatar_url || '',
    dob: u.dob || '',
    gender: u.gender || '',
    address: u.address || '',
  }
  if (u.preferences) Object.assign(preferences, u.preferences)
}

async function loadProfile() {
  try {
    const { data } = await api.get('/auth/profile')
    applyProfile(data.user)
  } catch (err) {
    // Fall back to whatever the session already holds rather than blanking
    // the screen; the banner explains that details may be stale.
    applyProfile(auth.user)
    loadError.value = apiMessage(err, 'Could not load your profile.')
  }
}

async function loadBookings() {
  try {
    const { data } = await api.get('/bookings')
    bookingsState.value = (Array.isArray(data) ? data : []).map((b) => ({
      id: b.id,
      courtName: b.court_name || `Court #${b.court_id}`,
      clubName: b.club_name || '',
      date: b.date,
      dateLabel: formatDate(b.date),
      timeSlot: `${String(b.start_time || '').slice(0, 5)} - ${String(b.end_time || '').slice(0, 5)}`,
      status: b.status === 'active' ? 'Confirmed' : b.status,
    }))
  } catch {
    bookingsState.value = []
  }
}

async function loadMemberships() {
  try {
    const { data } = await api.get('/memberships/my-memberships')
    memberships.value = Array.isArray(data) ? data : []
  } catch {
    memberships.value = []
  }
}

async function reload() {
  loadError.value = ''
  await Promise.all([loadProfile(), loadBookings(), loadMemberships()])
}

onMounted(async () => {
  if (!auth.initialized || !auth.user) {
    try {
      await auth.restoreUser()
    } catch {
      /* the route guard handles an expired session */
    }
  }
  await reload()
})

watch(() => auth.user?.id, (id, previous) => {
  if (id && id !== previous) reload()
})

// ---------------------------------------------------------------- avatar

/** Draw the chosen file to a canvas at most AVATAR_MAX_PX on its long edge. */
function downscale(file) {
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

function triggerAvatarUpload() {
  fileInput.value?.click()
}

async function onAvatarSelected(event) {
  const file = event.target.files?.[0]
  event.target.value = ''
  if (!file) return
  if (!file.type.startsWith('image/')) {
    toast?.error('Please choose an image file.')
    return
  }
  try {
    const dataUrl = await downscale(file)
    const { data } = await api.put('/auth/profile/details', { avatar_url: dataUrl })
    applyProfile(data.user)
    auth.user = { ...auth.user, avatar_url: data.user.avatar_url }
    toast?.success('Profile photo updated.')
  } catch (err) {
    toast?.error(apiMessage(err, 'Could not update your photo.'))
  }
}

// ------------------------------------------------------------ edit profile

const isEditProfileOpen = ref(false)
const editForm = reactive({ name: '', email: '', phone: '', dob: '', gender: '', address: '' })

function openEditProfileModal() {
  Object.assign(editForm, {
    name: userState.value.name,
    email: userState.value.email,
    phone: userState.value.phone,
    dob: userState.value.dob,
    gender: userState.value.gender,
    address: userState.value.address,
  })
  isEditProfileOpen.value = true
}

function closeEditProfileModal() {
  isEditProfileOpen.value = false
}

async function saveProfile() {
  const name = editForm.name.trim()
  const email = editForm.email.trim()
  if (!name) {
    toast?.error('Please enter your full name.')
    return
  }
  if (!email) {
    toast?.error('Please enter your email address.')
    return
  }

  isSaving.value = true
  try {
    // Email is the login identity and is not editable through the details
    // endpoint, so it goes through the profile endpoint instead.
    if (email !== userState.value.email) {
      await auth.updateProfile({ name, email })
    }

    const { data } = await api.put('/auth/profile/details', {
      name,
      phone: editForm.phone.trim(),
      dob: editForm.dob || '',
      gender: editForm.gender || '',
      address: editForm.address.trim(),
    })
    applyProfile(data.user)
    auth.user = { ...auth.user, ...data.user }
    isEditProfileOpen.value = false
    toast?.success('Profile updated.')
  } catch (err) {
    toast?.error(apiMessage(err, 'Could not save your profile.'))
  } finally {
    isSaving.value = false
  }
}

// --------------------------------------------------------- change password

const isPasswordOpen = ref(false)
const passwordForm = reactive({ current: '', next: '', confirm: '' })

function openPasswordModal() {
  passwordForm.current = ''
  passwordForm.next = ''
  passwordForm.confirm = ''
  isPasswordOpen.value = true
}

function closePasswordModal() {
  isPasswordOpen.value = false
}

async function submitPasswordChange() {
  if (passwordForm.next !== passwordForm.confirm) {
    toast?.error('The new passwords do not match.')
    return
  }
  isSavingPassword.value = true
  try {
    await api.post('/auth/change-password', {
      current_password: passwordForm.current,
      new_password: passwordForm.next,
    })
    isPasswordOpen.value = false
    toast?.success('Password changed.')
  } catch (err) {
    toast?.error(apiMessage(err, 'Could not change your password.'))
  } finally {
    isSavingPassword.value = false
  }
}

// ------------------------------------------------------------- preferences

const PREFERENCE_ROWS = [
  { key: 'notify_email', label: 'Email notifications',
    hint: 'Booking confirmations, receipts and club announcements.' },
  { key: 'notify_sms', label: 'SMS notifications',
    hint: 'Text reminders shortly before a slot starts.' },
  { key: 'notify_push', label: 'In-app alerts',
    hint: 'Live updates in the notification bell.' },
  { key: 'profile_public', label: 'Public profile',
    hint: 'Let other members see your name when you join an event.' },
]

async function updatePreference(key, value) {
  const previous = preferences[key]
  preferences[key] = value
  try {
    const { data } = await api.put('/auth/preferences', { [key]: value })
    if (data.user?.preferences) Object.assign(preferences, data.user.preferences)
  } catch (err) {
    preferences[key] = previous
    toast?.error(apiMessage(err, 'Could not save that preference.'))
  }
}
</script>


<style scoped>
.player-profile-view {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
}

/* --- HERO CARD --- */
.profile-hero-card {
  position: relative;
  background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4338ca 100%);
  border-radius: 1.5rem;
  padding: 2.25rem;
  color: #ffffff;
  overflow: hidden;
  box-shadow: 0 20px 40px -15px rgba(49, 46, 129, 0.35);
  margin-bottom: 2rem;
}

.hero-cover-pattern {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(rgba(255, 255, 255, 0.12) 1px, transparent 1px);
  background-size: 20px 20px;
  opacity: 0.6;
  pointer-events: none;
}

.hero-inner {
  position: relative;
  z-index: 1;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 2rem;
}

.avatar-col {
  flex-shrink: 0;
}

.avatar-box {
  position: relative;
  width: 96px;
  height: 96px;
  border-radius: 1.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
  border: 3px solid rgba(255, 255, 255, 0.2);
}

.avatar-image {
  width: 100%;
  height: 100%;
  border-radius: 1.35rem;
  object-fit: cover;
}

.avatar-initials {
  width: 100%;
  height: 100%;
  border-radius: 1.35rem;
  background: linear-gradient(135deg, #6366f1, #818cf8);
  display: grid;
  place-items: center;
  font-size: 2.2rem;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.02em;
}

.avatar-camera-btn {
  position: absolute;
  bottom: -4px;
  right: -4px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #ffffff;
  color: #4338ca;
  border: none;
  display: grid;
  place-items: center;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
  transition: transform 0.2s ease, background 0.2s ease;
}

.avatar-camera-btn:hover {
  transform: scale(1.1);
  background: #f8fafc;
}

.hero-info-col {
  flex: 1;
  min-width: 260px;
}

.name-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 0.35rem;
}

.user-display-name {
  margin: 0;
  font-size: 1.85rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: #ffffff;
}

.role-pill {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 0.25rem 0.65rem;
  background: rgba(255, 255, 255, 0.16);
  border-radius: 999px;
  color: #e0e7ff;
}

.status-pill {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  background: rgba(16, 185, 129, 0.22);
  color: #6ee7b7;
  border: 1px solid rgba(16, 185, 129, 0.4);
}

.user-email-text {
  margin: 0 0 1.25rem;
  font-size: 0.92rem;
  color: #c7d2fe;
}

/* Metrics Bar */
.metrics-bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.25rem;
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  padding: 0.75rem 1.25rem;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.08);
  width: fit-content;
}

.metric-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.metric-icon-wrap {
  width: 34px;
  height: 34px;
  border-radius: 0.65rem;
  display: grid;
  place-items: center;
}

.metric-icon-wrap.blue {
  background: rgba(99, 102, 241, 0.3);
  color: #a5b4fc;
}

.metric-icon-wrap.emerald {
  background: rgba(16, 185, 129, 0.3);
  color: #6ee7b7;
}

.metric-icon-wrap.violet {
  background: rgba(168, 85, 247, 0.3);
  color: #d8b4fe;
}

.metric-num {
  display: block;
  font-size: 0.95rem;
  font-weight: 800;
  color: #ffffff;
  line-height: 1.1;
}

.metric-lbl {
  display: block;
  font-size: 0.72rem;
  color: #cbd5e1;
  font-weight: 500;
}

.metric-divider {
  width: 1px;
  height: 24px;
  background: rgba(255, 255, 255, 0.15);
}

.hero-actions-col {
  flex-shrink: 0;
}

.btn-edit-hero {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #ffffff;
  color: #312e81;
  font-weight: 700;
  font-size: 0.9rem;
  padding: 0.75rem 1.4rem;
  border-radius: 0.85rem;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
  transition: all 0.2s ease;
}

.btn-edit-hero:hover {
  background: #f1f5f9;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.2);
}

/* --- 2-COLUMN GRID --- */
.profile-content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.75rem;
}

@media (max-width: 900px) {
  .profile-content-grid {
    grid-template-columns: 1fr;
  }
}

.card-panel {
  background: #ffffff;
  border-radius: 1.25rem;
  padding: 1.75rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
  margin-bottom: 1.75rem;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f1f5f9;
}

.panel-title-wrap {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.panel-icon-box {
  width: 38px;
  height: 38px;
  border-radius: 0.75rem;
  background: #eef2ff;
  color: #4f46e5;
  display: grid;
  place-items: center;
}

.panel-icon-box.gold {
  background: #fef3c7;
  color: #d97706;
}

.panel-icon-box.purple {
  background: #f3e8ff;
  color: #9333ea;
}

.panel-title {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 800;
  color: #1e293b;
  letter-spacing: -0.02em;
}

.panel-sub {
  margin: 0.15rem 0 0;
  font-size: 0.78rem;
  color: #64748b;
}

.panel-action-btn {
  font-size: 0.82rem;
  font-weight: 700;
  color: #4f46e5;
  background: #eef2ff;
  border: none;
  padding: 0.4rem 0.85rem;
  border-radius: 0.55rem;
  cursor: pointer;
  text-decoration: none;
  transition: background 0.2s ease;
}

.panel-action-btn:hover {
  background: #e0e7ff;
}

/* Info Rows List */
.info-rows-list {
  display: flex;
  flex-direction: column;
  gap: 0.95rem;
}

.info-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.65rem 0.85rem;
  background: #f8fafc;
  border-radius: 0.75rem;
}

.info-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #64748b;
}

.info-value {
  font-size: 0.9rem;
  font-weight: 700;
  color: #1e293b;
}

.info-value.text-muted {
  color: #94a3b8;
  font-weight: 500;
}

.badge-facility {
  background: #eff6ff;
  color: #2563eb;
  padding: 0.2rem 0.65rem;
  border-radius: 0.45rem;
  font-size: 0.85rem;
  font-weight: 800;
}

/* Membership Highlight Panel */
.membership-highlight-panel {
  background: linear-gradient(180deg, #ffffff 0%, #faf5ff 100%);
  border-color: #e9d5ff;
}

.badge-plan-active {
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: #dcfce7;
  color: #16a34a;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
}

.plan-hero {
  margin-bottom: 1.25rem;
}

.plan-type {
  font-size: 1.35rem;
  font-weight: 800;
  color: #581c87;
  letter-spacing: -0.02em;
}

.plan-desc {
  margin: 0.25rem 0 0;
  font-size: 0.85rem;
  color: #6b21a8;
  line-height: 1.4;
}

.plan-perks-list {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  margin-bottom: 1.5rem;
}

.perk-item {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-size: 0.85rem;
  color: #334155;
  font-weight: 600;
}

.perk-check {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #f3e8ff;
  color: #9333ea;
  font-size: 0.75rem;
  font-weight: 800;
  display: grid;
  place-items: center;
}

.plan-footer-actions {
  display: flex;
}

.btn-plan-action {
  display: block;
  width: 100%;
  text-align: center;
  padding: 0.75rem;
  background: linear-gradient(135deg, #7c3aed, #6d28d9);
  color: #ffffff;
  font-weight: 700;
  font-size: 0.88rem;
  border-radius: 0.75rem;
  text-decoration: none;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25);
  transition: all 0.2s ease;
}

.btn-plan-action:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(124, 58, 237, 0.35);
}

/* Compact Bookings List */
.empty-bookings-box {
  text-align: center;
  padding: 1.5rem 1rem;
}

.empty-icon {
  font-size: 2.25rem;
  display: block;
  margin-bottom: 0.5rem;
}

.empty-title {
  margin: 0;
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
}

.empty-sub {
  margin: 0.25rem 0 1rem;
  font-size: 0.82rem;
  color: #64748b;
}

.btn-quick-book {
  display: inline-block;
  padding: 0.6rem 1.25rem;
  background: #4f46e5;
  color: #ffffff;
  font-weight: 700;
  font-size: 0.85rem;
  border-radius: 0.65rem;
  text-decoration: none;
}

.compact-bookings-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.compact-booking-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.85rem 1rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.85rem;
}

.court-title {
  display: block;
  font-size: 0.88rem;
  font-weight: 700;
  color: #1e293b;
}

.time-title {
  display: block;
  font-size: 0.75rem;
  color: #64748b;
  margin-top: 0.15rem;
}

.badge-booking-status {
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  background: #dbeafe;
  color: #1e40af;
}

.badge-booking-status.cancelled {
  background: #fee2e2;
  color: #b91c1c;
}

.badge-booking-status.completed {
  background: #f1f5f9;
  color: #475569;
}

/* --- MODAL --- */
.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 999;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(4px);
  display: grid;
  place-items: center;
  padding: 1rem;
}

.modal-card {
  width: 100%;
  max-width: 480px;
  background: #ffffff;
  border-radius: 1.25rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  overflow: hidden;
  animation: modalPop 0.25s ease-out;
}

@keyframes modalPop {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(8px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.modal-title {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 800;
  color: #0f172a;
}

.modal-sub {
  margin: 0.15rem 0 0;
  font-size: 0.8rem;
  color: #64748b;
}

.modal-close-btn {
  background: #f1f5f9;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  font-size: 0.85rem;
  color: #64748b;
  cursor: pointer;
  transition: background 0.2s ease;
}

.modal-close-btn:hover {
  background: #e2e8f0;
  color: #0f172a;
}

.modal-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.15rem;
}

.form-label {
  display: block;
  font-size: 0.82rem;
  font-weight: 700;
  color: #334155;
  margin-bottom: 0.35rem;
}

.form-label .req {
  color: #ef4444;
}

.form-input {
  width: 100%;
  padding: 0.7rem 0.9rem;
  border: 1.5px solid #cbd5e1;
  border-radius: 0.65rem;
  font-size: 0.9rem;
  color: #0f172a;
  outline: none;
  transition: border-color 0.2s ease;
}

.form-input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.disabled-input {
  background: #f8fafc;
  color: #64748b;
  font-weight: 600;
  cursor: not-allowed;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  background: repeating-linear-gradient(90deg, #1e293b, #1e293b 1px, transparent 1px, transparent 5px);
}

.barcode-mock .bar.long {
  background: repeating-linear-gradient(90deg, #1e293b, #1e293b 3px, transparent 3px, transparent 7px);
}

.barcode-num {
  font-family: monospace;
  font-size: 0.75rem;
  color: #64748b;
  letter-spacing: 0.2em;
}

.hidden {
  display: none;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes scaleUp {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(14px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive Overrides */
@media (max-width: 1100px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .bookings-layout {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .events-layout {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .main-content {
    padding-top: 6rem;
    padding-bottom: 4rem;
  }

  .page-heading {
    margin-bottom: 2rem;
  }

  .block-header h3 {
    font-size: 1.4rem;
  }
}

@media (max-width: 576px) {
  .container {
    width: min(100% - 1.25rem, 1200px);
  }

  .bookings-layout,
  .events-layout {
    grid-template-columns: 1fr;
  }

  .badges-grid {
    grid-template-columns: 1fr;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .modal-form {
    padding: 1.25rem;
  }
}

/* --- Load error banner --- */
.profile-alert {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 1.25rem;
  padding: 0.85rem 1.1rem;
  border-radius: 0.85rem;
  background: #fff0f1;
  border: 1px solid #f3c9cd;
  color: #a3323f;
  font-size: 0.85rem;
}
.profile-alert-retry {
  border: 1px solid #e3aeb4;
  background: #fff;
  color: #a3323f;
  border-radius: 0.5rem;
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 650;
  cursor: pointer;
}

/* --- Account settings rows --- */
.panel-icon-box.slate {
  background: #eef2f7;
  color: #4b5a70;
}
.settings-list {
  display: flex;
  flex-direction: column;
}
.settings-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.95rem 0;
  border-bottom: 1px solid #eef1f6;
}
.settings-row:last-child {
  border-bottom: none;
}
.settings-copy {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 0;
}
.settings-title {
  font-size: 0.875rem;
  font-weight: 650;
  color: #1e293b;
}
.settings-hint {
  font-size: 0.75rem;
  color: #78849a;
  line-height: 1.45;
}

/* --- Toggle switch --- */
.switch {
  position: relative;
  flex-shrink: 0;
  display: inline-flex;
  cursor: pointer;
}
.switch input {
  position: absolute;
  opacity: 0;
  width: 100%;
  height: 100%;
  margin: 0;
  cursor: pointer;
}
.switch-track {
  display: block;
  width: 42px;
  height: 24px;
  border-radius: 999px;
  background: #d5dce7;
  transition: background 0.2s ease;
}
.switch-thumb {
  display: block;
  width: 18px;
  height: 18px;
  margin: 3px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.25);
  transition: transform 0.2s ease;
}
.switch input:checked + .switch-track {
  background: #4f46e5;
}
.switch input:checked + .switch-track .switch-thumb {
  transform: translateX(18px);
}
.switch input:focus-visible + .switch-track {
  outline: 2px solid #718fff;
  outline-offset: 2px;
}

.form-hint {
  margin: 0.35rem 0 0;
  font-size: 0.72rem;
  color: #78849a;
}
</style>
