import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'

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
  window.addEventListener('unauthorized', async () => {
    await auth.logout()
    router.push({ name: 'login' })
  })
  app.mount('#app')
})
