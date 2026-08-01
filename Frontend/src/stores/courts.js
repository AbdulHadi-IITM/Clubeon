import { defineStore } from 'pinia'
import { db } from '../data/storage.js'

export const useCourtStore = defineStore('courts', {
  state: () => ({
    courts: [],
  }),
  getters: {
    activeCourts: (state) => state.courts.filter((c) => c.isActive),
    sportsTypes: (state) => [...new Set(state.courts.map((c) => c.sportType))],
  },
  actions: {
    load() {
      this.courts = db.courts
    },
    getCourt(id) {
      return this.courts.find((c) => c.id === id)
    },
    toggleCourtActive(courtId) {
      const idx = this.courts.findIndex((c) => c.id === courtId)
      if (idx !== -1) {
        this.courts[idx] = { ...this.courts[idx], isActive: !this.courts[idx].isActive }
        db.courts = this.courts
      }
    },
    updatePrice(courtId, price) {
      const idx = this.courts.findIndex((c) => c.id === courtId)
      if (idx !== -1) {
        this.courts[idx] = { ...this.courts[idx], pricePerHour: price }
        db.courts = this.courts
      }
    },
  },
})
