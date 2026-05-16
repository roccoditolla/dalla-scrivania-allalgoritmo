# Plugin & Skill Installation Guide

> Setup di Claude Code per il progetto.  
> Da eseguire una volta sola, all'inizio.

---

## Buona notizia: zero plugin esterni richiesti

Il progetto è **100% custom**: le 5 skill che usa Claude Code sono già nella cartella `.claude/skills/` e funzionano automaticamente quando avvii Claude Code dalla root del progetto.

**Non serve installare nessun plugin marketplace.** Tutto quello che serve è nel repo.

---

## Le 5 skill custom

Quando Claude Code parte da `~/Desktop/Progetti_Claude_Code/dalla-scrivania-allalgoritmo/`, carica automaticamente:

| Skill | File | Quando si attiva |
|---|---|---|
| `storyboard-architect` | `.claude/skills/storyboard-architect/SKILL.md` | Modifiche all'arco narrativo |
| `veo-cinematic-prompt` | `.claude/skills/veo-cinematic-prompt/SKILL.md` | Scrittura/raffinamento prompt Veo |
| `audio-sourcing` | `.claude/skills/audio-sourcing/SKILL.md` | Ricerca/download audio Pixabay/Freesound |
| `reveal-cinematic-deck` | `.claude/skills/reveal-cinematic-deck/SKILL.md` | Modifiche al deck reveal.js |
| `speech-writer-italian` | `.claude/skills/speech-writer-italian/SKILL.md` | Scrittura/rifinitura speech italiano |

**Per usarle**, basta scrivere a Claude Code nel naturale flusso della conversazione:
- "Lavoriamo alla scena 8" → invoca automaticamente `veo-cinematic-prompt`
- "Cerca un audio per la tempesta" → invoca automaticamente `audio-sourcing`
- "Sistema il deck per la slide 16" → invoca `reveal-cinematic-deck`

Non serve `/skill nome` o sintassi esplicita. Le skill hanno descrizioni che permettono a Claude Code di sceglierle automaticamente.

---

## Test che le skill funzionino

Da Claude Code, primo prompt:

```
Leggi CLAUDE.md, poi dimmi quali sono le 5 skill custom disponibili 
e cosa fa ognuna in una frase.
```

Se Claude Code risponde elencando le 5 skill correttamente: ✅ tutto pronto.

Se dice "non vedo le skill": stai eseguendo Claude Code dalla **directory sbagliata**. Verificare di essere in `~/Desktop/Progetti_Claude_Code/dalla-scrivania-allalgoritmo/` con `pwd`.

---

## Plugin marketplace esterni (NON necessari)

In passato avevamo considerato:
- ElevenLabs Sound Effects plugin → **sostituito da Pixabay/Freesound** (free)
- Veo Tools (kdowswell) → **non serve**, generiamo via Gemini app manuale

Non installare nulla di esterno. Il progetto è autocontenuto.

---

## Cosa serve sul Mac

1. **Claude Code** installato e aggiornato
2. **Python 3.10+** con dipendenze da `requirements.txt`
3. **Node 20+** per `npx serve` del deck
4. **ffmpeg** per il backup MP4 (`brew install ffmpeg`)
5. **2 API keys gratis** in `.env`: Pixabay + Freesound (vedi README.md)
6. **Account Google AI Pro attivo** (49€/mese, già paghi)

Nient'altro.

---

## Avvio Claude Code

```bash
cd ~/Desktop/Progetti_Claude_Code/dalla-scrivania-allalgoritmo/
claude
```

Primo prompt suggerito:

```
Ho appena scaricato il progetto. Leggi CLAUDE.md, poi i 8 file in docs/, 
poi dimmi:
1. Hai capito tutto?
2. Cosa facciamo oggi (giorno 1)?
3. C'è qualcosa che secondo te non torna nel piano?

Voglio che tu mi metta in discussione, non che mi accontenti.
```

Da qui in poi è una conversazione naturale.
