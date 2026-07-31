<template>
  <div class="landing-page">
    <!-- ===== VIDEO BACKGROUND (only in hero) ===== -->
    <div class="hero-bg">
      <video
        ref="videoRef"
        class="hero-video"
        autoplay
        muted
        loop
        playsinline
        aria-hidden="true"
      >
        <source :src="landingVideo" type="video/mp4" />
      </video>
      <div class="hero-overlay" aria-hidden="true"></div>
    </div>

    <!-- ===== NAVBAR ===== -->
    <nav class="landing-nav" :class="{ scrolled: isScrolled }">
      <div class="nav-inner">
        <div class="nav-brand">
          <div class="brand-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <span class="brand-text">Sports<span class="brand-accent">Club</span></span>
        </div>
        <div class="nav-links">
          <a href="#features" class="nav-link">Features</a>
          <a href="#how-it-works" class="nav-link">How It Works</a>
          <a href="#pricing" class="nav-link">Pricing</a>
          <router-link to="/public" class="nav-link">Courts</router-link>
        </div>
        <div class="nav-actions">
          <router-link to="/login" class="nav-btn-secondary">Sign In</router-link>
          <router-link to="/register" class="nav-btn-primary">Get Started</router-link>
        </div>
        <button class="mobile-menu-btn" @click="mobileOpen = !mobileOpen">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path v-if="!mobileOpen" stroke-linecap="round" d="M4 6h16M4 12h16M4 18h16" />
            <path v-else stroke-linecap="round" d="M6 6l12 12M6 18L18 6" />
          </svg>
        </button>
      </div>
      <div v-if="mobileOpen" class="mobile-menu">
        <a href="#features" class="mobile-link" @click="mobileOpen = false">Features</a>
        <a href="#how-it-works" class="mobile-link" @click="mobileOpen = false">How It Works</a>
        <a href="#pricing" class="mobile-link" @click="mobileOpen = false">Pricing</a>
        <router-link to="/public" class="mobile-link" @click="mobileOpen = false">View Courts</router-link>
        <div class="mobile-actions">
          <router-link to="/login" class="nav-btn-secondary w-full block text-center">Sign In</router-link>
          <router-link to="/register" class="nav-btn-primary w-full block text-center">Get Started</router-link>
        </div>
      </div>
    </nav>

    <!-- ===== HERO with video background ===== -->
    <section class="hero">
      <div class="hero-content">
        <div class="hero-badge">
          <span class="badge-dot"></span>
          Trusted by 50+ sports clubs worldwide
        </div>
        <h1 class="hero-title">
          <span class="title-line">Book Courts.</span>
          <span class="title-line">Find Players.</span>
          <span class="title-line gradient-text">Play More.</span>
        </h1>
        <p class="hero-subtitle">
          The all-in-one platform for sports clubs. Streamline court bookings, connect with players,
          manage tournaments, and grow your community — all from one beautiful dashboard.
        </p>
        <div class="hero-actions">
          <router-link to="/register" class="hero-btn-primary">
            Start Free Trial
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
          </router-link>
          <router-link to="/public" class="hero-btn-secondary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/><path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            View Demo
          </router-link>
        </div>
        <div class="hero-stats">
          <div class="hero-stat">
            <span class="stat-number">10K+</span>
            <span class="stat-label">Active Members</span>
          </div>
          <div class="hero-stat">
            <span class="stat-number">500+</span>
            <span class="stat-label">Courts Managed</span>
          </div>
          <div class="hero-stat">
            <span class="stat-number">99.9%</span>
            <span class="stat-label">Uptime</span>
          </div>
        </div>
      </div>
      <div class="hero-visual">
        <!-- mini cards remain as in new design -->
        <div class="hero-card hero-card-1">
          <div class="mini-card">
            <div class="mini-card-header">
              <span class="mini-dot"></span>
              <span>Court A - Badminton</span>
            </div>
            <div class="mini-slots">
              <span class="mini-slot booked">09:00</span>
              <span class="mini-slot free">10:00</span>
              <span class="mini-slot free">11:00</span>
              <span class="mini-slot booked">12:00</span>
            </div>
          </div>
        </div>
        <div class="hero-card hero-card-2">
          <div class="mini-card">
            <div class="mini-card-header">
              <span class="mini-dot green"></span>
              <span>Match Found!</span>
            </div>
            <div class="mini-match">
              <div class="mini-avatars">
                <span class="mini-avatar">AT</span>
                <span class="mini-vs">vs</span>
                <span class="mini-avatar">PS</span>
              </div>
              <span class="mini-skill">Intermediate</span>
            </div>
          </div>
        </div>
        <div class="hero-card hero-card-3">
          <div class="mini-chart">
            <div class="mini-bars">
              <span v-for="h in 7" :key="h" class="mini-bar" :style="{ height: (15 + Math.random() * 60) + '%' }"></span>
            </div>
            <span class="mini-chart-label">Weekly Utilisation</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== REST OF SECTIONS (unchanged) ===== -->
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
              <span class="plan-currency">$</span>
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

    <section class="cta">
      <div class="cta-card">
        <div class="cta-glow"></div>
        <h2 class="cta-title">Ready to transform your sports club?</h2>
        <p class="cta-desc">Join thousands of clubs already using SportsClub to streamline operations and grow their community.</p>
        <div class="cta-actions">
          <router-link to="/register" class="hero-btn-primary">
            Get Started Free
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
          </router-link>
          <router-link to="/login" class="hero-btn-secondary">Sign In</router-link>
        </div>
      </div>
    </section>

    <footer class="landing-footer">
      <div class="footer-inner">
        <div class="footer-brand">
          <div class="brand-icon small">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <span class="brand-text small">Sports<span class="brand-accent">Club</span></span>
          <p class="footer-tagline">The modern way to manage your sports club.</p>
        </div>
        <div class="footer-links">
          <div class="footer-col">
            <h4>Product</h4>
            <a href="#features">Features</a>
            <a href="#pricing">Pricing</a>
            <router-link to="/public">Court Availability</router-link>
          </div>
          <div class="footer-col">
            <h4>Company</h4>
            <a href="#">About</a>
            <a href="#">Blog</a>
            <a href="#">Contact</a>
          </div>
          <div class="footer-col">
            <h4>Legal</h4>
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Service</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 SportsClub. All rights reserved. Team No. 096</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
// Import the video file (place LandingVideo.mp4 in your assets folder)
import landingVideo from '../assets/LandingVideo.mp4'

// --- Scroll & mobile state ---
const isScrolled = ref(false)
const mobileOpen = ref(false)

function onScroll() {
  isScrolled.value = window.scrollY > 50
}
onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))

// --- Data (features, steps, pricing) - unchanged from new design ---
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

const pricingPlans = [
  { name: 'Casual', price: '0', period: 'visit', desc: 'Pay per use. No commitment.', features: ['Browse court availability', 'Quick booking (pay per use)', 'Email confirmations'], cta: 'View Courts', link: '/public', popular: false },
  { name: 'Monthly', price: '50', period: 'month', desc: 'Best for regular players.', features: ['Priority court booking', 'Member discount (20% off)', 'Player matchmaking', 'Unlimited bookings', 'Tournament registration'], cta: 'Start Monthly', link: '/register', popular: true },
  { name: 'Yearly', price: '500', period: 'year', desc: 'Save 17% vs monthly.', features: ['All Monthly features', 'Access to all courts', 'Free tournament entry', 'Priority support', 'Guest passes (2/month)'], cta: 'Start Yearly', link: '/register', popular: false },
]
</script>

<style scoped>
/* ===== GLOBAL RESET & BASE ===== */
.landing-page {
  position: relative;
  overflow-x: hidden;
  min-height: 100vh;
  background: #030712; /* fallback if video fails */
  color: #e5e7eb;
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}

/* ===== HERO VIDEO BACKGROUND ===== */
.hero-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100vh; /* covers only hero area */
  z-index: 0;
  overflow: hidden;
}

.hero-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 0;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: rgba(3, 7, 18, 0.7); /* dark overlay for readability */
  z-index: 1;
}

/* ===== HERO SECTION (relative to place content above video) ===== */
.hero {
  position: relative;
  z-index: 2; /* above video */
  max-width: 1280px;
  margin: 0 auto;
  padding: 8rem 2rem 6rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  min-height: 100vh;
}

/* ===== NAVBAR ===== */
.landing-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: 1rem 0;
  transition: all 0.3s ease;
}
.landing-nav.scrolled {
  background: rgba(3, 7, 18, 0.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
}
/* ... (rest of navbar styles are unchanged, keep them from new design) ... */
/* Since the new design already has styles for all sections, we copy them below */
/* I'll include the full styles from the new design for completeness */

/* ===== COPY ALL STYLES FROM NEW DESIGN BELOW ===== */
/* (The new LandingView already has extensive styles, so we keep them) */

/* For brevity, I'll write a placeholder comment, but in the actual answer I'll include all styles. */
/* In the final answer, I will paste the complete CSS from the new design after the video styles. */

/* ===== SECTION STYLES (from new design) ===== */
/* ... all the styles for features, pricing, footer, etc. remain exactly as in the new LandingView ... */
/* We will include them fully in the final code snippet. */

/* --- NAVBAR STYLES (unchanged) --- */
.nav-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}
.nav-brand { display: flex; align-items: center; gap: 0.75rem; cursor: pointer; }
.brand-icon { width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, #6366f1, #8b5cf6); display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(99,102,241,0.3); }
.brand-icon svg { width: 20px; height: 20px; color: white; }
.brand-icon.small { width: 30px; height: 30px; border-radius: 8px; }
.brand-icon.small svg { width: 16px; height: 16px; }
.brand-text { font-size: 1.25rem; font-weight: 700; color: white; }
.brand-text.small { font-size: 1.1rem; }
.brand-accent { background: linear-gradient(135deg, #818cf8, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.nav-links { display: flex; align-items: center; gap: 0.25rem; }
.nav-link { padding: 0.5rem 1rem; border-radius: 0.75rem; font-size: 0.875rem; font-weight: 500; color: #9ca3af; text-decoration: none; transition: all 0.2s ease; }
.nav-link:hover { color: #e5e7eb; background: rgba(255,255,255,0.04); }
.nav-actions { display: flex; align-items: center; gap: 0.75rem; }
.nav-btn-secondary { padding: 0.5rem 1.25rem; border-radius: 0.75rem; font-size: 0.875rem; font-weight: 500; color: #d1d5db; text-decoration: none; transition: all 0.2s ease; }
.nav-btn-secondary:hover { background: rgba(255,255,255,0.06); }
.nav-btn-primary { padding: 0.5rem 1.25rem; border-radius: 0.75rem; font-size: 0.875rem; font-weight: 600; color: white; background: linear-gradient(135deg, #6366f1, #8b5cf6); text-decoration: none; box-shadow: 0 4px 15px rgba(99,102,241,0.3); transition: all 0.2s ease; }
.nav-btn-primary:hover { box-shadow: 0 6px 25px rgba(99,102,241,0.5); transform: translateY(-1px); }
.mobile-menu-btn { display: none; background: none; border: none; color: #9ca3af; cursor: pointer; padding: 0.5rem; border-radius: 0.5rem; }
.mobile-menu-btn svg { width: 24px; height: 24px; }
.mobile-menu-btn:hover { background: rgba(255,255,255,0.04); color: white; }
.mobile-menu { display: none; flex-direction: column; padding: 1rem 2rem 1.5rem; gap: 0.25rem; background: rgba(3,7,18,0.95); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.06); }
.mobile-link { padding: 0.75rem 1rem; border-radius: 0.75rem; font-size: 0.9375rem; font-weight: 500; color: #9ca3af; text-decoration: none; transition: all 0.2s ease; }
.mobile-link:hover { background: rgba(255,255,255,0.04); color: #e5e7eb; }
.mobile-actions { display: flex; flex-direction: column; gap: 0.5rem; margin-top: 0.5rem; padding-top: 0.75rem; border-top: 1px solid rgba(255,255,255,0.06); }

/* --- HERO CONTENT STYLES (unchanged) --- */
.hero-content { display: flex; flex-direction: column; gap: 1.5rem; }
.hero-badge { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.375rem 1rem; border-radius: 2rem; background: rgba(99,102,241,0.08); border: 1px solid rgba(99,102,241,0.15); font-size: 0.8125rem; color: #a5b4fc; width: fit-content; }
.badge-dot { width: 6px; height: 6px; border-radius: 50%; background: #818cf8; animation: dot-pulse 2s ease-in-out infinite; }
@keyframes dot-pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
.hero-title { font-size: 3.75rem; font-weight: 800; line-height: 1.1; letter-spacing: -0.02em; }
.title-line { display: block; color: white; }
.title-line.gradient-text { background: linear-gradient(135deg, #818cf8, #a78bfa, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-subtitle { font-size: 1.125rem; line-height: 1.7; color: #9ca3af; max-width: 540px; }
.hero-actions { display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; }
.hero-btn-primary { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.875rem 2rem; border-radius: 1rem; font-size: 1rem; font-weight: 600; color: white; background: linear-gradient(135deg, #6366f1, #8b5cf6); text-decoration: none; box-shadow: 0 8px 30px rgba(99,102,241,0.3); transition: all 0.3s ease; }
.hero-btn-primary:hover { box-shadow: 0 12px 40px rgba(99,102,241,0.5); transform: translateY(-2px); }
.hero-btn-primary svg { width: 18px; height: 18px; transition: transform 0.3s ease; }
.hero-btn-primary:hover svg { transform: translateX(3px); }
.hero-btn-secondary { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.875rem 2rem; border-radius: 1rem; font-size: 1rem; font-weight: 500; color: #d1d5db; border: 1px solid rgba(255,255,255,0.1); text-decoration: none; transition: all 0.3s ease; }
.hero-btn-secondary:hover { border-color: rgba(99,102,241,0.3); background: rgba(255,255,255,0.03); }
.hero-btn-secondary svg { width: 18px; height: 18px; }
.hero-stats { display: flex; gap: 2.5rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.06); }
.hero-stat { display: flex; flex-direction: column; gap: 0.25rem; }
.stat-number { font-size: 1.5rem; font-weight: 700; color: white; }
.stat-label { font-size: 0.8125rem; color: #6b7280; }

/* --- HERO VISUAL CARDS (unchanged) --- */
.hero-visual { position: relative; height: 500px; }
.hero-card { position: absolute; background: rgba(255,255,255,0.04); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.08); border-radius: 1.25rem; padding: 1.25rem; animation: card-float 6s ease-in-out infinite; box-shadow: 0 8px 32px rgba(0,0,0,0.4); }
.hero-card-1 { top: 10%; right: 10%; animation-delay: 0s; z-index: 3; }
.hero-card-2 { top: 45%; left: 0; animation-delay: -2s; z-index: 2; }
.hero-card-3 { bottom: 10%; right: 5%; animation-delay: -4s; z-index: 1; }
@keyframes card-float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-15px)} }
.mini-card { display: flex; flex-direction: column; gap: 0.75rem; }
.mini-card-header { display: flex; align-items: center; gap: 0.5rem; font-size: 0.8125rem; font-weight: 600; color: #e5e7eb; }
.mini-dot { width: 8px; height: 8px; border-radius: 50%; background: #818cf8; }
.mini-dot.green { background: #34d399; }
.mini-slots { display: flex; gap: 0.375rem; }
.mini-slot { padding: 0.25rem 0.625rem; border-radius: 0.5rem; font-size: 0.75rem; font-weight: 500; }
.mini-slot.booked { background: rgba(99,102,241,0.1); color: #818cf8; border: 1px solid rgba(99,102,241,0.15); }
.mini-slot.free { background: rgba(255,255,255,0.03); color: #6b7280; border: 1px solid rgba(255,255,255,0.05); }
.mini-match { display: flex; align-items: center; justify-content: space-between; }
.mini-avatars { display: flex; align-items: center; gap: 0.5rem; }
.mini-avatar { width: 28px; height: 28px; border-radius: 50%; background: linear-gradient(135deg, #6366f1, #8b5cf6); display: flex; align-items: center; justify-content: center; font-size: 0.625rem; font-weight: 700; color: white; }
.mini-vs { font-size: 0.6875rem; color: #6b7280; font-weight: 600; }
.mini-skill { font-size: 0.75rem; color: #fbbf24; font-weight: 500; }
.mini-chart { display: flex; flex-direction: column; gap: 0.5rem; }
.mini-bars { display: flex; align-items: flex-end; gap: 0.375rem; height: 50px; }
.mini-bar { flex: 1; border-radius: 3px 3px 0 0; background: linear-gradient(180deg, #818cf8, rgba(99,102,241,0.3)); }
.mini-chart-label { font-size: 0.6875rem; color: #6b7280; }

/* --- FEATURES, HOW IT WORKS, PRICING, CTA, FOOTER (unchanged from new design) --- */
/* I'm including them below, but they are identical to the new design's styles */
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

.pricing { position: relative; z-index: 1; max-width: 1280px; margin: 0 auto; padding: 6rem 2rem; }
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

.cta { position: relative; z-index: 1; max-width: 1280px; margin: 0 auto; padding: 6rem 2rem; }
.cta-card { position: relative; text-align: center; padding: 4rem 2rem; border-radius: 1.5rem; background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(139,92,246,0.08)); border: 1px solid rgba(99,102,241,0.15); overflow: hidden; }
.cta-glow { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 400px; height: 400px; border-radius: 50%; background: radial-gradient(circle, rgba(99,102,241,0.15), transparent 70%); pointer-events: none; }
.cta-title { font-size: 2rem; font-weight: 700; color: white; margin-bottom: 1rem; position: relative; }
.cta-desc { font-size: 1.0625rem; color: #9ca3af; max-width: 500px; margin: 0 auto 2rem; position: relative; }
.cta-actions { display: flex; align-items: center; justify-content: center; gap: 1rem; position: relative; flex-wrap: wrap; }

.landing-footer { position: relative; z-index: 1; border-top: 1px solid rgba(255,255,255,0.05); padding: 4rem 2rem 2rem; }
.footer-inner { max-width: 1280px; margin: 0 auto; display: grid; grid-template-columns: 2fr 3fr; gap: 4rem; }
.footer-brand { display: flex; flex-direction: column; gap: 0.75rem; align-items: flex-start; }
.footer-tagline { font-size: 0.875rem; color: #6b7280; margin-top: 0.25rem; }
.footer-links { display: grid; grid-template-columns: repeat(3,1fr); gap: 2rem; }
.footer-col h4 { font-size: 0.8125rem; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1rem; }
.footer-col a { display: block; font-size: 0.875rem; color: #6b7280; text-decoration: none; padding: 0.25rem 0; transition: color 0.2s ease; }
.footer-col a:hover { color: #d1d5db; }
.footer-bottom { max-width: 1280px; margin: 3rem auto 0; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.05); text-align: center; }
.footer-bottom p { font-size: 0.8125rem; color: #4b5563; }

/* --- Responsive (unchanged) --- */
@media (max-width: 1024px) {
  .hero { grid-template-columns: 1fr; gap: 2rem; min-height: auto; padding: 7rem 1.5rem 4rem; }
  .hero-visual { height: 350px; }
  .hero-title { font-size: 2.5rem; }
  .features-grid { grid-template-columns: repeat(2,1fr); }
  .steps-container { grid-template-columns: 1fr; max-width: 400px; margin: 0 auto; }
  .pricing-grid { grid-template-columns: 1fr; max-width: 400px; margin: 0 auto; }
  .pricing-card.popular { transform: none; }
  .footer-inner { grid-template-columns: 1fr; gap: 2rem; }
}
@media (max-width: 768px) {
  .nav-links, .nav-actions { display: none; }
  .mobile-menu-btn { display: block; }
  .mobile-menu { display: flex; }
  .hero-title { font-size: 2rem; }
  .hero-visual { height: 300px; }
  .hero-card-2 { left: 0; }
  .hero-card-3 { right: 0; }
  .features-grid { grid-template-columns: 1fr; }
  .hero-stats { gap: 1.5rem; }
  .section-title { font-size: 1.75rem; }
}
</style>