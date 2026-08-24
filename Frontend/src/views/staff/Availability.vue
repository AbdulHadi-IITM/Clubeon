<template>
  <div class="space-y-6">
    <div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
      <div>
        <p class="kicker">Today's schedule</p>
        <h1 class="title mt-1">Court Availability</h1>
        <p class="muted mt-2 text-sm">
          Scan every court and time slot from one operational matrix.
        </p>
      </div>
      <div class="flex gap-3">
        <ClubPicker v-model="clubId" @change="load" /><input
          v-model="selectedDate"
          type="date"
          class="field2 max-w-44"
          @change="load"
        />
      </div>
    </div>
    <div v-if="error" class="panel p-4 text-sm text-red-600">{{ error }}</div>
    <section class="panel overflow-hidden">
      <div class="flex flex-wrap items-center gap-4 border-b border-slate-100 p-4 text-xs">
        <span class="flex items-center gap-2 text-slate-600"
          ><i class="h-2.5 w-2.5 rounded-full bg-emerald-400"></i>Available</span
        ><span class="flex items-center gap-2 text-slate-600"
          ><i class="h-2.5 w-2.5 rounded-full bg-indigo-400"></i>Booked</span
        >
      </div>
      <div v-if="loading" class="p-12 text-center text-sm text-slate-500">
        Loading availability...
      </div>
      <div v-else-if="!courts.length" class="p-12 text-center text-sm text-slate-500">
        No availability returned.
      </div>
      <div v-else class="overflow-x-auto">
        <table class="min-w-max w-full">
          <tbody>
            <tr v-for="c in courts" :key="c.court_id" class="border-b border-slate-100">
              <th class="sticky left-0 z-10 min-w-44 bg-white p-4 text-left">
                <p class="text-sm font-bold text-slate-900">{{ c.court_name }}</p>
                <p class="mt-1 text-xs text-slate-400">{{ available(c) }} free slots</p>
              </th>
              <td v-for="s in c.slots || []" :key="s.start_time" class="p-2">
                <div
                  class="min-w-24 rounded-xl border px-3 py-3 text-center"
                  :class="
                    s.status === 'available'
                      ? 'border-emerald-200 bg-emerald-50'
                      : 'border-indigo-100 bg-indigo-50'
                  "
                >
                  <p class="text-xs font-bold text-slate-700">{{ time(s.start_time) }}</p>
                  <p
                    class="mt-1 text-[10px] font-bold"
                    :class="s.status === 'available' ? 'text-emerald-700' : 'text-indigo-700'"
                  >
                    {{ s.status === 'available' ? 'FREE' : 'BOOKED' }}
                  </p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import api from '@/api/axios'
import ClubPicker from './components/ClubPicker.vue'
import { today, time, errorMessage } from './_helpers'
const clubId = ref(''),
  selectedDate = ref(today()),
  courts = ref([]),
  loading = ref(false),
  error = ref('')
const available = (c) => (c.slots || []).filter((s) => s.status === 'available').length
async function load() {
  if (!clubId.value) return
  loading.value = true
  error.value = ''
  try {
    const r = await api.get('/availability/matrix', {
      params: { club_id: clubId.value, date: selectedDate.value },
    })
    courts.value = r.data?.courts || []
  } catch (e) {
    error.value = errorMessage(e, 'Unable to load availability.')
  } finally {
    loading.value = false
  }
}
</script>
