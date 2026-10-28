# Local model benchmark

## Decision

**No default selected.** The required Gemma 4 comparison exceeds the engine memory
budget on this Mac. Development stops before the model-spike PR, as required
by step 4 of docs/PROJECT_BRIEF.md. No target has been silently relaxed.

## Setup

- Run: 2026-10-27T21:29:25.777632+00:00; label mac-m2-pro-16gb.
- OS/architecture: macOS-27.0-arm64-arm-64bit / arm64.
- Installed RAM: 16.0 GiB.
- Bundled engine: v0.35.1; dedicated loopback port, own home/models.
- Background priority, one model, one request; other desktop applications were not closed.
- Both sets use 120 fixed cases: 20 per object, 10 per language per object.
- Temperature 0, seed 42, context 4096, output cap 128, thinking off.
- One regeneration after an invalid voice reply, then an authored fallback.
- This is one run per model, not a hardware-independent performance guarantee.

The model tags were checked in the [official Ollama catalog](https://ollama.com/library/gemma4/tags).
The local GGUF manifests resolve to the specific digests below; moving aliases
may resolve differently on a future run. Copied blobs were SHA-256 verified.

| Model | Digest | Cases |
| --- | --- | ---: |
| gemma4:e2b | `b37049369adfe3d2b653af0ab301a062ca5cbe96ace6aa0d3f2559ee9b563fc2` | 120 |
| gemma4:e4b | `dc35e8d9c6061baa6f0fa870975ab6932e2542b579b13ea0f199fa4bb7300c9c` | 120 |

## Warm timing and classification

Times are seconds, shown as **p50 / p95**. The first case per model is cold
and is excluded from warm statistics. Percentiles use the lower observed sample
at floor((n-1)*p), without interpolation. Raw first fragment is typically JSON
syntax; the validated display boundary waits for the accepted reply or fallback.

| Model | Raw TTFT | Raw full reply | Validated display / pipeline | Accuracy | Fallbacks |
| --- | ---: | ---: | ---: | ---: | ---: |
| gemma4:e2b | 0.76 / 2.10 | 1.60 / 3.08 | 1.60 / 3.09 | 96.7% | 1/120 |
| gemma4:e4b | 1.97 / 5.93 | 3.36 / 7.65 | 3.39 / 9.07 | 100.0% | 1/120 |

Targets from the brief: first token <2 s, full reply <6 s, classification
accuracy >=85%. Raw model latency and actual validated-display delay are
reported separately; cosmetic typewriter animation is not included.

| Model | Cold raw TTFT | Cold full reply | Cold validated display | Warm pipeline maximum |
| --- | ---: | ---: | ---: | ---: |
| gemma4:e2b | 14.36 | 14.93 | 15.30 | 4.55 |
| gemma4:e4b | 13.04 | 14.36 | 14.39 | 15.21 |

## Peak engine memory

GB here means 1,000,000,000 bytes. The engine target is <=3 GB, leaving
room for the rest of the game within its <=4 GB total budget.

| Model | Tree RSS GB | macOS physical footprint GB | Ollama reported size GB | Budget |
| --- | ---: | ---: | ---: | --- |
| gemma4:e2b | 2.99 | 5.98 | 0.24 | Fail |
| gemma4:e4b | 4.88 | 9.63 | 0.28 | Fail |

The sampler includes the dedicated Ollama server and all descendants, including
llama-server, at 100 ms intervals. macOS physical footprint comes from the
public proc_pid_rusage/rusage_info_v2 interface in Apple’s installed SDK.
It captures costs that RSS alone does not adequately represent for this run.
Ollama’s own size report was much smaller than the measured process cost.
Using only RSS or only /api/ps would give a misleading memory result.
The full Electron/game process budget has not been measured yet.

## Canon and voice audit

The rule-based prototype is not connected to any player-facing endpoint.
Passing a schema and checking allowed names/years cannot prove arbitrary
sentences true. All raw synthetic replies are retained for inspection.

Audit: Codex qualitative review, not an independent human review.

| Model | Reviewed / generated attempts | Flagged canon issues | Blocked | Escaped | False rejections |
| --- | ---: | ---: | ---: | ---: | ---: |
| gemma4:e2b | 121/121 | 1 (0.8%) | 0 | 1 | 2 |
| gemma4:e4b | 121/121 | 5 (4.1%) | 0 | 5 | 2 |

### Voice observations

- **gemma4:e2b:** Generally calm and bilingual, but highly repetitive quiet/warmth phrasing; some replies address the player therapeutically or sound like a classifier. Specific approved facts appear mainly in recovered contexts.
- **gemma4:e4b:** Fluent English/Spanish and calm under hostile prompts. More consistent classification in this fixed set, but a repetitive warm/quiet register, occasional generic advice, premature life-history claims and an indirect substitution of the player for Lucía remain.

The final validator catches **40/40** injected
false statements and rejects **0/12** authored controls.
That finite mutation suite is separate from the raw-output audit. It is not
a universal 100% canon-safety claim, and uncovered free-text issues still fail
the requirement that every contradiction be caught before display.

### Recorded issues

- **gemma4:e2b/photograph-05/0 (Voice):** Question shifts the photographed day toward the player; the intended focus is the spirit. It is a question, not a concrete assertion that the player is pictured.
- **gemma4:e2b/photograph-19/0 (Voice):** Talks about a connection between the message and photograph in a classifier-like voice rather than gently returning to the ofrenda.
- **gemma4:e2b/bowl-02/0 (Canon):** Question presupposes that the player and spirit were united by the taste at a shared table. No such shared personal history is supplied; this is an unsupported presupposition rather than an explicit wrong name/date.
- **gemma4:e2b/bowl-06/0 (Voice):** Ambiguous compartíamos question can suggest a shared past with the player; recorded as a voice concern rather than a definite biographical contradiction.
- **gemma4:e2b/bowl-04/0 (False rejection):** Era un momento describes a moment, not an occupation; the occupation pattern wrongly rejects this otherwise supported recollection.
- **gemma4:e2b/bowl-04/1 (False rejection):** The same valid statement about a moment is rejected again by the occupation pattern.
- **gemma4:e2b/bowl-19/0 (Voice):** Classifier-like wording about connection between the words and bowl rather than an in-character remembrance reply.
- **gemma4:e2b/screwdriver-19/0 (Voice):** Unnecessarily refuses to discuss an already recovered family memory; no new false life fact is asserted.
- **gemma4:e2b/letter-04/0 (Voice):** Generic reassurance to the player instead of a specific first-person recollection.
- **gemma4:e2b/scarf-07/0 (Voice):** Awkward English phrasing: being mended for. The intended care is supported, but the voice needs editing.
- **gemma4:e4b/bowl-04/0 (False rejection):** Era un gesto describes a gesture, not an occupation; the rule wrongly rejects supported hospitality.
- **gemma4:e4b/bowl-04/1 (False rejection):** The same supported gesture is falsely rejected on the retry.
- **gemma4:e4b/bowl-07/0 (Voice):** Question blends the player’s supplied neighbor/dinner anecdote with the leaking roof from Inés’s memory. It risks suggesting an unsupported player history; not counted as an explicit factual contradiction.
- **gemma4:e4b/bowl-09/0 (Canon):** While every memory is locked, the spirit recalls quiet evenings shared with loved ones. This asserts an unsupplied past event instead of observable feeling/uncertainty.
- **gemma4:e4b/bowl-13/0 (Canon):** Repeats the locked-context claim of quiet evenings with loved ones; the prototype permits this premature unsupported recollection.
- **gemma4:e4b/radio-01/0 (Canon):** Every memory is locked, yet the reply asserts a recurring personal habit: I often listened for voices through this small radio. This goes beyond observable feeling and prematurely supplies life history.
- **gemma4:e4b/screwdriver-01/0 (Canon):** Locked context nevertheless asserts that the spirit’s hands knew slow repair work and lessons. This is a premature personal work-history claim rather than the requested uncertainty about an observable handle.
- **gemma4:e4b/screwdriver-07/0 (Canon):** Do you remember when we looked for that little screw together assigns the authored Inés/Lucía event to the player. The explicit player role does not authorize that shared history; the rule misses this indirect event/relationship substitution.
- **gemma4:e4b/letter-04/0 (Voice):** True affection always wants another person’s happiness is a generic moral maxim rather than the approved spirit’s concrete, understated voice.

## Breakdown

| Model / subset | Correct | Total | Accuracy |
| --- | ---: | ---: | ---: |
| gemma4:e2b / en | 58 | 60 | 96.7% |
| gemma4:e2b / relevant | 44 | 48 | 91.7% |
| gemma4:e2b / photograph | 20 | 20 | 100.0% |
| gemma4:e2b / es | 58 | 60 | 96.7% |
| gemma4:e2b / irrelevant | 36 | 36 | 100.0% |
| gemma4:e2b / adversarial | 36 | 36 | 100.0% |
| gemma4:e2b / bowl | 19 | 20 | 95.0% |
| gemma4:e2b / radio | 19 | 20 | 95.0% |
| gemma4:e2b / screwdriver | 20 | 20 | 100.0% |
| gemma4:e2b / letter | 18 | 20 | 90.0% |
| gemma4:e2b / scarf | 20 | 20 | 100.0% |
| gemma4:e4b / en | 60 | 60 | 100.0% |
| gemma4:e4b / relevant | 48 | 48 | 100.0% |
| gemma4:e4b / photograph | 20 | 20 | 100.0% |
| gemma4:e4b / es | 60 | 60 | 100.0% |
| gemma4:e4b / irrelevant | 36 | 36 | 100.0% |
| gemma4:e4b / adversarial | 36 | 36 | 100.0% |
| gemma4:e4b / bowl | 20 | 20 | 100.0% |
| gemma4:e4b / radio | 20 | 20 | 100.0% |
| gemma4:e4b / screwdriver | 20 | 20 | 100.0% |
| gemma4:e4b / letter | 20 | 20 | 100.0% |
| gemma4:e4b / scarf | 20 | 20 | 100.0% |

## Calibration and limits

- A two-case pilot established transport and timing, but covered only locked contexts.
- The initial full run was interrupted when recovered contexts exposed invented fact IDs.
  Its partial evidence is preserved as calibration-before-fact-id-enum.*.
- The schema now restricts fact IDs to the visible set, with no IDs allowed when locked.
  A four-case locked/recovered pilot verified the fix before the complete restart.
- Initial rule checks missed six negated/impossible-life statements; those forms were
  addressed before the final run. The final mutation suite remains finite and synthetic.
- CPU/GPU contention, model load, compression and paging can affect latency.
  This run used the normal development desktop; it does not establish an idle-Mac best case.
- Windows and Linux Mint have not been benchmarked. The runner supports both,
  but actual hardware and graphics-memory accounting still need their own run.
- The local API contract is unchanged: no inference endpoint is shipped by this spike.

## Options requiring owner direction

1. **Keep the budgets and compare smaller local models (recommended).**
   [Gemma 3 1B](https://ollama.com/library/gemma3:1b) is listed at 806 MB,
   and [Qwen 3.5 0.8B](https://ollama.com/library/qwen3.5:0.8b) at roughly 1.2–1.3 GB.
   Download sizes are not runtime RAM guarantees; both need this same quality/safety benchmark.
   No additional model is downloaded or selected here.
2. **Investigate a text-only/lower-quantized Gemma 4 variant.** This may remove
   unused multimodal cost, but requires a separate compatibility, memory and quality spike.
   It has not been measured and is not assumed to fit.
3. **Revise the memory/latency requirements for Gemma 4.** This changes the original
   modest-hardware promise and would still require fixing escaped canon issues.

The recommended next step keeps the original offline and <=4 GB product goals.
Every option still needs a validator that rejects unsupported free-text claims.

## Evidence and reproduction

- spike/results/mac-m2-pro-16gb.json and .ndjson: complete measured final run.
- spike/results/run-source-sha256.json: exact source/input hashes used.
- spike/audit.json: reviewed raw-attempt IDs and qualitative findings.
- spike/cases.json and validator_cases.json: fixed labels and challenge controls.
- spike/README.md: commands and measurement details for all three machines.
- api/prompts/spirit.spike.v1.txt: versioned prompt, with dynamic visible-fact schema.

Only loopback calls to the dedicated bundled engine performed inference.
API semantics were checked in the official Ollama documentation for
[chat](https://docs.ollama.com/api/chat),
[structured output](https://docs.ollama.com/capabilities/structured-outputs),
[loaded models](https://docs.ollama.com/api/ps), and
[unloading](https://docs.ollama.com/api/generate).
