import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LandingView from '../views/LandingView.vue'
import AuthView from '../views/AuthView.vue'
import ProfileView from '../views/ProfileView.vue'
import AdminDashboardView from '../views/AdminDashboardView.vue'

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
      meta: { requiresAuth: true },
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminDashboardView,
      meta: { requiresAuth: true, requiresRole: 'owner' },
    },
      {
    path: '/public',
    name: 'PublicAvailability',
    component: () => import('../views/Availability.vue'),
  },
  ],
})

const getHomeRouteForUser = (user) => {
  return { name: user?.role === 'owner' ? 'admin' : 'profile' }
}

router.beforeEach(async (to) => {
  const auth = useAuthStore()

  const isAuthed = auth.isAuthenticated()

  if (to.meta.requiresAuth && !isAuthed) {
    return { name: 'login' }
  }

  if (to.meta.requiresRole && auth.user?.role !== to.meta.requiresRole) {
    return isAuthed ? getHomeRouteForUser(auth.user) : { name: 'login' }
  }

  if ((to.name === 'login' || to.name === 'register') && isAuthed) {
    return getHomeRouteForUser(auth.user)
  }

})

export default router
