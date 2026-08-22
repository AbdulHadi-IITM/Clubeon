<template>
  <div class="profile-page">
    <Navbar />

    <main class="main-content">
      <div class="container">
        <!-- Eyebrow & Title Section -->
        <div class="page-heading">
          <p class="eyebrow">{{ pageHeading.eyebrow }}</p>
          <h2>{{ pageHeading.title }}</h2>
          <p class="lede">{{ pageHeading.lede }}</p>
        </div>

        <!-- 1. Header Card (Full Width) -->
        <ProfileHeader
          :user="userState"
          :stats="statsState"
          @edit-avatar="triggerAvatarUpload"
        />

        <!-- Role Quick Actions Bar -->
        <div class="role-bar mb-8">
          <div class="flex items-center justify-between flex-wrap gap-4 p-4 rounded-2xl bg-white border border-slate-200/80 shadow-sm">
            <div class="flex items-center gap-3">
              <span class="relative flex h-2.5 w-2.5">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </span>
              <span class="text-xs font-bold uppercase tracking-wider text-slate-400">Current Role:</span>
              <span class="rounded-full px-3 py-1 text-xs font-extrabold" :class="roleBadgeClass">{{ roleLabel }}</span>
            </div>
            <div class="flex items-center gap-2 flex-wrap">
              <button v-for="act in roleQuickActions" :key="act.label" @click="router.push(act.to)" class="rounded-xl border border-slate-200 bg-slate-50/80 px-3.5 py-2 text-xs font-bold text-slate-700 hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-600 transition shadow-sm">
                {{ act.label }}
              </button>
            </div>
          </div>
        </div>

        <!-- 2. Dual Column Layout (Info & Membership / Settings & Achievements) -->
        <div class="dashboard-grid">
          <!-- Left: Info Card & Settings -->
          <div class="grid-column">
            <ProfileInfoCard
              :info="userState"
              @edit="openEditProfileModal"
            />
            <SettingsPanel
              @action="handleSettingsAction"
            />
          </div>

          <!-- Right: Membership Card & Achievements -->
          <div class="grid-column">
            <MembershipCard
              :membership="membershipState"
              @renew="renewMembership"
            />

            <!-- Achievements Box -->
            <div class="achievements-card">
              <div class="card-header">
                <div class="header-icon-box">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="20" height="20">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                  </svg>
                </div>
                <h3>Your Achievements</h3>
              </div>
              <div class="badges-grid">
                <div v-for="badge in badgesState" :key="badge.title">
                  <AchievementBadge :badge="badge" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. Recent Bookings (Grid of Booking Cards) -->
        <section class="section-block">
          <div class="block-header">
            <h3>Recent Bookings</h3>
            <span class="view-all-link">Showing active reservations</span>
          </div>
          <div v-if="bookingsState.length === 0" class="empty-state">
            <p>No bookings scheduled. Reserve a court now!</p>
          </div>
          <div v-else class="items-grid bookings-layout">
            <div v-for="booking in bookingsState" :key="booking.id">
              <BookingCard
                :booking="booking"
                @view="viewBookingDetails"
                @cancel="confirmCancelBooking"
              />
            </div>
          </div>
        </section>

        <!-- 4. Upcoming Events (Grid of Event Cards) -->
        <section class="section-block">
          <div class="block-header">
            <h3>Upcoming Events</h3>
            <span class="view-all-link">Matches, training and leagues</span>
          </div>
          <div v-if="eventsState.length === 0" class="empty-state">
            <p>No upcoming events currently scheduled.</p>
          </div>
          <div v-else class="items-grid events-layout">
            <div v-for="event in eventsState" :key="event.id">
              <EventCard
                :event="event"
                @click-action="handleEventAction"
              />
            </div>
          </div>
        </section>

        <!-- 5. Logout Button (Large Center) -->
        <div class="logout-container">
          <button @click="handleLogout" class="logout-btn" aria-label="Sign out of your account">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="20" height="20">
              <path stroke-linecap="round" stroke-linejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Sign Out from ClubDash
          </button>
        </div>
      </div>
    </main>

    <FooterSection />

    <!-- MODAL OVERLAYS (Interactive Features) -->
    <!-- Edit Profile Modal -->
    <div v-if="isEditProfileOpen" class="modal-overlay" role="dialog" aria-modal="true">
      <div class="modal-card">
        <div class="modal-header">
          <h3>Edit Personal Details</h3>
          <button @click="closeEditProfileModal" class="close-btn" aria-label="Close modal">×</button>
        </div>
        <form @submit.prevent="saveProfile" class="modal-form">
          <div class="form-row">
            <div class="form-group">
              <label for="edit-name">Full Name</label>
              <input type="text" id="edit-name" v-model="editForm.name" required />
            </div>
            <div class="form-group">
              <label for="edit-email">Email Address</label>
              <input type="email" id="edit-email" v-model="editForm.email" required />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="edit-phone">Phone Number</label>
              <input type="text" id="edit-phone" v-model="editForm.phone" required />
            </div>
            <div class="form-group">
              <label for="edit-dob">Date of Birth</label>
              <input type="text" id="edit-dob" v-model="editForm.dob" required />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="edit-gender">Gender</label>
              <select id="edit-gender" v-model="editForm.gender">
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label for="edit-address">Home Address</label>
            <input type="text" id="edit-address" v-model="editForm.address" required />
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeEditProfileModal" class="cancel-modal-btn">Cancel</button>
            <button type="submit" class="submit-modal-btn">Save Changes</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Booking Details Modal -->
    <div v-if="selectedBooking" class="modal-overlay" role="dialog" aria-modal="true">
      <div class="modal-card detail-modal">
        <div class="modal-header">
          <h3>Reservation Ticket</h3>
          <button @click="selectedBooking = null" class="close-btn">×</button>
        </div>
        <div class="ticket-body">
          <div class="ticket-main">
            <div class="ticket-logo">
              <span class="mark">C</span>
              <span>ClubDash Ticket</span>
            </div>
            <div class="ticket-status-badge" :class="selectedBooking.status.toLowerCase()">
              {{ selectedBooking.status }}
            </div>
          </div>
          <div class="ticket-grid">
            <div>
              <span class="ticket-label">COURT / VENUE</span>
              <span class="ticket-val">{{ selectedBooking.courtName }}</span>
            </div>
            <div>
              <span class="ticket-label">DATE</span>
              <span class="ticket-val">{{ selectedBooking.date }}</span>
            </div>
            <div>
              <span class="ticket-label">TIME SLOT</span>
              <span class="ticket-val">{{ selectedBooking.timeSlot }}</span>
            </div>
            <div>
              <span class="ticket-label">BOOKED BY</span>
              <span class="ticket-val">{{ userState.name }}</span>
            </div>
          </div>
          <div class="barcode-mock">
            <div class="bar"></div>
            <div class="bar short"></div>
            <div class="bar long"></div>
            <div class="bar"></div>
            <div class="bar long"></div>
            <div class="bar short"></div>
            <span class="barcode-num">CD-{{ 1000 + selectedBooking.id }}</span>
          </div>
        </div>
        <div class="modal-actions">
          <button @click="selectedBooking = null" class="submit-modal-btn">Close Ticket</button>
        </div>
      </div>
    </div>

    <!-- Hidden file input for avatar edit -->
    <input type="file" ref="fileInput" class="hidden" accept="image/*" @change="onAvatarSelected" />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import Navbar from '@/components/NavBar.vue'
import FooterSection from '@/components/FooterSection.vue'
import ProfileHeader from '@/components/ProfileHeader.vue'
import ProfileInfoCard from '@/components/ProfileInfoCard.vue'
import MembershipCard from '@/components/MembershipCard.vue'
import BookingCard from '@/components/BookingCard.vue'
import EventCard from '@/components/EventCard.vue'
import AchievementBadge from '@/components/AchievementBadge.vue'
import SettingsPanel from '@/components/SettingsPanel.vue'
import { getSportImage } from '@/utils/sportImages'

const router = useRouter()
const auth = useAuthStore()
const fileInput = ref(null)
const loading = ref(true)

// Role-based Heading Meta
const pageHeading = computed(() => {
  const role = auth.user?.role
  if (role === 'owner') {
    return {
      eyebrow: 'Admin Portal',
      title: 'Club Administrator Profile',
      lede: 'Manage your club facility profile, view system overview, and navigate administration tools.'
    }
  } else if (role === 'front-desk' || role === 'staff') {
    return {
      eyebrow: 'Staff Operations',
      title: 'Staff Member Profile',
      lede: 'View your operational assignment, daily booking desk, and member attendance logs.'
    }
  }
  return {
    eyebrow: 'Member Dashboard',
    title: 'Member Profile',
    lede: 'Manage your club membership details, active bookings, tournament registrations, and account settings.'
  }
})

const roleLabel = computed(() => {
  const role = auth.user?.role
  if (role === 'owner') return 'Club Owner & Admin'
  if (role === 'front-desk' || role === 'staff') return 'Front Desk Staff'
  return 'Club Member'
})

const roleBadgeClass = computed(() => {
  const role = auth.user?.role
  if (role === 'owner') return 'bg-amber-100 text-amber-800'
  if (role === 'front-desk' || role === 'staff') return 'bg-sky-100 text-sky-800'
  return 'bg-indigo-100 text-indigo-800'
})

const roleQuickActions = computed(() => {
  const role = auth.user?.role
  if (role === 'owner') {
    return [
      { label: 'Admin Dashboard', to: '/admin' },
      { label: 'Manage Courts', to: '/admin' },
      { label: 'Manage Events', to: '/admin' }
    ]
  } else if (role === 'front-desk' || role === 'staff') {
    return [
      { label: 'Staff Dashboard', to: '/staff/dashboard' },
      { label: 'Daily Bookings', to: '/staff/bookings' },
      { label: 'Event Check-In', to: '/staff/events' },
      { label: 'Attendance Log', to: '/staff/attendance' }
    ]
  }
  return [
    { label: 'Book a Court', to: '/member/book-court' },
    { label: 'Browse Events', to: '/member/events' },
    { label: 'My Bookings', to: '/member/my-booking' },
    { label: 'Membership Plans', to: '/member/memberships' }
  ]
})

// 1. User State
const userState = ref({
  name: '',
  email: '',
  phone: '',
  dob: '',
  gender: 'Male',
  address: '',
  membershipType: 'Standard',
  memberSince: '2026',
  avatarUrl: ''
})

// 2. Statistics State
const statsState = ref({
  bookings: 0,
  eventsJoined: 0,
  membershipStatus: 'Active'
})

// 3. Membership Details State
const membershipState = ref({
  type: 'Standard',
  expiryDate: 'December 31, 2026',
  status: 'Active',
  benefits: [
    'Online facility court reservations',
    'Club event access and match participation',
    'AI assistant powered court scheduling',
    'Personal schedule & match tracking'
  ]
})

// 4. Bookings State
const bookingsState = ref([])

// 5. Events State
const eventsState = ref([])

// 6. Achievements Badges State
const badgesState = ref([
  {
    title: 'Club Member',
    description: 'Active member of ClubDash',
    icon: '🏸',
    isUnlocked: true,
    unlockDate: '2026',
    color: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)'
  },
  {
    title: 'Match Ready',
    description: 'Booked and reserved courts',
    icon: '⚡',
    isUnlocked: true,
    unlockDate: '2026',
    color: 'linear-gradient(135deg, #10b981 0%, #059669 100%)'
  },
  {
    title: 'Tournament Participant',
    description: 'Joined club tournaments & leagues',
    icon: '🏆',
    isUnlocked: false,
    unlockDate: '',
    color: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
  },
  {
    title: 'VIP Access',
    description: 'Premium club privileges',
    icon: '💎',
    isUnlocked: true,
    unlockDate: '2026',
    color: 'linear-gradient(135deg, #a78bfa 0%, #7c3aed 100%)'
  }
])

// Interactive Modal states
const isEditProfileOpen = ref(false)
const selectedBooking = ref(null)
const editForm = reactive({
  name: '',
  email: '',
  phone: '',
  dob: '',
  gender: 'Male',
  address: ''
})

async function fetchProfileData() {
  loading.value = true
  if (!auth.user) {
    await auth.restoreUser()
  }

  const u = auth.user || {}
  userState.value = {
    name: u.name || 'Club Member',
    email: u.email || '',
    phone: u.phone || '+91 98765 43210',
    dob: u.dob || 'June 15, 2000',
    gender: u.gender || 'Male',
    address: u.address || 'Sports District, Chennai, India',
    membershipType: u.role === 'owner' ? 'Owner / Admin' : u.role === 'front-desk' ? 'Staff' : 'Active Member',
    memberSince: u.created_at ? new Date(u.created_at).toLocaleDateString('en-US', { month: 'long', year: 'numeric' }) : 'March 2026',
    avatarUrl: u.avatar_url || ''
  }

  // Setup membership card by role
  if (u.role === 'owner') {
    membershipState.value = {
      type: 'Club Owner & Admin',
      expiryDate: 'Lifetime Access',
      status: 'Active',
      benefits: [
        'Full administrative control over courts & operating schedules',
        'Manage club staff accounts and member roster',
        'Create and oversee club tournaments, events & registrations',
        'Real-time financial revenue and court occupancy analytics'
      ]
    }
  } else if (u.role === 'front-desk' || u.role === 'staff') {
    membershipState.value = {
      type: 'Staff Operational Pass',
      expiryDate: 'Active Staff Member',
      status: 'Active',
      benefits: [
        'Member check-in & court arrival verification',
        'Real-time court availability schedule lookup',
        'Attendance logging & front-desk queue management',
        'Event participant check-in and roster verification'
      ]
    }
  }

  // Fetch real Bookings
  try {
    const res = await api.get('/bookings')
    const bookings = Array.isArray(res.data) ? res.data : []
    bookingsState.value = bookings.map(b => ({
      id: b.id,
      courtName: b.court?.name || 'Main Arena Court',
      date: b.booking_date,
      timeSlot: `${(b.start_time || '09:00').substring(0, 5)} - ${(b.end_time || '10:00').substring(0, 5)}`,
      status: b.status ? (b.status.charAt(0).toUpperCase() + b.status.slice(1)) : 'Confirmed'
    }))
    statsState.value.bookings = bookingsState.value.length
  } catch (err) {
    console.warn('Could not load user bookings:', err)
  }

  // Fetch real Events
  try {
    const evRes = await api.get('/events')
    const events = Array.isArray(evRes.data) ? evRes.data : []
    eventsState.value = events.map(e => ({
      id: e.id,
      name: e.title,
      date: e.date,
      venue: e.venue || 'Club Arena',
      imageUrl: getSportImage(e.title || e.sport),
      category: e.type || 'Tournament',
      isRegistered: e.my_registration_status === 'registered'
    }))
    const registeredCount = eventsState.value.filter(e => e.isRegistered).length
    statsState.value.eventsJoined = registeredCount
    if (registeredCount > 0) {
      const b = badgesState.value.find(b => b.title === 'Tournament Participant')
      if (b) b.isUnlocked = true
    }
  } catch (err) {
    console.warn('Could not load events:', err)
  }

  // Fetch membership if member
  if (u.role === 'player' || !u.role) {
    try {
      const memRes = await api.get('/memberships/my-membership')
      if (memRes.data && memRes.data.plan) {
        membershipState.value = {
          type: memRes.data.plan.name || 'Premium Member',
          expiryDate: memRes.data.end_date || 'December 31, 2026',
          status: memRes.data.status === 'active' ? 'Active' : 'Active',
          benefits: [
            'Uncapped facility bookings across badminton, tennis and squash',
            'Early tournament reservation & member event discounts',
            'Complimentary training locker & gear checkroom access',
            'Access to AI club assistant and booking recommendations'
          ]
        }
      }
    } catch (e) {
      // Keep default
    }
  }

  loading.value = false
}

// Action Handlers
const triggerAvatarUpload = () => {
  if (fileInput.value) {
    fileInput.value.click()
  }
}

const onAvatarSelected = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      userState.value.avatarUrl = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const openEditProfileModal = () => {
  editForm.name = userState.value.name
  editForm.email = userState.value.email
  editForm.phone = userState.value.phone
  editForm.dob = userState.value.dob
  editForm.gender = userState.value.gender
  editForm.address = userState.value.address
  isEditProfileOpen.value = true
}

const closeEditProfileModal = () => {
  isEditProfileOpen.value = false
}

const saveProfile = () => {
  userState.value.name = editForm.name
  userState.value.email = editForm.email
  userState.value.phone = editForm.phone
  userState.value.dob = editForm.dob
  userState.value.gender = editForm.gender
  userState.value.address = editForm.address
  if (auth.user) {
    auth.user.name = editForm.name
    auth.user.phone = editForm.phone
  }
  isEditProfileOpen.value = false
  alert('Profile information updated successfully!')
}

const renewMembership = () => {
  if (auth.user?.role === 'owner' || auth.user?.role === 'front-desk') {
    router.push('/admin')
    return
  }
  router.push('/member/memberships')
}

const viewBookingDetails = (booking) => {
  selectedBooking.value = booking
}

const confirmCancelBooking = async (booking) => {
  if (confirm(`Are you sure you want to cancel your booking for "${booking.courtName}" on ${booking.date}?`)) {
    try {
      await api.delete(`/bookings/${booking.id}`)
    } catch (e) {
      console.warn(e)
    }
    const found = bookingsState.value.find(b => b.id === booking.id)
    if (found) {
      found.status = 'Cancelled'
      statsState.value.bookings = bookingsState.value.filter(b => b.status === 'Confirmed' || b.status === 'Completed').length
      alert('Booking cancelled successfully.')
    }
  }
}

const handleEventAction = (event) => {
  router.push({ name: 'member-event-details', params: { eventId: event.id } })
}

const handleSettingsAction = (action) => {
  switch (action) {
    case 'edit-profile':
      openEditProfileModal()
      break
    case 'change-password':
      alert('Password change dialog triggered.')
      break
    case 'notifications':
      alert('Notification preferences updated.')
      break
    case 'privacy':
      alert('Privacy settings saved.')
      break
    default:
      console.warn(`Action "${action}" is not supported.`)
  }
}

const handleLogout = async () => {
  if (confirm('Are you sure you want to log out from ClubDash?')) {
    await auth.logout()
    router.push({ name: 'login' })
  }
}

onMounted(() => {
  fetchProfileData()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Poppins:wght@600;700;800&display=swap');

.profile-page {
  min-height: 100vh;
  background:
    radial-gradient(circle at top left, rgba(79, 70, 229, 0.07), transparent 35%),
    radial-gradient(circle at right 22rem, rgba(249, 115, 22, 0.05), transparent 30%),
    #f8fafc;
  font-family: 'Inter', sans-serif;
  color: #0f172a;
}

.main-content {
  padding-top: 7rem;
  padding-bottom: 6rem;
}

.container {
  width: min(1200px, calc(100% - 2.5rem));
  margin: 0 auto;
}

.page-heading {
  margin-bottom: 2.75rem;
  animation: fadeUp 0.6s ease both;
}

.eyebrow {
  display: inline-flex;
  margin: 0 0 0.85rem;
  padding: 0.5rem 0.88rem;
  border-radius: 999px;
  background: rgba(79, 70, 229, 0.1);
  color: #4f46e5;
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

h2 {
  margin: 0;
  color: #0f172a;
  font-family: 'Poppins', sans-serif;
  font-size: clamp(2rem, 4vw, 3.2rem);
  line-height: 1.05;
  letter-spacing: -0.04em;
}

.lede {
  margin: 1.15rem 0 0;
  color: #64748b;
  font-size: 1.05rem;
  line-height: 1.75;
  max-width: 44rem;
}

/* Dashboard dual column grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 2rem;
  margin-bottom: 3.5rem;
}

.grid-column {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Achievements Container Inside Grid */
.achievements-card {
  background: #ffffff;
  border-radius: 1.5rem;
  border: 1px solid rgba(226, 232, 240, 0.8);
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.03);
  padding: 2rem;
  transition: all 0.3s ease;
}

.achievements-card:hover {
  border-color: rgba(79, 70, 229, 0.12);
  box-shadow: 0 16px 36px rgba(15, 23, 42, 0.05);
}

.achievements-card .card-header {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  margin-bottom: 1.75rem;
  padding-bottom: 1.15rem;
  border-bottom: 1px solid rgba(226, 232, 240, 0.6);
}

.header-icon-box {
  width: 2.35rem;
  height: 2.35rem;
  border-radius: 0.75rem;
  background: rgba(249, 115, 22, 0.08);
  color: #ea580c;
  display: grid;
  place-items: center;
}

.achievements-card h3 {
  margin: 0;
  font-family: 'Poppins', sans-serif;
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.02em;
}

.badges-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.15rem;
}

/* Block Content Layouts */
.section-block {
  margin-bottom: 3.5rem;
}

.block-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 1.75rem;
}

.block-header h3 {
  margin: 0;
  font-family: 'Poppins', sans-serif;
  font-size: 1.65rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.03em;
}

.view-all-link {
  font-size: 0.9rem;
  font-weight: 600;
  color: #4f46e5;
}

.items-grid {
  display: grid;
  gap: 1.5rem;
}

.bookings-layout {
  grid-template-columns: repeat(4, minmax(0, 1fr));
}

.events-layout {
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.empty-state {
  background: #ffffff;
  border: 2px dashed rgba(226, 232, 240, 0.9);
  padding: 3rem 2rem;
  text-align: center;
  border-radius: 1.5rem;
  color: #64748b;
  font-weight: 500;
}

/* Logout Actions */
.logout-container {
  display: flex;
  justify-content: center;
  margin-top: 4.5rem;
}

.logout-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.65rem;
  min-height: 3.5rem;
  padding: 1rem 2.25rem;
  border-radius: 999px;
  background: #ffffff;
  border: 1.5px solid rgba(239, 68, 68, 0.25);
  color: #dc2626;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  box-shadow: 0 8px 24px rgba(220, 38, 38, 0.02);
}

.logout-btn:hover {
  background: #dc2626;
  color: #ffffff;
  border-color: #dc2626;
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(220, 38, 38, 0.18);
}

.logout-btn:active {
  transform: translateY(0);
}

/* Interactive Modal Overlays styling */
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 2000;
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: grid;
  place-items: center;
  padding: 1.5rem;
  animation: fadeIn 0.3s ease;
}

.modal-card {
  background: #ffffff;
  border-radius: 1.75rem;
  border: 1px solid rgba(226, 232, 240, 0.8);
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.15);
  width: 100%;
  max-width: 38rem;
  overflow: hidden;
  animation: scaleUp 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(226, 232, 240, 0.6);
}

.modal-header h3 {
  margin: 0;
  font-family: 'Poppins', sans-serif;
  font-size: 1.35rem;
  font-weight: 700;
  color: #0f172a;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.75rem;
  color: #94a3b8;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  transition: color 0.2s ease;
}

.close-btn:hover {
  color: #4f46e5;
}

.modal-form {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.8rem 1rem;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  font-family: inherit;
  font-size: 0.95rem;
  color: #0f172a;
  background: #ffffff;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #4f46e5;
  box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1rem;
}

.cancel-modal-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  color: #475569;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-modal-btn:hover {
  background: #f8fafc;
}

.submit-modal-btn {
  padding: 0.75rem 1.75rem;
  border-radius: 0.75rem;
  border: none;
  background: #4f46e5;
  color: #ffffff;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}

.submit-modal-btn:hover {
  background: #4338ca;
}

/* Detail/Ticket Modal Specifics */
.detail-modal {
  max-width: 28rem;
}

.ticket-body {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.ticket-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding-bottom: 1.5rem;
  border-bottom: 2px dashed #e2e8f0;
  margin-bottom: 1.5rem;
}

.ticket-logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 700;
  color: #0f172a;
  font-size: 1rem;
}

.ticket-logo .mark {
  width: 1.75rem;
  height: 1.75rem;
  border-radius: 0.5rem;
  background: linear-gradient(135deg, #2563eb, #f97316);
  color: #ffffff;
  display: grid;
  place-items: center;
  font-size: 0.8rem;
}

.ticket-status-badge {
  display: inline-flex;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
}

.ticket-status-badge.confirmed {
  background: rgba(16, 185, 129, 0.1);
  color: #059669;
}

.ticket-status-badge.pending {
  background: rgba(245, 158, 11, 0.1);
  color: #d97706;
}

.ticket-status-badge.completed {
  background: rgba(59, 130, 246, 0.1);
  color: #2563eb;
}

.ticket-status-badge.cancelled {
  background: rgba(239, 68, 68, 0.1);
  color: #dc2626;
}

.ticket-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.5rem;
  width: 100%;
  text-align: left;
  margin-bottom: 2rem;
}

.ticket-label {
  display: block;
  font-size: 0.725rem;
  font-weight: 700;
  color: #94a3b8;
  letter-spacing: 0.05em;
  margin-bottom: 0.25rem;
}

.ticket-val {
  font-size: 0.95rem;
  font-weight: 600;
  color: #334155;
  word-break: break-word;
}

.barcode-mock {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.35rem;
  padding: 1.15rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.85rem;
  width: 100%;
}

.barcode-mock .bar {
  width: 90%;
  height: 2.25rem;
  background: repeating-linear-gradient(90deg, #1e293b, #1e293b 2px, transparent 2px, transparent 6px);
}

.barcode-mock .bar.short {
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
