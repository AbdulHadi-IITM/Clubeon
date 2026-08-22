<template>
  <div class="space-y-6">
    <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <p class="kicker">Club activities</p>
        <h1 class="title mt-1">Events</h1>
        <p class="muted mt-2 text-sm">Discover upcoming tournaments, meetups and activities.</p>
      </div>
      <div class="flex items-center gap-3">
        <div class="flex rounded-xl bg-slate-100 p-1 border border-slate-200">
          <button
            @click="activeTab = 'all'"
            :class="activeTab === 'all' ? 'bg-white text-indigo-600 shadow-sm font-bold' : 'text-slate-500 font-medium'"
            class="rounded-lg px-3 py-1.5 text-xs transition"
          >
            All Events
          </button>
          <button
            @click="activeTab = 'mine'"
            :class="activeTab === 'mine' ? 'bg-white text-indigo-600 shadow-sm font-bold' : 'text-slate-500 font-medium'"
            class="rounded-lg px-3 py-1.5 text-xs transition"
          >
            My Registrations
          </button>
        </div>
        <button class="btn btn-soft" @click="load">Refresh</button>
      </div>
    </div>
    <div v-if="error" class="panel p-4 text-sm text-red-600">{{ error }}</div>
    <div v-if="loading" class="panel p-12 text-center text-sm text-slate-500">
      Loading events...
    </div>
    <div v-else class="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
      <article v-for="e in displayedEvents" :key="e.id" class="panel overflow-hidden flex flex-col justify-between">
        <div class="relative h-36 w-full overflow-hidden bg-slate-900">
          <img :src="getSportImage(e.title || e.sport)" :alt="e.title" class="h-full w-full object-cover opacity-90 transition duration-300 hover:scale-105" />
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950/70 via-transparent to-transparent"></div>
          <span
            class="absolute top-3 right-3 pill shadow-sm"
            :class="
              e.my_registration_status === 'registered'
                ? 'bg-emerald-500 text-white'
                : 'bg-white/90 text-indigo-700'
            "
          >{{ e.my_registration_status === 'registered' ? 'Registered' : 'Upcoming' }}</span>
        </div>
        <div class="p-5 flex-1 flex flex-col justify-between">
          <div>
            <p class="kicker">{{ formatDate(e.date) }}</p>
            <h2 class="mt-1 text-lg font-extrabold text-slate-900">{{ e.title }}</h2>
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
        v-if="!displayedEvents.length"
        class="panel p-12 text-center text-sm text-slate-500 md:col-span-2 xl:col-span-3"
      >
        No events found.
      </div>
    </div>

    <!-- EVENT REGISTRATION DETAILS & CONFIRMATION MODAL -->
    <div v-if="showRegisterModal && selectedEventForRegistration" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4 animate-fade-in">
      <div class="w-full max-w-lg overflow-hidden rounded-2xl bg-white shadow-2xl border border-slate-200 animate-scale-up">
        <div class="border-b border-slate-100 bg-slate-50/75 p-5">
          <div class="flex items-center justify-between">
            <span class="text-[11px] font-extrabold uppercase tracking-wider text-indigo-600">Event Registration</span>
            <button @click="closeRegisterModal" class="rounded-lg p-1 text-slate-400 hover:bg-slate-200 hover:text-slate-600 transition">✕</button>
          </div>
          <h3 class="mt-1 text-xl font-bold text-slate-900">{{ selectedEventForRegistration.title }}</h3>
          <p class="mt-1 text-xs text-slate-500">{{ formatDate(selectedEventForRegistration.date) }} • {{ time(selectedEventForRegistration.start_time) }} - {{ time(selectedEventForRegistration.end_time) }}</p>
        </div>

        <form @submit.prevent="submitRegistration" class="p-6 space-y-4">
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
              <span class="text-indigo-600 font-extrabold text-base">{{ selectedEventForRegistration.registration_fee > 0 ? '₹' + selectedEventForRegistration.registration_fee : 'Free' }}</span>
            </div>
          </div>

          <label class="flex items-start gap-3 pt-1 cursor-pointer">
            <input type="checkbox" v-model="regForm.confirmedTerms" required class="mt-1 h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500" />
            <span class="text-xs text-slate-600 leading-relaxed">
              I confirm my registration for this event and agree to follow all club regulations and arrival times.
            </span>
          </label>

          <div class="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
            <button type="button" @click="closeRegisterModal" class="rounded-xl border border-slate-200 px-4 py-2.5 text-xs font-bold text-slate-600 hover:bg-slate-50 transition">Cancel</button>
            <button type="submit" :disabled="busy === selectedEventForRegistration.id" class="rounded-xl bg-indigo-600 px-5 py-2.5 text-xs font-bold text-white shadow-md shadow-indigo-200 hover:bg-indigo-700 transition disabled:opacity-50">
              {{ busy === selectedEventForRegistration.id ? 'Registering...' : selectedEventForRegistration.registration_fee > 0 ? 'Proceed to Payment (₹' + selectedEventForRegistration.registration_fee + ')' : 'Confirm & Register' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script setup>
import { computed, onMounted, ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'
import { getSportImage } from '@/utils/sportImages'

const router = useRouter()
const auth = useAuthStore()
const events = ref([]),
  loading = ref(false),
  error = ref(''),
  busy = ref(null),
  activeTab = ref('all')

const showRegisterModal = ref(false)
const selectedEventForRegistration = ref(null)
const regForm = reactive({
  name: '',
  email: '',
  phone: '',
  category: 'Open',
  notes: '',
  confirmedTerms: false
})

const displayedEvents = computed(() => {
  if (activeTab.value === 'mine') {
    return events.value.filter(e => e.my_registration_status === 'registered')
  }
  return events.value
})
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

function register(e) {
  selectedEventForRegistration.value = e
  regForm.name = auth.user?.name || ''
  regForm.email = auth.user?.email || ''
  regForm.phone = auth.user?.phone || ''
  regForm.category = 'Open'
  regForm.notes = ''
  regForm.confirmedTerms = false
  showRegisterModal.value = true
}

function closeRegisterModal() {
  showRegisterModal.value = false
  selectedEventForRegistration.value = null
}

async function submitRegistration() {
  if (!selectedEventForRegistration.value) return
  if (!regForm.confirmedTerms) {
    alert('Please agree to the confirmation terms.')
    return
  }

  const evt = selectedEventForRegistration.value
  if (Number(evt.registration_fee || 0) > 0) {
    closeRegisterModal()
    router.push({
      name: 'member-checkout',
      query: { payment_type: 'event', reference_id: String(evt.id) },
    })
    return
  }

  busy.value = evt.id
  try {
    await api.post(`/events/${evt.id}/register`)
    closeRegisterModal()
    await load()
  } catch (x) {
    alert(x?.response?.data?.message || 'Unable to register.')
  } finally {
    busy.value = null
  }
}

async function cancel(e) {
  if (!confirm(`Are you sure you want to cancel your registration for "${e.title}"?`)) return
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
onMounted(async () => {
  if (!auth.user) await auth.restoreUser()
  await load()
})
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
