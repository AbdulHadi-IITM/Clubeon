<template>
  <div class="space-y-6">
    <div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
      <div>
        <p class="kicker">Front desk operations</p>
        <h1 class="title mt-1">Today at the club</h1>
        <p class="muted mt-2 text-sm">Bookings, arrivals and current court status.</p>
      </div>
      <ClubPicker v-model="clubId" @change="load" />
    </div>
    <div v-if="error" class="panel p-4 text-sm text-red-600">{{ error }}</div>
    <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <div v-for="s in stats" :key="s.label" class="stat">
        <p class="kicker">{{ s.label }}</p>
        <p class="mt-2 text-3xl font-extrabold text-slate-900">{{ s.value }}</p>
        <p class="muted mt-1 text-xs">{{ s.note }}</p>
      </div>
    </div>
    <div class="grid gap-5 xl:grid-cols-[1.15fr_.85fr]">
      <section class="panel p-5">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="font-bold text-slate-900">Upcoming bookings</h2>
            <p class="muted mt-1 text-xs">Today's active schedule</p>
          </div>
          <router-link to="/staff/bookings" class="text-xs font-bold text-indigo-600"
            >Manage</router-link
          >
        </div>
        <div class="mt-4 space-y-2">
          <div
            v-for="b in activeBookings.slice(0, 7)"
            :key="b.id"
            class="flex items-center justify-between gap-4 rounded-xl border border-slate-200 bg-slate-50/70 p-4"
          >
            <div>
              <p class="text-sm font-bold text-slate-900">
                {{ time(b.start_time) }} · {{ b.court_name }}
              </p>
              <p class="mt-1 text-xs text-slate-500">{{ b.user_name }} · {{ b.user_email }}</p>
            </div>
            <span class="pill bg-emerald-50 text-emerald-700">Confirmed</span>
          </div>
          <p v-if="!activeBookings.length" class="py-8 text-center text-sm text-slate-500">
            No active bookings today.
          </p>
        </div>
      </section>
      <section class="panel p-5">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="font-bold text-slate-900">Court status</h2>
            <p class="muted mt-1 text-xs">Current availability</p>
          </div>
          <router-link to="/staff/availability" class="text-xs font-bold text-indigo-600"
            >Full matrix</router-link
          >
        </div>
        <div class="mt-4 space-y-2">
          <div
            v-for="c in courtStatus"
            :key="c.court_id"
            class="flex items-center justify-between rounded-xl border border-slate-200 p-4"
          >
            <p class="text-sm font-bold text-slate-800">{{ c.court_name }}</p>
            <span
              class="pill"
              :class="c.available ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'"
              >{{ c.available ? 'Available' : 'Occupied' }}</span
            >
          </div>
          <p v-if="!courtStatus.length" class="py-8 text-center text-sm text-slate-500">
            Select a club to view court status.
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
  data = ref({ bookings: [] }),
  matrix = ref([]),
  error = ref('')
const activeBookings = computed(() =>
  (data.value.bookings || []).filter((b) => b.status === 'active'),
)
const stats = computed(() => [
  { label: "Today's bookings", value: data.value.today_bookings || 0, note: 'scheduled today' },
  { label: 'Checked in', value: data.value.checked_in || 0, note: 'currently at club' },
  {
    label: 'Active courts',
    value: `${data.value.active_courts || 0}/${data.value.total_courts || 0}`,
    note: 'operational courts',
  },
  { label: 'Pending arrivals', value: data.value.pending_arrivals || 0, note: 'members expected' },
])
function minutes(v) {
  const [h, m] = String(v || '0:0').split(':')
  return +h * 60 + (+m || 0)
}
const courtStatus = computed(() => {
  const now = new Date(),
    n = now.getHours() * 60 + now.getMinutes()
  return matrix.value.map((c) => {
    const current = (c.slots || []).find(
      (s) => n >= minutes(s.start_time) && n < minutes(s.end_time),
    )
    return { ...c, available: !current || current.status === 'available' }
  })
})
async function load() {
  if (!clubId.value) return
  error.value = ''
  try {
    const [d, m] = await Promise.all([
      api.get('/staff/dashboard', { params: { club_id: clubId.value } }),
      api.get('/availability/matrix', { params: { club_id: clubId.value, date: today() } }),
    ])
    data.value = d.data
    matrix.value = m.data?.courts || []
  } catch (e) {
    error.value = errorMessage(e, 'Unable to load dashboard.')
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
