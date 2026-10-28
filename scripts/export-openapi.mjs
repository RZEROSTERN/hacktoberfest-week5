import fs from 'node:fs'
import path from 'node:path'
import { capture, root } from './lib.mjs'

const code = `import json
from app.config import Settings
from app.main import create_app
s = Settings(port=8765, data_dir='.dev', ollama_url='http://127.0.0.1:11500')
print(json.dumps(create_app(s).openapi(), indent=2))`
const result = capture('uv', ['run', '--frozen', 'python', '-c', code], {
  cwd: path.join(root, 'api'), env: { ...process.env, UV_CACHE_DIR: path.join(root, '.dev', 'uv-cache') },
})
if (result.status !== 0) throw new Error(result.stderr)
fs.writeFileSync(path.join(root, 'api', 'openapi.json'), result.stdout)
