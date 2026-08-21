<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between gap-4">
      <div>
        <router-link to="/staff/bookings" class="text-xs text-primary-400"
          >← Back to bookings</router-link
        >
        <h1 class="text-2xl font-bold gradient-text mt-2">Booking Details</h1>
        <p class="text-sm text-gray-500 mt-1">Operational details for the selected booking.</p>
      </div>
      <ClubPicker v-model="clubId" @change="load" />
    </div>
    <div v-if="error" class="glass p-4 text-sm text-red-400">{{ error }}</div>
    <div v-if="loading" class="glass p-10 text-center text-gray-500">Loading booking...</div>
    <template v-else-if="booking">
      <section class="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <div class="glass p-5 lg:col-span-2">
          <div class="flex items-start justify-between gap-4">
            <div>
              <p class="text-xs text-gray-500">Booking #{{ booking.id }}</p>
              <h2 class="text-xl font-semibold text-white mt-1">{{ booking.court_name }}</h2>
              <p class="text-sm text-gray-500 mt-1">{{ booking.club_name }}</p>
            </div>
            <span class="text-xs px-3 py-1.5 rounded-full bg-white/5 text-gray-300">{{
              booking.status
            }}</span>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-7">
            <div>
              <p class="text-xs text-gray-500">Date</p>
              <p class="text-sm text-gray-200 mt-1">{{ formatDate(booking.date) }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Start</p>
              <p class="text-sm text-gray-200 mt-1">{{ time(booking.start_time) }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">End</p>
              <p class="text-sm text-gray-200 mt-1">{{ time(booking.end_time) }}</p>
            </div>
            <div>
              <p class="text-xs text-gray-500">Court ID</p>
              <p class="text-sm text-gray-200 mt-1">#{{ booking.court_id }}</p>
            </div>
          </div>
        </div>
        <div class="glass p-5">
          <p class="text-xs uppercase tracking-wider text-gray-500">Member</p>
          <h2 class="text-lg font-semibold text-white mt-2">{{ booking.user_name }}</h2>
          <p class="text-sm text-gray-500 mt-1 break-all">{{ booking.user_email }}</p>
          <router-link
            :to="{
              name: 'staff-member-detail',
              params: { userId: booking.user_id },
              query: { club_id: clubId },
            }"
            class="inline-block mt-5 text-xs text-primary-400"
            >View member →</router-link
          >
        </div>
      </section>
    </template>
  </div>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/axios'
import ClubPicker from './components/ClubPicker.vue'
import { date as formatDate, time, errorMessage } from './_helpers'
const route = useRoute()
const clubId = ref(route.query.club_id ? String(route.query.club_id) : '')
const booking = ref(null)
const loading = ref(false)
const error = ref('')
const bookingId = Number((window.location.pathname.match(/bookings\/(\d+)/) || [])[1])
async function load() {
  if (!clubId.value || !bookingId) return
  loading.value = true
  error.value = ''
  try {
    booking.value = (
      await api.get(`/staff/bookings/${bookingId}`, { params: { club_id: clubId.value } })
    ).data
  } catch (e) {
    error.value = errorMessage(e, 'Unable to load booking.')
  } finally {
    loading.value = false
  }
}
onMounted(load)
</script>
