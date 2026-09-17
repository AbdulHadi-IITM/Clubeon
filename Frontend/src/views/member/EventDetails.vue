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
        <div class="relative h-48 sm:h-64 w-full overflow-hidden bg-slate-900">
          <img :src="getSportImage(event.title || event.sport)" :alt="event.title" class="h-full w-full object-cover opacity-90" />
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-slate-950/20 to-transparent"></div>
          <span class="absolute top-4 right-4 pill bg-white/95 text-indigo-700 font-bold shadow-md">{{ event.status || 'upcoming' }}</span>
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

    <!-- EVENT REGISTRATION DETAILS & CONFIRMATION MODAL -->
    <div v-if="showRegisterModal && event" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4 animate-fade-in">
      <div class="w-full max-w-lg overflow-hidden rounded-2xl bg-white shadow-2xl border border-slate-200 animate-scale-up">
        <div class="border-b border-slate-100 bg-slate-50/75 p-5">
          <div class="flex items-center justify-between">
            <span class="text-[11px] font-extrabold uppercase tracking-wider text-indigo-600">Event Registration</span>
            <button @click="showRegisterModal = false" class="rounded-lg p-1 text-slate-400 hover:bg-slate-200 hover:text-slate-600 transition">✕</button>
          </div>
          <h3 class="mt-1 text-xl font-bold text-slate-900">{{ event.title }}</h3>
          <p class="mt-1 text-xs text-slate-500">{{ formatDate(event.date) }} • {{ time(event.start_time) }} - {{ time(event.end_time) }}</p>
        </div>

        <form @submit.prevent="confirmAndSubmitRegistration" class="p-6 space-y-4">
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold uppercase text-slate-500 mb-1">Participant Name *</label>
              <input type="text" v-model="regForm.name" required class="w-full rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2.5 text-sm font-medium text-slate-900 outline-none focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-100" />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase text-slate-500 mb-1">Email Address *</label>
              <input type="email" v-model="regForm.email" required class="w-full rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2.5 text-sm font-medium text-slate-900 outline-none focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-100" />
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold uppercase text-slate-500 mb-1">Phone Number *</label>
              <input type="tel" v-model="regForm.phone" required placeholder="+91 98765 43210" class="w-full rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2.5 text-sm font-medium text-slate-900 outline-none focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-100" />
            </div>
            <div>
              <label class="block text-xs font-bold uppercase text-slate-500 mb-1">Skill Category</label>
              <select v-model="regForm.category" class="w-full rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2.5 text-sm font-medium text-slate-900 outline-none focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-100">
                <option value="Open">Open / All Levels</option>
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced / Competitive</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold uppercase text-slate-500 mb-1">Special Requirements / Notes</label>
            <textarea v-model="regForm.notes" rows="2" placeholder="e.g. Dietary requirements, equipment requests, partner name" class="w-full rounded-xl border border-slate-200 bg-slate-50 px-3.5 py-2 text-sm font-medium text-slate-900 outline-none focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-100"></textarea>
          </div>

          <div class="rounded-xl border border-slate-100 bg-indigo-50/50 p-4">
            <div class="flex items-center justify-between text-sm font-semibold">
              <span class="text-slate-600">Entry Fee</span>
              <span class="text-indigo-600 font-extrabold text-base">{{ event.registration_fee > 0 ? formatCurrency(event.registration_fee) : 'Free' }}</span>
            </div>
          </div>

          <label class="flex items-start gap-3 pt-1 cursor-pointer">
            <input type="checkbox" v-model="regForm.confirmedTerms" required class="mt-1 h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500" />
            <span class="text-xs text-slate-600 leading-relaxed">
              I confirm my registration for this event and agree to adhere to all club guidelines.
            </span>
          </label>

          <div class="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
            <button type="button" @click="showRegisterModal = false" class="rounded-xl border border-slate-200 px-4 py-2.5 text-xs font-bold text-slate-600 hover:bg-slate-50 transition">Cancel</button>
            <button type="submit" :disabled="busy" class="rounded-xl bg-indigo-600 px-5 py-2.5 text-xs font-bold text-white shadow-md shadow-indigo-200 hover:bg-indigo-700 transition disabled:opacity-50">
              {{ busy ? 'Registering...' : event.registration_fee > 0 ? 'Proceed to Payment (' + formatCurrency(event.registration_fee) + ')' : 'Confirm & Register' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, h, onMounted, ref, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import { getSportImage } from '@/utils/sportImages'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const event = ref(null)
const loading = ref(true)
const error = ref('')
const busy = ref(false)
const showRegisterModal = ref(false)

const regForm = reactive({
  name: '',
  email: '',
  phone: '',
  category: 'Open',
  notes: '',
  confirmedTerms: false
})

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
    const response = await api.get(`/events/${route.params.eventId}`)
    event.value = response.data || null
    if (!event.value) throw new Error('Event not found.')
  } catch (err) {
    error.value = err?.response?.data?.message || err?.message || 'Unable to load event.'
  } finally {
    loading.value = false
  }
}

function startRegistration() {
  if (!event.value) return
  regForm.name = auth.user?.name || ''
  regForm.email = auth.user?.email || ''
  regForm.phone = auth.user?.phone || ''
  regForm.category = 'Open'
  regForm.notes = ''
  regForm.confirmedTerms = false
  showRegisterModal.value = true
}

async function confirmAndSubmitRegistration() {
  if (!event.value) return
  if (!regForm.confirmedTerms) {
    alert('Please agree to the confirmation terms.')
    return
  }

  if (Number(event.value.registration_fee || 0) > 0) {
    showRegisterModal.value = false
    router.push({
      name: 'member-checkout',
      query: { payment_type: 'event', reference_id: String(event.value.id) },
    })
    return
  }

  busy.value = true
  error.value = ''
  try {
    await api.post(`/events/${event.value.id}/register`)
    showRegisterModal.value = false
    await load()
  } catch (err) {
    error.value = err?.response?.data?.message || 'Unable to register.'
  } finally {
    busy.value = false
  }
}

async function cancelRegistration() {
  if (!confirm(`Are you sure you want to cancel your registration for "${event.value.title}"?`)) return
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

onMounted(async () => {
  if (!auth.user) await auth.restoreUser()
  await load()
})
</script>

<style scoped>
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
.btn-primary {
  background: #4f46e5;
  color: white;
  box-shadow: 0 8px 18px rgba(79, 70, 229, 0.18);
}
.animate-fade-in {
  animation: fadeIn 0.2s ease-out;
}
.animate-scale-up {
  animation: scaleUp 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes scaleUp {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>
