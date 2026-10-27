# Decisions

## 2026-10-27 — Bootstrap and scaffold

- **README-only bootstrap on master.** The repository had no commits. The owner
  explicitly authorized this one-time exception to create a branchable history.
  All subsequent changes use feature PRs into develop, merged one at a time.
- **Copy PostCall and Slothshot infrastructure.** Keep PostCall's supervisor,
  pid recovery and CSP protocol, Slothshot's environment isolation and priority,
  and its cross-platform build scripts. Drop transcription, screenshot sorting,
  SQLite, tray scheduling, notifications and their assets. The game quits when
  its window closes; a hidden scheduler has no purpose here.
- **Fixed stack, current pins.** Nuxt 4.6.3 SPA, Electron 45.1.0 and
  electron-builder 26.18.0 were checked against the npm registry. Python 3.12,
  uv, FastAPI, Pydantic, Ruff, mypy and pytest follow the earlier projects.
  Lockfiles make installation reproducible. Node 24.21.0 is pinned in CI and as a local development dependency because
  the installed Node 24.13.0 is below Nuxt's supported minimum (24.15.0).
  This does not change the system installation.
- **No model selected during scaffolding.** The story must be approved first,
  then the spike decides the default from real measurements. The scaffold never
  loads a model or downloads weights. No previous project's model recommendation
  carries over to this game's different memory budget and latency requirements.
- **Local API contract first.** `/health` reports process readiness. FastAPI's
  OpenAPI snapshot is the contract artifact; a workspace binding and duplicate
  collection would add setup without helping this endpoint. The Python config
  refuses non-loopback inference URLs. No API keys are used.
- **Inherited limits are controls, not measurements.** One loaded model, one
  inference request, 30-second keep-alive, and low-priority child processes are
  preserved. They do not prove the 4 GB budget: measurement remains in the spike.
- **Build once, run the same scripts locally and in CI.** Preserve the macOS
  arm64, Windows x64 and Linux x64 matrix, checksum-pinned Ollama, CPU/Vulkan
  selection, size ceiling, smoke tests and draft releases. Full matrix execution
  and real installer playtests remain step 9, not a scaffold claim.
- **Validate before showing model output.** Streaming will need a canon-safe
  boundary: unvalidated text cannot reach the player. Resolve the latency tradeoff
  during the spike; a typewriter stream of accepted text is the safe baseline.
- **Deadline discrepancy is unresolved.** The owner's brief names Week 5 and
  November 2 at 00:59 Mexico City. DEV event 82 is titled Week 4 for the same
  theme; its `ends_at` is October 31 06:59 UTC, while its full text says October 31
  at 23:59 PDT (November 1 at 00:59 Mexico City). The public page also says
  October 31. Do not silently change the owner's schedule or claim a confirmed
  deadline. Source: https://dev.to/challenges/hacktoberfest-week4-2026-10-26

References checked: Electron security guide, Nuxt deployment guidance,
electron-builder configuration, and existing pinned infrastructure. Community
reports reinforce health-based startup and loopback-only listeners; they are
secondary evidence, not API documentation.

### Scaffold verification

Ruff, strict mypy, ESLint, TypeScript checks, 7 API tests, 2 web tests,
41 desktop tests and 13 build/release tests pass. The generated SPA was viewed
in Chrome. The API builds with PyInstaller and answers health without Ollama
or model weights, including an accented data path. actionlint 1.7.12 validates
the workflows; action inputs were read at their pinned revisions.

The inherited supervisor needed two lifecycle fixes: stop earlier services when
a later startup fails, and cancel startup cleanly when quit arrives during a
health check. Both have real subprocess regression tests. The desktop tests
need loopback sockets and process inspection, so they run outside this agent's
restricted sandbox; they perform no inference.

Remaining verification: bundled Ollama startup, the real Electron shell with its
bundled services, all three installers and hardware budgets belong to later
build steps. Static generation and unit tests do not prove those outcomes.

## 2026-10-27 — Scoped agent instructions

The root AGENTS.md is a short operational guide; api/, web/, desktop/, assets/
and .github/ carry their own rules. The full original build brief remains in
docs/PROJECT_BRIEF.md so shortening instructions cannot erase story approval,
benchmark thresholds, art restrictions or release stops. Commands match the
checked scaffold. No architecture or runtime behavior changes in this step.

## 2026-10-27 — Story draft, awaiting owner approval

- **Inés Robles Vega, a radio repairer.** An original fictional woman with an
  ordinary working life, family, humor and specific habits. Her hometown is
  explicitly fictional; the story does not stand in for every Mexican household.
  Her peaceful death is background canon, not a horror reveal.
- **Six independently recoverable memories.** Photograph, soup bowl, radio,
  screwdriver, letter and scarf explore belonging, hospitality, listening,
  patience, supporting a child's independence and accepting care. Observations
  and sincere questions can connect; the player must not guess hidden facts.
- **Reveal references are explicit.** Life facts and people identify which
  object reveals them. Partial and no-memory endings use no locked identities.
  Later dialogue must use only facts from recovered memories. The full private
  biography is not permission for a model to spoil it.
- **Authored replies cover every object state.** Each object has unrecovered,
  connected, recovered, unrelated, redirect and error replies in both languages.
  Global lines cover the night's phases, empty messages, resuming and endings.
  Model failure therefore does not require improvising dialogue.
- **Typed content with a complete review artifact.** Pydantic checks both
  languages, unique IDs, life dates, all three endings, fallback presence and
  cross-references. scripts/story-review.mjs renders every line and guardrail
  into docs/STORY_REVIEW.md for human approval. These are structural checks,
  not proof of cultural sensitivity, translation quality or semantic canon
  validation. Those require review and the later spike.
- **Approval is pending.** The story remains on feature/story-canon. No story
  PR opens and no model benchmark begins until the owner approves the full draft.
