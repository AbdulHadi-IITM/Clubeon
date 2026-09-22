import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 15000, // 15-second timeout to prevent hanging requests
  headers: { 'Content-Type': 'application/json' },
  withCredentials: true, // crucial: send cookies (HttpOnly cookies will be sent by the browser)
})

/**
 * Format API errors into human-readable messages.
 * @param {Error} err - Axios error object
 * @returns {string} User-friendly error message
 */
export function formatApiError(err) {
  if (!err) return 'An unexpected error occurred.'
  if (err.code === 'ECONNABORTED' || err.message?.includes('timeout')) {
    return 'The request timed out. Please verify your connection and try again.'
  }
  if (!err.response) {
    return 'Unable to reach the server. Please check your internet connection.'
  }
  return (
    err.response.data?.message ||
    err.response.data?.error ||
    `Request failed with status ${err.response.status}`
  )
}

/**
 * Check if the error is a connectivity or network failure.
 * @param {Error} err
 * @returns {boolean}
 */
export function isNetworkError(err) {
  return !err?.response || err.code === 'ECONNABORTED'
}

// Global response interceptor
api.interceptors.response.use(
  (res) => res,
  (err) => {
    const status = err?.response?.status

    // Attach standardized friendly message for downstream consumers
    err.friendlyMessage = formatApiError(err)

    if (status === 401) {
      // notify app-level handlers to logout the user
      if (typeof window !== 'undefined') {
        window.dispatchEvent(new CustomEvent('unauthorized', { detail: { error: err } }))
      }
    } else if (status >= 500) {
      if (typeof window !== 'undefined') {
        window.dispatchEvent(new CustomEvent('server-error', { detail: { error: err } }))
      }
    }

    return Promise.reject(err)
  },
)

export default api
