# API rules

- Local FastAPI only; bind to 127.0.0.1. Paths/ports come from CANDLE_ settings.
- The model tag comes from local settings, never a hardcoded runtime tag.
- Version every prompt under api/prompts/; bundle prompts and content with PyInstaller.
- The owner approved authored reply selection after the free-prose spikes failed.
  Runtime AI classifies relevance and chooses IDs; emit only state-scoped authored text.
  Reject extra fields/prose or unavailable IDs; retry once, then use an authored fallback.
- Never expose unvalidated tokens while streaming. Benchmark the accepted-text boundary.
- Model output classifies relevance and voices the spirit. Code owns state and endings.
- One inference request at a time. Timeouts/errors preserve a playable fallback path.
- Prepare the consented model before enabling dialogue; keep it resident during play.
  Show preparation separately, allow authored fallback mode, and unload on close.
- No cloud models, no remote inference URLs, no keys, no logging of player dialogue.
- Cross-platform paths use pathlib; process inspection uses psutil, never POSIX-only calls.
- Tests use scripted local fixtures; real-model tests are opt-in integration tests.
- Update api/openapi.json with `node scripts/export-openapi.mjs` when contracts change.
- From api/: `uv run ruff check .`, `uv run ruff format --check .`,
  `uv run mypy .`, `uv run pytest -q -m "not integration"`.
