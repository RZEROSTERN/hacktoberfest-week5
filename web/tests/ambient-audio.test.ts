import { afterEach, describe, expect, it, vi } from 'vitest'
import { AmbientAudio } from '../app/utils/ambient-audio'

function audioContext(resumeGate?: Promise<void>) {
  let state: AudioContextState = 'suspended'
  const gain = () => ({
    value: 0,
    setValueAtTime: vi.fn(),
    linearRampToValueAtTime: vi.fn(),
    exponentialRampToValueAtTime: vi.fn(),
  })
  const node = () => ({ connect: vi.fn().mockReturnThis(), disconnect: vi.fn() })
  const gains: ReturnType<typeof gain>[] = []
  const context = {
    get state() { return state },
    sampleRate: 8000,
    currentTime: 0,
    destination: node(),
    resume: vi.fn(async () => {
      if (resumeGate) await resumeGate
      state = 'running'
    }),
    close: vi.fn(async () => { state = 'closed' }),
    createBuffer: vi.fn((_channels: number, length: number) => ({
      getChannelData: () => new Float32Array(length),
    })),
    createBufferSource: vi.fn(() => ({ ...node(), buffer: null, loop: false, start: vi.fn() })),
    createBiquadFilter: vi.fn(() => ({ ...node(), type: '', frequency: gain() })),
    createGain: vi.fn(() => {
      const parameter = gain()
      gains.push(parameter)
      return { ...node(), gain: parameter }
    }),
    createOscillator: vi.fn(() => ({
      ...node(), type: '', frequency: gain(), start: vi.fn(), stop: vi.fn(), onended: null,
    })),
  }
  return { context, gains, native: context as unknown as AudioContext }
}

afterEach(() => vi.useRealTimers())

describe('procedural ambience', () => {
  it('starts only on request, shares a startup, clamps volume and closes cleanly', async () => {
    vi.useFakeTimers()
    const fake = audioContext()
    const factory = vi.fn(() => fake.native)
    const audio = new AmbientAudio(factory)
    expect(factory).not.toHaveBeenCalled()
    const first = audio.start()
    expect(audio.start()).toBe(first)
    expect(await first).toBe(true)
    expect(factory).toHaveBeenCalledTimes(1)
    expect(fake.context.createOscillator).toHaveBeenCalledTimes(1)
    vi.advanceTimersByTime(7500)
    expect(fake.context.createOscillator).toHaveBeenCalledTimes(2)
    audio.setVolume(2)
    expect(fake.gains[0]?.value).toBeCloseTo(0.28)
    audio.setVolume(Number.NaN)
    expect(fake.gains[0]?.value).toBe(0)
    await audio.stop()
    expect(fake.context.close).toHaveBeenCalledTimes(1)
    expect(vi.getTimerCount()).toBe(0)
  })

  it('does not start after the player stops during audio initialization', async () => {
    vi.useFakeTimers()
    let release: () => void = () => {}
    const gate = new Promise<void>(resolve => { release = resolve })
    const fake = audioContext(gate)
    const audio = new AmbientAudio(() => fake.native)
    const pending = audio.start()
    await audio.stop()
    release()
    expect(await pending).toBe(false)
    expect(fake.context.createBuffer).not.toHaveBeenCalled()
    expect(vi.getTimerCount()).toBe(0)
  })
})
