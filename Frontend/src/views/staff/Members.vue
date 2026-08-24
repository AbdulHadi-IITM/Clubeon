<template>
  <div class="space-y-6">
    <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold title">Members</h1>
        <p class="text-sm text-slate-500 mt-1">Members who have bookings at the selected club.</p>
      </div>
      <ClubPicker v-model="clubId" @change="load" />
    </div>
    <div class="panel p-4">
      <input v-model="search" class="input-field" placeholder="Search member by name or email" />
    </div>
    <div v-if="error" class="state-error">{{ error }}</div>
    <div v-if="loading" class="panel state-note">Loading members...</div>
    <div v-else-if="!filtered.length" class="panel state-note">
      No members found.
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
      <article v-for="m in filtered" :key="m.id" class="panel card-hover p-5">
        <div class="flex items-center gap-3">
          <div
            class="w-11 h-11 rounded-full bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold"
          >
            {{ m.name?.charAt(0)?.toUpperCase() || 'M' }}
          </div>
          <div class="min-w-0">
            <h2 class="font-medium text-slate-900 truncate">{{ m.name }}</h2>
            <p class="text-xs text-slate-500 truncate">{{ m.email }}</p>
          </div>
        </div>
        <div class="mt-5 pt-4 border-t border-slate-200 flex justify-between">
          <span class="text-xs text-slate-500">Bookings</span
          ><span class="text-sm font-semibold text-slate-900">{{ m.booking_count }}</span>
        </div>
        <router-link
          :to="{
            name: 'staff-member-detail',
            params: { userId: m.id },
            query: { club_id: clubId },
          }"
          class="mt-4 block text-center rounded-xl bg-indigo-50 py-2 text-xs text-indigo-600 hover:bg-indigo-100"
          >View member</router-link
        >
      </article>
    </div>
  </div>
</template>
<script setup>
import { computed, ref } from 'vue'
import api from '@/api/axios'
import ClubPicker from './components/ClubPicker.vue'
import { errorMessage } from './_helpers'
const clubId = ref('')
const members = ref([])
const search = ref('')
const loading = ref(false)
const error = ref('')
const filtered = computed(() => {
  const q = search.value.toLowerCase().trim()
  return !q
    ? members.value
    : members.value.filter((m) => `${m.name} ${m.email}`.toLowerCase().includes(q))
})
async function load() {
  if (!clubId.value) return
  loading.value = true
  error.value = ''
  try {
    members.value = (await api.get('/staff/members', { params: { club_id: clubId.value } })).data
  } catch (e) {
    error.value = errorMessage(e, 'Unable to load members.')
  } finally {
    loading.value = false
  }
}
</script>
