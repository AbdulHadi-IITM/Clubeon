// frontend/src/api/axios.js
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api/v1',
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true, // crucial: send cookies (HttpOnly cookies will be sent by the browser)
})

// Emit a global event on 401 so the app can clear in-memory user and redirect
api.interceptors.response.use(
  (res) => res,
  (err) => {
    const status = err?.response?.status
    if (status === 401) {
      // notify app-level handlers to logout the user
      if (typeof window !== 'undefined') {
        window.dispatchEvent(new CustomEvent('unauthorized', { detail: { error: err } }))
      }
    }
    return Promise.reject(err)
  },
)

export default api
