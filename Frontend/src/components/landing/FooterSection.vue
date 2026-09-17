<template>
  <footer class="landing-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <BrandMark :size="36" />
        <span class="brand-text small">Club<span class="brand-accent">eon</span></span>
        <p class="footer-tagline">The modern way to manage your sports club.</p>
      </div>
      <div class="footer-links">
        <div class="footer-col">
          <h4>Product</h4>
          <a href="#features">Features</a>
          <a href="#how-it-works">How it works</a>
          <a href="#pricing">Pricing</a>
        </div>
        <div class="footer-col">
          <h4>Get started</h4>
          <router-link to="/public">Court availability</router-link>
          <router-link to="/register">Create an account</router-link>
          <router-link to="/login">Sign in</router-link>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 Clubeon. All rights reserved. Team No. 096</p>
    </div>
  </footer>
</template>

<script setup>
import BrandMark from '@/components/BrandMark.vue'
</script>

<style scoped>
.landing-footer { position: relative; z-index: 1; border-top: 1px solid rgba(255,255,255,0.05); padding: 4rem 2rem 2rem; }
.footer-inner { max-width: 1280px; margin: 0 auto; display: grid; grid-template-columns: 2fr 3fr; gap: 4rem; }
.footer-brand { display: flex; flex-direction: column; gap: 0.75rem; align-items: flex-start; }
.brand-icon { width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, #6366f1, #8b5cf6); display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(99,102,241,0.3); }
.brand-icon svg { width: 20px; height: 20px; color: white; }
.brand-icon.small { width: 30px; height: 30px; border-radius: 8px; }
.brand-icon.small svg { width: 16px; height: 16px; }
.brand-text { font-size: 1.25rem; font-weight: 700; color: white; }
.brand-text.small { font-size: 1.1rem; }
.brand-accent { background: linear-gradient(135deg, #818cf8, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.footer-tagline { font-size: 0.875rem; color: #6b7280; margin-top: 0.25rem; }
.footer-links { display: grid; grid-template-columns: repeat(3,1fr); gap: 2rem; }
.footer-col h4 { font-size: 0.8125rem; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1rem; }
.footer-col a { display: block; font-size: 0.875rem; color: #6b7280; text-decoration: none; padding: 0.25rem 0; transition: color 0.2s ease; }
.footer-col a:hover { color: #d1d5db; }
.footer-bottom { max-width: 1280px; margin: 3rem auto 0; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.05); text-align: center; }
.footer-bottom p { font-size: 0.8125rem; color: #4b5563; }

@media (max-width: 1024px) {
  .footer-inner { grid-template-columns: 1fr; gap: 2rem; }
}
</style>