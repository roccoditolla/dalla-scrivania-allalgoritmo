# Realistic Prompts — Slide 13-23 (Nano Banana Pro)

> Master file copy-paste per Rocco. Un blocco prompt per ciascuna delle 11 slide realistic.
> Stile: minimal isometric, palette cream + orange, hand-drawn ink line art.

---

## README — Cosa devi fare, Rocco

**Workflow per ciascuna delle 11 slide (15-25 minuti totali):**

1. Apri **Gemini app web** (gemini.google.com) e seleziona il modello **Nano Banana Pro** (image generation).
2. Apri questo file e vai sulla slide che stai per generare (parti dalla 13, segui ordine numerico).
3. **Copia il blocco "Prompt finale"** (tutto il blocco grigio sotto la voce *Prompt finale*) e incollalo nel campo prompt di Gemini.
4. **Copia il blocco "Negative prompt"** e incollalo nel campo negative prompt (se Nano Banana lo espone) o in coda al prompt principale come "Avoid: ...".
5. Premi **Generate**. Aspetta 30-60 secondi.
6. Valuta il risultato contro gli **Acceptance criteria** della slide. Se passa → step 7. Se non passa → rigenera (max 3 tentativi prima di chiedermi di rifinire il prompt).
7. **Scarica la PNG** (tasto destro → salva immagine).
8. **Rinomina** il file usando il `Filename target` indicato sotto la slide (es. `realistic_13_anno_zero_compass.png`).
9. **Sposta** il file in `deck/assets/images/` del progetto.
10. Avvisa l'orchestratore quando hai finito tutte e 11 (oppure dopo ogni 3, fa lo stesso).

**Ordine consigliato:** sequenziale 13 → 14 → 15 → 16 → 17 → 18 → 19 → 20 → 21 → 22 → 23. La 13 e la 23 condividono il soggetto bussola (consistenza), la 21 riusa le bussole dei tool 16-20 (consistenza). Generandole in ordine fisserai il "carattere" della bussola arancione subito.

**Tempo stimato:** 1-2 minuti per prompt × 11 = ~15-25 minuti totali (incluse 1-2 rigenerazioni).

**Vincoli sacri (non negoziabili):**
- Nessun testo nelle immagini (il testo va sopra in CSS sul deck).
- Arancione `#FF6B1A` solo sull'elemento narrativo (la bussola, il checkmark, l'icona del tool). Mai decorativo.
- Mai volti chiari. Persone sempre di spalle, in silhouette o senza testa visibile.
- Sfondo cream pieno, mai texture di carta vecchia, mai gradient mesh, mai ombre realistiche.

---

## Negative prompt standard (riusabile su tutte le 11 slide)

```
text, words, letters, numbers, captions, watermark, logo, signature, photorealistic, 3D render, octane render, glossy plastic, neon, cyberpunk, faces in detail, eyes, mouth, cartoon eyes, Disney style, Pixar style, anime, manga, cel-shaded, busy background, gradient mesh, drop shadows, lens flare, bokeh, fake paper texture, vintage paper, grunge, low resolution, pixelated, jpeg artifacts, oversaturated, multiple oranges, orange used decoratively, modern smartphones, screens with UI mockups.
```

---

## Slide 13 — "Anno zero" (apertura sezione)

**Contesto narrativo:** Apertura della sezione realistic. La bussola arancione (estratta dalla scena 8 della storia) pulsa al centro di uno sfondo cream. Sotto andrà il claim "ANNO ZERO." Per chi sa già navigare.

**Prompt finale:**
```
Minimal isometric illustration of a single antique navigation compass viewed from a slight three-quarter top angle, centered on the canvas with abundant negative space around it. Hand-drawn ink line art with flat color fills. Palette: cream white #F5EFE6 background dominant covering the entire frame, deep ink black #1A1614 for the compass casing outline and the rose petals of the windrose, single accent of saturated orange #FF6B1A only on the central glowing core and the needle of the compass — the orange should look as if it emits a soft inner light, not a hard fill. Optional muted deep ocean blue #2C4357 for tiny tick marks on the rim. Composition: centered, generous white space, rule of thirds, no text or letters anywhere in the image. Line quality: uniform thin pen weight with slight hand-drawn irregularity, similar to high-end editorial illustration. Style references: Jon Klassen minimalism, Ikea assembly diagrams clarity, Matisse figural reduction. Mood: clean, confident, contemplative — a professional artifact made beautiful, the symbol of a new beginning. Output: square 1:1 aspect ratio, high resolution PNG with cream background.
```

**Acceptance criteria:**
- La bussola è chiaramente riconoscibile e centrata, occupa circa il 50-60% del frame.
- L'arancione appare solo nel cuore/ago della bussola, non nei contorni o nei dettagli decorativi.
- Nessun testo, nessun numero sulla rosa dei venti.

**Filename target:** `realistic_13_anno_zero_compass.png`

---

## Slide 14 — Chi siamo (Conflavoro AI)

**Contesto narrativo:** Vista isometrica di una sede/azienda con persone (anonime, di spalle) che lavorano a scrivanie. Sopra ogni scrivania piccole bussole stilizzate fluttuano — il segnale visivo di "5 piattaforme in costruzione".

**Prompt finale:**
```
Minimal isometric illustration of an open office space viewed from a high three-quarter angle, with three or four simple wooden desks arranged in a loose cluster on a cream floor. At each desk, a single human figure seen strictly from behind — only the back of the shoulders and the back of the head visible, no faces, no facial features at all, dressed in muted neutral tones. Above each desk, a small floating compass icon hovers gently, simplified to a circle with a single needle. Hand-drawn ink line art with flat color fills. Palette: cream white #F5EFE6 background dominant, deep ink black #1A1614 for all line work and silhouettes, single accent of saturated orange #FF6B1A only on the floating compass needles — five small orange pinpoints scattered across the composition. Optional muted deep ocean blue #2C4357 for tiny shadow accents under desks. Composition: balanced isometric layout, generous negative space at the top, rule of thirds, no text or letters anywhere. Line quality: uniform pen weight, slight hand-drawn irregularity. Style references: Jon Klassen, Ikea diagrams, Matisse. Mood: calm collective focus, a quiet workshop of builders. Output: square 1:1 aspect ratio, high resolution PNG.
```

**Acceptance criteria:**
- Le persone sono viste rigorosamente da dietro, niente facce o profili.
- Esattamente o circa 5 piccole bussole arancioni fluttuanti (richiamo alle 5 piattaforme).
- L'arancione è solo sulle bussole, non sui mobili o sulle persone.

**Filename target:** `realistic_14_conflavoro_office.png`

---

## Slide 15 — Il problema (scrivania oppressa)

**Contesto narrativo:** Una scrivania vista 3/4 dall'alto, sommersa da una pila enorme di fogli. Un orologio gira veloce. Una persona di spalle. Mood opprimente, palette spostata sui grigi (come la tempesta della scena 3): qui l'arancione NON deve comparire — è il problema, non ancora la soluzione.

**Prompt finale:**
```
Minimal isometric illustration of a single wooden desk seen from a three-quarter top angle, completely overwhelmed by a tall, leaning, almost comical pile of paper documents stacked precariously on top. To one side of the desk, a round wall clock with bold black hands pointing in tense positions. A single human figure seen strictly from behind sits at the desk, head slightly bowed, shoulders rounded — only back and shoulders visible, no face, no facial features. Hand-drawn ink line art with flat color fills. Palette: cream white #F5EFE6 background, deep ink black #1A1614 for all line work, muted fog gray #B8B5AD washing the paper pile and the figure to convey a heavy, oppressive mood, deep ocean blue #2C4357 only for the clock face. Critical: NO orange anywhere in this image — this scene represents the problem before the solution. Composition: centered desk, generous negative space above, rule of thirds, no text or letters anywhere, no numbers on the clock face. Line quality: uniform pen weight, slight hand-drawn irregularity. Style references: Jon Klassen, Ikea diagrams, Matisse. Mood: quiet exhaustion, the weight of routine compliance. Output: square 1:1 aspect ratio, high resolution PNG.
```

**Acceptance criteria:**
- Zero arancione nell'immagine — è una scelta narrativa esplicita.
- La pila di carte è visibilmente "troppo grande" rispetto alla scrivania (esagerazione editoriale).
- La persona è di spalle, postura curva, nessun volto visibile.

**Filename target:** `realistic_15_problema_scrivania.png`

---

## Slide 16 — DVR Validator (Tool 1)

**Contesto narrativo:** Stessa scrivania della slide 15, ma adesso un laptop emette luce arancione verso la pila di fogli, che si "ordina" in slow motion. La luce arancione = la bussola. Tool: validazione DVR D.Lgs. 81/08, da 4 ore a 12 minuti.

**Prompt finale:**
```
Minimal isometric illustration of the same wooden desk as before, viewed from a three-quarter top angle, but now the scene is transformed: a slim open laptop sits at the center of the desk emitting a soft, warm light toward a neat orderly stack of paper documents. The papers, previously chaotic, are now arranged in a tidy aligned pile with a single visible checkmark icon glowing on the top sheet. The same human figure seen strictly from behind, but shoulders relaxed, leaning back slightly — no face, no facial features, no head detail. Hand-drawn ink line art with flat color fills. Palette: cream white #F5EFE6 background dominant, deep ink black #1A1614 for line work, single accent of saturated orange #FF6B1A reserved exclusively for the inner glow of the laptop screen and the small checkmark on the document — the orange should look like emitted light, soft halo, not a hard fill. Composition: centered desk, generous negative space, rule of thirds, no text or letters anywhere on the documents or laptop screen. Line quality: uniform pen weight, slight hand-drawn irregularity. Style references: Jon Klassen, Ikea diagrams, Matisse. Mood: quiet relief, order restored. Output: square 1:1 aspect ratio, high resolution PNG.
```

**Acceptance criteria:**
- L'arancione appare solo come glow del laptop e checkmark — due punti narrativi precisi, niente altro.
- Lo schermo del laptop è "vuoto" — niente UI, niente testo, niente finestre.
- La continuità con la slide 15 è leggibile: stessa scrivania, stessa figura, ma postura ora rilassata.

**Filename target:** `realistic_16_dvr_validator.png`

---

## Slide 17 — AppaltoAI (Tool 2)

**Contesto narrativo:** Vista isometrica di un "imbuto" arancione che riceve molti documenti in entrata e ne fa uscire uno solo, pulito. Riferimento: gare pubbliche, 200 pagine condensate in un report di 4 pagine.

**Prompt finale:**
```
Minimal isometric illustration of a vertical funnel shape positioned at the center of the canvas, with many simplified rectangular paper sheets falling into the wide top opening from above and a single neat stacked report emerging at the narrow bottom onto a small platform. The funnel is the only object rendered in saturated orange. Hand-drawn ink line art with flat color fills. Palette: cream white #F5EFE6 background dominant, deep ink black #1A1614 for the outlines of all the paper sheets and the platform, muted fog gray #B8B5AD for the falling papers to suggest volume and quantity, single accent of saturated orange #FF6B1A reserved exclusively for the funnel shape itself, optional muted deep ocean blue #2C4357 for very small ticks on the resulting report pages. Composition: vertical centered axis, generous negative space on left and right, rule of thirds, no text or letters anywhere, no numbers visible on any document. Line quality: uniform pen weight, slight hand-drawn irregularity. Style references: Jon Klassen, Ikea assembly diagrams, Matisse. Mood: hypnotic continuous flow, complexity reduced to clarity. Output: square 1:1 aspect ratio, high resolution PNG.
```

**Acceptance criteria:**
- L'imbuto è chiaramente l'unico elemento arancione — il "filtro" è il significato.
- Molti fogli in entrata (almeno 8-10), un solo report in uscita (visivamente piccolo e ordinato).
- Nessun testo né numeri sui fogli.

**Filename target:** `realistic_17_appaltoai_funnel.png`

---

## Slide 18 — LeadHunter AI (Tool 3)

**Contesto narrativo:** Mappa stilizzata d'Italia. Punti che si accendono in arancione (lead qualificati). Tracce sottili che li collegano. Mood dinamico.

**Prompt finale:**
```
Minimal isometric illustration of a stylized flat outline map of Italy centered on the canvas, drawn as a single clean continuous ink line — the boot shape recognizable but simplified, no internal regional borders, no city names, no labels of any kind. Scattered across the map shape, approximately seven to nine small filled circular dots glow in saturated orange, distributed naturally over the territory. Thin black line segments connect a few of the dots in a sparse network pattern, suggesting a constellation rather than a dense web. Hand-drawn ink line art with flat color fills. Palette: cream white #F5EFE6 background dominant, deep ink black #1A1614 for the country outline and the connection lines, single accent of saturated orange #FF6B1A reserved exclusively for the glowing dots, optional muted deep ocean blue #2C4357 only for very faint coastal hints. Composition: country shape centered with breathing room on all sides, rule of thirds, no text or letters anywhere on the map, no compass rose, no scale bar. Line quality: uniform pen weight, slight hand-drawn irregularity. Style references: Jon Klassen, Ikea diagrams, Matisse. Mood: expansive, alive, qualified targets emerging across the territory. Output: square 1:1 aspect ratio, high resolution PNG.
```

**Acceptance criteria:**
- L'Italia è riconoscibile ma stilizzata (no confini regionali, no etichette).
- 7-9 punti arancioni distribuiti, alcuni connessi da linee sottili nere — non una ragnatela.
- Zero testo: niente nomi di città, niente "Italia", niente bussola/scala.

**Filename target:** `realistic_18_leadhunter_italy.png`

---

## Slide 19 — Project Manager AI (Tool 4)

**Contesto narrativo:** Vista isometrica semplificata di una board kanban. Card che si muovono tra colonne. Una piccola bussola arancione in alto a destra. Persone (anonime) che lavorano serene attorno.

**Prompt finale:**
```
Minimal isometric illustration of a flat board with three vertical columns rendered as simple rectangles, each column containing two or three small rectangular cards stacked loosely. The board is viewed at a three-quarter isometric angle. In the upper right corner of the board, a single small compass icon glows in saturated orange. Around the board, two human figures seen strictly from behind — only shoulders and back of head visible, no faces, no facial features — gesture calmly toward the cards as if collaborating. Hand-drawn ink line art with flat color fills. Palette: cream white #F5EFE6 background dominant, deep ink black #1A1614 for all line work including the columns, the cards, and the figures, single accent of saturated orange #FF6B1A reserved exclusively for the small corner compass icon, optional muted deep ocean blue #2C4357 for tiny status markers on two of the cards. Composition: board centered slightly low, figures flanking, generous negative space above, rule of thirds, no text or letters anywhere on the cards or columns. Line quality: uniform pen weight, slight hand-drawn irregularity. Style references: Jon Klassen, Ikea diagrams, Matisse. Mood: calm collaborative flow, work that thinks alongside you. Output: square 1:1 aspect ratio, high resolution PNG.
```

**Acceptance criteria:**
- Solo la bussola in alto a destra è arancione — le card e le colonne sono nere/cream.
- Le card sono rettangoli vuoti — niente testo, niente avatar, niente etichette.
- Le due figure sono di spalle, gesti calmi, niente volti.

**Filename target:** `realistic_19_project_manager_kanban.png`

---

## Slide 20 — Videoconferenze + Welfare (Tool 5)

**Contesto narrativo:** Split screen, due metà. Sinistra: videoconferenza con figure stilizzate sedute attorno a un tavolo. Destra: icona welfare (cuore + persone). Entrambe le metà hanno un piccolo richiamo arancione.

**Prompt finale:**
```
Minimal isometric illustration composed as a balanced diptych on a single square canvas, divided by a thin vertical line at the exact center. Left half: an isometric view of a round meeting table seen from above-three-quarter, with four simple seated human figures viewed strictly from behind, each shown only as a shoulder-and-back-of-head silhouette, no faces. A small orange dot floats above the center of the table representing a video call indicator. Right half: a simple flat icon composition of a heart shape with two abstract human silhouettes standing under it, the heart outlined in deep ink black with a single orange small accent inside it. Hand-drawn ink line art with flat color fills. Palette: cream white #F5EFE6 background dominant in both halves, deep ink black #1A1614 for all line work, single accent of saturated orange #FF6B1A used only twice — the small dot above the meeting table on the left and the small heart fill on the right. Composition: each half balanced internally, vertical divider clean and thin, generous negative space, rule of thirds in each panel, no text or letters anywhere. Line quality: uniform pen weight, slight hand-drawn irregularity. Style references: Jon Klassen, Ikea diagrams, Matisse. Mood: human-first technology, people before processes. Output: square 1:1 aspect ratio, high resolution PNG.
```

**Acceptance criteria:**
- Diptych chiaro: linea verticale al centro, due metà bilanciate visivamente.
- Esattamente due elementi arancioni (uno per lato) — niente di più, niente di meno.
- Volti delle figure sedute mai visibili (solo schiene).

**Filename target:** `realistic_20_video_welfare_diptych.png`

---

## Slide 21 — Il pattern (le 5 bussole)

**Contesto narrativo:** Tutte e 5 le bussole arancioni (una per tool) ruotano in cerchio attorno a una bussola più grande al centro. Si formano connessioni tra loro. È la sintesi visiva: 5 bussole, una visione.

**Prompt finale:**
```
Minimal isometric illustration of one large central compass surrounded by five smaller compasses arranged in a perfect circle around it, each smaller compass equidistant from its neighbors. Thin sparse line segments connect the central compass to each of the five outer compasses like spokes, and a few additional thin lines connect adjacent outer compasses suggesting an interlinked constellation. All compasses are simplified to a circular outline with a single needle inside. Hand-drawn ink line art with flat color fills. Palette: cream white #F5EFE6 background dominant, deep ink black #1A1614 for compass casings and connecting lines, single accent of saturated orange #FF6B1A reserved exclusively for the needles of all six compasses and the soft inner glow of the central one — the central compass slightly more luminous than the outer five. Composition: radial symmetry centered on the canvas, generous negative space at the corners, rule of thirds, no text or letters anywhere, no numbers on any compass face. Line quality: uniform pen weight, slight hand-drawn irregularity. Style references: Jon Klassen, Ikea diagrams, Matisse. Mood: convergence, system, family of tools sharing one direction. Output: square 1:1 aspect ratio, high resolution PNG.
```

**Acceptance criteria:**
- Esattamente 6 bussole (1 centrale + 5 in cerchio), distribuite con simmetria radiale.
- L'arancione è solo sugli aghi e sul glow centrale — i contorni delle bussole sono neri.
- Le linee di connessione sono nere, sottili, sparse — non una ragnatela densa.

**Filename target:** `realistic_21_pattern_five_compasses.png`

---

## Slide 22 — Metodologia BMAD

**Contesto narrativo:** Il processo BMAD a 4 step orizzontali: Build minimal, Test, Confirm, Next. Ognuno con una piccola icona. Frecce che scorrono. Palette panna + arancione, una cosa alla volta.

**Prompt finale:**
```
Minimal isometric illustration of four small square cards arranged in a clean horizontal row across the center of the canvas, each card connected to the next by a thin black arrow pointing right. Each card contains a single simplified pictogram: card one shows a small wooden block being placed (build), card two shows a magnifying glass over a small dot (test), card three shows a checkmark (confirm), card four shows a forward-pointing arrow (next). The third card — the checkmark — is the only one rendered with its pictogram filled in saturated orange. The other three pictograms are deep ink black. Hand-drawn ink line art with flat color fills. Palette: cream white #F5EFE6 background dominant, deep ink black #1A1614 for card outlines, arrows, and three of the four pictograms, single accent of saturated orange #FF6B1A reserved exclusively for the checkmark pictogram in the third card. Composition: horizontal row centered vertically, generous negative space above and below, rule of thirds, no text or letters anywhere on the cards or arrows. Line quality: uniform pen weight, slight hand-drawn irregularity. Style references: Jon Klassen, Ikea assembly diagrams, Matisse. Mood: clear sequence, disciplined progression, one step at a time. Output: square 1:1 aspect ratio, high resolution PNG.
```

**Acceptance criteria:**
- 4 card in fila orizzontale, ognuna con un pittogramma diverso (block, lente, check, freccia).
- Solo il checkmark (terzo step) è arancione — gli altri tre pittogrammi sono neri.
- Frecce sottili tra le card, nessun testo né numerazione.

**Filename target:** `realistic_22_bmad_methodology.png`

---

## Slide 23 — Anno zero. Adesso. (chiusura)

**Contesto narrativo:** Stessa bussola della slide 13 ma "compiuta": al centro la grande bussola arancione, attorno orbitano cinque piccole icone dei 5 tool. È la chiusura emotiva, la sintesi visiva del percorso.

**Prompt finale:**
```
Minimal isometric illustration of one large central compass viewed from a slight three-quarter top angle, identical in style to the opening compass, with five small simple tool icons orbiting around it in a wide circle — each icon a tiny pictogram representing one product (a stack of papers, a funnel, a map dot, a kanban card, a heart shape). The orbit is suggested by a single thin almost-invisible black ring passing through all five icons. The central compass emits a soft inner orange glow stronger than in the opening slide, suggesting culmination and arrival. Hand-drawn ink line art with flat color fills. Palette: cream white #F5EFE6 background dominant, deep ink black #1A1614 for the compass casing, the orbit ring, and the outlines of the five tool icons, single accent of saturated orange #FF6B1A reserved exclusively for the central compass needle and its inner glow halo — the orbiting tool icons remain entirely in black ink. Composition: radial centered, generous negative space at the corners, rule of thirds, no text or letters anywhere. Line quality: uniform pen weight, slight hand-drawn irregularity. Style references: Jon Klassen, Ikea diagrams, Matisse. Mood: arrival, emotional resolution, the orange compass now in our hands. Output: square 1:1 aspect ratio, high resolution PNG.
```

**Acceptance criteria:**
- La bussola centrale è visivamente parente di quella della slide 13 (stessa identità grafica) ma il glow è più intenso.
- 5 piccole icone orbitano attorno, tutte nere — solo la bussola centrale è arancione.
- Niente testo "ANNO ZERO" o "GRAZIE" nell'immagine — quello va sopra in CSS.

**Filename target:** `realistic_23_anno_zero_culmination.png`

---

## Note finali per Rocco

- Se Nano Banana ti restituisce un'immagine con testo dentro (capita), rigenera aggiungendo "ABSOLUTELY NO TEXT, NO LETTERS, NO NUMBERS" all'inizio del prompt. Funziona quasi sempre.
- Se l'arancione finisce in posti decorativi (sbagliato), aggiungi al negative prompt "orange used decoratively, multiple orange elements". Riprova.
- Se l'isometrica viene troppo "renderizzata 3D" e non hand-drawn, aggiungi al prompt "absolutely flat 2D, no perspective shading, no rendering, line drawing only".
- Quando sei in dubbio se un'immagine è "abbastanza buona", chiediti: *sta facendo dire al pubblico "minchia un fenomeno quel Rocco" o "bella slide"?*. Se non è il primo, rigenera.
