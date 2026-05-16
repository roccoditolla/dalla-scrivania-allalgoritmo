---
name: audio-sourcing
description: Searches, evaluates, and downloads royalty-free SFX, ambient sounds, and music from Pixabay (primary) and Freesound (fallback, CC0/CC-BY filter) for the "Dalla Scrivania all'Algoritmo" presentation. Use this skill whenever the user wants to find audio for a specific scene, refine search queries because the first results were poor, propose alternative search terms, balance audio levels in the deck, write attribution notes for Freesound CC-BY downloads, or orchestrate the complete sound design of the story. Invoke for anything touching prompts/audio/*, prompts/music/*, scripts/fetch_audio.py, scripts/fetch_music.py, or deck/assets/audio/.
---

# Audio Sourcing — Skill

## Cosa fa questa skill

Cura il sound design del progetto a costo zero, usando solo libraries royalty-free:
- **Pixabay API** (primario): licenza permissiva, commerciale, no attribuzione
- **Freesound API** (fallback): filtro CC0 e CC-BY, attribuzione automatica gestita

Garantisce che ogni file audio:
1. Supporti la narrazione senza coprire la voce di Rocco
2. Rispetti il sound design in `docs/05_VISUAL_GUIDE.md`
3. Sia licenziato in modo sicuro per uso commerciale
4. Sia mixato correttamente nel deck

## Quando si attiva

- "Cerca l'audio per la scena X"
- "Il suono della tempesta che abbiamo scaricato fa schifo, cerchiamone un altro"
- "Devo trovare un ambient per le slide realistic"
- "Sistema il volume dell'audio nella scena 8"
- "Cerca la musica main_theme"
- "Genera le note di attribuzione per i suoni Freesound che abbiamo usato"
- L'utente apre o modifica `prompts/audio/audio_search.json` o `prompts/music/music_search.json`

## Workflow per ogni audio

### Step 1 — Capire cosa serve

Leggere in ordine:
1. `prompts/audio/audio_search.json` per l'entry specifica (es. `08_compass_shimmer`)
2. `docs/02_STORYBOARD.md` per il contesto narrativo
3. `docs/05_VISUAL_GUIDE.md` sezione "Sound Design" per le linee guida

### Step 2 — Strategia di ricerca

**Pixabay è il primo tentativo, sempre.** Motivi:
- Licenza Pixabay = commerciale + no attribuzione = zero hassle
- API illimitata, veloce
- Cataloghi enormi su ambient, cinematic, sound design

**Freesound entra solo se Pixabay non trova nulla di buono.** Per cosa:
- Suoni molto specifici (es. shimmer cristallino, chime mistico, foley dettagliato)
- Suoni di nicchia che Pixabay non ha
- Filtri severi: solo `Creative Commons 0` o `Attribution`

### Step 3 — Costruire le query

Le query Pixabay sono **brevi e visive**. Tipo:
- ✅ `"ocean waves dawn calm"`
- ✅ `"thunderstorm heavy rain dramatic"`
- ✅ `"magical shimmer ethereal chime"`
- ❌ `"sound that feels like the awakening of artificial intelligence"` (troppo astratto)
- ❌ `"epic"` (troppo generico)

**Regole:**
- 3-5 parole max
- Combinare sostantivi concreti (mare, vento) + aggettivi sensoriali (caldo, drammatico)
- Mai genere musicale come query SFX (es. non "jazz piano" se cerchiamo ambient)

### Step 4 — Eseguire la ricerca

Comando standard:
```bash
python scripts/fetch_audio.py --id 08_compass_shimmer
```

Lo script mostra una tabella con i top 5 risultati ordinati per popolarità. **Mai accettare il primo automaticamente.** Verificare:
- Durata coerente con `min_duration`/`max_duration` nel JSON
- Anteprima ascoltata da Rocco (usare `preview N`)
- Se Pixabay è povero, lo script fa già fallback su Freesound

### Step 5 — Validare la scelta con Rocco

Mai scaricare in silenzio. Anche per audio "minori":
- Dire a Rocco: "Trovati 5 risultati Pixabay per 08_compass_shimmer. Ti propongo il #2 (Magical Shimmer, 4.2s, 1200 download). Vuoi un'altra opzione?"
- Aspettare la conferma

### Step 6 — Post-download

Se il file viene da Freesound CC-BY:
- Lo script aggiunge automaticamente l'attribuzione in `deck/assets/audio/ATTRIBUTIONS.md`
- Verificare che sia leggibile e completa
- Pixabay non richiede attribuzione, salta questo step

### Step 7 — Test in contesto

Una volta scaricato, **NON** considerarlo finito. Verificare:
- Apri il MP3 in QuickTime o VLC
- Ascolta con cuffie + casse
- Mentalmente: "se questo suona durante la scena, mi distrae o supporta la storia?"
- Se distrae: tornare allo step 3 con query diverse

## Mixing nel deck

I file audio vengono caricati nel deck reveal.js (`deck/js/transitions.js`). I volumi target (vedi `audio_search.json` campo `volume_db_in_deck`):

| Tipo | Volume target | Note |
|---|---|---|
| Audio nativo Veo (in MP4) | -3 dB | gestito da Veo, non toccare |
| Ambient sottofondo continuo | -14 a -18 dB | quasi subliminale |
| Ambient atmosferico (es. tempesta) | -8 a -12 dB | più presente, ma sotto la voce |
| SFX puntuali (shimmer, tuono) | -6 a -8 dB | brevi picchi |
| Musica (main theme) | -10 dB | sopra ambient, sotto voce |
| Musica outro | -12 dB | risolutiva ma calma |

Quando si modifica `volume_db_in_deck` nel JSON, **aggiornare anche** `deck/js/transitions.js` sezione `AudioMixer` se necessario.

## Differenze rispetto a ElevenLabs (vecchio piano)

| Aspetto | ElevenLabs SFX V2 (vecchio) | Pixabay/Freesound (nuovo) |
|---|---|---|
| Costo | $5-22/mese | 0€ |
| Generazione | testo → audio sintetico | ricerca → libreria umana |
| Specificità | esatta (descrivi e generi) | dipende dal catalogo |
| Velocità | 30s per audio | 5s ricerca + download |
| Licenza | inclusa nel piano | Pixabay License + CC |
| Workflow Claude Code | API automatica | API ricerca + scelta umana |

**Conseguenza pratica:** invece di scrivere prompt cinematici per ogni suono, scriviamo **search queries** efficaci e validiamo i risultati. Più simile a Google Images che a ChatGPT.

## Errori comuni

| Errore | Conseguenza | Fix |
|---|---|---|
| Query troppo astratta | 0 risultati o risultati inutili | Riformulare con parole concrete e sensoriali |
| Accettare il primo risultato sempre | Audio mediocre | Forzare l'ascolto di almeno 3 alternative |
| Volume troppo alto in deck | Copre la voce di Rocco | Rispetta i dB target |
| Audio Freesound senza attribuzione | Possibile violazione CC-BY | Lo script gestisce automaticamente, verificare che ATTRIBUTIONS.md esista |
| Loop file non seamless | Click udibile alla ripetizione | Cercare nelle metadata "seamless loop" o tagliare con ffmpeg |

## Per la musica (Pixabay Music)

Workflow simile ma con `scripts/fetch_music.py`. Brief più descrittivi (mood + stile + strumentazione). Riferimenti compositivi accettati (es. "olafur arnalds inspired").

Le due tracce attuali in `prompts/music/music_search.json`:
- `main_theme`: entra nella scena 9, peak in 11, fade out in 12
- `outro`: slide finale 23, loop fino ad applauso

Mai due tracce diverse nella stessa fase. Mai musica con lyrics. Mai musica con drums (rompe il mood).

## Tip avanzato: combinare layer

Per scene complesse (es. scena 3 tempesta), si possono usare **più audio insieme** stratificati nel deck:
- Layer A: ambient ufficiale (ambient_03_thunderstorm.mp3) a -8 dB
- Layer B: SFX one-shot puntuale (es. sfx_03_lightning_crack.mp3) a -3 dB sincrono al lampo

Questo si fa nel JavaScript del deck (`transitions.js`), non in fase di sourcing. Ma in `audio_search.json` possiamo dichiarare entrambi i layer come entry separate e scaricarli entrambi.

## Output finale di ogni invocazione

Dopo ogni audio scaricato/scelto, riportare:

```
Audio: [id]
Sorgente: pixabay | freesound
Nome trovato: [name]
Durata: [Xs]
Volume target deck: [Y dB]
File salvato: deck/assets/audio/[filename]
Attribuzione: nessuna (Pixabay) | aggiunta in ATTRIBUTIONS.md (Freesound)
Prossimo passo: [download successivo / test in deck / niente]
```
