<template>
  <header class="sticky top-0 z-30 border-b border-slate-200/70 bg-[#f7f9fc]/88 backdrop-blur-xl">
    <div class="flex h-[78px] items-center justify-between gap-4 px-4 sm:px-6 lg:px-8 xl:px-10">
      <div class="min-w-0">
        <div class="flex items-center gap-2 text-[11px] font-semibold uppercase tracking-[.11em] text-slate-400">
          <span class="text-indigo-500">ClubDash</span><span class="text-slate-300">/</span><span>{{ subtitle }}</span>
        </div>
        <h1 class="mt-1 truncate font-['Plus_Jakarta_Sans'] text-[21px] font-bold tracking-[-0.035em] text-[#172033]">{{ title }}</h1>
      </div>
      <div class="flex items-center gap-2.5">
        <div class="hidden items-center gap-2 rounded-xl border border-slate-200/80 bg-white/75 px-3 py-2 text-xs font-medium text-slate-500 shadow-sm md:flex">
          <span class="h-2 w-2 rounded-full bg-emerald-500 shadow-[0_0_0_3px_rgba(16,185,129,.11)]"></span> Live workspace
        </div>
        <button type="button" class="relative grid h-10 w-10 place-items-center rounded-xl border border-slate-200 bg-white text-slate-500 shadow-sm transition hover:border-indigo-200 hover:bg-indigo-50 hover:text-indigo-700" aria-label="Notifications">
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/></svg>
        </button>
        <button @click="logout" type="button" class="hidden items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 shadow-sm transition hover:border-indigo-200 hover:bg-indigo-50 hover:text-indigo-700 sm:flex">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h6a2 2 0 012 2v1"/></svg>
          Sign out
        </button>
      </div>
    </div>
  </header>
</template>
<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
const route=useRoute(); const router=useRouter(); const auth=useAuthStore()
const title=computed(()=>route.meta.title||'Dashboard'); const subtitle=computed(()=>route.meta.subtitle||'Portal')
async function logout(){ try{ await auth.logout() } finally{ router.push({name:'login'}) } }
</script>
