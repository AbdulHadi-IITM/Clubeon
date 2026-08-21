import { defineStore } from 'pinia'
import api from '@/api/axios'

export const useCourtStore = defineStore('courts', {
  state: () => ({
    club: null,
    courts: [],
    loading: false,
    error: null,
  }),

  getters: {
    activeCourts: (state) =>
      state.courts.filter((court) => court.is_active),

    inactiveCourts: (state) =>
      state.courts.filter((court) => !court.is_active),

    totalCourts: (state) => state.courts.length,
  },

  actions: {
    getErrorMessage(error, fallback = 'Something went wrong') {
      return (
        error?.response?.data?.message ||
        error?.response?.data?.error ||
        error?.response?.data?.msg ||
        fallback
      )
    },

    normalizeClub(data) {
      if (!data) return null

      return data.club ?? data.data ?? data
    },

    normalizeCourts(data) {
      if (Array.isArray(data)) return data
      if (Array.isArray(data?.courts)) return data.courts
      if (Array.isArray(data?.items)) return data.items
      if (Array.isArray(data?.data)) return data.data

      return []
    },

    async fetchMyClub() {
      try {
        const response = await api.get('/clubs/my-club')

        this.club = this.normalizeClub(response.data)

        return {
          success: true,
          club: this.club,
        }
      } catch (error) {
        /*
         * An owner may not have created a club yet.
         * In that situation the dashboard should remain usable
         * and show the "Create Club" state.
         */
        if (error?.response?.status === 404) {
          this.club = null

          return {
            success: true,
            club: null,
          }
        }

        const message = this.getErrorMessage(
          error,
          'Failed to load club information',
        )

        console.error('Failed to fetch owner club:', error)

        return {
          success: false,
          error: message,
        }
      }
    },

    async fetchCourts() {
      this.loading = true
      this.error = null

      try {
        /*
         * Load club first because AdminDashboardView.vue
         * uses courtStore.club for Club Settings.
         */
        await this.fetchMyClub()

        const response = await api.get('/clubs/courts')

        const data = response.data

        /*
         * Some backend responses may return club information
         * together with courts.
         */
        if (data?.club) {
          this.club = data.club
        }

        this.courts = this.normalizeCourts(data)

        return {
          success: true,
          courts: this.courts,
          club: this.club,
        }
      } catch (error) {
        const message = this.getErrorMessage(
          error,
          'Failed to load courts',
        )

        this.error = message
        this.courts = []

        console.error('Failed to fetch courts:', error)

        return {
          success: false,
          error: message,
        }
      } finally {
        this.loading = false
      }
    },

    async createClub(payload) {
      this.loading = true
      this.error = null

      try {
        const requestBody = {
          name: payload.name,
          address: payload.address,
          open_time: payload.open_time || null,
          close_time: payload.close_time || null,
          slot_duration_minutes:
            payload.slot_duration_minutes !== '' &&
            payload.slot_duration_minutes !== null &&
            payload.slot_duration_minutes !== undefined
              ? Number(payload.slot_duration_minutes)
              : null,
        }

        const response = await api.post(
          '/clubs',
          requestBody,
        )

        this.club = this.normalizeClub(response.data)

        /*
         * Reload because this keeps the store synchronized
         * with the actual PostgreSQL state.
         */
        await this.fetchCourts()

        return {
          success: true,
          club: this.club,
          data: response.data,
        }
      } catch (error) {
        const message = this.getErrorMessage(
          error,
          'Failed to create club',
        )

        this.error = message

        console.error('Failed to create club:', error)

        return {
          success: false,
          error: message,
        }
      } finally {
        this.loading = false
      }
    },

    async updateClubSettings(payload) {
      if (!this.club?.id) {
        return {
          success: false,
          error: 'No club found for this owner',
        }
      }

      this.loading = true
      this.error = null

      try {
        const requestBody = {
          name: payload.name,
          address: payload.address,
          open_time: payload.open_time || null,
          close_time: payload.close_time || null,
          slot_duration_minutes:
            payload.slot_duration_minutes !== '' &&
            payload.slot_duration_minutes !== null &&
            payload.slot_duration_minutes !== undefined
              ? Number(payload.slot_duration_minutes)
              : null,
        }

        const response = await api.put(
          `/clubs/${this.club.id}`,
          requestBody,
        )

        const updatedClub =
          this.normalizeClub(response.data)

        if (updatedClub) {
          this.club = {
            ...this.club,
            ...updatedClub,
          }
        } else {
          this.club = {
            ...this.club,
            ...requestBody,
          }
        }

        return {
          success: true,
          club: this.club,
          data: response.data,
        }
      } catch (error) {
        const message = this.getErrorMessage(
          error,
          'Failed to update club settings',
        )

        this.error = message

        console.error(
          'Failed to update club settings:',
          error,
        )

        return {
          success: false,
          error: message,
        }
      } finally {
        this.loading = false
      }
    },

    async createCourt(payload) {
      this.loading = true
      this.error = null

      try {
        const requestBody = {
          court_name: payload.court_name,
          is_active: payload.is_active ?? true,
        }

        /*
         * Only send override values when Custom Settings
         * is selected.
         */
        if (!payload.use_defaults) {
          requestBody.open_time_override =
            payload.open_time_override || null

          requestBody.close_time_override =
            payload.close_time_override || null

          requestBody.slot_duration_override =
            payload.slot_duration_override !== '' &&
            payload.slot_duration_override !== null &&
            payload.slot_duration_override !== undefined
              ? Number(payload.slot_duration_override)
              : null
        }

        const response = await api.post(
          '/clubs/courts',
          requestBody,
        )

        await this.fetchCourts()

        return {
          success: true,
          court:
            response.data?.court ??
            response.data?.data ??
            response.data,
        }
      } catch (error) {
        const message = this.getErrorMessage(
          error,
          'Failed to create court',
        )

        this.error = message

        console.error('Failed to create court:', error)

        return {
          success: false,
          error: message,
        }
      } finally {
        this.loading = false
      }
    },

    async updateCourt(courtId, payload) {
      if (!courtId) {
        return {
          success: false,
          error: 'Court ID is required',
        }
      }

      this.loading = true
      this.error = null

      try {
        const requestBody = {
          court_name:
            payload.court_name ??
            payload.name,

          is_active:
            payload.is_active ?? true,
        }

        if (payload.use_defaults === true) {
          requestBody.open_time_override = null
          requestBody.close_time_override = null
          requestBody.slot_duration_override = null
        } else {
          requestBody.open_time_override =
            payload.open_time_override || null

          requestBody.close_time_override =
            payload.close_time_override || null

          requestBody.slot_duration_override =
            payload.slot_duration_override !== '' &&
            payload.slot_duration_override !== null &&
            payload.slot_duration_override !== undefined
              ? Number(payload.slot_duration_override)
              : null
        }

        const response = await api.put(
          `/clubs/courts/${courtId}`,
          requestBody,
        )

        await this.fetchCourts()

        return {
          success: true,
          court:
            response.data?.court ??
            response.data?.data ??
            response.data,
        }
      } catch (error) {
        const message = this.getErrorMessage(
          error,
          'Failed to update court',
        )

        this.error = message

        console.error('Failed to update court:', error)

        return {
          success: false,
          error: message,
        }
      } finally {
        this.loading = false
      }
    },

    async deleteCourt(courtId) {
      if (!courtId) {
        return {
          success: false,
          error: 'Court ID is required',
        }
      }

      this.loading = true
      this.error = null

      try {
        await api.delete(
          `/clubs/courts/${courtId}`,
        )

        this.courts = this.courts.filter(
          (court) => court.id !== courtId,
        )

        return {
          success: true,
        }
      } catch (error) {
        const message = this.getErrorMessage(
          error,
          'Failed to delete court',
        )

        this.error = message

        console.error('Failed to delete court:', error)

        return {
          success: false,
          error: message,
        }
      } finally {
        this.loading = false
      }
    },

    clear() {
      this.club = null
      this.courts = []
      this.error = null
      this.loading = false
    },
  },
})