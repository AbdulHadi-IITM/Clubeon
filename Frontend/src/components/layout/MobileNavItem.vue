<template>
  <router-link
    :to="to"
    class="flex w-[84px] shrink-0 flex-col items-center gap-1 rounded-xl px-1 py-2 text-[10px] font-semibold transition"
    :class="active ? 'text-emerald-700' : 'text-slate-500'"
  >
    <span
      class="grid h-8 w-10 place-items-center rounded-xl transition"
      :class="
        active
          ? 'bg-emerald-50 text-emerald-600 ring-1 ring-emerald-200 shadow-[0_4px_14px_rgba(16,185,129,.10)]'
          : 'text-slate-400'
      "
    >
      <svg class="h-[19px] w-[19px]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" :d="icon" />
      </svg> </span
    ><span class="truncate">{{ label }}</span>
  </router-link>
</template>
<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
const props = defineProps({ to: String, icon: String, label: String })
const route = useRoute()
const active = computed(() => route.path === props.to || route.path.startsWith(`${props.to}/`))
</script>
