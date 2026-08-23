<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between gap-4">
      <div>
        <router-link to="/staff/events" class="text-xs text-primary-400"
          >← Back to events</router-link
        >
        <h1 class="text-2xl font-bold gradient-text mt-2">Event Details</h1>
        <p class="text-sm text-gray-500 mt-1">Event information and registered participants.</p>
      </div>
      <ClubPicker v-model="clubId" @change="load" />
    </div>
    <div v-if="error" class="glass p-4 text-sm text-red-400">{{ error }}</div>
    <div v-if="loading" class="glass p-10 text-center text-gray-500">Loading event...</div>
    <template v-else-if="event">
      <section class="glass p-6">
        <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
          <div>
            <span class="text-xs text-primary-400">{{ formatDate(event.date) }}</span>
            <h2 class="text-2xl font-semibold text-white mt-1">{{ event.title }}</h2>
            <p class="text-sm text-gray-500 mt-2 max-w-3xl">
              {{ event.description || 'No description provided.' }}
            </p>
          </div>
          <span class="text-xs rounded-full bg-white/5 px-3 py-1.5 text-gray-400">{{
            event.status
          }}</span>
        </div>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-7">
          <div>
            <p class="text-xs text-gray-500">Time</p>
            <p class="text-sm text-gray-200 mt-1">
              {{ time(event.start_time) }}–{{ time(event.end_time) }}
            </p>
          </div>
          <div>
            <p class="text-xs text-gray-500">Registered</p>
            <p class="text-sm text-gray-200 mt-1">
              {{ event.registered_count
              }}{{ event.max_attendees ? ` / ${event.max_attendees}` : '' }}
            </p>
          </div>
          <div>
            <p class="text-xs text-gray-500">Fee</p>
            <p class="text-sm text-gray-200 mt-1">
              ₹{{ Number(event.registration_fee || 0).toFixed(2) }}
            </p>
          </div>
          <div>
            <p class="text-xs text-gray-500">Event ID</p>
            <p class="text-sm text-gray-200 mt-1">#{{ event.id }}</p>
          </div>
        </div>
      </section>
      <section class="glass overflow-hidden">
        <div class="p-5 border-b border-white/5 flex items-center justify-between">
          <h2 class="font-semibold text-gray-200">Participants</h2>
          <span class="text-xs text-gray-500"
            >{{ event.participants?.length || 0 }} registered</span
          >
        </div>
        <div v-if="!event.participants?.length" class="p-10 text-center text-sm text-gray-500">
          No registered participants.
        </div>
        <div v-else class="overflow-x-auto">
          <table class="w-full text-left">
            <thead class="text-xs text-gray-500 border-b border-white/5">
              <tr>
                <th class="p-4">Member</th>
                <th class="p-4">Email</th>
                <th class="p-4">Registered</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="p in event.participants"
                :key="p.registration_id"
                class="border-b border-white/5"
              >
                <td class="p-4 text-sm text-gray-200">{{ p.name }}</td>
                <td class="p-4 text-sm text-gray-400">{{ p.email }}</td>
                <td class="p-4 text-sm text-gray-400">{{ dateTime(p.registered_at) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </template>
    <div v-else class="glass p-10 text-center text-gray-500">
      Please select a club to view event details.
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
const event = ref(null)
const loading = ref(false)
const error = ref('')
const eventId = computed(() => Number(route.params.eventId || (window.location.pathname.match(/events\/(\d+)/) || [])[1]))

function dateTime(v) {
  if (!v) return '—'
  const d = new Date(String(v).replace(' ', 'T'))
  return Number.isNaN(d.getTime())
    ? v
    : new Intl.DateTimeFormat('en-IN', {
        day: 'numeric',
        month: 'short',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
      }).format(d)
}

async function load() {
  if (!eventId.value) return
  
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
    event.value = (
      await api.get(`/staff/events/${eventId.value}`, { params: { club_id: clubId.value } })
    ).data
  } catch (e) {
    error.value = errorMessage(e, 'Unable to load event details.')
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
