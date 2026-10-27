# Context

I'm entering the DEV Hacktoberfest Open-Source AI Challenge, Week 5: "Ghost in the
Machine": build something spooky, or something that honors the past in the spirit of
Día de los Muertos, with open-weight models or open-source AI.
The project MUST comply with these rules:
- Open-source AI must be what makes the product work: at runtime, NO closed-model APIs
  and NO cloud inference. Everything runs on the player's own computer.
- Closed tools may be used ONLY during development (you as the coding agent, and image
  generation through my ChatGPT subscription for the art). Nothing in the shipped game
  may call them.
- The repo is created and completed within the challenge window, which closes Monday,
  November 2, 00:59 Mexico City time.
- Internal deadlines: playable on my Mac by Friday night; final art and Windows and Linux
  installers by Saturday night, including a playtest with another person; Sunday is for
  the write-up.

Reuse from my previous projects:
- PostCall at: ../hacktoberfest-week3
- Slothshot at: ../hacktoberfest-week4
Read their CLAUDE.md, .claude/rules/, and docs/DECISIONS.md to learn the architecture,
then reuse and adapt: the Electron shell with bundled Ollama, the first-launch model
wizard, the resource budget and low-priority process handling from Slothshot, and the
GitHub Actions build matrix for macOS, Windows, and Linux. Copy code; do not add those
repos as dependencies.

All architecture decisions below are already made. Build the whole project end to end,
following the build order, without waiting for confirmation between steps unless a step
explicitly says to stop. Time is the main constraint: always choose the simplest solution
that works.

# Git workflow: GitFlow with non-stacked PRs (ESSENTIAL, never skip)

STRICTLY FORBIDDEN: any alternate production branch. The production branch is "master".
Never create, push, reference, or target an alternate production branch in any command, PR, workflow file,
config, or doc.

Branches:
- master: production only. Changes arrive only through release/* or hotfix/* PRs.
- develop: integration branch. Changes arrive only through feature/* PRs.
- feature/<short-name>: one per build step, always created from the latest develop.
- release/<version>: created from develop when the MVP is ready; PR into master, then
  merged back into develop.
- hotfix/<short-name>: from master, only for urgent fixes; PR into master and merged back
  into develop.

Rules:
- Never commit directly to master or develop.
- One feature branch per build step, one PR per feature branch, base branch = develop.
- NO stacked PRs: never create a branch from another feature branch, and never open a PR
  whose base is anything other than develop (or master for release/hotfix).
- Sequence for every step:
  1. git checkout develop && git pull
  2. git checkout -b feature/<name>
  3. Work with small Conventional Commits.
  4. Run lint + typecheck + tests for the parts touched; all must pass.
  5. Push and open the PR with gh pr create --base develop.
  6. Merge it with gh pr merge (merge commit, delete the branch).
  7. Only then start the next step from the updated develop.
- PR description: what changed, why, how it was tested, and whether DECISIONS.md was
  updated. PR title follows Conventional Commits.

# The game: "La Última Vela / The Last Candle" (working title)

A short narrative game (15 to 20 minutes) played at night, in English and Spanish.

Premise: it's the night of November 1. An ofrenda glows with candles and cempasúchil.
A spirit has returned, as tradition says the dead do, but it doesn't remember who it was
in life. The player talks with the spirit and examines the objects on the ofrenda to help
it recover its memories before dawn on November 2, when it must return.

Mechanics:
- One scene: the ofrenda at night, with 5 or 6 interactive objects (e.g., a photograph, a
  favorite dish, a song, a tool of the spirit's trade, a letter, a personal item).
- The player selects an object and writes freely to the spirit about it.
- The local model voices the spirit and classifies whether the player's message connects
  meaningfully to that object's memory. When it does, the memory is recovered: a short
  authored scene plays and the spirit becomes more visible and more itself.
- A dawn clock: each interaction advances the night; candles burn down visibly as it
  approaches.
- Three endings, decided by code: all memories recovered (the spirit leaves at peace,
  having been remembered), some recovered (a bittersweet farewell), none (the spirit
  fades at dawn, still lost).
- Spirit replies stream token by token in a typewriter effect, which also hides latency.

The canon (the story is authored, the AI only gives it a voice):
- The spirit's life is a fixed, bilingual data file: name, era, family, trade, how they
  died, personality and way of speaking, and one memory per object with the authored
  scene for when it's recovered. The model never invents facts about the spirit's life.
- The game logic (unlocking memories, the clock, endings) is deterministic code.
- The model does only two things: speak as the spirit, and classify relevance.
- Every spirit reply is checked against the canon (names, dates, places, relationships);
  if it contradicts it, regenerate once, then use an authored fallback line.
- Authored fallback lines exist for every object and game state, so the game is fully
  playable even if the model is slow or fails.

Tone (non-negotiable):
- Treat Día de los Muertos with respect: it's a celebration of remembrance, not a horror
  theme. The eeriness comes from the atmosphere, the silence, the candlelight, and the
  approaching dawn, never from turning the dead into monsters or using the tradition as
  a costume.
- The spirit is gentle, dignified, and specific: a real person with a real life.
- Player messages that are abusive or try to break the character get an in-character,
  calm reply that steers back to the ofrenda; the canon is never broken.

# Art and assets (Día de los Muertos)

Original art generated during development with the image generation built into Codex,
through my ChatGPT subscription. Do NOT use an API key, the OpenAI Images API, or any
script that calls it. If image generation isn't available in your environment, STOP and
tell me; then write every prompt in docs/ART_PROMPTS.md with its target filename and
size, and I'll generate the images in ChatGPT and drop them into /assets/incoming/ for
you to process.

Style guide (write it first in docs/ART_STYLE.md and follow it for every asset):
- Mexican folk art at night: papel picado, cempasúchil (marigold) petals and garlands,
  candlelight, copal smoke, sugar skulls, pan de muerto, clay and talavera details, and
  calavera imagery in the spirit of José Guadalupe Posada's public-domain engravings.
- Palette: cempasúchil orange, rosa mexicano, deep purple, night blue, candle gold, and
  bone white. Warm light against dark.
- One consistent illustrated style across all assets.
- STRICTLY FORBIDDEN: imitating or referencing the film "Coco" or any other film, game,
  or brand; copying any existing artwork other than public-domain works; real people's
  likenesses; and any text inside generated images (all text is rendered by the game).

Asset list:
- Title screen illustration.
- The ofrenda scene as layered backgrounds (back wall, altar tiers, papel picado,
  foreground flowers and candles) for a subtle parallax effect.
- One illustration per object.
- The spirit in 4 states, from barely visible to fully present.
- A short illustrated image for each recovered-memory scene.
- One image per ending.
- UI elements: papel picado frames and dialog borders, candle icons for the dawn clock.

Done in code instead of generated images: candle flicker, drifting marigold petals,
smoke, and the spirit's translucency (CSS or canvas).

Sound: ambient night sound and soft music only from CC0 or similarly permissive sources,
or generated procedurally with the Web Audio API. Every external asset's source and
license goes in CREDITS.md.

Fonts: open-licensed fonts only (e.g., from Google Fonts), with their licenses included.

Keep every image generation prompt in docs/ART_PROMPTS.md so the art can be reproduced.
Optimize all images for size (WebP), and keep the total art under 30 MB.

# Architecture

Same stack as my previous projects:

/api      FastAPI (Python 3.12+, uv, Pydantic, pytest, ruff), packaged with PyInstaller:
          dialogue orchestration (spirit prompt built from the canon, relevance
          classification, canon validation, fallbacks), model management endpoints for
          the wizard. Model tag read from local settings, never hardcoded. Prompts in
          versioned files under api/prompts/.
/web      Nuxt (latest stable, TypeScript strict) in SPA mode, Vue: title screen,
          language selection, the ofrenda scene, dialogue, memory scenes, dawn clock,
          endings, settings, credits. Game state in a store; save and resume a game
          locally.
/content  The canon (bilingual JSON), authored scenes, fallback lines, and ending texts.
/assets   Generated art, audio, and fonts.
/desktop  Electron shell adapted from my previous projects, with bundled Ollama, the
          first-launch model wizard (recommended small models only), low process priority,
          and process-tree cleanup on quit.
/docs     DECISIONS.md, BENCHMARKS.md, ART_STYLE.md, ART_PROMPTS.md.
.github/workflows/  Build matrix for macOS arm64 (.dmg), Windows x64 (NSIS .exe), and
          Linux x64 (AppImage + .deb): artifacts on PRs from release/* into master, and a
          DRAFT GitHub Release with SHA256SUMS on v* tags.
Root:     README.md, AGENTS.md, CREDITS.md, cross-platform "npm run dist", .env.example,
          .gitignore.

Resource budget (from Slothshot): peak memory of the whole game at most 4 GB on a 16 GB
machine; a small model (Gemma 4 E2B or E4B, chosen in the spike); one request at a time;
the model unloaded when the game closes.

My machines:
- MacBook Pro M2 Pro, 16 GB, macOS: development.
- PC with Ryzen 9, Windows 11: installer testing.
- Intel MacBook running Linux Mint, no dedicated GPU: installer testing and the reference
  for modest hardware.

# Build order (each step = one feature branch + one PR into develop)

0. Git setup: verify the GitHub remote and that gh is authenticated, and confirm that
   master exists and is the default branch on GitHub. If any of these fails, STOP and
   tell me. Create develop from master and push it.

1. feature/scaffold: /api, /web, /desktop, and the CI workflow adapted from my previous
   projects and stripped of their specific features. docs/DECISIONS.md.

2. feature/agents-md: project instructions for Codex, short, with only what can't be
   inferred from the code:
   a. AGENTS.md at the root (committed, under ~60 lines): overview and layout; exact
      commands (install, dev, test, lint, typecheck, dist, CI); GitFlow rules condensed;
      workflow (lint + typecheck + tests before each commit, Conventional Commits,
      DECISIONS.md updates, check official docs instead of guessing); non-negotiables:
      never use any alternate production branch (production is "master"), no closed AI at runtime,
      no API keys anywhere in the project, the canon is never contradicted, the tone
      rules, the art restrictions; and a Gotchas section.
   b. Nested AGENTS.md files with rules scoped to their folder: api/ (canon validation,
      fallbacks, prompts in api/prompts/, one request at a time), web/ (SPA only, all text
      from /content or i18n files, never inside images, accessible contrast and font
      sizes), desktop/ (security settings, bundled Ollama only, low priority, cleanup),
      .github/ (pinned actions, minimal permissions, draft-only releases, production is master only),
      and assets/ (follow docs/ART_STYLE.md, log every prompt, licenses in CREDITS.md).

3. feature/story-canon: write the spirit's canon, the authored memory scenes, the
   fallback lines, and the three endings in /content, in English and Spanish. The spirit
   must be an original, specific, dignified person. STOP before opening the PR and show
   me the full story for approval; I may rewrite parts of it.

4. feature/model-spike: compare Gemma 4 E2B and Gemma 4 E4B (check exact tags in the
   Ollama docs) on voicing the spirit and on relevance classification, using 20 scripted
   player messages per object (relevant, irrelevant, and adversarial). Record in
   docs/BENCHMARKS.md: time to first token, full reply time, peak memory, classification
   accuracy, and how often replies contradict the canon. Leave a script so I can run the
   same benchmark on my Mint and Windows machines.
   Targets on my Mac: first token under 2 s, full reply under 6 s, peak memory of Ollama
   + model at most 3 GB, at least 85% classification accuracy, and canon contradictions
   caught by validation in 100% of cases.
   If no model meets them, STOP before opening the PR and show me the results with
   options. Otherwise, pick the default and continue.

5. feature/art-style-and-assets: docs/ART_STYLE.md, then generate every asset in the list
   with your built-in image generation following it (or, if unavailable, process the
   images I drop into /assets/incoming/), log every prompt in docs/ART_PROMPTS.md,
   optimize to WebP, and add audio and fonts with CREDITS.md. Show me a contact sheet of
   all the art in the PR description.

6. feature/game-core: the scene, objects, dialogue with streaming, relevance-based memory
   unlocking, memory scenes, dawn clock, endings, save and resume, language switch.
   Fully playable using only fallback lines when the model is unavailable.

7. feature/atmosphere: candle flicker, petals, smoke, parallax, the spirit's progressive
   visibility, ambient sound, and the candles burning down with the dawn clock.

8. feature/first-launch-wizard: adapt the model wizard (consent before downloading, the
   recommended small models from the spike, progress, compatibility check). Its art and
   copy match the game's style.

9. feature/cross-platform-builds: adapt and run the CI matrix; smoke-test the /api binary
   and bundled Ollama on each OS; record installer sizes. STOP and show me options if any
   installer exceeds 1.5 GB.

10. feature/readme: README in English: the story premise (no spoilers), screenshots and a
    short gameplay GIF, install per OS (including unsigned-app warnings), how it runs
    offline, the model comparison table, how the canon keeps the AI coherent,
    architecture diagram, the branching model, credits and licenses, an honest note that
    the art was generated with a closed image model during development (via a ChatGPT
    subscription) while all runtime AI is open, a short note on Día de los Muertos and
    why the game treats it as remembrance, and a "Why open source matters here" section
    (plays with the lights and the internet off, never stops working because a service
    disappears, no data leaves the machine, swappable models).

11. release/1.0.0: from develop, PR into master, merge, tag v1.0.0, merge master back into
    develop; the tag workflow creates the DRAFT release with the three installers.

Priority if time runs short: story canon > spike > game core > art > atmosphere > wizard >
Windows and Linux builds. The game must always be playable end to end, even if art is
partly placeholder. Even when cutting scope, never skip the GitFlow sequence.

# General rules

- Code, comments, commits, PRs, and README in English; game content in English and
  Spanish.
- Don't invent Ollama, Electron, electron-builder, PyInstaller, or GitHub Actions options
  or flags: when unsure, check the official docs before writing code, and tell me if
  something isn't documented.
- Ask before installing anything globally or touching anything outside the repo.
- No API keys are used anywhere in this project. Never add one to .env, .env.example,
  the code, or CI; check the repo and the built installers for leaked secrets before
  every release.
- Keep docs/DECISIONS.md logging each technical decision and why; I'll use it for the post.
- Whenever I correct you on something that should apply to future work, propose adding
  it to AGENTS.md or the right nested AGENTS.md instead of only fixing the code.