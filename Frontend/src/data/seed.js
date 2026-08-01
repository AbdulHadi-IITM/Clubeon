const today = new Date()
const d = (offset) => {
  const date = new Date(today)
  date.setDate(date.getDate() + offset)
  return date.toISOString().split('T')[0]
}

export const seedCourts = [
  { id: 'court-1', name: 'Court A - Badminton', sportType: 'Badminton', isActive: true, pricePerHour: 25 },
  { id: 'court-2', name: 'Court B - Badminton', sportType: 'Badminton', isActive: true, pricePerHour: 25 },
  { id: 'court-3', name: 'Court C - Tennis', sportType: 'Tennis', isActive: true, pricePerHour: 40 },
  { id: 'court-4', name: 'Court D - Tennis', sportType: 'Tennis', isActive: true, pricePerHour: 40 },
  { id: 'court-5', name: 'Court E - Squash', sportType: 'Squash', isActive: true, pricePerHour: 30 },
  { id: 'court-6', name: 'Court F - Basketball', sportType: 'Basketball', isActive: true, pricePerHour: 35 },
  { id: 'court-7', name: 'Court G - Basketball', sportType: 'Basketball', isActive: false, pricePerHour: 35 },
  { id: 'court-8', name: 'Court H - Volleyball', sportType: 'Volleyball', isActive: true, pricePerHour: 20 },
]

export const seedBookings = [
  { id: 'bk-1', courtId: 'court-1', userId: 'user-m1', date: d(0), startTime: '09:00', endTime: '10:00', status: 'confirmed', bookingType: 'member' },
  { id: 'bk-2', courtId: 'court-1', userId: 'user-m3', date: d(0), startTime: '11:00', endTime: '12:00', status: 'confirmed', bookingType: 'member' },
  { id: 'bk-3', courtId: 'court-2', userId: 'user-m2', date: d(0), startTime: '14:00', endTime: '15:00', status: 'confirmed', bookingType: 'member' },
  { id: 'bk-4', courtId: 'court-3', userId: 'user-m4', date: d(0), startTime: '10:00', endTime: '11:30', status: 'confirmed', bookingType: 'member' },
  { id: 'bk-5', courtId: 'court-4', userId: 'user-m5', date: d(0), startTime: '16:00', endTime: '17:00', status: 'confirmed', bookingType: 'member' },
  { id: 'bk-6', courtId: 'court-1', userId: 'user-m1', date: d(1), startTime: '09:00', endTime: '10:00', status: 'confirmed', bookingType: 'member' },
  { id: 'bk-7', courtId: 'court-2', userId: 'user-m3', date: d(1), startTime: '15:00', endTime: '16:00', status: 'confirmed', bookingType: 'member' },
  { id: 'bk-8', courtId: 'court-5', userId: 'user-m2', date: d(1), startTime: '11:00', endTime: '12:00', status: 'confirmed', bookingType: 'member' },
  { id: 'bk-9', courtId: 'court-6', userId: 'user-m4', date: d(2), startTime: '10:00', endTime: '11:00', status: 'released', bookingType: 'member' },
  { id: 'bk-10', courtId: 'court-3', userId: 'user-m5', date: d(2), startTime: '13:00', endTime: '14:00', status: 'confirmed', bookingType: 'member' },
  { id: 'bk-11', courtId: 'court-8', userId: 'user-m1', date: d(3), startTime: '18:00', endTime: '19:00', status: 'confirmed', bookingType: 'member' },
  { id: 'bk-12', courtId: 'court-1', userId: 'user-staff', date: d(4), startTime: '08:00', endTime: '09:00', status: 'confirmed', bookingType: 'member' },
  { id: 'bk-13', courtId: 'court-1', userId: 'guest-001', date: d(0), startTime: '17:00', endTime: '18:00', status: 'confirmed', bookingType: 'casual' },
  { id: 'bk-14', courtId: 'court-4', userId: 'guest-002', date: d(1), startTime: '19:00', endTime: '20:00', status: 'confirmed', bookingType: 'casual' },
  { id: 'bk-15', courtId: 'court-1', userId: 'user-m1', date: d(-1), startTime: '10:00', endTime: '11:00', status: 'confirmed', bookingType: 'member' },
  { id: 'bk-16', courtId: 'court-2', userId: 'user-m3', date: d(-1), startTime: '14:00', endTime: '15:00', status: 'cancelled', bookingType: 'member' },
]