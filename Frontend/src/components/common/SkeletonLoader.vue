<template>
  <div class="skeleton-wrapper w-full" aria-busy="true" aria-live="polite">
    <!-- STATS SKELETON -->
    <div v-if="type === 'stats'" class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div v-for="i in count" :key="i" class="glass p-5 animate-pulse space-y-3">
        <div class="h-3 w-20 bg-slate-200/80 rounded"></div>
        <div class="h-8 w-14 bg-slate-300/80 rounded-lg"></div>
        <div class="h-2.5 w-32 bg-slate-200/60 rounded"></div>
      </div>
    </div>

    <!-- CARD SKELETON (e.g. Courts / Events / Bookings) -->
    <div v-else-if="type === 'card'" :class="gridClass">
      <div
        v-for="i in count"
        :key="i"
        class="glass overflow-hidden animate-pulse border border-slate-200/70 shadow-sm"
      >
        <div class="h-40 w-full bg-slate-200/80"></div>
        <div class="p-5 space-y-3">
          <div class="flex items-center justify-between">
            <div class="h-5 w-36 bg-slate-300/80 rounded-md"></div>
            <div class="h-4 w-16 bg-slate-200 rounded-full"></div>
          </div>
          <div class="h-3.5 w-48 bg-slate-200/70 rounded"></div>
          <div class="grid grid-cols-2 gap-2 pt-2">
            <div class="h-10 bg-slate-200/60 rounded-xl"></div>
            <div class="h-10 bg-slate-200/60 rounded-xl"></div>
          </div>
          <div class="h-10 w-full bg-slate-300/60 rounded-xl mt-3"></div>
        </div>
      </div>
    </div>

    <!-- SLOTS SKELETON (e.g. Court Booking Time Slots) -->
    <div v-else-if="type === 'slots'" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
      <div
        v-for="i in count"
        :key="i"
        class="glass overflow-hidden animate-pulse border border-slate-200/70 p-5 space-y-4"
      >
        <div class="flex justify-between items-start">
          <div class="space-y-2">
            <div class="h-5 w-32 bg-slate-300 rounded-md"></div>
            <div class="h-3.5 w-20 bg-slate-200 rounded"></div>
          </div>
          <div class="h-5 w-16 bg-emerald-100 rounded-full"></div>
        </div>
        <div class="grid grid-cols-2 gap-2 pt-2">
          <div v-for="s in 6" :key="s" class="h-14 bg-slate-200/70 rounded-xl"></div>
        </div>
        <div class="h-11 w-full bg-indigo-200/60 rounded-xl mt-2"></div>
      </div>
    </div>

    <!-- TABLE SKELETON (e.g. Admin Bookings, Attendance, Members) -->
    <div v-else-if="type === 'table'" class="glass overflow-hidden animate-pulse border border-slate-200/70">
      <div class="p-4 border-b border-slate-200/60 flex items-center justify-between">
        <div class="h-5 w-40 bg-slate-300 rounded"></div>
        <div class="h-8 w-28 bg-slate-200 rounded-lg"></div>
      </div>
      <div class="divide-y divide-slate-100">
        <div v-for="i in count" :key="i" class="p-4 flex items-center justify-between gap-4">
          <div class="flex items-center gap-3 min-w-0 flex-1">
            <div class="h-9 w-9 bg-slate-200 rounded-full shrink-0"></div>
            <div class="space-y-1.5 min-w-0 flex-1">
              <div class="h-4 w-32 bg-slate-300 rounded"></div>
              <div class="h-3 w-48 bg-slate-200 rounded"></div>
            </div>
          </div>
          <div class="hidden sm:block h-4 w-24 bg-slate-200 rounded"></div>
          <div class="h-6 w-20 bg-slate-200 rounded-full"></div>
          <div class="h-8 w-16 bg-slate-200 rounded-lg"></div>
        </div>
      </div>
    </div>

    <!-- DEFAULT ROW LIST SKELETON -->
    <div v-else class="space-y-3">
      <div
        v-for="i in count"
        :key="i"
        class="glass p-4 animate-pulse flex items-center justify-between border border-slate-200/70"
      >
        <div class="space-y-2 flex-1">
          <div class="h-4 w-1/3 bg-slate-300 rounded"></div>
          <div class="h-3 w-1/2 bg-slate-200 rounded"></div>
        </div>
        <div class="h-8 w-24 bg-slate-200 rounded-lg"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'card',
    validator: (v) => ['card', 'slots', 'table', 'stats', 'list'].includes(v),
  },
  count: {
    type: Number,
    default: 3,
  },
  gridCols: {
    type: String,
    default: 'grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5',
  },
})

const gridClass = computed(() => props.gridCols)
</script>
