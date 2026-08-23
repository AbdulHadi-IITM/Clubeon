<template>
  <div class="player-profile-view">
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
            <span class="role-pill">
              {{ userState.role === 'front-desk' ? 'Staff Member' : 'Player' }}
            </span>
            <span class="status-pill live">Active Member</span>
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
                <span class="metric-num">ClubDash</span>
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
                <span class="metric-num">{{ userState.memberSince || 'Recent' }}</span>
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
              <span class="info-label">Club Facility</span>
              <span class="info-value badge-facility">ClubDash</span>
            </div>

            <div class="info-row">
              <span class="info-label">Member Since</span>
              <span class="info-value">{{ userState.memberSince || 'Recent' }}</span>
            </div>

            <div class="info-row">
              <span class="info-label">Account Role</span>
              <span class="info-value capitalize">{{ userState.role || 'Player' }}</span>
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
                <p class="panel-sub">Active privileges at ClubDash</p>
              </div>
            </div>
            <span class="badge-plan-active">Active</span>
          </div>

          <div class="membership-box-inner">
            <div class="plan-hero">
              <div class="plan-type">Club Member</div>
              <p class="plan-desc">Access to full court bookings, event entries, and live notifications.</p>
            </div>
            <div class="plan-perks-list">
              <div class="perk-item">
                <span class="perk-check">✓</span>
                <span>Unlimited court availability booking</span>
              </div>
              <div class="perk-item">
                <span class="perk-check">✓</span>
                <span>Instant match notifications & event alerts</span>
              </div>
              <div class="perk-item">
                <span class="perk-check">✓</span>
                <span>Real-time booking management & ticket receipts</span>
              </div>
            </div>

            <div class="plan-footer-actions">
              <router-link to="/member/membership" class="btn-plan-action">
                View Membership Plans
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
                <span class="time-title">{{ b.date }} • {{ b.timeSlot }}</span>
              </div>
              <span class="badge-booking-status" :class="(b.status || 'confirmed').toLowerCase()">
                {{ b.status || 'Confirmed' }}
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
            <label class="form-label">Club Facility</label>
            <input
              type="text"
              value="ClubDash"
              disabled
              class="form-input disabled-input"
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
import { ref, reactive, watch, onMounted, inject, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useBookingStore } from '@/stores/bookings'

const router = useRouter()
const auth = useAuthStore()
const bookingStore = useBookingStore()
const toast = inject('toast', null)
const fileInput = ref(null)
const isSaving = ref(false)

function getInitials(name) {
  if (!name) return 'MB'
  const parts = name.trim().split(' ').filter(Boolean)
  if (parts.length >= 2) {
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
  } else if (parts.length === 1 && parts[0].length > 0) {
    return parts[0].slice(0, 2).toUpperCase()
  }
  return 'MB'
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

// 1. Dynamic User State
const userState = ref({
  name: '',
  email: '',
  phone: '',
  role: 'player',
  memberSince: 'Recent',
  avatarUrl: ''
})

function syncUser() {
  const u = auth.user
  if (!u) return
  userState.value.name = u.name || 'Member'
  userState.value.email = u.email || 'member@clubdash.com'
  userState.value.role = u.role || 'player'
  userState.value.memberSince = formatMemberSince(u.created_at)

  // Load clean phone
  const cleanPhone = (u.phone && u.phone !== '+91 98765 43210') ? u.phone : ''

  // Load extra preferences from localStorage if exists
  const userKey = `player_profile_${u.id || u.email}`
  const saved = localStorage.getItem(userKey)
  if (saved) {
    try {
      const parsed = JSON.parse(saved)
      userState.value.phone = cleanPhone || (parsed.phone && parsed.phone !== '+91 98765 43210' ? parsed.phone : '')
      userState.value.avatarUrl = parsed.avatarUrl || ''
    } catch (e) {
      userState.value.phone = cleanPhone
    }
  } else {
    userState.value.phone = cleanPhone
    userState.value.avatarUrl = ''
  }
}

watch(() => auth.user, () => syncUser(), { immediate: true, deep: true })

// 2. Real-time Bookings State
const bookingsState = ref([])
const bookingsCount = computed(() => bookingsState.value.length)

async function fetchUserBookings() {
  try {
    await bookingStore.loadBookings()
    bookingsState.value = (bookingStore.bookings || []).map(b => ({
      id: b.id,
      courtName: b.court?.name || `Court #${b.court_id}`,
      date: b.booking_date || new Date().toISOString().split('T')[0],
      timeSlot: `${b.start_time || '08:00'} - ${b.end_time || '09:00'}`,
      status: b.status ? b.status.charAt(0).toUpperCase() + b.status.slice(1) : 'Confirmed'
    }))
  } catch (e) {
    console.warn('Could not fetch bookings:', e)
  }
}

// 3. Edit Form State
const isEditProfileOpen = ref(false)
const editForm = reactive({
  name: '',
  email: '',
  phone: ''
})

onMounted(async () => {
  if (!auth.initialized || !auth.user) {
    try {
      await auth.restoreUser()
    } catch (e) {}
  }
  syncUser()
  await fetchUserBookings()
})

const triggerAvatarUpload = () => {
  if (fileInput.value) fileInput.value.click()
}

const onAvatarSelected = (event) => {
  const file = event.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = (e) => {
    userState.value.avatarUrl = e.target.result
    const userKey = `player_profile_${auth.user?.id || auth.user?.email || 'default'}`
    const saved = JSON.parse(localStorage.getItem(userKey) || '{}')
    localStorage.setItem(userKey, JSON.stringify({ ...saved, avatarUrl: userState.value.avatarUrl }))
    if (toast) toast.success('Avatar updated!')
  }
  reader.readAsDataURL(file)
}

const openEditProfileModal = () => {
  editForm.name = userState.value.name
  editForm.email = userState.value.email
  editForm.phone = userState.value.phone || ''
  isEditProfileOpen.value = true
}

const closeEditProfileModal = () => {
  isEditProfileOpen.value = false
}

const saveProfile = async () => {
  if (!editForm.name || !editForm.name.trim()) {
    if (toast) toast.error('Please enter your full name.')
    return
  }
  if (!editForm.email || !editForm.email.trim()) {
    if (toast) toast.error('Please enter a valid email address.')
    return
  }

  isSaving.value = true
  const newName = editForm.name.trim()
  const newEmail = editForm.email.trim()
  const newPhone = editForm.phone.trim()

  try {
    if (auth.isAuthenticated()) {
      await auth.updateProfile({
        name: newName,
        email: newEmail,
        phone: newPhone,
        facility: 'ClubDash'
      })
    } else if (auth.user) {
      auth.user.name = newName
      auth.user.email = newEmail
      auth.user.phone = newPhone
    }
  } catch (err) {
    console.warn('Backend profile update note:', err)
    if (toast && err?.response?.data?.message) {
      toast.error(err.response.data.message)
      isSaving.value = false
      return
    }
  } finally {
    isSaving.value = false
  }

  userState.value.name = newName
  userState.value.email = newEmail
  userState.value.phone = newPhone

  try {
    const userKey = `player_profile_${auth.user?.id || auth.user?.email || 'default'}`
    localStorage.setItem(userKey, JSON.stringify({
      phone: userState.value.phone,
      avatarUrl: userState.value.avatarUrl
    }))
  } catch (e) {}

  isEditProfileOpen.value = false
  if (toast) {
    toast.success('Profile details updated successfully! ✨')
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
</style>
