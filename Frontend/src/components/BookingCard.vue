<template>
  <div class="booking-card" :class="{ 'is-cancelled': booking.status === 'Cancelled' }">
    <!-- Sport Image Thumbnail Banner -->
    <div class="booking-thumb">
      <img :src="getSportImage(booking.courtName || booking.sport)" :alt="booking.courtName" class="thumb-img" />
      <div class="thumb-overlay"></div>
      <span :class="['status-badge', booking.status.toLowerCase()]">
        {{ booking.status }}
      </span>
    </div>

    <div class="card-body">
      <!-- Court Info & Title -->
      <div class="main-info">
        <div class="title-details">
          <h3 class="court-name">{{ booking.courtName }}</h3>
        </div>
      </div>

      <!-- Date & Time Grid -->
      <div class="schedule-details">
        <div class="schedule-item">
          <svg class="schedule-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="16" height="16">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span>{{ booking.date }}</span>
        </div>
        <div class="schedule-item">
          <svg class="schedule-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="16" height="16">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>{{ booking.timeSlot }}</span>
        </div>
      </div>
    </div>

    <!-- Actions Area -->
    <div class="card-actions">
      <button 
        @click="$emit('view', booking)" 
        class="action-btn view-btn"
        aria-label="View booking details"
      >
        View Details
      </button>
      <button 
        v-if="booking.status !== 'Cancelled' && booking.status !== 'Completed'"
        @click="$emit('cancel', booking)" 
        class="action-btn cancel-btn"
        aria-label="Cancel booking"
      >
        Cancel
      </button>
    </div>
  </div>
</template>

<script setup>
import { getSportImage } from '@/utils/sportImages'

defineProps({
  booking: {
    type: Object,
    required: true,
    default: () => ({
      id: 1,
      courtName: 'Premium Tennis Court A',
      date: 'July 24, 2026',
      timeSlot: '08:00 AM - 10:00 AM',
      status: 'Confirmed'
    })
  }
})

defineEmits(['view', 'cancel'])
</script>

<script>
export default {
  name: 'BookingCard'
}
</script>

<style scoped>
.booking-card {
  background: #ffffff;
  border-radius: 1.25rem;
  border: 1px solid rgba(226, 232, 240, 0.8);
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.02);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  overflow: hidden;
  height: 100%;
}

.booking-thumb {
  position: relative;
  width: 100%;
  height: 110px;
  overflow: hidden;
}

.thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.booking-card:hover .thumb-img {
  transform: scale(1.05);
}

.thumb-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.1) 0%, rgba(15, 23, 42, 0.5) 100%);
}

.booking-thumb .status-badge {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
}

.booking-card:hover {
  transform: translateY(-4px);
  border-color: rgba(79, 70, 229, 0.15);
  box-shadow: 0 16px 36px rgba(15, 23, 42, 0.06);
}

.booking-card.is-cancelled {
  opacity: 0.72;
}

.card-body {
  padding: 1.5rem 1.5rem 1.25rem;
}

.main-info {
  display: flex;
  align-items: flex-start;
  gap: 0.875rem;
  margin-bottom: 1.25rem;
}

.sport-badge-container {
  flex-shrink: 0;
}

.sport-icon-box {
  width: 2.75rem;
  height: 2.75rem;
  border-radius: 0.85rem;
  background: rgba(79, 70, 229, 0.08);
  color: #4f46e5;
  display: grid;
  place-items: center;
}

.title-details {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.35rem;
}

.court-name {
  margin: 0;
  font-family: 'Poppins', sans-serif;
  font-size: 1.05rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.02em;
  line-height: 1.35;
}

.status-badge {
  display: inline-flex;
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  font-size: 0.725rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.status-badge.confirmed {
  background-color: rgba(16, 185, 129, 0.1);
  color: #059669;
}

.status-badge.pending {
  background-color: rgba(245, 158, 11 0.1);
  background-color: rgba(245, 158, 11, 0.1);
  color: #d97706;
}

.status-badge.completed {
  background-color: rgba(59, 130, 246, 0.1);
  color: #2563eb;
}

.status-badge.cancelled {
  background-color: rgba(239, 68, 68, 0.1);
  color: #dc2626;
}

.schedule-details {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
}

.schedule-item {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  color: #475569;
  font-size: 0.88rem;
  font-weight: 500;
}

.schedule-icon {
  color: #94a3b8;
  flex-shrink: 0;
}

.card-actions {
  display: flex;
  padding: 1rem 1.5rem 1.25rem;
  gap: 0.75rem;
  border-top: 1px solid rgba(226, 232, 240, 0.6);
  background: #f8fafc;
}

.action-btn {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.35rem;
  padding: 0.5rem 0.85rem;
  border-radius: 0.75rem;
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1);
}

.view-btn {
  background: #ffffff;
  border: 1px solid rgba(226, 232, 240, 0.9);
  color: #475569;
}

.view-btn:hover {
  background: #f1f5f9;
  border-color: rgba(203, 213, 225, 0.9);
  color: #0f172a;
}

.cancel-btn {
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.15);
  color: #dc2626;
}

.cancel-btn:hover {
  background: #dc2626;
  border-color: #dc2626;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.2);
}

@media (max-width: 576px) {
  .card-body {
    padding: 1.25rem 1.25rem 1rem;
  }
  .card-actions {
    padding: 0.85rem 1.25rem 1.15rem;
  }
}
</style>
