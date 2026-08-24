<template>
  <header class="sticky top-0 z-30 border-b border-slate-200/70 bg-[#f7f9fc]/88 backdrop-blur-xl">
    <div class="flex h-[78px] items-center justify-between gap-4 px-4 sm:px-6 lg:px-8 xl:px-10">
      <div class="min-w-0">
        <div
          class="flex items-center gap-2 text-[11px] font-semibold uppercase tracking-[.11em] text-slate-400"
        >
          <span class="text-indigo-500">ClubDash</span><span class="text-slate-300">/</span
          ><span>{{ subtitle }}</span>
        </div>
        <h1
          class="mt-1 truncate font-['Plus_Jakarta_Sans'] text-[21px] font-bold tracking-[-0.035em] text-[#172033]"
        >
          {{ title }}
        </h1>
      </div>
      <div class="flex items-center gap-2.5 relative">
        <div
          class="hidden items-center gap-2 rounded-xl border border-slate-200/80 bg-white/75 px-3 py-2 text-xs font-medium text-slate-500 shadow-sm md:flex"
        >
          <span
            class="h-2 w-2 rounded-full bg-emerald-500 shadow-[0_0_0_3px_rgba(16,185,129,.11)]"
          ></span>
          Live workspace
        </div>

          <!-- Notification Bell with Dropdown -->
        <div class="relative">
          <button
            type="button"
            @click="toggleNotifications"
            class="relative grid h-10 w-10 place-items-center rounded-xl border border-slate-200 bg-white text-slate-500 shadow-sm transition hover:border-indigo-200 hover:bg-indigo-50 hover:text-indigo-700"
            aria-label="Notifications"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.8"
                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
              />
            </svg>
            <span
              v-if="unreadCount > 0"
              class="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-red-500 text-[10px] font-bold text-white shadow-sm ring-2 ring-white"
            >
              {{ unreadCount > 9 ? '9+' : unreadCount }}
            </span>
          </button>

          <!-- Notifications Dropdown Popover -->
          <div
            v-if="showNotifications"
            class="absolute right-0 mt-2 w-80 sm:w-96 rounded-2xl border border-slate-200 bg-white shadow-2xl z-50 overflow-hidden"
          >
            <div class="flex items-center justify-between border-b border-slate-100 bg-slate-50/80 px-4 py-3">
              <div class="flex items-center gap-2">
                <span class="text-base">🔔</span>
                <h3 class="text-sm font-bold text-slate-900">Notifications & Alerts</h3>
              </div>
              <button
                v-if="unreadCount > 0"
                @click="notificationStore.markAllAsRead()"
                class="text-xs font-semibold text-indigo-600 hover:text-indigo-800"
              >
                Mark all read
              </button>
            </div>

            <div class="max-h-80 overflow-y-auto divide-y divide-slate-100">
              <div
                v-if="notificationsList.length === 0"
                class="py-8 text-center text-sm text-slate-400"
              >
                No announcements or notifications yet.
              </div>
              <div
                v-for="item in notificationsList"
                :key="item.id"
                class="p-3.5 transition hover:bg-slate-50 flex items-start gap-3 cursor-pointer"
                :class="{ 'bg-indigo-50/40': !item.is_read }"
                @click="notificationStore.markAsRead(item.id)"
              >
                <div class="mt-0.5 text-lg">
                  {{ item.icon || '📢' }}
                </div>
                <div class="min-w-0 flex-1">
                  <div class="flex items-center justify-between gap-2">
                    <span class="text-[11px] font-bold uppercase tracking-wider text-indigo-600">
                      {{ item.category || item.type || 'Notice' }}
                    </span>
                    <span class="text-[10px] text-slate-400">{{ item.date || item.created_at?.slice(0, 10) }}</span>
                  </div>
                  <h4 class="text-xs font-bold text-slate-900 line-clamp-1 mt-0.5">
                    {{ item.title }}
                  </h4>
                  <p class="text-xs text-slate-500 line-clamp-2 mt-0.5 leading-relaxed">
                    {{ item.body }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <button
          @click="logout"
          type="button"
          class="hidden items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 shadow-sm transition hover:border-indigo-200 hover:bg-indigo-50 hover:text-indigo-700 sm:flex"
        >
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.8"
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h6a2 2 0 012 2v1"
            />
          </svg>
          Sign out
        </button>
      </div>
    </div>
  </header>
</template>
<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotificationStore } from '@/stores/notifications'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const notificationStore = useNotificationStore()

const showNotifications = ref(false)
const title = computed(() => route.meta.title || 'Dashboard')
const subtitle = computed(() => route.meta.subtitle || 'Portal')

const notificationsList = computed(() => notificationStore.announcements)
const unreadCount = computed(() => notificationStore.unreadCount)

function toggleNotifications() {
  showNotifications.value = !showNotifications.value
  if (showNotifications.value) {
    notificationStore.fetchNotifications()
  }
}

let pollInterval = null

onMounted(() => {
  notificationStore.fetchNotifications()
  pollInterval = setInterval(() => {
    notificationStore.fetchNotifications()
  }, 15000)
})

onUnmounted(() => {
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
})

watch(
  () => route.fullPath,
  () => {
    showNotifications.value = false
    notificationStore.fetchNotifications()
  },
)

async function logout() {
  try {
    await auth.logout()
  } finally {
    router.push({ name: 'login' })
  }
}
</script>
