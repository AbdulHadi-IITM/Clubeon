import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import LandingView from '../views/LandingView.vue'
import AuthView from '../views/AuthView.vue'
import ProfileView from '../views/ProfileView.vue'
import AdminDashboardView from '../views/AdminDashboardView.vue'

// Member layout + pages
import MemberLayout from '@/components/member/layout/AppLayout.vue'
import MemberDashboard from '@/views/member/Dashboard.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    // ==========================
    // Public Routes
    // ==========================

    {
      path: '/',
      name: 'landing',
      component: LandingView,
    },

    {
      path: '/login',
      name: 'login',
      component: AuthView,
      props: {
        initialMode: 'login',
      },
    },

    {
      path: '/register',
      name: 'register',
      component: AuthView,
      props: {
        initialMode: 'register',
      },
    },

    {
      path: '/public',
      name: 'PublicAvailability',
      component: () => import('../views/Availability.vue'),
    },

    // ==========================
    // Member Routes
    // ==========================

    {
      path: '/member',
      component: MemberLayout,
      meta: {
        requiresAuth: true,
        requiresRole: 'player',
      },

      children: [
        {
          path: '',
          redirect: { name: 'member-dashboard' },
        },

        {
          path: 'dashboard',
          name: 'member-dashboard',
          component: MemberDashboard,
          meta: {
            title: 'Dashboard',
          },
        },
      ],
    },

    // ==========================
    // Owner Routes
    // ==========================

    {
      path: '/admin',
      name: 'admin',
      component: AdminDashboardView,
      meta: {
        requiresAuth: true,
        requiresRole: 'owner',
      },
    },

    // ==========================
    // Existing Profile
    // ==========================

    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: {
        requiresAuth: true,
      },
    },
  ],
})

// ==========================
// Role Home Route
// ==========================

function getHomeRouteForUser(user) {
  if (!user) {
    return { name: 'landing' }
  }

  switch (user.role) {
    case 'owner':
      return { name: 'admin' }

    case 'player':
      return { name: 'member-dashboard' }

    default:
      return { name: 'profile' }
  }
}

// ==========================
// Navigation Guard
// ==========================

router.beforeEach(async (to) => {
  const auth = useAuthStore()

  const isAuthed = auth.isAuthenticated()

  // Protected route without authentication
  if (to.meta.requiresAuth && !isAuthed) {
    return { name: 'login' }
  }

  // Route requires a particular role
  if (
    to.meta.requiresRole &&
    auth.user?.role !== to.meta.requiresRole
  ) {
    return isAuthed
      ? getHomeRouteForUser(auth.user)
      : { name: 'login' }
  }

  // Already logged in → don't show login/register
  if (
    (to.name === 'login' || to.name === 'register') &&
    isAuthed
  ) {
    return getHomeRouteForUser(auth.user)
  }
})

export default router