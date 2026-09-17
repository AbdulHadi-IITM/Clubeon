<!--
  Public pricing.

  Driven by GET /memberships/plans, which is the same list checkout charges
  against. It used to hardcode "₹50 / month" and "20% off" while the app
  actually billed ₹499 and applied a 50% or 100% booking discount.
-->
<template>
  <section id="pricing" class="pricing">
    <div class="section-header">
      <span class="section-tag">Pricing</span>
      <h2 class="section-title">Simple, transparent pricing</h2>
      <p class="section-desc">Pay per visit, or join a plan for a discount on every booking.</p>
    </div>

    <p v-if="error" class="pricing-error" role="alert">
      {{ error }}
      <button type="button" class="pricing-retry" @click="loadPlans">Retry</button>
    </p>

    <div v-else-if="loading" class="pricing-loading">Loading plans…</div>

    <div v-else class="pricing-grid">
      <!-- Pay as you go: always available, no plan needed. -->
      <div class="pricing-card">
        <div class="pricing-header">
          <h3 class="plan-name">Casual</h3>
          <div class="plan-price">
            <span class="plan-amount">Pay per visit</span>
          </div>
          <p class="plan-desc">No commitment. Book a court and pay for that slot.</p>
        </div>
        <ul class="plan-features">
          <li class="plan-feature">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
            Browse live court availability
          </li>
          <li class="plan-feature">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
            Book and pay online
          </li>
          <li class="plan-feature">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
            Booking confirmations and receipts
          </li>
        </ul>
        <router-link to="/public" class="plan-btn btn-secondary">View courts</router-link>
      </div>

      <div
        v-for="tier in tiers"
        :key="tier.name"
        class="pricing-card"
        :class="{ popular: tier.popular }"
      >
        <div v-if="tier.popular" class="popular-badge">Most Popular</div>
        <div class="pricing-header">
          <h3 class="plan-name">{{ tier.name }}</h3>
          <div class="plan-price">
            <span class="plan-currency">₹</span>
            <span class="plan-amount">{{ formatPrice(tier.headline.price) }}</span>
            <span class="plan-period">/{{ durationLabel(tier.headline.duration_months) }}</span>
          </div>
          <p class="plan-desc">{{ tier.headline.benefits || 'Membership plan' }}</p>
        </div>

        <ul class="plan-features">
          <li v-if="tier.headline.discount_percentage" class="plan-feature">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
            {{ tier.headline.discount_percentage }}% off every court booking
          </li>
          <li class="plan-feature">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
            Priority access to club events
          </li>
          <li class="plan-feature">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
            Cancel or let it lapse at any time
          </li>
          <li v-if="tier.otherDurations.length" class="plan-feature plan-feature-muted">
            Also available: {{ tier.otherDurations }}
          </li>
        </ul>

        <router-link to="/register" class="plan-btn" :class="tier.popular ? 'btn-primary' : 'btn-secondary'">
          Get started
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import api from '@/api/axios'

const plans = ref([])
const loading = ref(true)
const error = ref('')

function formatPrice(value) {
  return Number(value || 0).toLocaleString('en-IN')
}

function durationLabel(months) {
  if (months === 1) return 'month'
  if (months === 12) return 'year'
  return `${months} months`
}

/**
 * Plans arrive as one row per (tier, duration). Collapse them to one card per
 * tier, headlined by its shortest term.
 */
const tiers = computed(() => {
  const byName = new Map()
  for (const plan of plans.value) {
    if (!byName.has(plan.name)) byName.set(plan.name, [])
    byName.get(plan.name).push(plan)
  }

  const grouped = [...byName.entries()].map(([name, rows]) => {
    const sorted = [...rows].sort((a, b) => a.duration_months - b.duration_months)
    const [headline, ...rest] = sorted
    return {
      name,
      headline,
      otherDurations: rest
        .map((p) => `₹${formatPrice(p.price)} / ${durationLabel(p.duration_months)}`)
        .join(', '),
      popular: false,
    }
  })

  grouped.sort((a, b) => a.headline.price - b.headline.price)
  // Highlight the dearest tier — the one with the largest booking discount.
  if (grouped.length) grouped[grouped.length - 1].popular = true
  return grouped
})

async function loadPlans() {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.get('/memberships/plans')
    plans.value = Array.isArray(data) ? data : []
  } catch (err) {
    error.value = err?.response?.data?.message || 'Could not load current pricing.'
  } finally {
    loading.value = false
  }
}

onMounted(loadPlans)
</script>

<style scoped>
.pricing { position: relative; z-index: 1; max-width: 1280px; margin: 0 auto; padding: 6rem 2rem; }
.section-header { text-align: center; margin-bottom: 4rem; }
.section-tag { display: inline-block; padding: 0.25rem 0.875rem; border-radius: 2rem; background: rgba(99,102,241,0.08); border: 1px solid rgba(99,102,241,0.15); font-size: 0.8125rem; font-weight: 500; color: #a5b4fc; margin-bottom: 1rem; }
.section-title { font-size: 2.5rem; font-weight: 700; color: white; margin-bottom: 0.75rem; letter-spacing: -0.01em; }
.section-desc { font-size: 1.0625rem; color: #6b7280; max-width: 500px; margin: 0 auto; }

.pricing-loading { text-align: center; color: #6b7280; font-size: 0.9375rem; padding: 3rem 0; }
.pricing-error { display: flex; align-items: center; justify-content: center; gap: 0.75rem; color: #fca5a5; font-size: 0.9375rem; padding: 2rem 0; }
.pricing-retry { border: 1px solid rgba(252,165,165,0.35); background: transparent; color: #fca5a5; border-radius: 0.5rem; padding: 0.25rem 0.85rem; font-size: 0.8125rem; font-weight: 600; cursor: pointer; }

.pricing-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 1.5rem; align-items: start; }
.pricing-card { padding: 2rem; border-radius: 1.25rem; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); transition: all 0.3s ease; position: relative; display: flex; flex-direction: column; gap: 1.5rem; }
.pricing-card.popular { border-color: rgba(99,102,241,0.3); background: rgba(99,102,241,0.04); box-shadow: 0 8px 40px rgba(99,102,241,0.1); transform: scale(1.02); }
.popular-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); padding: 0.25rem 1rem; border-radius: 2rem; background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; font-size: 0.75rem; font-weight: 600; }
.pricing-header { text-align: center; }
.plan-name { font-size: 1.125rem; font-weight: 600; color: #f3f4f6; margin-bottom: 0.75rem; }
.plan-price { display: flex; align-items: baseline; justify-content: center; gap: 0.125rem; margin-bottom: 0.5rem; }
.plan-currency { font-size: 1.25rem; font-weight: 600; color: #6b7280; }
.plan-amount { font-size: 2.75rem; font-weight: 700; color: white; line-height: 1; }
.plan-period { font-size: 0.875rem; color: #6b7280; }
.plan-desc { font-size: 0.8125rem; color: #6b7280; }
.plan-features { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 0.75rem; flex: 1; }
.plan-feature { display: flex; align-items: center; gap: 0.625rem; font-size: 0.875rem; color: #9ca3af; }
.plan-feature svg { width: 18px; height: 18px; color: #34d399; flex-shrink: 0; }
.plan-feature-muted { color: #6b7280; font-size: 0.8125rem; }
.plan-btn { display: block; text-align: center; padding: 0.75rem 1.5rem; border-radius: 0.875rem; font-size: 0.9375rem; font-weight: 600; text-decoration: none; transition: all 0.3s ease; }
.plan-btn.btn-primary { background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; box-shadow: 0 4px 15px rgba(99,102,241,0.3); }
.plan-btn.btn-primary:hover { box-shadow: 0 6px 25px rgba(99,102,241,0.4); transform: translateY(-1px); }
.plan-btn.btn-secondary { background: rgba(255,255,255,0.04); color: #d1d5db; border: 1px solid rgba(255,255,255,0.08); }
.plan-btn.btn-secondary:hover { background: rgba(255,255,255,0.06); }

@media (max-width: 1024px) {
  .pricing-grid { grid-template-columns: 1fr; max-width: 400px; margin: 0 auto; }
  .pricing-card.popular { transform: none; }
}
@media (max-width: 768px) {
  .section-title { font-size: 1.75rem; }
}
</style>
