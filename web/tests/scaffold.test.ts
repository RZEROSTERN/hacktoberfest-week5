import { describe, expect, it } from 'vitest'
import { resolveApiBase } from '../app/utils/api'
import en from '../app/locales/en.json'
import es from '../app/locales/es.json'

describe('local shell integration', () => {
  it('uses the isolated desktop API port when provided', () => {
    expect(resolveApiBase({ apiBase: 'http://127.0.0.1:54321' }, 'dev')).toBe('http://127.0.0.1:54321')
    expect(resolveApiBase(undefined, 'dev')).toBe('dev')
  })
  it('provides the same labels in both languages', () => {
    expect(Object.keys(es).sort()).toEqual(Object.keys(en).sort())
  })
})
