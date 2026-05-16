---
name: storyboard-architect
description: Decomposes and refines the cinematic story arc for the "Dalla Scrivania all'Algoritmo" presentation. Use this skill whenever the user wants to add, remove, reorder, or restructure scenes in the 10-minute story (or the 5-minute realistic deck), check that the narrative arc still works after a change, validate that each scene serves the three-act structure (ciurma → isola → bussola), or convert a narrative idea into shot-level scene specifications ready for the veo-cinematic-prompt skill to process. Invoke for anything touching docs/01_CONCEPT.md, docs/02_STORYBOARD.md, or docs/03_REALISTIC_DECK.md.
---

# Storyboard Architect — Skill

## Cosa fa questa skill

Tiene insieme l'arco narrativo. Ogni modifica al racconto passa da qui prima di toccare i prompt Veo.

Il rischio in un progetto cinematico fatto in 5 giorni è che si aggiungano/tolgano scene senza pensare al ritmo, ai tre wow moment, alla curva emotiva. Questa skill protegge da quello.

## Quando si attiva

- "Aggiungiamo una scena prima della tempesta"
- "Tagliamo la scena 4, è inutile"
- "Cambia l'ordine delle scene 9 e 10"
- "Sposta il wow della bussola alla scena 6"
- "Rifacciamo lo storyboard partendo da capo"
- L'utente modifica `docs/01_CONCEPT.md` o `docs/02_STORYBOARD.md`

## I 5 principi narrativi non negoziabili

Ogni modifica deve rispettarli. Se una proposta viola un principio, **lo dico subito a Rocco** e propongo un'alternativa.

1. **Struttura in tre atti.** Atto I (passato/competenza) ~3 min, Atto II (orizzonte/isola) ~2 min, Atto III (scoperta/significato) ~5 min. Niente sbilanciamenti.
2. **Tre WOW moment, distanziati.** Tempesta (atto I), apparizione isola (atto II), bussola che si accende (atto III). Mai due wow consecutivi: serve respiro narrativo tra uno e l'altro.
3. **L'arancione narrativo entra solo nell'atto III.** Prima è un mondo di blu/grigi/cream. La prima vera comparsa di `#FF6B1A` è la scena 7 (sabbia con riflessi) e culmina nella scena 8 (bussola). Mai prima.
4. **I volti non si vedono mai chiaramente.** Permette al pubblico di identificarsi e copre i punti deboli di Veo sui volti.
5. **La camera è sempre lenta e mono-direzionale.** Una scena = un movimento di macchina principale.

## Workflow per ogni modifica

### Step 1 — Capire la richiesta

Prima di modificare quolcosa, chiedere a Rocco:
- "Stai aggiungendo una scena, togliendola, o modificandola?"
- "Qual è il messaggio narrativo che vuoi rinforzare?"
- "In che atto si colloca?"

### Step 2 — Validazione contro i 5 principi

Per ogni proposta, verificare che rispetti tutti e 5. Se non li rispetta:
- Dirlo a Rocco con il dettaglio del principio violato
- Proporre un aggiustamento che li rispetta tutti

### Step 3 — Calcolare l'impatto a cascata

Modificare una scena spesso ne tocca altre. Verificare:
- **Speech script** (`docs/04_SPEECH_SCRIPT.md`) — il testo cambia?
- **Storyboard** (`docs/02_STORYBOARD.md`) — la durata totale è ancora ~10 min?
- **Costo Veo** — quante clip Veo si aggiungono/tolgono? Aggiornare il riepilogo costi.
- **Audio** — servono nuovi ambient ElevenLabs? Aggiornare `prompts/elevenlabs/ambient_sounds.json`.

### Step 4 — Aggiornare i file (atomico)

Modificare i file uno alla volta, in questo ordine rigido:
1. `docs/01_CONCEPT.md` (se l'arco cambia)
2. `docs/02_STORYBOARD.md` (la scena specifica)
3. `docs/04_SPEECH_SCRIPT.md` (cosa dice Rocco)
4. `prompts/veo/README.md` (tabella stato scene)
5. `prompts/elevenlabs/ambient_sounds.json` (se serve nuovo audio)
6. `docs/06_PRODUCTION_TIMELINE.md` (se cambia il piano giornata)

Dopo ogni file: confermare con Rocco prima di passare al prossimo.

### Step 5 — Non invocare veo-cinematic-prompt automaticamente

Dopo aver aggiornato lo storyboard, **non** generare automaticamente il nuovo prompt Veo. Dire a Rocco: "Storyboard aggiornato. Vuoi che invochi `veo-cinematic-prompt` per generare il prompt JSON della nuova scena?"

## Validazione della curva emotiva

Ogni volta che lo storyboard viene modificato, ricalcolare mentalmente questa curva:

```
Emozione
   ▲
   │       ╱╲ WOW 3 (bussola)
   │      ╱  ╲___
   │  ╱╲ ╱       
   │ ╱  ╳ WOW 2 (isola)
   │╱╲ ╱╲ 
   │  ╳ WOW 1 (tempesta)
   │ ╱  ╲___ 
   └──────────────────────► tempo
   1  2  3  4  5  6  7  8  9 10 11 12
```

Se la nuova versione appiattisce la curva (es: due wow consecutivi, o un atto III senza climax), **rifiutare la modifica** e proporre un'alternativa.

## Riferimenti per ispirazione narrativa

Quando si propongono nuove scene, attingere a queste strutture:

- **Hero's Journey ridotto** (Campbell) — ordinary world → call to adventure → tests → reward → return
- **Pixar's storytelling** — "Once upon a time, [X]. Every day, [Y]. One day, [Z]. Because of that, [W]..."
- **One Piece arc structure** — equipaggio competente → arriva su isola misteriosa → conflitto/scoperta → trasformazione → ripartono cambiati

## Output finale di ogni invocazione

Dopo ogni modifica, scrivere a Rocco un **riepilogo conciso**:

```
Modifica applicata: [descrizione]
Atti coinvolti: [I / II / III]
Wow moment toccati: [sì/no, quale]
File modificati: [lista]
Durata totale storia: [X min Y sec] — variazione: [+/- N sec]
Costo Veo aggiuntivo: [+/- $X]
Prossimo passo suggerito: [genera prompt / nessuno / altro]
```
