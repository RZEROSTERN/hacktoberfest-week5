# Credits and licenses

La Última Vela / The Last Candle is original fiction about remembrance.

Code is MIT licensed; see LICENSE. Desktop isolation, process supervision and build
scripts are adapted from Marco Ramírez's MIT-licensed PostCall and Slothshot
projects. Their copyright notice is preserved in LICENSE. Neither is a dependency.

Runtime components: Ollama (MIT), Electron (MIT, with Chromium third-party notices),
Nuxt and Vue (MIT), FastAPI (MIT), Pydantic (MIT), HTTPX (BSD-3-Clause), Uvicorn
(BSD-3-Clause), psutil (BSD-3-Clause). Electron and Ollama licenses are copied into
the installed application by the packaging scripts. PyInstaller's distribution
exception permits shipping the bundled Python application.

## Artwork

The original illustrations were generated during development with the built-in
image-generation tool through a ChatGPT subscription, then reviewed and optimized
for this project. The complete prompts and revision notes are in
[docs/ART_PROMPTS.md](docs/ART_PROMPTS.md); the style guide is in
[docs/ART_STYLE.md](docs/ART_STYLE.md). The image tool is not used by the game.

## Fonts

- **Atkinson Hyperlegible**, copyright 2020 Braille Institute of America, Inc.,
  [source](https://fonts.google.com/specimen/Atkinson+Hyperlegible), SIL Open Font
  License 1.1: [license text](assets/licenses/AtkinsonHyperlegible-OFL.txt).
  Regular and bold font blobs: `b3cc4200fcf09d600eac74002ab4ea65b404a536` and
  `ca3f613847de62b8da83d2dab500ec391c8fe477` in the Google Fonts repository.
- **Cormorant Garamond**, copyright 2015 the Cormorant Project Authors,
  [source](https://fonts.google.com/specimen/Cormorant+Garamond), SIL Open Font
  License 1.1: [license text](assets/licenses/CormorantGaramond-OFL.txt).
  Variable font blob: `d992a83ce525c330fad3a19087746bcb2dc038ee` in Google Fonts.

The original font files were downloaded from the Google Fonts repository and
verified against those Git blob hashes. They are distributed without modification.

## Local model and sound

The recommended [Qwen 3.5 0.8B](https://ollama.com/library/qwen3.5:0.8b) weights
use Apache License 2.0; [the license](assets/licenses/Qwen3.5-Apache-2.0.txt) was
copied from the model manifest. Weights are not bundled and require explicit
download consent. All inference is local to the player's computer.

No external sound files are included. `web/app/utils/ambient-audio.ts` generates
a quiet breeze and simple musical tones with the Web Audio API. The player can enable it and adjust its volume in the game.
