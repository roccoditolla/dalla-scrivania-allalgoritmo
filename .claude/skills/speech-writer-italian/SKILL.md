---
name: speech-writer-italian
description: Writes, refines, and rehearses the Italian spoken script for the "Dalla Scrivania all'Algoritmo" presentation. Use this skill whenever the user wants to write or rewrite parts of the speech, time the speech against the slides (15 min total, 1850 words target), adjust the tone or rhythm of specific passages, add pauses or emphasis, prepare a printed cue sheet for the stage, generate vocal warm-up exercises, or write the open/close (most critical moments). Invoke for anything touching docs/04_SPEECH_SCRIPT.md or paper cue sheets for the event.
---

# Speech Writer Italian — Skill

## Cosa fa questa skill

Scrive e raffina lo speech italiano dei 15 minuti con slide. Bilancia:
- Sincronizzazione con le slide (timing al secondo)
- Tono confidenziale ma autorevole (Rocco a un pubblico di consulenti del lavoro PMI)
- Ritmo lento, drammatico (123 wpm target)
- Pause strategiche (le pause valgono il 30% dell'impatto)

## Quando si attiva

- "Riscrivi il pezzo della scena 8"
- "È troppo lungo il discorso sulla slide 16"
- "Aggiungi una pausa più forte prima della bussola"
- "Cambia il tono del finale, lo voglio più caldo"
- "Genera una cue sheet da stampare e mettere in tasca"
- L'utente modifica `docs/04_SPEECH_SCRIPT.md`

## Vincoli linguistici e di stile

### Tono
- **Confidenziale**, come se Rocco parlasse a un amico in una stanza piccola
- **Mai accademico**, mai "secondo le ricerche", mai "i dati ci dicono"
- **Mai paternalistico**, l'audience sa il suo mestiere. Rocco lo riconosce.
- **Sicuro ma non arrogante**. "Stiamo facendo questo" non "Siamo i migliori".

### Lessico
- **Frasi corte**. Soggetto-verbo-complemento. Punto.
- **Verbi forti**, non aggettivi forti.
- **Niente anglicismi** se esiste l'italiano (eccezioni: AI, brief, lead, deadline, kanban — accettati nel mondo PMI)
- **Numeri concreti** ("4 ore → 12 minuti") meglio degli aggettivi ("molto più veloce")
- **Ripetizione strategica**. Una frase ripetuta tre volte resta. "Anno zero. Adesso. Anno zero."

### Pause
- `*[Pausa Xs]*` in chiaro nel testo, mai opzionale
- Le pause prima e dopo i wow moment sono **sacre**
- Mai due frasi attaccate senza respiro nei momenti chiave
- Pausa di 3s = un'eternità sul palco, ma funziona

### Cadenza target
- **123 parole/minuto** = lento, drammatico
- 15 minuti × 123 = ~1.850 parole totali
- Verificare con `wc -w` ogni volta che si modifica

## Workflow per una modifica

### Step 1 — Identificare la sezione

Dove si interviene:
- Apertura (prima della scena 01) — i primi 30 secondi sono critici per catturare attenzione
- Una scena specifica della storia (es. scena 8 = il momento di silenzio)
- Transizione storia→realistic (cambio di registro)
- Una slide realistic (più informativa, meno narrativa)
- Chiusura (slide 23) — l'ultima impressione

### Step 2 — Calcolare il timing target

Per ogni sezione, il tempo è dettato dalla slide. Esempio:
- Scena 03 (tempesta) = 12s di video → speech che dura ~25-30s (Rocco parla sopra, ma rallentato)
- Slide 16 (DVR) = 30s totali → speech di ~60 parole massimo

### Step 3 — Scrivere/riscrivere il testo

Stile riferimento dai pezzi esistenti in `docs/04_SPEECH_SCRIPT.md`:
- "C'è una ciurma. / Da sempre c'è una ciurma. / Naviga da prima che noi nascessimo. / E naviga ancora oggi." (frasi corte, ritmo a 4 battute)
- "Hanno visto tempeste. / Le hanno passate." (azione-conferma)
- "Una bussola. / [Pausa 3s] / Arancione." (silenzio drammatico)

### Step 4 — Verifica wpm

```bash
# In Claude Code, da terminale:
sezione_text="..."
echo "$sezione_text" | wc -w
# Calcolare: parole / minuti = wpm. Target 120-130.
```

Se wpm > 140: troppo veloce, aggiungere pause o tagliare parole.
Se wpm < 100: troppo lento, può sembrare faticoso. Eccezione: il momento della bussola.

### Step 5 — Cue sheet stampabile

Su richiesta di Rocco, generare un file separato `outputs/cue_sheet.md` con:
- Solo le prime parole di ogni "blocco" (4-5 parole)
- Le pause grandi evidenziate
- Riferimento alla scena/slide a sinistra
- Font grande (formato A5 in 18pt)

Esempio:
```
[SCENA 01] C'è una ciurma. / Da sempre... / Naviga da prima... / E naviga ancora oggi.
[SCENA 02] Sono navigatori. Contabili. / Vedette. Timonieri. / Ognuno con un sapere. / Ognuno con anni...
[SCENA 03 — TEMPESTA] **rallenta** / Hanno visto tempeste. / Le hanno passate. / [pausa] / Ogni cicatrice...
```

## I 5 punti più critici dello speech

Da rivedere ogni volta con attenzione speciale:

1. **L'apertura (prima della scena 01)** — i primi 30 secondi decidono se l'audience entra nella storia o resta sospettosa.
2. **Il silenzio durante la scena 8** — 8 secondi senza parlare. Rocco deve sentirsi sicuro di farlo.
3. **La transizione "anno zero"** (scena 11) — il pivot da "metafora" a "oggi". Deve far sentire urgenza ma non panico.
4. **La transizione storia→realistic** (scena 12 → slide 13) — il cambio di registro. Rischio: il pubblico si sente "scaricato" dalla magia. Soluzione: tono che cambia ma con calma, la slide 13 riprende la bussola.
5. **La chiusura (slide 23)** — l'ultima frase resta. Adesso è "Grazie." Verificare che funzioni rispetto al ritmo emotivo.

## Riferimenti stilistici

Quando si cerca ispirazione:

- **Steve Jobs Stanford Commencement Speech (2005)** — ritmo, pause, frasi corte
- **Massimo Recalcati conferenze** — italiano contemplativo, gravità nelle pause
- **Alessandro Baricco "Mr Gwyn"** — l'arte della frase breve
- **Roberto Saviano discorsi pubblici** — capacità di tenere il silenzio
- **Sorrentino monologhi** ("La grande bellezza") — densità + sospensione

NON-riferimenti (cosa evitare):
- Speech motivazionali americani urlati
- TED Talk pieni di domande retoriche e dati
- Pitch da startup
- Anchor TV con cadenza meccanica

## Output finale

Dopo ogni modifica, riportare a Rocco:

```
Modifica applicata: [sezione modificata]
Parole totali speech: [N] (variazione [+/- N])
Wpm stimato sezione: [X]
Durata stimata sezione: [Y secondi]
File modificato: docs/04_SPEECH_SCRIPT.md
```
