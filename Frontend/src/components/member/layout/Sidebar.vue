<template>
  <!-- Desktop Sidebar -->
  <aside
    class="hidden lg:flex flex-col w-64 border-r border-white/5 bg-white/[0.02]"
  >
    <!-- Logo -->
    <div class="p-5 border-b border-white/5">
      <router-link to="/" class="flex items-center gap-3">
        <div
          class="w-9 h-9 rounded-lg bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center"
        >
          <svg
            class="w-5 h-5 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M13 10V3L4 14h7v7l9-11h-7z"
            />
          </svg>
        </div>

        <span class="font-bold text-lg gradient-text">
          ClubDash
        </span>
      </router-link>
    </div>

    <!-- Member Navigation -->
    <nav class="flex-1 p-4 space-y-1 overflow-y-auto">
      <NavItem
        to="/member/dashboard"
        :icon="icons.home"
        label="Dashboard"
      />

      <NavItem
        to="/member/book-court"
        :icon="icons.calendar"
        label="Book a Court"
      />

      <NavItem
        to="/member/my-bookings"
        :icon="icons.clipboard"
        label="My Bookings"
      />

  

      <NavItem
        to="/member/notifications"
        :icon="icons.bell"
        label="Notifications"
      />

      <NavItem
        to="/member/profile"
        :icon="icons.user"
        label="Profile"
      />
    </nav>

    <!-- Logged-in User -->
    <div class="p-4 border-t border-white/5">
      <div class="glass px-4 py-3 rounded-xl">
        <div class="flex items-center gap-3">
          <div
            class="w-8 h-8 rounded-full bg-gradient-to-br from-primary-400 to-accent-500 flex items-center justify-center text-white text-xs font-bold"
          >
            {{ userInitial }}
          </div>

          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium text-gray-200 truncate">
              {{ displayName }}
            </p>

            <p class="text-xs text-gray-500 capitalize">
              {{ authStore.user?.role || 'Member' }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </aside>

  <!-- Mobile Bottom Navigation -->
  <aside
    class="lg:hidden fixed bottom-0 left-0 right-0 z-50 glass-strong border-t border-white/10 rounded-none pb-safe"
  >
    <div class="flex justify-around py-2">
      <MobileNavItem
        to="/member/dashboard"
        :icon="icons.home"
        label="Home"
      />

      <MobileNavItem
        to="/member/book-court"
        :icon="icons.calendar"
        label="Book"
      />

      <MobileNavItem
        to="/member/my-bookings"
        :icon="icons.clipboard"
        label="Bookings"
      />

      <MobileNavItem
        to="/member/notifications"
        :icon="icons.bell"
        label="Alerts"
      />

      <MobileNavItem
        to="/member/profile"
        :icon="icons.user"
        label="Profile"
      />
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import NavItem from './NavItem.vue'
import MobileNavItem from './MobileNavItem.vue'

const authStore = useAuthStore()

const displayName = computed(() => {
  const user = authStore.user

  if (!user) return 'Member'

  return (
    user.name ||
    user.full_name ||
    user.username ||
    user.email ||
    'Member'
  )
})

const userInitial = computed(() => {
  return displayName.value.charAt(0).toUpperCase()
})

const icons = {
  home:
    'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6',

  calendar:
    'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',

  clipboard:
    'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',

  users:
    'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656-.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z',

  bell:
    'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9',

  user:
    'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
}
</script>