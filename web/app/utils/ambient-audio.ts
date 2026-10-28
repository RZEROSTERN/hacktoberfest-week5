/** Procedural night ambience. Call start only from an explicit player gesture. */
export class AmbientAudio {
  private context: AudioContext | null = null
  private starting: Promise<boolean> | null = null
  private master: GainNode | null = null
  private timer: ReturnType<typeof setInterval> | null = null
  private revision = 0
  private volume = 0.5
  private note = 0

  constructor(private readonly createContext: () => AudioContext = () => new AudioContext()) {}

  start(): Promise<boolean> {
    if (this.starting) return this.starting
    if (this.context) return Promise.resolve(true)
    let context: AudioContext
    try {
      context = this.createContext()
    } catch {
      return Promise.resolve(false)
    }
    this.context = context
    const revision = ++this.revision
    const pending = this.begin(context, revision)
    this.starting = pending
    void pending.finally(() => {
      if (this.starting === pending) this.starting = null
    })
    return pending
  }

  private async begin(context: AudioContext, revision: number): Promise<boolean> {
    try {
      if (context.state !== 'running') await context.resume()
      if (revision !== this.revision) return false
      if (context.state !== 'running') {
        await this.stop()
        return false
      }

      const master = context.createGain()
      master.gain.value = this.volume * 0.28
      master.connect(context.destination)
      this.master = master

      // Very quiet filtered noise suggests a night breeze without a sound file.
      const buffer = context.createBuffer(1, context.sampleRate * 2, context.sampleRate)
      const samples = buffer.getChannelData(0)
      const fade = Math.min(512, Math.floor(samples.length / 2))
      for (let i = 0; i < samples.length; i++) {
        const edge = Math.min(1, i / fade, (samples.length - 1 - i) / fade)
        samples[i] = (Math.random() * 2 - 1) * edge
      }
      const breeze = context.createBufferSource()
      breeze.buffer = buffer
      breeze.loop = true
      const filter = context.createBiquadFilter()
      filter.type = 'lowpass'
      filter.frequency.value = 350
      const breezeGain = context.createGain()
      breezeGain.gain.value = 0.035
      breeze.connect(filter).connect(breezeGain).connect(master)
      breeze.start()

      this.playNote(context, master)
      this.timer = setInterval(() => this.playNote(context, master), 7500)
      return true
    } catch {
      if (this.context === context) await this.stop()
      return false
    }
  }

  private playNote(context: AudioContext, master: GainNode): void {
    if (context.state !== 'running') return
    const notes = [220, 261.63, 329.63, 293.66]
    const oscillator = context.createOscillator()
    oscillator.type = 'sine'
    oscillator.frequency.value = notes[this.note % notes.length] ?? 220
    this.note++
    const envelope = context.createGain()
    const now = context.currentTime
    envelope.gain.setValueAtTime(0.0001, now)
    envelope.gain.linearRampToValueAtTime(0.12, now + 0.8)
    envelope.gain.exponentialRampToValueAtTime(0.0001, now + 4)
    oscillator.connect(envelope).connect(master)
    oscillator.onended = () => {
      oscillator.disconnect()
      envelope.disconnect()
    }
    oscillator.start(now)
    oscillator.stop(now + 4.1)
  }

  setVolume(value: number): void {
    this.volume = Number.isFinite(value) ? Math.max(0, Math.min(1, value)) : 0
    if (this.master) this.master.gain.value = this.volume * 0.28
  }

  async stop(): Promise<void> {
    this.revision++
    if (this.timer !== null) clearInterval(this.timer)
    this.timer = null
    this.master = null
    const context = this.context
    this.context = null
    this.starting = null
    if (context && context.state !== 'closed') {
      try {
        await context.close()
      } catch {
        // The browser may already have released the audio device.
      }
    }
  }
}
