import { seedCourts, seedBookings } from './seed'

const KEYS = {
  courts: 'sc_courts',
  bookings: 'sc_bookings',
}

function load(key, seed) {
  const stored = localStorage.getItem(key)
  if (stored) return JSON.parse(stored)
  localStorage.setItem(key, JSON.stringify(seed))
  return seed
}

function save(key, data) {
  localStorage.setItem(key, JSON.stringify(data))
}

export function initData() {
  if (!localStorage.getItem('sc_initialized')) {
    Object.entries({
      [KEYS.courts]: seedCourts,
      [KEYS.bookings]: seedBookings,
    }).forEach(([key, seed]) => localStorage.setItem(key, JSON.stringify(seed)))
    localStorage.setItem('sc_initialized', 'true')
  }
}

export const db = {
  get courts() { return load(KEYS.courts, seedCourts) },
  set courts(v) { save(KEYS.courts, v) },

  get bookings() { return load(KEYS.bookings, seedBookings) },
  set bookings(v) { save(KEYS.bookings, v) },
}

export function generateId(prefix = 'id') {
  return `${prefix}-${Date.now()}-${Math.random().toString(30).slice(2, 8)}`
}