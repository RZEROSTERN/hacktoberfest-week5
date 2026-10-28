// Copy checked-in assets into Nuxt's generated public directory for offline use.
import { copyFile, mkdir, readFile } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const assets = path.join(root, 'assets')
const output = path.join(root, 'web', 'public')
const manifest = JSON.parse(await readFile(path.join(assets, 'manifest.json'), 'utf8'))
const names = {
  art: manifest.images.map(item => item.filename),
  fonts: ['AtkinsonHyperlegible-Regular.ttf', 'AtkinsonHyperlegible-Bold.ttf', 'CormorantGaramond-Variable.ttf'],
  licenses: ['AtkinsonHyperlegible-OFL.txt', 'CormorantGaramond-OFL.txt', 'Qwen3.5-Apache-2.0.txt'],
}
for (const [directory, files] of Object.entries(names)) {
  await mkdir(path.join(output, directory), { recursive: true })
  for (const filename of files) {
    if (path.basename(filename) !== filename) throw new Error('Unsafe asset filename')
    await copyFile(path.join(assets, directory, filename), path.join(output, directory, filename))
  }
}
console.log(`Copied ${names.art.length} illustrations and local fonts for the offline SPA.`)
