<template>
  <span :class="badgeClass">
    <span v-if="dot" :class="dotClass" class="w-1.5 h-1.5 rounded-full mr-1.5 shrink-0"></span>
    <span>{{ label }}</span>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: { type: String, required: true },
  dot: { type: Boolean, default: true },
})

const normalized = computed(() => (props.status || '').toLowerCase().trim())

const statusStyles = {
  confirmed: {
    badge: 'bg-emerald-50 text-emerald-700 border-emerald-200/90',
    dot: 'bg-emerald-500 animate-pulse',
  },
  active: {
    badge: 'bg-emerald-50 text-emerald-700 border-emerald-200/90',
    dot: 'bg-emerald-500 animate-pulse',
  },
  accepted: {
    badge: 'bg-emerald-50 text-emerald-700 border-emerald-200/90',
    dot: 'bg-emerald-500',
  },
  present: {
    badge: 'bg-emerald-50 text-emerald-700 border-emerald-200/90',
    dot: 'bg-emerald-500',
  },
  pending: {
    badge: 'bg-amber-50 text-amber-800 border-amber-200/90',
    dot: 'bg-amber-500 animate-pulse',
  },
  upcoming: {
    badge: 'bg-blue-50 text-blue-700 border-blue-200/90',
    dot: 'bg-blue-500',
  },
  released: {
    badge: 'bg-slate-100 text-slate-600 border-slate-200',
    dot: 'bg-slate-400',
  },
  cancelled: {
    badge: 'bg-rose-50 text-rose-700 border-rose-200/90',
    dot: 'bg-rose-500',
  },
  declined: {
    badge: 'bg-rose-50 text-rose-700 border-rose-200/90',
    dot: 'bg-rose-500',
  },
  absent: {
    badge: 'bg-rose-50 text-rose-700 border-rose-200/90',
    dot: 'bg-rose-500',
  },
  overridden: {
    badge: 'bg-purple-50 text-purple-700 border-purple-200/90',
    dot: 'bg-purple-500',
  },
  completed: {
    badge: 'bg-slate-100 text-slate-700 border-slate-200',
    dot: 'bg-slate-500',
  },
  inactive: {
    badge: 'bg-slate-100 text-slate-600 border-slate-200',
    dot: 'bg-slate-400',
  },
}

const currentConfig = computed(() => {
  return statusStyles[normalized.value] || {
    badge: 'bg-slate-100 text-slate-700 border-slate-200',
    dot: 'bg-slate-400',
  }
})

const label = computed(() => {
  const s = normalized.value
  if (!s) return 'Unknown'
  return s.charAt(0).toUpperCase() + s.slice(1)
})

const badgeClass = computed(() => [
  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border shadow-xs transition-colors',
  currentConfig.value.badge,
])

const dotClass = computed(() => currentConfig.value.dot)
</script>
