<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between gap-4">
      <div>
        <router-link to="/staff/members" class="text-xs text-primary-400"
          >← Back to members</router-link
        >
        <h1 class="text-2xl font-bold gradient-text mt-2">Member Details</h1>
        <p class="text-sm text-gray-500 mt-1">
          Operational member information for front-desk support.
        </p>
      </div>
      <ClubPicker v-model="clubId" @change="load" />
    </div>
    <div v-if="error" class="glass p-4 text-sm text-red-400">{{ error }}</div>
    <div v-if="loading" class="glass p-10 text-center text-gray-500">Loading member...</div>
    <template v-else-if="member">
      <section class="glass p-6 flex flex-col md:flex-row md:items-center gap-5">
        <div
          class="w-16 h-16 rounded-2xl bg-primary-500/10 text-primary-400 flex items-center justify-center text-xl font-bold"
        >
          {{ initial }}
        </div>
        <div class="flex-1">
          <h2 class="text-xl font-semibold text-white">{{ member.name }}</h2>
          <p class="text-sm text-gray-500 mt-1">{{ member.email }}</p>
          <p class="text-xs text-gray-600 mt-2">
            Member since {{ formatDate(member.created_at?.slice(0, 10)) }}
          </p>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div class="rounded-xl bg-white/[0.03] border border-white/5 px-4 py-3">
            <p class="text-xs text-gray-500">Bookings</p>
            <p class="text-lg font-semibold text-white mt-1">{{ member.booking_count }}</p>
          </div>
          <div class="rounded-xl bg-white/[0.03] border border-white/5 px-4 py-3">
            <p class="text-xs text-gray-500">Attendance</p>
            <p class="text-lg font-semibold text-white mt-1">{{ member.attendance_count }}</p>
          </div>
        </div>
      </section>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <section class="glass p-5 lg:col-span-2">
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-semibold text-gray-200">Recent Bookings</h2>
            <span class="text-xs text-gray-500">Last 10</span>
          </div>
          <div v-if="!member.bookings?.length" class="py-8 text-center text-gray-500 text-sm">
            No bookings found.
          </div>
          <div v-else class="space-y-2">
            <div
              v-for="b in member.bookings"
              :key="b.id"
              class="flex items-center justify-between gap-4 rounded-xl border border-white/5 bg-white/[0.02] p-3"
            >
              <div>
                <p class="text-sm text-gray-200">{{ b.court_name }}</p>
                <p class="text-xs text-gray-500 mt-1">
                  {{ formatDate(b.date) }} · {{ time(b.start_time) }}–{{ time(b.end_time) }}
                </p>
              </div>
              <router-link
                :to="{
                  name: 'staff-booking-detail',
                  params: { bookingId: b.id },
                  query: { club_id: clubId },
                }"
                class="text-xs text-primary-400"
                >View</router-link
              >
            </div>
          </div>
        </section>
        <section class="glass p-5">
          <h2 class="font-semibold text-gray-200">Membership</h2>
          <div v-if="member.active_membership" class="mt-4">
            <p class="text-lg font-semibold text-white">{{ member.active_membership.plan_name }}</p>
            <p class="text-xs text-emerald-400 mt-1">{{ member.active_membership.status }}</p>
            <div class="mt-5 space-y-3 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-500">Start</span
                ><span class="text-gray-300">{{
                  formatDate(member.active_membership.start_date)
                }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Expires</span
                ><span class="text-gray-300">{{
                  formatDate(member.active_membership.end_date)
                }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Auto renew</span
                ><span class="text-gray-300">{{
                  member.active_membership.auto_renew ? 'On' : 'Off'
                }}</span>
              </div>
            </div>
          </div>
          <div v-else class="py-8 text-center text-sm text-gray-500">No active membership.</div>
        </section>
      </div>
    </template>
  </div>
</template>
<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '@/api/axios'
import ClubPicker from './components/ClubPicker.vue'
import { date as formatDate, time, errorMessage } from './_helpers'
const route = useRoute()
const clubId = ref(route.query.club_id ? String(route.query.club_id) : '')
const member = ref(null)
const loading = ref(false)
const error = ref('')
const userId = Number((window.location.pathname.match(/members\/(\d+)/) || [])[1])
const initial = computed(() => (member.value?.name || 'M').charAt(0).toUpperCase())
async function load() {
  if (!clubId.value || !userId) return
  loading.value = true
  error.value = ''
  try {
    member.value = (
      await api.get(`/staff/members/${userId}`, { params: { club_id: clubId.value } })
    ).data
  } catch (e) {
    error.value = errorMessage(e, 'Unable to load member.')
  } finally {
    loading.value = false
  }
}
onMounted(load)
</script>
