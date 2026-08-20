<template>
  <div class="member-page">
    <div class="page-head">
      <div>
        <p class="kicker">Club activity</p>
        <h1 class="title">Event Details</h1>
        <p class="muted">Everything you need to know before joining this event.</p>
      </div>
      <button class="btn btn-soft" type="button" @click="router.back()">Back</button>
    </div>

    <div v-if="loading" class="panel p-10 text-center text-slate-500">Loading event...</div>
    <div v-else-if="error" class="panel p-6">
      <p class="font-semibold text-red-700">{{ error }}</p>
      <button class="btn btn-soft mt-4" @click="load">Try again</button>
    </div>

    <div v-else-if="event" class="grid gap-5 lg:grid-cols-[1.5fr_.75fr]">
      <section class="panel overflow-hidden">
        <div class="event-banner">
          <span class="pill bg-white/90 text-indigo-700">{{ event.status || 'upcoming' }}</span>
        </div>
        <div class="p-6 sm:p-8">
          <p class="kicker">{{ formatDate(event.date) }}</p>
          <h2 class="mt-2 text-3xl font-extrabold tracking-tight text-slate-900">
            {{ event.title }}
          </h2>
          <p class="mt-3 text-sm leading-7 text-slate-600">
            {{ event.description || 'Club event. Join other members and take part.' }}
          </p>

          <div class="mt-7 grid gap-4 sm:grid-cols-3">
            <Info label="Date" :value="formatDate(event.date)" />
            <Info label="Time" :value="`${time(event.start_time)} – ${time(event.end_time)}`" />
            <Info label="Participants" :value="participantLabel" />
          </div>
        </div>
      </section>

      <aside class="panel p-6 sm:p-7">
        <p class="kicker">Registration</p>
        <div class="mt-3 flex items-end justify-between gap-4">
          <div>
            <p class="text-2xl font-extrabold text-slate-900">
              {{ event.registration_fee > 0 ? formatCurrency(event.registration_fee) : 'Free' }}
            </p>
            <p class="mt-1 text-xs text-slate-500">Registration fee</p>
          </div>
          <span
            class="pill"
            :class="registered ? 'bg-emerald-50 text-emerald-700' : 'bg-indigo-50 text-indigo-700'"
          >
            {{ registered ? 'Registered' : 'Open' }}
          </span>
        </div>

        <button
          v-if="!registered"
          class="btn btn-primary mt-7 w-full"
          :disabled="busy"
          @click="startRegistration"
        >
          {{
            busy
              ? 'Processing...'
              : event.registration_fee > 0
                ? 'Continue to Payment'
                : 'Register Now'
          }}
        </button>

        <button
          v-else
          class="btn btn-soft mt-7 w-full"
          :disabled="busy"
          @click="cancelRegistration"
        >
          {{ busy ? 'Cancelling...' : 'Cancel Registration' }}
        </button>

        <router-link to="/member/events" class="btn btn-soft mt-3 block w-full text-center">
          Back to Events
        </router-link>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { computed, h, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'

const route = useRoute()
const router = useRouter()
const event = ref(null)
const loading = ref(true)
const error = ref('')
const busy = ref(false)

const registered = computed(() => event.value?.my_registration_status === 'registered')
const participantLabel = computed(() => {
  if (!event.value) return '—'
  const count = event.value.registered_count || 0
  return event.value.max_attendees ? `${count} / ${event.value.max_attendees}` : `${count}`
})

function Info(props) {
  return h('div', { class: 'rounded-2xl border border-slate-200 bg-slate-50 p-4' }, [
    h(
      'p',
      { class: 'text-[11px] font-bold uppercase tracking-[.1em] text-slate-400' },
      props.label,
    ),
    h('p', { class: 'mt-2 text-sm font-bold text-slate-800' }, props.value || '—'),
  ])
}

function formatDate(value) {
  if (!value) return '—'
  return new Intl.DateTimeFormat('en-IN', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(new Date(`${value}T00:00:00`))
}

function time(value) {
  if (!value) return '—'
  const [h, m] = value.split(':')
  const d = new Date()
  d.setHours(Number(h), Number(m || 0), 0, 0)
  return new Intl.DateTimeFormat('en-IN', { hour: 'numeric', minute: '2-digit' }).format(d)
}

function formatCurrency(value) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 2,
  }).format(Number(value || 0))
}

async function load() {
  loading.value = true
  error.value = ''
  try {
    const response = await api.get('/events')
    const rows = Array.isArray(response.data) ? response.data : []
    event.value = rows.find((row) => String(row.id) === String(route.params.eventId)) || null
    if (!event.value) throw new Error('Event not found.')
  } catch (err) {
    error.value = err?.response?.data?.message || err?.message || 'Unable to load event.'
  } finally {
    loading.value = false
  }
}

function startRegistration() {
  if (!event.value) return
  if (Number(event.value.registration_fee || 0) > 0) {
    router.push({
      name: 'member-checkout',
      query: { payment_type: 'event', reference_id: String(event.value.id) },
    })
    return
  }
  registerFree()
}

async function registerFree() {
  busy.value = true
  error.value = ''
  try {
    await api.post(`/events/${event.value.id}/register`)
    await load()
  } catch (err) {
    error.value = err?.response?.data?.message || 'Unable to register.'
  } finally {
    busy.value = false
  }
}

async function cancelRegistration() {
  busy.value = true
  try {
    await api.post(`/events/${event.value.id}/cancel`)
    await load()
  } catch (err) {
    error.value = err?.response?.data?.message || 'Unable to cancel registration.'
  } finally {
    busy.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.member-page {
  max-width: 1180px;
  margin: 0 auto;
}
.page-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
}
.kicker {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #64748b;
}
.title {
  font-size: 30px;
  line-height: 1.15;
  font-weight: 800;
  letter-spacing: -0.04em;
  color: #172033;
  margin-top: 4px;
}
.muted {
  color: #64748b;
  margin-top: 8px;
  font-size: 14px;
}
.panel {
  background: rgba(255, 255, 255, 0.94);
  border: 1px solid #dfe7f1;
  border-radius: 20px;
  box-shadow: 0 12px 35px rgba(51, 65, 85, 0.06);
}
.event-banner {
  height: 170px;
  padding: 22px;
  display: flex;
  align-items: flex-start;
  justify-content: flex-end;
  background:
    radial-gradient(circle at 15% 20%, rgba(99, 102, 241, 0.9), transparent 45%),
    linear-gradient(135deg, #172554, #0f766e);
}
.pill {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 7px 11px;
  font-size: 11px;
  font-weight: 800;
  text-transform: capitalize;
}
.btn {
  border-radius: 11px;
  padding: 10px 14px;
  font-size: 12px;
  font-weight: 800;
  transition: 0.2s;
}
.btn-primary {
  background: #4f46e5;
  color: white;
  box-shadow: 0 8px 18px rgba(79, 70, 229, 0.18);
}
.btn-soft {
  background: #f8fafc;
  color: #475569;
  border: 1px solid #dfe7f1;
}
.btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}
</style>
