<!--
  The Clubeon logo mark.

  Single source of truth for the glyph. Modern athletic 'C' intertwined with
  an infinite loop and court center point, representing Clubeon's continuous
  member lifecycle and facility flow.

  `tone` picks the treatment rather than the colour, so the mark stays on-brand
  on both light and dark surfaces:
    brand  — indigo gradient tile, white glyph (default)
    light  — white tile, indigo glyph (for dark backgrounds)
    plain  — no tile, glyph inherits currentColor
-->
<template>
  <span class="brand-mark" :class="`tone-${tone}`" :style="sizing" aria-hidden="true">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M19 6.5C17.2 4.9 14.7 4 12 4C7.03 4 3 8.03 3 13C3 17.97 7.03 22 12 22C14.7 22 17.2 21.1 19 19.5" />
      <path d="M16 12C16 9.79 14.21 8 12 8C9.79 8 8 9.79 8 12C8 14.21 9.79 16 12 16C13.8 16 15.3 14.8 15.8 13.2" />
      <circle cx="12" cy="12" r="1.5" fill="currentColor" />
    </svg>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  /** Tile edge length in px. The glyph scales with it. */
  size: { type: Number, default: 40 },
  tone: {
    type: String,
    default: 'brand',
    validator: (v) => ['brand', 'light', 'plain'].includes(v),
  },
})

const sizing = computed(() => ({
  '--mark-size': `${props.size}px`,
  '--mark-radius': `${Math.round(props.size * 0.28)}px`,
  '--glyph-size': `${Math.round(props.size * 0.55)}px`,
}))
</script>

<style scoped>
.brand-mark {
  display: inline-grid;
  place-items: center;
  flex-shrink: 0;
  width: var(--mark-size);
  height: var(--mark-size);
  border-radius: var(--mark-radius);
}
.brand-mark svg {
  width: var(--glyph-size);
  height: var(--glyph-size);
}

.tone-brand {
  background: linear-gradient(135deg, #718fff, #4354d1);
  color: #fff;
  box-shadow: 0 8px 22px rgba(67, 84, 209, 0.28);
  border: 1px solid rgba(255, 255, 255, 0.12);
}
.tone-light {
  background: #fff;
  color: #4354d1;
  box-shadow: 0 8px 22px rgba(15, 23, 42, 0.18);
}
.tone-plain {
  background: none;
  box-shadow: none;
  border: none;
  color: inherit;
}
</style>
