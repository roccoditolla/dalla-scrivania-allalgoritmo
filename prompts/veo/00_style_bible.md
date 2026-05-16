# Veo Style Bible — DNA visivo

> Questo blocco viene **iniettato in ogni prompt Veo** dallo script `scripts/generate_scene.py`.
> Garantisce coerenza visiva attraverso tutte le 17 clip.

---

## STYLE_DNA (da iniettare alla fine di ogni prompt)

```
Style: cinematic animated illustration in the tradition of high-end European 2D animation.
Visible painterly brush strokes, hand-drawn quality with professional polish.
Limited and intentional color palette: cream white (#F5EFE6) dominates, deep ink black for lines and shadows, muted desaturated ocean blues, sand beige, with a single highly saturated orange (#FF6B1A) reserved for moments of narrative significance only.
Color temperature: warm but desaturated overall.
Lighting: cinematic and intentional, with strong directional light sources, long shadows, atmospheric haze, and god rays where appropriate.
Composition: rule of thirds, strong silhouettes, characters consistently in backlight or shadow, faces never shown in detail.
Camera movement: slow, deliberate, single direction per shot — never shaky, never fast cuts.
Atmosphere: contemplative, mythic, epic but intimate. The pacing of Studio Ghibli, the color discipline of Cartoon Saloon, the framing of cinematographer Roger Deakins.
Audio: ambient, naturalistic, supporting the visual without overwhelming.
```

---

## NEGATIVE_PROMPT (da iniettare in ogni call)

```
text, watermark, logo, ugly faces, deformed hands, deformed fingers, extra limbs, photorealistic humans, plastic skin, glossy 3D render, anime style, cel-shaded, manga, low-resolution, pixelated, oversaturated, neon, cyberpunk, dystopian, dark grim horror, gore, multiple suns, impossible reflections, jpeg artifacts, modern technology in fantasy scenes (no smartphones, no neon signs, no modern buildings unless in the futuristic island scenes 5-12 where they must remain mythic not literal).
```

---

## Camera language (vocabolario condiviso)

Da usare nei prompt per essere consistenti:

| Termine | Significato pratico |
|---|---|
| **slow dolly in** | Camera avanza lentamente verso il soggetto, profondità di campo che si riduce |
| **slow dolly out** | Camera si allontana, rivela contesto |
| **slow pan left/right** | Camera ruota orizzontalmente su asse fisso |
| **slow crane down** | Camera scende dall'alto, verticale |
| **slow crane up** | Camera sale verso l'alto |
| **static wide** | Camera ferma, shot grande |
| **static medium** | Camera ferma, busto |
| **macro close-up** | Camera molto vicina, dettaglio (mano, occhio, oggetto) |
| **tracking shot** | Camera segue il soggetto in movimento, parallela |

**Mai usare:** zoom, shaky cam, dutch angle, whip pan, jump cut.

---

## Character language

| Termine | Significato pratico |
|---|---|
| **in silhouette** | Personaggio in nero contro luce di sfondo |
| **in backlight** | Luce dietro al personaggio, contorni illuminati, faccia in ombra |
| **seen from behind** | Vista da dietro, spalle/nuca |
| **3/4 profile** | Tre quarti di profilo |
| **only hands visible** | Solo le mani entrano in inquadratura |
| **weathered hands** | Mani rugose, segnate, esperte |

---

## Lighting language

| Termine | Significato pratico |
|---|---|
| **golden hour light** | Luce dorata bassa, calda (alba/tramonto) |
| **stormy overcast** | Cielo nuvoloso, luce diffusa, fredda |
| **diffused midday** | Luce di giorno con foschia, soft |
| **warm interior glow** | Luce calda interna (lampada, fuoco) |
| **inner orange glow** | **TERMINE SPECIALE** — usato solo per la bussola arancione che emette luce dall'interno |
| **god rays through clouds** | Raggi di luce visibili che attraversano le nuvole |
| **moonlight on water** | Riflessi argentei sull'acqua di notte |

---

## Sound language (per audio_generation: true)

Da inserire nel prompt come hint per Veo audio:

| Scena | Audio descritto nel prompt |
|---|---|
| Mare calmo | "Soft ocean waves, distant seagulls, wind through sails" |
| Tempesta | "Thunder crashing, heavy rain on wood, howling wind, ship creaking under strain" |
| Mistery isola | "Eerie low drone, distant chimes, foreboding silence" |
| Bussola accende | "Crystalline magical shimmer, deep warm resonance, ethereal hum" |
| Sbarco | "Oars in calm water, distant gulls, sand crunching" |

---

## Template prompt (struttura da seguire)

Ogni prompt Veo finale è una stringa di ~150-250 parole costruita così:

```
[SHOT TYPE] of [SUBJECT] [ACTION] in [ENVIRONMENT].
[CAMERA MOVEMENT].
[LIGHTING DESCRIPTION].
[MOOD/ATMOSPHERE].
[AUDIO HINT].
[STYLE_DNA — blocco completo iniettato]
```

Esempio (Scena 01):
```
Wide cinematic shot of an antique wooden sailing ship gliding through calm dawn ocean waters. Slow crane down from sky to the ship's bow, ending on a static shot of the prow cutting through water. Golden hour light from low east, long warm shadows on white sails, atmospheric mist over horizon. Contemplative, mythic mood — the beginning of a journey. Soft ocean waves, distant seagulls, gentle wind through sails. Style: cinematic animated illustration in the tradition of high-end European 2D animation. [...STYLE_DNA completo...]
```

---

## Riferimenti visivi (da mostrare a Rocco per allineamento iniziale)

Per allineare il gusto, valgono come moodboard:

- **Studio Ghibli** — "Porco Rosso", "Castle in the Sky" — palette, atmosfera
- **Cartoon Saloon** — "Song of the Sea", "The Secret of Kells" — disciplina cromatica
- **Tomer Hanuka** — illustrazioni editoriali — silhouette forti
- **Jon Klassen** — minimalismo + emozione
- **Roger Deakins** — cinematografia "1917", "Blade Runner 2049" — lighting

NON-riferimenti (cosa evitare):
- Disney 3D (Frozen, Tangled)
- Pixar (troppo "lucidato")
- Anime giapponese stilizzato
- Illustrazione corporate piatta
