# Audio Fetch Plan — Piano esecuzione per Rocco

> Generato da audio-engineer in `STATUS.md` round 1.
> **Pre-requisito**: serve `.env` con `PIXABAY_API_KEY` (e opzionalmente `FREESOUND_API_KEY` per i 3 audio difficili).

---

## Step 0 — API keys (5 minuti, una volta sola)

```bash
# Da terminale, dalla root del repo:
cp .env.example .env
```

Apri `.env` e metti le tue chiavi. Come ottenerle (entrambe gratuite):

**Pixabay API key** (obbligatoria):
1. Crea account su https://pixabay.com/accounts/register/
2. Vai su https://pixabay.com/api/docs/ → la tua chiave è in alto nella pagina
3. Incolla in `.env` come `PIXABAY_API_KEY=abc123...`

**Freesound API key** (opzionale, serve solo per 3 audio difficili):
1. Account su https://freesound.org/home/register/
2. Vai su https://freesound.org/apiv2/apply/ → crea una app, ottieni la chiave
3. Incolla in `.env` come `FREESOUND_API_KEY=xyz789...`

---

## Step 1 — Test rapido che le API funzionino

```bash
python3 scripts/fetch_audio.py --preview
```

Deve elencare i 14 audio target senza errori. Se dice "PIXABAY_API_KEY non trovata" → torna a Step 0.

---

## Step 2 — Esecuzione (in ordine di priorità narrativa)

> Lo script è **interattivo**: ti mostra una tabella di 5 risultati, scegli con 1-5, oppure `preview N` per ottenere l'URL di ascolto, oppure `skip`. **Mai accettare il primo senza ascoltare** — apri sempre la preview di almeno 2 alternative.

### Tier 1 — i 3 WOW critici (fai questi PER PRIMI)

```bash
python3 scripts/fetch_audio.py --id 03_thunderstorm     # WOW 1 — tempesta
python3 scripts/fetch_audio.py --id 05_island_appears   # WOW 2 — isola misteriosa
python3 scripts/fetch_audio.py --id 08_compass_shimmer  # WOW 3 — bussola che si accende (CRITICO)
```

**08_compass_shimmer è il più difficile**. Se Pixabay non ti convince, forza Freesound:
```bash
python3 scripts/fetch_audio.py --id 08_compass_shimmer --source freesound
```

### Tier 2 — gli ambient continui (sottofondo)

```bash
python3 scripts/fetch_audio.py --id 01_ocean_dawn
python3 scripts/fetch_audio.py --id 04_calm_after
python3 scripts/fetch_audio.py --id 09_revelation
python3 scripts/fetch_audio.py --id 13_realistic_intro
python3 scripts/fetch_audio.py --id 23_end_pulse
```

### Tier 3 — gli ambient di scena (riempitivi)

```bash
python3 scripts/fetch_audio.py --id 02_deck_work
python3 scripts/fetch_audio.py --id 06_rowing
python3 scripts/fetch_audio.py --id 07_sand_shift
python3 scripts/fetch_audio.py --id 10_returning
python3 scripts/fetch_audio.py --id 11_sails_wind
python3 scripts/fetch_audio.py --id 12_transition_pad
```

### Tier 4 — la musica (2 tracce, Pixabay Music)

```bash
python3 scripts/fetch_music.py --id main_theme
python3 scripts/fetch_music.py --id outro
```

---

## Audio probabilmente su Freesound (Pixabay scarso)

Questi 3 hanno alta probabilità di non trovare nulla su Pixabay:

| ID | Perché | Comando |
|---|---|---|
| **07_sand_shift** | "sabbia granulare" è troppo specifico per Pixabay | `python3 scripts/fetch_audio.py --id 07_sand_shift --source freesound` |
| **08_compass_shimmer** | shimmer magici/cristallini sono nicchia Freesound | `python3 scripts/fetch_audio.py --id 08_compass_shimmer --source freesound` |
| **23_end_pulse** | "warm pulse" è raro su Pixabay | `python3 scripts/fetch_audio.py --id 23_end_pulse --source freesound` |

**Attenzione attribuzione**: se scarichi da Freesound CC-BY, lo script aggiunge in automatico la riga in `deck/assets/audio/ATTRIBUTIONS.md`. **Verifica** che ci sia. Se l'autore non è citato, contatta l'audio-engineer per fix manuale.

---

## Query migliorate in questo round (vs versione iniziale)

| ID | Before | After | Motivo |
|---|---|---|---|
| `05_island_appears` | "mystery atmosphere drone ambient **mysterious**" | "**deep low drone foreboding ambient**" | rimossa ridondanza |
| `09_revelation` | "warm resonance sustained ambient **inspirational**" | "**warm cinematic sustained pad**" | "inspirational" portava risultati corporate junk |
| `10_returning` | "rowing return **purposeful** gentle ocean" | "**rowing oars steady wooden boat**" | "purposeful" è astratto, Pixabay non lo capisce |
| `13_realistic_intro` | "modern ambient **corporate uplifting** subtle" | "**minimal ambient calm pad**" | "corporate uplifting" = stock junk |
| `23_end_pulse` | "warm closing pulse ambient **resolution**" | "**warm slow pulse ambient**" | "resolution" astratta |

Le altre 9 query erano già buone (concrete + sensoriali, 3-5 parole).

---

## Checklist post-download (per ogni audio)

- [ ] File esiste in `deck/assets/audio/<nome>.mp3`
- [ ] Dimensione > 50 KB (se è 0-10 KB c'è stato errore download)
- [ ] Aperto in QuickTime/VLC — suono OK
- [ ] Mentalmente: "supporta la scena o distrae?" Se distrae → riprovare con query diversa
- [ ] (Solo Freesound) attribuzione presente in `ATTRIBUTIONS.md`

---

## Note di Mixing (per dopo, deck-builder lo userà)

Volumi target già impostati nel JSON (`volume_db_in_deck`). Da rispettare in `deck/js/transitions.js` quando si scrive l'AudioMixer:

| Tipo | dB |
|---|---|
| Loop ambient continuo (sottofondo) | -14 a -18 |
| Ambient atmosferico (tempesta) | -8 a -12 |
| SFX puntuali (shimmer, tuono) | -6 a -8 |
| Musica main theme | -10 |
| Musica outro | -12 |

La voce di Rocco (live, dal microfono) NON viene mixata nel deck — passa direttamente dalle casse della sala. L'audio del deck deve quindi stare sotto la sua proiezione vocale.

---

## Quanto ti aspetti di metterci

- Step 0 (chiavi): 5 min una volta
- Step 1 (test): 1 min
- Step 2 Tier 1 (3 WOW): 15-20 min (più cura)
- Step 2 Tier 2 (5 ambient continui): 15 min
- Step 2 Tier 3 (6 ambient scena): 15 min
- Step 2 Tier 4 (2 musica): 10 min
- **Totale**: ~60-75 minuti

Se trovi un audio che fa schifo dopo download, **non rifare tutto** — usa il comando singolo con `--id` per ri-scaricare solo quello.
