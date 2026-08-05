<template>
  <header
    class="glass border-b border-white/5 rounded-none m-0 px-4 md:px-6 py-3 flex items-center justify-between"
  >
    <div>
      <h1 class="text-lg font-semibold text-gray-200">
        {{ pageTitle }}
      </h1>

      <p class="text-xs text-gray-500">
        {{ pageSubtitle }}
      </p>
    </div>

    <div class="flex items-center gap-3">
      <router-link
        to="/member/notifications"
        class="relative p-2 rounded-lg hover:bg-white/5 text-gray-400 transition-colors"
        aria-label="Notifications"
      >
        <svg
          class="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
          />
        </svg>
      </router-link>

      <button
        type="button"
        class="btn-secondary text-sm !py-1.5 !px-3"
        :disabled="authStore.loading"
        @click="handleLogout"
      >
        {{ authStore.loading ? 'Logging out...' : 'Logout' }}
      </button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const pageTitle = computed(() => route.meta.title || 'Sports Club')

const pageSubtitle = computed(
  () => route.meta.subtitle || 'Member Portal',
)

async function handleLogout() {
  await authStore.logout()
  await router.push({ name: 'login' })
}
</script>