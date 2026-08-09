<template>
  <section id="pricing" class="pricing">
    <div class="section-header">
      <span class="section-tag">Pricing</span>
      <h2 class="section-title">Simple, transparent pricing</h2>
      <p class="section-desc">Choose the plan that fits your needs. Cancel anytime.</p>
    </div>
    <div class="pricing-grid">
      <div v-for="(plan, i) in pricingPlans" :key="i" class="pricing-card" :class="{ popular: plan.popular }">
        <div v-if="plan.popular" class="popular-badge">Most Popular</div>
        <div class="pricing-header">
          <h3 class="plan-name">{{ plan.name }}</h3>
          <div class="plan-price">
            <span class="plan-currency">₹</span>
            <span class="plan-amount">{{ plan.price }}</span>
            <span class="plan-period">/{{ plan.period }}</span>
          </div>
          <p class="plan-desc">{{ plan.desc }}</p>
        </div>
        <ul class="plan-features">
          <li v-for="(f, j) in plan.features" :key="j" class="plan-feature">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
            {{ f }}
          </li>
        </ul>
        <router-link :to="plan.link" class="plan-btn" :class="plan.popular ? 'btn-primary' : 'btn-secondary'">
          {{ plan.cta }}
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup>
const pricingPlans = [
  { name: 'Casual', price: '0', period: 'visit', desc: 'Pay per use. No commitment.', features: ['Browse court availability', 'Quick booking (pay per use)', 'Email confirmations'], cta: 'View Courts', link: '/public', popular: false },
  { name: 'Monthly', price: '50', period: 'month', desc: 'Best for regular players.', features: ['Priority court booking', 'Member discount (20% off)', 'Player matchmaking', 'Unlimited bookings', 'Tournament registration'], cta: 'Start Monthly', link: '/register', popular: true },
  { name: 'Yearly', price: '500', period: 'year', desc: 'Save 17% vs monthly.', features: ['All Monthly features', 'Access to all courts', 'Free tournament entry', 'Priority support', 'Guest passes (2/month)'], cta: 'Start Yearly', link: '/register', popular: false },
]
</script>

<style scoped>
.pricing { position: relative; z-index: 1; max-width: 1280px; margin: 0 auto; padding: 6rem 2rem; }
.section-header { text-align: center; margin-bottom: 4rem; }
.section-tag { display: inline-block; padding: 0.25rem 0.875rem; border-radius: 2rem; background: rgba(99,102,241,0.08); border: 1px solid rgba(99,102,241,0.15); font-size: 0.8125rem; font-weight: 500; color: #a5b4fc; margin-bottom: 1rem; }
.section-title { font-size: 2.5rem; font-weight: 700; color: white; margin-bottom: 0.75rem; letter-spacing: -0.01em; }
.section-desc { font-size: 1.0625rem; color: #6b7280; max-width: 500px; margin: 0 auto; }
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