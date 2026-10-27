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

## 2026-10-27 — Story approved

The owner approved the full bilingual draft in this session and authorized
continuing development. canon.json now records approved status; the story
text is unchanged. The story PR can proceed before the model-spike branch.

## 2026-10-27 — Local model spike methodology

- **One combined structured response.** The model returns relevance, a short
  spirit reply and visible fact IDs in one request. This avoids two sequential
  inference passes while keeping progression in deterministic code. A fact ID
  is not proof that the accompanying prose is supported.
- **Restrict the schema to visible facts.** Calibration found the model could
  write valid JSON with invented fact IDs. Constraining the schema's ID enum
  fixes that structural problem; it does not solve semantic hallucinations.
  The interrupted calibration evidence is preserved separately from the final run.
- **Fixed, bilingual cases.** Each of six objects has eight relevant, six
  irrelevant and six adversarial messages, with ten cases per language. Expected
  labels precede inference. Locked and recovered contexts are both exercised.
- **Measure the player-safe boundary too.** Raw first fragments often contain
  JSON syntax. The prototype buffers text until validation, retries once, then
  falls back. Both raw timing and complete validated-display latency are recorded.
- **Charge the model's full process tree.** Reuse Slothshot's sampler concept but
  scope it to the owned engine PID and descendants, avoiding a system engine.
  On macOS, sample physical footprint with proc_pid_rusage/rusage_info_v2 as
  defined in Apple's installed SDK. RSS and Ollama's own reported allocation
  substantially understated this run's memory cost. Keep all metrics separately.
- **Reuse weights without touching the source.** Existing manifests and blobs
  were copied into .dev/spike-models and every copied blob checked by SHA-256.
  The bundled engine gets its own home, ports, low priority and process cleanup.
  A rerun on another computer needs explicit --allow-download consent for missing
  weights. No model download or inference is performed in CI.
- **Audit semantics separately.** The final rule prototype catches 40 injected
  bilingual contradictions and preserves 12 authored controls, but raw-output
  review also checks unsupported history, premature revelations, and false
  rejections. A finite passing mutation suite cannot certify arbitrary prose.
- **No inference endpoint yet.** The spike adds a reusable loopback-only client
  and an unshipped validation prototype. It changes no public API contract.
  A simulated service cannot establish real model latency, memory or quality;
  the benchmark deliberately uses the real bundled local engine instead.

### Spike outcome — stop before the PR

Both models completed the same 120-case corpus. E2B classified 116/120 correctly
(96.7%); E4B classified 120/120 (100%). Their peak engine-tree macOS physical
footprints were 5.98 GB and 9.63 GB, respectively, versus a 3 GB engine ceiling
and a 4 GB whole-game ceiling. RSS alone (2.99 GB and 4.88 GB) would misrepresent
the resource cost, especially for E2B.

The finite validator mutation set passes 40/40, with zero false rejections among
12 authored controls. Reviewing all 242 generated candidates nevertheless found
unsupported or premature history and indirect attribution of a canonical event
to the player. It also exposed a Spanish false positive: era un momento/gesto
was mistaken for an occupation. This prototype cannot be called canon-safe.

No default is selected, no model-spike PR is opened, and no art/game-core step
is started. The owner must choose how to address the failed targets. The
recommended option keeps the resource budget and compares smaller local models;
a text-only Gemma 4 variant or revised requirements are alternatives, not
assumptions. Complete timings, raw evidence, audit limitations and reproducible
commands are in docs/BENCHMARKS.md and spike/README.md.

## 2026-10-27 — Approved smaller-model follow-up

The owner approved comparing Gemma 3 1B and Qwen 3.5 0.8B while keeping the
original memory, latency, classification and canon requirements. Downloads went
only to the repository's isolated .dev/spike-models store with explicit consent.
No global install, cloud inference, system engine or runtime default was added.

- **Split classification from voice for the smaller models.** The combined-call
  pilot confused relevance with the spirit's forgotten knowledge. A dedicated
  classifier improved the decision task. Its time counts toward every voice
  latency metric; the voice's redundant boolean cannot replace its decision.
- **Use capability-aware thinking controls.** Omit think for text-only Gemma 3;
  disable it for Qwen where supported. The runner records capabilities/options,
  the model digest and measured source hashes for reproduction.
- **Preserve calibration and unchanged labels.** The first 20-case split pilot
  scored 45% / 75%; a clearer JSON contract, quoted player data and generic
  examples on different objects improved the next pilot to 90% / 85%. Both
  pilots remain in spike/results. Because those cases also occur in the full
  corpus, this is a development result, not independent holdout accuracy.
- **Turn original escapes into regressions, without claiming complete safety.**
  The expanded validator set catches 48/48 false statements and rejects none of
  16 valid controls. It adds known shared-history/premature-memory failures and
  fixes the Spanish era un momento/gesto false positive. Conservative free-text
  checks still overreject supported references and miss indirect false claims.
- **Keep historical evidence intact.** Original Gemma 4 measurements and audit
  retain their source hashes and revision 3858576. Their report now lives in
  docs/BENCHMARKS_GEMMA4.md; docs/BENCHMARKS.md presents the follow-up. Each
  report has its own generator. This run freezes the v2 voice/v3 classifier.

### Follow-up outcome — stop before the PR again

Both models completed all 120 unchanged cases. Gemma 3 scored 103/120 (85.8%)
with conservative peak engine memory 1.294 GB; Qwen scored 105/120 (87.5%) at
2.119 GB. Warm raw voice TTFT p95 was 1.01 / 1.86 s and raw full reply p95
2.48 / 2.34 s. Safe display p95 was 3.39 / 2.48 s; Qwen's cold TTFT was 3.46 s
and its warm worst-case raw TTFT/full/safe delay was 5.91 / 6.44 / 7.64 s.
These tails are reported rather than silently redefining the targets as means.

Codex reviewed all 283 raw candidates (not an independent human verification).
The qualitative audit flags 48 / 40 canon issues, including unsupported fixed
object/scene details: 29 / 22 were blocked, leaving 19 / 18 escapes. Gemma 3
substitutes Berta for Aurelio's radio lesson and invents new life habits. Qwen
denies recovered identity and invents a favorite football team. Both also break
character, and conservative rules falsely reject some supported family wording.
This clearly fails the canon requirement despite passing the finite mutation set.

No default, spike PR or subsequent feature branch is created. The recommended
next option is local AI classification plus selection from authored, state-scoped
reply IDs, with code resolving all displayed text. That preserves free player
input and local semantic interpretation, but changes open-ended voice generation
and therefore needs owner approval. The alternative is another text-only model/
backend spike with stronger validation; no new model is assumed to qualify.
