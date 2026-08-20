<template>
  <div class="min-w-64">
    <label class="block text-xs text-gray-500 mb-2">Club</label
    ><select :value="modelValue" class="input-field" @change="select">
      <option value="">Select club</option>
      <option v-for="c in clubs" :key="c.id" :value="c.id">{{ c.name }}</option>
    </select>
  </div>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import api from '@/api/axios'
const props = defineProps({ modelValue: [String, Number] })
const emit = defineEmits(['update:modelValue', 'change'])
const clubs = ref([])
async function load() {
  try {
    const r = await api.get('/clubs')
    clubs.value = Array.isArray(r.data) ? r.data : []
    if (!props.modelValue && clubs.value.length === 1) {
      emit('update:modelValue', clubs.value[0].id)
      setTimeout(() => emit('change'), 0)
    }
  } catch (e) {
    console.error(e)
  }
}
function select(e) {
  emit('update:modelValue', e.target.value)
  emit('change')
}
onMounted(load)
</script>
