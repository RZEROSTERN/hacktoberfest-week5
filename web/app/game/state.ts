export const objectIds = ['photograph', 'bowl', 'radio', 'screwdriver', 'letter', 'scarf'] as const
export type ObjectId = typeof objectIds[number]
export type Language = 'en' | 'es'
export const MAX_TURNS = 12
export const SAVE_KEY = 'last-candle-save-v1'

export interface GameState {
  version: 1
  language: Language
  turns: number
  recovered: ObjectId[]
  selected: ObjectId | null
  phase: 'opening' | 'playing' | 'memory' | 'ending'
  memory: ObjectId | null
}

export function newGame(language: Language): GameState {
  return { version: 1, language, turns: 0, recovered: [], selected: null, phase: 'opening', memory: null }
}

export function isObjectId(value: unknown): value is ObjectId {
  return typeof value === 'string' && objectIds.some(id => id === value)
}

export function readSave(raw: string | null): GameState | null {
  if (!raw) return null
  try {
    const state: unknown = JSON.parse(raw)
    if (!state || typeof state !== 'object') return null
    const s = state as Record<string, unknown>
    if (s.version !== 1 || (s.language !== 'en' && s.language !== 'es') ||
      !Number.isInteger(s.turns) || typeof s.turns !== 'number' || s.turns < 0 || s.turns > MAX_TURNS ||
      !Array.isArray(s.recovered) || !s.recovered.every(isObjectId) || new Set(s.recovered).size !== s.recovered.length ||
      (s.selected !== null && !isObjectId(s.selected)) ||
      (s.memory !== null && !isObjectId(s.memory)) ||
      !['opening', 'playing', 'memory', 'ending'].includes(String(s.phase)) ||
      s.recovered.length > s.turns ||
      (s.phase === 'opening' && (s.turns !== 0 || s.recovered.length !== 0 || s.selected !== null)) ||
      (s.phase === 'memory' && (!isObjectId(s.memory) || s.memory !== s.selected || !s.recovered.includes(s.memory))) ||
      (s.phase !== 'memory' && s.memory !== null) ||
      (s.phase === 'ending' && s.turns !== MAX_TURNS) ||
      (s.phase === 'playing' && s.turns >= MAX_TURNS)) return null
    return s as unknown as GameState
  } catch { return null }
}

export function interact(state: GameState, relevant: boolean): GameState {
  if (state.phase !== 'playing' || !state.selected || state.turns >= MAX_TURNS) return state
  const turns = state.turns + 1
  const discovered = relevant && !state.recovered.includes(state.selected)
  const recovered = discovered ? [...state.recovered, state.selected] : state.recovered
  return { ...state, turns, recovered, phase: discovered ? 'memory' : turns === MAX_TURNS ? 'ending' : 'playing', memory: discovered ? state.selected : null }
}

export function finishMemory(state: GameState): GameState {
  if (state.phase !== 'memory') return state
  return { ...state, phase: state.turns === MAX_TURNS ? 'ending' : 'playing', memory: null }
}

export function ending(state: GameState): 'peace' | 'bittersweet' | 'lost' {
  return state.recovered.length === objectIds.length ? 'peace' : state.recovered.length ? 'bittersweet' : 'lost'
}
