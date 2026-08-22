import { defineStore } from 'pinia'
import api from '@/api/axios'

const DEFAULT_ANNOUNCEMENTS = [
  {
    id: 101,
    title: 'Court Resurfacing Schedule - Summer 2026',
    body: 'Courts 3 and 4 will be temporarily closed from Aug 25 to Aug 27 for annual synthetic turf and acrylic resurfacing. Please book alternate courts.',
    type: 'maintenance',
    priority: 'high',
    target_audience: 'all',
    is_read: false,
    created_at: new Date(Date.now() - 3600000 * 24).toISOString(),
  },
  {
    id: 102,
    title: 'Registration Open: Apex Tennis Summer Championship 2026',
    body: 'Registrations are officially open for all club members and ranked players. Singles & Doubles brackets available with trophy awards and ₹50,000 prize pool.',
    type: 'tournament',
    priority: 'normal',
    target_audience: 'members',
    is_read: false,
    created_at: new Date(Date.now() - 3600000 * 48).toISOString(),
  },
  {
    id: 103,
    title: 'Updated Evening Guest Policies & Peak Hours Guidelines',
    body: 'Non-member guests must be registered at the reception 15 minutes prior to booking. Peak hours will remain 06:00 PM to 09:00 PM on weekdays.',
    type: 'policy',
    priority: 'urgent',
    target_audience: 'all',
    is_read: true,
    created_at: new Date(Date.now() - 3600000 * 72).toISOString(),
  },
  {
    id: 104,
    title: 'New High-Performance LED Floodlights Installed',
    body: 'We have upgraded the lighting fixtures across Tennis Court 1 and Badminton Hall A to 1000-lux tournament spec LED floodlights for clearer evening visibility.',
    type: 'broadcast',
    priority: 'normal',
    target_audience: 'all',
    is_read: true,
    created_at: new Date(Date.now() - 3600000 * 96).toISOString(),
  },
]

const getStoredAnnouncements = () => {
  try {
    const raw = localStorage.getItem('admin_announcements')
    return raw ? JSON.parse(raw) : null
  } catch {
    return null
  }
}

const saveStoredAnnouncements = (items) => {
  try {
    localStorage.setItem('admin_announcements', JSON.stringify(items))
  } catch (err) {
    console.error('Failed to cache announcements in localStorage:', err)
  }
}

export const useNotificationStore = defineStore('notifications', {
  state: () => ({
    notifications: getStoredAnnouncements() || DEFAULT_ANNOUNCEMENTS,
    isLoading: false,
    error: null,
  }),

  getters: {
    announcements: (state) => {
      // Return all items, mapped with friendly display helpers
      return state.notifications.map((item) => {
        let category = 'General'
        let categoryClass = 'blue'
        let icon = '📢'

        const rawType = (item.type || '').toLowerCase()
        if (rawType.includes('announc') || rawType === 'broadcast') {
          category = 'Broadcast'
          categoryClass = 'purple'
          icon = '📣'
        } else if (rawType.includes('tourn') || rawType.includes('event')) {
          category = 'Tournament'
          categoryClass = 'emerald'
          icon = '🏆'
        } else if (rawType.includes('policy') || rawType.includes('alert') || rawType.includes('guideline')) {
          category = 'Policy'
          categoryClass = 'orange'
          icon = '📜'
        } else if (rawType.includes('maint') || rawType.includes('court') || rawType.includes('closure')) {
          category = 'Maintenance'
          categoryClass = 'rose'
          icon = '🛠️'
        } else if (rawType.includes('book')) {
          category = 'Booking'
          categoryClass = 'blue'
          icon = '📅'
        } else if (rawType.includes('pay')) {
          category = 'Payment'
          categoryClass = 'purple'
          icon = '💳'
        } else if (rawType === 'general') {
          category = 'General'
          categoryClass = 'blue'
          icon = '📢'
        }

        // Format friendly date
        let formattedDate = item.created_at || 'Recent'
        try {
          if (item.created_at) {
            const d = new Date(item.created_at)
            if (!isNaN(d.getTime())) {
              formattedDate = d.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
              })
            }
          }
        } catch {
          // fallback to raw string
        }

        return {
          id: item.id,
          title: item.title,
          body: item.body || '',
          type: item.type || 'general',
          priority: item.priority || 'normal',
          target_audience: item.target_audience || 'all',
          is_read: item.is_read || false,
          date: formattedDate,
          created_at: item.created_at,
          category,
          categoryClass,
          icon,
        }
      })
    },

    unreadCount: (state) => {
      return state.notifications.filter((n) => !n.is_read).length
    },
  },

  actions: {
    async fetchNotifications() {
      this.isLoading = true
      this.error = null
      try {
        // Try admin announcements endpoint first, fallback to notifications
        let response = await api.get('/admin/announcements').catch(() => null)
        if (!response || !Array.isArray(response.data) || response.data.length === 0) {
          response = await api.get('/notifications').catch(() => null)
        }

        if (response && Array.isArray(response.data) && response.data.length > 0) {
          const stored = getStoredAnnouncements() || DEFAULT_ANNOUNCEMENTS
          const customItems = stored.filter((s) => !response.data.some((d) => d.id === s.id))
          this.notifications = [...customItems, ...response.data]
          saveStoredAnnouncements(this.notifications)
        } else if (!this.notifications || this.notifications.length === 0) {
          const stored = getStoredAnnouncements()
          this.notifications = stored || DEFAULT_ANNOUNCEMENTS
        }
      } catch (err) {
        console.error('Failed to fetch notifications/announcements:', err)
        this.error = err.response?.data?.message || 'Failed to load announcements'
        if (!this.notifications || this.notifications.length === 0) {
          this.notifications = getStoredAnnouncements() || DEFAULT_ANNOUNCEMENTS
        }
      } finally {
        this.isLoading = false
      }
    },

    async markAsRead(id) {
      try {
        await api.post(`/notifications/${id}/read`).catch(() => null)
      } catch (err) {
        console.error(`Failed to mark notification ${id} as read:`, err)
      } finally {
        const target = this.notifications.find((n) => n.id === id)
        if (target) target.is_read = true
        saveStoredAnnouncements(this.notifications)
      }
    },

    async markAllAsRead() {
      try {
        await api.post('/notifications/read-all').catch(() => null)
      } catch (err) {
        console.error('Failed to mark all notifications as read:', err)
      } finally {
        this.notifications.forEach((n) => {
          n.is_read = true
        })
        saveStoredAnnouncements(this.notifications)
      }
    },

    async createAnnouncement(payload) {
      this.isLoading = true
      try {
        const response = await api.post('/admin/announcements', payload).catch(() => null)

        const newAnnouncement = response?.data?.announcement || {
          id: Date.now(),
          title: payload.title,
          body: payload.body || payload.message || '',
          type: payload.category ? payload.category.toLowerCase() : 'general',
          priority: payload.priority || 'normal',
          target_audience: payload.target_audience || 'all',
          is_read: false,
          created_at: new Date().toISOString(),
        }

        this.notifications.unshift(newAnnouncement)
        saveStoredAnnouncements(this.notifications)
        return { success: true, data: newAnnouncement }
      } catch (err) {
        console.error('Failed to broadcast announcement:', err)
        return {
          success: false,
          error: err.response?.data?.message || 'Failed to publish announcement',
        }
      } finally {
        this.isLoading = false
      }
    },

    async deleteAnnouncement(id) {
      try {
        await api.delete(`/admin/announcements/${id}`).catch(() => null)
      } catch (err) {
        console.error('Delete announcement API error:', err)
      } finally {
        this.notifications = this.notifications.filter((n) => n.id !== id)
        saveStoredAnnouncements(this.notifications)
      }
      return { success: true }
    },
  },
})
