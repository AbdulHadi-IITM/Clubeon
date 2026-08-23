<template>
  <div class="space-y-6">
    <!-- Header & Club Picker -->
    <div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
      <div>
        <p class="kicker">Front desk</p>
        <h1 class="title mt-1">Attendance & Daily Schedule</h1>
        <p class="muted mt-2 text-sm">Track expected member arrivals, view future court schedules, and manage on-site visits.</p>
      </div>
      <ClubPicker v-model="clubId" @change="load" />
    </div>

    <!-- Date Navigation & Calendar Toolbar -->
    <div class="panel p-5">
      <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <!-- Date Selector with Prev / Today / Next -->
        <div class="flex flex-wrap items-center gap-2">
          <button
            class="btn-nav"
            title="Previous Day"
            @click="changeDate(-1)"
          >
            ← Prev Day
          </button>
          
          <button
            class="btn-nav font-bold"
            :class="{ 'btn-nav-active': isSelectedToday }"
            @click="setToday"
          >
            Today
          </button>
          
          <button
            class="btn-nav"
            title="Next Day"
            @click="changeDate(1)"
          >
            Next Day →
          </button>

          <!-- Native Date Picker Input with Calendar Icon -->
          <div class="relative flex items-center">
            <input
              type="date"
              v-model="selectedDate"
              @change="load"
              class="date-input"
            />
          </div>
        </div>

        <!-- Quick Jump Chips (Tomorrow, +2 Days, +1 Week) -->
        <div class="flex flex-wrap items-center gap-2">
          <button
            v-for="chip in quickChips"
            :key="chip.days"
            class="date-chip"
            :class="{ 'date-chip-active': isDateMatchingOffset(chip.days) }"
            @click="setDateOffset(chip.days)"
          >
            {{ chip.label }}
          </button>
        </div>
      </div>

      <!-- Selected Date Info Banner -->
      <div class="mt-4 flex flex-wrap items-center justify-between border-t border-slate-100 pt-3 text-sm">
        <div class="flex items-center gap-2">
          <span class="text-base font-bold text-slate-800">📅 {{ formattedSelectedDate }}</span>
          <span class="pill" :class="relativeDateBadge.class">
            {{ relativeDateBadge.label }}
          </span>
        </div>
        <span class="text-xs font-semibold text-slate-500">
          Showing {{ expected.length }} scheduled booking{{ expected.length === 1 ? '' : 's' }}
        </span>
      </div>
    </div>

    <div v-if="error" class="panel p-4 text-sm font-medium text-red-600">{{ error }}</div>

    <!-- Daily KPI Metric Cards -->
    <div class="grid grid-cols-2 gap-4 md:grid-cols-4">
      <div class="stat">
        <span class="kicker">Expected Total</span>
        <p class="mt-2 text-2xl font-black text-slate-900">{{ expected.length }}</p>
        <span class="mt-1 text-xs text-slate-500">Scheduled for this date</span>
      </div>
      <div class="stat">
        <span class="kicker text-emerald-600">Checked In</span>
        <p class="mt-2 text-2xl font-black text-emerald-600">{{ checkedInCount }}</p>
        <span class="mt-1 text-xs text-slate-500">Currently on premise</span>
      </div>
      <div class="stat">
        <span class="kicker text-indigo-600">Completed</span>
        <p class="mt-2 text-2xl font-black text-indigo-600">{{ checkedOutCount }}</p>
        <span class="mt-1 text-xs text-slate-500">Completed visits</span>
      </div>
      <div class="stat">
        <span class="kicker text-amber-600">Pending Arrival</span>
        <p class="mt-2 text-2xl font-black text-amber-600">{{ pendingCount }}</p>
        <span class="mt-1 text-xs text-slate-500">Awaiting arrival</span>
      </div>
    </div>

    <!-- Search / Filter Input -->
    <div class="panel p-4">
      <div class="flex items-center gap-3">
        <svg class="h-5 w-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search expected member, email, or court name on this date..."
          class="w-full bg-transparent text-sm text-slate-800 placeholder-slate-400 outline-none"
        />
        <button v-if="searchQuery" @click="searchQuery = ''" class="text-xs text-slate-400 hover:text-slate-600">✕ Clear</button>
      </div>
    </div>

    <!-- Main Dual Section (Expected Schedule & Current On-Site Visits) -->
    <div class="grid gap-5 xl:grid-cols-2">
      <!-- Section 1: Expected Members for Selected Date -->
      <section class="panel p-5">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="font-bold text-slate-900">{{ isSelectedToday ? "Today's" : formattedSelectedDay + "'s" }} Expected Members</h2>
            <p class="muted mt-1 text-xs">Active bookings for {{ formattedSelectedDate }}</p>
          </div>
          <span class="pill bg-slate-100 text-slate-700 font-bold text-xs">{{ filteredExpected.length }} slots</span>
        </div>

        <div class="mt-4 space-y-3">
          <div v-for="b in filteredExpected" :key="b.id" class="rounded-xl border border-slate-200 bg-white p-4 transition-all hover:border-indigo-200 hover:shadow-sm">
            <div class="flex items-start justify-between gap-3">
              <div class="flex items-center gap-3">
                <div class="user-avatar-sm">{{ getInitials(b.user_name) }}</div>
                <div>
                  <p class="text-sm font-bold text-slate-900">{{ b.user_name }}</p>
                  <p class="mt-0.5 text-xs text-slate-500">{{ b.user_email || '—' }}</p>
                  <p class="mt-1 text-xs font-semibold text-indigo-600">
                    🏟️ {{ b.court_name }} · ⏰ {{ time(b.start_time) }} – {{ time(b.end_time) }}
                  </p>
                </div>
              </div>
              <span class="pill" :class="statusClass(b.attendance_status)">
                {{ label(b.attendance_status) }}
              </span>
            </div>

            <!-- Action Area -->
            <div class="mt-3 flex items-center justify-between border-t border-slate-100 pt-2 text-xs">
              <span class="text-slate-400">Ref #{{ b.booking_id || b.id }}</span>
              <button
                v-if="b.attendance_status === 'expected' && isSelectedToday"
                class="btn btn-primary2"
                @click="checkIn(b)"
              >
                ✓ Check in member
              </button>
              <span v-else-if="b.attendance_status === 'expected' && !isSelectedToday" class="text-xs font-medium text-slate-500">
                📅 Scheduled for {{ b.booking_date }}
              </span>
              <span v-else-if="b.attendance_status === 'checked-in'" class="text-xs font-bold text-emerald-600">
                ✓ Currently checked in
              </span>
              <span v-else class="text-xs text-slate-400">
                Visit completed
              </span>
            </div>
          </div>

          <div v-if="!filteredExpected.length" class="py-12 text-center text-sm text-slate-500">
            <div class="mb-2 text-3xl">📅</div>
            <p class="font-semibold text-slate-700">No scheduled bookings on {{ formattedSelectedDate }}</p>
            <p class="text-xs text-slate-400 mt-1">Use the calendar navigation above to check another day.</p>
          </div>
        </div>
      </section>

      <!-- Section 2: On-Site / Checked In Visits -->
      <section class="panel p-5">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="font-bold text-slate-900">Currently Checked In</h2>
            <p class="muted mt-1 text-xs">Members presently on-site at the club</p>
          </div>
          <span class="pill bg-emerald-50 text-emerald-700 font-bold text-xs">{{ current.length }} Active</span>
        </div>

        <div class="mt-4 space-y-3">
          <div
            v-for="r in current"
            :key="r.id"
            class="flex items-center justify-between gap-4 rounded-xl border border-emerald-100 bg-emerald-50/30 p-4"
          >
            <div class="flex items-center gap-3">
              <div class="user-avatar-sm" style="background: linear-gradient(135deg, #059669, #10b981);">{{ getInitials(r.user_name) }}</div>
              <div>
                <p class="text-sm font-bold text-slate-900">{{ r.user_name }}</p>
                <p class="mt-0.5 text-xs text-slate-500">
                  {{ r.court_name || 'Club Visit' }} · Checked in {{ dateTime(r.check_in_at) }}
                </p>
              </div>
            </div>
            <button class="btn btn-soft text-rose-600 hover:bg-rose-50 hover:border-rose-200" @click="checkOut(r)">
              Check out
            </button>
          </div>

          <div v-if="!current.length" class="py-12 text-center text-sm text-slate-500">
            <div class="mb-2 text-3xl">🚪</div>
            <p class="font-semibold text-slate-700">Nobody is currently checked in.</p>
            <p class="text-xs text-slate-400 mt-1">Check in expected members from the schedule when they arrive.</p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>
<script setup>
import { computed, ref } from 'vue'
import api from '@/api/axios'
import ClubPicker from './components/ClubPicker.vue'
import { today, time, errorMessage } from './_helpers'

const clubId = ref('')
const expected = ref([])
const records = ref([])
const error = ref('')

// Calendar & Date Navigation State
const selectedDate = ref(today())
const isSelectedToday = computed(() => selectedDate.value === today())

function formatDateStr(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

function changeDate(daysOffset) {
  const current = new Date(selectedDate.value + 'T00:00:00')
  current.setDate(current.getDate() + daysOffset)
  selectedDate.value = formatDateStr(current)
  load()
}

function setToday() {
  selectedDate.value = today()
  load()
}

function setDateOffset(days) {
  const d = new Date()
  d.setDate(d.getDate() + days)
  selectedDate.value = formatDateStr(d)
  load()
}

function isDateMatchingOffset(days) {
  const d = new Date()
  d.setDate(d.getDate() + days)
  return selectedDate.value === formatDateStr(d)
}

const quickChips = [
  { label: 'Today', days: 0 },
  { label: 'Tomorrow', days: 1 },
  { label: '+2 Days', days: 2 },
  { label: '+3 Days', days: 3 },
  { label: '+1 Week', days: 7 },
]

const formattedSelectedDate = computed(() => {
  if (!selectedDate.value) return '—'
  const d = new Date(selectedDate.value + 'T00:00:00')
  return new Intl.DateTimeFormat('en-US', { weekday: 'long', month: 'short', day: 'numeric', year: 'numeric' }).format(d)
})

const formattedSelectedDay = computed(() => {
  if (!selectedDate.value) return 'Day'
  const d = new Date(selectedDate.value + 'T00:00:00')
  return new Intl.DateTimeFormat('en-US', { weekday: 'long' }).format(d)
})

const relativeDateBadge = computed(() => {
  const todayStr = today()
  if (selectedDate.value === todayStr) {
    return { label: 'Today', class: 'bg-emerald-50 text-emerald-700 border border-emerald-200' }
  }
  const sel = new Date(selectedDate.value + 'T00:00:00').getTime()
  const tod = new Date(todayStr + 'T00:00:00').getTime()
  const diffDays = Math.round((sel - tod) / (1000 * 60 * 60 * 24))
  if (diffDays === 1) {
    return { label: 'Tomorrow', class: 'bg-indigo-50 text-indigo-700 border border-indigo-200' }
  }
  if (diffDays > 1) {
    return { label: `In ${diffDays} Days`, class: 'bg-purple-50 text-purple-700 border border-purple-200' }
  }
  return { label: `${Math.abs(diffDays)} Days Ago`, class: 'bg-slate-100 text-slate-600 border border-slate-200' }
})

// Current Checked In and KPIs
const current = computed(() => records.value.filter((r) => !r.check_out_at))
const checkedInCount = computed(() => expected.value.filter(b => b.attendance_status === 'checked-in').length)
const checkedOutCount = computed(() => expected.value.filter(b => b.attendance_status === 'checked-out').length)
const pendingCount = computed(() => expected.value.filter(b => b.attendance_status === 'expected').length)

// Search & Filtering
const searchQuery = ref('')
const filteredExpected = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return expected.value
  return expected.value.filter(b => 
    (b.user_name && b.user_name.toLowerCase().includes(q)) ||
    (b.user_email && b.user_email.toLowerCase().includes(q)) ||
    (b.court_name && b.court_name.toLowerCase().includes(q)) ||
    String(b.id).includes(q)
  )
})

function getInitials(name) {
  if (!name) return 'M'
  return name.split(/\s+/).filter(Boolean).map(n => n[0]).join('').slice(0, 2).toUpperCase() || 'M'
}

function dateTime(v) {
  if (!v) return '—'
  const d = new Date(String(v).replace(' ', 'T'))
  return Number.isNaN(d.getTime())
    ? v
    : new Intl.DateTimeFormat('en-IN', { hour: 'numeric', minute: '2-digit' }).format(d)
}

function label(s) {
  return s === 'checked-in' ? 'Checked in' : s === 'checked-out' ? 'Completed' : 'Expected'
}

function statusClass(s) {
  return s === 'checked-in'
    ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
    : s === 'checked-out'
      ? 'bg-slate-100 text-slate-600 border border-slate-200'
      : 'bg-indigo-50 text-indigo-700 border border-indigo-200'
}

async function load() {
  if (!clubId.value) return
  error.value = ''
  try {
    const [e, r] = await Promise.all([
      api.get('/staff/attendance/expected', { params: { club_id: clubId.value, date: selectedDate.value } }),
      api.get('/staff/attendance', { params: { club_id: clubId.value } }),
    ])
    expected.value = e.data
    records.value = r.data
  } catch (x) {
    error.value = errorMessage(x, 'Unable to load attendance.')
  }
}

async function checkIn(b) {
  try {
    await api.post('/staff/attendance/check-in', { booking_id: b.id, club_id: clubId.value })
    await load()
  } catch (x) {
    error.value = errorMessage(x, 'Unable to check in member.')
  }
}

async function checkOut(r) {
  try {
    await api.post(`/staff/attendance/${r.id}/check-out`, null, { params: { club_id: clubId.value } })
    await load()
  } catch (x) {
    error.value = errorMessage(x, 'Unable to check out member.')
  }
}
</script>
<style scoped>
.panel {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid #dfe7f1;
  border-radius: 18px;
  box-shadow: 0 12px 35px rgba(51, 65, 85, 0.05);
}
.kicker {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #64748b;
}
.title {
  font-size: 28px;
  line-height: 1.15;
  font-weight: 800;
  letter-spacing: -0.035em;
  color: #172033;
}
.muted {
  color: #64748b;
}
.stat {
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 4px 12px rgba(51, 65, 85, 0.03);
}
.pill {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 11px;
  font-weight: 700;
}
.btn {
  border-radius: 11px;
  padding: 8px 14px;
  font-size: 12px;
  font-weight: 700;
  transition: 0.2s;
  cursor: pointer;
}
.btn-primary2 {
  background: #4f46e5;
  color: white;
  box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2);
}
.btn-primary2:hover {
  background: #4338ca;
}
.btn-soft {
  background: #f8fafc;
  color: #475569;
  border: 1px solid #dfe7f1;
}
.btn-soft:hover {
  background: #f1f5f9;
}
.btn-nav {
  padding: 7px 14px;
  border-radius: 10px;
  border: 1px solid #dbe4ef;
  background: #ffffff;
  color: #334155;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-nav:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}
.btn-nav-active {
  background: #4f46e5;
  color: #ffffff;
  border-color: #4f46e5;
}
.btn-nav-active:hover {
  background: #4338ca;
}
.date-input {
  padding: 6px 12px;
  border-radius: 10px;
  border: 1px solid #dbe4ef;
  background: #f8fafc;
  color: #1e293b;
  font-size: 12px;
  font-weight: 600;
  outline: none;
  cursor: pointer;
}
.date-input:focus {
  border-color: #818cf8;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}
.date-chip {
  padding: 5px 12px;
  border-radius: 999px;
  border: 1px solid #e2e8f0;
  background: #f8fafc;
  color: #475569;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}
.date-chip:hover {
  background: #eff6ff;
  color: #2563eb;
  border-color: #bfdbfe;
}
.date-chip-active {
  background: #eff6ff;
  color: #2563eb;
  border-color: #3b82f6;
  font-weight: 700;
}
.user-avatar-sm {
  width: 34px;
  height: 34px;
  border-radius: 999px;
  background: linear-gradient(135deg, #4f46e5, #6366f1);
  color: white;
  font-weight: 700;
  font-size: 11px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
}
</style>

