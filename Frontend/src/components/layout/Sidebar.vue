<template>
  <aside
    class="fixed inset-y-0 left-0 z-40 hidden w-[276px] flex-col overflow-hidden bg-[#151d2e] text-white shadow-[18px_0_50px_rgba(23,32,51,.08)] lg:flex"
  >
    <div class="px-5 pb-5 pt-6">
      <router-link :to="homePath" class="flex items-center gap-3">
        <div
          class="grid h-11 w-11 place-items-center rounded-2xl bg-gradient-to-br from-indigo-400 to-indigo-600 text-white shadow-[0_10px_26px_rgba(82,103,232,.28)] ring-1 ring-white/10"
        >
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M13 3L4 14h7v7l9-11h-7V3z"
            />
          </svg>
        </div>
        <div>
          <div class="text-[19px] font-extrabold tracking-[-0.03em] text-white">
            Club<span class="text-indigo-300">Dash</span>
          </div>
          <div class="mt-0.5 text-[10px] font-bold uppercase tracking-[0.18em] text-slate-500">
            {{ portalLabel }}
          </div>
        </div>
      </router-link>
    </div>
    <div class="mx-5 h-px bg-white/[0.07]"></div>
    <nav class="flex-1 space-y-1.5 overflow-y-auto px-4 py-5">
      <p class="mb-3 px-3 text-[10px] font-bold uppercase tracking-[0.16em] text-slate-500">
        Workspace
      </p>
      <NavItem v-for="item in navigation" :key="item.to" v-bind="item" />
    </nav>
    <div class="p-4">
      <router-link
        :to="profilePath"
        class="flex items-center gap-3 rounded-2xl border border-white/[0.08] bg-white/[0.045] p-3 transition hover:border-indigo-400/30 hover:bg-white/[0.075]"
      >
        <div
          class="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-indigo-500/20 text-sm font-bold text-indigo-200 ring-1 ring-indigo-400/20"
        >
          {{ userInitial }}
        </div>
        <div class="min-w-0 flex-1">
          <p class="truncate text-sm font-semibold text-slate-100">{{ displayName }}</p>
          <p class="mt-0.5 text-xs text-slate-500">{{ roleLabel }}</p>
        </div>
        <svg class="h-4 w-4 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </router-link>
    </div>
  </aside>

  <aside
    class="fixed bottom-3 left-3 right-3 z-50 overflow-x-auto rounded-2xl border border-slate-200/90 bg-white/95 p-1.5 shadow-[0_16px_45px_rgba(15,23,42,.14)] backdrop-blur-xl lg:hidden"
  >
    <div class="flex min-w-max items-center justify-start">
      <MobileNavItem
        v-for="item in mobileNavigation"
        :key="item.to"
        :to="item.to"
        :icon="item.icon"
        :label="item.mobileLabel || item.label"
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
const icons = {
  home: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6',
  map: 'M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0zM15 11a3 3 0 11-6 0 3 3 0 016 0z',
  calendar:
    'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
  clipboard:
    'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
  users:
    'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656-.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z',
  check: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
  courts: 'M5 5h14v14H5zM5 12h14M12 5v14',
  events: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
  card: 'M3 7a2 2 0 012-2h14a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2V7zm0 3h18m-13 4h3',
}
const memberNavigation = [
  { to: '/member/dashboard', icon: icons.home, label: 'Dashboard', mobileLabel: 'Home' },
  { to: '/member/book-court', icon: icons.calendar, label: 'Book a Court', mobileLabel: 'Book' },
  { to: '/member/nearby-courts', icon: icons.map, label: 'Nearby Courts', mobileLabel: 'Nearby' },
  {
    to: '/member/my-bookings',
    icon: icons.clipboard,
    label: 'My Bookings',
    mobileLabel: 'Bookings',
  },
  { to: '/member/events', icon: icons.events, label: 'Events' },
  { to: '/member/membership', icon: icons.card, label: 'Membership', mobileLabel: 'Membership' },
]
const staffNavigation = [
  { to: '/staff/dashboard', icon: icons.home, label: 'Dashboard', mobileLabel: 'Home' },
  { to: '/staff/bookings', icon: icons.clipboard, label: 'Bookings' },
  {
    to: '/staff/availability',
    icon: icons.courts,
    label: 'Court Availability',
    mobileLabel: 'Courts',
  },
  { to: '/staff/attendance', icon: icons.check, label: 'Attendance' },
  { to: '/staff/members', icon: icons.users, label: 'Members' },
  { to: '/staff/events', icon: icons.events, label: 'Events' },
]
const isStaff = computed(() => authStore.user?.role === 'front-desk')
const navigation = computed(() => (isStaff.value ? staffNavigation : memberNavigation))
const mobileNavigation = computed(() => navigation.value)
const homePath = computed(() => (isStaff.value ? '/staff/dashboard' : '/member/dashboard'))
const profilePath = computed(() => (isStaff.value ? '/staff/profile' : '/member/profile'))
const portalLabel = computed(() => (isStaff.value ? 'Front Desk Portal' : 'Member Portal'))
const roleLabel = computed(() => (isStaff.value ? 'Front Desk' : 'Member'))
const displayName = computed(() => {
  const u = authStore.user
  return u?.name || u?.full_name || u?.username || u?.email || roleLabel.value
})
const userInitial = computed(() => displayName.value.charAt(0).toUpperCase())
</script>
