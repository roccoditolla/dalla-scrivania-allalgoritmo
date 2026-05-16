---
name: reveal-cinematic-deck
description: Builds, modifies, and debugs the Reveal.js cinematic presentation deck for "Dalla Scrivania all'Algoritmo". Use this skill whenever the user wants to assemble or modify deck/index.html, add or remove slides, change transitions, debug fullscreen/audio/video issues on the slides, integrate GSAP animations on the realistic slides (13-23), generate the backup MP4 from the deck, or do anything live-presentation related (clicker config, speaker view, presenter notes). Invoke for anything touching deck/index.html, deck/css/, deck/js/, scripts/assemble_deck.py, or scripts/render_backup_video.py.
---

# Reveal Cinematic Deck — Skill

## Cosa fa questa skill

Costruisce e mantiene il deck Reveal.js che gira live sul palco. Tre responsabilità:

1. **Assemblaggio** — generare `deck/index.html` dalle scene e dalle slide realistic
2. **Stile** — gestire `deck/css/cinematic.css` (palette, tipografia, layout)
3. **Comportamento** — `deck/js/transitions.js` (timing video, mixing audio, GSAP)

E il backup MP4: la pipeline `decktape` o screen recording per generare il render finale.

## Quando si attiva

- "Costruisci il deck con le scene generate finora"
- "Aggiungi la slide 17 con l'illustrazione di AppaltoAI"
- "Il video della scena 3 non parte fullscreen"
- "Crea il backup MP4 della presentazione"
- "Sistema la transizione tra scena 12 e slide 13"
- "Voglio cambiare il font dei titoli"
- L'utente lavora su `deck/` o su `scripts/assemble_deck.py`

## Struttura del deck

```
deck/
├── index.html              # Entry point — generato da assemble_deck.py
├── css/
│   ├── cinematic.css       # Palette, tipografia, layout custom
│   └── reveal.css          # Stock reveal.js (non toccare)
├── js/
│   ├── transitions.js      # GSAP animations, audio mixer custom
│   └── reveal.js           # Stock reveal.js (non toccare)
└── assets/
    ├── videos/             # MP4 generati da Veo
    ├── audio/              # MP3 generati da ElevenLabs
    └── images/             # SVG/PNG per slide realistic + logo
```

## Anatomia di una slide della storia (1-12)

Full-bleed video, niente testo sovrapposto, audio sincronizzato:

```html
<section data-scene-id="01" data-bg-color="#F5EFE6">
  <div class="cinematic-video">
    <video data-autoplay 
           data-src="assets/videos/scene_01_FINAL.mp4"
           preload="auto" 
           muted="false"
           playsinline>
    </video>
  </div>
  <aside class="notes">
    [Speech text from docs/04_SPEECH_SCRIPT.md, scene 01]
  </aside>
</section>
```

Note:
- `data-autoplay` fa partire il video quando la slide diventa attiva
- `muted="false"` perché Veo include l'audio nativo (necessario interazione utente prima — gestito in `transitions.js`)
- `<aside class="notes">` appare nella Speaker View di reveal.js (Rocco le vede sul laptop, il pubblico no)

## Anatomia di una slide realistic (13-23)

Layout disciplinato con illustrazione + numero/frase:

```html
<section data-slide-id="16" data-bg-color="#F5EFE6">
  <div class="realistic-slide">
    <div class="big-number" data-gsap="fade-up">12 min</div>
    <div class="illustration" data-gsap="orange-glow">
      <img src="assets/images/realistic_16_dvr.svg" alt="" />
    </div>
    <div class="caption">DVR Validator — D.Lgs. 81/08</div>
  </div>
  <aside class="notes">
    [Speech text from docs/04_SPEECH_SCRIPT.md, slide 16]
  </aside>
</section>
```

## Transizioni — regole

Da implementare in `transitions.js` + `cinematic.css`:

| Tra | Tipo | Durata | Note |
|---|---|---|---|
| Storia (scene contigue narrative) | fade nero | 600ms | come uno stacco filmico |
| Storia → Storia (atto a atto) | fade nero | 1000ms | respiro più lungo |
| Storia 12 → Realistic 13 | crossfade arancione | 2000ms | bussola → logo |
| Realistic → Realistic | crossfade | 400ms | leggero |
| Slide finale → Black | fade | 800ms | per applauso |

Implementazione (esempio in `transitions.js`):

```javascript
Reveal.on('slidechanged', (event) => {
  const prev = event.previousSlide;
  const curr = event.currentSlide;
  if (prev?.dataset.sceneId === '12' && curr?.dataset.slideId === '13') {
    // Crossfade speciale storia→realistic
    applyOrangeFade(prev, curr, 2000);
  }
});
```

## Audio mixing nel deck

Ogni slide può avere:
- **Audio nativo del video Veo** (dentro l'MP4, gestito dal browser)
- **Ambient ElevenLabs loop** (file MP3 separato, partito su `slidechanged`)
- **SFX one-shot** (es. shimmer della bussola — partito su evento specifico)

Implementare in `transitions.js` un `AudioMixer` che:
- Mantiene una sola istanza ambient attiva alla volta
- Fa crossfade tra ambient quando la scena cambia
- Riproduce SFX overlay senza interrompere l'ambient
- Rispetta i livelli dB definiti in `docs/05_VISUAL_GUIDE.md` (vedi sezione Sound design)

## Workflow assemble_deck.py

Lo script Python che genera `index.html`:

1. Legge `docs/02_STORYBOARD.md` per la sequenza scene
2. Legge `docs/03_REALISTIC_DECK.md` per la sequenza slide
3. Per ogni scena: cerca il video in `deck/assets/videos/scene_XX_FINAL.mp4`
4. Per ogni slide realistic: cerca l'illustrazione in `deck/assets/images/realistic_XX_*.svg`
5. Per ogni scena: trova l'audio ambient da `prompts/elevenlabs/ambient_sounds.json`
6. Inietta lo speech (per le notes) da `docs/04_SPEECH_SCRIPT.md`
7. Scrive `deck/index.html`

Se un asset manca: warning, ma non blocca. Lo script crea una `<section>` placeholder con scritto "ASSET MANCANTE: scene_XX" per essere visibile in fase di test.

## Backup MP4

Il backup si genera con `scripts/render_backup_video.py`:

**Approccio raccomandato:** `decktape` con il preset video.

```bash
npx decktape -p 1000 reveal http://localhost:8000 outputs/backup_video.mp4 \
  --size 1920x1080 --pause 0 --videos
```

**Limite di decktape:** non cattura audio video HTML5 nativamente. Soluzione: usare `puppeteer` + `ffmpeg` con cattura schermo + audio, OPPURE concatenare i video MP4 originali con le illustrazioni statiche in ffmpeg.

Approccio realistic (più semplice): screen recording di alta qualità (es. ScreenFlow su Mac, o OBS) della presentazione completa, esportato come MP4 4K. Si fa una volta sola, in giorno 4.

## Test del deck — checklist

Prima di considerare il deck "pronto":

- [ ] `npx serve deck/` → apre in Chrome, fullscreen funziona (F)
- [ ] Tutte le 23 slide si vedono con il loro contenuto
- [ ] Tutti i video Veo partono in autoplay quando la slide diventa attiva
- [ ] L'audio si sente alle casse del laptop
- [ ] Le transizioni rispettano i tempi della tabella sopra
- [ ] Speaker View (S) mostra le note del docs/04_SPEECH_SCRIPT
- [ ] Clicker/frecce funzionano per avanzare
- [ ] Backspace torna indietro
- [ ] Da nessuna slide si "scappa" fuori dal fullscreen
- [ ] Backup MP4 generato e in `outputs/`

## Errori comuni

| Errore | Causa | Fix |
|---|---|---|
| Video non parte in autoplay | Browser blocca autoplay con audio | Aggiungere `playsinline` + interazione iniziale (click su slide 1) |
| Audio "graffia" tra transizioni | Crossfade troppo aggressivo | Aumentare durata fade-out |
| Slide non in fullscreen vero | Reveal.js è in "presentation mode" ma non full | Premere F dopo il caricamento |
| Font diversi tra Mac e proiettore | Font non caricato | Importare Inter da CDN, non da locale |
| Bianco panna sembra grigio sul proiettore | Profilo colore proiettore | Test in sala, eventuale aggiustamento di `--color-cream` |

## Variabili CSS chiave (`cinematic.css`)

```css
:root {
  --color-cream: #F5EFE6;
  --color-orange: #FF6B1A;
  --color-orange-soft: #FFA463;
  --color-ink: #1A1614;
  --color-ocean-deep: #2C4357;
  --color-fog: #B8B5AD;
  
  --font-display: 'Inter', system-ui, sans-serif;
  
  --transition-fast: 400ms;
  --transition-base: 600ms;
  --transition-slow: 1000ms;
  --transition-orange-bridge: 2000ms;
}
```

Tutto il deck riferisce queste variabili. Cambiare qui = cambiare ovunque coerentemente.
