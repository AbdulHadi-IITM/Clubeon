import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/axios'
import { useCourtStore } from '@/stores/courts.js'
import { useBookingStore } from '@/stores/bookings.js'
import { useNotificationStore } from '@/stores/notifications.js'

export const useAuthStore = defineStore('auth', () => {
  // Initialize user from cached localStorage if available to avoid flash of logged-out state
  const cachedUser = typeof window !== 'undefined'
    ? JSON.parse(localStorage.getItem('clubeon_user') || localStorage.getItem('clubdash_user') || 'null')
    : null
  const user = ref(cachedUser)
  const initialized = ref(false)
  const loading = ref(false)
  const error = ref(null)

  // Restoring is deduped on an in-flight promise. main.js and the router guard
  // both call it during startup, and `initialized` is only set once the first
  // call resolves, so without this both fired a /auth/me request. The second
  // 401 arrived after the global `unauthorized` listener was installed and
  // bounced anonymous visitors off the public landing page to /login.
  let restorePromise = null

  async function restoreUser() {
    if (initialized.value) return user.value
    if (restorePromise) return restorePromise

    loading.value = true
    error.value = null
    restorePromise = (async () => {
      try {
        const res = await api.get('/auth/me') // backend reads cookie and returns user
        user.value = res.data?.user ?? null
        if (user.value) {
          localStorage.setItem('clubeon_user', JSON.stringify(user.value))
        } else {
          localStorage.removeItem('clubeon_user')
        }
      } catch (err) {
        if (err?.response?.status === 401) {
          user.value = null
          localStorage.removeItem('clubeon_user')
        }
      } finally {
        initialized.value = true
        loading.value = false
        restorePromise = null
      }
      return user.value
    })()

    return restorePromise
  }

  // Login: server must set HttpOnly cookie (session or similar) and optionally return user
  async function login(credentials) {
    loading.value = true
    error.value = null
    try {
      const res = await api.post('/auth/login', credentials)
      user.value = res.data?.user ?? null
      if (user.value) {
        localStorage.setItem('clubeon_user', JSON.stringify(user.value))
      }
      initialized.value = true
      return user.value
    } catch (err) {
      error.value = err?.response?.data?.message || err.message || 'Login failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  // Register then login: server should set cookie (or return user)
  async function register(payload) {
    loading.value = true
    error.value = null
    try {
      const res = await api.post('/auth/register', payload)
      user.value = res.data?.user ?? null
      if (user.value) {
        localStorage.setItem('clubeon_user', JSON.stringify(user.value))
      }
      initialized.value = true
      return user.value
    } catch (err) {
      error.value = err?.response?.data?.message || err.message || 'Registration failed'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    loading.value = true
    try {
      await api.post('/auth/logout')
    } catch {
      // The cookie is cleared locally either way.
    } finally {
      user.value = null
      localStorage.removeItem('clubeon_user')
      loading.value = false
      // Clear every store that holds another user's data, so signing in as
      // someone else on the same browser never shows the previous session's
      // club, bookings or notifications.
      useCourtStore().reset()
      useBookingStore().reset()
      useNotificationStore().reset()
    }
  }

  async function updateProfile(payload) {
    loading.value = true
    error.value = null
    try {
      const res = await api.put('/auth/profile', payload)
      if (res.data?.user) {
        user.value = { ...user.value, ...res.data.user }
      }
      return user.value
    } catch (err) {
      error.value = err?.response?.data?.message || err.message || 'Failed to update profile'
      throw err
    } finally {
      loading.value = false
    }
  }

  function isAuthenticated() {
    return !!user.value
  }

  // React to global 'unauthorized' events from the axios interceptor.
  if (typeof window !== 'undefined') {
    window.addEventListener('unauthorized', () => {
      user.value = null
      localStorage.removeItem('clubeon_user')
    })
  }

  /** True when a session existed and the server has since rejected it. */
  function hadSession() {
    return initialized.value && !!localStorage.getItem('clubeon_user')
  }

  return {
    user,
    initialized,
    loading,
    error,
    restoreUser,
    login,
    register,
    logout,
    updateProfile,
    isAuthenticated,
    hadSession,
  }
})
