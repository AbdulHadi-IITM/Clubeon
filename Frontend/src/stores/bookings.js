import { defineStore } from 'pinia'
import { db, generateId } from '../data/storage.js'

export const useBookingStore = defineStore('bookings', {
  state: () => ({
    bookings: [],
    waitlist: [],
  }),
  actions: {
    load() {
      this.bookings = db.bookings
      this.waitlist = db.waitlist
    },
    getUserBookings(userId) {
      return this.bookings.filter((b) => b.userId === userId)
    },
    getBookingsByDate(date) {
      return this.bookings.filter((b) => b.date === date)
    },
    getBookingsByCourt(courtId, date) {
      return this.bookings.filter((b) => b.courtId === courtId && b.date === date)
    },
    createBooking(booking) {
      const court = db.courts.find((c) => c.id === booking.courtId)
      if (!court || !court.isActive) return { success: false, error: 'Court is not available' }

      const existing = this.bookings.filter(
        (b) => b.courtId === booking.courtId && b.date === booking.date && b.status !== 'cancelled' && b.status !== 'released'
      )
      const conflict = existing.some((b) => {
        return booking.startTime < b.endTime && booking.endTime > b.startTime
      })
      if (conflict) {
        this.waitlist = [...this.waitlist, { ...booking, id: generateId('wl') }]
        db.waitlist = this.waitlist
        return { success: false, error: 'Time slot is already booked. You have been added to the waitlist.' }
      }

      const newBooking = { ...booking, id: generateId('bk') }
      this.bookings = [...this.bookings, newBooking]
      db.bookings = this.bookings

      return { success: true, booking: newBooking }
    },
    releaseBooking(bookingId) {
      const idx = this.bookings.findIndex((b) => b.id === bookingId)
      if (idx === -1) return { success: false, error: 'Booking not found' }
      this.bookings[idx] = { ...this.bookings[idx], status: 'released' }
      db.bookings = this.bookings

      const releasedBooking = this.bookings[idx]
      const wlIdx = this.waitlist.findIndex(
        (w) => w.courtId === releasedBooking.courtId && w.date === releasedBooking.date
          && w.startTime === releasedBooking.startTime && w.endTime === releasedBooking.endTime
      )
      if (wlIdx !== -1) {
        const wlItem = this.waitlist[wlIdx]
        this.waitlist = this.waitlist.filter((_, i) => i !== wlIdx)
        db.waitlist = this.waitlist
        return { success: true, booking: releasedBooking, waitlistFilled: wlItem }
      }

      return { success: true, booking: releasedBooking }
    },
    cancelBooking(bookingId) {
      const idx = this.bookings.findIndex((b) => b.id === bookingId)
      if (idx === -1) return { success: false, error: 'Booking not found' }
      this.bookings[idx] = { ...this.bookings[idx], status: 'cancelled' }
      db.bookings = this.bookings
      return { success: true }
    },
    staffCreateBooking(booking) {
      return this.createBooking(booking)
    },
  },
})
