<template>
  <div class="space-y-6">
    <div class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold title">Events</h1>
        <p class="text-sm text-slate-500 mt-1">
          View upcoming club events and registered participants.
        </p>
      </div>
      <div class="flex flex-col sm:flex-row gap-3">
        <ClubPicker v-model="clubId" @change="load" />
        <div>
          <label class="block text-xs text-slate-500 mb-2">Date</label
          ><input v-model="selectedDate" type="date" class="input-field" @change="load" />
        </div>
      </div>
    </div>
    <div v-if="error" class="state-error">{{ error }}</div>
    <div v-if="loading" class="panel state-note">Loading events...</div>
    <div v-else-if="!events.length" class="panel state-note">
      No events found for this club/date.
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
      <article
        v-for="event in events"
        :key="event.id"
        class="rounded-2xl border border-slate-200 bg-slate-900/60 overflow-hidden flex flex-col justify-between"
      >
        <div class="relative h-32 w-full overflow-hidden bg-slate-950">
          <img :src="getSportImage(event.title || event.sport)" :alt="event.title" class="h-full w-full object-cover opacity-85" />
          <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent"></div>
          <span class="absolute top-3 right-3 text-xs rounded-full bg-slate-900/80 backdrop-blur-sm px-2.5 py-1 text-white border border-slate-200">{{ event.status || 'upcoming' }}</span>
        </div>
        <div class="p-5 flex-1 flex flex-col justify-between">
          <div>
            <p class="text-xs text-indigo-600 font-bold uppercase tracking-wider">{{ formatDate(event.date) }}</p>
            <h2 class="font-bold text-white mt-1 text-base">{{ event.title }}</h2>
            <p class="text-xs text-slate-500 mt-2 line-clamp-2">
              {{ event.description || 'No description provided.' }}
            </p>
          </div>
          <div>
            <div class="grid grid-cols-2 gap-3 mt-4 text-xs pt-3 border-t border-slate-200">
              <div>
                <p class="text-slate-500">Time</p>
                <p class="text-slate-700 font-semibold mt-0.5">
                  {{ time(event.start_time) }}–{{ time(event.end_time) }}
                </p>
              </div>
              <div>
                <p class="text-slate-500">Participants</p>
                <p class="text-slate-700 font-semibold mt-0.5">
                  {{ event.registered_count }}{{ event.max_attendees ? ` / ${event.max_attendees}` : '' }}
                </p>
              </div>
            </div>
            <router-link
              :to="{
                name: 'staff-event-detail',
                params: { eventId: event.id },
                query: { club_id: clubId },
              }"
              class="mt-4 block text-center rounded-xl bg-indigo-50 py-2.5 text-xs font-bold text-indigo-600 hover:bg-indigo-100 transition"
            >View event & participants</router-link>
          </div>
        </div>
      </article>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import api from '@/api/axios'
import ClubPicker from './components/ClubPicker.vue'
import { date as formatDate, time, errorMessage } from './_helpers'
import { getSportImage } from '@/utils/sportImages'
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
