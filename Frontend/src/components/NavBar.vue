<template>
  <nav class="landing-nav" :class="{ scrolled: isScrolled }">
    <div class="nav-inner">
      <div class="nav-brand">
        <div class="brand-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <span class="brand-text">Club<span class="brand-accent">Dash</span></span>
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
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isScrolled = ref(false)
const mobileOpen = ref(false)

function onScroll() {
  isScrolled.value = window.scrollY > 50
}
onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
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
.brand-text { font-size: 1.25rem; font-weight: 700; color: white; }
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

@media (max-width: 768px) {
  .nav-links, .nav-actions { display: none; }
  .mobile-menu-btn { display: block; }
  .mobile-menu { display: flex; }
}
</style>