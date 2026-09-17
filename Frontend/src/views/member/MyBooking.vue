<template>
  <div class="space-y-6">
    <!-- =====================================================
         HEADER
    ====================================================== -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold gradient-text">My Bookings</h1>

        <p class="text-sm text-slate-500 mt-1">View and manage your court reservations.</p>
      </div>

      <button type="button" class="btn-primary" @click="goToBookCourt">+ Book a Court</button>
    </div>

    <!-- =====================================================
         STATS
    ====================================================== -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div class="glass p-5">
        <p class="text-xs text-slate-500">Upcoming</p>

        <p class="text-2xl font-bold text-slate-900 mt-2">
          {{ upcomingBookings.length }}
        </p>
      </div>

      <div class="glass p-5">
        <p class="text-xs text-slate-500">Past</p>

        <p class="text-2xl font-bold text-slate-900 mt-2">
          {{ pastBookings.length }}
        </p>
      </div>

      <div class="glass p-5">
        <p class="text-xs text-slate-500">Total</p>

        <p class="text-2xl font-bold text-slate-900 mt-2">
          {{ bookings.length }}
        </p>
      </div>
    </div>

    <!-- =====================================================
         FILTERS
    ====================================================== -->
    <div class="glass p-2 flex flex-wrap gap-2">
      <button
        v-for="tab in tabs"
        :key="tab.value"
        type="button"
        class="tab-button"
        :class="{
          'tab-active': activeTab === tab.value,
        }"
        @click="activeTab = tab.value"
      >
        {{ tab.label }}

        <span class="tab-count">
          {{ getTabCount(tab.value) }}
        </span>
      </button>
    </div>

    <!-- =====================================================
         ERROR
    ====================================================== -->
    <div v-if="error" class="glass p-5 border border-red-500/20">
      <div class="flex items-start gap-3">
        <div class="w-9 h-9 rounded-lg bg-red-500/10 flex items-center justify-center">
          <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 9v2m0 4h.01M5.07 19h13.86c1.54 0 2.5-1.67 1.73-3L13.73 4c-.77-1.33-2.69-1.33-3.46 0L3.34 16c-.77 1.33.19 3 1.73 3z"
            />
          </svg>
        </div>

        <div>
          <p class="text-sm text-red-400">
            {{ error }}
          </p>

          <button type="button" class="text-xs text-primary-400 mt-2" @click="loadBookings">
            Try Again
          </button>
        </div>
      </div>
    </div>

    <!-- =====================================================
         LOADING
    ====================================================== -->
    <SkeletonLoader v-if="loading" type="list" :count="3" />

    <!-- =====================================================
         EMPTY STATE
    ====================================================== -->
    <EmptyState
      v-else-if="filteredBookings.length === 0"
      icon="calendar"
      :title="emptyTitle"
      :description="emptyMessage"
      :action-label="activeTab !== 'past' ? 'Book a Court' : ''"
      @action="goToBookCourt"
    />

    <!-- =====================================================
         BOOKINGS
    ====================================================== -->
    <div v-else class="space-y-4">
      <article v-for="booking in filteredBookings" :key="booking.id" class="glass booking-card">
        <div class="p-5 sm:p-6">
          <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-5">
            <!-- =============================================
                 LEFT
            ============================================== -->
            <div class="flex gap-4 items-center">
              <img
                :src="getSportImage(booking.courtName || booking.sport)"
                :alt="booking.courtName"
                class="w-14 h-14 rounded-xl object-cover shadow-sm shrink-0 border border-slate-200"
              />

              <div>
                <div class="flex flex-wrap items-center gap-2">
                  <h3 class="font-semibold text-gray-100">
                    {{ booking.courtName }}
                  </h3>

                  <span class="status-badge" :class="statusClass(booking)">
                    {{ statusLabel(booking) }}
                  </span>

                  <span
                    v-if="booking.status === 'active'"
                    class="px-2.5 py-0.5 rounded-full text-[11px] font-bold"
                    :class="
                      booking.paymentStatus === 'completed'
                        ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                        : 'bg-amber-50 text-amber-700 border border-amber-200'
                    "
                  >
                    {{ booking.paymentStatus === 'completed' ? 'Paid' : 'Payment Pending' }}
                  </span>
                </div>

                <p v-if="booking.clubName" class="text-xs text-slate-500 mt-1">
                  {{ booking.clubName }}
                </p>

                <!-- Booking information -->
                <div class="flex flex-wrap gap-x-6 gap-y-2 mt-4">
                  <div>
                    <p class="text-[10px] uppercase tracking-wide text-gray-600">Date</p>

                    <p class="text-sm text-slate-700 mt-1">
                      {{ formatDate(booking.bookingDate) }}
                    </p>
                  </div>

                  <div>
                    <p class="text-[10px] uppercase tracking-wide text-gray-600">Time</p>

                    <p class="text-sm text-slate-700 mt-1">
                      {{ formatTime(booking.startTime) }}
                      –
                      {{ formatTime(booking.endTime) }}
                    </p>
                  </div>

                  <div>
                    <p class="text-[10px] uppercase tracking-wide text-gray-600">Court Fee</p>

                    <p class="text-sm text-slate-700 mt-1">₹{{ booking.amount }}</p>
                  </div>

                  <div>
                    <p class="text-[10px] uppercase tracking-wide text-gray-600">Booking ID</p>

                    <p class="text-sm text-slate-700 mt-1">#{{ booking.id }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- =============================================
                 ACTIONS
            ============================================== -->
            <div class="flex flex-col sm:flex-row gap-2">
              <button
                v-if="booking.status === 'active' && booking.paymentStatus !== 'completed'"
                type="button"
                class="btn-primary text-xs px-3.5 py-2 rounded-xl font-bold flex items-center justify-center gap-1.5"
                @click="
                  router.push({
                    name: 'member-checkout',
                    query: { payment_type: 'booking', reference_id: String(booking.id) },
                  })
                "
              >
                <span>Pay with Stripe</span>
              </button>

              <button
                type="button"
                class="detail-button"
                @click="
                  router.push({ name: 'member-booking-details', params: { bookingId: booking.id } })
                "
              >
                View Details
              </button>

              <button
                v-if="canRelease(booking)"
                type="button"
                class="release-button"
                :disabled="releasingId === booking.id"
                @click="openReleaseModal(booking)"
              >
                {{ releasingId === booking.id ? 'Releasing...' : 'Release Booking' }}
              </button>
            </div>
          </div>
        </div>
      </article>
    </div>

    <!-- =====================================================
         RELEASE CONFIRMATION
    ====================================================== -->
    <div
      v-if="bookingToRelease"
      class="fixed inset-0 z-50 bg-black/70 flex items-center justify-center px-4"
      @click.self="closeReleaseModal"
    >
      <div class="glass max-w-md w-full p-6">
        <div class="w-12 h-12 rounded-xl bg-red-500/10 flex items-center justify-center">
          <svg class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </div>

        <h3 class="text-lg font-semibold text-slate-900 mt-4">Release Booking?</h3>

        <p class="text-sm text-gray-400 mt-2">
          This will release your reservation for
          <span class="text-slate-800">
            {{ bookingToRelease.courtName }}
          </span>
          on
          <span class="text-slate-800">
            {{ formatDate(bookingToRelease.bookingDate) }} </span
          >.
        </p>

        <div class="grid grid-cols-2 gap-3 mt-6">
          <button
            type="button"
            class="btn-secondary"
            :disabled="releasingId !== null"
            @click="closeReleaseModal"
          >
            Keep Booking
          </button>

          <button
            type="button"
            class="danger-button"
            :disabled="releasingId !== null"
            @click="releaseBooking"
          >
            {{ releasingId !== null ? 'Releasing...' : 'Release' }}
          </button>
        </div>
      </div>
    </div>

    <!-- =====================================================
         SUCCESS MESSAGE
    ====================================================== -->
    <div
      v-if="successMessage"
      class="fixed bottom-6 right-6 z-50 max-w-sm glass p-4 border border-emerald-500/20"
    >
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-full bg-emerald-500/10 flex items-center justify-center">
          <svg
            class="w-4 h-4 text-emerald-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5 13l4 4L19 7"
            />
          </svg>
        </div>

        <p class="text-sm text-slate-700">
          {{ successMessage }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { useBookingStore } from '@/stores/bookings'
import { getSportImage } from '@/utils/sportImages'
import SkeletonLoader from '@/components/common/SkeletonLoader.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const router = useRouter()
const bookingStore = useBookingStore()
const { bookings: bookingRecords, loading, error } = storeToRefs(bookingStore)

// =========================================================
// STATE
// =========================================================

const bookings = computed(() => {
  return normalizeList(bookingRecords.value)
    .map(normalizeBooking)
    .filter((booking) => booking.id !== undefined && booking.id !== null)
    .sort(sortNewestFirst)
})

const activeTab = ref('upcoming')

const releasingId = ref(null)
const bookingToRelease = ref(null)

const successMessage = ref('')

// =========================================================
// TABS
// =========================================================

const tabs = [
  {
    label: 'Upcoming',
    value: 'upcoming',
  },

  {
    label: 'Past',
    value: 'past',
  },

  {
    label: 'All',
    value: 'all',
  },
]

// =========================================================
// NORMALIZE LIST
// =========================================================

function normalizeList(data) {
  if (Array.isArray(data)) {
    return data
  }

  if (Array.isArray(data?.bookings)) {
    return data.bookings
  }

  if (Array.isArray(data?.items)) {
    return data.items
  }

  if (Array.isArray(data?.data)) {
    return data.data
  }

  return []
}

// =========================================================
// NORMALIZE BOOKING
// =========================================================

function normalizeBooking(item) {
  const court = item.court ?? {}

  const club = item.club ?? {}

  return {
    raw: item,

    id: item.id ?? item.booking_id,

    courtId: item.court_id ?? court.id,

    courtName: item.court_name ?? court.name ?? `Court ${item.court_id ?? ''}`,

    clubId: item.club_id ?? club.id ?? court.club_id,

    clubName: item.club_name ?? club.name ?? court.club_name ?? '',

    bookingDate: item.booking_date ?? item.date ?? '',

    startTime: item.start_time ?? item.start ?? '',

    endTime: item.end_time ?? item.end ?? '',

    status: String(item.status ?? 'active').toLowerCase(),

    sport: item.sport_type ?? item.sport ?? court.sport_type ?? 'tennis',

    amount: item.amount ?? item.price ?? 500,

    paymentStatus: item.payment_status ?? 'pending',

    releasedAt: item.released_at ?? item.cancelled_at ?? null,
  }
}

// =========================================================
// LOAD BOOKINGS
// =========================================================

async function loadBookings() {
  try {
    await bookingStore.loadBookings()
  } catch (err) {
    console.error('Failed to load bookings:', err)
  }
}

// =========================================================
// DATE/TIME HELPERS
// =========================================================

function bookingDateTime(booking) {
  if (!booking.bookingDate) {
    return null
  }

  const time = String(booking.endTime || booking.startTime || '23:59').slice(0, 5)

  const value = new Date(`${booking.bookingDate}T${time}:00`)

  if (Number.isNaN(value.getTime())) {
    return null
  }

  return value
}

function bookingStartDateTime(booking) {
  if (!booking.bookingDate) {
    return null
  }

  const time = String(booking.startTime || '00:00').slice(0, 5)

  const value = new Date(`${booking.bookingDate}T${time}:00`)

  if (Number.isNaN(value.getTime())) {
    return null
  }

  return value
}

// =========================================================
// STATUS HELPERS
// =========================================================

function isInactive(booking) {
  return ['released', 'overridden'].includes(booking.status)
}

function isPast(booking) {
  if (isInactive(booking)) {
    return false
  }

  const end = bookingDateTime(booking)

  if (!end) {
    return false
  }

  return end < new Date()
}

function isUpcoming(booking) {
  if (isInactive(booking)) {
    return false
  }

  const end = bookingDateTime(booking)

  if (!end) {
    return false
  }

  return end >= new Date()
}

// =========================================================
// COMPUTED BOOKING GROUPS
// =========================================================

const upcomingBookings = computed(() => {
  return bookings.value.filter(isUpcoming)
})

const pastBookings = computed(() => {
  return bookings.value.filter(isPast)
})

const filteredBookings = computed(() => {
  if (activeTab.value === 'upcoming') {
    return bookings.value.filter(isUpcoming)
  }

  if (activeTab.value === 'past') {
    return bookings.value.filter(isPast)
  }

  return bookings.value
})

// =========================================================
// COUNTS
// =========================================================

function getTabCount(tab) {
  if (tab === 'upcoming') {
    return upcomingBookings.value.length
  }

  if (tab === 'past') {
    return pastBookings.value.length
  }

  return bookings.value.length
}

// =========================================================
// EMPTY TEXT
// =========================================================

const emptyTitle = computed(() => {
  if (activeTab.value === 'upcoming') {
    return 'No Upcoming Bookings'
  }

  if (activeTab.value === 'past') {
    return 'No Past Bookings'
  }

  return 'No Bookings Yet'
})

const emptyMessage = computed(() => {
  if (activeTab.value === 'upcoming') {
    return 'You do not have any upcoming court reservations.'
  }

  if (activeTab.value === 'past') {
    return 'Your past court reservations will appear here.'
  }

  return 'Reserve your first court to get started.'
})

// =========================================================
// RELEASE PERMISSION
// =========================================================

function canRelease(booking) {
  return booking.status === 'active'
}

// =========================================================
// RELEASE MODAL
// =========================================================

function openReleaseModal(booking) {
  if (!canRelease(booking)) {
    return
  }

  bookingToRelease.value = booking
}

function closeReleaseModal() {
  if (releasingId.value !== null) {
    return
  }

  bookingToRelease.value = null
}

// =========================================================
// RELEASE BOOKING
// =========================================================

async function releaseBooking() {
  const booking = bookingToRelease.value

  if (!booking) {
    return
  }

  if (releasingId.value !== null) {
    return
  }

  try {
    releasingId.value = booking.id

    await bookingStore.releaseBooking(booking.id)

    successMessage.value = 'Booking released successfully.'

    bookingToRelease.value = null

    window.setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (err) {
    console.error('Failed to release booking:', err)
  } finally {
    releasingId.value = null
  }
}

// =========================================================
// SORT
// =========================================================

function sortNewestFirst(a, b) {
  const first = bookingStartDateTime(a)

  const second = bookingStartDateTime(b)

  if (!first && !second) {
    return 0
  }

  if (!first) {
    return 1
  }

  if (!second) {
    return -1
  }

  return second.getTime() - first.getTime()
}

// =========================================================
// STATUS LABEL
// =========================================================

function statusLabel(booking) {
  switch (booking.status) {
    case 'active':
      return 'Active'

    case 'released':
      return 'Released'

    case 'overridden':
      return 'Overridden'

    default:
      return booking.status ? capitalize(booking.status) : 'Active'
  }
}

// =========================================================
// STATUS CLASS
// =========================================================

function statusClass(booking) {
  if (booking.status === 'released') {
    return 'status-released'
  }

  if (booking.status === 'overridden') {
    return 'status-overridden'
  }

  return 'status-active'
}

// =========================================================
// FORMAT DATE
// =========================================================

function formatDate(date) {
  if (!date) {
    return '—'
  }

  const value = new Date(`${date}T00:00:00`)

  if (Number.isNaN(value.getTime())) {
    return date
  }

  return new Intl.DateTimeFormat('en-IN', {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }).format(value)
}

// =========================================================
// FORMAT TIME
// =========================================================

function formatTime(time) {
  if (!time) {
    return '—'
  }

  const parts = String(time).split(':')

  const hour = Number(parts[0])

  const minute = parts[1] ?? '00'

  if (Number.isNaN(hour)) {
    return time
  }

  const period = hour >= 12 ? 'PM' : 'AM'

  const displayHour = hour % 12 || 12

  return `${displayHour}:` + `${minute} ` + period
}

// =========================================================
// CAPITALIZE
// =========================================================

function capitalize(value) {
  if (!value) {
    return ''
  }

  return value.charAt(0).toUpperCase() + value.slice(1)
}

// =========================================================
// NAVIGATION
// =========================================================

function goToBookCourt() {
  router.push({
    name: 'member-book-court',
  })
}

// =========================================================
// INITIAL LOAD
// =========================================================

onMounted(() => {
  loadBookings()
})
</script>

<style scoped>
.booking-card {
  transition:
    transform 0.2s ease,
    border-color 0.2s ease;
}

.booking-card:hover {
  transform: translateY(-1px);
}

.tab-button {
  display: inline-flex;

  align-items: center;

  gap: 0.45rem;

  padding: 0.6rem 0.9rem;

  border-radius: 0.65rem;

  font-size: 0.75rem;

  color: rgb(100 116 139);

  transition: 0.2s ease;
}

.tab-button:hover {
  color: rgb(15 23 42);

  background: rgb(248 250 252);
}

.tab-active {
  color: rgb(37 99 235);

  background: rgb(239 246 255);
}

.tab-count {
  min-width: 1.25rem;

  height: 1.25rem;

  padding: 0 0.35rem;

  display: inline-flex;

  align-items: center;

  justify-content: center;

  border-radius: 9999px;

  background: rgb(241 245 249);

  font-size: 0.65rem;
}

.status-badge {
  padding: 0.25rem 0.55rem;

  border-radius: 9999px;

  font-size: 0.65rem;

  font-weight: 500;
}

.status-active {
  color: rgb(52 211 153);

  background: rgb(16 185 129 / 0.1);
}

.status-overridden {
  color: rgb(251 191 36);

  background: rgb(245 158 11 / 0.1);
}

.status-released {
  color: rgb(248 113 113);

  background: rgb(239 68 68 / 0.1);
}

.detail-button {
  padding: 0.6rem 0.9rem;
  border-radius: 0.65rem;
  border: 1px solid rgb(99 102 241 / 0.18);
  color: rgb(67 56 202);
  background: rgb(238 242 255);
  font-size: 0.75rem;
  transition: 0.2s ease;
}
.detail-button:hover {
  background: rgb(224 231 255);
}
.release-button {
  padding: 0.6rem 0.9rem;

  border-radius: 0.65rem;

  border: 1px solid rgb(239 68 68 / 0.2);

  color: rgb(248 113 113);

  background: rgb(239 68 68 / 0.05);

  font-size: 0.75rem;

  transition: 0.2s ease;
}

.release-button:hover:not(:disabled) {
  background: rgb(239 68 68 / 0.1);

  border-color: rgb(239 68 68 / 0.35);
}

.release-button:disabled {
  opacity: 0.5;

  cursor: not-allowed;
}

.danger-button {
  padding: 0.65rem 1rem;

  border-radius: 0.65rem;

  background: rgb(220 38 38);

  color: #0f172a;

  font-size: 0.8rem;

  transition: 0.2s ease;
}

.danger-button:hover:not(:disabled) {
  background: rgb(239 68 68);
}

.danger-button:disabled {
  opacity: 0.5;

  cursor: not-allowed;
}

.loader {
  width: 30px;

  height: 30px;

  border: 3px solid rgb(226 232 240);

  border-top-color: rgb(129 140 248);

  border-radius: 9999px;

  animation: spin 0.75s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
