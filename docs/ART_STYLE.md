# Art style

Original illustrated Mexican folk art at night: matte gouache color, hand-cut
paper shapes and fine relief-print linework. Use one coherent visual language,
simple readable silhouettes and restrained paper grain. Warm light rests on
dark surfaces. This is a family vigil and a celebration of remembrance.

## Palette and light

| Role | Color | Hex |
| --- | --- | --- |
| Night/background | Night blue | #10172E |
| Deep shadow | Deep purple | #392748 |
| Flowers/accent | Cempasúchil orange | #F2A12C |
| Paper/accent | Rosa mexicano | #CD3975 |
| Light/accent | Candle gold | #F6C56C |
| Highlights | Bone white | #FFF1D2 |

Use candle gold and orange as localized light, with quiet night blue and purple
around them. Rosa mexicano belongs mainly to papel picado and small accents.
Warm bone text is rendered by code over a dark opaque panel; art never carries
essential text or supplies the only indication that something is interactive.

## Setting and objects

The single scene is a modest home's ofrenda: stucco back wall, a small window,
three altar tiers with cloth and clay/talavera details, papel picado, marigold
garlands, flowers, pan de muerto, candles and a little copal vessel. A small
traditional sugar skull may appear as decoration, never a monster or a face
for the spirit. Leave quiet space around the six selectable objects.

The photograph shows three entirely fictional people in a sunny yard, slightly
tilted in a worn frame. The bowl holds dark bean soup and a green epazote leaf.
The wooden radio has a worn knob and a cloth grille. The screwdriver has a
smooth red handle and a small worn tip. The folded letter has a grease mark;
its visible paper is blank. The scarf is blue wool with one visible yellow seam.
Do not add readable writing, labels, signatures, numbers or pseudo-lettering.

## Character continuity

Inés is an entirely fictional older Mexican woman with warm brown skin, a softly
lined oval face, dark gentle eyes and silver hair gathered in a low bun. She
wears a plain cream blouse, deep purple skirt and a simple night-blue apron.
Her posture is dignified and relaxed, with hands resting naturally. No costume,
spectral injury, glowing eyes, theatrical grin or frightening skeletal anatomy.

At younger ages retain the same facial structure and plain clothing, with dark
hair in the same low bun. Other people are original fictional figures, with
ordinary period-appropriate clothing. The photograph is 1974 (Inés 38, Ernesto
an adult, Julián 10); the radio lesson is around her youth and the workshop opens
in 1958. Lucía is seven in 2009; the letter is from 1987; the scarf repair is 2011.
Memory images illustrate only the approved events, without adding new life facts.

The four spirit poses share the same design and crop. They progress from a
quiet uncertain outline to a relaxed, present person. Actual translucency and
visibility changes are applied by code, preserving clean transparent cutouts.

## Composition and deliverables

- Title/memory/ending illustrations: 1536 x 1024 target, one clear scene, no text.
- Ofrenda layers: the same 1536 x 1024 canvas and fixed eye-level perspective.
  Back wall is opaque; altar, papel picado and foreground are transparent layers.
- Object illustrations: 1024 x 1024 target, isolated on true transparency, generous
  breathing room, complete silhouettes and matching warm light from upper left.
- Spirit states: 1024 x 1536 target, full figure, same scale/crop, true transparency.
- UI: transparent paper/dialog borders and a candle icon, empty centers, no text.
- Decorative motion (flicker, smoke, drifting petals and parallax) is done in code.

Targets are final export dimensions; preserve source aspect ratio and alpha.
Keep originals locally, ship optimized WebP, and keep all shipped art under 30 MB.
Log every exact prompt, target and generation/processing result in ART_PROMPTS.md.
Inspect every asset for hands, faces, state continuity, text and cultural tone.

The selected source PNGs are preserved locally in `.dev/art-sources/`; their
names and hashes are recorded in `assets/manifest.json`. The source files are
not committed. To re-export from those selected sources, install the project
dependencies and run:

```sh
uv run --project api --with Pillow==13.0.0 python scripts/prepare-art.py
```

The script checks transparency and dimensions, exports the WebP files, and
creates the [contact sheet](ART_CONTACT_SHEET.webp) and a local composition
preview. The prompts allow new illustrations to be generated, but generated
images cannot be reproduced bit for bit from prompts alone.

## Restrictions

Use only original compositions. Do not reference or imitate any film, game,
brand, existing protected artwork or real person's likeness. Generic relief-print
techniques and public-domain Mexican engraving traditions may inform linework;
do not copy a specific work. No text inside generated images. No jump-scare,
monster, grotesque death or costume framing. Any external fonts/audio must have
permissive licenses and entries in CREDITS.md; procedural audio is preferred.

Generation uses the built-in development subscription tool only. No image API,
API credentials or generation code enters the shipped game. If the built-in tool
is unavailable, stop and supply the complete prompt list for assets/incoming/.
