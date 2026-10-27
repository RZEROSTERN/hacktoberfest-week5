import { describe, expect, it, vi } from 'vitest'
import { killTree, sameProgram, spawnOptions } from '../src/processes'

describe('spawnOptions', () => {
  it('leads its own process group everywhere but Windows', () => {
    expect(spawnOptions('darwin').detached).toBe(true)
    expect(spawnOptions('linux').detached).toBe(true)
    // `detached` on Windows would open a console window instead of making a group.
    expect(spawnOptions('win32').detached).toBe(false)
  })
})

describe('killTree', () => {
  it('ends the whole tree with taskkill on Windows', () => {
    const exec = vi.fn(() => '')
    killTree(42, 'SIGTERM', 'win32', exec)
    expect(exec).toHaveBeenCalledWith('taskkill', ['/PID', '42', '/T', '/F'])
  })

  it('swallows a process that has already gone', () => {
    const exec = vi.fn(() => {
      throw new Error('not found')
    })
    expect(() => killTree(42, 'SIGTERM', 'win32', exec)).not.toThrow()
  })
})

describe('sameProgram', () => {
  it('compares only the file name on Windows', () => {
    expect(sameProgram('ollama.exe', 'C:\\apps\\LastCandle\\ollama.exe', 'win32')).toBe(true)
    expect(sameProgram('other.exe', 'C:\\apps\\LastCandle\\ollama.exe', 'win32')).toBe(false)
  })

  it('matches the full command elsewhere, and refuses an empty reading', () => {
    expect(sameProgram('/apps/LastCandle/ollama serve', '/apps/LastCandle/ollama', 'darwin')).toBe(true)
    expect(sameProgram(null, '/apps/LastCandle/ollama', 'darwin')).toBe(false)
  })
})
