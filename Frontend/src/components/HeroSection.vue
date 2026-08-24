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
          One workspace for bookings, members and events
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
            Create free account
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6"/></svg>
          </router-link>
          <router-link to="/public" class="hero-btn-secondary">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"/><path stroke-linecap="round" stroke-linejoin="round" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            See live availability
          </router-link>
        </div>
        <div class="hero-stats">
          <div class="hero-stat">
            <span class="stat-number">10</span>
            <span class="stat-label">Sports supported</span>
          </div>
          <div class="hero-stat">
            <span class="stat-number">3</span>
            <span class="stat-label">Roles: member, staff, owner</span>
          </div>
          <div class="hero-stat">
            <span class="stat-number">Stripe</span>
            <span class="stat-label">Secure card payments</span>
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
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
  min-height: 100vh;
  justify-content: center;
}
.hero-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  text-align: left;
  gap: 1.5rem;
  max-width: 650px;
}
.hero-badge { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.375rem 1rem; border-radius: 2rem; background: rgba(99,102,241,0.08); border: 1px solid rgba(99,102,241,0.15); font-size: 0.8125rem; color: #a5b4fc; width: fit-content; }
.badge-dot { width: 6px; height: 6px; border-radius: 50%; background: #818cf8; animation: dot-pulse 2s ease-in-out infinite; }
@keyframes dot-pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
.hero-title { font-size: 3.75rem; font-weight: 800; line-height: 1.1; letter-spacing: -0.02em; text-align: left; }
.title-line { display: block; color: white; }
.title-line.gradient-text { background: linear-gradient(135deg, #818cf8, #a78bfa, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-subtitle { font-size: 1.125rem; line-height: 1.7; color: #9ca3af; max-width: 580px; margin: 0; text-align: left; }
.hero-actions { display: flex; align-items: center; justify-content: flex-start; gap: 1rem; flex-wrap: wrap; }
.hero-btn-primary { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.875rem 2rem; border-radius: 1rem; font-size: 1rem; font-weight: 600; color: white; background: linear-gradient(135deg, #6366f1, #8b5cf6); text-decoration: none; box-shadow: 0 8px 30px rgba(99,102,241,0.3); transition: all 0.3s ease; }
.hero-btn-primary:hover { box-shadow: 0 12px 40px rgba(99,102,241,0.5); transform: translateY(-2px); }
.hero-btn-primary svg { width: 18px; height: 18px; transition: transform 0.3s ease; }
.hero-btn-primary:hover svg { transform: translateX(3px); }
.hero-btn-secondary { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.875rem 2rem; border-radius: 1rem; font-size: 1rem; font-weight: 500; color: #d1d5db; border: 1px solid rgba(255,255,255,0.1); text-decoration: none; transition: all 0.3s ease; }
.hero-btn-secondary:hover { border-color: rgba(99,102,241,0.3); background: rgba(255,255,255,0.03); }
.hero-btn-secondary svg { width: 18px; height: 18px; }
.hero-stats { display: flex; justify-content: flex-start; gap: 3rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.06); width: fit-content; }
.hero-stat { display: flex; flex-direction: column; gap: 0.25rem; }
.stat-number { font-size: 1.5rem; font-weight: 700; color: white; }
.stat-label { font-size: 0.8125rem; color: #6b7280; }

@media (max-width: 1024px) {
  .hero { padding: 7rem 1.5rem 4rem; }
  .hero-title { font-size: 2.5rem; }
}
@media (max-width: 768px) {
  .hero-title { font-size: 2rem; }
  .hero-stats { gap: 1.5rem; }
}
</style>