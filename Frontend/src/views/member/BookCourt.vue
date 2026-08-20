<template>
  <div class="space-y-6">
    <!-- =====================================================
         PAGE HEADING
    ====================================================== -->
    <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <h1 class="text-2xl font-bold gradient-text">Book a Court</h1>

        <p class="text-sm text-gray-500 mt-1">
          Find an available court and reserve your preferred time slot.
        </p>
      </div>

      <router-link
        to="/member/nearby-courts"
        class="btn-secondary inline-flex items-center justify-center gap-2"
      >
        <svg class="h-4 w-4 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
          />
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
          />
        </svg>
        Find nearby courts
      </router-link>
    </div>

    <!-- =====================================================
         FILTERS
    ====================================================== -->
    <div class="glass p-5">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <!-- Club -->
        <div>
          <label class="block text-xs text-gray-500 mb-2"> Select Club </label>

          <select
            v-model="selectedClubId"
            class="field"
            :disabled="booking"
            @change="handleClubChange"
          >
            <option value="">Select a club</option>

            <option v-for="club in clubs" :key="club.id" :value="club.id">
              {{ club.name }}
            </option>
          </select>
        </div>

        <!-- Date -->
        <div>
          <label class="block text-xs text-gray-500 mb-2"> Booking Date </label>

          <input
            v-model="selectedDate"
            type="date"
            :min="today"
            class="field"
            :disabled="booking"
            @change="loadAvailability"
          />
        </div>
      </div>

      <!-- Time Period -->
      <div class="mt-5">
        <label class="block text-xs text-gray-500 mb-3"> Time of Day </label>

        <div class="flex flex-wrap gap-2">
          <button
            v-for="period in periods"
            :key="period.value"
            type="button"
            class="period-button"
            :disabled="booking"
            :class="{
              'period-button-active': selectedPeriod === period.value,
            }"
            @click="selectPeriod(period.value)"
          >
            {{ period.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- =====================================================
         ERROR
    ====================================================== -->
    <div v-if="error" class="glass p-5 border border-red-500/20">
      <div class="flex items-start gap-3">
        <div class="w-9 h-9 rounded-lg bg-red-500/10 flex items-center justify-center shrink-0">
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

          <button type="button" class="text-xs text-primary-400 mt-2" @click="refreshData">
            Try Again
          </button>
        </div>
      </div>
    </div>

    <!-- =====================================================
         LOADING
    ====================================================== -->
    <div v-if="loading" class="glass p-12 text-center">
      <div class="loader mx-auto mb-4"></div>

      <p class="text-sm text-gray-500">Checking court availability...</p>
    </div>

    <!-- =====================================================
         NO CLUB SELECTED
    ====================================================== -->
    <div v-else-if="!selectedClubId" class="glass p-12 text-center">
      <div class="w-14 h-14 mx-auto rounded-xl bg-primary-500/10 flex items-center justify-center">
        <svg class="w-7 h-7 text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="1.5"
            d="M3 21h18M5 21V7l7-4 7 4v14M9 10h1m4 0h1M9 14h1m4 0h1"
          />
        </svg>
      </div>

      <h3 class="font-semibold text-gray-200 mt-4">Select a Club</h3>

      <p class="text-sm text-gray-500 mt-2">Choose a club to view its available courts.</p>
    </div>

    <!-- =====================================================
         COURTS
    ====================================================== -->
    <template v-else-if="!loading">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-lg font-semibold text-gray-200">Available Courts</h2>

          <p class="text-xs text-gray-500 mt-1">
            {{ activeCourts.length }}
            {{ activeCourts.length === 1 ? 'court' : 'courts' }}
            available for {{ formatDate(selectedDate) }}
          </p>
        </div>

        <button
          type="button"
          class="text-xs text-primary-400 hover:text-primary-300"
          :disabled="booking"
          @click="refreshData"
        >
          Refresh
        </button>
      </div>

      <!-- No Active Courts -->
      <div v-if="activeCourts.length === 0" class="glass p-12 text-center">
        <div
          class="w-14 h-14 mx-auto rounded-xl bg-primary-500/10 flex items-center justify-center"
        >
          <svg
            class="w-7 h-7 text-primary-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-width="1.5" d="M5 5h14v14H5zM5 12h14M12 5v14" />
          </svg>
        </div>

        <h3 class="font-semibold text-gray-300 mt-4">No Active Courts</h3>

        <p class="text-sm text-gray-500 mt-2">This club currently has no active courts.</p>
      </div>

      <!-- Court Grid -->
      <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
        <div
          v-for="court in activeCourts"
          :id="'court-card-' + court.id"
          :key="court.id"
          class="glass overflow-hidden transition-all duration-300"
          :class="{
            'ring-2 ring-indigo-500 shadow-lg': String(selectedSlot?.courtId) === String(court.id),
          }"
        >
          <!-- Sport-specific court visual -->
          <div class="court-image-shell">
            <img
              :src="getCourtImage(court)"
              :alt="`${formatSportName(court.sport_type)} court - ${court.name}`"
              class="court-image"
              loading="lazy"
              decoding="async"
              @error="handleCourtImageError"
            />
            <div class="court-image-badge">
              {{ formatSportName(court.sport_type) }}
            </div>
          </div>

          <div class="p-5">
            <!-- Court Header -->
            <div class="flex justify-between items-start gap-3">
              <div>
                <h3 class="font-semibold text-gray-200">
                  {{ court.name }}
                </h3>
              </div>

              <span
                class="px-2.5 py-1 rounded-full text-[11px] bg-emerald-500/10 text-emerald-400 whitespace-nowrap"
              >
                Available
              </span>
            </div>

            <!-- Slot Count -->
            <div class="flex justify-between mt-5 mb-3">
              <span class="text-xs text-gray-500"> Available Slots </span>

              <span class="text-xs text-gray-400"> {{ availableSlotCount(court) }} available </span>
            </div>

            <!-- =================================================
                 TIME SLOTS
            ================================================== -->
            <div v-if="getVisibleSlots(court).length > 0" class="grid grid-cols-2 gap-2">
              <button
                v-for="slot in getVisibleSlots(court)"
                :key="`${court.id}-${slot.start_time}-${slot.end_time}`"
                type="button"
                class="slot-button"
                :class="{
                  'slot-selected': isSelectedSlot(court, slot),

                  'slot-unavailable':
                    !slot.available || isSlotInPast(selectedDate, slot.start_time),
                }"
                :disabled="
                  !slot.available || isSlotInPast(selectedDate, slot.start_time) || booking
                "
                @click.stop.prevent="selectSlot(court, slot)"
              >
                <div>
                  {{ formatTime(slot.start_time) }}
                </div>

                <div class="text-[10px] opacity-50 mt-0.5">to {{ formatTime(slot.end_time) }}</div>

                <div
                  v-if="!slot.available || isSlotInPast(selectedDate, slot.start_time)"
                  class="text-[9px] mt-1 opacity-70"
                >
                  {{ slotStatusText(slot) }}
                </div>
              </button>
            </div>

            <!-- No Slots -->
            <div v-else class="rounded-lg border border-white/5 bg-white/[0.02] p-5 text-center">
              <p class="text-xs text-gray-500">No slots available for the selected time period.</p>
            </div>

            <!-- =================================================
                 BOOKING BUTTON
            ================================================== -->
            <button
              type="button"
              class="btn-primary w-full mt-5"
              :disabled="
                booking || !selectedSlot || String(selectedSlot?.courtId) !== String(court.id)
              "
              :class="{
                'opacity-50 cursor-not-allowed':
                  booking || !selectedSlot || String(selectedSlot?.courtId) !== String(court.id),
              }"
              @click.stop.prevent="bookCourt(court)"
            >
              <template v-if="booking && String(selectedSlot?.courtId) === String(court.id)">
                Booking...
              </template>

              <template
                v-else-if="selectedSlot && String(selectedSlot?.courtId) === String(court.id)"
              >
                Book {{ formatTime(selectedSlot.start_time) }}
              </template>

              <template v-else> Select a Time Slot </template>
            </button>
          </div>
        </div>
      </div>
    </template>

    <!-- =====================================================
         SUCCESS MODAL
    ====================================================== -->
    <div
      v-if="successMessage"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 px-4"
      @click.self="closeSuccess"
    >
      <div class="glass max-w-md w-full p-7 text-center">
        <div
          class="w-14 h-14 mx-auto rounded-full bg-emerald-500/10 flex items-center justify-center"
        >
          <svg
            class="w-7 h-7 text-emerald-400"
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

        <h3 class="text-xl font-semibold text-white mt-4">Booking Confirmed</h3>

        <p class="text-sm text-gray-400 mt-2">
          {{ successMessage }}
        </p>

        <div class="grid grid-cols-2 gap-3 mt-6">
          <button type="button" class="btn-secondary" @click="closeSuccess">Book Another</button>

          <button type="button" class="btn-primary" @click="goToBookings">My Bookings</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref } from 'vue'

import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'
import { useBookingStore } from '@/stores/bookings'

import tennisCourtImage from '@/assets/courts/tennis.webp'
import badmintonCourtImage from '@/assets/courts/badminton.webp'
import basketballCourtImage from '@/assets/courts/basketball.webp'
import golfCourtImage from '@/assets/courts/golf.webp'
import footballCourtImage from '@/assets/courts/football.webp'
import pickleballCourtImage from '@/assets/courts/pickleball.webp'
import padelCourtImage from '@/assets/courts/padel.webp'
import squashCourtImage from '@/assets/courts/squash.webp'
import volleyballCourtImage from '@/assets/courts/volleyball.webp'
import multiPurposeCourtImage from '@/assets/courts/multi-purpose.webp'

const route = useRoute()
const router = useRouter()
const bookingStore = useBookingStore()

// =========================================================
// SPORT-SPECIFIC COURT IMAGES
// =========================================================

const courtImages = {
  tennis: tennisCourtImage,
  badminton: badmintonCourtImage,
  basketball: basketballCourtImage,
  golf: golfCourtImage,
  football: footballCourtImage,
  soccer: footballCourtImage,
  pickleball: pickleballCourtImage,
  padel: padelCourtImage,
  squash: squashCourtImage,
  volleyball: volleyballCourtImage,
  'multi-purpose': multiPurposeCourtImage,
  multipurpose: multiPurposeCourtImage,
}

function normalizeSportType(value) {
  return String(value || 'multi-purpose')
    .trim()
    .toLowerCase()
    .replace(/_/g, '-')
    .replace(/\s+/g, '-')
}

function getCourtImage(court) {
  const sport = normalizeSportType(court?.sport_type ?? court?.sport)
  return courtImages[sport] || multiPurposeCourtImage
}

function formatSportName(value) {
  const sport = normalizeSportType(value)
  if (sport === 'multi-purpose' || sport === 'multipurpose') {
    return 'Multi-purpose'
  }
  return sport
    .split('-')
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function handleCourtImageError(event) {
  if (event?.target) {
    event.target.onerror = null
    event.target.src = multiPurposeCourtImage
  }
}

// =========================================================
// STATE
// =========================================================

const clubs = ref([])
const courts = ref([])
const availability = ref([])

const selectedClubId = ref('')
const selectedDate = ref('')
const selectedPeriod = ref('all')
const selectedSlot = ref(null)

const loading = ref(false)
const booking = ref(false)

const error = ref('')
const successMessage = ref('')

const currentTime = ref(new Date())
let currentTimeInterval = null

// =========================================================
// TIME PERIODS
// =========================================================

const periods = [
  {
    label: 'All Day',
    value: 'all',
  },
  {
    label: 'Morning',
    value: 'morning',
  },
  {
    label: 'Afternoon',
    value: 'afternoon',
  },
  {
    label: 'Evening',
    value: 'evening',
  },
]

// =========================================================
// TODAY
// =========================================================

const today = computed(() => {
  const date = new Date()

  const year = date.getFullYear()

  const month = String(date.getMonth() + 1).padStart(2, '0')

  const day = String(date.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
})

// =========================================================
// ACTIVE COURTS
// =========================================================

const activeCourts = computed(() => {
  return courts.value.filter((court) => court.isActive)
})

// =========================================================
// NORMALIZE API LIST
// =========================================================

function normalizeList(data) {
  if (Array.isArray(data)) {
    return data
  }

  if (Array.isArray(data?.items)) {
    return data.items
  }

  if (Array.isArray(data?.clubs)) {
    return data.clubs
  }

  if (Array.isArray(data?.courts)) {
    return data.courts
  }

  if (Array.isArray(data?.data)) {
    return data.data
  }

  return []
}

// =========================================================
// NORMALIZE COURT
// =========================================================

function normalizeCourt(court) {
  const status = String(court.status ?? '').toLowerCase()

  return {
    ...court,

    id: court.id ?? court.court_id,

    name: court.name ?? court.court_name ?? `Court ${court.id ?? court.court_id ?? ''}`,

    sport_type: court.sport_type ?? court.sport ?? '',

    isActive: court.is_active !== false && court.active !== false && status !== 'inactive',

    price: court.price_per_hour ?? court.hourly_rate ?? court.price ?? null,
  }
}

// =========================================================
// LOAD CLUBS
// =========================================================

async function loadClubs() {
  try {
    error.value = ''

    const response = await api.get('/clubs')

    clubs.value = normalizeList(response.data)

    console.log('CLUBS:', clubs.value)
  } catch (err) {
    console.error('Failed to load clubs:', err)

    error.value = getApiError(err, 'Unable to load clubs.')
  }
}

// =========================================================
// LOAD COURTS
// =========================================================

async function loadCourts() {
  if (!selectedClubId.value) {
    courts.value = []
    return
  }

  try {
    error.value = ''

    const response = await api.get(`/clubs/${selectedClubId.value}/courts`)

    courts.value = normalizeList(response.data).map(normalizeCourt)

    console.log('COURTS:', courts.value)
  } catch (err) {
    console.error('Failed to load courts:', err)

    courts.value = []

    error.value = getApiError(err, 'Unable to load courts.')
  }
}

// =========================================================
// LOAD AVAILABILITY
// =========================================================

async function loadAvailability() {
  /*
   * Any refresh invalidates the old selected slot.
   */
  selectedSlot.value = null

  if (!selectedClubId.value || !selectedDate.value) {
    availability.value = []
    return
  }

  try {
    loading.value = true
    error.value = ''

    const response = await api.get('/availability/matrix', {
      params: {
        club_id: selectedClubId.value,

        date: selectedDate.value,
      },
    })

    console.log('AVAILABILITY API RESPONSE:', response.data)

    /*
     * Confirmed backend response:
     *
     * {
     *   courts: [
     *     {
     *       court_id: 1,
     *       court_name: "Tennis Court 1",
     *       slots: [...]
     *     }
     *   ]
     * }
     */
    availability.value = Array.isArray(response.data?.courts) ? response.data.courts : []

    console.log('AVAILABILITY COURTS:', availability.value)
  } catch (err) {
    console.error('Failed to load availability:', err)

    availability.value = []

    error.value = getApiError(err, 'Unable to load court availability.')
  } finally {
    loading.value = false
  }
}

// =========================================================
// CLUB CHANGE
// =========================================================

async function handleClubChange() {
  if (booking.value) {
    return
  }

  courts.value = []
  availability.value = []
  selectedSlot.value = null

  if (!selectedClubId.value) {
    return
  }

  loading.value = true

  try {
    await loadCourts()
    await loadAvailability()
  } finally {
    loading.value = false
  }
}

// =========================================================
// GET COURT AVAILABILITY
// =========================================================

function getCourtAvailability(courtId) {
  const courtAvailability = availability.value.find(
    (entry) => String(entry.court_id) === String(courtId),
  )

  if (!courtAvailability || !Array.isArray(courtAvailability.slots)) {
    return []
  }

  return courtAvailability.slots
}

// =========================================================
// NORMALIZE SLOT
// =========================================================

function normalizeSlot(slot) {
  const status = String(slot?.status ?? '').toLowerCase()

  const unavailableStatuses = [
    'booked',
    'blocked',
    'maintenance',
    'unavailable',
    'reserved',
    'inactive',
  ]

  const availableStatuses = ['available', 'free', 'open']

  const available = availableStatuses.includes(status) && !unavailableStatuses.includes(status)

  return {
    ...slot,

    start_time: slot?.start_time ?? '',

    end_time: slot?.end_time ?? '',

    status,

    reason: slot?.reason ?? null,

    available,
  }
}

// =========================================================
// ALL COURT SLOTS
// =========================================================

function getAllCourtSlots(court) {
  return getCourtAvailability(court.id)
    .map(normalizeSlot)
    .filter((slot) => slot.start_time && slot.end_time)
}

// =========================================================
// VISIBLE SLOTS
// =========================================================

function getVisibleSlots(court) {
  const slots = getAllCourtSlots(court)

  if (selectedPeriod.value === 'all') {
    return slots
  }

  return slots.filter((slot) => {
    const hour = Number(String(slot.start_time).split(':')[0])

    if (selectedPeriod.value === 'morning') {
      return hour < 12
    }

    if (selectedPeriod.value === 'afternoon') {
      return hour >= 12 && hour < 17
    }

    if (selectedPeriod.value === 'evening') {
      return hour >= 17
    }

    return true
  })
}

// =========================================================
// PAST SLOT CHECK
// =========================================================

function isSlotInPast(date, startTime) {
  if (!date || !startTime) return false

  const [hours, minutes] = String(startTime).split(':').map(Number)
  if (Number.isNaN(hours) || Number.isNaN(minutes)) return false

  const slotStart = new Date(`${String(date).slice(0, 10)}T00:00:00`)
  slotStart.setHours(hours, minutes, 0, 0)

  return slotStart <= currentTime.value
}

// =========================================================
// SELECT PERIOD
// =========================================================

function selectPeriod(period) {
  if (booking.value) {
    return
  }

  selectedPeriod.value = period

  /*
   * Clear old selected slot when changing filter.
   * This prevents accidentally booking a hidden slot.
   */
  selectedSlot.value = null
}

// =========================================================
// AVAILABLE SLOT COUNT
// =========================================================

function availableSlotCount(court) {
  return getVisibleSlots(court).filter(
    (slot) => slot.available && !isSlotInPast(selectedDate.value, slot.start_time),
  ).length
}

// =========================================================
// SLOT STATUS
// =========================================================

function slotStatusText(slot) {
  if (isSlotInPast(selectedDate.value, slot.start_time)) {
    return 'Past'
  }

  if (slot.available) {
    return 'Available'
  }

  if (slot.reason === 'admin_block') {
    return 'Blocked'
  }

  switch (slot.status) {
    case 'booked':
    case 'reserved':
      return 'Booked'

    case 'blocked':
      return 'Blocked'

    case 'maintenance':
      return 'Maintenance'

    default:
      return 'Unavailable'
  }
}

// =========================================================
// SELECT SLOT
// =========================================================

function selectSlot(court, slot) {
  /*
   * Prevent changing selection while
   * a booking POST is in progress.
   */
  if (booking.value) {
    return
  }

  if (!slot.available || isSlotInPast(selectedDate.value, slot.start_time)) {
    return
  }

  selectedSlot.value = {
    courtId: court.id,

    courtName: court.name,

    start_time: slot.start_time,

    end_time: slot.end_time,
  }
}

// =========================================================
// CHECK SELECTED SLOT
// =========================================================

function isSelectedSlot(court, slot) {
  return (
    String(selectedSlot.value?.courtId) === String(court.id) &&
    selectedSlot.value?.start_time === slot.start_time &&
    selectedSlot.value?.end_time === slot.end_time
  )
}

// =========================================================
// CREATE BOOKING
// =========================================================

async function bookCourt(court) {
  /*
   * CRITICAL DUPLICATE-SUBMIT GUARD
   *
   * The backend log previously showed:
   *
   * POST /bookings -> 201
   * POST /bookings -> 409
   *
   * This prevents a second request while
   * the first request is still running.
   */
  if (booking.value) {
    console.warn('Duplicate booking request prevented.')

    return
  }

  if (!selectedSlot.value || String(selectedSlot.value.courtId) !== String(court.id)) {
    return
  }

  if (isSlotInPast(selectedDate.value, selectedSlot.value.start_time)) {
    selectedSlot.value = null
    error.value = 'This time slot has already passed. Please select another slot.'
    return
  }

  /*
   * Copy selected slot BEFORE the request.
   *
   * This allows us to safely clear
   * selectedSlot after success.
   */
  const slot = {
    courtId: selectedSlot.value.courtId,

    courtName: selectedSlot.value.courtName,

    start_time: selectedSlot.value.start_time,

    end_time: selectedSlot.value.end_time,
  }

  const bookingDate = selectedDate.value

  /*
   * Set this BEFORE awaiting anything.
   * This blocks a rapid second click.
   */
  booking.value = true
  error.value = ''

  try {
    /*
     * IMPORTANT:
     *
     * Availability API returns:
     *
     * 13:45:00
     *
     * Booking backend expects:
     *
     * 13:45
     *
     * Therefore slice(0, 5).
     */
    const payload = {
      court_id: Number(court.id),

      booking_date: bookingDate,

      start_time: String(slot.start_time).slice(0, 5),

      end_time: String(slot.end_time).slice(0, 5),
    }

    console.log('BOOKING PAYLOAD:', payload)

    /*
     * EXACTLY ONE POST.
     */
    const createdBooking = await bookingStore.createBooking(payload)

    console.log('BOOKING CREATED:', createdBooking)

    /*
     * Build success message using the
     * original availability times.
     */
    successMessage.value =
      `${court.name} reserved for ` +
      `${formatTime(slot.start_time)} – ` +
      `${formatTime(slot.end_time)} on ` +
      `${formatDate(bookingDate)}.`

    /*
     * Clear selected slot.
     */
    selectedSlot.value = null

    /*
     * Refresh availability.
     *
     * This is a GET request, not another POST.
     *
     * The successfully booked slot should
     * now return as booked/unavailable.
     */
    await loadAvailability()
  } catch (err) {
    console.error('Booking failed:', err)

    const status = err?.response?.status

    /*
     * 409 means another booking already
     * occupies this time range.
     */
    if (status === 409) {
      error.value = 'This time slot is no longer available. Please select another slot.'

      selectedSlot.value = null

      /*
       * Refresh backend availability after
       * concurrency conflict.
       */
      await loadAvailability()

      return
    }

    /*
     * Backend validation errors.
     */
    if (status === 400) {
      error.value = getApiError(err, 'The booking information is invalid.')

      return
    }

    error.value = getApiError(err, 'Unable to create booking.')
  } finally {
    /*
     * Always unlock the booking button.
     */
    booking.value = false
  }
}

// =========================================================
// REFRESH
// =========================================================

async function refreshData() {
  if (booking.value || !selectedClubId.value) {
    return
  }

  loading.value = true
  error.value = ''

  try {
    await loadCourts()
    await loadAvailability()
  } finally {
    loading.value = false
  }
}

// =========================================================
// API ERROR MESSAGE
// =========================================================

function getApiError(err, fallback) {
  const data = err?.response?.data

  if (typeof data === 'string') {
    return data
  }

  return data?.message || data?.error || data?.msg || data?.detail || fallback
}

// =========================================================
// FORMAT TIME
// =========================================================

function formatTime(time) {
  if (!time) {
    return ''
  }

  const [hourString, minuteString] = String(time).split(':')

  const hour = Number(hourString)

  const period = hour >= 12 ? 'PM' : 'AM'

  const displayHour = hour % 12 || 12

  return `${displayHour}:` + `${minuteString || '00'} ` + period
}

// =========================================================
// FORMAT DATE
// =========================================================

function formatDate(date) {
  if (!date) {
    return ''
  }

  return new Intl.DateTimeFormat('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }).format(new Date(`${date}T00:00:00`))
}

// =========================================================
// SUCCESS MODAL
// =========================================================

function closeSuccess() {
  successMessage.value = ''
}

// =========================================================
// MY BOOKINGS
// =========================================================

function goToBookings() {
  successMessage.value = ''

  router.push({
    name: 'member-my-bookings',
  })
}

// =========================================================
// INITIAL LOAD
// =========================================================

onMounted(async () => {
  /*
   * Default to today's date.
   */
  selectedDate.value = today.value

  currentTime.value = new Date()
  currentTimeInterval = setInterval(() => {
    currentTime.value = new Date()
  }, 30000)

  /*
   * Load real clubs.
   */
  await loadClubs()

  const targetClubId = route.query.club_id || route.query.club
  const targetCourtId = route.query.court_id || route.query.court

  if (targetClubId && clubs.value.some((c) => String(c.id) === String(targetClubId))) {
    selectedClubId.value = Number(targetClubId) || targetClubId
    await handleClubChange()

    if (targetCourtId) {
      await nextTick()
      const targetEl = document.getElementById(`court-card-${targetCourtId}`)
      if (targetEl) {
        targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
    }
  } else if (clubs.value.length === 1) {
    selectedClubId.value = clubs.value[0].id
    await handleClubChange()
  }
})

onUnmounted(() => {
  if (currentTimeInterval) {
    clearInterval(currentTimeInterval)
    currentTimeInterval = null
  }
})
</script>

<style scoped>
/* Member Book Court — Midnight Sidebar + Soft Blue
   Functional/API code is unchanged. */

.field {
  width: 100%;
  min-height: 48px;
  border: 1px solid #dce4ef;
  border-radius: 12px;
  background: #fbfcff;
  padding: 0.75rem 0.9rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #172033;
  outline: none;
  transition:
    border-color 0.18s ease,
    box-shadow 0.18s ease,
    background 0.18s ease;
}
.field:hover {
  border-color: #c7d2e2;
  background: #fff;
}
.field:focus {
  border-color: #7c89e8;
  background: #fff;
  box-shadow: 0 0 0 4px rgba(79, 95, 215, 0.1);
}
.field:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}
.field option {
  background: #fff;
  color: #172033;
}

.period-button {
  min-height: 40px;
  border: 1px solid #dfe6f0;
  border-radius: 11px;
  background: #f8faff;
  padding: 0.55rem 1rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: #667085;
  transition: all 0.18s ease;
}
.period-button:hover:not(:disabled) {
  border-color: #bdc7ef;
  background: #fff;
  color: #3f4fc5;
  transform: translateY(-1px);
}
.period-button-active {
  border-color: #aeb8f4;
  background: #eef1ff;
  color: #4656cc;
  box-shadow: 0 4px 12px rgba(79, 95, 215, 0.08);
}

/* Court cards */
.glass {
  border: 1px solid #dfe6f0 !important;
  background: #fff !important;
  box-shadow: 0 10px 28px rgba(38, 55, 88, 0.055) !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  color: #172033;
}

/* Override legacy dark Tailwind utility colors inside this page. */
.glass .text-gray-200,
.glass .text-gray-300 {
  color: #172033 !important;
}
.glass .text-gray-400 {
  color: #526078 !important;
}
.glass .text-gray-500 {
  color: #667085 !important;
}
.glass .text-white {
  color: #172033 !important;
}
.glass .border-white\/5 {
  border-color: #e4e9f1 !important;
}
.glass .bg-white\/\[0\.02\] {
  background: #f8faff !important;
}

/* The old page looked "blurry" because disabled/unavailable slots used
   very low opacity. Keep every label crisp and encode state with color. */
.slot-button {
  min-height: 72px;
  border: 1px solid #bfe4d7;
  border-radius: 12px;
  background: #f0faf6;
  padding: 0.7rem 0.55rem;
  font-size: 0.75rem;
  font-weight: 700;
  color: #213047;
  opacity: 1;
  transition:
    border-color 0.16s ease,
    background 0.16s ease,
    box-shadow 0.16s ease,
    transform 0.16s ease;
}
.slot-button:hover:not(:disabled) {
  border-color: #69c4a5;
  background: #e8f7f1;
  box-shadow: 0 6px 15px rgba(21, 150, 111, 0.09);
  transform: translateY(-1px);
}
.slot-selected {
  border-color: #6574e5 !important;
  background: #e9edff !important;
  color: #3445c2 !important;
  box-shadow: 0 0 0 3px rgba(79, 95, 215, 0.09);
}
.slot-unavailable {
  border-color: #e1e6ee !important;
  background: #f4f6f9 !important;
  color: #9aa5b4 !important;
  opacity: 1 !important;
  cursor: not-allowed;
  box-shadow: none !important;
}
.slot-unavailable div {
  color: #9aa5b4 !important;
  opacity: 1 !important;
}
.slot-button > div:nth-child(2) {
  color: #758298;
  opacity: 1 !important;
}
.slot-selected > div:nth-child(2) {
  color: #6876d4 !important;
}

/* Available badge */
.bg-emerald-500\/10 {
  background: #e9f8f2 !important;
}
.text-emerald-400 {
  color: #12815f !important;
}

/* Court visual: subtle soft-blue header, not washed out. */
.bg-primary-500\/10 {
  background: linear-gradient(135deg, #eef1ff, #f6f8ff) !important;
}
.text-primary-400 {
  color: #4f5fd7 !important;
}

/* Primary booking action */
.btn-primary {
  min-height: 46px;
  border: 1px solid #4f5fd7 !important;
  border-radius: 12px !important;
  background: linear-gradient(135deg, #5969df, #4858cf) !important;
  color: #fff !important;
  font-weight: 800 !important;
  box-shadow: 0 8px 18px rgba(79, 95, 215, 0.16) !important;
  transition: all 0.18s ease;
}
.btn-primary:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 11px 22px rgba(79, 95, 215, 0.22) !important;
}
.btn-primary:disabled,
.btn-primary.opacity-50 {
  border-color: #dfe4ec !important;
  background: #eef1f6 !important;
  color: #8d99aa !important;
  opacity: 1 !important;
  box-shadow: none !important;
}

/* Secondary actions / success modal */
.btn-secondary {
  min-height: 44px;
  border: 1px solid #dce4ef !important;
  border-radius: 12px !important;
  background: #fff !important;
  color: #4d5a70 !important;
  font-weight: 750 !important;
}
.fixed .glass {
  border-radius: 20px !important;
  box-shadow: 0 30px 70px rgba(20, 32, 56, 0.22) !important;
}
.fixed.inset-0 {
  backdrop-filter: blur(4px);
}

/* Error */
.border-red-500\/20 {
  border-color: #f0cbd0 !important;
  background: #fffafa !important;
}
.text-red-400 {
  color: #c94c59 !important;
}
.bg-red-500\/10 {
  background: #fff0f1 !important;
}

/* Loader */
.loader {
  width: 30px;
  height: 30px;
  border: 3px solid #e3e8f0;
  border-top-color: #4f5fd7;
  border-radius: 9999px;
  animation: spin 0.75s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 767px) {
  .glass {
    border-radius: 16px !important;
  }
  .slot-button {
    min-height: 68px;
  }
}

/* Sport-specific court image: complete frame remains visible */
.court-image-shell {
  position: relative;
  width: 100%;
  height: 190px;
  overflow: hidden;
  background: #eef3f8;
  border-bottom: 1px solid #e5eaf1;
}

.court-image {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  image-rendering: auto;
}

.court-image-badge {
  position: absolute;
  left: 16px;
  bottom: 14px;
  z-index: 2;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(30, 41, 59, 0.88);
  color: #ffffff;
  font-size: 10px;
  font-weight: 700;
  line-height: 1;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  border: 1px solid rgba(255, 255, 255, 0.35);
  box-shadow: 0 3px 10px rgba(15, 23, 42, 0.14);
  backdrop-filter: blur(6px);
}

@media (max-width: 767px) {
  .court-image-shell {
    height: 175px;
  }
}

/* Restored compact court header hierarchy */
.court-name {
  margin: 0;
  color: #111827;
  font-size: 16px;
  font-weight: 650;
  line-height: 1.35;
  letter-spacing: -0.015em;
}

.court-status {
  flex-shrink: 0;
  padding: 6px 12px;
  border-radius: 999px;
  background: #e8f7f1;
  color: #07845f;
  font-size: 11px;
  font-weight: 600;
  line-height: 1;
}
</style>
