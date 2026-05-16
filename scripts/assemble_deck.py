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

from rich.console import Console

ROOT = Path(__file__).resolve().parent.parent
DECK_DIR = ROOT / "deck"
VIDEOS_DIR = DECK_DIR / "assets" / "videos"
AUDIO_DIR = DECK_DIR / "assets" / "audio"
IMAGES_DIR = DECK_DIR / "assets" / "images"
DOCS_DIR = ROOT / "docs"
PROMPTS_DIR = ROOT / "prompts"

console = Console()

# Sequenza scene story (1-12) — IDs come da storyboard
STORY_SCENES = [
    {"id": "01", "title": "Open Sea"},
    {"id": "02A", "title": "Ciurma sul ponte"},
    {"id": "02B", "title": "Mani al lavoro"},
    {"id": "03A", "title": "Tempesta — WOW 1"},
    {"id": "03B", "title": "Capitano nella tempesta"},
    {"id": "04", "title": "Mare calmo dopo"},
    {"id": "05", "title": "Isola appare — WOW 2"},
    {"id": "06", "title": "Sbarco"},
    {"id": "07", "title": "Mano sulla sabbia"},
    {"id": "08A", "title": "Bussola si accende — WOW 3"},
    {"id": "08B", "title": "Ago della bussola"},
    {"id": "09A", "title": "Cerchio attorno alla bussola"},
    {"id": "09B", "title": "Ago si ferma"},
    {"id": "10", "title": "Ritorno alla nave"},
    {"id": "11A", "title": "Nave salpa"},
    {"id": "11B", "title": "Due bussole sul ponte"},
    {"id": "12", "title": "Transizione al realistic"},
]

# Sequenza slide realistic (13-23)
REALISTIC_SLIDES = [
    {"id": "13", "title": "Anno zero", "big": "ANNO ZERO."},
    {"id": "14", "title": "Chi siamo", "big": "5"},
    {"id": "15", "title": "Il problema", "big": "60%"},
    {"id": "16", "title": "DVR Validator", "big": "12 min"},
    {"id": "17", "title": "AppaltoAI", "big": "200 → 4"},
    {"id": "18", "title": "LeadHunter AI", "big": "AUTO"},
    {"id": "19", "title": "Project Manager AI", "big": "PENSA"},
    {"id": "20", "title": "Videoconferenze + Welfare", "big": "PERSONE"},
    {"id": "21", "title": "Il pattern", "big": "5 bussole"},
    {"id": "22", "title": "Metodologia BMAD", "big": "BMAD"},
    {"id": "23", "title": "Chiusura", "big": "ADESSO."},
]


def find_scene_video(scene_id: str) -> Path | None:
    """Trova il video di una scena: prima FINAL, poi v più alta."""
    sid = scene_id.lower()
    final = VIDEOS_DIR / f"scene_{sid}_FINAL.mp4"
    if final.exists():
        return final
    versions = sorted(VIDEOS_DIR.glob(f"scene_{sid}_v*.mp4"))
    return versions[-1] if versions else None


def find_realistic_image(slide_id: str) -> Path | None:
    """Trova l'illustrazione per una slide realistic."""
    candidates = list(IMAGES_DIR.glob(f"realistic_{slide_id}_*.svg"))
    candidates += list(IMAGES_DIR.glob(f"realistic_{slide_id}_*.png"))
    return candidates[0] if candidates else None


def find_ambient_for_scene(scene_id: str) -> str | None:
    """Trova il filename dell'audio ambient per una scena."""
    try:
        data = json.loads((PROMPTS_DIR / "elevenlabs" / "ambient_sounds.json").read_text())
        for entry in data["ambient_sounds"]:
            if entry["scene"] == scene_id or entry["scene"].startswith(scene_id):
                fname = entry["filename"]
                if (AUDIO_DIR / fname).exists():
                    return fname
    except Exception:
        pass
    return None


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
      <!-- Slide 0: cover (logo) -->
      <section class="cover-slide">
        <div class="logo-mark"></div>
        <h1>Dalla Scrivania all'Algoritmo</h1>
        <p class="subtitle">Rocco Di Tolla — Eleven Digital and AI Consulting</p>
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
  <script src="js/transitions.js"></script>
  <script>
    Reveal.initialize({
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
      <section data-scene-id="$id" class="story-slide" data-background-color="#000000">
        $body
        <aside class="notes">$notes</aside>
      </section>""")


REALISTIC_SLIDE_TEMPLATE = Template("""
      <section data-slide-id="$id" class="realistic-slide" data-background-color="#F5EFE6">
        <div class="realistic-grid">
          <div class="big-number" data-gsap="fade-up">$big</div>
          $image_block
          <div class="caption">$title</div>
        </div>
        <aside class="notes">$notes</aside>
      </section>""")


def build_story_slide_html(scene: dict) -> str:
    video_path = find_scene_video(scene["id"])
    ambient = find_ambient_for_scene(scene["id"])
    notes = extract_speech_for(f"SCENA {scene['id']}")
    
    if video_path:
        rel_video = video_path.relative_to(DECK_DIR)
        body = f'''
        <video data-autoplay class="full-bleed-video"
               src="{rel_video}"
               preload="auto" playsinline></video>'''
        if ambient:
            body += f'\n        <audio data-ambient src="assets/audio/{ambient}" loop></audio>'
    else:
        # Placeholder slide
        body = f'''
        <div class="placeholder-slide">
          <div class="placeholder-icon">⚠️</div>
          <h2>Scena {scene["id"]} — {scene["title"]}</h2>
          <p>Video non ancora generato.<br>
          File atteso: <code>deck/assets/videos/scene_{scene["id"].lower()}_FINAL.mp4</code></p>
        </div>'''
    
    return STORY_SLIDE_TEMPLATE.substitute(
        id=scene["id"],
        body=body,
        notes=notes or f"[Speech per scena {scene['id']} non trovato in docs/04_SPEECH_SCRIPT.md]",
    )


def build_realistic_slide_html(slide: dict) -> str:
    image_path = find_realistic_image(slide["id"])
    notes = extract_speech_for(f"SLIDE {slide['id']}")
    
    if image_path:
        rel = image_path.relative_to(DECK_DIR)
        image_block = f'<div class="illustration" data-gsap="orange-glow"><img src="{rel}" alt="" /></div>'
    else:
        image_block = f'''<div class="illustration placeholder">
          <p>Illustrazione mancante:<br>
          <code>deck/assets/images/realistic_{slide["id"]}_*.svg</code></p>
        </div>'''
    
    return REALISTIC_SLIDE_TEMPLATE.substitute(
        id=slide["id"],
        big=slide["big"],
        title=slide["title"],
        image_block=image_block,
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
    missing_videos = sum(1 for s in STORY_SCENES if not find_scene_video(s["id"]))
    missing_images = sum(1 for s in REALISTIC_SLIDES if not find_realistic_image(s["id"]))
    
    console.print(f"[green]✓ Deck generato:[/green] {out_path}")
    console.print(f"  Story slides:     {len(STORY_SCENES)} (mancanti: {missing_videos} video)")
    console.print(f"  Realistic slides: {len(REALISTIC_SLIDES)} (mancanti: {missing_images} illustrazioni)")
    console.print(f"\n[cyan]Avvia il dev server:[/cyan] npx serve deck/ -l 8000")
    console.print(f"[cyan]Apri:[/cyan] http://localhost:8000")
    console.print(f"[cyan]Speaker view:[/cyan] premi [bold]S[/bold] dopo aver aperto")


if __name__ == "__main__":
    main()
