# Business Presentation Brief — Standard Apple Keynote / Linear / Stripe / Pitch.com

> Brief operativo per portare il deck Reveal.js di "Dalla Scrivania all'Algoritmo" allo standard delle migliori presentazioni business contemporanee.
> Fonti: Linear brand guidelines, Pitch.com design guides, Y Combinator pitch deck library, Apple HIG, Stripe Merchant Dashboard analysis (Rauno Freiberg, Matt Ström-Awn), Mantlr "How Stripe/Linear/Vercel ship premium UI".
> Target: slide realistic 13-23 (atto IV, espositive). Le slide 1-12 cinematic restano blu/cream + arancione narrativo.

---

## Filosofia di fondo (3 principi non negoziabili)

1. **Restraint is the discipline most teams skip** (Mantlr). Una sola famiglia tipografica, max 3 pesi, max 3 colori per slide. La fiducia visiva nasce dalla sottrazione.
2. **Color = meaning, not decoration** (Stripe / Linear / Vercel). L'accento esiste solo per dire "guarda qui" — mai per "decorare".
3. **One idea per slide, generous whitespace**. American audiences process slides con 40%+ whitespace il 20% più rapidamente (Pitch.com data).

---

## Palette finale consigliata (60-30-10 rule)

```css
:root {
  /* Brand core - 60% (background, surface) */
  --bg-primary:    #FFFFFF;   /* white puro per business presentations */
  --bg-elevated:   #FAFAF7;   /* off-white cream per card / contenitori */

  /* Ink - 30% (testi, struttura) */
  --ink-primary:   #0A1628;   /* navy deep — titoli e numeri hero */
  --ink-secondary: #4A5568;   /* slate — body */
  --ink-muted:     #94A3B8;   /* slate light — caption, label */
  --border-hair:   #E5E7EB;   /* divisori sottilissimi */

  /* Accent - 10% max (CTA, highlight singolo per slide) */
  --accent:        #FF6B1A;   /* arancione Conflavoro/Eleven — coerente con storia */
  --accent-soft:   #FFF1E6;   /* fondo soft per badge/pill */
  --accent-ink:    #C24A0A;   /* arancione scuro per testo su soft */
}
```

**Regola d'oro applicata**: l'arancione (`--accent`) occupa **<5%** dell'area della slide. Mai sui titoli H1. Solo su: numeri hero KPI, una keyword per slide, underline animata, bordo card attiva, freccia CTA. Verde: bandito. Titoli verdi che staccano dai body neri = errore #1 nel brief di Rocco.

---

## Pattern 1 — Linear Inter typography stack

**Spiegazione**: Linear usa Inter Variable con letter-spacing negativo per display sizes (-0.022em) per ottenere il look "tight, premium, tech-confident". Pitch.com e YC raccomandano una sola famiglia per tutto il deck.

```css
@import url('https://rsms.me/inter/inter.css');

:root {
  --font-display: 'Inter', -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', ui-monospace, monospace;
}

.reveal { font-family: var(--font-display); font-feature-settings: 'cv11','ss03','ss04'; }
.reveal h1, .reveal h2, .reveal h3 { letter-spacing: -0.022em; font-weight: 600; }
.reveal p, .reveal li { letter-spacing: -0.011em; font-weight: 400; }
```

**Esempio visivo**: titolo "AI per il commercialista" a 84px peso 600 spacing tight = vibe Linear, non vibe Comic Sans.

---

## Pattern 2 — Modular type scale 1.250 (Major Third)

**Spiegazione**: scala tipografica matematica = gerarchia immediatamente leggibile. Apple HIG, Material 3 e Linear usano scale modulari. Per slide a schermo 1920x1080 usa base 18px e ratio 1.25.

```css
:root {
  --fs-caption: 14px;   /* eyebrow / label */
  --fs-body:    18px;   /* body text */
  --fs-lead:    22px;   /* sottotitoli, paragrafi hero */
  --fs-h3:      32px;   /* section title */
  --fs-h2:      56px;   /* slide title standard */
  --fs-h1:      96px;   /* hero number / statement slide */
  --fs-mega:    144px;  /* big number KPI */

  --lh-tight:   1.05;   /* per H1/H2 */
  --lh-snug:    1.25;   /* per H3/lead */
  --lh-base:    1.55;   /* per body */
}

.reveal h1 { font-size: var(--fs-h1); line-height: var(--lh-tight); }
.reveal h2 { font-size: var(--fs-h2); line-height: var(--lh-tight); }
.reveal h3 { font-size: var(--fs-h3); line-height: var(--lh-snug); font-weight: 500; }
.reveal p  { font-size: var(--fs-body); line-height: var(--lh-base); color: var(--ink-secondary); }
.reveal .eyebrow { font-size: var(--fs-caption); text-transform: uppercase; letter-spacing: 0.12em; font-weight: 500; color: var(--ink-muted); }
.reveal .mega    { font-size: var(--fs-mega); font-weight: 700; letter-spacing: -0.04em; color: var(--ink-primary); }
```

**Esempio visivo**: slide "DVR Validator" → eyebrow "CASO STUDIO 01" 14px, H1 "DVR Validator" 96px, lead "Controlla 47 punti normativi in 12 secondi" 22px. Tre livelli, niente di più.

---

## Pattern 3 — 8pt grid spacing system

**Spiegazione**: Apple e Google raccomandano grid 8pt. Ogni margin/padding multiplo di 8. Elimina indecisione, scala perfettamente.

```css
:root {
  --s-1:  4px;   /* hairline */
  --s-2:  8px;
  --s-3: 16px;
  --s-4: 24px;
  --s-5: 32px;
  --s-6: 48px;
  --s-7: 64px;
  --s-8: 96px;   /* slide outer padding minimum */
  --s-9: 128px;  /* slide hero padding */
}

.reveal .slides section {
  padding: var(--s-9) var(--s-8);   /* 128px verticale, 96px orizzontale = ~8% slide */
}
.reveal .slide-stack > * + * { margin-top: var(--s-5); }
.reveal .slide-stack-lg > * + * { margin-top: var(--s-7); }
```

**Esempio visivo**: una slide 1920x1080 con padding 96px lascia respirare. È il single biggest fix che separa "PowerPoint 2010" da "Linear pitch".

---

## Pattern 4 — Bento grid layout (Apple-style)

**Spiegazione**: griglia modulare a rettangoli di dimensioni differenti, hero metric nel rettangolo più grande, quote secondaria nel secondo, KPI minori intorno. Popolare nel 2025-26 da Apple keynote, Notion, Vercel.

```css
.bento {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: var(--s-4);
  width: 100%;
  height: 70vh;
}
.bento__hero  { grid-column: 1; grid-row: 1 / span 2; }
.bento__item  {
  background: var(--bg-elevated);
  border: 1px solid var(--border-hair);
  border-radius: 16px;
  padding: var(--s-5);
  display: flex; flex-direction: column; justify-content: space-between;
}
.bento__item--accent {
  background: var(--accent-soft);
  border-color: transparent;
}
.bento__item .mega { font-size: 72px; }
```

**Esempio visivo**: slide "I 5 prodotti Eleven Digital" → hero card "AppaltoAI" a sinistra, quattro card piccole con DVR / LeadHunter / PM AI / Welfare. Aria, ordine, gerarchia immediata.

---

## Pattern 5 — Color usage rule (10% accent max)

**Spiegazione**: regola 60-30-10 declinata su slide. Background neutro 60%, ink 30%, accent ≤10% (idealmente 5%). Mai accent su titolo H1, sempre su un dettaglio puntuale.

```css
/* CORRETTO: accent solo come highlight puntuale */
.reveal .kw { color: var(--accent); font-weight: 600; }      /* keyword inline */
.reveal .pill {
  display: inline-flex; padding: 6px 12px;
  background: var(--accent-soft); color: var(--accent-ink);
  border-radius: 999px; font-size: 13px; font-weight: 500;
}
.reveal .underline-accent {
  background-image: linear-gradient(transparent 60%, var(--accent) 60%, var(--accent) 88%, transparent 88%);
  background-size: 100% 100%;
}

/* SBAGLIATO — non fare: */
/* h1 { color: green; }  →  titolo verde su body nero = errore #1 */
```

**Esempio visivo**: titolo "Cinque bussole reali" in `--ink-primary` (navy), parola "reali" sottolineata con `--accent`. Una sola macchia di colore.

---

## Pattern 6 — Stripe-grade animations (no bounce, ease-out only)

**Spiegazione**: animazioni professionali = ease-out custom, durata 400-600ms, NO bounce/elastic. Stripe e Linear usano cubic-bezier(0.16, 1, 0.3, 1) — il famoso "expo out" che dà la sensazione di "elementi che atterrano dolcemente".

```css
:root {
  --ease-out-expo:  cubic-bezier(0.16, 1, 0.3, 1);
  --ease-out-quart: cubic-bezier(0.25, 1, 0.5, 1);
  --ease-in-out:    cubic-bezier(0.65, 0, 0.35, 1);
  --dur-fast: 200ms;
  --dur-base: 400ms;
  --dur-slow: 600ms;
}

.reveal .fade-up {
  opacity: 0; transform: translateY(24px);
  transition: opacity var(--dur-base) var(--ease-out-expo),
              transform var(--dur-base) var(--ease-out-expo);
}
.reveal .present .fade-up { opacity: 1; transform: translateY(0); }

/* Stagger 80ms tra elementi */
.reveal .present .fade-up:nth-child(1) { transition-delay:  0ms; }
.reveal .present .fade-up:nth-child(2) { transition-delay: 80ms; }
.reveal .present .fade-up:nth-child(3) { transition-delay: 160ms; }
.reveal .present .fade-up:nth-child(4) { transition-delay: 240ms; }
.reveal .present .fade-up:nth-child(5) { transition-delay: 320ms; }
```

E nel JS Reveal:
```js
Reveal.initialize({
  transition: 'fade',
  transitionSpeed: 'default',  // 400ms
  backgroundTransition: 'fade',
});
```

**Esempio visivo**: gli elementi di una bullet list emergono uno dopo l'altro con 80ms di stagger, dal basso verso l'alto di 24px. Smooth, professionale, mai bouncy.

---

## Pattern 7 — Hairline borders + soft shadow elevation

**Spiegazione**: Linear, Vercel e Stripe usano bordi 1px hairline e ombre sottilissime. NIENTE box-shadow drop tipo PowerPoint 2010 (10px 10px black).

```css
.card {
  background: var(--bg-elevated);
  border: 1px solid var(--border-hair);
  border-radius: 12px;
  box-shadow:
    0 1px 2px rgba(10, 22, 40, 0.04),
    0 4px 12px rgba(10, 22, 40, 0.06);
  padding: var(--s-5);
}
.card--elevated {
  box-shadow:
    0 1px 2px rgba(10, 22, 40, 0.04),
    0 8px 32px rgba(10, 22, 40, 0.08);
}
```

**Esempio visivo**: card "DVR Validator" sembra fluttuare 2mm sopra la slide, non 2cm. Eleganza si vede dai dettagli sub-pixel.

---

## Pattern 8 — Big number KPI with eyebrow + caption

**Spiegazione**: pattern Stripe/Linear per metriche hero. Eyebrow label all'caps spaziato + mega number + caption descrittiva sotto. Stop.

```css
.kpi {
  display: flex; flex-direction: column; gap: var(--s-3);
}
.kpi__eyebrow { font-size: 13px; text-transform: uppercase; letter-spacing: 0.14em;
                color: var(--ink-muted); font-weight: 500; }
.kpi__value   { font-size: 144px; font-weight: 700; line-height: 0.95;
                letter-spacing: -0.04em; color: var(--ink-primary);
                font-variant-numeric: tabular-nums; }
.kpi__value .unit { font-size: 56px; color: var(--ink-muted); font-weight: 500;
                    vertical-align: super; margin-left: 4px; }
.kpi__caption { font-size: 18px; color: var(--ink-secondary); max-width: 480px;
                line-height: 1.55; }
```

**Esempio visivo**: slide "12 secondi" → eyebrow "TEMPO MEDIO DI VALIDAZIONE", number "12s" a 144px navy, caption "vs 4 ore in modalità manuale tradizionale" a 18px slate.

---

## Pattern 9 — Slide reveal: fade only, no slide-from-side

**Spiegazione**: cambiare slide con fade (200-300ms) anziché slide/zoom = look Pitch.com/Keynote. Slide transition orizzontale = look amatoriale PPT.

```js
Reveal.initialize({
  transition: 'fade',         // mai 'slide', 'convex', 'zoom'
  transitionSpeed: 'fast',
  backgroundTransition: 'fade',
  controls: false,            // controlli visibili = unprofessional su stage
  progress: true,              // ma sottile, in basso
  hash: true,
});
```

```css
.reveal .progress { color: var(--accent); height: 2px; }
.reveal .progress span { background: var(--accent); }
```

---

## Pattern 10 — Eyebrow + Title + Lead trio

**Spiegazione**: ogni slide expository segue lo stesso schema head — riconoscibilità immediata, ritmo di lettura prevedibile. Pattern usato da Linear changelog, Vercel keynote, Stripe sessions.

```html
<section class="slide-doc">
  <header class="slide-head fade-up">
    <p class="eyebrow">Caso studio 01</p>
    <h2>DVR Validator</h2>
    <p class="lead">Il primo strumento AI che valida un Documento di Valutazione Rischi in 12 secondi.</p>
  </header>
  <div class="slide-body fade-up">
    <!-- bento / kpi / grafico -->
  </div>
</section>
```

```css
.slide-head { max-width: 1200px; margin-bottom: var(--s-7); }
.slide-head .eyebrow + h2 { margin-top: var(--s-3); }
.slide-head h2 + .lead    { margin-top: var(--s-4); max-width: 900px;
                            color: var(--ink-secondary); font-size: var(--fs-lead);
                            font-weight: 400; line-height: var(--lh-snug); }
```

---

## Pattern 11 — Underline accent invece di highlight box

**Spiegazione**: per evidenziare una keyword, usa underline con offset (look moderno) anziché background giallo (look 2008).

```css
.reveal .accent-underline {
  text-decoration: underline;
  text-decoration-color: var(--accent);
  text-decoration-thickness: 4px;
  text-underline-offset: 8px;
}
```

**Esempio visivo**: titolo "L'AI **affianca**, non sostituisce" → "affianca" sottolineata arancione 4px con offset 8px. Pulito, moderno.

---

## Pattern 12 — Numeric typography tabular-nums

**Spiegazione**: usa `font-variant-numeric: tabular-nums` su tutti i numeri per allinearli verticalmente nelle tabelle/KPI grid. Dettaglio sub-pixel che Stripe e Linear hanno sempre.

```css
.reveal .num, .reveal .kpi__value, .reveal table {
  font-variant-numeric: tabular-nums;
  font-feature-settings: 'tnum' 1, 'ss01' 1;
}
```

---

## 5 errori da evitare (cosa fa sembrare amatoriale)

1. **Titoli verdi staccati dal body nero**. Più di 3 colori in slide = caos. Regola: 1 ink colour per testi + 1 accent <5%. Mai usare green/red sui titoli, solo navy/slate.
2. **Più di una famiglia tipografica**. Pitch.com: "use one font family, less visual decoration". Pile Bold+Medium+Regular+Light nella stessa slide = gerarchia collassa.
3. **Bounce/elastic animations stile PowerPoint 2010**. Solo ease-out curves (cubic-bezier(0.16, 1, 0.3, 1)). Mai overshoot. Mai spin/flip. Durate 200-600ms max.
4. **Drop shadow nere 10px stile Word 2003**. Usa hairline 1px + shadow sub-pixel (0 1px 2px rgba(10,22,40,0.04)). Eleganza = ombre quasi invisibili.
5. **Slide affollata con bullet+immagine+grafico+logo+disclaimer**. One idea per slide. Se ci sono 4 cose, fanne 4 slide. American audiences process slides con 40%+ whitespace il 20% più rapidamente.

Bonus errori da evitare:
- Slide transition orizzontali (`slide`, `convex`, `zoom`). Solo `fade`.
- Bullet point con dot pieno nero (•). Usa eyebrow numeri "01 / 02 / 03" o icone hairline.
- Stock photo people-smiling-at-laptop. Mai. Solo illustrazioni Nano Banana o screenshot reali prodotto.

---

## Riferimenti repo / fonti

- **Linear brand & design**: https://linear.app/brand — typography Inter Variable, letter-spacing tight
- **Pitch.com design guide**: https://pitch.com/guides/presentation/design-your-presentation — one font family, subtraction
- **YC Pitch Deck Library**: https://www.ycombinator.com/library/4T-how-to-design-a-better-pitch-deck — 10-12 slide, una idea per slide
- **Stripe Merchant Dashboard analysis** (Matt Ström-Awn) — color = meaning, microstates
- **Rauno Freiberg "Devouring Details"** — Linear/Vercel/Stripe motion principles
- **Mantlr "How Stripe, Linear, Vercel ship premium UI"** — restraint, microstates
- **Apple HIG Typography** — type hierarchy, character spacing
- **8pt Grid** (Spec.fm, FreeCodeCamp) — spacing system
- **Reveal.js themes** — `joshed-io/revealjs-themes`, `julie-ng/tidy-revealjs`, `AnneTee/reveal-js-themes` (riferimenti per struttura SCSS modulare)

---

## Applicazione consigliata al deck (priorità)

1. **Phase 1** (massimo impatto, minimo rischio): aggiornare `:root` variables in `deck/css/cinematic.css` con la palette navy/cream/orange-accent + scala tipografica modulare + 8pt spacing.
2. **Phase 2**: introdurre classi `.eyebrow`, `.lead`, `.kpi`, `.bento`, `.card` come componenti riutilizzabili sulle slide 13-23.
3. **Phase 3**: sostituire transitions Reveal.js a `fade` 300ms; aggiungere fade-up con stagger 80ms via CSS.
4. **Phase 4**: code review slide 13-23 — eliminare bullet •, sostituire con eyebrow numerati; rimuovere ogni verde/red dal CSS; verificare che l'accent occupi <5% area su ogni slide.

Le slide cinematic 1-12 NON si toccano — restano nel mondo narrativo blu/cream con arancione narrativo dell'atto III. Questo brief si applica SOLO al ramo realistic atto IV (13-23) dove serve il look "Stripe/Linear pitch".
