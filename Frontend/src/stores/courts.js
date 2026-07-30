import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/axios'

export const useCourtStore = defineStore('courts', () => {
  const courts = ref([])
  const loading = ref(false)

  async function fetchCourts() {
    loading.value = true
    try {
      const res = await api.get('/bookings/courts')
      courts.value = res.data
    } catch (err) {
      console.error("Failed to fetch courts", err)
    } finally {
      loading.value = false
    }
  }

  async function createCourt(payload) {
    loading.value = true
    try {
      await api.post('/bookings/courts', payload)
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
      await api.put(`/bookings/courts/${courtId}`, payload)
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
      await api.delete(`/bookings/courts/${courtId}`)
      await fetchCourts()
      return { success: true }
    } catch (err) {
      return { success: false, error: err.response?.data?.message || 'Failed to delete court' }
    } finally {
      loading.value = false
    }
  }

  return { courts, loading, fetchCourts, createCourt, updateCourt, deleteCourt }
})
