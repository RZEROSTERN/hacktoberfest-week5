import path from 'node:path'
import { root, run } from './lib.mjs'

process.env.UV_CACHE_DIR = path.join(root, '.dev', 'uv-cache')
process.env.npm_config_cache = path.join(root, '.dev', 'npm-cache')
const npm = process.platform === 'win32' ? 'npm.cmd' : 'npm'
const shell = process.platform === 'win32'
const api = args => run('uv', ['run', '--frozen', ...args], { cwd: path.join(root, 'api') })
const part = (folder, args) => run(npm, args, { cwd: path.join(root, folder), shell })
const tasks = {
  setup() {
    run('uv', ['sync', '--frozen', '--python', '3.12'], { cwd: path.join(root, 'api') })
    for (const folder of ['web', 'desktop']) part(folder, ['ci'])
  },
  lint() {
    api(['ruff', 'check', '.']); api(['ruff', 'format', '--check', '.'])
    for (const folder of ['web', 'desktop']) part(folder, ['run', 'lint'])
  },
  typecheck() {
    api(['mypy', 'app', 'entrypoint.py', 'tests'])
    for (const folder of ['web', 'desktop']) part(folder, ['run', 'typecheck'])
  },
  test() {
    api(['pytest', '-q', '-m', 'not integration'])
    for (const folder of ['web', 'desktop']) part(folder, ['test'])
    run(process.execPath, ['--test', 'scripts/assets.test.mjs', 'scripts/dist.test.mjs', 'scripts/release.test.mjs'], { cwd: root })
  },
  check() { tasks.lint(); tasks.typecheck(); tasks.test() },
}
const name = process.argv[2]
if (!Object.hasOwn(tasks, name)) throw new Error(`Unknown task: ${name}`)
tasks[name]()
