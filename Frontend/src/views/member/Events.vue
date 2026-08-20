<template>
  <div class="space-y-6">
    <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <p class="kicker">Club activities</p>
        <h1 class="title mt-1">Events</h1>
        <p class="muted mt-2 text-sm">Discover upcoming tournaments, meetups and activities.</p>
      </div>
      <button class="btn btn-soft" @click="load">Refresh</button>
    </div>
    <div v-if="error" class="panel p-4 text-sm text-red-600">{{ error }}</div>
    <div v-if="loading" class="panel p-12 text-center text-sm text-slate-500">
      Loading events...
    </div>
    <div v-else class="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
      <article v-for="e in events" :key="e.id" class="panel overflow-hidden">
        <div class="h-2 bg-gradient-to-r from-indigo-500 to-emerald-400"></div>
        <div class="p-5">
          <div class="flex items-start justify-between gap-3">
            <div>
              <p class="kicker">{{ formatDate(e.date) }}</p>
              <h2 class="mt-2 text-lg font-extrabold text-slate-900">{{ e.title }}</h2>
            </div>
            <span
              class="pill"
              :class="
                e.my_registration_status === 'registered'
                  ? 'bg-emerald-50 text-emerald-700'
                  : 'bg-indigo-50 text-indigo-700'
              "
              >{{ e.my_registration_status === 'registered' ? 'Registered' : 'Upcoming' }}</span
            >
          </div>
          <p class="mt-3 min-h-10 text-sm leading-6 text-slate-600">
            {{ e.description || 'Club event. Join other members and take part.' }}
          </p>
          <div class="mt-4 grid grid-cols-2 gap-3 text-xs">
            <div class="rounded-xl bg-slate-50 p-3">
              <p class="text-slate-400">Time</p>
              <p class="mt-1 font-bold text-slate-700">
                {{ time(e.start_time) }} – {{ time(e.end_time) }}
              </p>
            </div>
            <div class="rounded-xl bg-slate-50 p-3">
              <p class="text-slate-400">Registration</p>
              <p class="mt-1 font-bold text-slate-700">
                {{ e.registered_count || 0 }}{{ e.max_attendees ? ` / ${e.max_attendees}` : '' }}
              </p>
            </div>
          </div>
          <div class="mt-5 flex gap-2">
            <button
              class="btn btn-soft flex-1"
              @click="router.push({ name: 'member-event-details', params: { eventId: e.id } })"
            >
              View Details</button
            ><button
              v-if="e.my_registration_status !== 'registered'"
              class="btn btn-primary2 flex-1"
              @click="register(e)"
              :disabled="busy === e.id"
            >
              {{ busy === e.id ? 'Registering...' : 'Register' }}</button
            ><button
              v-else
              class="btn btn-soft flex-1"
              @click="cancel(e)"
              :disabled="busy === e.id"
            >
              Cancel registration
            </button>
          </div>
        </div>
      </article>
      <div
        v-if="!events.length"
        class="panel p-12 text-center text-sm text-slate-500 md:col-span-2 xl:col-span-3"
      >
        No upcoming events.
      </div>
    </div>
  </div>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/axios'
const router = useRouter()
const events = ref([]),
  loading = ref(false),
  error = ref(''),
  busy = ref(null)
function formatDate(v) {
  return new Intl.DateTimeFormat('en-IN', {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
  }).format(new Date(`${v}T00:00:00`))
}
function time(v) {
  if (!v) return '—'
  const [h, m] = v.split(':')
  const d = new Date()
  d.setHours(+h, +m)
  return new Intl.DateTimeFormat('en-IN', { hour: 'numeric', minute: '2-digit' }).format(d)
}
async function load() {
  loading.value = true
  error.value = ''
  try {
    const r = await api.get('/events')
    events.value = Array.isArray(r.data) ? r.data : []
  } catch (e) {
    error.value = e?.response?.data?.message || 'Unable to load events.'
  } finally {
    loading.value = false
  }
}
async function register(e) {
  busy.value = e.id
  try {
    await api.post(`/events/${e.id}/register`)
    await load()
  } catch (x) {
    error.value = x?.response?.data?.message || 'Unable to register.'
  } finally {
    busy.value = null
  }
}
async function cancel(e) {
  busy.value = e.id
  try {
    await api.post(`/events/${e.id}/cancel`)
    await load()
  } catch (x) {
    error.value = x?.response?.data?.message || 'Unable to cancel registration.'
  } finally {
    busy.value = null
  }
}
onMounted(load)
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
