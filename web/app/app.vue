<script setup lang="ts">
import en from './locales/en.json'
import es from './locales/es.json'

const language = ref<'en' | 'es'>('en')
const text = computed(() => language.value === 'es' ? es : en)
useHead(() => ({ htmlAttrs: { lang: language.value } }))
</script>

<template>
  <main>
    <div class="candle" aria-hidden="true">🕯</div>
    <p class="eyebrow">{{ text.subtitle }}</p>
    <h1>{{ text.title }}</h1>
    <p>{{ text.description }}</p>
    <label for="language">{{ text.language }}</label>
    <select id="language" v-model="language">
      <option value="en">{{ text.english }}</option>
      <option value="es">{{ text.spanish }}</option>
    </select>
    <p role="status" class="status">{{ text.status }}</p>
  </main>
</template>
