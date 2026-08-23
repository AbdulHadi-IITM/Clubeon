<template>
  <div class="space-y-6">
    <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold gradient-text">Bookings</h1>
        <p class="text-sm text-gray-500 mt-1">Manage the club's booking schedule.</p>
      </div>
      <div class="flex flex-col sm:flex-row gap-3">
        <ClubPicker v-model="clubId" @change="load" />
        <div>
          <label class="block text-xs text-gray-500 mb-2">Date</label
          ><input v-model="selectedDate" type="date" class="input-field" @change="load" />
        </div>
      </div>
    </div>
    <div v-if="error" class="glass p-4 text-red-400 text-sm">{{ error }}</div>
    <div class="glass overflow-hidden">
      <div class="p-4 border-b border-white/5 flex items-center justify-between">
        <p class="text-sm text-gray-400">{{ bookings.length }} bookings</p>
        <button class="text-xs text-primary-400" @click="load">Refresh</button>
      </div>
      <div v-if="loading" class="p-10 text-center text-gray-500">Loading bookings...</div>
      <div v-else-if="!bookings.length" class="p-10 text-center text-gray-500">
        No bookings found.
      </div>
      <div v-else class="overflow-x-auto">
        <table class="w-full text-left">
          <thead class="text-xs text-gray-500 border-b border-white/5">
            <tr>
              <th class="p-4">Time</th>
              <th class="p-4">Court</th>
              <th class="p-4">Member</th>
              <th class="p-4">Status</th>
              <th class="p-4">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="b in bookings" :key="b.id" class="border-b border-white/5">
              <td class="p-4 text-sm text-gray-300">
                {{ time(b.start_time) }} – {{ time(b.end_time) }}
              </td>
              <td class="p-4 text-sm text-gray-300">
                <div class="flex items-center gap-2.5">
                  <img :src="getSportImage(b.court_name)" :alt="b.court_name" class="w-8 h-8 rounded-lg object-cover shadow-sm border border-white/10 shrink-0" />
                  <span>{{ b.court_name }}</span>
                </div>
              </td>
              <td class="p-4">
                <p class="text-sm text-gray-200">{{ b.user_name }}</p>
                <p class="text-xs text-gray-500">{{ b.user_email }}</p>
              </td>
              <td class="p-4">
                <span class="text-xs px-2 py-1 rounded-full bg-white/5 text-gray-300">{{
                  b.status
                }}</span>
              </td>
              <td class="p-4 flex items-center gap-3">
                <router-link
                  :to="{
                    name: 'staff-booking-detail',
                    params: { bookingId: b.id },
                    query: { club_id: clubId },
                  }"
                  class="text-xs text-primary-400"
                  >View</router-link
                ><button
                  v-if="b.status === 'active'"
                  class="text-xs text-emerald-400"
                  @click="checkIn(b)"
                >
                  Check in</button
                ><span v-else class="text-xs text-gray-600">—</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import api from '@/api/axios'
import ClubPicker from './components/ClubPicker.vue'
import { today, time, errorMessage } from './_helpers'
import { getSportImage } from '@/utils/sportImages'
const clubId = ref('')
const selectedDate = ref(today())
const bookings = ref([])
const loading = ref(false)
const error = ref('')
async function load() {
  if (!clubId.value) return
  loading.value = true
  error.value = ''
  try {
    bookings.value = (
      await api.get('/staff/bookings', {
        params: { club_id: clubId.value, date: selectedDate.value },
      })
    ).data
  } catch (e) {
    error.value = errorMessage(e, 'Unable to load bookings.')
  } finally {
    loading.value = false
  }
}
async function checkIn(b) {
  try {
    await api.post('/staff/attendance/check-in', { booking_id: b.id })
    await load()
    alert(`${b.user_name} checked in successfully.`)
  } catch (e) {
    error.value = errorMessage(e, 'Unable to check in member.')
  }
}
</script>
