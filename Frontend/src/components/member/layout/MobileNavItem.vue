<template>
  <router-link
    :to="to"
    :class="[
      'flex flex-col items-center gap-0.5 px-2 py-1 rounded-lg transition-colors relative',
      isActive ? 'text-primary-400' : 'text-gray-500',
    ]"
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
        stroke-width="1.5"
        :d="icon"
      />
    </svg>

    <span class="text-[10px]">{{ label }}</span>

    <span
      v-if="badge"
      class="absolute -top-0.5 -right-0.5 bg-red-500 text-white text-[9px] rounded-full w-4 h-4 flex items-center justify-center"
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