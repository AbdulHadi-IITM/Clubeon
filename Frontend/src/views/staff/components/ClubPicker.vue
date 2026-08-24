<template>
  <div class="min-w-64">
    <label class="block text-xs font-semibold text-slate-500 mb-2" :for="id">Club</label>
    <select :id="id" :value="modelValue" class="field2" @change="select">
      <option v-if="!clubs.length" value="">
        {{ error ? 'Could not load clubs' : 'Loading clubs…' }}
      </option>
      <option v-for="c in clubs" :key="c.id" :value="c.id">{{ c.name }}</option>
    </select>
  </div>
</template>
<script setup>
import { onMounted, ref, useId } from 'vue'
import api from '@/api/axios'

const props = defineProps({ modelValue: [String, Number] })
const emit = defineEmits(['update:modelValue', 'change'])

const id = useId()
const clubs = ref([])
const error = ref('')

async function load() {
  try {
    const r = await api.get('/clubs')
    clubs.value = Array.isArray(r.data) ? r.data : []
    // Select the first club rather than only auto-selecting when exactly one
    // exists. With two or more, staff previously landed on an empty screen
    // with no indication that a club had to be chosen first.
    if (!props.modelValue && clubs.value.length) {
      emit('update:modelValue', clubs.value[0].id)
      setTimeout(() => emit('change'), 0)
    }
  } catch (e) {
    error.value = e?.response?.data?.message || 'Could not load clubs.'
  }
}

function select(e) {
  emit('update:modelValue', e.target.value)
  emit('change')
}

onMounted(load)
</script>
