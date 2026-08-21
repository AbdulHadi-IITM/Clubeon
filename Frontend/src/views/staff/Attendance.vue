<template>
  <div class="space-y-6">
    <div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
      <div>
        <p class="kicker">Front desk</p>
        <h1 class="title mt-1">Attendance</h1>
        <p class="muted mt-2 text-sm">Check expected members in and manage current visits.</p>
      </div>
      <ClubPicker v-model="clubId" @change="load" />
    </div>
    <div v-if="error" class="panel p-4 text-sm text-red-600">{{ error }}</div>
    <div class="grid gap-5 xl:grid-cols-2">
      <section class="panel p-5">
        <div>
          <h2 class="font-bold text-slate-900">Today's expected members</h2>
          <p class="muted mt-1 text-xs">Active bookings scheduled today</p>
        </div>
        <div class="mt-4 space-y-3">
          <div v-for="b in expected" :key="b.id" class="rounded-xl border border-slate-200 p-4">
            <div class="flex items-start justify-between gap-3">
              <div>
                <p class="text-sm font-bold text-slate-900">{{ b.user_name }}</p>
                <p class="mt-1 text-xs text-slate-500">
                  {{ b.court_name }} · {{ time(b.start_time) }} – {{ time(b.end_time) }}
                </p>
              </div>
              <span class="pill" :class="statusClass(b.attendance_status)">{{
                label(b.attendance_status)
              }}</span>
            </div>
            <button
              v-if="b.attendance_status === 'expected'"
              class="btn btn-primary2 mt-3"
              @click="checkIn(b)"
            >
              Check in
            </button>
          </div>
          <p v-if="!expected.length" class="py-8 text-center text-sm text-slate-500">
            No expected arrivals.
          </p>
        </div>
      </section>
      <section class="panel p-5">
        <div>
          <h2 class="font-bold text-slate-900">Currently checked in</h2>
          <p class="muted mt-1 text-xs">Members presently at the club</p>
        </div>
        <div class="mt-4 space-y-3">
          <div
            v-for="r in current"
            :key="r.id"
            class="flex items-center justify-between gap-4 rounded-xl border border-slate-200 p-4"
          >
            <div>
              <p class="text-sm font-bold text-slate-900">{{ r.user_name }}</p>
              <p class="mt-1 text-xs text-slate-500">
                {{ r.court_name || 'Club visit' }} · checked in {{ dateTime(r.check_in_at) }}
              </p>
            </div>
            <button class="btn btn-soft" @click="checkOut(r)">Check out</button>
          </div>
          <p v-if="!current.length" class="py-8 text-center text-sm text-slate-500">
            Nobody is currently checked in.
          </p>
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
const clubId = ref(''),
  expected = ref([]),
  records = ref([]),
  error = ref('')
const current = computed(() => records.value.filter((r) => !r.check_out_at))
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
    ? 'bg-emerald-50 text-emerald-700'
    : s === 'checked-out'
      ? 'bg-slate-100 text-slate-600'
      : 'bg-indigo-50 text-indigo-700'
}
async function load() {
  if (!clubId.value) return
  error.value = ''
  try {
    const [e, r] = await Promise.all([
      api.get('/staff/attendance/expected', { params: { club_id: clubId.value, date: today() } }),
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
    await api.post('/staff/attendance/check-in', { booking_id: b.id })
    await load()
  } catch (x) {
    error.value = errorMessage(x, 'Unable to check in member.')
  }
}
async function checkOut(r) {
  try {
    await api.post(`/staff/attendance/${r.id}/check-out`)
    await load()
  } catch (x) {
    error.value = errorMessage(x, 'Unable to check out member.')
  }
}
</script>
<style scoped>
.panel {
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid #dfe7f1;
  border-radius: 18px;
  box-shadow: 0 12px 35px rgba(51, 65, 85, 0.06);
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
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 18px;
}
.pill {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 11px;
  font-weight: 700;
}
.btn {
  border-radius: 11px;
  padding: 10px 14px;
  font-size: 12px;
  font-weight: 700;
  transition: 0.2s;
}
.btn-primary2 {
  background: #4f46e5;
  color: white;
  box-shadow: 0 8px 18px rgba(79, 70, 229, 0.18);
}
.btn-soft {
  background: #f8fafc;
  color: #475569;
  border: 1px solid #dfe7f1;
}
.field2 {
  width: 100%;
  border: 1px solid #dbe4ef;
  border-radius: 11px;
  background: #f8fafc;
  padding: 10px 12px;
  color: #172033;
  outline: none;
}
.field2:focus {
  border-color: #818cf8;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}
</style>
