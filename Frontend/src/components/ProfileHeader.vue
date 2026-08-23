<template>
  <div class="profile-header-card">
    <!-- Cover Background -->
    <div class="cover-bg">
      <div class="cover-overlay"></div>
      <div class="cover-pattern"></div>
    </div>

    <!-- Profile Main Content -->
    <div class="profile-content">
      <!-- Avatar Section -->
      <div class="avatar-wrapper">
        <div class="avatar-container">
          <img 
            :src="user.avatarUrl || 'https://placehold.co/150x150/4f46e5/ffffff?text=' + encodeURIComponent(((user.name || 'Member').trim().split(' ').map(n=>n[0]).join('') || 'M').slice(0, 2))" 
            :alt="user.name || 'Member'" 
            class="avatar-img"
          />
          <button @click="$emit('edit-avatar')" class="edit-avatar-btn" aria-label="Edit profile picture">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Info Area -->
      <div class="details-container">
        <div class="meta-info">
          <h1 class="user-name">{{ user.name || 'Member Profile' }}</h1>
          <div class="badge-group">
            <span :class="['membership-badge', (user.membershipType || 'member').toLowerCase()]">
              {{ user.membershipType || 'Active Member' }}
            </span>
            <span class="member-since">Member since {{ user.memberSince || 'Recent' }}</span>
          </div>
        </div>

        <!-- Quick Stats -->
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon bookings-icon">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="20" height="20">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <div class="stat-details">
              <span class="stat-value">{{ stats.bookings }}</span>
              <span class="stat-label">Bookings</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon events-icon">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="20" height="20">
                <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 005.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <div class="stat-details">
              <span class="stat-value">{{ stats.eventsJoined }}</span>
              <span class="stat-label">Events Joined</span>
            </div>
          </div>

          <div class="stat-card">
            <div class="stat-icon status-icon" :class="stats.membershipStatus.toLowerCase()">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" width="20" height="20">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <div class="stat-details">
              <span class="stat-value status-text" :class="stats.membershipStatus.toLowerCase()">
                {{ stats.membershipStatus }}
              </span>
              <span class="stat-label">Status</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  user: {
    type: Object,
    required: true,
    default: () => ({
      name: 'Varun Karthik',
      membershipType: 'Premium',
      memberSince: 'March 2025',
      avatarUrl: ''
    })
  },
  stats: {
    type: Object,
    required: true,
    default: () => ({
      bookings: 14,
      eventsJoined: 6,
      membershipStatus: 'Active'
    })
  }
})

defineEmits(['edit-avatar'])
</script>

<script>
export default {
  name: 'ProfileHeader'
}
</script>

<style scoped>
.profile-header-card {
  position: relative;
  background: #ffffff;
  border-radius: 1.75rem;
  border: 1px solid rgba(226, 232, 240, 0.8);
  box-shadow: 0 16px 40px rgba(15, 23, 42, 0.04);
  overflow: hidden;
  margin-bottom: 2rem;
  animation: fadeUp 0.6s ease both;
}

.cover-bg {
  position: relative;
  height: 11rem;
  background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 50%, #f97316 130%);
}

.cover-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(15, 23, 42, 0) 20%, rgba(15, 23, 42, 0.25) 100%);
}

.cover-pattern {
  position: absolute;
  inset: 0;
  opacity: 0.12;
  background-image: 
    radial-gradient(circle at 20% 30%, rgba(255, 255, 255, 0.2) 1px, transparent 1px),
    radial-gradient(circle at 75% 60%, rgba(255, 255, 255, 0.2) 1px, transparent 1px);
  background-size: 24px 24px;
}

.profile-content {
  position: relative;
  padding: 0 2rem 2.25rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.avatar-wrapper {
  position: relative;
  margin-top: -5.5rem;
  margin-bottom: 1.25rem;
  z-index: 10;
}

.avatar-container {
  position: relative;
  width: 9.5rem;
  height: 9.5rem;
  border-radius: 50%;
  padding: 0.35rem;
  background: #ffffff;
  box-shadow: 0 12px 30px rgba(15, 23, 42, 0.15);
}

.avatar-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid rgba(226, 232, 240, 0.6);
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1);
}

.avatar-container:hover .avatar-img {
  transform: scale(1.04);
}

.edit-avatar-btn {
  position: absolute;
  right: 0.35rem;
  bottom: 0.35rem;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: #4f46e5;
  border: 3px solid #ffffff;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 6px 14px rgba(79, 70, 229, 0.3);
  transition: transform 0.2s ease, background-color 0.2s ease;
}

.edit-avatar-btn:hover {
  transform: scale(1.1);
  background: #4338ca;
}

.details-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.meta-info {
  margin-bottom: 1.75rem;
}

.user-name {
  margin: 0 0 0.65rem;
  font-family: 'Poppins', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: -0.03em;
}

.badge-group {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.85rem;
}

.membership-badge {
  display: inline-flex;
  padding: 0.4rem 0.9rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.membership-badge.premium {
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.12), rgba(59, 130, 246, 0.12));
  color: #4f46e5;
  border: 1px solid rgba(79, 70, 229, 0.2);
}

.membership-badge.standard,
.membership-badge.basic {
  background: rgba(100, 116, 139, 0.08);
  color: #475569;
  border: 1px solid rgba(100, 116, 139, 0.15);
}

.member-since {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 500;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.25rem;
  width: 100%;
  max-width: 50rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.15rem 1.4rem;
  border-radius: 1.25rem;
  background: rgba(248, 250, 252, 0.7);
  border: 1px solid rgba(226, 232, 240, 0.8);
  transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.3s ease, border-color 0.3s ease;
  text-align: left;
}

.stat-card:hover {
  transform: translateY(-3px);
  border-color: rgba(79, 70, 229, 0.15);
  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.04);
  background: #ffffff;
}

.stat-icon {
  width: 2.75rem;
  height: 2.75rem;
  border-radius: 0.85rem;
  display: grid;
  place-items: center;
  flex-shrink: 0;
}

.bookings-icon {
  background: rgba(59, 130, 246, 0.1);
  color: #2563eb;
}

.events-icon {
  background: rgba(249, 115, 22, 0.1);
  color: #ea580c;
}

.status-icon {
  background: rgba(16, 185, 129, 0.1);
  color: #059669;
}

.status-icon.expired {
  background: rgba(239, 68, 68, 0.1);
  color: #dc2626;
}

.stat-details {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-family: 'Poppins', sans-serif;
  font-size: 1.35rem;
  font-weight: 700;
  color: #0f172a;
  line-height: 1.2;
}

.stat-value.active {
  color: #059669;
}

.stat-value.expired {
  color: #dc2626;
}

.stat-label {
  font-size: 0.8rem;
  font-weight: 500;
  color: #64748b;
  margin-top: 0.15rem;
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (min-width: 768px) {
  .profile-content {
    flex-direction: row;
    align-items: flex-end;
    text-align: left;
    padding: 0 2.5rem 2.25rem;
  }

  .avatar-wrapper {
    margin-top: -4.5rem;
    margin-bottom: 0;
    margin-right: 2.25rem;
  }

  .details-container {
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-end;
    flex: 1;
    margin-top: 1rem;
  }

  .meta-info {
    margin-bottom: 0;
  }

  .badge-group {
    justify-content: flex-start;
  }

  .stats-grid {
    width: auto;
    flex-shrink: 0;
    max-width: none;
    min-width: 26rem;
  }
}

@media (max-width: 576px) {
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 0.85rem;
  }

  .profile-content {
    padding: 0 1.25rem 1.75rem;
  }

  .avatar-container {
    width: 8rem;
    height: 8rem;
  }

  .avatar-wrapper {
    margin-top: -4rem;
  }

  .user-name {
    font-size: 1.65rem;
  }
}
</style>
