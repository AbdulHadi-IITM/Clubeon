<template>
  <div class="badge-card" :class="{ 'is-locked': !badge.isUnlocked }" :title="badge.isUnlocked ? 'Unlocked on ' + badge.unlockDate : 'Locked'">
    <!-- Badge Graphic/Icon -->
    <div class="badge-graphic-wrapper">
      <div class="badge-ring">
        <div class="badge-sphere" :style="{ background: badge.isUnlocked ? badge.color : '#e2e8f0' }">
          <!-- Icon placeholder or custom SVG icons based on name -->
          <div class="badge-icon-content">
            <span class="emoji-icon" v-if="badge.isUnlocked">{{ badge.icon }}</span>
            <svg v-else class="lock-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" width="20" height="20">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Badge Info -->
    <div class="badge-info">
      <h3 class="badge-title">{{ badge.title }}</h3>
      <p class="badge-desc">{{ badge.description }}</p>
      <span class="unlock-date" v-if="badge.isUnlocked">Unlocked {{ badge.unlockDate }}</span>
      <span class="unlock-date locked" v-else>In Progress</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  badge: {
    type: Object,
    required: true,
    default: () => ({
      title: 'Early Bird',
      description: 'First booking before 07:00 AM',
      icon: '🌅',
      isUnlocked: true,
      unlockDate: 'Mar 15, 2025',
      color: 'linear-gradient(135deg, #fb923c 0%, #f97316 100%)'
    })
  }
})
</script>

<script>
export default {
  name: 'AchievementBadge'
}
</script>

<style scoped>
.badge-card {
  background: #ffffff;
  border-radius: 1.25rem;
  border: 1px solid rgba(226, 232, 240, 0.8);
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.02);
  padding: 1.5rem 1.25rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  position: relative;
  height: 100%;
}

.badge-card:hover {
  transform: translateY(-4px) scale(1.02);
  border-color: rgba(79, 70, 229, 0.15);
  box-shadow: 0 16px 36px rgba(15, 23, 42, 0.05);
}

.badge-card.is-locked {
  background: rgba(248, 250, 252, 0.6);
  opacity: 0.8;
}

.badge-graphic-wrapper {
  margin-bottom: 1.15rem;
}

.badge-ring {
  width: 4.75rem;
  height: 4.75rem;
  border-radius: 50%;
  padding: 0.25rem;
  background: rgba(226, 232, 240, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.badge-card:hover .badge-ring {
  background: rgba(79, 70, 229, 0.08);
}

.badge-sphere {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    0 8px 16px rgba(15, 23, 42, 0.08),
    inset 0 2px 4px rgba(255, 255, 255, 0.2);
  transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.badge-card:hover .badge-sphere {
  transform: rotate(8deg);
}

.badge-icon-content {
  display: flex;
  align-items: center;
  justify-content: center;
}

.emoji-icon {
  font-size: 1.85rem;
  filter: drop-shadow(0 4px 6px rgba(15, 23, 42, 0.12));
}

.lock-icon {
  color: #94a3b8;
}

.badge-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.badge-title {
  margin: 0 0 0.45rem;
  font-family: 'Poppins', sans-serif;
  font-size: 0.95rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.01em;
}

.badge-card.is-locked .badge-title {
  color: #64748b;
}

.badge-desc {
  margin: 0 0 0.85rem;
  font-size: 0.8rem;
  color: #64748b;
  line-height: 1.4;
  font-weight: 500;
  flex: 1;
}

.unlock-date {
  font-size: 0.725rem;
  font-weight: 700;
  color: #4f46e5;
  background: rgba(79, 70, 229, 0.06);
  padding: 0.25rem 0.65rem;
  border-radius: 999px;
  letter-spacing: 0.01em;
}

.unlock-date.locked {
  color: #64748b;
  background: rgba(100, 116, 139, 0.08);
}
</style>
