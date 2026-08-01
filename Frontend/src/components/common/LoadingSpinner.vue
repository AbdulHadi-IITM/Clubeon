<template>
  <div class="flex items-center justify-center py-12">
    <div class="flex flex-col items-center gap-4">
      <div class="relative w-10 h-10">
        <div class="w-10 h-10 rounded-full border-2 border-primary-500/20 border-t-primary-500 animate-spin"></div>
      </div>
      <p v-if="text" class="text-sm text-gray-500">{{ text }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({ text: { type: String, default: 'Loading...' } })
</script>
