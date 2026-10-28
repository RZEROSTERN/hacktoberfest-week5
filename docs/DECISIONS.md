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

## 2026-10-27 — Owner-approved authored reply selection

The owner approved the recommended reply-selection approach (LGTM) and asked to
continue. Runtime now classifies the free player message, then chooses an ID from
two authored replies permitted for the selected object/recovery/relevance state.
No generated prose is displayed. The existing approved content supplies every
line; the biography and scenes are unchanged. Strict whole-response validation
rejects extra fields/prose and unavailable IDs, retries once, then uses an authored
fallback. Historical free-prose clients/validators remain only as spike evidence.

The full comparison uses the original 120 cases and 120 new bilingual cases
written before inference, including partially recovered states. Gemma 3 scores
85.8% / 83.3% on original/new cases; Qwen scores 87.5% / 90.8%. All 480 resolved
outputs replay exactly to their legal authored text. The boundary rejects all
1,152 false-prose injections beside legal IDs, with 96 legal controls accepted.
This is structural output confinement, not perfect semantic classification.

The first bounded run measures cold loading as part of the first interaction:
Qwen needs 3.04 s for safe first text, versus about 0.41 s warmed. It otherwise
meets classification and memory targets (1.86 GB). Gemma fits at 1.07 GB but falls
below accuracy on the new cases. No PR/default is selected from this cold run.

The next orchestration fix is an explicit preparation phase before accepting
player messages: preload the selected local model, keep it resident during this
short game, and unload on close. Startup cost must be reported separately and
its memory charged to the budget. The actual preparation helper will be measured;
game/wizard work must gate input on readiness rather than silently moving the
same cold delay onto the first player message. All interactive targets remain.

### Prepared-play outcome — spike qualifies

The preparation helper uses the documented empty /api/generate preload with
keep_alive=-1; classifier and selector calls also retain the model. The owned
engine is still explicitly unloaded and stopped on close. A 35-second pause
after the first interaction verifies residency beyond the previous 30-second
keep-alive, with the following reply timed normally. Process-tree memory sampling
includes preparation and idle time. Reference: https://docs.ollama.com/faq.

Qwen 3.5 0.8B is the recommended default. Its unchanged classifier scores
105/120 (87.5%) original and 109/120 (90.8%) new cases. All 240 prepared replies
finish safely within 0.55 s, including both inference calls, validation and text
resolution; warm safe-display p95 is 0.45 s. Peak engine memory is 1.85 GB.
Startup preparation takes 2.61 s and is reported separately. No generated prose
escapes the authored boundary, all 1,152 injected-prose cases are blocked and 96
legal controls pass. Both tested models remain loaded across the idle probe and
their owned process trees stop after the run. Gemma 3 remains ineligible because
new-corpus accuracy is 83.3%, below the unchanged 85% threshold.

content/models.json records the tested Qwen digest, size, license, context and
preparation requirement for the later wizard. Runtime must read the player's
local model selection; the catalog is a recommendation, not an implicit download.
Game input must wait for successful preparation or explicitly enter authored
fallback mode. The wizard/readiness UI, whole-game <=4 GB measurement, Windows/
Mint benchmarks and installers remain later build steps. The cold-interaction
baseline is preserved at revision 7d468fe and in BENCHMARKS_BOUNDED_COLD.md.

## 2026-10-27 — Offline art, typography and ambience

The original illustrated assets were generated with the built-in development
image tool using the style and recorded prompts, then visually reviewed and
revised for the approved story and consistent character. The 27 shipped WebP
images occupy 4,877,374 bytes. Transparent cutouts retain alpha; the manifest
records source and export hashes, dimensions and sizes. A contact sheet and a
local layered composition support review. Selected source PNGs remain in the
ignored local development directory; Pillow 13 is used only for export.

Atkinson Hyperlegible and Cormorant Garamond are bundled with their SIL Open
Font Licenses, and the model license is included. The SPA build copies art,
fonts and license texts from the asset directory into its offline output.
Credits identify sources and disclose the development image generation.

Ambient sound uses locally generated Web Audio noise and oscillator tones, with
no audio downloads. The utility starts only on request, supports volume and
cleanup, and is tested for interrupted startup. Its playback controls and
audible integration belong to the later atmosphere step; no listening test is
claimed yet.

## 2026-10-27 — Game progression and local dialogue

The player has twelve conversations before dawn. Code advances one turn for a
submitted interaction, unlocks each memory once and selects one of the three
endings from the recovered count. A memory recovered on the final turn is shown
before the ending. Saves include a version and are checked for known objects,
valid counts, phases and language before they are resumed.

The local API prepares only a player-selected, installed model from local
settings and serializes preparation and inference. It returns only the approved
state-scoped authored line, never raw model tokens; the client reveals that safe
line with a typewriter effect. Inference timeout or failure enters fallback mode.
When AI classification is unavailable, the player explicitly reflects on
whether their thought connects to the object, so a model failure cannot block
memory recovery or any ending. Players can also choose fallback during model
preparation. The later wizard will provide the selection and consent flow.

## 2026-10-27 — Atmosphere and player-controlled sound

Candle glow, drifting petals and smoke are lightweight CSS effects over the
illustrated scene; pointer movement adds a small parallax offset. The spirit's
four authored states become progressively more visible, while a candle and
accessible progress indicator track the remaining conversations. Reduced-motion
preferences disable the animation and pointer offset.

Procedural Web Audio is opt-in from an explicit player gesture, with an off
control and volume slider. The audio context closes when switched off or when
the view is destroyed. A browser check verified the context reaches running and
closed states; actual listening and playtesting remain human checks.

## 2026-10-27 — First-launch model setup

The wizard reads its recommended model and download size from the benchmarked
catalog, shows local memory and disk information, and never starts a download
until the player explicitly chooses it. Players may instead persist fallback
mode and change that choice from the title screen. An already installed model
is reused. The download uses the bundled loopback Ollama engine and reports its
layer progress; insufficient disk and failures leave fallback mode available.

The model is prepared and exercises the same classifier and authored-reply
selection before its tag is saved atomically to local settings. Downloads and
inference share one lock. The process only reads local settings and does not
request an account or credentials. A local HTTP stand-in exercised consent,
download and failure paths; a separate browser check verified the installed
model and actual compatibility path. A separate browser interaction went from
model preparation through relevance classification to a recovered memory. A
fresh network download and other OS hardware still need installer testing.

## 2026-10-27 — Installer smoke checks

The shared local/CI installer pipeline now checks the packaged model catalog,
authored fallback dialogue, representative illustrations and bundled font in
addition to starting Ollama and the API. Its disposable extraction and smoke
directories live under the repository's ignored development directory. The
local macOS arm64 DMG and its packaged services passed these checks; its size
and digest are recorded in BUILD_SIZES.md. The macOS, Windows and Linux CI matrix also passed built and packaged smoke
checks; all four installer sizes and hashes are recorded in BUILD_SIZES.md.
Human installation and playtesting remain separate evidence to collect.

## 2026-10-27 — Player and contributor documentation

The README describes the game's premise without revealing its memories, shows
screenshots and a short gameplay capture, and documents installation, consent,
offline operation, the authored-output boundary, benchmark limitations and the
open-source rationale. It identifies unsigned or non-notarized packages and
links to platform guidance. Captures are from the running local game; playtest
claims remain explicitly pending. Credits and benchmark status now reflect the
implemented sound and setup controls.

## 2026-10-27 — Release candidate and secret checks

Version the desktop app, Python package and local API contract together at
1.0.0; the tag is checked against these versions before the draft release.
The preceding 0.1.0 Git history and extracted application code, authored content
and web assets from the macOS bundle and Windows, deb and AppImage CI packages
were scanned with checksum-verified Gitleaks 8.30.1 with no matches. This is a
pattern-based check, not proof that no secret can exist; repeat it on the final
release candidates and inspect the generated draft assets. Runtime model
weights and user data are not bundled in the installers.
