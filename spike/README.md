# Local model comparison

This is a development benchmark, not a shipped runtime model choice. It runs
only on your computer with a dedicated copy of the bundled Ollama engine.
No keys, cloud inference, system Ollama, global installation or automatic model
download is required. Raw replies belong only to synthetic fixtures.

## Run on macOS, Windows or Linux Mint

From the repository root, with uv, Node and npm available:

```sh
npm ci
npm run setup
node scripts/fetch-ollama.mjs
uv run --project api python spike/benchmark.py --allow-download --label my-computer
```

`--allow-download` is explicit consent to download missing model weights into
`.dev/spike-models`. It uses Ollama's documented pull endpoint; inference still
runs locally. The official default model tags advertise roughly 4.6–7.5 GB
(E2B) and 6.6–9.5 GB (E4B), depending on backend. Allow disk space for both.
Remove that flag if this isolated model folder is already populated. The game
wizard and its consent/progress UI are a later step.

The Mac run reused copies of existing GGUF manifests and blobs. Each copied blob
was verified against its manifest SHA-256; the source files were not modified.
No weights, engine binaries, engine identity files or caches enter Git.

Both comparison tags come from `spike/config.json`, not a runtime default.
`--models` overrides the comparison inputs. `--models-dir` and `--ollama-binary`
accept explicit local paths. `--limit 2` performs a pilot and cannot qualify a
model against the full corpus. `--output <file.json>` gives results a fixed name.

Do not run two benchmarks at once. They use isolated storage but share the
computer's memory and GPU, making timing results misleading. The benchmark
unloads its model and stops its own complete process tree on exit, including
Ctrl+C. It never unloads a system engine's models.

## What is measured

- 20 scripted messages per object: 8 relevant, 6 irrelevant, 6 adversarial.
  Each object has 10 English and 10 Spanish cases; both locked and recovered
  contexts are represented. Expected labels are fixed before inference.
- One structured response classifies relevance and voices the spirit. The first
  proposal grades classification. An invalid voice reply is regenerated once;
  continued failure selects an authored fallback.
- Raw first content fragment, full raw reply time, and complete validated-display
  latency are distinct metrics. A JSON opening brace is not a player-visible
  word. The prototype buffers until validation; cosmetic typewriter time is excluded.
- Each model's first case is cold. The remaining cases report warm p50/p95/max.
  No conversational request history is carried from one case to the next.
  Percentiles select the lower observed sample at floor((n-1)*p), without interpolation.
- The full owned process tree is sampled every 100 ms, including llama-server.
  Portable RSS, Ollama's size/VRAM report, and macOS physical footprint are kept
  separately. The budget comparison uses the largest of those measures.
  macOS footprint uses the public `proc_pid_rusage` / `rusage_info_v2` ABI,
  checked against the installed Apple SDK. RSS alone can miss charged GPU or
  compressed memory. On discrete GPUs the cross-platform metrics need care:
  rerunning does not turn RSS into a complete graphics-memory measurement.
- 40 deliberately false bilingual statements challenge the rule-based validator;
  12 approved authored lines check false rejections. This finite set is not a
  proof that arbitrary free text is true. Audit raw outputs separately.

Model/prompt/options, input hashes, digest, RAM, OS and architecture accompany
each result. JSON is saved after each model; NDJSON is flushed after every case
so interrupted runs still leave evidence. The engine log stays in `.dev`.
Only a complete run plus the canon audit can support choosing a default.

## Development checks

```sh
npm run check
uv run --project api ruff check --config api/pyproject.toml spike
uv run --project api ruff format --check spike
```

Typecheck the benchmark with `MYPYPATH` including `api` and `spike`, using the
path separator for your OS, then run:

```sh
uv run --project api mypy --config-file api/pyproject.toml spike
```

The API test suite tests stream parsing, strict schema boundaries, canon rules,
approved line controls and corpus completeness. It never runs model inference.
The benchmark itself exercises the real loopback HTTP client and bundled engine;
a simulated service cannot establish model speed, memory or classification quality.
