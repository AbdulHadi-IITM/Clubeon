<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between gap-4">
      <div>
        <router-link to="/staff/members" class="text-xs text-indigo-600"
          >← Back to members</router-link
        >
        <h1 class="text-2xl font-bold title mt-2">Member Details</h1>
        <p class="text-sm text-slate-500 mt-1">
          Operational member information for front-desk support.
        </p>
      </div>
      <ClubPicker v-model="clubId" @change="load" />
    </div>
    <div v-if="error" class="state-error">{{ error }}</div>
    <div v-if="loading" class="panel state-note">Loading member...</div>
    <template v-else-if="member">
      <section class="panel p-6 flex flex-col md:flex-row md:items-center gap-5">
        <div
          class="w-16 h-16 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center text-xl font-bold"
        >
          {{ initial }}
        </div>
        <div class="flex-1">
          <h2 class="text-xl font-semibold text-slate-900">{{ member.name }}</h2>
          <p class="text-sm text-slate-500 mt-1">{{ member.email }}</p>
          <p class="text-xs text-slate-400 mt-2">
            Member since {{ formatDate(member.created_at?.slice(0, 10)) }}
          </p>
        </div>
        <div class="grid grid-cols-2 gap-3">
          <div class="rounded-xl bg-slate-50 border border-slate-200 px-4 py-3">
            <p class="text-xs text-slate-500">Bookings</p>
            <p class="text-lg font-semibold text-slate-900 mt-1">{{ member.booking_count }}</p>
          </div>
          <div class="rounded-xl bg-slate-50 border border-slate-200 px-4 py-3">
            <p class="text-xs text-slate-500">Attendance</p>
            <p class="text-lg font-semibold text-slate-900 mt-1">{{ member.attendance_count }}</p>
          </div>
        </div>
      </section>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-5">
        <section class="panel p-5 lg:col-span-2">
          <div class="flex items-center justify-between mb-4">
            <h2 class="font-semibold text-slate-900">Recent Bookings</h2>
            <span class="text-xs text-slate-500">Last 10</span>
          </div>
          <div v-if="!member.bookings?.length" class="py-8 text-center text-slate-500 text-sm">
            No bookings found.
          </div>
          <div v-else class="space-y-2">
            <div
              v-for="b in member.bookings"
              :key="b.id"
              class="flex items-center justify-between gap-4 rounded-xl border border-slate-200 bg-slate-50 p-3"
            >
              <div>
                <p class="text-sm text-slate-900">{{ b.court_name }}</p>
                <p class="text-xs text-slate-500 mt-1">
                  {{ formatDate(b.date) }} · {{ time(b.start_time) }}–{{ time(b.end_time) }}
                </p>
              </div>
              <router-link
                :to="{
                  name: 'staff-booking-detail',
                  params: { bookingId: b.id },
                  query: { club_id: clubId },
                }"
                class="text-xs text-indigo-600"
                >View</router-link
              >
            </div>
          </div>
        </section>
        <section class="panel p-5">
          <h2 class="font-semibold text-slate-900">Membership</h2>
          <div v-if="member.active_membership" class="mt-4">
            <p class="text-lg font-semibold text-slate-900">{{ member.active_membership.plan_name }}</p>
            <p class="text-xs text-emerald-400 mt-1">{{ member.active_membership.status }}</p>
            <div class="mt-5 space-y-3 text-sm">
              <div class="flex justify-between">
                <span class="text-slate-500">Start</span
                ><span class="text-slate-700">{{
                  formatDate(member.active_membership.start_date)
                }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-500">Expires</span
                ><span class="text-slate-700">{{
                  formatDate(member.active_membership.end_date)
                }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-500">Auto renew</span
                ><span class="text-slate-700">{{
                  member.active_membership.auto_renew ? 'On' : 'Off'
                }}</span>
              </div>
            </div>
          </div>
          <div v-else class="py-8 text-center text-sm text-slate-500">No active membership.</div>
        </section>
      </div>
    </template>
    <div v-else class="glass p-10 text-center text-gray-500">
      Please select a club to view member details.
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
const member = ref(null)
const loading = ref(false)
const error = ref('')
const userId = computed(() => Number(route.params.userId || (window.location.pathname.match(/members\/(\d+)/) || [])[1]))
const initial = computed(() => (member.value?.name || 'M').charAt(0).toUpperCase())

async function load() {
  if (!userId.value) return
  
  // If clubId is not set, try to fetch the first available club
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
    member.value = (
      await api.get(`/staff/members/${userId.value}`, { params: { club_id: clubId.value } })
    ).data
  } catch (e) {
    error.value = errorMessage(e, 'Unable to load member details.')
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
