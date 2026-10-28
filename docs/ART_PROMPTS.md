# Art prompts

Every entry uses the built-in development subscription image tool only. No image API or credentials.
Targets are final export sizes. Preserve source aspect ratio and alpha; optimize selected outputs to WebP.
If generation is unavailable, create these images in ChatGPT and put the PNGs in assets/incoming/
using the target basename. All generated images are text-free; the game renders every label.

## title

Target: assets/art/title.webp — 1536 x 1024; transparent: False. Status: initial version rejected; corrected version exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: A modest home’s ofrenda at night, viewed at eye level: three tiers with clay/talavera details, candles, cempasúchil garlands, papel picado, pan de muerto and a small traditional sugar skull decoration. A gentle barely suggested human presence beyond the altar, never a monster. The emotional focus is the final candle. Quiet dark space in the upper third for a title rendered later by code. No visible writing on any object.
Constraints: One complete scene, restrained detail, no frames, no text. Keep the illustration legible at small display sizes.
```

## ofrenda-wall

Target: assets/art/ofrenda-wall.webp — 1536 x 1024; transparent: False. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Back-wall layer only for a fixed eye-level ofrenda scene: quiet purple-blue stucco wall, a small dark window in the upper right showing night, subtle warm reflected candlelight around lower center. Empty central and lower canvas for separate altar layers; no altar, people, flowers, hanging paper or candles in this layer.
Constraints: One complete scene, restrained detail, no frames, no text. Keep the illustration legible at small display sizes.
```

## ofrenda-altar

Target: assets/art/ofrenda-altar.webp — 1536 x 1024; transparent: True. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Altar-tier layer only on a fixed 1536 x 1024 canvas at eye level: three modest cloth-covered tiers centered in the lower two thirds, top tier around 43 percent canvas height, bottom edge around 90 percent. A few clay/talavera dishes and pan de muerto, one small sugar skull decoration and a copal vessel. Leave six generous clear spaces for separate objects. No photograph, soup bowl, radio, screwdriver, letter, scarf, wall, flowers or burning candles. The upper third stays transparent.
Constraints: True transparent background; clean alpha; preserve the complete subject with generous margins. No backdrop or cast shadow beyond the subject.
```

## ofrenda-papel

Target: assets/art/ofrenda-papel.webp — 1536 x 1024; transparent: True. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: A single loose garland of rosa mexicano, orange and purple papel picado across the upper fifth of the same fixed canvas. Original cut-paper floral, bird and simple traditional calavera motifs, delicate perforations, no writing. All lower canvas transparent; no wall, altar or people.
Constraints: True transparent background; clean alpha; preserve the complete subject with generous margins. No backdrop or cast shadow beyond the subject.
```

## ofrenda-foreground

Target: assets/art/ofrenda-foreground.webp — 1536 x 1024; transparent: True. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Foreground layer on the same fixed canvas: loose cempasúchil flower clusters and petals in the bottom corners, with modest unlit candle holders and a few complete warm wax candles along the bottom eighth. Clear transparent center so separate altar objects remain visible. No people, altar tiers, wall or hanging paper. Candle flames will be animated by code; wax candles themselves are unlit.
Constraints: True transparent background; clean alpha; preserve the complete subject with generous margins. No backdrop or cast shadow beyond the subject.
```

## object-photograph

Target: assets/art/object-photograph.webp — 1024 x 1024; transparent: True. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1024 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: A small worn wooden frame, slightly tilted, holding an illustrated sunny 1974 yard portrait of three fictional people: a 38-year-old Mexican woman with dark hair in a low bun laughing, an adult man beside her and their ten-year-old boy. No names or dates printed on the image. Warm light from upper left.
Constraints: True transparent background; clean alpha; preserve the complete subject with generous margins. No backdrop or cast shadow beyond the subject.
```

## object-bowl

Target: assets/art/object-bowl.webp — 1024 x 1024; transparent: True. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1024 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: One glazed clay bowl of dark black-bean soup, with a single green epazote leaf floating on the surface; understated blue talavera detail along the rim, no letters. Warm light from upper left.
Constraints: True transparent background; clean alpha; preserve the complete subject with generous margins. No backdrop or cast shadow beyond the subject.
```

## object-radio

Target: assets/art/object-radio.webp — 1024 x 1024; transparent: True. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1024 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: One small mid-century wooden radio, rounded modest cabinet, worn tuning knob and cloth speaker grille. Dial has simple unlettered marks only, no words, numbers or brands. Warm light from upper left.
Constraints: True transparent background; clean alpha; preserve the complete subject with generous margins. No backdrop or cast shadow beyond the subject.
```

## object-screwdriver

Target: assets/art/object-screwdriver.webp — 1024 x 1024; transparent: True. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1024 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: One small well-used screwdriver diagonally arranged, smooth polished red handle with a natural thumb-worn area, small worn metal tip. No letters, marks or labels. Warm light from upper left.
Constraints: True transparent background; clean alpha; preserve the complete subject with generous margins. No backdrop or cast shadow beyond the subject.
```

## object-letter

Target: assets/art/object-letter.webp — 1024 x 1024; transparent: True. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1024 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: One cream paper letter folded and unfolded many times, partly open with a small dark grease mark at one corner. All visible paper is completely blank: no handwriting, text or pseudo-lettering. Warm light from upper left.
Constraints: True transparent background; clean alpha; preserve the complete subject with generous margins. No backdrop or cast shadow beyond the subject.
```

## object-scarf

Target: assets/art/object-scarf.webp — 1024 x 1024; transparent: True. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1024 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: One soft blue wool scarf loosely folded, a short clearly visible yellow-thread seam crossing the wool. A careful practical repair, readable silhouette and visible fabric texture. No words or labels. Warm light from upper left.
Constraints: True transparent background; clean alpha; preserve the complete subject with generous margins. No backdrop or cast shadow beyond the subject.
```

## spirit-1

Target: assets/art/spirit-1.webp — 1024 x 1536; transparent: True. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1024 x 1536 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Inés is fictional: warm brown skin, a softly lined oval face, gentle dark eyes, silver hair in a low bun, plain cream blouse, deep purple skirt and simple night-blue apron. Dignified relaxed posture; natural hands. For younger ages keep the face structure and bun, using dark hair and fewer lines. Full figure, both feet visible, consistent straight-on three-quarter stance and scale. Quiet uncertain posture, hands resting together, looking gently toward the viewer; a clean simple silhouette. Full opaque painted figure with clean transparent surround; the game will apply translucency, not baked-in dark fog.
Constraints: True transparent background; clean alpha; preserve the complete subject with generous margins. No backdrop or cast shadow beyond the subject.
```

## spirit-2

Target: assets/art/spirit-2.webp — 1024 x 1536; transparent: True. Status: initial prompt not used; identity-preserving revision exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1024 x 1536 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Inés is fictional: warm brown skin, a softly lined oval face, gentle dark eyes, silver hair in a low bun, plain cream blouse, deep purple skirt and simple night-blue apron. Dignified relaxed posture; natural hands. For younger ages keep the face structure and bun, using dark hair and fewer lines. Full figure, both feet visible, consistent straight-on three-quarter stance and scale. Looking at a small detail just below eye level, one hand beginning a gentle gesture of recognition. Full opaque painted figure with clean transparent surround; the game will apply translucency, not baked-in dark fog.
Constraints: True transparent background; clean alpha; preserve the complete subject with generous margins. No backdrop or cast shadow beyond the subject.
```

## spirit-3

Target: assets/art/spirit-3.webp — 1024 x 1536; transparent: True. Status: initial prompt not used; identity-preserving revision exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1024 x 1536 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Inés is fictional: warm brown skin, a softly lined oval face, gentle dark eyes, silver hair in a low bun, plain cream blouse, deep purple skirt and simple night-blue apron. Dignified relaxed posture; natural hands. For younger ages keep the face structure and bun, using dark hair and fewer lines. Full figure, both feet visible, consistent straight-on three-quarter stance and scale. A calm slight smile, open relaxed hands, shoulders less guarded. Full opaque painted figure with clean transparent surround; the game will apply translucency, not baked-in dark fog.
Constraints: True transparent background; clean alpha; preserve the complete subject with generous margins. No backdrop or cast shadow beyond the subject.
```

## spirit-4

Target: assets/art/spirit-4.webp — 1024 x 1536; transparent: True. Status: initial prompt not used; identity-preserving revision exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1024 x 1536 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Inés is fictional: warm brown skin, a softly lined oval face, gentle dark eyes, silver hair in a low bun, plain cream blouse, deep purple skirt and simple night-blue apron. Dignified relaxed posture; natural hands. For younger ages keep the face structure and bun, using dark hair and fewer lines. Full figure, both feet visible, consistent straight-on three-quarter stance and scale. Fully relaxed and present, a warm small smile and one open hand in a dignified farewell. Full opaque painted figure with clean transparent surround; the game will apply translucency, not baked-in dark fog.
Constraints: True transparent background; clean alpha; preserve the complete subject with generous margins. No backdrop or cast shadow beyond the subject.
```

## memory-photograph

Target: assets/art/memory-photograph.webp — 1536 x 1024; transparent: False. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Inés is fictional: warm brown skin, a softly lined oval face, gentle dark eyes, silver hair in a low bun, plain cream blouse, deep purple skirt and simple night-blue apron. Dignified relaxed posture; natural hands. For younger ages keep the face structure and bun, using dark hair and fewer lines. Memory vignette with age as specified: Sunny 1974 yard: fictional Inés at 38 with dark hair in a low bun is caught laughing before she can compose herself. Her adult husband Ernesto is trying to stand properly for the picture, their ten-year-old son Julián has just made her laugh. Three people only. A modest Puebla home yard, not a landmark. No camera interface, writing or dates.
Constraints: One complete scene, restrained detail, no frames, no text. Keep the illustration legible at small display sizes.
```

## memory-bowl

Target: assets/art/memory-bowl.webp — 1536 x 1024; transparent: False. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Inés is fictional: warm brown skin, a softly lined oval face, gentle dark eyes, silver hair in a low bun, plain cream blouse, deep purple skirt and simple night-blue apron. Dignified relaxed posture; natural hands. For younger ages keep the face structure and bun, using dark hair and fewer lines. Memory vignette with age as specified: A modest home table: adult fictional Inés divides black-bean soup between two clay bowls for herself and her friend Berta, two women seated talking. Rain is suggested outside a small window; the soup and an offered place at the table are central. No extra diners, writing or dramatic distress.
Constraints: One complete scene, restrained detail, no frames, no text. Keep the illustration legible at small display sizes.
```

## memory-radio

Target: assets/art/memory-radio.webp — 1536 x 1024; transparent: False. Status: initial version generated; corrected version exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Inés is fictional: warm brown skin, a softly lined oval face, gentle dark eyes, silver hair in a low bun, plain cream blouse, deep purple skirt and simple night-blue apron. Dignified relaxed posture; natural hands. For younger ages keep the face structure and bun, using dark hair and fewer lines. Memory vignette with age as specified: A quiet lesson in a modest room: young adult fictional Inés with dark hair in a low bun pauses beside her father Aurelio, an older Mexican man whose hand rests on a small wooden radio. They listen before touching a tool. Warm daylight, practical unbranded objects, no writing or modern screens.
Constraints: One complete scene, restrained detail, no frames, no text. Keep the illustration legible at small display sizes.
```

## memory-screwdriver

Target: assets/art/memory-screwdriver.webp — 1536 x 1024; transparent: False. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Inés is fictional: warm brown skin, a softly lined oval face, gentle dark eyes, silver hair in a low bun, plain cream blouse, deep purple skirt and simple night-blue apron. Dignified relaxed posture; natural hands. For younger ages keep the face structure and bun, using dark hair and fewer lines. Memory vignette with age as specified: 2009: fictional Inés at 73 with silver hair in a low bun patiently sits with her seven-year-old granddaughter Lucía at a low worktable. An unplugged small radio is open with its batteries visibly removed and laid aside. The smooth red-handled screwdriver rests on the table; a little screw has fallen onto the floor and both pause to look for it. No live electrical work, extra people or text.
Constraints: One complete scene, restrained detail, no frames, no text. Keep the illustration legible at small display sizes.
```

## memory-letter

Target: assets/art/memory-letter.webp — 1536 x 1024; transparent: False. Status: initial version generated; corrected version exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Inés is fictional: warm brown skin, a softly lined oval face, gentle dark eyes, silver hair in a low bun, plain cream blouse, deep purple skirt and simple night-blue apron. Dignified relaxed posture; natural hands. For younger ages keep the face structure and bun, using dark hair and fewer lines. Memory vignette with age as specified: 1987: fictional Inés at 51, dark hair with a few silver strands in a low bun, sits at her workbench composing a letter on completely blank folded cream paper with a grease mark at one corner. Her hand pauses thoughtfully with a pencil. A quiet empty chair and a window suggest distance, without extra people. No visible writing or pseudo-lettering anywhere.
Constraints: One complete scene, restrained detail, no frames, no text. Keep the illustration legible at small display sizes.
```

## memory-scarf

Target: assets/art/memory-scarf.webp — 1536 x 1024; transparent: False. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Inés is fictional: warm brown skin, a softly lined oval face, gentle dark eyes, silver hair in a low bun, plain cream blouse, deep purple skirt and simple night-blue apron. Dignified relaxed posture; natural hands. For younger ages keep the face structure and bun, using dark hair and fewer lines. Memory vignette with age as specified: 2011: fictional Inés at 75 with silver hair in a low bun accepts her blue wool scarf from her friend Berta, an older Mexican woman. A short yellow seam is clear between their hands. A small, practical gesture of care in a modest home; two people only, no text.
Constraints: One complete scene, restrained detail, no frames, no text. Keep the illustration legible at small display sizes.
```

## ending-peace

Target: assets/art/ending-peace.webp — 1536 x 1024; transparent: False. Status: clarified version generated; canon-corrected version exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Dawn at the same modest home ofrenda. Inés is fictional: warm brown skin, a softly lined oval face, gentle dark eyes, silver hair in a low bun, plain cream blouse, deep purple skirt and simple night-blue apron. Dignified relaxed posture; natural hands. For younger ages keep the face structure and bun, using dark hair and fewer lines. The spirit calmly offers a final open-handed farewell, her face quietly at peace. The six familiar objects rest on the altar in warm low candlelight; pale gold-blue dawn through the window. Remembrance, not triumph or spectacle. No text or new people.
Constraints: One complete scene, restrained detail, no frames, no text. Keep the illustration legible at small display sizes.
```

## ending-bittersweet

Target: assets/art/ending-bittersweet.webp — 1536 x 1024; transparent: False. Status: clarified version generated; canon-corrected version exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Dawn at the same modest home ofrenda. Inés is fictional: warm brown skin, a softly lined oval face, gentle dark eyes, silver hair in a low bun, plain cream blouse, deep purple skirt and simple night-blue apron. Dignified relaxed posture; natural hands. For younger ages keep the face structure and bun, using dark hair and fewer lines. The spirit sits in a quiet, dignified pause, a small tender smile and a little uncertainty. A few candles remain, the six familiar objects are present, blue-gold window light approaches. Gentle bittersweet parting, no crying spectacle or new people.
Constraints: One complete scene, restrained detail, no frames, no text. Keep the illustration legible at small display sizes.
```

## ending-forgotten

Target: assets/art/ending-forgotten.webp — 1536 x 1024; transparent: False. Status: clarified version generated; canon-corrected version exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Dawn at the same modest home ofrenda, now with an empty place beyond the candlelight. No person or monster appears. The six familiar objects remain and a last small candle rests among orange marigolds. Quiet pale blue light through the window, dignified absence and remembrance. No scary faces or text.
Constraints: One complete scene, restrained detail, no frames, no text. Keep the illustration legible at small display sizes.
```

## ui-papel-frame

Target: assets/art/ui-papel-frame.webp — 1536 x 1024; transparent: True. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: An original papel picado rectangular border only, with small orange and rosa mexicano floral perforations and a few bone-white accents. Broad empty transparent center, restrained corners and thin edges so later code-rendered text remains readable. No backdrop, words or symbols resembling writing.
Constraints: True transparent background; clean alpha; preserve the complete subject with generous margins. No backdrop or cast shadow beyond the subject.
```

## ui-dialog-border

Target: assets/art/ui-dialog-border.webp — 1536 x 1024; transparent: True. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: A restrained thin hand-printed rectangular dialog border with small cempasúchil corner motifs and candle-gold relief-print edges. Wide empty transparent center, no opaque panel, flowers only at corners, no text. The game supplies its own dark accessible panel behind this border.
Constraints: True transparent background; clean alpha; preserve the complete subject with generous margins. No backdrop or cast shadow beyond the subject.
```

## ui-candle

Target: assets/art/ui-candle.webp — 1024 x 1024; transparent: True. Status: generated and exported.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1024 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: One simple tall bone-white wax candle in a small clay holder, warm golden highlight along one side, centered and complete. No painted flame: the game adds flicker in code. Clear silhouette at icon scale, no other objects, words or numbers.
Constraints: True transparent background; clean alpha; preserve the complete subject with generous margins. No backdrop or cast shadow beyond the subject.
```

## Title revision 2 — remove unrequested figures

Target: assets/art/title.webp — 1536 x 1024, opaque.

The first image is retained locally as title-v1.png and rejected: it adds a young woman, a dog and multiple portrait frames. The revision preserves its palette and painting style while removing these unrequested narrative details.

```text
Edit the supplied title illustration. Keep the same composition, warm candlelight, folk-art gouache texture, marigolds, talavera, papel picado and night palette. Remove every person and animal completely: no woman, dog, human silhouette or spirit. Replace the multiple portrait frames with exactly one small tilted wooden frame containing a simple sunny-yard illustration of three fictional people: a laughing 38-year-old woman with dark hair in a low bun, her adult husband and their ten-year-old son. Add only the six canonical altar objects among the existing decorations: that single framed picture, one dark bean-soup bowl with a green leaf, one small unbranded wooden radio with no writing or numbers, a smooth red-handled screwdriver, a folded completely blank letter with a grease mark, and blue wool scarf with a yellow seam. Keep the upper third quiet for a title rendered later by code. No text, labels, numbers, signatures, watermarks, extra people or animals anywhere.
```

## spirit-2 — identity-preserving revision

Target: assets/art/spirit-2.webp — 1024 x 1536; transparent. Input: selected spirit-1 portrait as an edit target.

```text
Edit the supplied full-body portrait of a fictional, dignified older Mexican woman. Preserve exactly her face, silver low bun, skin tone, cream blouse, night-blue apron, purple floral skirt, shoes, illustration style, lighting, proportions, centered position, full-body crop and true transparent background. Keep both feet fully visible; no real person likeness, monsters, text or additional objects. Only change the expression and hands: She looks gently downward in thought, with one hand raised lightly toward her chest and the other relaxed near her waist. Maintain the same single character; no words, marks or pseudo-lettering.
```

## spirit-3 — identity-preserving revision

Target: assets/art/spirit-3.webp — 1024 x 1536; transparent. Input: selected spirit-1 portrait as an edit target.

```text
Edit the supplied full-body portrait of a fictional, dignified older Mexican woman. Preserve exactly her face, silver low bun, skin tone, cream blouse, night-blue apron, purple floral skirt, shoes, illustration style, lighting, proportions, centered position, full-body crop and true transparent background. Keep both feet fully visible; no real person likeness, monsters, text or additional objects. Only change the expression and hands: She has a small, warm smile; one hand is open at waist height in a calm welcoming gesture, the other rests naturally. Maintain the same single character; no words, marks or pseudo-lettering.
```

## spirit-4 — identity-preserving revision

Target: assets/art/spirit-4.webp — 1024 x 1536; transparent. Input: selected spirit-1 portrait as an edit target.

```text
Edit the supplied full-body portrait of a fictional, dignified older Mexican woman. Preserve exactly her face, silver low bun, skin tone, cream blouse, night-blue apron, purple floral skirt, shoes, illustration style, lighting, proportions, centered position, full-body crop and true transparent background. Keep both feet fully visible; no real person likeness, monsters, text or additional objects. Only change the expression and hands: She looks peacefully toward the viewer with a warm subtle smile and gives a small, dignified farewell with one raised open hand; the other hand rests near her waist. Maintain the same single character; no words, marks or pseudo-lettering.
```

## ending-peace — clarified canonical object list

Target: assets/art/ending-peace.webp — 1536 x 1024; opaque.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Dawn at the same modest home ofrenda. Inés is fictional: warm brown skin, a softly lined oval face, gentle dark eyes, silver hair in a low bun, plain cream blouse, deep purple skirt and simple night-blue apron. Dignified relaxed posture; natural hands. For younger ages keep the face structure and bun, using dark hair and fewer lines. The spirit calmly offers a final open-handed farewell, her face quietly at peace. The six familiar objects rest on the altar in warm low candlelight; pale gold-blue dawn through the window. Remembrance, not triumph or spectacle. No text or new people.
Constraints: One complete scene, restrained detail, no frames, no text. Keep the illustration legible at small display sizes. The six objects are a single tilted family photograph, black-bean soup with one green leaf, an unlabelled wooden radio, a red-handled screwdriver, a completely blank folded letter with one grease mark, and a blue wool scarf with one short yellow seam. No lettering or numbers, including on the radio or letter.
```

## ending-bittersweet — clarified canonical object list

Target: assets/art/ending-bittersweet.webp — 1536 x 1024; opaque.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Dawn at the same modest home ofrenda. Inés is fictional: warm brown skin, a softly lined oval face, gentle dark eyes, silver hair in a low bun, plain cream blouse, deep purple skirt and simple night-blue apron. Dignified relaxed posture; natural hands. For younger ages keep the face structure and bun, using dark hair and fewer lines. The spirit sits in a quiet, dignified pause, a small tender smile and a little uncertainty. A few candles remain, the six familiar objects are present, blue-gold window light approaches. Gentle bittersweet parting, no crying spectacle or new people.
Constraints: One complete scene, restrained detail, no frames, no text. Keep the illustration legible at small display sizes. The six objects are a single tilted family photograph, black-bean soup with one green leaf, an unlabelled wooden radio, a red-handled screwdriver, a completely blank folded letter with one grease mark, and a blue wool scarf with one short yellow seam. No lettering or numbers, including on the radio or letter.
```

## ending-forgotten — clarified canonical object list

Target: assets/art/ending-forgotten.webp — 1536 x 1024; opaque.

```text
Use case: illustration-story. Asset type: original narrative-game illustration, 1536 x 1024 target.
Style/medium: Original illustrated Mexican folk art: matte gouache, hand-cut paper shapes, fine relief-print linework, restrained paper grain. Night blue #10172E and deep purple #392748, cempasúchil orange #F2A12C, rosa mexicano #CD3975, candle gold #F6C56C and bone white #FFF1D2. Warm candlelight against dark. A dignified family vigil celebrating remembrance. Entirely original fictional people and composition. No text, numbers, signatures, watermarks, labels or pseudo-lettering. No film, game, brand, protected-artwork or real-person references. No monsters, injuries, glowing eyes or costume treatment.
Primary request: Dawn at the same modest home ofrenda, now with an empty place beyond the candlelight. No person or monster appears. The six familiar objects remain and a last small candle rests among orange marigolds. Quiet pale blue light through the window, dignified absence and remembrance. No scary faces or text.
Constraints: One complete scene, restrained detail, no frames, no text. Keep the illustration legible at small display sizes. The six objects are a single tilted family photograph, black-bean soup with one green leaf, an unlabelled wooden radio, a red-handled screwdriver, a completely blank folded letter with one grease mark, and a blue wool scarf with one short yellow seam. No lettering or numbers, including on the radio or letter.
```

## memory-radio — correction

Target: assets/art/memory-radio.webp — 1536 x 1024; opaque. Input: the first generated memory image as the edit target.

```text
Edit the supplied radio memory illustration. Preserve the two fictional people, their faces, clothing, posture, hands, room, colors, warm light and composition exactly. Change only the radio face: replace every tiny letter-like, number-like and station marking with plain woven speaker cloth and simple unlabelled horizontal texture. Keep the wooden radio and its two knobs. No text, numbers, logos, signatures or pseudo-lettering anywhere.
```

## memory-letter — correction

Target: assets/art/memory-letter.webp — 1536 x 1024; opaque. Input: the first generated memory image as the edit target.

```text
Edit the supplied letter memory illustration. Preserve the fictional woman, face, clothing, posture, hands, fully blank paper with the grease mark, window, chair, colors, lighting and composition exactly. Remove both framed pictures from the upper-left wall, including the devotional figure. Replace them only with plain textured stucco matching the nearby wall. Do not add symbols, religious imagery, new people, letters, numbers, signatures or pseudo-lettering.
```

## ending-peace — canon correction

Target: assets/art/ending-peace.webp — 1536 x 1024; opaque. Input: first generated ending as the edit target.

```text
Edit this fictional game ending illustration. Keep the existing folk-art painting style, dawn light, altar objects, flowers, clothing and composition. Remove the younger translucent woman behind the altar completely. There must be exactly one person in the scene outside the small framed photograph: the existing silver-haired older woman seated at the left, who is the spirit Inés. Do not add any other person, ghost, figure, animal or face. In the little framed photograph depict exactly three fictional people: a laughing adult woman with dark hair in a low bun, an adult man and their ten-year-old son. Keep the letter paper blank and the radio free of writing or numbers. No text, logos or symbols anywhere. Give the seated older woman a gentle, dignified small farewell gesture with one open hand and a peaceful expression. The altar retains the bowl, photo, radio, screwdriver, blank letter and blue scarf with one yellow seam.
```

## ending-bittersweet — canon correction

Target: assets/art/ending-bittersweet.webp — 1536 x 1024; opaque. Input: first generated ending as the edit target.

```text
Edit this fictional game ending illustration. Keep the existing folk-art painting style, dawn light, altar objects, flowers, clothing and composition. Remove the younger translucent woman behind the altar completely. There must be exactly one person in the scene outside the small framed photograph: the existing silver-haired older woman seated at the left, who is the spirit Inés. Do not add any other person, ghost, figure, animal or face. In the little framed photograph depict exactly three fictional people: a laughing adult woman with dark hair in a low bun, an adult man and their ten-year-old son. Keep the letter paper blank and the radio free of writing or numbers. No text, logos or symbols anywhere. Keep her seated in a quiet, dignified pause with a tender small smile and a little uncertainty. The altar retains the bowl, photo, radio, screwdriver, blank letter and blue scarf with one yellow seam.
```

## ending-forgotten — canon correction

Target: assets/art/ending-forgotten.webp — 1536 x 1024; opaque. Input: first generated ending as the edit target.

```text
Edit this fictional game ending illustration. Keep the empty chair, dawn light, altar, flowers, bowl, radio, red-handled screwdriver, blank letter, blue scarf and composition exactly unchanged. Change only the small framed photograph: show exactly three fictional people, a laughing adult woman with dark hair in a low bun, an adult man, and their ten-year-old son. Remove the extra fourth person in the photograph. No people anywhere outside the photograph, no monsters, no text, numbers, labels, logos, signatures or pseudo-lettering.
```
