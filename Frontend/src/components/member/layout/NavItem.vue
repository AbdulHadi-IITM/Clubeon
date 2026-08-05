<template>
  <router-link
    :to="to"
    :class="[
      'flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all duration-200',
      isActive
        ? 'bg-primary-500/10 text-primary-400 border border-primary-500/20'
        : 'text-gray-400 hover:text-gray-200 hover:bg-white/[0.04]',
    ]"
  >
    <svg
      class="w-5 h-5 flex-shrink-0"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="1.5"
        :d="icon"
      />
    </svg>

    <span class="flex-1">{{ label }}</span>

    <span
      v-if="badge"
      class="bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center"
    >
      {{ badge > 99 ? '99+' : badge }}
    </span>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  to: {
    type: String,
    required: true,
  },
  icon: {
    type: String,
    required: true,
  },
  label: {
    type: String,
    required: true,
  },
  badge: {
    type: Number,
    default: 0,
  },
})

const route = useRoute()

const isActive = computed(() => route.path.startsWith(props.to))
</script>