import { describe, expect, it } from 'vitest'
import { ending, finishMemory, interact, MAX_TURNS, newGame, objectIds, readSave } from '../app/game/state'

describe('game progression', () => {
  it('recovers each memory once and chooses the all-memory ending at dawn', () => {
    let state = { ...newGame('en'), phase: 'playing' as const }
    for (const id of objectIds) {
      state = finishMemory(interact({ ...state, selected: id }, true)) as typeof state
    }
    while (state.turns < MAX_TURNS) state = interact({ ...state, selected: 'radio' }, true) as typeof state
    expect(state.recovered).toHaveLength(6)
    expect(state.phase).toBe('ending')
    expect(ending(state)).toBe('peace')
  })

  it('chooses the other endings and preserves a final-turn memory scene', () => {
    const state = { ...newGame('es'), phase: 'playing' as const, selected: 'bowl' as const, turns: MAX_TURNS - 1 }
    expect(ending(state)).toBe('lost')
    const last = interact(state, true)
    expect(last.phase).toBe('memory')
    expect(finishMemory(last).phase).toBe('ending')
    expect(ending(last)).toBe('bittersweet')
  })

  it('rejects corrupt, inconsistent and unknown saves', () => {
    const valid = newGame('en')
    expect(readSave(JSON.stringify(valid))).toEqual(valid)
    for (const bad of ['{', JSON.stringify({ ...valid, recovered: ['radio', 'radio'] }), JSON.stringify({ ...valid, selected: 'other' }), JSON.stringify({ ...valid, phase: 'ending' }), JSON.stringify({ ...valid, recovered: ['radio'] })]) {
      expect(readSave(bad)).toBeNull()
    }
  })
})
