# 05 — Visual Guide (Style Bible)

> Il DNA visivo di questo progetto.
> Ogni prompt Veo, ogni illustrazione realistica, ogni slide reveal.js deve passare attraverso questo filtro.

---

## Palette colori

### Colori primari (sempre)

| Nome | Hex | RGB | Uso |
|---|---|---|---|
| **Bianco panna** | `#F5EFE6` | 245, 239, 230 | Sfondo dominante di tutto |
| **Arancione bussola** | `#FF6B1A` | 255, 107, 26 | Solo per: bussola, scoperta, accenti narrativi forti |
| **Arancione soft** | `#FFA463` | 255, 164, 99 | Glow, riflessi, sabbia luminosa |
| **Nero inchiostro** | `#1A1614` | 26, 22, 20 | Mai nero puro. Linee, contorni, ombre profonde |

### Colori secondari (parsimoniosi)

| Nome | Hex | Uso |
|---|---|---|
| Blu mare profondo | `#2C4357` | Solo mare, cieli notturni, tempeste |
| Blu mare calmo | `#7A9CB0` | Mare diurno, cieli sereni |
| Sabbia naturale | `#E8DDC8` | Spiagge, parti dell'isola non "illuminate" |
| Grigio nebbia | `#B8B5AD` | Atmosfere, transizioni, ambiguità |
| Oro tramonto | `#D4A76A` | SOLO tramonto/alba reali. NON confondere con arancione narrativo |

### Regola del colore narrativo

L'**arancione `#FF6B1A`** ha **un significato narrativo**.
Appare solo nei momenti in cui sta accadendo qualcosa di significativo legato all'AI/bussola:
- La bussola che si accende (scena 8)
- La sabbia che la circonda (scena 7)
- I riflessi sulla spiaggia (scena 6)
- Le icone delle slide realistiche

**Mai** decorativo. Mai "perché sta bene". Sempre intenzionale.

---

## Tipografia

| Uso | Font | Pesi |
|---|---|---|
| Titoli grandi (slide realistic) | **Inter** | 700, 900 |
| Testo body (raro) | **Inter** | 400, 500 |
| Numeri grandi (slide stat) | **Inter** | 900 condensed |
| Voiceover/sottotitoli (se servono) | **Inter** | 400 |

Niente serif. Niente font decorativi. **Mai Comic Sans, mai Papyrus.** L'eleganza è nella semplicità.

Importazione font:
```html
<link rel="stylesheet" href="https://rsms.me/inter/inter.css">
```

---

## Stile illustrativo (per Veo)

### Cosa scrivere SEMPRE nei prompt Veo

Ogni prompt include questo blocco "style DNA" (incollabile da `prompts/veo/00_style_bible.md`):

```
Style: cinematic animated illustration, painterly cartoon, like a high-end 2D animated film,
visible brush strokes, hand-drawn quality but with professional polish,
limited and intentional color palette of cream white #F5EFE6, deep ink black, muted ocean blues,
with a single saturated orange #FF6B1A used only for narrative emphasis.
Color temperature: warm but desaturated.
Lighting: cinematic, with strong directional light sources, long shadows, atmospheric depth.
Composition: rule of thirds, strong silhouettes, characters often in backlight or shadow.
Faces never shown clearly — characters seen from behind, in profile, or in silhouette.
Camera movement: slow and deliberate, never shaky, never fast cuts.
Mood: contemplative, mythic, epic but intimate.
Inspired by: Studio Ghibli, Cartoon Saloon (Song of the Sea), The Boy and the Heron.
```

### Cosa NON deve apparire mai

Inseriti come `negative_prompt` in ogni call Veo:

```
text, watermark, logo, ugly faces, deformed hands, photorealistic humans, 
glossy 3D render, plastic skin, anime style, cel-shaded, low-resolution, 
pixelated, oversaturated colors, neon, cyberpunk, dystopian, dark grim, 
gore, multiple suns, impossible reflections, jpeg artifacts.
```

---

## Stile illustrativo (per le slide realistiche)

Le slide 13-23 NON usano Veo. Usano illustrazioni statiche o leggermente animate.

### Tool consigliati per generarle

1. **Recraft v3** (API) — perché genera SVG vettoriali, animabili con GSAP
2. **Imagen 3** (Vertex AI) — se serve raster di alta qualità per fondi
3. **Adobe Firefly** — alternativa enterprise

### Prompt template per le slide realistiche

```
A flat illustrated [scene description], isometric perspective, 
limited palette: cream white #F5EFE6 background, soft beige neutrals, 
deep ink lines, one accent of saturated orange #FF6B1A used sparingly 
for the [compass icon / glowing element / specific narrative anchor].
Style: minimalist editorial illustration, clean vector style, 
slight texture but not painterly. 
No text. No people with visible faces. 
Composition: rule of thirds, generous negative space.
Inspired by: Slack illustration style, Stripe Press book covers, Tom Haugomat.
```

---

## Stile delle slide (composizione)

### Slide della storia (1-12) — Full bleed video

- Il video Veo riempie il 100% dello schermo
- Niente testo sovrapposto, niente logo, niente layer
- L'audio viene dalle casse della sala (non dal browser dell'host)
- Transizione: fade-to-black di 600ms tra una scena e l'altra (le scene contigue narrate da Rocco fluiscono come un singolo film)

### Slide realistiche (13-23) — Layout disciplinato

```
┌──────────────────────────────────────┐
│                                       │
│   [Numero o titolo grande]            │
│                                       │
│         [Illustrazione centrale]      │
│              (animata)                │
│                                       │
│   [Frase short]                       │
│                                       │
└──────────────────────────────────────┘
```

- Titolo: 6vw, weight 900, color nero inchiostro
- Frase: 2vw, weight 400, color nero al 80%
- Illustrazione: max 60vh
- Margini: padding 8% su tutti i lati
- Background: bianco panna pieno

---

## Sound design — Style guide

### Principi

- **Frequenze gravi** = momenti di peso narrativo (tempesta, scoperta isola)
- **Frequenze acute** = momenti di rivelazione (la bussola che si accende)
- **Silenzio** = uso strategico, soprattutto prima dei momenti chiave
- **Ambient layer continuo** = mai vuoto, sempre un sottofondo (mare, vento, sala)

### Volumi (rispetto a 0 dB master del deck)

| Tipo | Volume target | Note |
|---|---|---|
| Audio nativo Veo | -3 dB | Già bilanciato |
| Ambient ElevenLabs | -12 dB | Sotto la voce |
| Sound design picchi (tuono, shimmer) | -1 dB | Picchi precisi |
| Musica (da scena 8) | -8 dB | Sopra ambient, sotto voce |

Il volume **del PA della sala** è gestito dal fonico — questi sono i livelli interni del file.

---

## Transizioni — Style guide

### Tra scene della storia (1-12)

- **Cut secco** quando narrativamente c'è un cambio di pensiero (es: tempesta → calma)
- **Cross-dissolve 800ms** quando c'è continuità (es: scialuppa che parte → scialuppa che torna)
- **Fade to black 600ms + fade from black 600ms** solo tra Atti

### Tra slide realistiche (13-23)

- **Cross-fade 400ms** tra slide consecutive
- **Slide-up 600ms con ease-out** quando si introduce un nuovo tool
- **Hold senza transizione** quando l'animazione interna alla slide fa il lavoro

### Tra storia (12) e realistic (13)

Questa è la transizione più importante. Vedi `docs/01_CONCEPT.md` sezione "La transizione dallo story al realistic".

---

## Checklist visiva — prima di considerare "fatta" una scena

- [ ] Lo sfondo dominante è bianco panna o coerente con la palette
- [ ] L'arancione `#FF6B1A` appare solo dove ha significato narrativo
- [ ] Nessun volto chiaramente visibile
- [ ] Camera movement lento e mono-direzionale
- [ ] Nessun testo nel frame
- [ ] L'audio nativo (se presente) è coerente con l'ambient
- [ ] La scena dialoga con la precedente e la successiva (continuità)
