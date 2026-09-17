import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/axios'

export const useCourtStore = defineStore('courts', () => {
  const courts = ref([])
  const club = ref(null)
  const loading = ref(false)

  function reset() {
    courts.value = []
    club.value = null
    loading.value = false
  }

  async function fetchCourts() {
    // Clear stale data immediately
    courts.value = []
    club.value = null
    loading.value = true
    try {
      const res = await api.get('/clubs/courts')
      club.value = res.data.club
      courts.value = res.data.courts
    } catch (err) {
      console.error('Failed to fetch courts', err)
    } finally {
      loading.value = false
    }
  }

  async function createClub(payload) {
    loading.value = true
    try {
      await api.post('/clubs', payload)
      await fetchCourts()
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data?.message || 'Failed to create club' }
    } finally {
      loading.value = false
    }
  }

  async function createCourt(payload) {
    loading.value = true
    try {
      await api.post('/clubs/courts', payload)
      await fetchCourts()
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data?.message || 'Failed to create court' }
    } finally {
      loading.value = false
    }
  }

  async function updateCourt(courtId, payload) {
    loading.value = true
    try {
      await api.put(`/clubs/courts/${courtId}`, payload)
      await fetchCourts()
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data?.message || 'Failed to update court' }
    } finally {
      loading.value = false
    }
  }

  async function deleteCourt(courtId) {
    loading.value = true
    try {
      await api.delete(`/clubs/courts/${courtId}`)
      await fetchCourts()
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data?.message || 'Failed to delete court' }
    } finally {
      loading.value = false
    }
  }

  async function updateClubSettings(payload) {
    loading.value = true
    try {
      await api.put(`/clubs/${club.value.id}`, payload)
      await fetchCourts() // refresh everything
      return { success: true }
    } catch (err) {
      return {
        success: false,
        error: err.response?.data?.message || 'Failed to update club settings',
      }
    } finally {
      loading.value = false
    }
  }

  const activeCourts = computed(() => courts.value.filter((c) => c.is_active))
  const sportsTypes = computed(() => [
    { value: 'tennis', label: 'Tennis', icon: '🎾' },
    { value: 'badminton', label: 'Badminton', icon: '🏸' },
    { value: 'basketball', label: 'Basketball', icon: '🏀' },
    { value: 'golf', label: 'Golf', icon: '⛳' },
    { value: 'football', label: 'Football', icon: '⚽' },
    { value: 'pickleball', label: 'Pickleball', icon: '🟡' },
    { value: 'padel', label: 'Padel', icon: '🔵' },
    { value: 'squash', label: 'Squash', icon: '🏸' },
    { value: 'volleyball', label: 'Volleyball', icon: '🏐' },
    { value: 'multi-purpose', label: 'Multi-purpose', icon: '🏟️' },
  ])

  return {
    courts,
    club,
    loading,
    reset,
    fetchCourts,
    createCourt,
    updateCourt,
    deleteCourt,
    updateClubSettings,
    createClub,
    activeCourts,
    sportsTypes,
  }
})
