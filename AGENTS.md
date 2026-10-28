# La Última Vela / The Last Candle

A bilingual (English/Spanish), offline narrative game about helping a gentle spirit
recover its memories at an ofrenda before dawn. Día de los Muertos is remembrance.
The full product brief, build order and explicit stop points are in docs/PROJECT_BRIEF.md.

## Layout
- api/: FastAPI, Python 3.12, uv, Pydantic; PyInstaller executable.
- web/: Nuxt SPA, strict TypeScript, Vue; local save/resume and bilingual UI.
- desktop/: Electron, isolated bundled Ollama, service supervision and cleanup.
- content/: authored bilingual canon, scenes, fallback dialogue and endings.
- assets/: original art, audio and fonts; docs/: decisions, benchmarks and art prompts.

## Commands (repository root)
- Install: `npm ci && npm run setup` (uv and Node must be available).
- Dev: `npm run dev`; separately `npm run dev:api` or `npm run dev:web`.
- Desktop: `npm run dev:desktop` (needs generated web and bundled API/Ollama).
- Checks: `npm run lint`, `npm run typecheck`, `npm test`; all: `npm run check`.
- Static SPA: `npm --prefix web run generate`; shell: `npm --prefix desktop run build`.
- Installer: `npm run dist`; plan: `npm run dist:plan`; resume: `npm run dist -- --from <step>`.
- API contract: `node scripts/export-openapi.mjs` regenerates api/openapi.json.
- CI: checks.yml runs per-package lint/typecheck/tests and SPA generation on PRs;
  build.yml runs the same dist scripts per OS; v* tags create draft releases only.

## GitFlow (one build step, one feature PR; no stacked PRs)
- Production is master only. Never create or target an alternate production branch.
- Never commit directly to master or develop. Bootstrap exception is already complete.
- `git checkout develop && git pull`, then `git checkout -b feature/<name>`.
- Small Conventional Commits; lint + typecheck + tests must pass before every commit.
- Push; `gh pr create --base develop`; wait for checks; `gh pr merge --merge --delete-branch`.
- Only then update develop and start the next step. release/* and hotfix/* target master.
- PR body: what changed, why, validation and whether docs/DECISIONS.md changed.
- Record technical decisions and why in docs/DECISIONS.md; consult official docs when unsure.

## Non-negotiables
- No closed-model APIs or cloud inference at runtime; no API keys anywhere in the project.
- The model only voices the spirit and classifies relevance. Code decides progression/endings.
- Runtime dialogue selects authored reply IDs; reject prose/illegal IDs, retry once, then fallback.
- Fully playable without a working model. Prompts are versioned files in api/prompts/.
- Respect remembrance: no monsters, costume treatment or sensationalized death.
- Original illustrated art only; no film/game/brand imitation, real likenesses or image text.
- Use built-in image generation during development only; log prompts and asset licenses.
- Code/comments/commits/PRs/docs in English; player content in English and Spanish.
- Ask before global installs or changes outside this repository. Never commit personal data.
- Respect explicit stops: Git failure, story approval, failed spike, unavailable imagegen,
  or installer >1.5 GB. Model downloads require the player's consent.

## Gotchas
- Node 24.21.0 is pinned locally and in CI; system Node 24.13.0 is too old for Nuxt.
- `nuxt prepare` must run before web ESLint/typecheck; npm installation does it.
- Generated web/dist is a symlink: ignore `dist`, not only `dist/`.
- Desktop uses dynamic loopback ports, its own models/data, and only bundled Ollama.
- Whole game <=4 GB; Ollama/model <=3 GB; one request at a time; unload on quit.
- Desktop process tests need loopback sockets/process inspection; CI never runs inference.
- Challenge dates disagree with the brief; see DECISIONS.md before scheduling submission.
