import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/axios'

export const useBookingStore = defineStore('bookings', () => {
  const bookings = ref([])
  const loading = ref(false)
  const error = ref(null)

  const upcomingBookings = computed(() =>
    bookings.value.filter(
      booking =>
        booking.status !== 'cancelled' &&
        booking.status !== 'released',
    ),
  )

  async function loadBookings() {
    loading.value = true
    error.value = null

    try {
      const { data } = await api.get('/bookings')
      bookings.value = data
      return data
    } catch (err) {
      error.value =
        err.response?.data?.message ||
        err.message ||
        'Failed to load bookings'

      throw err
    } finally {
      loading.value = false
    }
  }

  async function createBooking({
    court_id,
    booking_date,
    start_time,
    end_time,
  }) {
    loading.value = true
    error.value = null

    try {
      const { data } = await api.post('/bookings', {
        court_id,
        booking_date,
        start_time,
        end_time,
      })

      await loadBookings()

      return data
    } catch (err) {
      error.value =
        err.response?.data?.message ||
        err.message ||
        'Failed to create booking'

      throw err
    } finally {
      loading.value = false
    }
  }

  async function releaseBooking(bookingId) {
    loading.value = true
    error.value = null

    try {
      const { data } = await api.post(`/bookings/${bookingId}/release`)

      await loadBookings()

      return data
    } catch (err) {
      error.value =
        err.response?.data?.message ||
        err.message ||
        'Failed to release booking'

      throw err
    } finally {
      loading.value = false
    }
  }

  function getUserBookings() {
    return bookings.value
  }

  function reset() {
    bookings.value = []
    loading.value = false
    error.value = null
  }

  return {
    bookings,
    loading,
    error,

    upcomingBookings,

    loadBookings,
    createBooking,
    releaseBooking,
    getUserBookings,
    reset,
  }
})