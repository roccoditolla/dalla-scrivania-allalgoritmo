#!/usr/bin/env python3
"""
assemble_deck.py — Assembla il deck Reveal.js dalla configurazione del progetto.

USO:
    python scripts/assemble_deck.py
    python scripts/assemble_deck.py --output deck/index.html

WORKFLOW:
    1. Legge la lista scene e slide dai docs
    2. Per ogni scena: cerca il video in deck/assets/videos/scene_<ID>_FINAL.mp4
       (fallback a v più alto disponibile)
    3. Per ogni slide realistic: cerca l'illustrazione in deck/assets/images/realistic_<NN>_*.svg
    4. Estrae le speech notes da docs/04_SPEECH_SCRIPT.md
    5. Genera deck/index.html

NB: i file di asset mancanti generano una slide placeholder evidente (non bloccante).
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from string import Template

try:
    from rich.console import Console as _RichConsole
    console = _RichConsole()
except ImportError:
    # Fallback: stampe colorate ANSI senza dipendenze
    class _PlainConsole:
        _RE = __import__('re').compile(r'\[/?[a-zA-Z0-9_ #]+\]')
        def print(self, msg=""):
            print(self._RE.sub('', str(msg)))
    console = _PlainConsole()

ROOT = Path(__file__).resolve().parent.parent
DECK_DIR = ROOT / "deck"
VIDEOS_DIR = DECK_DIR / "assets" / "videos"
AUDIO_DIR = DECK_DIR / "assets" / "audio"
IMAGES_DIR = DECK_DIR / "assets" / "images"
ANIMATIONS_DIR = DECK_DIR / "assets" / "animations"
DOCS_DIR = ROOT / "docs"
PROMPTS_DIR = ROOT / "prompts"

# Sequenza scene story (1-12) — IDs come da storyboard
STORY_SCENES = [
    {"id": "01",  "title": "Una ciurma in mare aperto",
     "caption": "I consulenti del lavoro navigano. Da sempre."},
    {"id": "02A", "title": "La ciurma sul ponte",
     "caption": "Ognuno con il suo mestiere. Anni di esperienza addosso."},
    {"id": "03A", "title": "La tempesta",
     "caption": "Hanno passato tempeste. Hanno imparato la rotta."},
    {"id": "03B", "title": "Il capitano nella tempesta",
     "caption": "Chi non ha cicatrici non sa navigare."},
    {"id": "04",  "title": "Dopo la tempesta",
     "caption": "Quello che hanno imparato resta. Diventa metodo."},
    {"id": "05",  "title": "Appare un'isola",
     "caption": "Un giorno appare qualcosa che non era nei libri."},
    {"id": "06",  "title": "Lo sbarco",
     "caption": "Chi sa navigare non si butta. Studia, poi decide."},
    {"id": "08A", "title": "La bussola si accende",
     "caption": "Sulla sabbia trovano una bussola. Arancione."},
    {"id": "08B", "title": "L'ago della bussola",
     "caption": "Non punta a nord. Punta dove tu vuoi arrivare."},
    {"id": "09A", "title": "La rivelazione",
     "caption": "Funziona solo in mano a chi sa già navigare."},
    {"id": "10",  "title": "Tornano alla nave",
     "caption": "Non gettano niente. Aggiungono. Bussola vecchia + nuova."},
    {"id": "11A", "title": "La nave salpa",
     "caption": "Altre navi all'orizzonte. Ferme. Non hanno ancora capito."},
    {"id": "11B", "title": "Due bussole sul ponte",
     "caption": "La vecchia dice da dove vieni. La nuova dove vuoi andare."},
    {"id": "12",  "title": "Anno zero",
     "caption": "Quella nave siamo noi. Adesso."},
]

# Sequenza slide realistic (13-25) — 7 piattaforme di prodotto.
# Big number concettuali (NON tempi/numeri specifici come richiesto da Rocco).
# Bullet descrivono input/output concettuali, non quanto-veloci-siamo.
REALISTIC_SLIDES = [
    {
        "id": "13", "title": "Anno zero", "big": "ANNO ZERO.",
        "bullets": [
            "Il presente, non la fantascienza",
            "Chi capisce l'AI prima costruisce un vantaggio",
            "Tre anni nel lavoro sono una vita",
        ],
    },
    {
        "id": "14", "title": "Conflavoro AI", "big": "7",
        "bullets": [
            "Sette piattaforme. Una visione.",
            "Per consulente, PMI e lavoratore",
            "Non chatbot. Strumenti specifici verticali",
            "Costruiti da chi ha visto la vostra giornata",
        ],
    },
    {
        "id": "15", "title": "Il problema", "big": "TEMPO",
        "bullets": [
            "Compliance, controlli, refresh normativo",
            "Tempo rubato al cliente, alla relazione, al mestiere",
            "L'AI libera il tempo, non lo sostituisce",
        ],
    },
    {
        "id": "16", "title": "Piattaforma DVR", "big": "RAPIDO",
        "bullets": [
            "Input: documento normativo + dati azienda",
            "Output: DVR validato, conforme, completo",
            "Non per togliere lavoro. Per ridarlo a chi conta.",
        ],
    },
    {
        "id": "17", "title": "Preventivatore", "big": "FIRMA",
        "bullets": [
            "Input: anagrafica cliente + listino dello studio",
            "Output: PDF impaginato pronto all'invio",
            "Il preventivo non aspetta più la settimana prossima",
        ],
    },
    {
        "id": "18", "title": "Lead Hunter", "big": "AGENDA",
        "bullets": [
            "Cerca, qualifica e contatta lead nei canali giusti",
            "Già attivo per noi e per il primo cliente",
            "Un agente che vi riempie l'agenda mentre dormite",
        ],
    },
    {
        "id": "19", "title": "Project Manager", "big": "360°",
        "bullets": [
            "Allinea l'organizzazione interna a 360°",
            "Velocizza l'operatività di tutto lo studio",
            "Pensa con voi. Non al posto vostro.",
        ],
    },
    {
        "id": "20", "title": "Falco AI", "big": "VOCE",
        "bullets": [
            "Agenti vocali che operano per conto dell'azienda",
            "Sotto agenti coordinati che lavorano come umani",
            "Si integra dentro il Project Manager",
            "L'azienda parla, gli agenti eseguono",
        ],
    },
    {
        "id": "21", "title": "Piattaforma HR", "big": "UNICO",
        "bullets": [
            "Busta paga, presenze, contratti, ferie, formazione",
            "Un sistema unico. Fine dell'Excel a sette schede",
            "Consulente, azienda e dipendente: stessa verità",
            "Il dipendente non è una riga di Excel",
        ],
    },
    {
        "id": "22", "title": "Videoconferenze ed eLearning", "big": "LIVE",
        "bullets": [
            "Videoconferenze GDPR + trascrizione automatica",
            "Salvataggio nel fascicolo del dipendente",
            "Formazione obbligatoria sempre disponibile",
            "La formazione smette di essere una scartoffia. Torna a essere un sapere.",
        ],
    },
    {
        "id": "23", "title": "Il pattern", "big": "7 bussole",
        "bullets": [
            "Ogni processo del lavoro ha il suo strumento AI",
            "Specifico. Verticale. Fatto da chi conosce il settore.",
            "Una bussola per ogni rotta che vi serve",
        ],
    },
    {
        "id": "24", "title": "Metodologia BMAD", "big": "BMAD",
        "bullets": [
            "Build. Measure. Adjust. Deploy.",
            "Una modifica alla volta, testata e confermata",
            "Niente big bang, niente promesse impossibili",
            "Si naviga in mare nuovo una bracciata alla volta",
        ],
    },
    {
        "id": "25", "title": "Chiusura", "big": "ADESSO.",
        "bullets": [
            "Anno zero. Adesso.",
            "Abbiamo trovato la nostra isola",
            "La bussola arancione è in mano nostra",
            "All'orizzonte altre navi ferme. La vostra no.",
        ],
    },
]


def find_scene_video(scene_id: str) -> Path | None:
    """Trova il video di una scena: prima FINAL, poi v più alta."""
    sid = scene_id.lower()
    final = VIDEOS_DIR / f"scene_{sid}_FINAL.mp4"
    if final.exists():
        return final
    versions = sorted(VIDEOS_DIR.glob(f"scene_{sid}_v*.mp4"))
    return versions[-1] if versions else None


def find_scene_animation_svg(scene_id: str) -> Path | None:
    """Trova SVG animato per una scena (fallback se manca MP4)."""
    sid = scene_id.lower()
    candidates = list(ANIMATIONS_DIR.glob(f"scene_{sid}_*.svg"))
    return candidates[0] if candidates else None


def find_scene_photo(scene_id: str) -> Path | None:
    """Trova foto-illustrazione AI (Pollinations) per una scena."""
    sid = scene_id.lower()
    photo_dir = DECK_DIR / "assets" / "images" / "scenes"
    candidates = list(photo_dir.glob(f"scene_{sid}.jpg"))
    candidates += list(photo_dir.glob(f"scene_{sid}.png"))
    return candidates[0] if candidates else None


def find_realistic_image(slide_id: str) -> Path | None:
    """Trova l'illustrazione PNG/SVG per una slide realistic (in deck/assets/images)."""
    candidates = list(IMAGES_DIR.glob(f"realistic_{slide_id}_*.svg"))
    candidates += list(IMAGES_DIR.glob(f"realistic_{slide_id}_*.png"))
    return candidates[0] if candidates else None


def find_realistic_animation_svg(slide_id: str) -> Path | None:
    """Trova SVG animato per una slide realistic (fallback se manca PNG/SVG generato)."""
    candidates = list(ANIMATIONS_DIR.glob(f"slide_{slide_id}_*.svg"))
    return candidates[0] if candidates else None


def find_realistic_photo(slide_id: str) -> Path | None:
    """Trova foto-illustrazione AI Pollinations per una slide realistic."""
    photo_dir = DECK_DIR / "assets" / "images" / "realistic"
    candidates = list(photo_dir.glob(f"slide_{slide_id}.jpg"))
    candidates += list(photo_dir.glob(f"slide_{slide_id}.png"))
    return candidates[0] if candidates else None


def inline_svg_content(svg_path: Path) -> str:
    """Legge un SVG e lo restituisce inline (senza la xml declaration)."""
    text = svg_path.read_text(encoding="utf-8")
    if text.startswith("<?xml"):
        text = text.split("?>", 1)[-1].lstrip()
    return text


def find_ambient_for_scene(scene_id: str) -> tuple[str | None, int | None]:
    """Trova (filename, volume_db) dell'audio ambient per una scena.

    Legge prompts/audio/audio_search.json (Pixabay/Freesound pipeline).
    Il campo `scene` può essere "01" o "03A_03B" (multi-scene): match per startswith
    e per inclusione del scene_id nella lista separata da '_'.
    """
    try:
        data = json.loads((PROMPTS_DIR / "audio" / "audio_search.json").read_text())
        for entry in data["audio_items"]:
            scenes_in_entry = entry.get("scene", "").split("_")
            if scene_id in scenes_in_entry or entry.get("scene", "") == scene_id:
                fname = entry["filename"]
                if (AUDIO_DIR / fname).exists():
                    return fname, entry.get("volume_db_in_deck")
    except Exception:
        pass
    return None, None


def extract_speech_for(marker: str) -> str:
    """Estrae il pezzo di speech da docs/04_SPEECH_SCRIPT.md per una scena/slide."""
    script_path = DOCS_DIR / "04_SPEECH_SCRIPT.md"
    if not script_path.exists():
        return ""
    text = script_path.read_text(encoding="utf-8")
    # Pattern semplificato: cerca "SCENA NN" o "SLIDE NN" come header
    pattern = rf"## (?:Durante )?{re.escape(marker)}.*?(?=## |\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0).strip()
    return ""


# ----------------------------------------------------------------------------
# HTML templates
# ----------------------------------------------------------------------------

DECK_TEMPLATE = Template("""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Dalla Scrivania all'Algoritmo — Rocco Di Tolla</title>
  
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.css" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/theme/black.css" id="theme" />
  <link rel="stylesheet" href="https://rsms.me/inter/inter.css" />
  <link rel="stylesheet" href="css/cinematic.css" />
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <!-- Slide 0: cover (logo Conflavoro AI) -->
      <section class="cover-slide">
        <h1>Dalla Scrivania all'Algoritmo</h1>
        <p class="subtitle">Rocco Di Tolla &mdash; Responsabile Conflavoro <span class="ai-accent">AI</span></p>
        <img class="cover-logo" src="assets/images/conflavoro_ai_logo.svg" alt="Conflavoro AI" />
        <p class="hint">Premere F per fullscreen, poi SPACE per iniziare</p>
      </section>

$story_slides

      <!-- Slide di ponte / transizione (12 → 13) gestita da CSS .bridge -->

$realistic_slides

      <!-- Slide finale: black + logo che pulsa -->
      <section class="end-slide" data-background-color="#1A1614">
        <div class="end-compass"></div>
      </section>
    </div>
  </div>

  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/dist/reveal.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@5.1.0/plugin/notes/notes.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
  <script src="js/synth_audio.js"></script>
  <script src="js/transitions.js"></script>
  <script>
    Reveal.initialize({
      width: 1920,
      height: 1080,
      margin: 0,
      minScale: 0.2,
      maxScale: 2.0,
      controls: true,
      progress: true,
      hash: true,
      slideNumber: 'c/t',
      transition: 'fade',
      transitionSpeed: 'default',
      backgroundTransition: 'fade',
      plugins: [ RevealNotes ]
    });
  </script>
</body>
</html>
""")


STORY_SLIDE_TEMPLATE = Template("""
      <section data-scene-id="$id" class="story-slide" data-background-color="#F5EFE6">
        $body
        <div class="story-caption">
          <h3 class="story-caption-title">$title</h3>
          <p class="story-caption-text">$caption</p>
        </div>
        <aside class="notes">$notes</aside>
      </section>""")


REALISTIC_SLIDE_TEMPLATE = Template("""
      <section data-slide-id="$id" class="realistic-slide" data-background-color="#F5EFE6">
        <div class="realistic-layout">
          <header class="r-header">
            <div class="big-number" data-anim="bignum">$big</div>
            <h2 class="r-title" data-anim="title">$title</h2>
          </header>
          <div class="r-body">
            <div class="r-visual" data-anim="visual">$image_block</div>
            <ul class="r-bullets">$bullets</ul>
          </div>
        </div>
        <aside class="notes">$notes</aside>
      </section>""")


BULLET_ITEM_TEMPLATE = Template('<li class="r-bullet" data-anim="bullet" data-i="$i"><span class="r-bullet-mark"></span><span class="r-bullet-text">$text</span></li>')


def build_story_slide_html(scene: dict) -> str:
    """
    Ordine di preferenza per il visual:
      1. MP4 video Veo finale (deck/assets/videos/scene_XX_FINAL.mp4)
      2. MP4 versione precedente (scene_XX_vN.mp4)
      3. JPG/PNG AI fotorealistic (deck/assets/images/scenes/scene_XX.jpg)
         con overlay SVG per movimento (particles, caption, transitions)
      4. SVG animato in-code (deck/assets/animations/scene_XX_*.svg)
      5. Placeholder testuale (ultima spiaggia)
    """
    video_path = find_scene_video(scene["id"])
    photo_path = find_scene_photo(scene["id"])
    svg_anim_path = find_scene_animation_svg(scene["id"])
    ambient, ambient_db = find_ambient_for_scene(scene["id"])
    notes = extract_speech_for(f"SCENA {scene['id']}")

    if video_path:
        rel_video = video_path.relative_to(DECK_DIR)
        body = f'''
        <video data-autoplay class="full-bleed-video"
               src="{rel_video}"
               preload="auto" playsinline></video>'''
    elif photo_path:
        # AI photo background (Pollinations) + overlay SVG per movimento.
        rel_photo = photo_path.relative_to(DECK_DIR)
        body = f'''
        <div class="full-bleed-photo" style="background-image: url('{rel_photo}');"></div>
        <div class="photo-overlay">
          <svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="photo-overlay-svg">
            <defs>
              <radialGradient id="vig_{scene["id"]}" cx="50%" cy="50%" r="78%">
                <stop offset="60%" stop-color="#000" stop-opacity="0"/>
                <stop offset="100%" stop-color="#000" stop-opacity="0.45"/>
              </radialGradient>
              <filter id="dustGlow_{scene["id"]}"><feGaussianBlur stdDeviation="3"/></filter>
            </defs>
            <rect width="1920" height="1080" fill="url(#vig_{scene["id"]})" pointer-events="none"/>
            <g class="dust-layer">
              <circle r="2.5" cx="320" cy="140" fill="#FFE9C2" filter="url(#dustGlow_{scene["id"]})">
                <animate attributeName="cy" values="140;680" dur="9s" repeatCount="indefinite"/>
                <animate attributeName="opacity" values="0;0.6;0" dur="9s" repeatCount="indefinite"/>
              </circle>
              <circle r="2" cx="780" cy="220" fill="#FFE9C2" filter="url(#dustGlow_{scene["id"]})">
                <animate attributeName="cy" values="220;780" dur="11s" repeatCount="indefinite"/>
                <animate attributeName="opacity" values="0;0.5;0" dur="11s" repeatCount="indefinite"/>
              </circle>
              <circle r="2.5" cx="1240" cy="180" fill="#FFE9C2" filter="url(#dustGlow_{scene["id"]})">
                <animate attributeName="cy" values="180;720" dur="13s" repeatCount="indefinite"/>
                <animate attributeName="opacity" values="0;0.55;0" dur="13s" repeatCount="indefinite"/>
              </circle>
              <circle r="2" cx="1620" cy="240" fill="#FFE9C2" filter="url(#dustGlow_{scene["id"]})">
                <animate attributeName="cy" values="240;820" dur="10s" repeatCount="indefinite"/>
                <animate attributeName="opacity" values="0;0.5;0" dur="10s" repeatCount="indefinite"/>
              </circle>
            </g>
          </svg>
        </div>'''
    elif svg_anim_path:
        # Fallback SVG animato in-code (zero costi, sempre disponibile)
        svg_inline = inline_svg_content(svg_anim_path)
        body = f'''
        <div class="full-bleed-svg" data-anim-scene="{scene["id"]}">
          {svg_inline}
        </div>'''
    else:
        body = f'''
        <div class="placeholder-slide">
          <div class="placeholder-icon">⚠️</div>
          <h2>Scena {scene["id"]} — {scene["title"]}</h2>
          <p>Asset visivo non ancora pronto.<br>
          File atteso: <code>deck/assets/videos/scene_{scene["id"].lower()}_FINAL.mp4</code>
          oppure <code>deck/assets/animations/scene_{scene["id"].lower()}_*.svg</code></p>
        </div>'''

    # Audio: MP3 prima, altrimenti synth fallback via data-attribute
    if ambient and (AUDIO_DIR / ambient).exists():
        db_attr = f' data-volume-db="{ambient_db}"' if ambient_db is not None else ''
        body += f'\n        <audio data-ambient{db_attr} src="assets/audio/{ambient}" loop></audio>'
    else:
        # transitions.js leggera questo attributo e attivera SynthAudio
        body += f'\n        <!-- audio fallback: SynthAudio per scena {scene["id"]} -->'

    return STORY_SLIDE_TEMPLATE.substitute(
        id=scene["id"],
        title=scene.get("title", ""),
        caption=scene.get("caption", ""),
        body=body,
        notes=notes or f"[Speech per scena {scene['id']} non trovato in docs/04_SPEECH_SCRIPT.md]",
    )


def build_realistic_slide_html(slide: dict) -> str:
    """
    Ordine preferenza illustrazione realistic:
      1. PNG/SVG da Gemini app (deck/assets/images/realistic_NN_*.png)
      2. SVG animato in-code (deck/assets/animations/slide_NN_*.svg)
      3. Placeholder testuale
    """
    image_path = find_realistic_image(slide["id"])
    photo_path = find_realistic_photo(slide["id"])
    svg_anim_path = find_realistic_animation_svg(slide["id"])
    notes = extract_speech_for(f"SLIDE {slide['id']}")

    if image_path:
        rel = image_path.relative_to(DECK_DIR)
        image_block = f'<div class="illustration"><img src="{rel}" alt="" /></div>'
    elif photo_path:
        rel = photo_path.relative_to(DECK_DIR)
        image_block = f'<div class="illustration photo-ai"><img src="{rel}" alt="" /></div>'
    elif svg_anim_path:
        svg_inline = inline_svg_content(svg_anim_path)
        image_block = f'<div class="illustration svg-anim">{svg_inline}</div>'
    else:
        image_block = f'''<div class="illustration placeholder">
          <p>Illustrazione mancante:<br>
          <code>deck/assets/images/realistic_{slide["id"]}_*.png</code></p>
        </div>'''

    bullets_html = "\n            ".join(
        BULLET_ITEM_TEMPLATE.substitute(i=i, text=b)
        for i, b in enumerate(slide.get("bullets", []))
    )

    return REALISTIC_SLIDE_TEMPLATE.substitute(
        id=slide["id"],
        big=slide["big"],
        title=slide["title"],
        image_block=image_block,
        bullets=bullets_html,
        notes=notes or f"[Speech per slide {slide['id']} non trovato]",
    )


def main():
    parser = argparse.ArgumentParser(description="Assembla il deck reveal.js")
    parser.add_argument("--output", default=str(DECK_DIR / "index.html"), help="Output path")
    args = parser.parse_args()

    console.print("[bold cyan]Assemblando deck reveal.js...[/bold cyan]")
    
    story_html = "\n".join(build_story_slide_html(s) for s in STORY_SCENES)
    realistic_html = "\n".join(build_realistic_slide_html(s) for s in REALISTIC_SLIDES)
    
    full_html = DECK_TEMPLATE.substitute(
        story_slides=story_html,
        realistic_slides=realistic_html,
    )
    
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(full_html, encoding="utf-8")
    
    # Report
    story_with_video = sum(1 for s in STORY_SCENES if find_scene_video(s["id"]))
    story_with_svg = sum(1 for s in STORY_SCENES if not find_scene_video(s["id"]) and find_scene_animation_svg(s["id"]))
    story_placeholder = len(STORY_SCENES) - story_with_video - story_with_svg

    realistic_with_image = sum(1 for s in REALISTIC_SLIDES if find_realistic_image(s["id"]))
    realistic_with_svg = sum(1 for s in REALISTIC_SLIDES if not find_realistic_image(s["id"]) and find_realistic_animation_svg(s["id"]))
    realistic_placeholder = len(REALISTIC_SLIDES) - realistic_with_image - realistic_with_svg

    console.print(f"[green]✓ Deck generato:[/green] {out_path}")
    console.print(f"  Story slides ({len(STORY_SCENES)}): {story_with_video} MP4 + {story_with_svg} SVG anim + {story_placeholder} placeholder")
    console.print(f"  Realistic slides ({len(REALISTIC_SLIDES)}): {realistic_with_image} PNG + {realistic_with_svg} SVG anim + {realistic_placeholder} placeholder")
    console.print(f"\n[cyan]Avvia il dev server:[/cyan] npx serve deck/ -l 8000")
    console.print(f"[cyan]Apri:[/cyan] http://localhost:8000")
    console.print(f"[cyan]Speaker view:[/cyan] premi [bold]S[/bold] dopo aver aperto")


if __name__ == "__main__":
    main()
