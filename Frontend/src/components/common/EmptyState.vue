<template>
  <div class="flex flex-col items-center justify-center py-12 px-6 text-center rounded-2xl border border-slate-200/80 bg-white/70 shadow-sm backdrop-blur-sm">
    <!-- Icon Container -->
    <div class="w-16 h-16 rounded-2xl bg-indigo-50 border border-indigo-100/80 flex items-center justify-center mb-4 text-indigo-500 shadow-sm">
      <!-- Calendar Icon -->
      <svg v-if="icon === 'calendar'" class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.6" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
      <!-- Courts / Grid Icon -->
      <svg v-else-if="icon === 'courts'" class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.6" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
      </svg>
      <!-- Search Icon -->
      <svg v-else-if="icon === 'search'" class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.6" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
      <!-- Members / Users Icon -->
      <svg v-else-if="icon === 'members'" class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.6" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656-.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
      <!-- Default Inbox Icon -->
      <svg v-else class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.6" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
      </svg>
    </div>

    <h3 class="text-base font-bold text-slate-800 mb-1.5">{{ title }}</h3>
    <p class="text-sm text-slate-500 max-w-sm leading-relaxed mb-4">{{ description }}</p>

    <!-- Optional Slot or Action Button -->
    <slot>
      <button v-if="actionLabel" @click="$emit('action')" class="btn-primary text-sm shadow-md">
        {{ actionLabel }}
      </button>
    </slot>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, default: 'No data found' },
  description: { type: String, default: 'There is nothing to display here yet.' },
  actionLabel: { type: String, default: '' },
  icon: { type: String, default: 'inbox' },
})
defineEmits(['action'])
</script>
