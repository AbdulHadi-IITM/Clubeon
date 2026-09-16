<template>
  <div class="event-card">
    <!-- Image Frame -->
    <div class="image-frame">
      <img 
        :src="event.imageUrl || getSportImage(event.name || event.title || event.sport || event.category)" 
        :alt="event.name || event.title" 
        class="event-img"
      />
      <div class="image-overlay"></div>
      <div class="category-badge">{{ event.category || event.sport || 'Tournament' }}</div>
    </div>

    <!-- Details Body -->
    <div class="card-body">
      <h3 class="event-name">{{ event.name }}</h3>

      <div class="event-meta">
        <div class="meta-item">
          <svg class="meta-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="16" height="16">
            <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span>{{ event.date }}</span>
        </div>
        <div class="meta-item">
          <svg class="meta-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="16" height="16">
            <path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span>{{ event.venue }}</span>
        </div>
      </div>
    </div>

    <!-- Action Footer -->
    <div class="card-footer">
      <button 
        @click="$emit('click-action', event)" 
        class="action-btn"
        aria-label="Register or view details for the event"
      >
        <span>{{ event.isRegistered ? 'View Details' : 'Register Now' }}</span>
        <svg class="arrow-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" width="14" height="14">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { getSportImage } from '@/utils/sportImages'

defineProps({
  event: {
    type: Object,
    required: true,
    default: () => ({
      id: 1,
      name: 'Summer Badminton Championship',
      date: 'August 12, 2026',
      venue: 'Main Indoor Hall (Courts 1-4)',
      imageUrl: '',
      category: 'Tournament',
      isRegistered: false
    })
  }
})

defineEmits(['click-action'])
</script>

<script>
export default {
  name: 'EventCard'
}
</script>

<style scoped>
.event-card {
  background: #ffffff;
  border-radius: 1.5rem;
  border: 1px solid rgba(226, 232, 240, 0.8);
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.03);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
  height: 100%;
}

.event-card:hover {
  transform: translateY(-6px);
  border-color: rgba(79, 70, 229, 0.15);
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.07);
}

.image-frame {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 10;
  overflow: hidden;
  background: #0f172a;
}

.event-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
}

.event-card:hover .event-img {
  transform: scale(1.05);
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(15, 23, 42, 0) 60%, rgba(15, 23, 42, 0.4) 100%);
}

.category-badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  padding: 0.35rem 0.75rem;
  border-radius: 999px;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  color: #ffffff;
  font-size: 0.725rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.card-body {
  padding: 1.5rem 1.5rem 1.25rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.event-name {
  margin: 0 0 1rem;
  font-family: 'Poppins', sans-serif;
  font-size: 1.15rem;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.35;
  letter-spacing: -0.02em;
}

.event-meta {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-top: auto;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-size: 0.88rem;
  color: #475569;
  font-weight: 500;
}

.meta-icon {
  color: #94a3b8;
  flex-shrink: 0;
}

.card-footer {
  padding: 0 1.5rem 1.5rem;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  width: 100%;
  min-height: 2.85rem;
  padding: 0.65rem 1.25rem;
  border-radius: 0.95rem;
  background: rgba(79, 70, 229, 0.06);
  border: 1px solid rgba(79, 70, 229, 0.12);
  color: #4f46e5;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s ease;
}

.action-btn:hover {
  background: #4f46e5;
  color: #ffffff;
  border-color: #4f46e5;
  box-shadow: 0 6px 16px rgba(79, 70, 229, 0.25);
}

.arrow-icon {
  transition: transform 0.2s ease;
}

.action-btn:hover .arrow-icon {
  transform: translateX(2px);
}

@media (max-width: 576px) {
  .card-body {
    padding: 1.25rem 1.25rem 1rem;
  }
  .card-footer {
    padding: 0 1.25rem 1.25rem;
  }
}
</style>
