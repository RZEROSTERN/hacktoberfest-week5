<script setup lang="ts">
import objects from '../../content/objects.json'
import lines from '../../content/lines.json'
import endings from '../../content/endings.json'
import en from './locales/en.json'
import es from './locales/es.json'
import { AmbientAudio } from './utils/ambient-audio'
import { ending, finishMemory, interact, MAX_TURNS, newGame, readSave, SAVE_KEY, type GameState, type Language, type ObjectId } from './game/state'

const language = ref<Language>('en')
const game = ref<GameState | null>(null)
const saved = ref<GameState | null>(null)
const message = ref('')
const reply = ref('')
const reflecting = ref(false)
const showCredits = ref(false)
const audio = new AmbientAudio()
const soundOn = ref(false)
const soundBusy = ref(false)
const soundError = ref(false)
const volume = ref(0.5)
const parallax = ref({ x: 0, y: 0 })
const mode = ref<'preparing' | 'ready' | 'fallback'>('preparing')
const busy = ref(false)
const saveAvailable = ref(true)
const api = useApi()
let session = 0
let typingTimer: ReturnType<typeof setTimeout> | undefined
const text = computed(() => language.value === 'es' ? es : en)
const selected = computed(() => objects.find(item => item.id === game.value?.selected))
const memory = computed(() => objects.find(item => item.id === game.value?.memory))
const currentEnding = computed(() => game.value ? endings.find(item => item.id === ending(game.value!)) : undefined)
const spirit = computed(() => Math.min(4, 1 + Math.floor((game.value?.recovered.length || 0) / 2)))
useHead(() => ({ htmlAttrs: { lang: language.value } }))

onMounted(() => {
  try { saved.value = readSave(localStorage.getItem(SAVE_KEY)) } catch { saved.value = null }
})
watch(game, value => {
  if (!value) return
  try { localStorage.setItem(SAVE_KEY, JSON.stringify(value)); saved.value = value } catch { saveAvailable.value = false }
}, { deep: true })
watch(language, value => { if (game.value) game.value.language = value })
onBeforeUnmount(() => { session++; if (typingTimer) clearTimeout(typingTimer); void audio.stop() })
watch(volume, value => audio.setVolume(value))
async function toggleSound() {
  if (soundBusy.value) return
  soundBusy.value = true
  soundError.value = false
  if (soundOn.value) { await audio.stop(); soundOn.value = false }
  else { soundOn.value = await audio.start(); soundError.value = !soundOn.value }
  soundBusy.value = false
}
function moveScene(event: PointerEvent) {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
  const rect = (event.currentTarget as HTMLElement).getBoundingClientRect()
  parallax.value = { x: (event.clientX - rect.left) / rect.width - 0.5, y: (event.clientY - rect.top) / rect.height - 0.5 }
}
async function prepare() {
  const current = ++session
  mode.value = 'preparing'
  try {
    const result = await api<{ mode: 'ready' | 'fallback' }>('/prepare', { method: 'POST', timeout: 65000 })
    if (current === session) mode.value = result.mode
  } catch { if (current === session) mode.value = 'fallback' }
}
function skipModel() { session++; mode.value = 'fallback' }
function start() { game.value = newGame(language.value); reply.value = ''; reflecting.value = false; void prepare() }
function resume() { if (saved.value) { game.value = { ...saved.value, recovered: [...saved.value.recovered] }; language.value = saved.value.language; reply.value = ''; void prepare() } }
function choose(id: string) { if (game.value) { if (typingTimer) clearTimeout(typingTimer); game.value.selected = id as ObjectId; reply.value = ''; reflecting.value = false; message.value = '' } }
function showReply(line: string) {
  if (typingTimer) clearTimeout(typingTimer)
  reply.value = ''
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { reply.value = line; return }
  let index = 0
  const tick = () => {
    index = Math.min(line.length, index + 3)
    reply.value = line.slice(0, index)
    if (index < line.length) typingTimer = setTimeout(tick, 20)
  }
  tick()
}
async function speak() {
  if (!message.value.trim()) { reply.value = text.value.empty; return }
  if (!game.value || !selected.value || busy.value || mode.value === 'preparing') return
  if (mode.value === 'fallback') { reflecting.value = true; return }
  const current = session
  const state = game.value
  busy.value = true
  try {
    const result = await api<{ relevant: boolean | null, reply: string, fallback_used: boolean }>('/dialogue', {
      method: 'POST', timeout: 8000,
      body: { object_id: state.selected, recovered: state.recovered, language: language.value, message: message.value },
    })
    if (current !== session || game.value !== state) return
    showReply(result.reply)
    if (result.relevant === null) { mode.value = 'fallback'; reflecting.value = true; return }
    game.value = interact(state, result.relevant)
    message.value = ''
  } catch {
    if (current === session) { mode.value = 'fallback'; reflecting.value = true }
  } finally { if (current === session) busy.value = false }
}
function decide(relevant: boolean) {
  if (!game.value || !selected.value) return
  const already = game.value.recovered.includes(game.value.selected!)
  showReply(selected.value.fallbacks[already ? 'recovered' : relevant ? 'connected' : 'unrelated'][language.value])
  game.value = interact(game.value, relevant)
  reflecting.value = false
  message.value = ''
}
function continueMemory() { if (game.value) game.value = finishMemory(game.value) }
function title() { session++; busy.value = false; if (typingTimer) clearTimeout(typingTimer); game.value = null; reflecting.value = false; reply.value = '' }
</script>

<template>
  <main>
    <header class="toolbar">
      <label for="language">{{ text.language }}</label>
      <select id="language" v-model="language" :disabled="busy"><option value="en">{{ text.english }}</option><option value="es">{{ text.spanish }}</option></select>
      <button class="quiet" type="button" :disabled="soundBusy" :aria-pressed="soundOn" @click="toggleSound">{{ soundOn ? text.sound_off : text.sound_on }}</button><label v-if="soundOn" for="volume">{{ text.volume }}</label><input v-if="soundOn" id="volume" v-model.number="volume" type="range" min="0" max="1" step="0.05"><button class="quiet" type="button" @click="showCredits = !showCredits">{{ text.credits }}</button>
    </header>
    <p v-if="soundError" class="notice" role="status">{{ text.sound_error }}</p>
    <div v-if="showCredits" class="notice"><p>{{ text.credits_text }}</p><button type="button" @click="showCredits = false">{{ text.close }}</button></div>
    <section v-if="!game" class="title-screen">
      <div class="title-card"><p class="eyebrow">{{ text.subtitle }}</p><h1>{{ text.title }}</h1><p>{{ text.description }}</p><div class="actions"><button type="button" @click="start">{{ text.start }}</button><button v-if="saved" type="button" class="secondary" @click="resume">{{ text.resume }}</button></div></div>
    </section>
    <section v-else-if="game.phase === 'opening'" class="story-card"><img src="/art/title.webp" alt=""><p>{{ lines.opening[language] }}</p><button type="button" @click="game.phase = 'playing'">{{ text.continue_ }}</button></section>
    <section v-else-if="game.phase === 'memory' && memory" class="story-card"><img :src="`/art/${memory.memory.id}.webp`" alt=""><p v-if="reply" role="status" class="reply">{{ reply }}</p><p class="eyebrow">{{ text.memory }}</p><h1>{{ memory.memory.title[language] }}</h1><p>{{ memory.memory.scene[language] }}</p><button type="button" @click="continueMemory">{{ text.continue_ }}</button></section>
    <section v-else-if="game.phase === 'ending' && currentEnding" class="story-card"><img :src="`/art/ending-${currentEnding.id === 'lost' ? 'forgotten' : currentEnding.id}.webp`" alt=""><p class="eyebrow">{{ text.ending }}</p><h1>{{ currentEnding.title[language] }}</h1><p>{{ currentEnding.scene[language] }}</p><button type="button" @click="title">{{ text.restart }}</button></section>
    <section v-else class="game-layout">
      <div class="scene" :style="{ '--shift-x': `${parallax.x * 5}px`, '--shift-y': `${parallax.y * 5}px` }" @pointermove="moveScene" @pointerleave="parallax = { x: 0, y: 0 }"><img src="/art/ofrenda-wall.webp" alt=""><img src="/art/ofrenda-altar.webp" alt=""><img src="/art/ofrenda-papel.webp" alt=""><img class="spirit" :class="`presence-${spirit}`" :src="`/art/spirit-${spirit}.webp`" alt=""><img src="/art/ofrenda-foreground.webp" alt=""><div class="atmosphere" aria-hidden="true"><span v-for="i in 3" :key="`flame-${i}`" :class="`flame flame-${i}`" /><span v-for="i in 8" :key="`petal-${i}`" class="petal" :style="{ '--petal-index': i }" /><span class="smoke" /></div><button v-for="item in objects" :key="item.id" type="button" :disabled="busy" :class="['scene-object', `object-${item.id}`, { active: game.selected === item.id }]" :aria-label="item.title[language]" :aria-pressed="game.selected === item.id" @click="choose(item.id)"><img :src="`/art/object-${item.id}.webp`" alt=""></button></div>
      <div class="game-panel"><div class="clock"><span>{{ text.clock }}: {{ MAX_TURNS - game.turns }}</span><div class="candle-clock" aria-hidden="true"><div class="candle-clock-body" :style="{ height: `${20 + (MAX_TURNS - game.turns) / MAX_TURNS * 80}%` }" /><span class="candle-clock-flame" :style="{ bottom: `${20 + (MAX_TURNS - game.turns) / MAX_TURNS * 80}%` }" /></div><progress :value="game.turns" :max="MAX_TURNS" /></div><p class="intro">{{ lines[game.turns >= 8 ? 'late' : game.turns >= 4 ? 'middle' : 'early'][language] }}</p><h2>{{ text.choose }}</h2>
        <div class="object-grid"><button v-for="item in objects" :key="item.id" type="button" :disabled="busy" :class="{ active: game.selected === item.id }" :aria-pressed="game.selected === item.id" @click="choose(item.id)"><img :src="`/art/object-${item.id}.webp`" alt=""><span>{{ item.title[language] }}</span><small v-if="game.recovered.includes(item.id as ObjectId)">{{ text.recovered }}</small></button></div>
        <div v-if="selected" class="dialogue"><h2>{{ selected.title[language] }}</h2><p>{{ selected.description[language] }}</p><p class="hint">{{ text.hint }}: {{ selected.hint[language] }}</p><p class="notice" role="status">{{ mode === 'preparing' ? text.preparing : mode === 'ready' ? text.ready : text.fallback }}</p><button v-if="mode === 'preparing'" type="button" class="secondary" @click="skipModel">{{ text.skip_model }}</button><label for="message">{{ text.message }}</label><textarea id="message" v-model="message" maxlength="1000" rows="3" /><button v-if="!reflecting" type="button" :disabled="busy || mode === 'preparing'" @click="speak">{{ busy ? text.loading : text.send }}</button><div v-else class="reflection"><p>{{ text.reflection }}</p><div class="actions"><button type="button" @click="decide(true)">{{ text.connect }}</button><button type="button" class="secondary" @click="decide(false)">{{ text.no_connect }}</button></div></div><p v-if="reply" role="status" class="reply">{{ reply }}</p></div>
        <p class="save-note">{{ saveAvailable ? text.saved : text.unavailable_save }}</p><button type="button" class="quiet" @click="title">{{ text.restart }}</button>
      </div>
    </section>
  </main>
</template>
