# Disney / Pixar / Cartoon Saloon — SVG Style Brief

> Reference operativo per portare le SVG procedurali del deck "Dalla Scrivania all'Algoritmo" a uno standard "designer professionale". Ogni regola è **SVG-actionable**: niente teoria astratta, solo path, gradient, filter.

---

## Filosofia di partenza

Disney/Pixar/Cartoon Saloon non sono "stili" intercambiabili — ma condividono **4 invarianti**:

1. **Appeal** = ogni forma deve essere piacevole all'occhio anche fuori contesto.
2. **Solid drawing** = volume percepito anche senza ombra (linea + forma raccontano massa).
3. **Shape language** = ogni elemento è leggibile come silhouette nera al 100%.
4. **Asymmetry & life** = niente è perfettamente centrato, simmetrico, o matematico.

Cartoon Saloon (*Song of the Sea*, *Wolfwalkers*) aggiunge: **decorative geometric overlay** (pattern celtici, cerchi concentrici, linee a spirale) come secondo layer narrativo.

---

## 15 caratteristiche tecniche (SVG-actionable)

### 1. Curve Bezier morbide, mai poligoni `L L L`
**Spiegazione**: Disney usa archi continui. Le linee rette uccidono l'organico.
**SVG**: privilegia `Q` (quadratic) e `C` (cubic). Vietato encatenare `L` per simulare curve.
```xml
<!-- NO --> <path d="M 0,50 L 25,20 L 50,40 L 75,15 L 100,50"/>
<!-- SI --> <path d="M 0,50 C 15,10 35,10 50,40 S 85,5 100,50"/>
```

### 2. Squash & stretch nelle forme principali
**Spiegazione**: niente è un cerchio perfetto. Anche una mela è leggermente schiacciata o tirata in base alla "forza" del momento.
**SVG**: invece di `<circle r="50"/>` usa `<ellipse rx="52" ry="46"/>` o un path con asse non uniforme. Per personaggi: testa più larga che alta in pose "rilassate", più alta che larga in pose "tese".

### 3. Line of action — silhouette dinamica
**Spiegazione**: ogni figura segue un'unica curva-guida (S, C, o arco). Mai posa "a tavoletta".
**SVG**: prima di disegnare il personaggio, traccia un `<path d="..." stroke="red"/>` invisibile che descriva la curva del corpo, poi costruisci attorno. Spalle/anche mai paralleli al ground.

### 4. Shape language semantico
**Spiegazione**: cerchi = amichevole/buono, quadrati = solido/affidabile, triangoli = pericolo/tensione.
**SVG**: capitano (autorevole, affidabile) → silhouette dominata da rettangoli e cilindri. Ciurma giovane → cerchi e ovali. Tempesta/onda minacciosa → forme triangolari acute. Bussola buona = cerchio caldo.

### 5. Proporzioni cartoon (non realistiche)
**Spiegazione**: testa = 1/4 o 1/5 del corpo (non 1/7-1/8 realistico). Mani sproporzionate (grandi). Piedi piccoli.
**SVG**: in personaggi 200px alti, testa ~50px. Mani ~22px (overscale di ~1.4x).

### 6. Stroke a peso variabile (line weight modulation)
**Spiegazione**: in animazione tradizionale (Glen Keane, Cartoon Saloon) il contorno **si ispessisce** nelle zone d'ombra/peso e si **assottiglia** nelle zone illuminate/fini (capelli, dita).
**SVG**: `stroke-width` uniforme = morto. Usa più path sovrapposti con stroke diversi:
```xml
<path d="..." stroke="#1a1a1a" stroke-width="4" stroke-linecap="round"/> <!-- zona ombra -->
<path d="..." stroke="#1a1a1a" stroke-width="1.5" stroke-linecap="round"/> <!-- dettagli fini -->
```
In alternativa: `<path>` con `stroke="url(#weightGradient)"` o `pathLength` + dasharray per simulare.

### 7. Palette complementare con un colore "hero"
**Spiegazione**: Disney non usa 20 colori. Usa **3-5 colori** + bianco + nero, con UN colore "hero" saturo (es. l'arancione della bussola). Cartoon Saloon spinge ancora di più: 2-3 tonalità per scena.
**SVG**: definire una palette `<defs>` con max 6 stop, riusarli ovunque. Hero color sempre `#FF6B1A` SOLO Atto III. Atto I-II: blu/grigi/cream con micro-shift di hue (mai stessa saturazione su 2 oggetti adiacenti).

### 8. Gradient morbidi ma direzionali (form shading, no flat)
**Spiegazione**: ogni forma volumetrica ha un `linearGradient` o `radialGradient` che simula UNA luce direzionale (mai due luci, mai gradient piatti orizzontali "Bootstrap").
**SVG**:
```xml
<radialGradient id="formShade" cx="35%" cy="30%" r="70%">
  <stop offset="0%" stop-color="#FFD4A8"/>   <!-- light -->
  <stop offset="60%" stop-color="#E89160"/>  <!-- midtone -->
  <stop offset="100%" stop-color="#7A3A1A"/> <!-- shadow -->
</radialGradient>
```
La direzione del gradient (cx/cy off-center) crea il volume. Mai 50%/50%.

### 9. Highlight specular asimmetrico (Disney sparkle)
**Spiegazione**: occhi, gocce d'acqua, oggetti riflettenti hanno SEMPRE 1 highlight grande + 1 micro-highlight ("catch light"), MAI centrati.
**SVG**: due `<ellipse>` o `<circle>` bianchi semitrasparenti sopra l'occhio:
```xml
<ellipse cx="45%" cy="35%" rx="18%" ry="12%" fill="#fff" opacity="0.95"/>
<circle cx="60%" cy="55%" r="3%" fill="#fff" opacity="0.7"/>
```

### 10. Ambient occlusion line (contact shadow)
**Spiegazione**: dove due forme si toccano (mano-corno, piede-terra, capelli-volto) c'è una **linea sottile più scura** che "incastra" gli oggetti.
**SVG**: un path con `stroke="rgba(0,0,0,0.35)" stroke-width="2" filter="url(#blur1)"` dove le forme combaciano. Mai bordo netto.

### 11. Texture noise / grana "painterly" (Cartoon Saloon signature)
**Spiegazione**: il flat color puro = stock Illustrator. Cartoon Saloon aggiunge una `feTurbulence` leggera per simulare carta/pittura.
**SVG**:
```xml
<filter id="painterly">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="5"/>
  <feColorMatrix values="0 0 0 0 0   0 0 0 0 0   0 0 0 0 0   0 0 0 0.08 0"/>
  <feComposite in2="SourceGraphic" operator="in"/>
</filter>
```
Applicato sopra i colori piatti con `mix-blend-mode="multiply"`.

### 12. Decorative geometric overlay (Celtic / Cartoon Saloon)
**Spiegazione**: in *Song of the Sea*, cerchi concentrici e spirali appaiono SOPRA l'illustrazione come un secondo layer "magico". Funziona benissimo per il momento bussola.
**SVG**: gruppi di `<circle stroke fill="none">` con `stroke-dasharray` o spirali generate con `<path>` di archi consecutivi. Opacity 0.15-0.4. Concentrate nei punti focali (bussola, isola).

### 13. Asimmetria intenzionale ovunque
**Spiegazione**: nessun elemento è perfettamente speculare. Capelli un po' più lunghi a sx, occhio sx 2px più grande, montagna dx un po' più alta della sx.
**SVG**: dopo aver duplicato un elemento (`<use>`), perturbalo con `transform="rotate(2) scale(0.97,1.03)"`. Mai `transform="scale(-1,1)"` puro.

### 14. Background a 3+ layer parallax (depth ladder)
**Spiegazione**: Disney background painters lavorano in 3 piani: far (chiaro/desaturo/blu), mid (saturo), near (scuro/contrastato/dettagliato).
**SVG**: 3 `<g>` separati con saturazione/luminosità decrescenti. Il near layer ha dettaglio fine; il far layer è quasi monocromo.
```xml
<g opacity="1" filter="url(#nearDetail)">...near...</g>
<g opacity="0.85">...mid...</g>
<g opacity="0.6" filter="url(#farHaze)">...far (atmospheric perspective)...</g>
```

### 15. Rim light / controluce (mood signature)
**Spiegazione**: in scene drammatiche (silhouette controluce, isola misteriosa) c'è SEMPRE un **rim light**: linea sottile luminosa sul bordo opposto alla luce principale.
**SVG**: duplica il path della silhouette, `transform="translate(2,-1)"`, `fill="url(#rimGradient)"`, `clip-path` o `mask` per mostrare solo il bordo. Colore complementare alla luce (luce arancione → rim ciano).

---

## 5 errori da evitare (anti-pattern: "questo NON è Disney")

### Errore 1 — Flat color block senza shading
`<rect fill="#3A7BC8"/>` puro = web mockup, non illustrazione.
**Fix**: sempre un `<linearGradient>` con almeno 2 stop (anche piccolissima differenza). Mai un solo colore solido su superfici >50px.

### Errore 2 — Stroke uniforme `stroke-width="2"` ovunque
Manca peso, manca gerarchia visiva.
**Fix**: usa minimo 3 spessori (es. 1px dettagli interni, 2.5px contorno medio, 4-5px contorno esterno principale / zone d'ombra). Sempre `stroke-linecap="round"` e `stroke-linejoin="round"`.

### Errore 3 — Geometrie matematiche perfette (cerchi, simmetria assoluta)
Un `<circle cx="500" cy="500" r="100"/>` con simmetria perfetta sembra clipart.
**Fix**: sostituisci con `<ellipse>` leggermente asimmetrico, o `<path>` con 4 Bezier non identici. Ruota di 2-3 gradi. Sposta il centro di qualche pixel.

### Errore 4 — Personaggi rigidi, pose "a soldatino"
Spalle parallele al suolo, anche allineate, testa dritta = morto.
**Fix**: applica una `line of action`: spalle inclinate ±5°, anche opposte (contrapposto), testa girata leggermente. Mai entrambi i piedi alla stessa altezza.

### Errore 5 — Palette troppo desaturata o troppo "pastel digital"
Tutto in `#cccccc` e `#ddeeff` = wireframe Figma. Tutto in `#FFB6C1`/`#B6E5FF` saturi = candy.
**Fix**: scegli **una temperatura dominante** (warm o cool), aggiungi UN colore complementare saturato come accento (5-10% dell'area), tieni shadow/midtone con leggera tinta (mai grigio neutro `#888`).

---

## Checklist applicativa (per ogni SVG)

Prima di considerare una SVG "Disney-ready", verifica:

- [ ] Ogni forma principale ha **gradient** (no `fill="#xxx"` solido su superfici grandi)
- [ ] Almeno **3 stroke-width** diversi nell'illustrazione
- [ ] Silhouette **leggibile** se la riempi tutta di nero (test: `* { fill: black; stroke: none; }`)
- [ ] Personaggi: testa ~1/4 del corpo, mani grandi, **line of action** evidente
- [ ] Background a **3 layer** con atmospheric perspective (far più chiaro/blu)
- [ ] **Highlight asimmetrico** su ogni superficie riflettente (occhi, bussola, acqua)
- [ ] Almeno UN elemento **decorativo overlay** (cerchio concentrico, spirale, pattern)
- [ ] **Painterly noise filter** applicato globalmente (`feTurbulence` molto leggera)
- [ ] **Zero `L L L` consecutivi** se non per linee deliberatamente rette (orizzonte)
- [ ] **Asimmetria** in ogni coppia (occhi, montagne, alberi)
- [ ] **Rim light** in scene controluce/drammatiche
- [ ] Palette = max 6 colori + bianco/nero, hero color rispetta principio narrativo (arancione SOLO Atto III)

---

## Reference visivi (mentali, non da scaricare)

- **Cartoon Saloon — Song of the Sea**: per onde, mare, decorative overlay, palette desaturata atto I-II
- **Cartoon Saloon — Wolfwalkers**: per stroke variabile, energy lines, posa dinamica
- **Disney — Moana**: per acqua animata, character design semi-realistico ma stilizzato
- **Pixar — Finding Nemo / Luca**: per sottomarino lighting, atmospheric perspective in acqua
- **Glen Keane sketches**: per line of action e curve continue (rifinitura personaggi)

---

## Note finali per l'agent designer

Ogni SVG del deck deve passare la regola "**3 secondi**": se un illustratore Disney professionista guarda 3 secondi e dice "ok, ben fatto", passa. Se dice "sembra clipart" o "sembra Illustrator default", rigenerare.

L'obiettivo NON è copiare Disney pixel-per-pixel — è **applicare gli stessi principi** ad ogni scelta tecnica (Bezier, gradient, stroke, layer order, palette). Il risultato avrà la stessa "qualità di sguardo" senza essere derivativo.
