<!--
  Public court availability.

  Reachable at /public without signing in, so it uses only the anonymous
  endpoints: GET /clubs, GET /clubs/:id/courts and GET /availability/matrix.
-->
<template>
  <div class="availability-page">
    <header class="page-header">
      <div class="header-inner">
        <router-link :to="{ name: 'landing' }" class="brand" aria-label="Clubeon home">
          <BrandMark :size="38" />
          <span class="brand-text">Club<span class="brand-accent">eon</span></span>
        </router-link>
        <div class="header-actions">
          <router-link to="/login" class="btn-ghost">Sign in</router-link>
          <router-link to="/register" class="btn-solid">Get started</router-link>
        </div>
      </div>
    </header>

    <main class="page-body">
      <div class="intro">
        <p class="kicker">Live availability</p>
        <h1 class="title">Find an open court</h1>
        <p class="lede">
          Browse today's schedule across our clubs. Create a free account to reserve a slot.
        </p>
      </div>

      <section class="controls" aria-label="Filters">
        <div class="control">
          <label class="control-label" for="club-select">Club</label>
          <select id="club-select" v-model="selectedClubId" class="control-input" @change="loadMatrix">
            <option v-if="!clubs.length" value="">No clubs available</option>
            <option v-for="club in clubs" :key="club.id" :value="club.id">{{ club.name }}</option>
          </select>
        </div>

        <div class="control">
          <label class="control-label" for="date-input">Date</label>
          <input
            id="date-input"
            v-model="selectedDate"
            type="date"
            :min="today"
            class="control-input"
            @change="loadMatrix"
          />
        </div>

        <div v-if="sportOptions.length > 1" class="control control-grow">
          <span class="control-label">Sport</span>
          <div class="chip-row">
            <button
              type="button"
              class="chip"
              :class="{ 'chip-on': !selectedSport }"
              @click="selectedSport = ''"
            >
              All
            </button>
            <button
              v-for="sport in sportOptions"
              :key="sport"
              type="button"
              class="chip"
              :class="{ 'chip-on': selectedSport === sport }"
              @click="selectedSport = sport"
            >
              {{ labelForSport(sport) }}
            </button>
          </div>
        </div>
      </section>

      <p v-if="error" class="alert" role="alert">
        {{ error }}
        <button type="button" class="alert-retry" @click="reload">Retry</button>
      </p>

      <LoadingSpinner v-if="loading" text="Loading availability…" />

      <EmptyState
        v-else-if="!visibleCourts.length"
        title="No courts to show"
        :description="
          courts.length
            ? 'No courts match this sport. Try another filter.'
            : 'This club has no courts published yet.'
        "
      />

      <div v-else class="court-grid">
        <article v-for="court in visibleCourts" :key="court.court_id" class="court-card">
          <div class="court-head">
            <div>
              <h2 class="court-name">{{ court.court_name }}</h2>
              <p class="court-sport">{{ labelForSport(court.sport_type) }}</p>
            </div>
            <span class="count-pill" :class="{ 'count-none': !court.openCount }">
              {{ court.openCount }} open
            </span>
          </div>

          <div v-if="court.slots.length" class="slot-grid">
            <span
              v-for="slot in court.slots"
              :key="`${court.court_id}-${slot.start_time}`"
              class="slot"
              :class="`slot-${slot.status}`"
              :title="slot.reason || slot.status"
            >
              {{ hhmm(slot.start_time) }}
            </span>
          </div>
          <p v-else class="no-slots">The club is closed on this date.</p>

          <router-link
            class="book-link"
            :to="{ name: 'register', query: { redirect: '/member/book-court' } }"
          >
            Sign up to book
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </router-link>
        </article>
      </div>

      <div class="legend">
        <span><i class="dot dot-available"></i>Available</span>
        <span><i class="dot dot-booked"></i>Booked</span>
        <span><i class="dot dot-blocked"></i>Blocked</span>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '@/api/axios'
import BrandMark from '@/components/BrandMark.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const SPORT_LABELS = {
  tennis: 'Tennis',
  badminton: 'Badminton',
  basketball: 'Basketball',
  golf: 'Golf',
  football: 'Football',
  pickleball: 'Pickleball',
  padel: 'Padel',
  squash: 'Squash',
  volleyball: 'Volleyball',
  swimming: 'Swimming',
  'multi-purpose': 'Multi-purpose',
}

const today = new Date().toISOString().slice(0, 10)

const clubs = ref([])
const courts = ref([])
const matrix = ref([])
const selectedClubId = ref('')
const selectedDate = ref(today)
const selectedSport = ref('')
const loading = ref(true)
const error = ref('')

function labelForSport(value) {
  if (!value) return 'Multi-purpose'
  return SPORT_LABELS[value] || value.charAt(0).toUpperCase() + value.slice(1)
}

function hhmm(value) {
  return String(value || '').slice(0, 5)
}

function message(err, fallback) {
  return err?.response?.data?.message || err?.message || fallback
}

/**
 * The matrix carries slots but not each court's sport, and the court list
 * carries the sport but no slots. Join them so the sport filter can work.
 */
const mergedCourts = computed(() => {
  const sportById = new Map(courts.value.map((c) => [c.id, c.sport_type]))
  return matrix.value.map((court) => {
    const slots = court.slots || []
    return {
      ...court,
      slots,
      sport_type: sportById.get(court.court_id) || 'multi-purpose',
      openCount: slots.filter((s) => s.status === 'available').length,
    }
  })
})

const sportOptions = computed(() =>
  [...new Set(mergedCourts.value.map((c) => c.sport_type))].sort(),
)

const visibleCourts = computed(() =>
  selectedSport.value
    ? mergedCourts.value.filter((c) => c.sport_type === selectedSport.value)
    : mergedCourts.value,
)

async function loadMatrix() {
  if (!selectedClubId.value) {
    matrix.value = []
    courts.value = []
    return
  }
  loading.value = true
  error.value = ''
  try {
    const [matrixRes, courtsRes] = await Promise.all([
      api.get('/availability/matrix', {
        params: { club_id: selectedClubId.value, date: selectedDate.value },
      }),
      api.get(`/clubs/${selectedClubId.value}/courts`),
    ])
    matrix.value = matrixRes.data?.courts || []
    courts.value = Array.isArray(courtsRes.data) ? courtsRes.data : []
    selectedSport.value = ''
  } catch (err) {
    matrix.value = []
    courts.value = []
    error.value = message(err, 'Could not load availability for this club.')
  } finally {
    loading.value = false
  }
}

async function reload() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/clubs')
    clubs.value = Array.isArray(data) ? data : []
    if (clubs.value.length) {
      selectedClubId.value = clubs.value[0].id
      await loadMatrix()
      return
    }
  } catch (err) {
    error.value = message(err, 'Could not load the club directory.')
  }
  loading.value = false
}

onMounted(reload)
</script>

<style scoped>
.availability-page {
  min-height: 100vh;
}

/* Header ---------------------------------------------------------------- */
.page-header {
  position: sticky;
  top: 0;
  z-index: 20;
  background: rgba(247, 249, 252, 0.9);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--border);
}
.header-inner {
  max-width: 1180px;
  margin: 0 auto;
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}
.brand-text {
  font-family: 'Plus Jakarta Sans', Inter, sans-serif;
  font-size: 19px;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--text);
}
.brand-accent {
  color: var(--brand);
}
.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}
.btn-ghost,
.btn-solid {
  border-radius: 11px;
  padding: 9px 16px;
  font-size: 13px;
  font-weight: 650;
  text-decoration: none;
  transition: all 0.2s ease;
}
.btn-ghost {
  color: var(--text-soft);
  border: 1px solid var(--border);
  background: var(--surface);
}
.btn-ghost:hover {
  border-color: #b9c9f8;
  color: var(--brand-dark);
}
.btn-solid {
  color: #fff;
  background: linear-gradient(135deg, #5267e8, #4354d1);
  box-shadow: 0 7px 18px rgba(67, 84, 209, 0.22);
}
.btn-solid:hover {
  transform: translateY(-1px);
}

/* Body ------------------------------------------------------------------ */
.page-body {
  max-width: 1180px;
  margin: 0 auto;
  padding: 40px 24px 72px;
}
.lede {
  color: var(--muted);
  max-width: 46ch;
}

.controls {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 16px;
  margin: 28px 0 20px;
}
.control {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 190px;
}
.control-grow {
  flex: 1 1 260px;
}
.control-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
}
.control-input {
  width: 100%;
  padding: 10px 12px;
  border-radius: 11px;
  border: 1px solid #d6dfeb;
  background: var(--surface);
  color: var(--text);
  outline: none;
  transition: all 0.2s ease;
}
.control-input:focus {
  border-color: #718fff;
  box-shadow: 0 0 0 4px rgba(82, 103, 232, 0.11);
}

.chip-row {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
}
.chip {
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-soft);
  border-radius: 999px;
  padding: 7px 14px;
  font-size: 12px;
  font-weight: 650;
  cursor: pointer;
  transition: all 0.15s ease;
}
.chip:hover {
  border-color: #b9c9f8;
}
.chip-on {
  background: var(--brand-soft);
  border-color: #c6d5ff;
  color: var(--brand-dark);
}

.alert {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
  padding: 12px 16px;
  border-radius: 12px;
  background: var(--surface-rose);
  border: 1px solid #f3c9cd;
  color: #a3323f;
  font-size: 13px;
}
.alert-retry {
  border: 1px solid #e3aeb4;
  background: #fff;
  color: #a3323f;
  border-radius: 8px;
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 650;
  cursor: pointer;
}

/* Court cards ----------------------------------------------------------- */
.court-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 18px;
}
.court-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 20px;
  box-shadow: var(--shadow-sm);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    border-color 0.2s ease;
}
.court-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: #c6d5ff;
}
.court-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 16px;
}
.court-name {
  font-size: 16px;
  font-weight: 700;
  margin: 0;
}
.court-sport {
  font-size: 12px;
  color: var(--brand-dark);
  font-weight: 650;
  margin: 3px 0 0;
}
.count-pill {
  flex-shrink: 0;
  border-radius: 999px;
  padding: 5px 11px;
  font-size: 11px;
  font-weight: 700;
  background: var(--surface-mint);
  color: #0b7a63;
  border: 1px solid #b9e5d8;
}
.count-pill.count-none {
  background: var(--surface-soft);
  color: var(--muted);
  border-color: var(--border);
}

.slot-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(58px, 1fr));
  gap: 6px;
  margin-bottom: 18px;
}
.slot {
  text-align: center;
  padding: 6px 4px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 650;
  font-variant-numeric: tabular-nums;
  border: 1px solid transparent;
}
.slot-available {
  background: var(--surface-mint);
  color: #0b7a63;
  border-color: #c3e9de;
}
.slot-booked {
  background: var(--surface-blue);
  color: #3745ad;
  border-color: #cfdcff;
}
.slot-blocked {
  background: var(--surface-soft);
  color: var(--muted-light);
  border-color: var(--border);
  text-decoration: line-through;
}
.no-slots {
  color: var(--muted);
  font-size: 13px;
  margin: 0 0 18px;
}

.book-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 700;
  color: var(--brand-dark);
  text-decoration: none;
}
.book-link svg {
  width: 15px;
  height: 15px;
  transition: transform 0.2s ease;
}
.book-link:hover svg {
  transform: translateX(3px);
}

.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  margin-top: 28px;
  font-size: 12px;
  color: var(--muted);
}
.legend span {
  display: inline-flex;
  align-items: center;
  gap: 7px;
}
.dot {
  width: 10px;
  height: 10px;
  border-radius: 3px;
  display: inline-block;
}
.dot-available {
  background: #7fd3bd;
}
.dot-booked {
  background: #9db7ff;
}
.dot-blocked {
  background: #cdd7e5;
}

@media (max-width: 640px) {
  .header-actions .btn-ghost {
    display: none;
  }
}
</style>
