<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <button @click="prevMonth" class="p-2 rounded-lg hover:bg-white/5 text-gray-400">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <h3 class="text-lg font-semibold text-gray-200">{{ monthLabel }}</h3>
      <button @click="nextMonth" class="p-2 rounded-lg hover:bg-white/5 text-gray-400">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>
    </div>

    <div class="grid grid-cols-7 gap-1 mb-1">
      <div v-for="day in dayNames" :key="day" class="text-center text-xs font-medium text-gray-600 py-1">{{ day }}</div>
    </div>

    <div class="grid grid-cols-7 gap-1">
      <div v-for="(day, i) in calendarDays" :key="i" :class="dayCellClass(day)" @click="day && day.currentMonth ? $emit('select', day.date) : null">
        <span v-if="day" class="relative z-10">{{ day.dayNum }}</span>
        <div v-if="day && day.currentMonth && hasEvents(day.date)" class="absolute bottom-1 left-1/2 -translate-x-1/2 flex gap-0.5">
          <span class="w-1 h-1 rounded-full bg-primary-500"></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  events: { type: Array, default: () => [] },
})

defineEmits(['select'])

const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

const currentDate = ref(new Date())

const monthLabel = computed(() => {
  return currentDate.value.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
})

function prevMonth() {
  const d = new Date(currentDate.value)
  d.setMonth(d.getMonth() - 1)
  currentDate.value = d
}

function nextMonth() {
  const d = new Date(currentDate.value)
  d.setMonth(d.getMonth() + 1)
  currentDate.value = d
}

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  const firstDay = new Date(year, month, 1).getDay()
  const daysInMonth = new Date(year, month + 1, 0).getDate()
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  const days = []
  for (let i = 0; i < firstDay; i++) {
    days.push(null)
  }
  for (let d = 1; d <= daysInMonth; d++) {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`
    const dateObj = new Date(year, month, d)
    days.push({
      dayNum: d,
      date: dateStr,
      currentMonth: true,
      isToday: dateObj.getTime() === today.getTime(),
      isPast: dateObj < today,
    })
  }
  return days
})

function hasEvents(date) {
  return props.events.some((e) => e.date === date)
}

function dayCellClass(day) {
  if (!day) return 'aspect-square'
  const base = 'aspect-square flex items-center justify-center rounded-xl text-sm relative cursor-pointer transition-all duration-200'
  if (!day.currentMonth) return `${base} text-gray-700`
  if (day.isToday) return `${base} bg-primary-500/20 text-primary-400 font-semibold border border-primary-500/30`
  if (day.isPast) return `${base} text-gray-600 cursor-default`
  return `${base} text-gray-300 hover:bg-white/[0.04] hover:text-white`
}
</script>
