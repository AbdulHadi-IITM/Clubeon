<template>
  <router-link :to="to" class="group relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-[13.5px] font-semibold transition-all duration-200" :class="active ? 'bg-emerald-400/[0.11] text-emerald-200 shadow-[inset_0_0_0_1px_rgba(110,231,183,.20),0_0_24px_rgba(16,185,129,.08)]' : 'text-slate-400 hover:bg-white/[0.055] hover:text-slate-100'">
    <span v-if="active" class="absolute -left-4 h-7 w-[3px] rounded-r-full bg-emerald-300 shadow-[0_0_14px_rgba(110,231,183,.75)]"></span>
    <span class="grid h-8 w-8 place-items-center rounded-lg transition-all" :class="active?'bg-emerald-400/[0.14] text-emerald-200 ring-1 ring-emerald-300/20':'text-slate-500 group-hover:bg-white/[0.05] group-hover:text-slate-300'">
      <svg class="h-[18px] w-[18px]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" :d="icon"/></svg>
    </span><span>{{ label }}</span>
  </router-link>
</template>
<script setup>
import { computed } from 'vue'; import { useRoute } from 'vue-router'
const props=defineProps({to:String,icon:String,label:String}); const route=useRoute(); const active=computed(()=>route.path===props.to||route.path.startsWith(`${props.to}/`))
</script>
