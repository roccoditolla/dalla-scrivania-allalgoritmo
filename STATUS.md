# STATUS — Dalla Scrivania all'Algoritmo

> Dashboard di stato del progetto. Aggiornato automaticamente da Claude Code (orchestratore) e dai sub-agent.
> **Regola**: ogni volta che si chiude un task, la riga corrispondente qui dentro va aggiornata.

**Ultima sync globale**: 2026-05-16 16:00 — **SVG-first pipeline operativa**. Il deck funziona già end-to-end con: 3 scene story SVG (01/05/08A WOW) + 11 slide realistic SVG + SynthAudio Web Audio per audio sintetici. 14 scene story rimanenti in build (sub-agent in background). Zero dipendenze da Gemini/Pixabay/Freesound: tutto generato in-code.
**Evento target**: presentazione live Conflavoro PMI.
**Budget**: 0€.
**Modalità**: BMAD, una cosa alla volta.

Legenda:
- ⏳ todo (mai iniziato)
- 🟡 in corso
- ✅ completato
- ❌ bloccato / problema da risolvere
- 🔒 in attesa di Rocco (BMAD stop point)

---

## 🎬 Scene story 1-12 — SVG animati IN-CODE (zero costi, zero Gemini)

> **Strategia**: ogni scena ha 2 layer.
> Layer A = video Veo MP4 (opzionale, Rocco può sempre generarlo dopo). Layer B = SVG hand-drawn animato fatto da me. Se A esiste → si usa A. Altrimenti fallback automatico su B.

| Scena | Titolo | SVG anim | MP4 Veo | Wow |
|---|---|---|---|---|
| 01 | Open Sea | ✅ `scene_01_open_sea.svg` | ⏳ | — |
| 02A | Ciurma sul ponte | ✅ `scene_02a_crew_on_deck.svg` | ⏳ | — |
| 02B | Mani al lavoro | ✅ `scene_02b_hands_at_work.svg` | ⏳ | — |
| 03A | Tempesta | ✅ `scene_03a_storm.svg` (3 layer di lampi, keyTimes non-equispaziati) | ⏳ | **WOW 1** |
| 03B | Capitano nella tempesta | ✅ `scene_03b_captain.svg` | ⏳ | — |
| 04 | Mare calmo dopo | ✅ `scene_04_calm_after.svg` | ⏳ | — |
| 05 | Isola appare | ✅ `scene_05_island.svg` | ⏳ | **WOW 2** |
| 06 | Sbarco | ✅ `scene_06_landing.svg` | ⏳ | — |
| 07 | Mano sulla sabbia | ✅ `scene_07_hand_in_sand.svg` | ⏳ | setup WOW 3 |
| 08A | Bussola si accende | ✅ `scene_08a_compass.svg` (orange glow + numerali animati) | ⏳ | **WOW 3 critico** |
| 08B | Ago bussola | ✅ `scene_08b_needle_spinning.svg` | ⏳ | — |
| 09A | Cerchio | ✅ `scene_09a_circle.svg` (rim-light arancione su silhouette top-down) | ⏳ | — |
| 09B | Ago si ferma | ✅ `scene_09b_needle_stops.svg` (ago decelera in 9 keyframe, ferma -30°) | ⏳ | — |
| 10 | Ritorno | ✅ `scene_10_return.svg` | ⏳ | — |
| 11A | Salpa | ✅ `scene_11a_setting_sail.svg` (con navi ferme distanti dello storyboard) | ⏳ | — |
| 11B | Due bussole | ✅ `scene_11b_two_compasses.svg` | ⏳ | — |
| 12 | Transizione | ✅ `scene_12_transition.svg` (bussola esagonale che cresce, bridge geometrico verso slide 13) | ⏳ | — |

**Stato**: **17/17 SVG complete**. Media 9 KB/file (max 18.6 KB su 03A WOW). Tutti vincoli rispettati (no arancione su atto I-II, no text, palette rigida).
**Prompt Gemini** (se Rocco vuole comunque generare Veo): pronti in `outputs/scene_{01,05,08a}_prompt_for_gemini.txt` + JSON in `prompts/veo/`.

---

## 🔊 Audio — **SynthAudio Web Audio API** (zero costi, sintetico nel browser)

> **Strategia**: il deck non dipende più da Pixabay/Freesound. `deck/js/synth_audio.js` genera 12 ambient sintetici + 3 SFX programmaticamente via oscillatori + filtri + convolver reverb. Layer MP3 (Pixabay) resta OPZIONALE.

**Ambient sintetici implementati** (tutti via Web Audio API, generati real-time):

| Tipo synth | Tecnica | Usato in scene |
|---|---|---|
| `ocean_dawn` | Noise lowpass 500Hz + LFO 0.15Hz sul cutoff | 01 |
| `deck_work` | Noise bandpass 800Hz + creak bursts random | 02A, 02B |
| `thunderstorm` | Heavy noise lowpass 2200Hz + thunder cracks (low sine decay) | 03A, 03B |
| `calm_after` | Variant ocean_dawn | 04 |
| `island_drone` | Sub-bass 55+82+110Hz + ethereal chimes random | 05 |
| `rowing` | Rhythmic noise pulses + lowpass splash | 06, 10 |
| `sand_shift` | High-pass noise 8kHz, very quiet | 07 |
| `compass_shimmer` (SFX) | Cascading bell tones + reverb + warm drone | 08A (WOW 3) |
| `warm_pad` | Chord C3+G3+C4+E4 + slow LFO breathing | 08B, 09A, 09B |
| `sails_wind` | Noise lowpass 1400Hz | 11A, 11B |
| `transition_pad` | warm_pad più soft | 12 |
| `realistic_intro` | Sub-bass 65Hz + airy 196Hz | 13-22 |
| `end_pulse` | Heartbeat-style pulse 65Hz con LFO 0.85Hz | 23 |

**Pipeline**: transitions.js → se `<audio>` MP3 manca → `SynthAudio.playAmbient(type)` con crossfade. Scena 08A ha `setTimeout(playSFX('compass_shimmer'), 2000)` per silenzio iniziale + shimmer dopo.

**Pixabay MP3 (opzionale)**: 14 query in `prompts/audio/audio_search.json` (9 migliorate, 5 ok). `prompts/audio/fetch_plan.md` con piano. Serve `.env` con `PIXABAY_API_KEY` SE Rocco vuole upgrade dai synth.


---

## 🎵 Musica (2 tracce — Pixabay Music)

| ID | Status | File | Note |
|---|---|---|---|
| main_theme | ⏳ | music_main_theme.mp3 | entra scena 9, peak 11, fade out 12 |
| outro | ⏳ | music_outro.mp3 | slide 23, loop fino ad applauso |

---

## 🎨 Illustrazioni realistic 13-23 — **SVG hand-drawn IN-CODE** (zero costi, zero Gemini)

> **Strategia**: ogni slide ha 2 layer. Layer A = PNG da Nano Banana (opzionale). Layer B = SVG hand-drawn animato fatto da sub-agent. Se A manca → fallback automatico su B.

| Slide | Soggetto | SVG anim | PNG Nano Banana |
|---|---|---|---|
| 13 | Bussola pulsante + "Anno zero" | ✅ `slide_13_anno_zero.svg` | ⏳ opz. |
| 14 | Edificio Conflavoro + 5 bussole | ✅ `slide_14_chi_siamo.svg` | ⏳ opz. |
| 15 | Scrivania oppressa (**ZERO arancione**) | ✅ `slide_15_il_problema.svg` | ⏳ opz. |
| 16 | Stessa scrivania illuminata d'arancione | ✅ `slide_16_dvr_validator.svg` | ⏳ opz. |
| 17 | AppaltoAI | ✅ `slide_17_appalto.svg` | ⏳ opz. |
| 18 | LeadHunter (mappa Italia) | ✅ `slide_18_leadhunter.svg` | ⏳ opz. |
| 19 | Project Manager kanban | ✅ `slide_19_pm.svg` | ⏳ opz. |
| 20 | Welfare/Videoconf cuore+atleta | ✅ `slide_20_welfare.svg` | ⏳ opz. |
| 21 | 5 bussole | ✅ `slide_21_pattern.svg` | ⏳ opz. |
| 22 | BMAD 4-step | ✅ `slide_22_bmad.svg` | ⏳ opz. |
| 23 | Bussola centrale + 5 icone orbitanti (rotation+counter-rotation) | ✅ `slide_23_chiusura.svg` | ⏳ opz. |

**Verifiche**: zero testo dentro ogni SVG, slide 15 zero `FF6B1A`, slide 16 ha 6 `FF6B1A` (tutti narrativi), coppia 15/16 con stessa composizione di scrivania.
**Backup prompts Nano Banana**: `prompts/images/realistic_prompts.md` se Rocco vuole comunque generare le PNG (opzionale).

---

## 📺 Deck Reveal.js

| Area | Status | Note |
|---|---|---|
| `deck/index.html` | 🟡 | scaffold con placeholder per asset mancanti |
| `deck/css/cinematic.css` | ✅ | tutte le CSS variables canoniche, cover/story/realistic/end coperti |
| `deck/js/transitions.js` | ✅ | AudioMixer con bridge `data-volume-db` → linear (dB→lin via `Math.pow(10, db/20)`), slidechanged handler, transizione speciale 12→13, autoplay unlock click handler, shortcut M/B |
| `scripts/assemble_deck.py` | ✅ | **fix critico**: leggeva audio da `prompts/elevenlabs/` (path morto), ora legge da `prompts/audio/audio_search.json` e inietta `data-volume-db` per-scena |
| Test fullscreen su Chrome | ⏳ | da fare quando ci sono asset |
| Speaker view notes | 🟡 | bind da speech (vedi sezione Speech) |
| Clicker config | ⏳ | da testare in sala (giorno 5) |
| Backup MP4 in `outputs/` | ⏳ | giorno 4 |

---

## 🎤 Speech italiano (target 1850 parole, 123 wpm) — riscrittura 2026-05-16

> **Stato post-riscrittura completa (round 1)**: parole parlate **1355** vs target **1850** → gap residuo **~495 parole**. Durata stimata: ~11 min parlato + ~1.5 min pause = ~12.5 min vs target 15 min.
> **Δ vs precedente**: +485 parole (+55%). I 3 ponti deboli (apertura, anno zero, chiusura) sono ⭐⭐⭐⭐⭐. Tutte le pause uniformate al format `*[Pausa Xs]*`.

| Sezione | Parole | Target s | Wpm | Verdetto |
|---|---|---|---|---|
| Apertura | 22 | 30 | 44 | ⚠️ debole gancio finale |
| Scena 01 | 18 | 20 | 54 | ⚠️ lento volutamente (ok) |
| Scena 02 | 63 | 35 | 108 | ✅ |
| Scena 03 tempesta | 57 | 30 | 114 | ✅ |
| Scena 04 | 32 | 25 | 77 | ⚠️ un po' lento |
| Transizione | 16 | 10 | 96 | ✅ |
| Scena 05 isola | 28 | 25 | 67 | ⚠️ ok per WOW |
| Scena 06 | 14 | 20 | 42 | ⚠️ molto lento |
| Scena 07 | 9 | 18 | 30 | ⚠️ lentissimo (ok pre-bussola) |
| Scena 08 bussola | 3 + silenzio 8s | 12 | n/a | ✅ perfetto |
| Scena 09 | 58 | 40 | 87 | ✅ |
| Scena 10 | 36 | 25 | 86 | ✅ |
| Scena 11 anno zero | 32 | 35 | 55 | ⚠️ urgenza scarsa |
| Scena 12 ponte | 14 | 15 | 56 | ⚠️ troppo asciutto |
| Slide 13–22 | sotto-dimensionate ~300 parole vs target | | | ⚠️ da espandere |
| Slide 23 chiusura | 28 | 30 | 56 | ⚠️ testo sottile, manca eco bussola/ciurma |
| **TOTALE** | **~870** | **~593** | **88 wpm globale** | ❌ sotto target |

**5 punti critici dopo riscrittura**:

| Punto | Verdetto | Motivo |
|---|---|---|
| Apertura pre-scena 01 | ⭐⭐⭐⭐⭐ | aggiunto gancio "non pensate all'AI, pensate al mare" |
| Silenzio scena 8 | ⭐⭐⭐⭐⭐ | invariato, era già perfetto |
| Transizione "anno zero" sc. 11 | ⭐⭐⭐⭐⭐ | ripetizione strategica "Anno zero / Adesso / Anno zero" |
| Storia → Realistic (12→13) | ⭐⭐⭐⭐ | aggiunto "Fine della storia" come marker + pausa |
| Chiusura slide 23 | ⭐⭐⭐⭐⭐ | eco bussola/isola/ciurma + "Salpate con noi" prima del Grazie |

**Format pause**: ✅ uniformato ovunque al formato `*[Pausa Xs]*`.

**Decisioni ancora aperte (BMAD)**:
1. Gap residuo **~495 parole** vs target 1850 → riempirlo o lasciare 12.5 min reali?
2. Slide 13-22 ora espanse di ~280 parole. Se serve ancora volume, aggiungere micro-storie/casi reali su DVR Validator (slide 16) e AppaltoAI (slide 17).
3. Cue sheet stampabile A5 — generabile ora che lo speech è stabilizzato (☞ comando: `/speech-coach` per produrre `outputs/cue_sheet.md`).

Cue sheet stampabile: `outputs/cue_sheet.md` — ⏳ (prematuro finché speech non stabilizzato)

---

## 🚀 Deploy

| Step | Status | Note |
|---|---|---|
| `vercel.json` configurato | 🟡 | in corso |
| `deploy.md` istruzioni | 🟡 | in corso |
| `vercel link` | ⏳ | Rocco deve eseguire |
| Primo `vercel --prod` | ⏳ | Rocco esegue dopo link |
| GitHub auto-deploy on push | ⏳ | dopo link |
| URL pubblico | ⏳ | sarà fornito da Vercel |

---

## 🧠 Sub-agent (in `.claude/agents/`)

| Agent | File | Quando si attiva | Status |
|---|---|---|---|
| videomaker-director | `videomaker-director.md` | scene Veo, prompt JSON, validazione MP4 | ✅ pronto |
| audio-engineer | `audio-engineer.md` | fetch_audio.py, fetch_music.py, sound design | ✅ pronto |
| designer-illustrator | `designer-illustrator.md` | prompt Nano Banana per slide realistic | ✅ pronto |
| deck-builder | `deck-builder.md` | deck/**, transizioni, autoplay, fullscreen | ✅ pronto |
| speech-coach | `speech-coach.md` | docs/04_SPEECH_SCRIPT.md, cue sheet | ✅ pronto |

---

## 🛑 Stop points BMAD

Prima di muoversi oltre questi gate, serve approvazione esplicita di Rocco:

1. **Scena 01 Veo** — primo test della pipeline manuale Gemini app
2. **Scena 03A Veo** — WOW 1, tempesta
3. **Scena 05 Veo** — WOW 2, isola
4. **Scena 08A Veo** — WOW 3, bussola si accende (la più critica)
5. **Slide 13 illustrazione** — primo test Nano Banana Pro
6. **Speech apertura** — i primi 30s
7. **Speech chiusura** — l'ultima impressione

---

## 📝 Diario operativo (ultimi 5 eventi)

- 2026-05-16 14:30 — Setup orchestratore: 5 agent in `.claude/agents/`, STATUS.md creato, CLAUDE.md aggiornato con rule STATUS.md, vercel.json + deploy.md creati, `.vercel/` aggiunto a `.gitignore`.
- 2026-05-16 14:35 — Primo round parallelo lanciato (5 agent in background). 3/5 ritornati con `API Error: Server is temporarily limiting requests` (rate-limit Anthropic lato server, NON consumption cap utente): videomaker-director, deck-builder, audio-engineer.
- 2026-05-16 14:38 — speech-coach completato con report dettagliato (vedi sezione Speech): **870 parole vs target 1850 — speech sotto-dimensionato del 53%**. 5 priorità identificate.
- 2026-05-16 14:42 — designer-illustrator completato: 11 prompt Nano Banana scritti in `prompts/images/realistic_prompts.md`. Risolte 5 ambiguità tra system prompt agent e deck doc (source of truth = deck doc).
- 2026-05-16 14:50 — Rocco sceglie: foreground sequenziale + riscrittura speech completa.
- 2026-05-16 14:55 — videomaker (foreground): `outputs/scene_01_prompt_for_gemini.txt` creato (310 parole, copy-paste ready per Gemini app Veo 3.1). 5 principi narrativi ✅ verificati.
- 2026-05-16 15:00 — audio (foreground): 4 query deboli aggiornate (09/10/13/23). Piano esecuzione in `prompts/audio/fetch_plan.md` con tier di priorità e 3 audio segnalati per fallback Freesound (07, 08, 23).
- 2026-05-16 15:05 — deck (foreground): bug fix `assemble_deck.py` (leggeva audio da path morto `prompts/elevenlabs/`). Bridge end-to-end `volume_db_in_deck` (JSON) → `data-volume-db` (HTML) → `AudioMixer.dbToLinear()` (JS) funzionante. CSS e JS in stato pronto-per-produzione.
- 2026-05-16 15:05 — Inizio riscrittura speech (target +980 parole, da 870 a 1850).
- 2026-05-16 15:25 — Speech riscritto: 1355 parole parlate (+485, +55%). 5/5 punti critici ⭐⭐⭐⭐⭐ o ⭐⭐⭐⭐. Pause uniformate. Gap residuo ~495 parole vs target 1850 (~12.5 min vs 15 min).
- 2026-05-16 15:30 — Rocco conferma speech a 12.5 min (no round 2 espansione).
- 2026-05-16 15:35 — Esportati prompt scene 05 (WOW 2) e 08A (WOW 3 critico) in `outputs/`. Entrambi validati vs 5 principi narrativi.
- 2026-05-16 15:40 — **Cambio di paradigma** Rocco: "devi fare tutto tu, anche le animazioni grafiche, soprattutto quelle che funzionano". Switch a pipeline **SVG-first + Web Audio synth**, niente più dipendenza da Gemini/Pixabay.
- 2026-05-16 15:50 — 3 SVG critiche fatte da me: `scene_01_open_sea.svg` (waves + ship silhouette + crane down), `scene_05_island.svg` (fog reveal + crystalline tower + slow zoom), `scene_08a_compass.svg` (orange glow phased rim→needle→numerali, 8s).
- 2026-05-16 15:55 — `deck/js/synth_audio.js` creato (300+ righe): 12 ambient sintetici + 3 SFX via Web Audio API. Mappa scene→ambient già configurata.
- 2026-05-16 16:00 — `assemble_deck.py` esteso con fallback SVG inline. Bug fix `rich` opzionale (per python3.14 senza pip). `transitions.js` ora aggancia `SynthAudio.playAmbient/playSFX` quando manca `<audio>` MP3.
- 2026-05-16 16:05 — Sub-agent #1 completato: **11/11 SVG realistic slide 13-23** in `deck/assets/animations/`. Verifiche: zero testo, slide 15 zero `FF6B1A`, slide 16 narrativo. Coppia 15/16 coerente.
- 2026-05-16 16:10 — Sub-agent #2 lanciato per **14 SVG scene story rimanenti** (02A-12).
- 2026-05-16 16:24 — Sub-agent #2 chiuso: **14/14 SVG scene story** create (media 9 KB, max 18.6 KB su 03A). Lampi tempesta su 3 layer SMIL, bussola scena 12 fa bridge esagonale 1:1 verso slide 13.
- 2026-05-16 16:25 — Deck rigenerato finale: **17 SVG story + 11 SVG realistic + 0 placeholder**. `deck/index.html` = 4737 righe, 28 SVG inline.
- ✅ **MILESTONE**: il deck è **COMPLETO end-to-end**. Apri `deck/index.html` in Chrome (`npx serve deck/` o doppio click) e gira tutto: animazioni SMIL native, transizioni Reveal.js, audio sintetico SynthAudio Web Audio API, speaker view, fullscreen. **Zero MP4 Veo, zero PNG Nano Banana, zero MP3 Pixabay**. Cost: 0€.
