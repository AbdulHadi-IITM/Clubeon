<template>
  <header class="navbar" :class="{ 'is-scrolled': isScrolled }">
    <div class="container">
      <a href="#top" class="logo" aria-label="ClubDash home">
        <span class="mark">C</span>
        <span class="logo-text">ClubDash</span>
      </a>

      <nav class="nav-links" aria-label="Primary navigation">
        <a href="#features" :class="{ active: activeSection === 'features' }" @click="activeSection = 'features'">Features</a>
        <a href="#facilities" :class="{ active: activeSection === 'facilities' }" @click="activeSection = 'facilities'">Facilities</a>
        <a href="#membership" :class="{ active: activeSection === 'membership' }" @click="activeSection = 'membership'">Membership</a>
        <a href="#contact" :class="{ active: activeSection === 'contact' }" @click="activeSection = 'contact'">Contact</a>
      </nav>

      <div class="actions">
        <router-link to="/login" class="login-btn">Login</router-link>
        <router-link to="/register" class="primary-btn">Get Started</router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'

const isScrolled = ref(false)
const activeSection = ref('')

const updateScrollState = () => {
  isScrolled.value = window.scrollY > 80
  if (window.scrollY < 120) {
    activeSection.value = ''
  }
}

let observer = null

onMounted(() => {
  updateScrollState()
  window.addEventListener('scroll', updateScrollState, { passive: true })

  // Intersection Observer to highlight active navbar links on scroll
  const sections = ['features', 'facilities', 'membership', 'contact']
  const observerOptions = {
    root: null,
    rootMargin: '-30% 0px -60% 0px',
    threshold: 0.1
  }

  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        activeSection.value = entry.target.id
      }
    })
  }, observerOptions)

  sections.forEach((id) => {
    const el = document.getElementById(id)
    if (el) observer.observe(el)
  })
})

onBeforeUnmount(() => {
  window.removeEventListener('scroll', updateScrollState)
  if (observer) {
    observer.disconnect()
  }
})
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: transparent;
  border-bottom: 1px solid transparent;
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  box-shadow: none;
  transition:
    background-color 0.4s ease,
    backdrop-filter 0.4s ease,
    -webkit-backdrop-filter 0.4s ease,
    border-color 0.4s ease,
    box-shadow 0.4s ease;
}

.navbar.is-scrolled {
  background: rgba(255, 255, 255, 0.82);
  border-bottom-color: rgba(226, 232, 240, 0.75);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  box-shadow: 0 8px 32px rgba(15, 23, 42, 0.06);
}

.container {
  width: min(1200px, calc(100% - 2rem));
  margin: 0 auto;
  min-height: 5rem;
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 1.25rem;
}

.logo {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  font-family: 'Poppins', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  transition: color 0.4s ease;
}

.navbar:not(.is-scrolled) .logo {
  color: #ffffff;
}

.navbar.is-scrolled .logo {
  color: #0f172a;
}

.mark {
  width: 2.45rem;
  height: 2.45rem;
  display: grid;
  place-items: center;
  border-radius: 0.95rem;
  color: #ffffff;
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 55%, #f97316 150%);
  box-shadow: 0 14px 28px rgba(37, 99, 235, 0.22);
  flex-shrink: 0;
}

.nav-links {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
}

.nav-links a,
.login-btn,
.primary-btn {
  transition:
    transform 0.2s ease,
    color 0.35s ease,
    background-color 0.35s ease,
    box-shadow 0.2s ease,
    border-color 0.35s ease;
}

.nav-links a {
  position: relative;
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.navbar:not(.is-scrolled) .nav-links a {
  color: #ffffff;
}

.navbar.is-scrolled .nav-links a {
  color: #475569;
}

.nav-links a::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -0.55rem;
  width: 100%;
  height: 2px;
  border-radius: 999px;
  background: linear-gradient(90deg, #2563eb, #f97316);
  transform: scaleX(0);
  transform-origin: center;
  transition: transform 0.2s ease;
}

.navbar.is-scrolled .nav-links a:hover,
.navbar.is-scrolled .nav-links a:focus-visible {
  color: #0f172a;
}

.navbar:not(.is-scrolled) .nav-links a:hover,
.navbar:not(.is-scrolled) .nav-links a:focus-visible {
  color: rgba(255, 255, 255, 0.85);
}

.nav-links a:hover::after,
.nav-links a:focus-visible::after,
.nav-links a.active::after {
  transform: scaleX(1);
}

.navbar:not(.is-scrolled) .nav-links a.active {
  color: #ffffff;
}

.navbar.is-scrolled .nav-links a.active {
  color: #2563eb;
}

.actions {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
}

.login-btn,
.primary-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.75rem;
  padding: 0.8rem 1.15rem;
  border-radius: 999px;
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.navbar:not(.is-scrolled) .login-btn {
  color: #ffffff;
  background: transparent;
  border: 1.5px solid rgba(255, 255, 255, 0.85);
}

.navbar.is-scrolled .login-btn {
  color: #0f172a;
  background: rgba(15, 23, 42, 0.04);
  border: 1px solid rgba(15, 23, 42, 0.08);
}

.primary-btn {
  color: #ffffff;
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  border: 1px solid transparent;
  box-shadow: 0 14px 28px rgba(37, 99, 235, 0.22);
}

.login-btn:hover,
.login-btn:focus-visible,
.primary-btn:hover,
.primary-btn:focus-visible {
  transform: translateY(-1px);
}

.navbar:not(.is-scrolled) .login-btn:hover,
.navbar:not(.is-scrolled) .login-btn:focus-visible {
  background: rgba(255, 255, 255, 0.1);
}

.navbar.is-scrolled .login-btn:hover,
.navbar.is-scrolled .login-btn:focus-visible {
  background: rgba(15, 23, 42, 0.07);
}

.primary-btn:hover,
.primary-btn:focus-visible {
  box-shadow: 0 18px 36px rgba(37, 99, 235, 0.28);
}

@media (max-width: 980px) {
  .container {
    grid-template-columns: auto auto;
    grid-template-areas:
      'logo actions'
      'nav nav';
    padding: 0.9rem 0;
  }

  .logo {
    grid-area: logo;
  }

  .nav-links {
    grid-area: nav;
    justify-content: flex-start;
    overflow-x: auto;
    padding-bottom: 0.25rem;
    scrollbar-width: none;
  }

  .nav-links::-webkit-scrollbar {
    display: none;
  }

  .actions {
    grid-area: actions;
    margin-left: auto;
  }
}

@media (max-width: 640px) {
  .container {
    width: min(100% - 1rem, 1200px);
  }

  .actions {
    width: 100%;
    gap: 0.6rem;
  }

  .login-btn,
  .primary-btn {
    flex: 1 1 0;
    min-width: 0;
  }
}
</style>
