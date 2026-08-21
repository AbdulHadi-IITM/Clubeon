<template>
  <div class="member-page">
    <div class="page-head">
      <div>
        <p class="kicker">Booking</p>
        <h1 class="title">Booking Details</h1>
        <p class="muted">Review the complete details of your court reservation.</p>
      </div>
      <button class="btn btn-soft" type="button" @click="router.back()">Back</button>
    </div>

    <div v-if="loading" class="panel p-10 text-center text-slate-500">Loading booking...</div>
    <div v-else-if="error" class="panel p-6">
      <p class="font-semibold text-red-700">{{ error }}</p>
      <button class="btn btn-soft mt-4" @click="load">Try again</button>
    </div>

    <div v-else-if="booking" class="grid gap-5 lg:grid-cols-[1.4fr_.8fr]">
      <section class="panel p-6 sm:p-7">
        <div class="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p class="kicker">{{ booking.sportType || 'Court booking' }}</p>
            <h2 class="mt-2 text-2xl font-extrabold tracking-tight text-slate-900">
              {{ booking.courtName || booking.court_name || `Court #${booking.court_id || '—'}` }}
            </h2>
            <p v-if="booking.clubName || booking.club_name" class="mt-1 text-sm text-slate-500">
              {{ booking.clubName || booking.club_name }}
            </p>
          </div>
          <span class="pill" :class="statusClass(booking.status)">
            {{ booking.status || 'Unknown' }}
          </span>
        </div>

        <div class="mt-7 grid gap-4 sm:grid-cols-2">
          <Info label="Date" :value="formatDate(booking.bookingDate || booking.date)" />
          <Info
            label="Time"
            :value="`${formatTime(booking.startTime || booking.start_time)} – ${formatTime(booking.endTime || booking.end_time)}`"
          />
          <Info label="Booking ID" :value="`#${booking.id}`" />
          <Info
            label="Amount"
            :value="formatCurrency(booking.amount ?? booking.price ?? booking.total_amount)"
          />
        </div>

        <div class="mt-7 rounded-2xl border border-slate-200 bg-slate-50 p-5">
          <p class="text-xs font-bold uppercase tracking-[.12em] text-slate-400">
            Reservation status
          </p>
          <p class="mt-2 text-sm leading-6 text-slate-600">
            {{
              booking.status === 'active'
                ? 'Your reservation is active. Please arrive a few minutes before your scheduled slot.'
                : 'This reservation is no longer active.'
            }}
          </p>
        </div>
      </section>

      <aside class="panel p-6 sm:p-7">
        <p class="kicker">Actions</p>
        <h3 class="mt-2 text-lg font-extrabold text-slate-900">Manage booking</h3>
        <p class="mt-2 text-sm leading-6 text-slate-500">
          Release this booking only if you no longer need the reserved slot.
        </p>

        <button
          v-if="booking.status === 'active'"
          class="btn btn-danger mt-6 w-full"
          :disabled="releasing"
          @click="releaseBooking"
        >
          {{ releasing ? 'Releasing...' : 'Release Booking' }}
        </button>

        <router-link to="/member/my-bookings" class="btn btn-soft mt-3 block w-full text-center">
          View My Bookings
        </router-link>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api/axios'

const route = useRoute()
const router = useRouter()
const booking = ref(null)
const loading = ref(true)
const error = ref('')
const releasing = ref(false)

function Info(props) {
  return h('div', { class: 'rounded-2xl border border-slate-200 bg-white p-4' }, [
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
    weekday: 'short',
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }).format(new Date(`${value}T00:00:00`))
}

function formatTime(value) {
  if (!value) return '—'
  const [h, m] = String(value).split(':')
  const d = new Date()
  d.setHours(Number(h), Number(m || 0), 0, 0)
  return new Intl.DateTimeFormat('en-IN', { hour: 'numeric', minute: '2-digit' }).format(d)
}

function formatCurrency(value) {
  if (value === undefined || value === null || value === '') return '—'
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 2,
  }).format(Number(value))
}

function statusClass(status) {
  if (status === 'active' || status === 'completed') return 'bg-emerald-50 text-emerald-700'
  if (status === 'cancelled' || status === 'released') return 'bg-red-50 text-red-700'
  return 'bg-amber-50 text-amber-700'
}

async function load() {
  loading.value = true
  error.value = ''
  try {
    // The existing booking API exposes the member's bookings.
    // Find the requested record locally so this screen stays compatible
    // with the current backend contract.
    const response = await api.get('/bookings')
    const rows = Array.isArray(response.data) ? response.data : []
    const found = rows.find((row) => String(row.id) === String(route.params.bookingId))
    if (!found) throw new Error('Booking not found.')
    booking.value = found
  } catch (err) {
    error.value = err?.response?.data?.message || err?.message || 'Unable to load booking.'
  } finally {
    loading.value = false
  }
}

async function releaseBooking() {
  if (!booking.value) return
  releasing.value = true
  try {
    await api.post(`/bookings/${booking.value.id}/release`)
    await load()
  } catch (err) {
    error.value = err?.response?.data?.message || 'Unable to release booking.'
  } finally {
    releasing.value = false
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
.btn-soft {
  background: #f8fafc;
  color: #475569;
  border: 1px solid #dfe7f1;
}
.btn-danger {
  background: #dc2626;
  color: white;
  box-shadow: 0 8px 18px rgba(220, 38, 38, 0.16);
}
.btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}
</style>
