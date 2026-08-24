import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// ============================================================
// Public / Common Views
// ============================================================

import LandingView from '@/views/LandingView.vue'
import AuthView from '@/views/AuthView.vue'

// ============================================================
// Admin / Owner
// ============================================================

import AdminDashboardView from '@/views/AdminDashboardView.vue'

// ============================================================
// Shared Authenticated Layout
// ============================================================

import AppLayout from '@/components/layout/AppLayout.vue'

// ============================================================
// Member
// ============================================================

import MemberDashboard from '@/views/member/Dashboard.vue'

// ============================================================
// Router
// ============================================================

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    // ========================================================
    // PUBLIC ROUTES
    // ========================================================

    {
      path: '/',
      name: 'landing',
      component: LandingView,
      meta: {
        title: 'ClubDash',
      },
    },

    {
      path: '/login',
      name: 'login',
      component: AuthView,
      props: {
        initialMode: 'login',
      },
      meta: {
        title: 'Sign In',
      },
    },

    {
      path: '/register',
      name: 'register',
      component: AuthView,
      props: {
        initialMode: 'register',
      },
      meta: {
        title: 'Register',
      },
    },

    {
      path: '/public',
      name: 'public-availability',
      component: () => import('@/views/Availability.vue'),
      meta: {
        title: 'Court Availability',
      },
    },

    // ========================================================
    // MEMBER / PLAYER PORTAL
    // ========================================================

    {
      path: '/member',
      component: AppLayout,

      meta: {
        requiresAuth: true,
        requiresRole: 'player',
      },

      children: [
        {
          path: '',
          redirect: {
            name: 'member-dashboard',
          },
        },

        {
          path: 'dashboard',
          name: 'member-dashboard',
          component: MemberDashboard,

          meta: {
            requiresAuth: true,
            requiresRole: 'player',
            title: 'Dashboard',
            subtitle: 'Member Portal',
          },
        },

        {
          path: 'book-court',
          name: 'member-book-court',
          component: () =>
            import('@/views/member/BookCourt.vue'),

          meta: {
            requiresAuth: true,
            requiresRole: 'player',
            title: 'Book a Court',
            subtitle: 'Member Portal',
          },
        },

        {
          path: 'nearby-courts',
          name: 'member-nearby-courts',
          component: () => import('@/views/member/NearbyCourts.vue'),
          meta: {
            requiresAuth: true,
            requiresRole: 'player',
            title: 'Nearby Courts',
            subtitle: 'Member Portal',
          },
        },

        {
          path: 'my-bookings',
          name: 'member-my-bookings',
          component: () =>
            import('@/views/member/MyBooking.vue'),

          meta: {
            requiresAuth: true,
            requiresRole: 'player',
            title: 'My Bookings',
            subtitle: 'Member Portal',
          },
        },

        {
          path: 'events',
          name: 'member-events',
          component: () => import('@/views/member/Events.vue'),
          meta: { requiresAuth: true, requiresRole: 'player', title: 'Events', subtitle: 'Member Portal' },
        },

        {
          path: 'bookings/:bookingId',
          name: 'member-booking-details',
          component: () => import('@/views/member/BookingDetails.vue'),
          meta: { requiresAuth: true, requiresRole: 'player', title: 'Booking Details', subtitle: 'Member Portal' },
        },

        {
          path: 'events/:eventId',
          name: 'member-event-details',
          component: () => import('@/views/member/EventDetails.vue'),
          meta: { requiresAuth: true, requiresRole: 'player', title: 'Event Details', subtitle: 'Member Portal' },
        },

        {
          path: 'membership',
          name: 'member-membership',
          component: () => import('@/views/member/MembershipPlans.vue'),
          meta: { requiresAuth: true, requiresRole: 'player', title: 'Membership', subtitle: 'Member Portal' },
        },

        {
          path: 'checkout',
          name: 'member-checkout',
          component: () => import('@/views/member/Checkout.vue'),
          meta: { requiresAuth: true, requiresRole: 'player', title: 'Checkout', subtitle: 'Member Portal' },
        },

        {
          path: 'profile',
          name: 'member-profile',
          component: () => import('@/views/ProfileView.vue'),
          meta: { requiresAuth: true, requiresRole: 'player', title: 'My Profile', subtitle: 'Member Portal' },
        },
      ],
    },

    // ========================================================
    // FRONT DESK / STAFF PORTAL
    // ========================================================

    {
      path: '/staff',
      component: AppLayout,

      meta: {
        requiresAuth: true,
        requiresRole: 'front-desk',
      },

      children: [
        {
          path: '',
          redirect: {
            name: 'staff-dashboard',
          },
        },

        {
          path: 'dashboard',
          name: 'staff-dashboard',
          component: () =>
            import('@/views/staff/Dashboard.vue'),

          meta: {
            requiresAuth: true,
            requiresRole: 'front-desk',
            title: 'Dashboard',
            subtitle: 'Front Desk Portal',
          },
        },

        {
          path: 'bookings',
          name: 'staff-bookings',
          component: () =>
            import('@/views/staff/Bookings.vue'),

          meta: {
            requiresAuth: true,
            requiresRole: 'front-desk',
            title: 'Bookings',
            subtitle: 'Front Desk Portal',
          },
        },

        {
          path: 'availability',
          name: 'staff-availability',
          component: () =>
            import('@/views/staff/Availability.vue'),

          meta: {
            requiresAuth: true,
            requiresRole: 'front-desk',
            title: 'Court Availability',
            subtitle: 'Front Desk Portal',
          },
        },

        {
          path: 'attendance',
          name: 'staff-attendance',
          component: () =>
            import('@/views/staff/Attendance.vue'),

          meta: {
            requiresAuth: true,
            requiresRole: 'front-desk',
            title: 'Attendance',
            subtitle: 'Front Desk Portal',
          },
        },

        {
          path: 'bookings/:bookingId',
          name: 'staff-booking-detail',
          component: () => import('@/views/staff/BookingDetails.vue'),
          meta: { requiresAuth: true, requiresRole: 'front-desk', title: 'Booking Details', subtitle: 'Front Desk Portal' },
        },

        {
          path: 'members/:userId',
          name: 'staff-member-detail',
          component: () => import('@/views/staff/MemberDetails.vue'),
          meta: { requiresAuth: true, requiresRole: 'front-desk', title: 'Member Details', subtitle: 'Front Desk Portal' },
        },

        {
          path: 'members',
          name: 'staff-members',
          component: () => import('@/views/staff/Members.vue'),
          meta: { requiresAuth: true, requiresRole: 'front-desk', title: 'Members', subtitle: 'Front Desk Portal' },
        },

        {
          path: 'events',
          name: 'staff-events',
          component: () => import('@/views/staff/Events.vue'),
          meta: { requiresAuth: true, requiresRole: 'front-desk', title: 'Events', subtitle: 'Front Desk Portal' },
        },

        {
          path: 'profile',
          name: 'staff-profile',
          component: () => import('@/views/ProfileView.vue'),
          meta: { requiresAuth: true, requiresRole: 'front-desk', title: 'My Profile', subtitle: 'Front Desk Portal' },
        },
      ],
    },

    // ========================================================
    // OWNER / ADMIN
    // ========================================================

    {
      path: '/admin',
      name: 'admin',
      component: AdminDashboardView,

      meta: {
        requiresAuth: true,
        requiresRole: 'owner',
        title: 'Admin Dashboard',
        subtitle: 'Owner Portal',
      },
    },

    // ========================================================
    // COMMON AUTHENTICATED ROUTES
    // ========================================================

    {
      path: '/profile',
      name: 'profile',
      redirect: () => {
        const auth = useAuthStore()
        if (auth.user?.role === 'front-desk') return { name: 'staff-profile' }
        if (auth.user?.role === 'owner') return { name: 'admin' }
        return { name: 'member-profile' }
      },
    },

    // ========================================================
    // FALLBACK
    // ========================================================

    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
  ],
})

// ============================================================
// ROLE HOME ROUTING
// ============================================================

function getHomeRouteForUser(user) {
  if (!user) {
    return {
      name: 'landing',
    }
  }

  switch (user.role) {
    case 'owner':
      return {
        name: 'admin',
      }

    case 'player':
      return {
        name: 'member-dashboard',
      }

    case 'front-desk':
      return {
        name: 'staff-dashboard',
      }

    default:
      return {
        name: 'profile',
      }
  }
}

// ============================================================
// GLOBAL ROUTE GUARD
// ============================================================

router.beforeEach(async (to) => {
  const auth = useAuthStore()

  // ----------------------------------------------------------
  // Restore authenticated user
  // ----------------------------------------------------------
  //
  // Authentication uses cookies, so after a hard refresh
  // Pinia may initially have no user even though the browser
  // still has a valid authenticated session.
  //
  // Restore the user before evaluating RBAC.
  // ----------------------------------------------------------

  if (!auth.initialized) {
    try {
      await auth.restoreUser()
    } catch (error) {
      console.error(
        'Failed to restore authentication session:',
        error,
      )
    }
  }

  const isAuthed = auth.isAuthenticated()

  // ----------------------------------------------------------
  // Authentication Guard
  // ----------------------------------------------------------

  if (to.meta.requiresAuth && !isAuthed) {
    return {
      name: 'login',
      query: {
        redirect: to.fullPath,
      },
    }
  }

  // ----------------------------------------------------------
  // Role Guard
  // ----------------------------------------------------------

  if (
    to.meta.requiresRole &&
    auth.user?.role !== to.meta.requiresRole
  ) {
    return isAuthed
      ? getHomeRouteForUser(auth.user)
      : {
          name: 'login',
        }
  }

  // ----------------------------------------------------------
  // Prevent authenticated users from returning to auth pages
  // ----------------------------------------------------------

  if (
    (to.name === 'login' || to.name === 'register') &&
    isAuthed
  ) {
    return getHomeRouteForUser(auth.user)
  }

  return true
})

// ============================================================
// PAGE TITLE
// ============================================================

router.afterEach((to) => {
  const title = to.meta?.title

  // The landing route's own title is the brand, so don't render "ClubDash | ClubDash".
  document.title = title && title !== 'ClubDash'
    ? `${title} | ClubDash`
    : 'ClubDash — Sports Club Management'
})

export default router