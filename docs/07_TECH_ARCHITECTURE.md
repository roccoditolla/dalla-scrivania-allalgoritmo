# 07 — Tech Architecture

> Come tutti i pezzi si parlano, in versione 100% free.

---

## Diagramma a blocchi

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            ROCCO (MacBook M5)                            │
│                                                                          │
│  ┌─────────────────┐         ┌──────────────────────┐                   │
│  │  Claude Code    │◄────────┤  Browser (Gemini)    │                   │
│  │  (terminal)     │         │  veo 3.1 fast        │                   │
│  │                 │         │  nano banana pro     │                   │
│  │  REGISTA        │         │  manuale, 3/giorno   │                   │
│  └────────┬────────┘         └──────────┬───────────┘                   │
│           │                              │                              │
│           │ orchestra                    │ scarica MP4/PNG              │
│           ▼                              ▼                              │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                  Project: dalla-scrivania-allalgoritmo/         │    │
│  │                                                                  │    │
│  │  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐     │    │
│  │  │ docs/       │  │ prompts/     │  │ deck/              │     │    │
│  │  │ - storyboard│  │ - veo/       │  │ - index.html       │     │    │
│  │  │ - speech    │  │ - audio/     │  │ - css/cinematic    │     │    │
│  │  │ - visual    │  │ - music/     │  │ - js/transitions   │     │    │
│  │  │ - timeline  │  └──────────────┘  │ - assets/          │     │    │
│  │  └─────────────┘                    │   videos/ (Veo)    │     │    │
│  │                                     │   audio/ (Pixabay) │     │    │
│  │  ┌─────────────┐  ┌──────────────┐  │   images/ (NB Pro) │     │    │
│  │  │ scripts/    │  │ .claude/     │  └────────────────────┘     │    │
│  │  │ - export    │  │ skills/      │                              │    │
│  │  │ - fetch_aud │  │ - 5 custom   │  ┌────────────────────┐     │    │
│  │  │ - fetch_mus │  └──────────────┘  │ outputs/           │     │    │
│  │  │ - assemble  │                    │ - backup_video.mp4 │     │    │
│  │  │ - render    │                    │ - veo_prompts.md   │     │    │
│  │  └─────────────┘                    └────────────────────┘     │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │ via HTTPS API
                                   ▼
                  ┌────────────────────────────────┐
                  │  External services (free APIs) │
                  │                                 │
                  │  • Pixabay     (SFX + Music)   │
                  │  • Freesound   (SFX fallback)  │
                  └────────────────────────────────┘
```

## Flussi principali

### Flusso 1 — Generazione di una scena Veo

```
Rocco → "Lavoriamo alla scena 8" 
   ↓
Claude Code legge prompts/veo/scene_08a_*.json + 00_style_bible.md
   ↓
Claude Code invoca skill veo-cinematic-prompt
   ↓
Claude Code esporta il prompt finale (testo formattato per Gemini)
   ↓
Rocco apre Gemini app, seleziona Veo 3.1 Fast
   ↓
Rocco incolla il prompt, attende ~60s
   ↓
Rocco scarica l'MP4
   ↓
Rocco rinomina in scene_08a_FINAL.mp4 e lo sposta in deck/assets/videos/
   ↓
Rocco → "Ho la scena 8 in cartella"
   ↓
Claude Code aggiorna prompts/veo/README.md (status: approved)
```

### Flusso 2 — Sourcing di un audio

```
Rocco → "Cerca l'audio per la tempesta"
   ↓
Claude Code legge prompts/audio/audio_search.json (entry 03_thunderstorm)
   ↓
Claude Code invoca skill audio-sourcing
   ↓
Claude Code esegue python scripts/fetch_audio.py --id 03_thunderstorm
   ↓
Script chiama API Pixabay con query "thunderstorm heavy rain dramatic"
   ↓
Script mostra tabella top 5 risultati
   ↓
Rocco ascolta (usando preview URLs) e sceglie #3
   ↓
Script scarica MP3 in deck/assets/audio/ambient_03_thunderstorm.mp3
   ↓
Claude Code aggiorna log e propone next step
```

### Flusso 3 — Assemblaggio deck

```
Rocco → "Aggiorna il deck con gli ultimi asset"
   ↓
Claude Code invoca skill reveal-cinematic-deck
   ↓
Claude Code esegue python scripts/assemble_deck.py
   ↓
Script scansiona:
   - deck/assets/videos/ → trova FINAL.mp4 per ogni scena
   - deck/assets/audio/ → trova ambient_NN.mp3 per ogni scena
   - deck/assets/images/ → trova realistic_NN.png per ogni slide
   - docs/04_SPEECH_SCRIPT.md → estrae le notes per ogni slide
   ↓
Script genera deck/index.html con:
   - Asset presenti = slide pronte
   - Asset mancanti = slide placeholder con warning visibile
   ↓
Claude Code mostra report: "23 slide, 0 mancanti, deck pronto"
```

## Stack tecnico dettagliato

### Frontend deck (reveal.js)

| Libreria | Versione | Come si carica | Perché |
|---|---|---|---|
| reveal.js | 5.1.0 | CDN jsdelivr | Standard de facto per presentazioni HTML |
| GSAP | 3.12.5 | CDN jsdelivr | Animazioni delle slide realistic |
| Inter font | latest | rsms.me/inter | Tipografia coerente Mac/proiettore |
| Custom CSS | locale | deck/css/cinematic.css | Palette + layout custom |
| Custom JS | locale | deck/js/transitions.js | AudioMixer + bridge arancione |

**Niente bundler, niente build step.** Apri `index.html` e funziona.

### Backend Python (scripts)

| Script | Cosa fa | Dipendenze critiche |
|---|---|---|
| `export_veo_prompts.py` | Crea markdown con prompt copy-paste per Gemini | rich (output) |
| `fetch_audio.py` | API Pixabay + Freesound, download MP3 | requests, dotenv |
| `fetch_music.py` | API Pixabay Music | requests, dotenv |
| `assemble_deck.py` | Genera deck/index.html da template | nessuna esterna (stdlib) |
| `render_backup_video.py` | Concatena video + slide statiche in MP4 4K | ffmpeg (binary di sistema) |

### Sicurezza API keys

In `.env` (mai committato, già in `.gitignore`):
- `PIXABAY_API_KEY` — free, illimitata, no rate limit aggressivo
- `FREESOUND_API_KEY` — free, 60 req/min default

Entrambe sono "leggibili dal server" ma non sensibili (sono **read API keys**, non scrivono nulla, non hanno accesso a account o pagamenti).

## Performance budget

| Asset | Dimensione tipica | Note |
|---|---|---|
| 1 video Veo 3.1 Fast 8s | 3-8 MB (MP4 H.264 1080p) | 17 video × 5 MB ≈ 85 MB totali |
| 1 ambient MP3 (Pixabay) | 200-500 KB | 14 × 350 KB ≈ 5 MB |
| 2 musiche (Pixabay Music) | 1-3 MB ciascuna | 6 MB totali |
| 1 illustrazione PNG (Nano Banana) | 200-800 KB | 11 × 500 KB ≈ 5.5 MB |
| Backup MP4 finale 4K | 1.5-3 GB | non in repo, solo locale |

**Totale repo + asset ≈ 100 MB.** Si carica/scarica in ~30s da fibra.

## Compatibilità

- **macOS**: target primario (Rocco usa MacBook Pro M5)
- **Browser**: Chrome / Safari (testato), Firefox (probabilmente OK)
- **Proiettore**: 1920×1080 minimo, 4K se disponibile
- **Audio**: jack stereo dal MacBook al mixer dell'evento

## Path di degradazione (cosa succede se qualcosa si rompe)

1. **Veo offline / quota finita** → backup MP4 (pre-renderizzato in giorno 5)
2. **Browser crasha durante presentazione** → laptop secondario con MP4 in VLC, switch HDMI
3. **Audio non si sente** → Rocco recita più drammaticamente, la storia regge anche senza ambient
4. **Slide realistic mancante** → Rocco la racconta a voce, salta avanti
5. **Tutto crasha** → Rocco ha studiato lo speech, può farla parlata senza supporto

Dettagli in `docs/08_BACKUP_PLAN.md`.
