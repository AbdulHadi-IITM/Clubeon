<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between gap-4">
      <div>
        <router-link to="/staff/bookings" class="text-xs text-indigo-600"
          >← Back to bookings</router-link
        >
        <h1 class="text-2xl font-bold title mt-2">Booking Details</h1>
        <p class="text-sm text-slate-500 mt-1">Operational details for the selected booking.</p>
      </div>
      <ClubPicker v-model="clubId" @change="load" />
    </div>
    <div v-if="error" class="state-error">{{ error }}</div>
    <div v-if="loading" class="panel state-note">Loading booking...</div>
    <template v-else-if="booking">
      <section class="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <div class="panel p-5 lg:col-span-2">
          <div class="flex items-start justify-between gap-4">
            <div>
              <p class="text-xs text-slate-500">Booking #{{ booking.id }}</p>
              <h2 class="text-xl font-semibold text-slate-900 mt-1">{{ booking.court_name }}</h2>
              <p class="text-sm text-slate-500 mt-1">{{ booking.club_name }}</p>
            </div>
            <span class="text-xs px-3 py-1.5 rounded-full bg-slate-100 text-slate-700">{{
              booking.status
            }}</span>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-7">
            <div>
              <p class="text-xs text-slate-500">Date</p>
              <p class="text-sm text-slate-900 mt-1">{{ formatDate(booking.date) }}</p>
            </div>
            <div>
              <p class="text-xs text-slate-500">Start</p>
              <p class="text-sm text-slate-900 mt-1">{{ time(booking.start_time) }}</p>
            </div>
            <div>
              <p class="text-xs text-slate-500">End</p>
              <p class="text-sm text-slate-900 mt-1">{{ time(booking.end_time) }}</p>
            </div>
            <div>
              <p class="text-xs text-slate-500">Court ID</p>
              <p class="text-sm text-slate-900 mt-1">#{{ booking.court_id }}</p>
            </div>
          </div>
        </div>
        <div class="panel p-5">
          <p class="text-xs uppercase tracking-wider text-slate-500">Member</p>
          <h2 class="text-lg font-semibold text-slate-900 mt-2">{{ booking.user_name }}</h2>
          <p class="text-sm text-slate-500 mt-1 break-all">{{ booking.user_email }}</p>
          <router-link
            :to="{
              name: 'staff-member-detail',
              params: { userId: booking.user_id },
              query: { club_id: clubId },
            }"
            class="inline-block mt-5 text-xs text-indigo-600"
            >View member →</router-link
          >
        </div>
      </section>
    </template>
    <div v-else class="glass p-10 text-center text-gray-500">
      Please select a club to view booking details.
    </div>
  </div>
</template>
<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/axios'
import ClubPicker from './components/ClubPicker.vue'
import { date as formatDate, time, errorMessage } from './_helpers'

const route = useRoute()
const clubId = ref(route.query.club_id ? String(route.query.club_id) : '')
const booking = ref(null)
const loading = ref(false)
const error = ref('')
const bookingId = computed(() => Number(route.params.bookingId || (window.location.pathname.match(/bookings\/(\d+)/) || [])[1]))
async function load() {
  if (!bookingId.value) return
  
  if (!clubId.value) {
    try {
      const clubsRes = await api.get('/clubs')
      if (Array.isArray(clubsRes.data) && clubsRes.data.length > 0) {
        clubId.value = String(clubsRes.data[0].id)
      }
    } catch (e) {
      console.warn('Unable to auto-fetch clubs:', e)
    }
  }

  if (!clubId.value) return

  loading.value = true
  error.value = ''
  try {
    booking.value = (
      await api.get(`/staff/bookings/${bookingId.value}`, { params: { club_id: clubId.value } })
    ).data
  } catch (e) {
    error.value = errorMessage(e, 'Unable to load booking details.')
  } finally {
    loading.value = false
  }
}

watch(() => clubId.value, () => {
  if (clubId.value) {
    load()
  }
})

onMounted(load)
</script>
