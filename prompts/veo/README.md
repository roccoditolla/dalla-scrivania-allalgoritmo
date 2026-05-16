# Scene Veo — Stato dei prompt

> Questo file traccia lo stato di tutti i prompt scena.
> Aggiornare ad ogni iterazione.

## Stato attuale — tutti i prompt JSON pronti ✅

I prompt sono pronti per essere passati a `scripts/generate_scene.py`.
Lo **status di generazione** (`generated`/`approved`/`rejected`) va aggiornato dopo ogni esecuzione.

| Scena | File JSON | Prompt | Generato | Approvato | Note |
|---|---|---|---|---|---|
| 01 — Open Sea | `scene_01_open_sea.json` | ✅ | ⏳ | ⏳ | Apertura |
| 02A — Ciurma sul ponte | `scene_02a_crew_on_deck.json` | ✅ | ⏳ | ⏳ | |
| 02B — Mani al lavoro | `scene_02b_hands_at_work.json` | ✅ | ⏳ | ⏳ | Macro montage |
| 03A — Tempesta | `scene_03a_storm.json` | ✅ | ⏳ | ⏳ | **WOW 1** |
| 03B — Capitano nella tempesta | `scene_03b_captain.json` | ✅ | ⏳ | ⏳ | |
| 04 — Mare calmo dopo | `scene_04_calm_after.json` | ✅ | ⏳ | ⏳ | |
| 05 — Isola appare | `scene_05_horizon_island.json` | ✅ | ⏳ | ⏳ | **WOW 2** |
| 06 — Sbarco | `scene_06_landing.json` | ✅ | ⏳ | ⏳ | Primo accenno arancione |
| 07 — Mano sulla sabbia | `scene_07_hand_in_sand.json` | ✅ | ⏳ | ⏳ | Setup WOW 3 |
| 08A — Bussola si accende | `scene_08a_compass_lights_up.json` | ✅ | ⏳ | ⏳ | **WOW 3 critico** |
| 08B — Ago della bussola | `scene_08b_needle_spinning.json` | ✅ | ⏳ | ⏳ | Continuazione 08A |
| 09A — Cerchio attorno alla bussola | `scene_09a_circle.json` | ✅ | ⏳ | ⏳ | Musica entra |
| 09B — Ago si ferma | `scene_09b_needle_stops.json` | ✅ | ⏳ | ⏳ | |
| 10 — Ritorno alla nave | `scene_10_return.json` | ✅ | ⏳ | ⏳ | Mirror di 06 |
| 11A — Nave salpa | `scene_11a_setting_sail.json` | ✅ | ⏳ | ⏳ | Climax narrativo |
| 11B — Due bussole sul ponte | `scene_11b_two_compasses.json` | ✅ | ⏳ | ⏳ | Sintesi |
| 12 — Transizione al realistic | `scene_12_transition.json` | ✅ | ⏳ | ⏳ | Difficile, fallback Imagen 3 |

**Totale clip:** 17 | **Costo stimato quality mode:** ~$102 + margine 30% rigenerazioni

## Come creare i prompt mancanti

Usare la skill `veo-cinematic-prompt` (in `.claude/skills/veo-cinematic-prompt/SKILL.md`).

Da Claude Code:
```
@veo-cinematic-prompt crea il prompt per la scena 02A leggendo lo storyboard
```

La skill assembla automaticamente:
- I dettagli dello storyboard (`docs/02_STORYBOARD.md`)
- Il DNA stilistico (`prompts/veo/00_style_bible.md`)
- Le costanti di camera/lighting (vedere style_bible)

## Convenzioni di naming

- File: `scene_<ID>_<descriptor>.json` (snake_case)
- Output video: `deck/assets/videos/scene_<ID>_v<N>.mp4` dove N parte da 1
- `v1`, `v2`, `v3`... sono iterazioni della stessa scena (mai sovrascrivere v1)
- La versione "approvata" viene linkata simbolicamente come `scene_<ID>_FINAL.mp4`
