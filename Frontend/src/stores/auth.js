import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/axios'
import { useCourtStore } from '@/stores/courts.js'

export const useAuthStore = defineStore('auth', () => {
  // Initialize user from cached localStorage if available to avoid flash of logged-out state
  const cachedUser = typeof window !== 'undefined' ? JSON.parse(localStorage.getItem('clubdash_user') || 'null') : null
  const user = ref(cachedUser)
  const initialized = ref(false)
  const loading = ref(false)
  const error = ref(null)

  // Call on app startup to rehydrate user from HttpOnly cookie session
  async function restoreUser() {
    if (initialized.value) return user.value
    loading.value = true
    error.value = null
    try {
      const res = await api.get('/auth/me') // backend reads cookie and returns user
      user.value = res.data?.user ?? null
      if (user.value) {
        localStorage.setItem('clubdash_user', JSON.stringify(user.value))
      } else {
        localStorage.removeItem('clubdash_user')
      }
    } catch (err) {
      if (err?.response?.status === 401) {
        user.value = null
        localStorage.removeItem('clubdash_user')
      }
    } finally {
      initialized.value = true
      loading.value = false
    }
    return user.value
  }

  // Login: server must set HttpOnly cookie (session or similar) and optionally return user
  async function login(credentials) {
    loading.value = true
    error.value = null
    try {
      const res = await api.post('/auth/login', credentials)
      user.value = res.data?.user ?? null
      if (user.value) {
        localStorage.setItem('clubdash_user', JSON.stringify(user.value))
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
        localStorage.setItem('clubdash_user', JSON.stringify(user.value))
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
      // ignore
    } finally {
      user.value = null
      localStorage.removeItem('clubdash_user')
      loading.value = false
      // Reset all dependent stores
      const courtStore = useCourtStore()
      courtStore.reset() // <-- clear club and courts
    }
  }

  function isAuthenticated() {
    return !!user.value
  }

  // react to global 'unauthorized' events from axios interceptor
  if (typeof window !== 'undefined') {
    window.addEventListener('unauthorized', () => {
      user.value = null
      localStorage.removeItem('clubdash_user')
    })
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
    isAuthenticated,
  }
})
