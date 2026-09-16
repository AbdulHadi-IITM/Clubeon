<template>
  <div class="auth-page">
    <!-- Left branding panel -->
    <div class="branding-panel">
      <div class="panel-background">
        <img :src="loginBackground" alt="Sports Arena" />
        <div class="panel-overlay"></div>
      </div>

      <div class="branding-content">
        <router-link :to="{ name: 'landing' }" class="logo">
          <BrandMark :size="34" tone="light" />
          <span class="logo-text">Clubeon</span>
        </router-link>

        <div class="branding-middle">
          <p class="panel-eyebrow">Clubeon</p>
          <h2 class="panel-heading" style="color: #ffffff !important;">Elevate Your Game.</h2>
          <p class="panel-description">
            The ultimate destination for data-driven athletic performance.
          </p>

          <div class="panel-stats">
            <div class="stat-item">
              <span class="stat-number">Live</span>
              <span class="stat-label">Court availability</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-number">Instant</span>
              <span class="stat-label">Booking confirmation</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right forms panel -->
    <div class="form-panel">
      <div class="panel-header">
        <router-link :to="{ name: 'landing' }" class="back-link">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Back to website
        </router-link>
      </div>

      <div class="form-container">
        <!-- Tab Switcher -->
        <div class="tab-switcher" role="tablist">
          <button
            class="tab-btn"
            :class="{ active: currentMode === 'login' }"
            role="tab"
            :aria-selected="currentMode === 'login'"
            @click="currentMode = 'login'"
          >
            Sign In
          </button>
          <button
            class="tab-btn"
            :class="{ active: currentMode === 'register' }"
            role="tab"
            :aria-selected="currentMode === 'register'"
            @click="currentMode = 'register'"
          >
            Create Account
          </button>
          <div
            class="tab-indicator"
            :style="{
              transform: currentMode === 'register' ? 'translateX(100%)' : 'translateX(0)',
            }"
          ></div>
        </div>

        <!-- Switchable forms -->
        <div class="form-wrapper">
          <!-- LOGIN FORM -->
          <form v-if="currentMode === 'login'" @submit.prevent="handleLogin" class="auth-form">
            <div class="form-header">
              <h2>Welcome Back</h2>
              <p>Log in to access your analytics and bookings.</p>
            </div>

            <div class="form-group">
              <label for="login-email">Email Address</label>
              <div class="input-wrapper">
                <svg
                  class="input-icon"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"
                  />
                </svg>
                <input
                  type="email"
                  id="login-email"
                  placeholder="name@example.com"
                  v-model="loginForm.email"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <div class="label-row">
                <label for="login-password">Password</label>
                <a href="#" class="forgot-link" @click.prevent="handleForgotPassword"
                  >Forgot Password?</a
                >
              </div>
              <div class="input-wrapper">
                <svg
                  class="input-icon"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                  />
                </svg>
                <input
                  :type="showPassword ? 'text' : 'password'"
                  id="login-password"
                  placeholder="••••••••"
                  v-model="loginForm.password"
                  required
                />
                <button
                  type="button"
                  class="toggle-password"
                  @click="showPassword = !showPassword"
                  aria-label="Toggle password visibility"
                >
                  <svg
                    v-if="showPassword"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="2"
                    width="18"
                    height="18"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88L8.62 8.62m4.52 4.52l1.26 1.26M18.825 18.825L3 3"
                    />
                  </svg>
                  <svg
                    v-else
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="2"
                    width="18"
                    height="18"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                    />
                  </svg>
                </button>
              </div>
            </div>

            <button type="submit" class="submit-btn">Sign In</button>
          </form>

          <!-- REGISTER FORM -->
          <form v-else @submit.prevent="handleRegister" class="auth-form">
            <div class="form-header">
              <h2>Create Account</h2>
              <p>Get started to reserve courts and manage memberships.</p>
            </div>

            <div class="form-group">
              <label for="register-name">Full Name</label>
              <div class="input-wrapper">
                <svg
                  class="input-icon"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
                <input
                  type="text"
                  id="register-name"
                  placeholder="John Doe"
                  v-model="registerForm.name"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="register-email">Email Address</label>
              <div class="input-wrapper">
                <svg
                  class="input-icon"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207"
                  />
                </svg>
                <input
                  type="email"
                  id="register-email"
                  placeholder="name@example.com"
                  v-model="registerForm.email"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label for="register-password">Password</label>
              <div class="input-wrapper">
                <svg
                  class="input-icon"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                  />
                </svg>
                <input
                  :type="showPassword ? 'text' : 'password'"
                  id="register-password"
                  placeholder="••••••••"
                  v-model="registerForm.password"
                  required
                />
                <button
                  type="button"
                  class="toggle-password"
                  @click="showPassword = !showPassword"
                  aria-label="Toggle password visibility"
                >
                  <svg
                    v-if="showPassword"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="2"
                    width="18"
                    height="18"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88L8.62 8.62m4.52 4.52l1.26 1.26M18.825 18.825L3 3"
                    />
                  </svg>
                  <svg
                    v-else
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="2"
                    width="18"
                    height="18"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                    />
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                    />
                  </svg>
                </button>
              </div>
            </div>

            <div class="form-group">
              <label class="role-label">Register As</label>
              <div class="role-cards" role="radiogroup" aria-label="Register As">
                <label
                  v-for="roleOption in roleOptions"
                  :key="roleOption.value"
                  class="role-card"
                  :class="{ active: registerForm.role === roleOption.value }"
                >
                  <input
                    type="radio"
                    name="role"
                    :value="roleOption.value"
                    v-model="registerForm.role"
                    required
                    class="role-radio-input"
                  />
                  <span class="role-card-content">
                    <span class="role-icon">
                      <svg
                        v-if="roleOption.value === 'player'"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                        />
                      </svg>
                      <svg
                        v-else-if="roleOption.value === 'front-desk'"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                        />
                      </svg>
                      <svg
                        v-else
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                        stroke-width="2"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                        />
                      </svg>
                    </span>
                    <span class="role-name">{{ roleOption.label }}</span>
                  </span>
                </label>
              </div>
            </div>

            <button type="submit" class="submit-btn">Create Account</button>
          </form>
        </div>

        <!-- The Terms and Privacy Policy links pointed at "#": the signup flow
             asked users to agree to documents that do not exist. Restore this
             line once those pages are written and routed. -->
        <div class="terms-footer">
          Your details are used only to run your club bookings.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import loginBackground from '@/assets/login_background.png'
import BrandMark from '@/components/BrandMark.vue'

const roleOptions = [
  { label: 'Player', value: 'player' },
  { label: 'Front Desk', value: 'front-desk' },
  { label: 'Owner', value: 'owner' },
]

const props = defineProps({
  initialMode: { type: String, default: 'login' },
})

const router = useRouter()
const auth = useAuthStore()

const currentMode = ref(props.initialMode)
const showPassword = ref(false)

watch(
  () => props.initialMode,
  (newVal) => {
    currentMode.value = newVal
  },
)

const loginForm = reactive({ email: '', password: '' })
const registerForm = reactive({ name: '', email: '', password: '', role: 'player' })

const redirectAfterAuth = (user) => {
  if (!auth.isAuthenticated()) {
    router.push({ name: 'login' })
    return
  }

  const redirect = router.currentRoute.value.query.redirect
  if (redirect && typeof redirect === 'string' && redirect.startsWith('/')) {
    const isOwnerOnly = redirect.startsWith('/admin')
    const isStaffOnly = redirect.startsWith('/staff')
    const isMemberOnly = redirect.startsWith('/member')

    const allowed =
      (!isOwnerOnly || user?.role === 'owner') &&
      (!isStaffOnly || user?.role === 'front-desk') &&
      (!isMemberOnly || user?.role === 'player')

    if (allowed) {
      router.push(redirect)
      return
    }
  }

  switch (user?.role) {
    case 'owner':
      router.push({ name: 'admin' })
      break

    case 'player':
      router.push({ name: 'member-dashboard' })
      break

    case 'front-desk':
      router.push({ name: 'staff-dashboard' })
      break

    default:
      router.push({ name: 'profile' })
  }
}

const handleLogin = async () => {
  try {
    const user = await auth.login({ email: loginForm.email, password: loginForm.password })
    redirectAfterAuth(user)
  } catch (err) {
    // auth.error contains message; you can show it in UI
    console.log(err)
    alert(auth.error || 'Login failed')
  }
}

const handleRegister = async () => {
  try {
    const user = await auth.register({
      name: registerForm.name,
      email: registerForm.email,
      password: registerForm.password,
      role: registerForm.role,
    })
    redirectAfterAuth(user)
  } catch (err) {
    console.log(err)
    alert(auth.error || 'Registration failed')
  }
}

const handleForgotPassword = () => {
  alert('Password reset link sent!')
}
</script>

<style scoped>
.auth-page {
  display: flex;
  min-height: 100vh;
  background: #ffffff;
  font-family: 'Inter', sans-serif;
  color: #0f172a;
}

/* Left panel style */
.branding-panel {
  position: relative;
  width: 44%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 3rem;
  color: #ffffff;
  overflow: hidden;
}

.panel-background {
  position: absolute;
  inset: 0;
  z-index: 0;
}

.panel-background img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.panel-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.45) 0%, rgba(15, 23, 42, 0.85) 100%);
}

.branding-content {
  position: relative;
  z-index: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.logo {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: #ffffff;
}

.logo-icon {
  font-size: 1.5rem;
  filter: drop-shadow(0 0 8px rgba(37, 99, 235, 0.5));
}

.logo-text {
  font-size: 1.35rem;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.branding-middle {
  margin-top: auto;
  margin-bottom: 2rem;
  max-width: 28rem;
}

.panel-eyebrow {
  color: #f97316;
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  margin: 0 0 0.85rem;
}

.panel-heading {
  font-family: 'Poppins', sans-serif;
  font-size: 2.8rem;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -0.03em;
  color: #ffffff !important;
  margin: 0 0 1.2rem;
}

.panel-description {
  color: #cbd5e1;
  font-size: 1.05rem;
  line-height: 1.6;
  margin: 0 0 3rem;
}

.panel-stats {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 700;
  font-family: 'Poppins', sans-serif;
  line-height: 1.2;
}

.stat-label {
  color: #94a3b8;
  font-size: 0.85rem;
}

.stat-divider {
  width: 1px;
  height: 2.5rem;
  background: rgba(255, 255, 255, 0.15);
}

/* Right panel style */
.form-panel {
  width: 56%;
  display: flex;
  flex-direction: column;
  background: #ffffff;
}

.panel-header {
  display: flex;
  justify-content: flex-end;
  padding: 2rem 3rem;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #64748b;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  transition: color 0.2s ease;
}

.back-link:hover {
  color: #0f172a;
}

.form-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-width: 27rem;
  width: 100%;
  margin: 0 auto;
  padding: 0 2rem 4rem;
}

/* Tab controls */
.tab-switcher {
  position: relative;
  display: flex;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 2.5rem;
}

.tab-btn {
  flex: 1;
  background: none;
  border: none;
  padding: 0.85rem 0;
  font-size: 0.95rem;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  text-align: center;
  transition: color 0.3s ease;
}

.tab-btn.active {
  color: #2563eb;
}

.tab-indicator {
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 50%;
  height: 2px;
  background: #2563eb;
  transition: transform 0.3s cubic-bezier(0.25, 1, 0.5, 1);
}

/* Form layouts */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-header {
  margin-bottom: 0.5rem;
}

.form-header h2 {
  font-family: 'Poppins', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 0.5rem;
  letter-spacing: -0.02em;
}

.form-header p {
  color: #64748b;
  font-size: 0.95rem;
  margin: 0;
  line-height: 1.5;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

label {
  font-size: 0.88rem;
  font-weight: 600;
  color: #334155;
}

.forgot-link {
  font-size: 0.85rem;
  font-weight: 600;
  color: #2563eb;
  text-decoration: none;
  transition: color 0.2s ease;
}

.forgot-link:hover {
  color: #1d4ed8;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  width: 1.2rem;
  height: 1.2rem;
  color: #94a3b8;
  pointer-events: none;
}

input {
  width: 100%;
  padding: 0.85rem 1rem 0.85rem 2.8rem;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  font-family: inherit;
  font-size: 0.95rem;
  color: #0f172a;
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}

input::placeholder {
  color: #94a3b8;
}

input:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1);
}

.toggle-password {
  position: absolute;
  right: 1rem;
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease;
}

.toggle-password:hover {
  color: #475569;
}

.submit-btn {
  margin-top: 0.5rem;
  padding: 0.9rem;
  border-radius: 0.75rem;
  border: none;
  background: #2563eb;
  color: #ffffff;
  font-family: inherit;
  font-weight: 700;
  font-size: 0.98rem;
  cursor: pointer;
  transition:
    background-color 0.2s ease,
    transform 0.1s ease;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
}

.submit-btn:hover {
  background: #1d4ed8;
}

.submit-btn:active {
  transform: scale(0.98);
}

/* Social buttons styling */
.social-section {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  color: #94a3b8;
  font-size: 0.85rem;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid #e2e8f0;
}

.divider:not(:empty)::before {
  margin-right: 0.75em;
}

.divider:not(:empty)::after {
  margin-left: 0.75em;
}

.social-buttons {
  display: flex;
  gap: 1rem;
}

.social-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.65rem;
  padding: 0.8rem;
  border-radius: 0.75rem;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  font-family: inherit;
  font-weight: 600;
  font-size: 0.92rem;
  color: #334155;
  cursor: pointer;
  transition:
    background-color 0.2s ease,
    border-color 0.2s ease;
}

.social-btn:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.terms-footer {
  margin-top: 2rem;
  text-align: center;
  font-size: 0.78rem;
  color: #64748b;
  line-height: 1.5;
}

.terms-footer a {
  color: #334155;
  font-weight: 600;
  text-decoration: underline;
}

/* Responsive collapse rules */
@media (max-width: 992px) {
  .branding-panel {
    display: none;
  }
  .form-panel {
    width: 100%;
  }
  .form-container {
    padding: 2rem 2rem 6rem;
  }
}

/* Role selector styling */
.role-label {
  font-size: 0.88rem;
  font-weight: 600;
  color: #334155;
  margin-bottom: 0.25rem;
}

.role-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.65rem;
}

.role-card {
  position: relative;
  display: flex;
  cursor: pointer;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  background: #ffffff;
  padding: 0.75rem 0.5rem;
  transition: all 0.2s ease;
  user-select: none;
}

.role-card:hover {
  border-color: #cbd5e1;
  background: #f8fafc;
}

.role-card.active {
  border-color: #2563eb;
  background: #eff6ff;
  box-shadow: 0 0 0 1px #2563eb;
}

.role-radio-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
  margin: 0;
  pointer-events: none;
}

.role-card-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  gap: 0.4rem;
}

.role-icon {
  width: 1.35rem;
  height: 1.35rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  transition: color 0.2s ease;
}

.role-icon svg {
  width: 100%;
  height: 100%;
}

.role-card.active .role-icon {
  color: #2563eb;
}

.role-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: #334155;
  transition: color 0.2s ease;
  white-space: nowrap;
}

.role-card.active .role-name {
  color: #2563eb;
}
</style>
