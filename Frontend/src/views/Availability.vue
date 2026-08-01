<template>
  <div class="min-h-screen relative">
    <div class="absolute inset-0 bg-gradient-to-br from-primary-900/20 via-gray-950 to-accent-900/20"></div>

    <div class="relative z-10 max-w-7xl mx-auto px-4 py-8">
      <div class="glass-strong p-8 mb-8" style="background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(139,92,246,0.08)); border-color: rgba(99,102,241,0.2);">
        <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-4">
          <div>
            <h1 class="text-3xl font-bold text-white mb-2">SportsClub - Court Availability</h1>
            <p class="text-gray-400">View our courts and pricing</p>
          </div>
          <div class="flex items-center gap-3">
            <router-link to="/login" class="btn-secondary text-sm">Sign In</router-link>
            <router-link to="/register" class="btn-primary text-sm">Register</router-link>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div class="lg:col-span-1 space-y-6">
          <div class="glass p-5">
            <h3 class="text-sm font-semibold text-gray-300 mb-3">Filter by Sport</h3>
            <div class="space-y-1.5">
              <button
                v-for="sport in sportTypes"
                :key="sport"
                @click="toggleSport(sport)"
                :class="[
                  'w-full text-left px-3 py-2 rounded-lg text-sm transition-all duration-200',
                  selectedSports.includes(sport)
                    ? 'bg-primary-500/15 text-primary-400 border border-primary-500/30'
                    : 'text-gray-400 hover:bg-white/[0.03] border border-transparent'
                ]"
              >
                {{ sport }}
              </button>
            </div>
            <button
              v-if="sportTypes.length > 0 && selectedSports.length > 0"
              @click="clearFilters"
              class="text-xs text-gray-500 hover:text-gray-400 mt-2 transition-colors"
            >
              Clear filters
            </button>
          </div>

          <div class="glass p-5">
            <h3 class="text-sm font-semibold text-gray-300 mb-3">Select Date</h3>
            <input
              type="date"
              :value="selectedDate"
              @input="selectedDate = $event.target.value"
              :min="today"
              class="input-field mb-4"
            />
            <Calendar :events="bookingEvents" @select="onCalendarSelect" />
          </div>
        </div>

        <div class="lg:col-span-3">
          <LoadingSpinner v-if="loading" text="Loading courts..." />

          <EmptyState
            v-else-if="filteredCourts.length === 0"
            title="No courts available"
            description="No courts match the selected filters. Try adjusting your sport filter."
          />

          <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div
              v-for="court in filteredCourts"
              :key="court.id"
              class="glass card-hover p-5"
            >
              <div class="flex items-start justify-between mb-4">
                <div>
                  <h3 class="text-lg font-semibold text-white">{{ court.name }}</h3>
                  <p class="text-sm text-primary-400 mt-0.5">{{ court.sportType }}</p>
                </div>
                <StatusBadge :status="court.isActive ? 'active' : 'inactive'" />
              </div>

              <div class="flex items-center gap-2 mb-4">
                <span class="text-2xl font-bold text-white">${{ court.pricePerHour }}</span>
                <span class="text-sm text-gray-500">/ hour</span>
              </div>

              <div class="border-t border-white/5 pt-4 mb-4">
                <h4 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
                  {{ selectedDate === today ? "Today's" : 'Booked' }} Slots
                </h4>
                <div v-if="courtBookings[court.id] && courtBookings[court.id].length > 0" class="space-y-1.5 max-h-32 overflow-y-auto">
                  <div
                    v-for="slot in courtBookings[court.id]"
                    :key="slot.id"
                    class="flex items-center gap-2 text-sm"
                  >
                    <div class="w-2 h-2 rounded-full flex-shrink-0" :class="slot.status === 'confirmed' ? 'bg-primary-500/50' : 'bg-gray-500/50'"></div>
                    <span class="text-gray-400">{{ slot.startTime }} - {{ slot.endTime }}</span>
                    <StatusBadge :status="slot.status" />
                  </div>
                </div>
                <p v-else class="text-sm text-gray-600">All slots available</p>
              </div>

              <router-link
                :to="{ name: 'QuickBook', query: { court: court.id, date: selectedDate } }"
                class="btn-primary w-full text-center block text-sm"
              >
                Quick Book
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCourtStore } from '../stores/courts'
import { useBookingStore } from '../stores/bookings'
import EmptyState from '../components/common/EmptyState.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import Calendar from '../components/common/Calendar.vue'
import StatusBadge from '../components/common/StatusBadge.vue'

const courtStore = useCourtStore()
const bookingStore = useBookingStore()

const loading = ref(true)
const selectedDate = ref('')
const selectedSports = ref([])

const today = computed(() => new Date().toISOString().split('T')[0])

const sportTypes = computed(() => courtStore.sportsTypes)

const filteredCourts = computed(() => {
  const active = courtStore.activeCourts
  if (selectedSports.value.length === 0) return active
  return active.filter((c) => selectedSports.value.includes(c.sportType))
})

const bookingEvents = computed(() => {
  const all = bookingStore.bookings.filter((b) => b.status !== 'cancelled' && b.status !== 'released')
  return all.map((b) => ({ date: b.date, label: b.courtId }))
})

const courtBookings = computed(() => {
  const date = selectedDate.value || today.value
  const map = {}
  const bookings = bookingStore.getBookingsByDate(date).filter((b) => b.status !== 'cancelled' && b.status !== 'released')
  filteredCourts.value.forEach((c) => {
    map[c.id] = bookings.filter((b) => b.courtId === c.id)
  })
  return map
})

function toggleSport(sport) {
  const idx = selectedSports.value.indexOf(sport)
  if (idx === -1) {
    selectedSports.value = [...selectedSports.value, sport]
  } else {
    selectedSports.value = selectedSports.value.filter((s) => s !== sport)
  }
}

function clearFilters() {
  selectedSports.value = []
}

function onCalendarSelect(dateStr) {
  selectedDate.value = dateStr
}

onMounted(() => {
  courtStore.load()
  bookingStore.load()
  selectedDate.value = today.value
  loading.value = false
})
</script>
