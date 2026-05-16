# Dalla Scrivania all'Algoritmo

> Presentazione cinematic live di 15 min per evento Conflavoro PMI.  
> 10 min storia animata (Veo 3.1 Fast) + 5 min slide realistic.  
> Speaker: Rocco Di Tolla — Eleven Digital and AI Consulting.

## Strategia: 100% Free + Claude Code come regista

Tutta la produzione è a **costo zero**, sfruttando solo strumenti gratuiti o già inclusi nel piano Google AI Pro (49€/mese) che Rocco già paga.

| Componente | Strumento | Costo |
|---|---|---|
| Video storia (17 clip) | **Veo 3.1 Fast** via Gemini app (manuale) | 0€ — incluso nel Pro |
| Illustrazioni slide realistic (11) | **Nano Banana Pro** via Gemini app | 0€ — incluso nel Pro |
| Ambient + SFX (14 elementi) | **Pixabay API** (royalty-free, no attribuzione) | 0€ |
| Fallback SFX rari | **Freesound API** (filtro CC0/CC-BY) | 0€ |
| Musica (2 tracce) | **Pixabay Music** | 0€ |
| Speech italiano (1850 parole) | Claude Code | 0€ |
| Deck cinematic | Reveal.js + GSAP | 0€ |
| Backup MP4 | ffmpeg | 0€ |
| **TOTALE** | | **0€** |

## Il ruolo di Claude Code

Claude Code è il **regista umano** del progetto. Orchestrando tutto da terminale:

1. **Scrive e raffina i prompt Veo** scena per scena, secondo i 5 principi narrativi della skill `storyboard-architect`
2. **Esporta i prompt** pronti da incollare in Gemini app (Rocco fa il click manuale)
3. **Cerca, scarica e cura l'audio** automaticamente da Pixabay/Freesound API
4. **Genera le illustrazioni realistic** (Rocco le fa in Nano Banana, Claude scrive i prompt)
5. **Assembla il deck reveal.js** automaticamente dai prompt e dagli asset
6. **Renderizza il backup MP4** con ffmpeg

Rocco fa solo 2 cose con le mani:
- Click in Gemini app per generare i 17 video (1-2 ore totali, distribuite in 5 giorni)  
- Click in Gemini app per generare le 11 illustrazioni (30 min totali)

Tutto il resto è automatizzato e curato da Claude Code.

## Quick start (sul Mac)

```bash
# 1. Setup ambiente
cd ~/Desktop/Progetti_Claude_Code/dalla-scrivania-allalgoritmo/
cp .env.example .env
# Apri .env e metti le tue API keys (vedi sotto come ottenerle, sono gratuite)

# 2. Dipendenze
pip install -r requirements.txt --break-system-packages
npm install

# 3. Avvia Claude Code dalla root del progetto
claude

# Da Claude Code, primo prompt:
# "Leggi CLAUDE.md e dammi il piano dei prossimi 5 giorni"
```

## API keys gratuite da ottenere (5 min)

### Pixabay (musica + SFX)
1. Vai su https://pixabay.com/api/docs/
2. Login (o sign up free)
3. Copia la tua API key dalla docs page
4. Mettila in `.env` come `PIXABAY_API_KEY=...`

### Freesound (SFX extra)
1. Vai su https://freesound.org/apiv2/apply/
2. Login (o sign up free)
3. Compila il form (uso: "personal/educational content creation")
4. Ricevi API key in pochi secondi
5. Mettila in `.env` come `FREESOUND_API_KEY=...`

## Workflow giornaliero (5 giorni)

Dettaglio completo in `docs/06_PRODUCTION_TIMELINE.md`. In breve:

- **Giorno 1**: setup ambiente, Claude Code legge tutto, esporta i prompt Veo, Rocco genera 3 prime scene in Gemini app come validazione stilistica
- **Giorno 2**: Rocco completa la generazione delle 17 scene (3-9 al giorno, limite Pro). Claude Code scarica audio/musica e li mette in deck/assets/
- **Giorno 3**: Rocco genera le 11 illustrazioni realistic in Nano Banana Pro. Claude Code rifinisce lo speech italiano e aggiorna il deck
- **Giorno 4**: assembla, test sul Mac, genera il backup MP4, prova sala (se possibile)
- **Giorno 5**: ripasso speech, ultima checklist, evento

## Struttura cartella

```
dalla-scrivania-allalgoritmo/
├── README.md                       # questo file
├── CLAUDE.md                       # master prompt per Claude Code
├── .env.example                    # template per API keys
├── docs/                           # documentazione completa (8 file)
├── prompts/
│   ├── veo/                        # 17 prompt JSON per Veo (da incollare in Gemini)
│   ├── audio/                      # search terms per Pixabay/Freesound
│   └── music/                      # search terms per Pixabay Music
├── .claude/
│   ├── skills/                     # 5 skill custom Claude Code
│   └── plugins/PLUGIN_INSTALL.md   # cosa installare in Claude Code
├── scripts/
│   ├── export_veo_prompts.py       # esporta prompt Veo formattati per Gemini
│   ├── fetch_audio.py              # scarica SFX da Pixabay/Freesound
│   ├── fetch_music.py              # scarica musica da Pixabay Music
│   ├── assemble_deck.py            # genera deck/index.html
│   └── render_backup_video.py      # genera backup MP4 con ffmpeg
├── deck/                           # reveal.js + asset
├── outputs/                        # backup MP4 finale
└── tests/                          # checklist pre-evento
```

## Filosofia BMAD

Una modifica alla volta → test → conferma → prossima.  
Mai cambiare 3 cose insieme.  
Mai accettare un risultato "boh, ok": o è ⭐⭐⭐⭐⭐ (5/5) o si rigenera.

**Mantra:** "Sta facendo dire al pubblico *minchia un fenomeno quel Rocco* o *bella slide*?"

Se non è il primo, si rilavora.
