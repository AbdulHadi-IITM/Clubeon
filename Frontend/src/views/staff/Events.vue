<template>
  <div class="space-y-6">
    <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold gradient-text">Events</h1>
        <p class="text-sm text-gray-500 mt-1">
          View upcoming club events and registered participants.
        </p>
      </div>
      <div class="flex flex-col sm:flex-row gap-3">
        <ClubPicker v-model="clubId" @change="load" />
        <div>
          <label class="block text-xs text-gray-500 mb-2">Date</label
          ><input v-model="selectedDate" type="date" class="input-field" @change="load" />
        </div>
      </div>
    </div>
    <div v-if="error" class="glass p-4 text-sm text-red-400">{{ error }}</div>
    <div v-if="loading" class="glass p-10 text-center text-gray-500">Loading events...</div>
    <div v-else-if="!events.length" class="glass p-10 text-center text-gray-500">
      No events found for this club/date.
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
      <article v-for="event in events" :key="event.id" class="glass card-hover p-5">
        <div class="flex items-start justify-between gap-3">
          <div>
            <p class="text-xs text-primary-400">{{ formatDate(event.date) }}</p>
            <h2 class="font-semibold text-white mt-1">{{ event.title }}</h2>
          </div>
          <span class="text-xs rounded-full bg-white/5 px-2.5 py-1 text-gray-400">{{
            event.status
          }}</span>
        </div>
        <p class="text-sm text-gray-500 mt-4 line-clamp-2">
          {{ event.description || 'No description provided.' }}
        </p>
        <div class="grid grid-cols-2 gap-3 mt-5 text-xs">
          <div>
            <p class="text-gray-600">Time</p>
            <p class="text-gray-300 mt-1">
              {{ time(event.start_time) }}–{{ time(event.end_time) }}
            </p>
          </div>
          <div>
            <p class="text-gray-600">Participants</p>
            <p class="text-gray-300 mt-1">
              {{ event.registered_count
              }}{{ event.max_attendees ? ` / ${event.max_attendees}` : '' }}
            </p>
          </div>
        </div>
        <router-link
          :to="{
            name: 'staff-event-detail',
            params: { eventId: event.id },
            query: { club_id: clubId },
          }"
          class="mt-5 block text-center rounded-xl bg-primary-500/10 py-2.5 text-xs font-medium text-primary-400 hover:bg-primary-500/15"
          >View event & participants</router-link
        >
      </article>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import api from '@/api/axios'
import ClubPicker from './components/ClubPicker.vue'
import { today, date as formatDate, time, errorMessage } from './_helpers'
const clubId = ref('')
const selectedDate = ref('')
const events = ref([])
const loading = ref(false)
const error = ref('')
async function load() {
  if (!clubId.value) return
  loading.value = true
  error.value = ''
  try {
    const r = await api.get('/staff/events', {
      params: { club_id: clubId.value, date: selectedDate.value || undefined },
    })
    events.value = Array.isArray(r.data) ? r.data : []
  } catch (e) {
    error.value = errorMessage(e, 'Unable to load events.')
  } finally {
    loading.value = false
  }
}
</script>
