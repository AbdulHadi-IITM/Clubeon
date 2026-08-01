<template>
  <div class="hero-wrapper">
    <div class="hero-bg">
      <video ref="videoRef" class="hero-video" autoplay muted loop playsinline aria-hidden="true">
        <source :src="landingVideo" type="video/mp4" />
      </video>
      <div class="hero-overlay" aria-hidden="true"></div>
    </div>

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
              <span v-for="(h, idx) in chartBars" :key="idx" class="mini-bar" :style="{ height: h + '%' }"></span>
            </div>
            <span class="mini-chart-label">Weekly Utilisation</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import landingVideo from '../assets/LandingVideo.mp4'

const videoRef = ref(null)

// Chart bar heights, generated once (fixes flicker on re-render)
const chartBars = [42, 68, 35, 79, 51, 24, 63]
</script>

<style scoped>
.hero-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100vh;
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
  background: rgba(3, 7, 18, 0.7);
  z-index: 1;
}
.hero {
  position: relative;
  z-index: 2;
  max-width: 1280px;
  margin: 0 auto;
  padding: 8rem 2rem 6rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
  min-height: 100vh;
}
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

@media (max-width: 1024px) {
  .hero { grid-template-columns: 1fr; gap: 2rem; min-height: auto; padding: 7rem 1.5rem 4rem; }
  .hero-visual { height: 350px; }
  .hero-title { font-size: 2.5rem; }
}
@media (max-width: 768px) {
  .hero-title { font-size: 2rem; }
  .hero-visual { height: 300px; }
  .hero-card-2 { left: 0; }
  .hero-card-3 { right: 0; }
  .hero-stats { gap: 1.5rem; }
}
</style>