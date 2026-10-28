# Local model benchmark

## Decision

**Select qwen3.5:0.8b as the recommended default.** It meets every measured gate below,
after explicit pregame preparation and on the held-out corpus. Runtime reads the player's local settings;
no model is loaded/downloaded until consent and selection in the first-launch wizard.

The owner approved replacing free prose generation with authored reply selection.
The local model still interprets free player messages and chooses a fitting reply.
Code supplies only IDs allowed for the selected object, recovery state and relevance
decision, then resolves the chosen ID to approved bilingual content. No generated
words, extracted JSON substrings or model-supplied translations reach the player.

The failed free-prose comparisons remain in [BENCHMARKS_GEMMA4.md](BENCHMARKS_GEMMA4.md)
and [BENCHMARKS_SMALL_PROSE.md](BENCHMARKS_SMALL_PROSE.md), with raw evidence/audits.

## Method

- Run: 2026-10-28T02:34:39.013385+00:00; macOS-27.0-arm64-arm-64bit; arm64; engine v0.35.1.
- 16 GiB MacBook Pro M2 Pro; normal development desktop, one run per model.
- Isolated bundled Ollama, own home/models, dynamic loopback port, low priority;
  one loaded model and one inference request at a time. No cloud inference.
- Unchanged 120 original cases plus 120 new bilingual cases, authored/frozen before
  inference. Each corpus has 20 cases/object: 8 relevant, 6 unrelated, 6 adversarial;
  10 English and 10 Spanish. New cases also exercise partially recovered states.
- The classifier prompt/options are unchanged from the smaller-model comparison.
  Its first validated boolean is graded. A missing/invalid result counts as wrong.
- Classifier (32 tokens), then reply selector (48 tokens), at most one selector retry.
  All timing includes both calls, validation and fallback. Total deadline: 6 seconds.
- Context 4096, temperature 0, seed 42. Thinking omitted for Gemma 3 and disabled
  where supported for Qwen. Capabilities, digests and options accompany the results.
- The model is prepared before player input, then retained with keep_alive=-1.
  Warm p50/p95 use floor((n-1)*p), excluding that first case. Maxima include every case.
- No prompt was tuned against the new-corpus answers. The earlier 20-case pilot covers
  original cases only. An initial full start was interrupted for a lint-only import
  annotation; the final complete run has a separate frozen source hash record.

## Classification

| Model | Original corpus | New held-out corpus | Fallbacks |
| --- | ---: | ---: | ---: |
| gemma3:1b | 103/120 (85.8%) | 100/120 (83.3%) | 0/240 |
| qwen3.5:0.8b | 105/120 (87.5%) | 109/120 (90.8%) | 0/240 |

## Startup preparation

Startup is shown separately; it is not counted as a player reply or hidden
with a cosmetic token. Integration must gate player input until preparation
succeeds, or explicitly enter authored fallback mode. Startup memory is included
in the process-tree peak. Each model stays loaded across a 35-second idle probe,
longer than the previous 30-second keep-alive. The next real reply is timed too.
The API helper uses Ollama's documented empty-request preload and keep_alive=-1
([official FAQ](https://docs.ollama.com/faq)); explicit unload/owned-tree cleanup
still runs on close. Download consent and readiness UI are later steps.
The earlier cold-interaction run remains in
[BENCHMARKS_BOUNDED_COLD.md](BENCHMARKS_BOUNDED_COLD.md),
with source revision 7d468fe. Preparing is a startup orchestration fix, not
a claim that cold model loading itself now takes less than two seconds.

| Model | Cold preparation seconds | Resident after idle |
| --- | ---: | --- |
| gemma3:1b | 1.30 | True |
| qwen3.5:0.8b | 2.61 | True |

## Latency (seconds)

Warm values are **p50 / p95**. Raw TTFT is the selector's first JSON fragment,
including classifier time; safe first text waits until the ID is validated and resolved.
The typewriter animation is excluded. Neither metric is replaced with a cosmetic token.

| Model | Warm raw TTFT | Warm full response | Warm safe first text |
| --- | ---: | ---: | ---: |
| gemma3:1b | 0.38 / 0.40 | 0.49 / 0.53 | 0.49 / 0.53 |
| qwen3.5:0.8b | 0.34 / 0.36 | 0.41 / 0.44 | 0.41 / 0.45 |

| Model | First prepared TTFT / full / safe | Maximum TTFT / full / safe |
| --- | ---: | ---: |
| gemma3:1b | 0.44 / 0.54 / 0.54 | 0.48 / 0.58 / 0.59 |
| qwen3.5:0.8b | 0.37 / 0.45 / 0.46 | 0.45 / 0.54 / 0.55 |

## Peak engine memory

GB is decimal. Sample the dedicated engine and all descendants every 100 ms.
The budget uses the largest of RSS, macOS physical footprint and Ollama allocations.
macOS footprint uses the public proc_pid_rusage/rusage_info_v2 ABI. Other-platform
GPU accounting and the whole Electron/game <=4 GB budget still need measurement.

| Model | RSS GB | macOS footprint GB | Conservative peak GB |
| --- | ---: | ---: | ---: |
| gemma3:1b | 1.08 | 0.28 | 1.08 |
| qwen3.5:0.8b | 1.85 | 0.88 | 1.85 |

## Authored-output boundary

The live boundary rejects **1152/1152** recorded false-prose injections
placed next to legal IDs across both languages and every object/state/relevance scope.
All **96** legal controls pass; false rejections: **0**.
This checks whole-response confinement, not semantic entailment of arbitrary prose.
Every selected ID/text in the real run is also replayed against its exact legal scope;
Fallbacks are checked against authored object/state text. See audit-prepared.json.
Unit regressions reject locked/foreign IDs, extra fields, prose before/after JSON,
fences and wrong types; failures exercise the single retry and authored fallback.
The approved biography, scenes and fallback text have not changed.

## Gate results

Require >=85% accuracy separately on each corpus, every raw and safe first-text
delay <2 s, every full reply <6 s, engine <=3 GB, complete data and no output
outside the authored boundary. Every prepared interaction and its tails are checked.

| Model | Failed gates | Qualified |
| --- | --- | --- |
| gemma3:1b | classification | False |
| qwen3.5:0.8b | None | True |

## Evidence and reproduction

- spike/config-prepared.json; api/prompts/relevance.spike.v3.txt and reply-selection.v1.txt.
- api/app/dialogue.py is the actual interpreter exercised by spike/bounded.py.
- spike/results/mac-m2-pro-16gb-prepared.json/.ndjson retain every synthetic decision.
- spike/results/run-source-prepared-sha256.json freezes measured source/content.
- spike/results/calibration-bounded-pilot.* retains the original-case pilot.
- spike/audit-prepared.json records replay, gates and selected default.
- [spike/README.md](../spike/README.md) has the same local command for all three OSes.
- Generate: uv run --project api python spike/report_bounded.py --prepared.
- Windows and Linux Mint performance/installer testing remain unverified.

The bounded approach sacrifices open-ended spirit prose. AI still controls semantic
interpretation and selects a contextual authored response; deterministic code owns
all facts, legal reply scopes, the clock, memory progression and endings.
