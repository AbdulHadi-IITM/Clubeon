import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/axios'
import { useCourtStore } from '@/stores/courts.js'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const initialized = ref(false)
  const loading = ref(false)
  const error = ref(null)

  // Call on app startup to rehydrate user from HttpOnly cookie session
  async function restoreUser() {
    if (initialized.value) return user.value
    initialized.value = true
    loading.value = true
    error.value = null
    try {
      const res = await api.get('/auth/me') // backend reads cookie and returns user
      user.value = res.data?.user ?? null
    } catch {
      user.value = null
      // ignore error; user is not authenticated
    } finally {
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
      // server may return user in body; otherwise fallback to /auth/me
      user.value = res.data?.user ?? (await restoreUser())
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
      user.value = res.data?.user ?? (await restoreUser())
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
