import assert from 'node:assert/strict'
import { createHash } from 'node:crypto'
import { readFile, stat } from 'node:fs/promises'
import path from 'node:path'
import { test } from 'node:test'
import { fileURLToPath } from 'node:url'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')

test('all required illustrations are present, intact WebP files under the art budget', async () => {
  const manifest = JSON.parse(await readFile(path.join(root, 'assets/manifest.json'), 'utf8'))
  const required = [
    'title', 'ofrenda-wall', 'ofrenda-altar', 'ofrenda-papel', 'ofrenda-foreground',
    ...['photograph', 'bowl', 'radio', 'screwdriver', 'letter', 'scarf'].flatMap(name => [`object-${name}`, `memory-${name}`]),
    ...[1, 2, 3, 4].map(index => `spirit-${index}`),
    'ending-peace', 'ending-bittersweet', 'ending-forgotten',
    'ui-papel-frame', 'ui-dialog-border', 'ui-candle',
  ]
  assert.deepEqual(new Set(manifest.images.map(item => item.id)), new Set(required))
  assert.equal(manifest.images.length, required.length)
  let total = 0
  for (const image of manifest.images) {
    assert.equal(image.status, 'exported')
    assert.equal(image.filename, `${image.id}.webp`)
    const data = await readFile(path.join(root, 'assets/art', image.filename))
    assert.equal(data.toString('ascii', 0, 4), 'RIFF')
    assert.equal(data.toString('ascii', 8, 12), 'WEBP')
    if (image.transparent) {
      // VP8X's alpha flag indicates that the cutout retains transparency.
      assert.equal(data.toString('ascii', 12, 16), 'VP8X')
      assert.notEqual(data[20] & 0x10, 0)
    }
    assert.equal(createHash('sha256').update(data).digest('hex'), image.sha256)
    assert.equal(data.length, image.bytes)
    total += data.length
  }
  assert.equal(total, manifest.export_bytes)
  assert.ok(total <= 30_000_000, `Art uses ${total} bytes`)
})

test('the shipped fonts and model have their license texts', async () => {
  for (const filename of ['AtkinsonHyperlegible-OFL.txt', 'CormorantGaramond-OFL.txt', 'Qwen3.5-Apache-2.0.txt']) {
    assert.ok((await stat(path.join(root, 'assets/licenses', filename))).size > 1000)
  }
})
