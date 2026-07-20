<template>
  <div class="profile-page">
    <Navbar />

    <main class="main-content">
      <div class="container">
        <!-- Eyebrow & Title Section -->
        <div class="page-heading">
          <p class="eyebrow">Dashboard</p>
          <h2>Member Profile</h2>
          <p class="lede">Manage your club membership details, active bookings, tournament registrations, and account settings.</p>
        </div>

        <!-- 1. Header Card (Full Width) -->
        <ProfileHeader 
          :user="userState" 
          :stats="statsState" 
          @edit-avatar="triggerAvatarUpload" 
        />

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
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import FooterSection from '@/components/FooterSection.vue'
import ProfileHeader from '@/components/ProfileHeader.vue'
import ProfileInfoCard from '@/components/ProfileInfoCard.vue'
import MembershipCard from '@/components/MembershipCard.vue'
import BookingCard from '@/components/BookingCard.vue'
import EventCard from '@/components/EventCard.vue'
import AchievementBadge from '@/components/AchievementBadge.vue'
import SettingsPanel from '@/components/SettingsPanel.vue'

const router = useRouter()
const fileInput = ref(null)

// 1. User State
const userState = ref({
  name: 'Varun Karthik',
  email: 'varun.karthik@example.com',
  phone: '+91 98765 43210',
  dob: 'June 15, 2000',
  gender: 'Male',
  address: '123 Playmaker Avenue, Sports District, Chennai, 600001',
  membershipType: 'Premium',
  memberSince: 'March 2025',
  avatarUrl: ''
})

// 2. Statistics State
const statsState = ref({
  bookings: 12,
  eventsJoined: 4,
  membershipStatus: 'Active'
})

// 3. Membership Details State
const membershipState = ref({
  type: 'Premium',
  expiryDate: 'December 31, 2026',
  status: 'Active',
  benefits: [
    'Uncapped facility bookings across badminton, tennis and squash',
    'Early event reservation & 15% tournament entry discounts',
    'Complimentary training locker & gear checkroom access',
    'Access to premium dashboards and training metrics'
  ]
})

// 4. Bookings State
const bookingsState = ref([
  {
    id: 1,
    courtName: 'Indoor Badminton Court A',
    date: 'July 24, 2026',
    timeSlot: '08:00 AM - 10:00 AM',
    status: 'Confirmed'
  },
  {
    id: 2,
    courtName: 'Premium Clay Tennis Court B',
    date: 'July 28, 2026',
    timeSlot: '04:00 PM - 06:00 PM',
    status: 'Pending'
  },
  {
    id: 3,
    courtName: 'Indoor Basketball Arena',
    date: 'July 15, 2026',
    timeSlot: '06:00 PM - 07:30 PM',
    status: 'Completed'
  },
  {
    id: 4,
    courtName: 'Indoor Badminton Court C',
    date: 'July 10, 2026',
    timeSlot: '09:00 AM - 10:30 AM',
    status: 'Cancelled'
  }
])

// 5. Events State
const eventsState = ref([
  {
    id: 1,
    name: 'Club Singles Squash Championship',
    date: 'August 08, 2026',
    venue: 'Squash Courts 1 & 2',
    imageUrl: 'https://images.unsplash.com/photo-1587280501635-68a0e82cd5ff?w=600&auto=format&fit=crop&q=80',
    category: 'Tournament',
    isRegistered: true
  },
  {
    id: 2,
    name: 'Weekend Tennis Pro Coaching',
    date: 'August 19, 2026',
    venue: 'Main Tennis Clay Arena',
    imageUrl: 'https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=600&auto=format&fit=crop&q=80',
    category: 'Coaching',
    isRegistered: false
  },
  {
    id: 3,
    name: 'Inter-Club Basketball League Opener',
    date: 'September 02, 2026',
    venue: 'Outdoor Court 1',
    imageUrl: 'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=600&auto=format&fit=crop&q=80',
    category: 'League',
    isRegistered: false
  }
])

// 6. Achievements Badges State
const badgesState = ref([
  {
    title: 'Early Bird',
    description: 'Booked a slot before 07:00 AM',
    icon: '🌅',
    isUnlocked: true,
    unlockDate: 'Mar 15, 2025',
    color: 'linear-gradient(135deg, #fb923c 0%, #f97316 100%)'
  },
  {
    title: 'Tournament Winner',
    description: 'Placed 1st in any club league',
    icon: '🏆',
    isUnlocked: true,
    unlockDate: 'May 20, 2025',
    color: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)'
  },
  {
    title: '50 Bookings Milestone',
    description: 'Complete 50 court bookings',
    icon: '⚡',
    isUnlocked: false,
    unlockDate: '',
    color: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)'
  },
  {
    title: 'Premium Member',
    description: 'Subscribed to premium membership',
    icon: '💎',
    isUnlocked: true,
    unlockDate: 'Mar 10, 2025',
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
  isEditProfileOpen.value = false
  alert('Profile information updated successfully!')
}

const renewMembership = () => {
  if (membershipState.value.status === 'Active') {
    // Extends by 1 year
    membershipState.value.expiryDate = 'December 31, 2027'
    alert('Membership extended successfully until Dec 31, 2027!')
  } else {
    membershipState.value.status = 'Active'
    membershipState.value.expiryDate = 'December 31, 2026'
    statsState.value.membershipStatus = 'Active'
    alert('Membership renewed and activated successfully!')
  }
}

const viewBookingDetails = (booking) => {
  selectedBooking.value = booking
}

const confirmCancelBooking = (booking) => {
  if (confirm(`Are you sure you want to cancel your booking for "${booking.courtName}" on ${booking.date}?`)) {
    const found = bookingsState.value.find(b => b.id === booking.id)
    if (found) {
      found.status = 'Cancelled'
      statsState.value.bookings = bookingsState.value.filter(b => b.status === 'Confirmed' || b.status === 'Completed').length
      alert('Booking cancelled successfully.')
    }
  }
}

const handleEventAction = (event) => {
  const found = eventsState.value.find(e => e.id === event.id)
  if (found) {
    if (found.isRegistered) {
      alert(`Viewing details for: ${found.name}`)
    } else {
      found.isRegistered = true
      statsState.value.eventsJoined++
      alert(`Successfully registered for: ${found.name}!`)
    }
  }
}

const handleSettingsAction = (action) => {
  switch (action) {
    case 'edit-profile':
      openEditProfileModal()
      break
    case 'change-password':
      alert('Change password module triggered! (Mock Dialog)')
      break
    case 'notifications':
      alert('Notification preferences triggered! (Mock Dialog)')
      break
    case 'privacy':
      alert('Privacy settings triggered! (Mock Dialog)')
      break
    default:
      console.warn(`Action "${action}" is not supported.`)
  }
}

const handleLogout = () => {
  if (confirm('Are you sure you want to log out from ClubDash?')) {
    alert('Logging out...')
    router.push('/')
  }
}
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
