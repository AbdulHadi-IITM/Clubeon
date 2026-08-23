<template>
  <div class="membership-card-container" :class="[(membership.type || 'premium').toLowerCase(), { 'is-active': (membership.status || 'Active') === 'Active' }]">
    <!-- Main Info Layout -->
    <div class="card-inner">
      <div class="header-section">
        <span class="badge">Current Plan</span>
        <h3 class="tier-name">{{ membership.type }}</h3>
        <p class="expiry-info">
          Expires: <strong>{{ membership.expiryDate }}</strong>
        </p>
      </div>

      <!-- Plan Benefits -->
      <div class="benefits-section">
        <h4 class="section-title">Your Plan Benefits</h4>
        <ul class="benefits-list">
          <li v-for="benefit in membership.benefits" :key="benefit" class="benefit-item">
            <svg class="check-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
            </svg>
            <span>{{ benefit }}</span>
          </li>
        </ul>
      </div>

      <!-- Action Footer -->
      <div class="card-footer">
        <div class="status-summary">
          <span class="status-dot" :class="(membership.status || 'active').toLowerCase()"></span>
          <span class="status-text">Status: {{ membership.status }}</span>
        </div>
        <button 
          @click="$emit('renew')" 
          class="renew-btn"
          aria-label="Renew membership"
        >
          Renew Membership
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  membership: {
    type: Object,
    required: true,
    default: () => ({
      type: 'Premium',
      expiryDate: 'December 31, 2026',
      status: 'Active',
      benefits: [
        'Uncapped facility bookings',
        'Early event access & 15% registration discount',
        'Complimentary training locker access',
        'Access to advanced performance analytics'
      ]
    })
  }
})

defineEmits(['renew'])
</script>

<script>
export default {
  name: 'MembershipCard'
}
</script>

<style scoped>
.membership-card-container {
  border-radius: 1.5rem;
  overflow: hidden;
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.04);
  transition: all 0.35s cubic-bezier(0.22, 1, 0.36, 1);
  display: flex;
  flex-direction: column;
  height: 100%;
}

.membership-card-container:hover {
  transform: translateY(-5px);
}

.card-inner {
  padding: 2.25rem 2rem 2rem;
  display: flex;
  flex-direction: column;
  height: 100%;
  position: relative;
  z-index: 1;
}

/* Premium Styling (Dark / Indigo-Purple Gradient) */
.membership-card-container.premium {
  background: linear-gradient(135deg, #1e1b4b 0%, #311042 50%, #1e1b4b 100%);
  border: 1px solid rgba(139, 92, 246, 0.25);
  color: #ffffff;
  box-shadow: 
    0 20px 48px rgba(79, 70, 229, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.membership-card-container.premium:hover {
  box-shadow: 
    0 26px 56px rgba(79, 70, 229, 0.22),
    inset 0 1px 0 rgba(255, 255, 255, 0.18);
  border-color: rgba(139, 92, 246, 0.4);
}

.membership-card-container.premium .badge {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.16);
  color: rgba(255, 255, 255, 0.9);
}

.membership-card-container.premium .tier-name {
  color: #ffffff;
}

.membership-card-container.premium .expiry-info {
  color: rgba(255, 255, 255, 0.75);
}

.membership-card-container.premium .section-title {
  color: rgba(255, 255, 255, 0.65);
}

.membership-card-container.premium .benefit-item {
  color: rgba(255, 255, 255, 0.88);
}

.membership-card-container.premium .check-icon {
  color: #8b5cf6;
  background: rgba(139, 92, 246, 0.15);
}

.membership-card-container.premium .renew-btn {
  background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
  color: #ffffff;
  box-shadow: 0 8px 24px rgba(139, 92, 246, 0.35);
}

.membership-card-container.premium .renew-btn:hover {
  background: linear-gradient(135deg, #b59dfb 0%, #9065f7 100%);
  box-shadow: 0 12px 30px rgba(139, 92, 246, 0.5);
}

/* Standard/Basic Styling (Light Theme) */
.membership-card-container:not(.premium) {
  background: #ffffff;
  border: 1px solid rgba(226, 232, 240, 0.8);
  color: #0f172a;
}

.membership-card-container:not(.premium):hover {
  border-color: rgba(37, 99, 235, 0.15);
  box-shadow: 0 16px 36px rgba(15, 23, 42, 0.05);
}

.membership-card-container:not(.premium) .badge {
  background: rgba(71, 85, 105, 0.06);
  border: 1px solid rgba(71, 85, 105, 0.12);
  color: #475569;
}

.membership-card-container:not(.premium) .tier-name {
  color: #0f172a;
}

.membership-card-container:not(.premium) .expiry-info {
  color: #64748b;
}

.membership-card-container:not(.premium) .section-title {
  color: #94a3b8;
}

.membership-card-container:not(.premium) .benefit-item {
  color: #334155;
}

.membership-card-container:not(.premium) .check-icon {
  color: #2563eb;
  background: rgba(37, 99, 235, 0.08);
}

.membership-card-container:not(.premium) .renew-btn {
  background: #2563eb;
  color: #ffffff;
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.2);
}

.membership-card-container:not(.premium) .renew-btn:hover {
  background: #1d4ed8;
  box-shadow: 0 12px 28px rgba(37, 99, 235, 0.3);
}

/* Common Layout Inner Styling */
.header-section {
  margin-bottom: 2rem;
}

.badge {
  display: inline-flex;
  padding: 0.35rem 0.85rem;
  border-radius: 999px;
  font-size: 0.725rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 1rem;
}

.tier-name {
  margin: 0 0 0.45rem;
  font-family: 'Poppins', sans-serif;
  font-size: 2.1rem;
  font-weight: 700;
  letter-spacing: -0.03em;
}

.expiry-info {
  margin: 0;
  font-size: 0.9rem;
}

.benefits-section {
  flex: 1;
  margin-bottom: 2.25rem;
}

.section-title {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin: 0 0 1rem;
}

.benefits-list {
  display: grid;
  gap: 0.85rem;
  padding: 0;
  margin: 0;
  list-style: none;
}

.benefit-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  font-size: 0.95rem;
  line-height: 1.45;
  font-weight: 500;
}

.check-icon {
  width: 1.25rem;
  height: 1.25rem;
  border-radius: 50%;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  padding: 0.2rem;
  margin-top: 0.1rem;
}

.card-footer {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(226, 232, 240, 0.15);
}

/* Light theme footer border */
.membership-card-container:not(.premium) .card-footer {
  border-top-color: rgba(226, 232, 240, 0.6);
}

.status-summary {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.88rem;
  font-weight: 600;
}

.status-dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
}

.status-dot.active {
  background-color: #10b981;
  box-shadow: 0 0 8px #10b981;
}

.status-dot.expired {
  background-color: #ef4444;
  box-shadow: 0 0 8px #ef4444;
}

.renew-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 3rem;
  border: none;
  border-radius: 0.95rem;
  font-size: 0.95rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.22, 1, 0.36, 1);
}

.renew-btn:hover {
  transform: translateY(-2px);
}

.renew-btn:active {
  transform: translateY(0);
}

@media (max-width: 576px) {
  .card-inner {
    padding: 1.75rem 1.5rem 1.5rem;
  }

  .tier-name {
    font-size: 1.85rem;
  }
}
</style>
