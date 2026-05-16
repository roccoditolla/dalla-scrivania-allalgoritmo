# 06 — Production Timeline (5 giorni, metodo BMAD)

> Piano operativo giorno-per-giorno con il nuovo workflow **100% free**.  
> Ogni giorno ha **un solo focus principale**.

---

## Vincoli fissi

- Evento: **giorno 5**, sera
- **Limite Veo 3.1 Fast nel piano Google AI Pro: 3 video al giorno**
  - 5 giorni × 3 = 15 video totali → abbiamo 17 scene da generare
  - Strategia: alcune scene possono essere combinate o sostituite con elementi statici (slide animata via reveal.js anziché video Veo)
- **Costo target: 0€**
- Tempo serale Rocco: ~2 ore/giorno utili al progetto

---

## Giorno 1 — Setup & Validazione stilistica

**Focus:** verificare che lo stile visivo Veo funzioni prima di produrre tutto.

### Mattina (15 min)
- Setup ambiente: clone repo, `pip install`, `npm install`
- Creare API keys Pixabay e Freesound (5 min ciascuna)
- Compilare `.env`

### Pomeriggio (1 ora)
- Avviare Claude Code dalla root del progetto
- Primo prompt: "Leggi CLAUDE.md e i docs, dammi il tuo piano operativo per oggi"
- Claude Code legge tutto e si presenta come regista
- Esportare i prompt Veo del Giorno 1 con `python scripts/export_veo_prompts.py --day 1`
- File generato: `outputs/veo_prompts_for_gemini.md`

### Sera (1.5 ore) — Le 3 scene chiave
**Apri Gemini app, seleziona Veo 3.1 Fast.** Genera in quest'ordine:

1. **Scena 01 — Open Sea** (apertura, validazione stile)
2. **Scena 05 — Isola Appare** (WOW 2, validazione mood misterioso)
3. **Scena 08A — Bussola Si Accende** (WOW 3 critico, validazione arancione)

Per ognuna:
- Copia il prompt dal markdown esportato
- Incolla in Gemini, genera (~60s)
- Scarica MP4
- Rinomina in `scene_XX_FINAL.mp4` (o `_v1.mp4` se non sei sicuro)
- Mettilo in `deck/assets/videos/`

### Decisione di fine giornata 1
Con Rocco + Claude Code, valutare i 3 video:
- Lo stile è coerente con `docs/05_VISUAL_GUIDE.md`?
- L'arancione della scena 8 è giusto (#FF6B1A saturated)?
- I volti sono nascosti come previsto?

**Se SÌ:** procedere con giorno 2.  
**Se NO:** lavorare con Claude Code per rivedere il prompt e rigenerare. Anche a costo di perdere 1 giorno qui, la coerenza stilistica è non negoziabile.

---

## Giorno 2 — Generazione storia (atto I + tempesta)

**Focus:** completare le scene dell'atto I (passato/competenza/tempesta).

### Quota Veo del giorno: 3 video
1. **Scena 02A** — Ciurma sul ponte
2. **Scena 03A** — Tempesta (WOW 1)
3. **Scena 03B** — Capitano nella tempesta

Stesso workflow: prompt → Gemini → scarica → rinomina → metti in `deck/assets/videos/`.

### In parallelo, Claude Code lavora sull'audio
Dopo aver lanciato i 3 video Veo:

```bash
# Da Claude Code, mentre i video si renderizzano:
# "Cerca gli audio per scene 1-5"
```

Claude Code:
- Esegue `python scripts/fetch_audio.py --id 01_ocean_dawn`
- Mostra 5 risultati Pixabay
- Tu scegli ascoltando l'anteprima
- Salva in `deck/assets/audio/`

Ripeti per: `02_deck_work`, `03_thunderstorm`, `04_calm_after`, `05_island_appears`.

### Sera: speech check
Da Claude Code: "Rivedi lo speech per le scene 1-5 con la skill `speech-writer-italian`. Verifica il timing (123 wpm target)."

---

## Giorno 3 — Generazione storia (atto II + III)

**Focus:** scene dell'isola e della bussola.

### Quota Veo del giorno: 3 video — le scene contemplative
1. **Scena 04** — Mare calmo dopo (riflessione)
2. **Scena 06** — Sbarco (primo accenno arancione)
3. **Scena 07** — Mano sulla sabbia (setup WOW 3)

### Quota Veo "extra" da recuperare (3 video con bonus): le scene difficili
Se Rocco riesce a salire al giorno 2 con scene "facili" senza usare tutti i 3 slot, può tenere 1-2 in riserva qui.

Scene del giorno 3, parte 2:
4. **Scena 08B** — Ago della bussola che ruota
5. **Scena 09A** — Cerchio attorno alla bussola
6. **Scena 09B** — Ago si ferma

⚠️ **Se la quota si esaurisce**: rimandare 09B al giorno 4. Mai forzare.

### In parallelo, audio per scene 6-9
```bash
python scripts/fetch_audio.py --id 06_rowing
python scripts/fetch_audio.py --id 07_sand_shift
python scripts/fetch_audio.py --id 08_compass_shimmer   # ⭐ critico
python scripts/fetch_audio.py --id 09_revelation
```

### Sera: musica
```bash
python scripts/fetch_music.py --id main_theme
python scripts/fetch_music.py --id outro
```

Claude Code mostra 5 opzioni per ogni brief. Tu ascolti e scegli quella con il mood giusto (cinematic, contemplativo, MAI corporate).

---

## Giorno 4 — Storia (finale) + slide realistic + deck

**Focus:** chiudere la storia, generare le slide realistic, assemblare il deck.

### Quota Veo del giorno: 3 video — il finale
1. **Scena 10** — Ritorno alla nave
2. **Scena 11A** — Nave salpa
3. **Scena 11B** — Due bussole sul ponte

Eventualmente al posto della 11A se la 11B viene complicata, oppure rimandare 11B a domani.

⏳ **Scena 12 (transizione)**: questa è difficile per Veo. Strategia alternativa: NON usare Veo per la 12. Invece:
- Generare in **Nano Banana Pro** una immagine fissa con la bussola arancione su sfondo che si trasforma da nave a moderno
- Animarla in CSS/GSAP nel deck (fade dissolve di 2s)
- Risparmia 1 slot Veo per recuperi

### Pomeriggio: slide realistic (11 immagini)
Da Gemini app, switch a **Nano Banana Pro**. Genera in batch le 11 illustrazioni per le slide 13-23.

Prompt template (Claude Code te li scrive):
```
Minimal isometric illustration, cream background #F5EFE6, 
single orange accent #FF6B1A only on the key element.
Style: editorial, modern, clean line-art. No text.
Subject: [contenuto specifico slide N].
```

Salva tutte le PNG in `deck/assets/images/realistic_NN_descrittore.png`.

### Sera: assemblaggio deck
```bash
python scripts/assemble_deck.py
```

Genera `deck/index.html` con tutti i video, audio, illustrazioni che ci sono. Quelle che mancano hanno placeholder visibili.

Test:
```bash
npx serve deck/ -l 8000
open http://localhost:8000
```

Naviga le 24 slide (0-23). Tutto a posto?

---

## Giorno 5 — Backup MP4, test, evento

**Mattina:** controllo finale di ogni asset, ascolto integrale.

```bash
# Eventuali audio mancanti (dimenticati):
python scripts/fetch_audio.py --all   # scarica tutto quello che manca

# Eventuali scene Veo da rigenerare se ne avanza:
# (massimo 3 oggi, sii selettivo)

# Backup MP4
python scripts/render_backup_video.py
```

Verifica `outputs/backup_video.mp4`:
- Apri in QuickTime e guardalo TUTTO dall'inizio alla fine
- Se ci sono buchi: scena per scena, vedi quale asset manca

**Pomeriggio:** test in sala (se possibile), seguire `tests/stage_test_checklist.md`.

**Sera:** evento. 🎬

---

## Riepilogo costi (sanity check)

| Voce | Costo |
|---|---|
| Veo 3.1 Fast (15-17 generazioni) | 0€ (incluso nel piano Google AI Pro che paghi già) |
| Nano Banana Pro (11 immagini) | 0€ (idem) |
| Pixabay API (14 SFX/ambient + 2 musiche) | 0€ |
| Freesound fallback (eventuale) | 0€ |
| Reveal.js + GSAP via CDN | 0€ |
| ffmpeg | 0€ |
| Claude Code | 0€ (Pro abbonamento esistente) |
| **TOTALE EXTRA** | **0€** |

Sotto i 20€ richiesti con margine totale.

---

## Cosa fare se qualcosa va male

- **Veo genera scene brutte ripetutamente**: cambia prompt con Claude Code (`veo-cinematic-prompt` skill), prova varianti
- **Quota Veo finita**: aspetti mezzanotte Pacific Time (in Italia mattina presto)
- **Pixabay non trova audio adatto**: lo script fa automaticamente fallback a Freesound CC0
- **Una scena è impossibile**: sostituiscila con una slide statica + GSAP (vedi Plan B in `docs/08_BACKUP_PLAN.md`)
- **Deck crasha sul palco**: hai il backup MP4 in 2 USB + laptop di backup pronto
