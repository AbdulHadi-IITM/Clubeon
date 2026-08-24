<template>
  <div class="space-y-6">
    <div>
      <p class="kicker">Member workspace</p>
      <h1 class="title mt-1">Welcome back, {{ firstName }}</h1>
      <p class="muted mt-2 text-sm">
        Your next reservation, activity and club events in one place.
      </p>
    </div>
    <div v-if="error" class="panel p-4 text-sm text-red-600">{{ error }}</div>
    <section class="panel overflow-hidden">
      <div class="p-6 md:p-7 bg-gradient-to-r from-indigo-50 to-emerald-50">
        <p class="kicker">Next booking</p>
        <div
          v-if="nextBooking"
          class="mt-3 flex flex-col gap-4 md:flex-row md:items-end md:justify-between"
        >
          <div>
            <h2 class="text-xl font-extrabold text-slate-900">{{ nextBooking.court_name }}</h2>
            <p class="mt-1 text-sm text-slate-600">{{ nextBooking.club_name }}</p>
            <p class="mt-3 text-sm font-semibold text-slate-700">
              {{ formatDate(nextBooking.date) }} · {{ formatTime(nextBooking.start_time) }} –
              {{ formatTime(nextBooking.end_time) }}
            </p>
          </div>
          <router-link to="/member/my-bookings" class="btn btn-primary2 text-center"
            >View booking</router-link
          >
        </div>
        <div v-else class="mt-3 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <p class="text-sm text-slate-600">You have no upcoming court reservation.</p>
          <router-link to="/member/book-court" class="btn btn-primary2 text-center"
            >Book a court</router-link
          >
        </div>
      </div>
    </section>
    <div class="grid gap-4 sm:grid-cols-3">
      <div class="stat">
        <p class="kicker">Upcoming</p>
        <p class="mt-2 text-3xl font-extrabold text-slate-900">{{ upcoming.length }}</p>
        <p class="muted mt-1 text-xs">court bookings</p>
      </div>
      <div class="stat">
        <p class="kicker">Total bookings</p>
        <p class="mt-2 text-3xl font-extrabold text-slate-900">{{ bookings.length }}</p>
        <p class="muted mt-1 text-xs">all reservations</p>
      </div>
      <div class="stat">
        <p class="kicker">Upcoming events</p>
        <p class="mt-2 text-3xl font-extrabold text-slate-900">{{ events.length }}</p>
        <p class="muted mt-1 text-xs">club activities</p>
      </div>
    </div>
    <!-- Club Announcements & Notice Board -->
    <section v-if="announcements.length > 0" class="panel p-5 sm:p-6 border-indigo-100 bg-gradient-to-br from-white via-indigo-50/20 to-blue-50/30">
      <div class="flex items-center justify-between pb-3 border-b border-slate-100">
        <div class="flex items-center gap-2">
          <span class="text-xl">📢</span>
          <div>
            <h2 class="font-bold text-slate-900 text-base sm:text-lg">Club Announcements & Notices</h2>
            <p class="muted text-xs">Official facility updates, maintenance, and club news</p>
          </div>
        </div>
        <span class="pill bg-indigo-50 text-indigo-700 font-semibold text-xs px-2.5 py-1">
          {{ announcements.length }} active
        </span>
      </div>

      <div class="mt-4 grid gap-3.5 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="item in announcements.slice(0, 3)"
          :key="item.id"
          class="rounded-xl border border-slate-200 bg-white p-4.5 shadow-sm hover:shadow-md transition duration-200 flex flex-col justify-between"
          :style="{
            borderLeftWidth: '4px',
            borderLeftColor: item.category === 'Maintenance' ? '#ef4444' : item.category === 'Policy' ? '#f59e0b' : item.category === 'Tournament' ? '#10b981' : item.category === 'Broadcast' ? '#8b5cf6' : '#2563eb'
          }"
        >
          <div>
            <div class="flex items-center justify-between gap-2 mb-2">
              <span 
                class="text-[11px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full"
                :class="{
                  'bg-rose-50 text-rose-700 border border-rose-200': item.category === 'Maintenance',
                  'bg-amber-50 text-amber-700 border border-amber-200': item.category === 'Policy',
                  'bg-emerald-50 text-emerald-700 border border-emerald-200': item.category === 'Tournament',
                  'bg-purple-50 text-purple-700 border border-purple-200': item.category === 'Broadcast',
                  'bg-blue-50 text-blue-700 border border-blue-200': !['Maintenance', 'Policy', 'Tournament', 'Broadcast'].includes(item.category)
                }"
              >
                {{ item.icon || '📢' }} {{ item.category || 'General' }}
              </span>
              <span class="text-[11px] text-slate-400 font-medium">{{ item.date || item.created_at?.slice(0, 10) }}</span>
            </div>
            <h3 class="font-bold text-slate-900 text-sm leading-snug line-clamp-2 mb-1.5">
              {{ item.title }}
            </h3>
            <p class="text-xs text-slate-600 leading-relaxed line-clamp-3">
              {{ item.body }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <div class="grid gap-5 lg:grid-cols-[1.35fr_.65fr]">
      <section class="panel p-5">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="font-bold text-slate-900">Upcoming bookings</h2>
            <p class="muted mt-1 text-xs">Your nearest reservations</p>
          </div>
          <router-link to="/member/my-bookings" class="text-xs font-bold text-indigo-600"
            >View all</router-link
          >
        </div>
        <div class="mt-4 space-y-3">
          <div
            v-for="b in upcoming.slice(0, 4)"
            :key="b.id"
            class="rounded-xl border border-slate-200 bg-slate-50/70 p-3 flex items-center justify-between gap-4 overflow-hidden"
          >
            <div class="flex items-center gap-3">
              <img :src="getSportImage(b.court_name)" :alt="b.court_name" class="h-12 w-16 rounded-lg object-cover shadow-sm flex-shrink-0" />
              <div>
                <p class="text-sm font-bold text-slate-900">{{ b.court_name }}</p>
                <p class="mt-0.5 text-xs text-slate-500">
                  {{ formatDate(b.date) }} · {{ formatTime(b.start_time) }}
                </p>
              </div>
            </div>
            <span class="pill bg-emerald-50 text-emerald-700">Confirmed</span>
          </div>
          <p v-if="!upcoming.length" class="py-8 text-center text-sm text-slate-500">
            No upcoming bookings.
          </p>
        </div>
      </section>
      <section class="panel p-5">
        <div class="flex items-center justify-between">
          <h2 class="font-bold text-slate-900">Quick actions</h2>
        </div>
        <div class="mt-4 grid gap-2">
          <router-link to="/member/book-court" class="btn btn-primary2 text-center"
            >Book a Court</router-link
          ><router-link to="/member/my-bookings" class="btn btn-soft text-center"
            >My Bookings</router-link
          ><router-link to="/member/events" class="btn btn-soft text-center"
            >Explore Events</router-link
          ><router-link to="/member/membership" class="btn btn-soft text-center"
            >Membership Plans</router-link
          >
        </div>
        <div class="mt-6 border-t border-slate-100 pt-5">
          <h3 class="text-sm font-bold text-slate-900">Next club event</h3>
          <div v-if="events[0]" class="mt-3 flex items-center gap-3">
            <img :src="getSportImage(events[0].title || events[0].sport)" :alt="events[0].title" class="h-12 w-16 rounded-lg object-cover shadow-sm flex-shrink-0" />
            <div>
              <p class="text-sm font-semibold text-slate-800">{{ events[0].title }}</p>
              <p class="mt-0.5 text-xs text-slate-500">
                {{ formatDate(events[0].date) }} · {{ formatTime(events[0].start_time) }}
              </p>
            </div>
          </div>
          <p v-else class="mt-3 text-xs text-slate-500">No upcoming events.</p>
        </div>
      </section>
    </div>
  </div>
</template>
<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '@/api/axios'
import { useAuthStore } from '@/stores/auth'
import { getSportImage } from '@/utils/sportImages'
import { useNotificationStore } from '@/stores/notifications'

const auth = useAuthStore()
const notificationStore = useNotificationStore()
const bookings = ref([])
const events = ref([])
const error = ref('')

const announcements = computed(() => notificationStore.announcements)
const firstName = computed(
  () => String(auth.user?.name || auth.user?.username || 'Member').split(' ')[0],
)
function dt(b) {
  return new Date(`${b.date}T${String(b.start_time || '00:00').slice(0, 8)}`)
}
const upcoming = computed(() =>
  bookings.value
    .filter((b) => b.status === 'active' && dt(b) >= new Date())
    .sort((a, b) => dt(a) - dt(b)),
)
const nextBooking = computed(() => upcoming.value[0] || null)
function formatDate(v) {
  if (!v) return '—'
  return new Intl.DateTimeFormat('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  }).format(new Date(`${v}T00:00:00`))
}
function formatTime(v) {
  if (!v) return '—'
  const [h, m] = String(v).split(':')
  const d = new Date()
  d.setHours(+h, +m || 0)
  return new Intl.DateTimeFormat('en-IN', { hour: 'numeric', minute: '2-digit' }).format(d)
}
async function load() {
  error.value = ''
  try {
    const [b, e] = await Promise.all([
      api.get('/bookings').catch(() => ({ data: [] })), 
      api.get('/events').catch(() => ({ data: [] })),
      notificationStore.fetchNotifications().catch(() => null)
    ])
    bookings.value = Array.isArray(b.data) ? b.data : []
    events.value = Array.isArray(e.data) ? e.data : []
  } catch (err) {
    error.value = err?.response?.data?.message || 'Unable to load dashboard.'
  }
}
onMounted(async () => {
  if (!auth.user) await auth.restoreUser()
  await load()
})
</script>
