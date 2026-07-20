import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import AuthView from '../views/AuthView.vue'
import ProfileView from '../views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView,
    },
    {
      path: '/login',
      name: 'login',
      component: AuthView,
      props: { initialMode: 'login' },
    },
    {
      path: '/register',
      name: 'register',
      component: AuthView,
      props: { initialMode: 'register' },
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
    },
  ],
})

export default router