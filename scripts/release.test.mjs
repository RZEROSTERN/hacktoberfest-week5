// What a release must get right before anyone downloads it. Run with: node --test scripts/
import assert from 'node:assert/strict'
import { test } from 'node:test'
import { checkTag, checksumLines, findInstallers, readVersions, renderNotes } from './release.mjs'

const ROWS = [
  { system: 'macOS (Apple Silicon, macOS 14 or later)', file: 'LastCandle-1.0.0-arm64.dmg', bytes: 302_700_000 },
  { system: 'Windows 11 (x64)', file: 'LastCandle-1.0.0-x64-setup.exe', bytes: 165_000_000 },
  { system: 'Linux, any distribution with FUSE 2 (x64)', file: 'LastCandle-1.0.0-x86_64.AppImage', bytes: 204_100_000 },
  { system: 'Linux Mint, Ubuntu and Debian (x64)', file: 'last-candle_1.0.0_amd64.deb', bytes: 165_100_000 },
]

test('a tag has to match the versions the installers will carry', () => {
  assert.deepEqual(checkTag('v1.0.0', '1.0.0', '1.0.0'), [])
  assert.equal(checkTag('v1.0.0', '0.1.0', '1.0.0').length, 1)
  assert.equal(checkTag('v1.0.0', '1.0.0', '0.1.0').length, 1)
  assert.equal(checkTag('v1.0.0', '0.1.0', '0.1.0').length, 2)
  assert.match(checkTag('1.0.0', '1.0.0', '1.0.0')[0], /not a version tag/)
  assert.match(checkTag('vlatest', '1.0.0', '1.0.0')[0], /not a version tag/)
})

test('a pre-release tag is matched in full', () => {
  assert.deepEqual(checkTag('v1.0.0-rc.1', '1.0.0-rc.1', '1.0.0-rc.1'), [])
  assert.equal(checkTag('v1.0.0-rc.1', '1.0.0', '1.0.0').length, 2)
})

test('the repository versions agree with each other', () => {
  // The two the tag is checked against; a release stops if they ever drift.
  const { desktop, api } = readVersions()
  assert.equal(desktop, api, `desktop/package.json is ${desktop} but api/pyproject.toml is ${api}`)
})

test('a release is refused unless all four installers are there', () => {
  const names = ROWS.map(r => r.file)
  assert.equal(findInstallers(names).length, 4)
  assert.equal(findInstallers([...names, 'LastCandle-1.0.0-arm64.dmg.sha256']).length, 4)
  assert.throws(() => findInstallers(names.slice(1)), /macOS/)
  assert.throws(() => findInstallers(names.slice(0, 2)), /Linux/)
})

test('SHA256SUMS is in the format the standard tools read', () => {
  const lines = checksumLines([
    { file: 'b.dmg', sha: 'b'.repeat(64) },
    { file: 'a.exe', sha: 'a'.repeat(64) },
  ])
  assert.equal(lines, `${'a'.repeat(64)}  a.exe\n${'b'.repeat(64)}  b.dmg\n`)
})

test('release notes describe the game and require consent before model downloads', () => {
  const notes = renderNotes({ version: '1.0.0', rows: ROWS })
  assert.match(notes, /remembrance/)
  assert.match(notes, /unsigned/)
  assert.match(notes, /consent/)
  assert.match(notes, /draft/)
  for (const row of ROWS) assert.ok(notes.includes(row.file))
})
