<!--
  The ClubDash logo mark.

  Single source of truth for the glyph. Before this existed the landing nav,
  auth screen, sidebar and admin header each inlined their own bolt path with
  different geometry and gradients, so the logo changed shape between screens.

  `tone` picks the treatment rather than the colour, so the mark stays on-brand
  on both light and dark surfaces:
    brand  — indigo gradient tile, white glyph (default)
    light  — white tile, indigo glyph (for dark backgrounds)
    plain  — no tile, glyph inherits currentColor
-->
<template>
  <span class="brand-mark" :class="`tone-${tone}`" :style="sizing" aria-hidden="true">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <path stroke-linecap="round" stroke-linejoin="round" d="M13 3L4 14h7v7l9-11h-7V3z" />
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
