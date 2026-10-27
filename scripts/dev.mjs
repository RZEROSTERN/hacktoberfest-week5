import { spawn } from 'node:child_process'
import path from 'node:path'
import { root } from './lib.mjs'

const children = []
const env = {
  ...process.env,
  UV_CACHE_DIR: path.join(root, '.dev', 'uv-cache'),
  CANDLE_HOST: '127.0.0.1', CANDLE_PORT: '8765',
  CANDLE_DATA_DIR: path.join(root, '.dev', 'data'),
  CANDLE_OLLAMA_URL: 'http://127.0.0.1:11434',
  CANDLE_CORS_ORIGINS: JSON.stringify(['http://localhost:3000', 'http://127.0.0.1:3000']),
}
function start(file, args, folder) {
  const child = spawn(file, args, { cwd: path.join(root, folder), env, stdio: 'inherit',
    detached: process.platform !== 'win32', shell: process.platform === 'win32' })
  children.push(child)
  child.on('error', () => shutdown(1))
  child.on('exit', code => shutdown(code ?? 1))
}
let stopping = false
function shutdown(code = 0) {
  if (stopping) return
  stopping = true
  for (const child of children) {
    try {
      if (process.platform === 'win32') spawn('taskkill', ['/PID', String(child.pid), '/T', '/F'])
      else process.kill(-child.pid, 'SIGTERM')
    } catch { /* already gone */ }
  }
  process.exitCode = code
}
for (const signal of ['SIGINT', 'SIGTERM']) process.on(signal, () => shutdown())
start('uv', ['run', '--frozen', 'python', '-m', 'app'], 'api')
if (!process.argv.includes('--api-only')) start(process.platform === 'win32' ? 'npm.cmd' : 'npm', ['run', 'dev'], 'web')
