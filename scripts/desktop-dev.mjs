import path from 'node:path'
import { root, run } from './lib.mjs'

const env = { ...process.env }
delete env.ELECTRON_RUN_AS_NODE
run(process.platform === 'win32' ? 'npm.cmd' : 'npm', ['run', 'build'], {
  cwd: path.join(root, 'desktop'), env, shell: process.platform === 'win32',
})
run(path.join(root, 'desktop', 'node_modules', '.bin', process.platform === 'win32' ? 'electron.cmd' : 'electron'),
  ['.', `--user-data-dir=${path.join(root, '.dev', 'desktop-data')}`], {
    cwd: path.join(root, 'desktop'), env, shell: process.platform === 'win32',
  })
