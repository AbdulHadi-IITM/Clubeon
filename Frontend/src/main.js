import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)
app.use(router)

// Restore user before mounting to avoid flicker (optional but recommended)
const auth = useAuthStore(pinia)

auth.restoreUser().finally(() => {
  // Handle global unauthorized event (fired by axios interceptor)
  window.addEventListener('unauthorized', async () => {
    await auth.logout()
    // redirect to login page
    try {
      router.push({ name: 'login' })
    } catch (e) {
      // ignore if routing fails during teardown
    }
  })

  app.mount('#app')
})
