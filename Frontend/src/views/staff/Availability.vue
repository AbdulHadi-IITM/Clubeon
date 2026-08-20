<template>
  <div class="space-y-6">
    <div class="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
      <div>
        <p class="kicker">Live schedule</p>
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
<style scoped>
.panel {
  background: rgba(255, 255, 255, 0.92);
  border: 1px solid #dfe7f1;
  border-radius: 18px;
  box-shadow: 0 12px 35px rgba(51, 65, 85, 0.06);
}
.kicker {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #64748b;
}
.title {
  font-size: 28px;
  line-height: 1.15;
  font-weight: 800;
  letter-spacing: -0.035em;
  color: #172033;
}
.muted {
  color: #64748b;
}
.stat {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 18px;
}
.pill {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 6px 10px;
  font-size: 11px;
  font-weight: 700;
}
.btn {
  border-radius: 11px;
  padding: 10px 14px;
  font-size: 12px;
  font-weight: 700;
  transition: 0.2s;
}
.btn-primary2 {
  background: #4f46e5;
  color: white;
  box-shadow: 0 8px 18px rgba(79, 70, 229, 0.18);
}
.btn-soft {
  background: #f8fafc;
  color: #475569;
  border: 1px solid #dfe7f1;
}
.field2 {
  width: 100%;
  border: 1px solid #dbe4ef;
  border-radius: 11px;
  background: #f8fafc;
  padding: 10px 12px;
  color: #172033;
  outline: none;
}
.field2:focus {
  border-color: #818cf8;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}
</style>
