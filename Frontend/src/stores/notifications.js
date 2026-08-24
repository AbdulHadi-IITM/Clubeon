/**
 * Notifications and club announcements.
 *
 * Everything here comes from the API. The previous version shipped four
 * invented announcements ("Court Resurfacing Schedule", a "₹50,000 prize pool"
 * tournament, …) as its default state, mirrored them into localStorage, and
 * fell back to them whenever the server returned an empty list — so every user
 * saw club notices that no club had ever published. It also swallowed write
 * failures and mutated local state anyway, which made a failed delete look
 * like it had worked.
 */
import { defineStore } from 'pinia'
import api from '@/api/axios'

/** Maps a notification's `type` onto the label, colour and icon the UI shows. */
const CATEGORIES = [
  { match: (t) => t.includes('announc') || t === 'broadcast',
    category: 'Broadcast', categoryClass: 'purple', icon: '📣' },
  { match: (t) => t.includes('tourn') || t.includes('event'),
    category: 'Tournament', categoryClass: 'emerald', icon: '🏆' },
  { match: (t) => t.includes('policy') || t.includes('alert') || t.includes('guideline'),
    category: 'Policy', categoryClass: 'orange', icon: '📜' },
  { match: (t) => t.includes('maint') || t.includes('court') || t.includes('closure'),
    category: 'Maintenance', categoryClass: 'rose', icon: '🛠️' },
  { match: (t) => t.includes('book'), category: 'Booking', categoryClass: 'blue', icon: '📅' },
  { match: (t) => t.includes('pay'), category: 'Payment', categoryClass: 'purple', icon: '💳' },
]

const DEFAULT_CATEGORY = { category: 'General', categoryClass: 'blue', icon: '📢' }

function classify(type) {
  const raw = String(type || '').toLowerCase()
  return CATEGORIES.find((c) => c.match(raw)) || DEFAULT_CATEGORY
}

function formatDate(value) {
  if (!value) return ''
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return String(value)
  return d.toLocaleDateString('en-IN', { year: 'numeric', month: 'short', day: 'numeric' })
}

function errorMessage(err, fallback) {
  return err?.response?.data?.message || err?.message || fallback
}

export const useNotificationStore = defineStore('notifications', {
  state: () => ({
    notifications: [],
    isLoading: false,
    error: null,
  }),

  getters: {
    announcements: (state) =>
      state.notifications.map((item) => {
        const { category, categoryClass, icon } = classify(item.type)
        return {
          id: item.id,
          title: item.title,
          body: item.body || '',
          type: item.type || 'general',
          is_read: Boolean(item.is_read),
          created_at: item.created_at,
          date: formatDate(item.created_at),
          category,
          categoryClass,
          icon,
        }
      }),

    unreadCount: (state) => state.notifications.filter((n) => !n.is_read).length,
  },

  actions: {
    reset() {
      this.notifications = []
      this.isLoading = false
      this.error = null
    },

    async fetchNotifications() {
      this.isLoading = true
      this.error = null
      try {
        const { data } = await api.get('/notifications')
        this.notifications = Array.isArray(data) ? data : []
      } catch (err) {
        this.notifications = []
        this.error = errorMessage(err, 'Could not load notifications.')
      } finally {
        this.isLoading = false
      }
    },

    /** Owner view: the announcements this owner has published. */
    async fetchAnnouncements() {
      this.isLoading = true
      this.error = null
      try {
        const { data } = await api.get('/admin/announcements')
        this.notifications = Array.isArray(data) ? data : []
      } catch (err) {
        this.notifications = []
        this.error = errorMessage(err, 'Could not load announcements.')
      } finally {
        this.isLoading = false
      }
    },

    async markAsRead(id) {
      const target = this.notifications.find((n) => n.id === id)
      if (!target || target.is_read) return { success: true }
      try {
        await api.post(`/notifications/${id}/read`)
        target.is_read = true
        return { success: true }
      } catch (err) {
        return { success: false, error: errorMessage(err, 'Could not mark as read.') }
      }
    },

    async markAllAsRead() {
      try {
        await api.post('/notifications/read-all')
        this.notifications.forEach((n) => {
          n.is_read = true
        })
        return { success: true }
      } catch (err) {
        return { success: false, error: errorMessage(err, 'Could not mark all as read.') }
      }
    },

    async createAnnouncement(payload) {
      this.isLoading = true
      try {
        const { data } = await api.post('/admin/announcements', {
          title: payload.title,
          body: payload.body || payload.message || '',
          category: payload.category || 'General',
          target_audience: payload.target_audience || 'all',
        })
        if (data?.announcement) this.notifications.unshift(data.announcement)
        return { success: true, data: data?.announcement }
      } catch (err) {
        return { success: false, error: errorMessage(err, 'Could not publish the announcement.') }
      } finally {
        this.isLoading = false
      }
    },

    async deleteAnnouncement(id) {
      try {
        await api.delete(`/admin/announcements/${id}`)
        this.notifications = this.notifications.filter((n) => n.id !== id)
        return { success: true }
      } catch (err) {
        // The row stays in the list: it still exists on the server.
        return { success: false, error: errorMessage(err, 'Could not delete the announcement.') }
      }
    },
  },
})
