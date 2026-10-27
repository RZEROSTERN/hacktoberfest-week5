// A complete human-readable view generated from the exact content the game will consume.
import fs from 'node:fs'
import path from 'node:path'
import { root } from './lib.mjs'

const read = file => JSON.parse(fs.readFileSync(path.join(root, 'content', file), 'utf8'))
const canon = read('canon.json')
const objects = read('objects.json')
const endings = read('endings.json')
const lines = read('lines.json')
const output = [
  '# Full story review — La Última Vela / The Last Candle', '',
  `Status: **${canon.review_status}**. Generated from the four JSON files in content/.`, '',
  'This review includes every authored player-facing line, all life facts, reveal rules,',
  'relevance guidance and endings. Story changes belong in the JSON, then regenerate this file.', '',
  'The story PR must wait for owner approval. Structural tests cannot approve fiction.', '',
]
for (const language of ['en', 'es']) {
  const label = language === 'en' ? 'English' : 'Español'
  const text = localized => localized[language]
  output.push(`## ${label}`, '', '### Premise and player', '', text(canon.premise), '', text(canon.player_role), '',
    '### The spirit and fixed biography', '',
    `${canon.spirit.name} · ${canon.spirit.born} — ${canon.spirit.died}`, '',
    `${canon.spirit.home} (fictional town) · ${text(canon.spirit.era)} · ${text(canon.spirit.trade)}`, '',
    text(canon.spirit.personality), '', text(canon.spirit.voice), '')
  for (const person of canon.people) output.push(`- **${person.name}:** ${text(person.relationship)}. Revealed by: ${person.revealed_by.join(', ')}.`)
  output.push('')
  for (const fact of canon.facts) output.push(`- **${fact.id}:** ${text(fact.text)} Revealed by: ${fact.revealed_by.join(', ')}.`)
  output.push('', '### Opening', '', text(lines.opening), '')
  for (const object of objects) {
    output.push(`### ${text(object.title)} (${object.id})`, '', text(object.description), '',
      `**Hint:** ${text(object.hint)}`, '', `**Memory: ${text(object.memory.title)}**`, '',
      text(object.memory.scene), '', `**Accepted connections:** ${text(object.relevance.accept)}`, '',
      `**Rejected connections:** ${text(object.relevance.reject)}`, '', '**Authored replies for every object state:**', '')
    for (const [state, line] of Object.entries(object.fallbacks)) output.push(`- **${state}:** ${text(line)}`)
    output.push('')
  }
  output.push('### Endings', '')
  for (const ending of endings) output.push(`#### ${text(ending.title)} — ${ending.condition}`, '', text(ending.scene), '')
  output.push('### Other game-state lines', '')
  for (const [state, line] of Object.entries(lines)) if (state !== 'opening') output.push(`- **${state}:** ${text(line)}`)
  output.push('')
}
output.push('## Canon and tone guardrails', '')
for (const rule of canon.guardrails) output.push(`- ${rule}`)
output.push('', '## Review notes', '',
  '- Memory order is free. A thoughtful question or observation can connect; no guessing of secret names or dates is required.',
  '- The letter is sent, kept by the son, and later returned; its presence on the ofrenda is intentional.',
  '- Partial and no-memory endings avoid unrecovered names and life facts.',
  '- Birth/death and the cause of death are fixed background facts, not a graphic or tragic reveal.',
  '- No ending makes remembrance a moral score or promises a supernatural consequence.',
  '- The model spike still has to establish classification quality and how canon validation behaves.', '')
fs.writeFileSync(path.join(root, 'docs', 'STORY_REVIEW.md'), `${output.join('\n').trimEnd()}\n`)
console.log('Generated docs/STORY_REVIEW.md from all authored content.')
