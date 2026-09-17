import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'
import './style.css'

import Vue3Toastify, { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(Vue3Toastify, { autoClose: 3000 }) // 3 seconds timeout

// Provide toast globally so you can use it anywhere without importing
app.provide('toast', toast)

const auth = useAuthStore(pinia)

auth.restoreUser().finally(() => {
  // A 401 means "this request needed a session". Only send the user to the
  // login screen if they were actually on a page that requires one — an
  // anonymous visitor browsing the landing or public-availability page used to
  // be bounced to /login by the 401 from the startup /auth/me probe.
  window.addEventListener('unauthorized', async () => {
    const route = router.currentRoute.value
    if (!route.matched.some((record) => record.meta?.requiresAuth)) return

    await auth.logout()
    router.push({ name: 'login', query: { redirect: route.fullPath } })
  })
  app.mount('#app')
})
