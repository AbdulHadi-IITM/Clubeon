<template>
  <div class="space-y-6">

    <!-- Welcome -->
    <div>
      <h1 class="text-2xl font-bold gradient-text">
        Welcome back, {{ firstName }}
      </h1>
      <p class="text-sm text-gray-500 mt-1">
        Here is what's happening at the club today.
      </p>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

      <!-- Total Bookings -->
      <div class="glass card-hover p-5 fade-up">
        <div class="flex items-center gap-3 mb-3">
          <div
            class="w-10 h-10 rounded-xl bg-primary-500/10 flex items-center justify-center"
          >
            <svg
              class="w-5 h-5 text-primary-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.5"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
          </div>

          <span class="text-xs text-gray-500 uppercase tracking-wider">
            Total Bookings
          </span>
        </div>

        <p class="text-3xl font-bold text-white">
          {{ bookings.length }}
        </p>
      </div>

      <!-- Days Left -->
      <div
        class="glass card-hover p-5 fade-up"
        style="animation-delay: 0.1s"
      >
        <div class="flex items-center gap-3 mb-3">
          <div
            class="w-10 h-10 rounded-xl bg-emerald-500/10 flex items-center justify-center"
          >
            <svg
              class="w-5 h-5 text-emerald-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.5"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>

          <span class="text-xs text-gray-500 uppercase tracking-wider">
            Days Left
          </span>
        </div>

        <p class="text-3xl font-bold text-white">
          {{ daysLeft }}
        </p>
      </div>

      <!-- Upcoming -->
      <div
        class="glass card-hover p-5 fade-up"
        style="animation-delay: 0.2s"
      >
        <div class="flex items-center gap-3 mb-3">
          <div
            class="w-10 h-10 rounded-xl bg-accent-500/10 flex items-center justify-center"
          >
            <svg
              class="w-5 h-5 text-accent-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.5"
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
          </div>

          <span class="text-xs text-gray-500 uppercase tracking-wider">
            Upcoming
          </span>
        </div>

        <p class="text-3xl font-bold text-white">
          {{ upcomingBookings.length }}
        </p>
      </div>

      <!-- Membership -->
      <div
        class="glass card-hover p-5 fade-up"
        style="animation-delay: 0.3s"
      >
        <div class="flex items-center gap-3 mb-3">
          <div
            class="w-10 h-10 rounded-xl bg-amber-500/10 flex items-center justify-center"
          >
            <svg
              class="w-5 h-5 text-amber-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.5"
                d="M12 3l7 4v5c0 5-3 8-7 9-4-1-7-4-7-9V7l7-4z"
              />
            </svg>
          </div>

          <span class="text-xs text-gray-500 uppercase tracking-wider">
            Membership
          </span>
        </div>

        <p class="text-xl font-bold text-white capitalize">
          {{ activeMembership?.plan_name || 'No Plan' }}
        </p>
      </div>
    </div>

    <!-- Main dashboard -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Left -->
      <div class="lg:col-span-2 space-y-6">

        <!-- Membership Status -->
        <div
          class="glass p-5 fade-up"
          style="animation-delay: 0.2s"
        >
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-base font-semibold text-gray-200">
              Membership Status
            </h3>

            <span
              class="px-3 py-1 rounded-full text-xs font-medium capitalize"
              :class="
                activeMembership
                  ? 'bg-emerald-500/10 text-emerald-400'
                  : 'bg-red-500/10 text-red-400'
              "
            >
              {{ activeMembership ? 'Active' : 'Inactive' }}
            </span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">

            <div>
              <p class="text-xs text-gray-500 mb-1">
                Plan Type
              </p>

              <p class="text-sm font-medium text-gray-200">
                {{ activeMembership?.plan_name || 'No active membership' }}
              </p>
            </div>

            <div>
              <p class="text-xs text-gray-500 mb-1">
                Start Date
              </p>

              <p class="text-sm font-medium text-gray-200">
                {{ activeMembership?.start_date || 'N/A' }}
              </p>
            </div>

            <div>
              <p class="text-xs text-gray-500 mb-1">
                Expiry Date
              </p>

              <p class="text-sm font-medium text-gray-200">
                {{ activeMembership?.end_date || 'N/A' }}
              </p>
            </div>

          </div>
        </div>

        <!-- Upcoming bookings -->
        <div
          class="glass p-5 fade-up"
          style="animation-delay: 0.3s"
        >
          <div class="flex items-center justify-between mb-4">

            <h3 class="text-base font-semibold text-gray-200">
              Upcoming Bookings
            </h3>

            <router-link
              to="/member/my-bookings"
              class="text-xs text-primary-400 hover:text-primary-300"
            >
              View all
            </router-link>

          </div>

          <!-- Loading -->
          <div
            v-if="loading"
            class="py-10 text-center text-sm text-gray-500"
          >
            Loading bookings...
          </div>

          <!-- Error -->
          <div
            v-else-if="error"
            class="py-10 text-center"
          >
            <p class="text-sm text-red-400">
              {{ error }}
            </p>
          </div>

          <!-- Empty -->
          <div
            v-else-if="upcomingBookings.length === 0"
            class="py-10 text-center"
          >
            <div
              class="w-12 h-12 mx-auto mb-3 rounded-xl bg-primary-500/10 flex items-center justify-center"
            >
              <svg
                class="w-6 h-6 text-primary-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="1.5"
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
            </div>

            <p class="text-sm font-medium text-gray-300">
              No upcoming bookings
            </p>

            <p class="text-xs text-gray-500 mt-1">
              You have no upcoming court bookings.
            </p>

            <button
              class="btn-primary mt-4"
              @click="goTo('/member/book-court')"
            >
              Book a Court
            </button>
          </div>

          <!-- Booking list -->
          <div
            v-else
            class="space-y-3"
          >
            <div
              v-for="booking in upcomingBookings"
              :key="booking.id"
              class="flex items-center justify-between p-3 rounded-xl bg-white/[0.02] border border-white/5 hover:border-primary-500/20 transition-all duration-200"
            >
              <div class="flex items-center gap-3">

                <div
                  class="w-10 h-10 rounded-lg bg-primary-500/10 flex items-center justify-center"
                >
                  <svg
                    class="w-5 h-5 text-primary-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="1.5"
                      d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                    />
                  </svg>
                </div>

                <div>
                  <p class="text-sm font-medium text-gray-200">
                    {{ booking.court_name }}
                  </p>

                  <p class="text-xs text-gray-500">
                    {{ booking.club_name }}
                  </p>

                  <p class="text-xs text-gray-500 mt-1">
                    {{ booking.date }}
                    |
                    {{ formatTime(booking.start_time) }}
                    -
                    {{ formatTime(booking.end_time) }}
                  </p>
                </div>

              </div>

              <span
                class="px-2.5 py-1 rounded-full text-xs font-medium capitalize"
                :class="statusClass(booking.status)"
              >
                {{ booking.status }}
              </span>

            </div>
          </div>
        </div>
      </div>

      <!-- Right -->
      <div class="space-y-6">

        <!-- Quick Actions -->
        <div
          class="glass p-5 fade-up"
          style="animation-delay: 0.1s"
        >
          <h3 class="text-base font-semibold text-gray-200 mb-4">
            Quick Actions
          </h3>

          <div class="space-y-2">

            <button
              @click="goTo('/member/book-court')"
              class="btn-primary w-full flex items-center gap-3 justify-center"
            >
              <svg
                class="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                />
              </svg>

              Book a Court
            </button>

            <button
              @click="goTo('/member/my-bookings')"
              class="btn-secondary w-full flex items-center gap-3 justify-center"
            >
              <svg
                class="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>

              My Bookings
            </button>

            <button
              @click="goTo('/profile')"
              class="btn-secondary w-full flex items-center gap-3 justify-center"
            >
              <svg
                class="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 12a4 4 0 100-8 4 4 0 000 8zm-7 8a7 7 0 0114 0"
                />
              </svg>

              Manage Profile
            </button>

          </div>
        </div>

        <!-- Club Activity -->
        <div
          class="glass p-5 fade-up"
          style="animation-delay: 0.4s"
        >
          <h3 class="text-base font-semibold text-gray-200 mb-4">
            Club Activity
          </h3>

          <div class="space-y-4">

            <div
              class="flex items-center justify-between p-3 rounded-xl bg-white/[0.02] border border-white/5"
            >
              <div>
                <p class="text-xs text-gray-500">
                  Upcoming bookings
                </p>

                <p class="text-lg font-semibold text-gray-200 mt-1">
                  {{ upcomingBookings.length }}
                </p>
              </div>

              <div
                class="w-9 h-9 rounded-lg bg-primary-500/10 flex items-center justify-center"
              >
                <svg
                  class="w-4 h-4 text-primary-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="1.5"
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
            </div>

            <div
              class="flex items-center justify-between p-3 rounded-xl bg-white/[0.02] border border-white/5"
            >
              <div>
                <p class="text-xs text-gray-500">
                  Membership
                </p>

                <p
                  class="text-sm font-semibold mt-1 capitalize"
                  :class="
                    activeMembership
                      ? 'text-emerald-400'
                      : 'text-gray-400'
                  "
                >
                  {{ activeMembership?.status || 'Inactive' }}
                </p>
              </div>

              <div
                class="w-9 h-9 rounded-lg bg-emerald-500/10 flex items-center justify-center"
              >
                <svg
                  class="w-4 h-4 text-emerald-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="1.5"
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/axios'

const router = useRouter()
const authStore = useAuthStore()

const bookings = ref([])
const memberships = ref([])

const loading = ref(true)
const error = ref('')

const firstName = computed(() => {
  const user = authStore.user

  if (!user) return 'Member'

  const name =
    user.name ||
    user.full_name ||
    user.username ||
    user.email ||
    'Member'

  return String(name).split(' ')[0]
})

const activeMembership = computed(() => {
  if (!memberships.value.length) return null

  return (
    memberships.value.find(
      (membership) =>
        String(membership.status).toLowerCase() === 'active'
    ) || null
  )
})

const daysLeft = computed(() => {
  if (!activeMembership.value?.end_date) return 0

  const end = new Date(
    `${activeMembership.value.end_date}T23:59:59`
  )

  const today = new Date()

  const difference = Math.ceil(
    (end.getTime() - today.getTime()) /
      (1000 * 60 * 60 * 24)
  )

  return Math.max(0, difference)
})

const upcomingBookings = computed(() => {
  const now = new Date()

  return bookings.value
    .filter((booking) => {
      if (!booking.date) return false

      const status = String(
        booking.status || ''
      ).toLowerCase()

      if (
        status === 'cancelled' ||
        status === 'released' ||
        status === 'overridden'
      ) {
        return false
      }

      const time =
        booking.start_time ||
        '00:00:00'

      const bookingDate = new Date(
        `${booking.date}T${time}`
      )

      return bookingDate >= now
    })
    .sort((a, b) => {
      const first = new Date(
        `${a.date}T${a.start_time || '00:00:00'}`
      )

      const second = new Date(
        `${b.date}T${b.start_time || '00:00:00'}`
      )

      return first - second
    })
    .slice(0, 5)
})

async function loadDashboard() {
  loading.value = true
  error.value = ''

  try {
    const [bookingResponse, membershipResponse] =
      await Promise.all([
        api.get('/bookings'),
        api.get('/memberships/my-memberships'),
      ])

    bookings.value = Array.isArray(bookingResponse.data)
      ? bookingResponse.data
      : []

    memberships.value = Array.isArray(
      membershipResponse.data
    )
      ? membershipResponse.data
      : []
  } catch (err) {
    console.error(
      'Failed to load member dashboard:',
      err
    )

    error.value =
      err?.response?.data?.message ||
      'Unable to load dashboard data.'
  } finally {
    loading.value = false
  }
}

function formatTime(time) {
  if (!time) return ''

  return String(time).slice(0, 5)
}

function statusClass(status) {
  const value = String(status || '').toLowerCase()

  if (
    value === 'active' ||
    value === 'confirmed'
  ) {
    return 'bg-emerald-500/10 text-emerald-400'
  }

  if (
    value === 'cancelled' ||
    value === 'released' ||
    value === 'overridden'
  ) {
    return 'bg-red-500/10 text-red-400'
  }

  return 'bg-amber-500/10 text-amber-400'
}

function goTo(path) {
  router.push(path)
}

onMounted(async () => {
  if (!authStore.user) {
    await authStore.restoreUser()
  }

  await loadDashboard()
})
</script>

<style scoped>
.fade-up {
  animation: fade-up-in 0.5s ease-out both;
}

@keyframes fade-up-in {
  from {
    opacity: 0;
    transform: translateY(24px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>