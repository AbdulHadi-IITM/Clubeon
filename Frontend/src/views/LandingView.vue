<template>
  <div class="landing-page">
    <NavBar />
    <HeroSection />

    <section id="features" class="features">
      <div class="section-header">
        <span class="section-tag">Features</span>
        <h2 class="section-title">Everything your club needs</h2>
        <p class="section-desc">Powerful tools to manage courts, members, and events effortlessly.</p>
      </div>
      <div class="features-grid">
        <div v-for="(feat, i) in features" :key="i" class="feature-card" :style="{ animationDelay: (i * 0.1) + 's' }">
          <div class="feature-icon" :class="feat.color">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" :d="feat.icon"/></svg>
          </div>
          <h3 class="feature-title">{{ feat.title }}</h3>
          <p class="feature-desc">{{ feat.desc }}</p>
        </div>
      </div>
    </section>

    <section id="how-it-works" class="how-it-works">
      <div class="section-header">
        <span class="section-tag">How It Works</span>
        <h2 class="section-title">Get started in 3 simple steps</h2>
        <p class="section-desc">From registration to your first booking in minutes.</p>
      </div>
      <div class="steps-container">
        <div v-for="(step, i) in steps" :key="i" class="step-card">
          <div class="step-number">0{{ i + 1 }}</div>
          <div class="step-icon" :class="step.color">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" :d="step.icon"/></svg>
          </div>
          <h3 class="step-title">{{ step.title }}</h3>
          <p class="step-desc">{{ step.desc }}</p>
          <div v-if="i < 2" class="step-connector">
            <svg viewBox="0 0 100 24" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="6 4">
              <path d="M0 12h80l10-10M90 2l10 10-10 10"/>
            </svg>
          </div>
        </div>
      </div>
    </section>

    <PricingSection />

    <section class="cta">
      <div class="cta-card">
        <div class="cta-glow"></div>
        <h2 class="cta-title">Ready to transform your sports club?</h2>
        <p class="cta-desc">Join thousands of clubs already using ClubDash to streamline operations and grow their community.</p>
        <div class="cta-actions">
          <router-link to="/register" class="hero-btn-primary">
            Get Started Free
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
          </router-link>
          <router-link to="/login" class="hero-btn-secondary">Sign In</router-link>
        </div>
      </div>
    </section>

    <FooterSection />
  </div>
</template>

<script setup>
import NavBar from '../components/NavBar.vue'
import HeroSection from '../components/HeroSection.vue'
import PricingSection from '../components/PricingSection.vue'
import FooterSection from '../components/FooterSection.vue'

const features = [
  { title: 'Smart Court Booking', desc: 'Real-time availability calendar with conflict prevention. Members get priority, casuals pay per use.', icon: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z', color: 'purple' },
  { title: 'Player Matchmaking', desc: 'Find players by skill level, send match requests, and build your network. Never play alone again.', icon: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z', color: 'emerald' },
  { title: 'Tournament Management', desc: 'Create tournaments, auto-generate brackets, manage registrations, and track results in one place.', icon: 'M16 4h2a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2M16 4v2M8 4v2m4 10l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2', color: 'amber' },
  { title: 'Attendance Tracking', desc: 'Mark attendance per session. Coaches and staff can track member participation with one tap.', icon: 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4', color: 'sky' },
  { title: 'Analytics Dashboard', desc: 'Beautiful charts showing court utilisation, membership growth, revenue, and popular time slots.', icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z', color: 'rose' },
  { title: 'Instant Notifications', desc: 'In-app alerts for bookings, cancellations, match requests, and announcements. Never miss a thing.', icon: 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9', color: 'indigo' },
]

const steps = [
  { title: 'Create Your Account', desc: 'Sign up in seconds. Choose your role — member, coach, or organiser — and set up your profile.', icon: 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z', color: 'purple' },
  { title: 'Book Your First Court', desc: 'Pick a sport, choose a court, select a time slot, and confirm. Real-time availability means no conflicts.', icon: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z', color: 'emerald' },
  { title: 'Play & Connect', desc: 'Show up, play, and connect with fellow players. Track your progress and join tournaments.', icon: 'M13 10V3L4 14h7v7l9-11h-7z', color: 'amber' },
]
</script>

<style scoped>
.landing-page {
  position: relative;
  overflow-x: hidden;
  min-height: 100vh;
  background: #030712;
  color: #e5e7eb;
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}

.features { position: relative; z-index: 1; max-width: 1280px; margin: 0 auto; padding: 6rem 2rem; }
.section-header { text-align: center; margin-bottom: 4rem; }
.section-tag { display: inline-block; padding: 0.25rem 0.875rem; border-radius: 2rem; background: rgba(99,102,241,0.08); border: 1px solid rgba(99,102,241,0.15); font-size: 0.8125rem; font-weight: 500; color: #a5b4fc; margin-bottom: 1rem; }
.section-title { font-size: 2.5rem; font-weight: 700; color: white; margin-bottom: 0.75rem; letter-spacing: -0.01em; }
.section-desc { font-size: 1.0625rem; color: #6b7280; max-width: 500px; margin: 0 auto; }
.features-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 1.5rem; }
.feature-card { padding: 2rem; border-radius: 1.25rem; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); transition: all 0.3s ease; animation: fade-up 0.6s ease-out both; }
.feature-card:hover { border-color: rgba(99,102,241,0.2); background: rgba(99,102,241,0.03); transform: translateY(-4px); box-shadow: 0 12px 40px rgba(99,102,241,0.08); }
@keyframes fade-up { from { opacity:0; transform: translateY(30px); } to { opacity:1; transform: translateY(0); } }
.feature-icon { width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 1.25rem; }
.feature-icon svg { width: 24px; height: 24px; }
.feature-icon.purple { background: rgba(99,102,241,0.1); color: #818cf8; }
.feature-icon.emerald { background: rgba(52,211,153,0.1); color: #34d399; }
.feature-icon.amber { background: rgba(251,191,36,0.1); color: #fbbf24; }
.feature-icon.sky { background: rgba(6,182,212,0.1); color: #06b6d4; }
.feature-icon.rose { background: rgba(244,96,132,0.1); color: #f472b6; }
.feature-icon.indigo { background: rgba(79,70,229,0.1); color: #6366f1; }
.feature-title { font-size: 1.0625rem; font-weight: 600; color: #f3f4f6; margin-bottom: 0.5rem; }
.feature-desc { font-size: 0.875rem; color: #6b7280; line-height: 1.6; }

.how-it-works { position: relative; z-index: 1; max-width: 1280px; margin: 0 auto; padding: 6rem 2rem; }
.steps-container { display: grid; grid-template-columns: repeat(3,1fr); gap: 2rem; align-items: flex-start; }
.step-card { position: relative; text-align: center; padding: 2.5rem 1.5rem; border-radius: 1.25rem; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); transition: all 0.3s ease; }
.step-card:hover { border-color: rgba(99,102,241,0.2); background: rgba(99,102,241,0.03); }
.step-number { position: absolute; top: -1rem; left: 50%; transform: translateX(-50%); font-size: 4rem; font-weight: 800; color: rgba(255,255,255,0.02); line-height: 1; pointer-events: none; }
.step-icon { width: 56px; height: 56px; border-radius: 14px; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.25rem; }
.step-icon svg { width: 28px; height: 28px; }
.step-icon.purple { background: rgba(99,102,241,0.12); color: #818cf8; }
.step-icon.emerald { background: rgba(52,211,153,0.12); color: #34d399; }
.step-icon.amber { background: rgba(251,191,36,0.12); color: #fbbf24; }
.step-title { font-size: 1.125rem; font-weight: 600; color: #f3f4f6; margin-bottom: 0.5rem; }
.step-desc { font-size: 0.875rem; color: #6b7280; line-height: 1.6; }
.step-connector { display: none; }

.cta { position: relative; z-index: 1; max-width: 1280px; margin: 0 auto; padding: 6rem 2rem; }
.cta-card { position: relative; text-align: center; padding: 4rem 2rem; border-radius: 1.5rem; background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(139,92,246,0.08)); border: 1px solid rgba(99,102,241,0.15); overflow: hidden; }
.cta-glow { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 400px; height: 400px; border-radius: 50%; background: radial-gradient(circle, rgba(99,102,241,0.15), transparent 70%); pointer-events: none; }
.cta-title { font-size: 2rem; font-weight: 700; color: white; margin-bottom: 1rem; position: relative; }
.cta-desc { font-size: 1.0625rem; color: #9ca3af; max-width: 500px; margin: 0 auto 2rem; position: relative; }
.cta-actions { display: flex; align-items: center; justify-content: center; gap: 1rem; position: relative; flex-wrap: wrap; }
.hero-btn-primary { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.875rem 2rem; border-radius: 1rem; font-size: 1rem; font-weight: 600; color: white; background: linear-gradient(135deg, #6366f1, #8b5cf6); text-decoration: none; box-shadow: 0 8px 30px rgba(99,102,241,0.3); transition: all 0.3s ease; }
.hero-btn-primary:hover { box-shadow: 0 12px 40px rgba(99,102,241,0.5); transform: translateY(-2px); }
.hero-btn-primary svg { width: 18px; height: 18px; transition: transform 0.3s ease; }
.hero-btn-primary:hover svg { transform: translateX(3px); }
.hero-btn-secondary { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.875rem 2rem; border-radius: 1rem; font-size: 1rem; font-weight: 500; color: #d1d5db; border: 1px solid rgba(255,255,255,0.1); text-decoration: none; transition: all 0.3s ease; }
.hero-btn-secondary:hover { border-color: rgba(99,102,241,0.3); background: rgba(255,255,255,0.03); }

@media (max-width: 1024px) {
  .features-grid { grid-template-columns: repeat(2,1fr); }
  .steps-container { grid-template-columns: 1fr; max-width: 400px; margin: 0 auto; }
}
@media (max-width: 768px) {
  .features-grid { grid-template-columns: 1fr; }
  .section-title { font-size: 1.75rem; }
}
</style>