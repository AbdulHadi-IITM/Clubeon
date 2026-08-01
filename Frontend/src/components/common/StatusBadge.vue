<template>
  <span :class="badgeClass">{{ label }}</span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  status: { type: String, required: true },
})

const variants = {
  confirmed: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
  pending: 'bg-amber-500/10 text-amber-400 border border-amber-500/20',
  cancelled: 'bg-red-500/10 text-red-400 border border-red-500/20',
  released: 'bg-purple-500/10 text-purple-400 border border-purple-500/20',
  active: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
  inactive: 'bg-gray-500/10 text-gray-400 border border-gray-500/20',
  accepted: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
  declined: 'bg-red-500/10 text-red-400 border border-red-500/20',
  upcoming: 'bg-blue-500/10 text-blue-400 border border-blue-500/20',
  completed: 'bg-gray-500/10 text-gray-400 border border-gray-500/20',
  present: 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20',
  absent: 'bg-red-500/10 text-red-400 border border-red-500/20',
}

const label = computed(() => props.status.charAt(0).toUpperCase() + props.status.slice(1))
const badgeClass = computed(() => `px-2.5 py-0.5 rounded-full text-xs font-medium ${variants[props.status] || variants.confirmed}`)
</script>
