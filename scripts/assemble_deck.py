#!/usr/bin/env python3
"""
assemble_deck.py. Assembla il deck Reveal.js dalla configurazione del progetto.

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

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from scene_overlays import SCENE_OVERLAYS
except ImportError:
    SCENE_OVERLAYS = {}

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

# NUOVO BRIEF Rocco: rimossa storia ciurma/mare (non e' piaciuta al pubblico
# di test). Presentazione diretta Conflavoro AI come rivoluzione del mondo
# del lavoro PMI italiano. Palette teal del brand kit originale.
#
# Le SCENE STORY sono state svuotate. Tutto il deck e' nella sezione realistic.
STORY_SCENES = []


# === LEGACY STORY (non in uso, conservata per restore eventuale) ===
_LEGACY_STORY_SCENES = [
    {"id": "01",  "title": "C'è sempre stata una ciurma",
     "caption": "Voi navigate da prima che si parlasse di tecnologia.",
     "cue": "Voce bassa. Pausa 3s prima."},
    {"id": "02A", "title": "Un sapere che vale ancora",
     "caption": "Ognuno ha un mestiere addosso. Anni nelle mani.",
     "cue": "Indica il pubblico. Tono caldo."},
    {"id": "03A", "title": "Le tempeste le conoscete",
     "caption": "Anni di norme che cambiano. Scadenze impossibili.",
     "cue": "Rallenta. Volume cresce sul suono."},
    {"id": "03B", "title": "Chi ha cicatrici sa navigare",
     "caption": "La differenza non è la fortuna. È l'esperienza.",
     "cue": "Frase chiave. 'Chi non ha cicatrici.'"},
    {"id": "04",  "title": "Ogni tempesta diventa metodo",
     "caption": "Quello che imparate resta. Diventa il vostro libro mastro.",
     "cue": "Ammorbidisci. Sguardo lungo."},
    {"id": "05",  "title": "Poi un giorno, un'isola",
     "caption": "Sull'orizzonte appare qualcosa che non era nei libri.",
     "cue": "Sussurra: 'E un giorno...' Pausa 2s."},
    {"id": "06",  "title": "Non si corre. Si studia.",
     "caption": "Chi sa il mestiere sbarca con cautela. Ascolta prima.",
     "cue": "Passo avanti. Calma assoluta."},
    {"id": "08A", "title": "Sulla sabbia, qualcosa brilla",
     "caption": "Trovano una bussola. Si accende. Arancione.",
     "cue": "SILENZIO 8s. Poi sussurra: 'Una bussola.'"},
    {"id": "08B", "title": "Non punta a nord",
     "caption": "Punta dove tu vuoi arrivare. Tu dici la rotta.",
     "cue": "Indica con la mano. Voce intensa."},
    {"id": "09A", "title": "Funziona solo per chi sa",
     "caption": "Nelle mani sbagliate brilla, ma non porta nulla.",
     "cue": "Pausa lunga. 'Funziona solo se sapete navigare.'"},
    {"id": "10",  "title": "Non si butta nulla, si aggiunge",
     "caption": "Tornano alla nave con la nuova bussola accanto alla vecchia.",
     "cue": "Tono fermo. Gesto: due mani vicine."},
    {"id": "11A", "title": "Altre navi sono ferme",
     "caption": "All'orizzonte chi non ha cercato l'isola. Non si muove.",
     "cue": "Sguardo lontano. Pausa 3s."},
    {"id": "11B", "title": "Due bussole, una rotta",
     "caption": "La vecchia dice da dove venite. La nuova dove andate.",
     "cue": "Voce piena. Crescendo."},
    {"id": "12",  "title": "Quella nave siamo noi",
     "caption": "Fine della storia. Adesso vi mostro la bussola vera.",
     "cue": "Passo avanti. Cambio registro. Sorridi."},
]

# Sequenza slide realistic. NUOVA STRUTTURA Conflavoro AI (5 piattaforme).
# Big number concettuali (NON tempi/numeri specifici come richiesto da Rocco).
# Bullet descrivono input/output concettuali, non quanto-veloci-siamo.
# caption + cue: stesso schema della story (chiarimento pubblico + delivery Rocco).
REALISTIC_SLIDES = [
    # =============== INTRO: chi siamo, perchè, il problema ===============
    {
        "id": "13", "title": "Siamo all'anno zero dell'AI",
        "big": "ANNO ZERO",
        "caption": "L'AI entra nel lavoro adesso. Consulenti, aziende, lavoratori, insieme.",
        "cue": "Tono diretto, voce piena. Pausa dopo 'pionieri'.",
        "bullets": [
            "L'AI nel lavoro inizia oggi. Per chi guida, chi opera, chi controlla.",
            "Chi la usa adesso costruisce un vantaggio vero per tutto il sistema.",
            "Possiamo guidare il cambiamento insieme. Non subirlo da soli.",
        ],
    },
    {
        "id": "14", "title": "Conflavoro AI",
        "big": "CHI",
        "caption": "Strumenti AI per chi consiglia, chi produce, chi lavora ogni giorno.",
        "cue": "Indica il logo. 'Costruita per voi.'",
        "bullets": [
            "Cinque piattaforme. Una visione: tempo restituito a tutto il sistema.",
            "Per chi consiglia, chi guida l'azienda, chi opera in reparto.",
            "Non assistenti generici. Strumenti pensati per il lavoro italiano.",
            "Costruite da chi ha visto le giornate di studi, aziende, dipendenti.",
        ],
    },
    {
        "id": "15", "title": "Il vero ladro è il tempo",
        "big": "TEMPO",
        "caption": "Ogni ora persa è un'ora tolta al cliente, all'impresa, alla persona.",
        "cue": "Rallenta. Sguardo al pubblico. 'Il vero ladro è il tempo.'",
        "bullets": [
            "Adempimenti, controlli, aggiornamenti di legge che non finiscono mai.",
            "Tempo tolto al cliente, all'azienda, al lavoratore, alla relazione.",
            "L'AI non sostituisce nessuno. Restituisce ore a tutti.",
        ],
    },

    # =============== 5 PIATTAFORME (presentate come 5 progetti per la nuova era) ===============
    {
        "id": "16", "title": "CRM-DVR",
        "big": "DVR",
        "caption": "Il documento di sicurezza pronto per il consulente, l'azienda, il lavoratore.",
        "cue": "Frase forte: 'Da 30 ore a 4 ore. Per ogni documento.'",
        "bullets": [
            "Il documento di sicurezza, completo e a norma, per studio, impresa e team.",
            "Da 15 o 30 ore a 2 o 4 ore. L'85 per cento del tempo torna a chi lavora.",
            "Si carica tutto in una volta. L'AI controlla, valida, cita la norma.",
            "Doppia firma di consulente e titolare. Ogni passaggio resta tracciato.",
        ],
    },
    {
        "id": "17", "title": "Project Manager con FALCO AI",
        "big": "PARLA",
        "caption": "Per chi guida progetti, chi coordina squadre, chi deve solo parlare.",
        "cue": "Alza energia. 'L'AI esegue, non si limita a suggerire.'",
        "bullets": [
            "L'AI non solo consiglia. Crea progetti, attività e riunioni davvero.",
            "Si comanda con la voce, in italiano. 'FALCO, crea il progetto.'",
            "Videoconferenze integrate. Trascrizione e riepilogo per tutta la squadra.",
            "Un'ora al giorno restituita a chi guida e a chi opera.",
        ],
    },
    {
        "id": "18", "title": "Preventivatore AI",
        "big": "AUTO",
        "caption": "Per chi propone, chi decide, chi firma. Dal contatto al contratto.",
        "cue": "Tono pratico. 'Niente più preventivi dimenticati nel cassetto.'",
        "bullets": [
            "Una registrazione, una mail, un appunto. L'AI ne fa un preventivo finito.",
            "Applica il listino, sceglie i servizi, prepara il documento per il cliente.",
            "Quando il cliente dice sì, il preventivo diventa contratto da firmare.",
            "Firma digitale integrata. Un solo flusso per chi propone e chi accetta.",
        ],
    },
    {
        "id": "19", "title": "VCS, la formazione che vale",
        "big": "AULA",
        "caption": "Formazione vera, valida per legge. Per chi forma, chi assume, chi impara.",
        "cue": "Voce ferma. 'La conformità non si spunta. Si garantisce.'",
        "bullets": [
            "A norma con Accordo Stato Regioni 2025 e Decreto Sicurezza 81.",
            "Il sistema blocca da solo ogni configurazione fuori legge.",
            "In aula l'AI ascolta e suggerisce al docente in tempo reale.",
            "Quiz a prova di furbizia. Attestato con QR di verifica pubblica.",
        ],
    },
    {
        "id": "20", "title": "Lead Search",
        "big": "CLIENTI",
        "caption": "Per chi cerca clienti, chi qualifica, chi chiude la trattativa.",
        "cue": "Frase chiave: 'Da una ricerca alla rubrica clienti in pochi minuti.'",
        "bullets": [
            "Trova nuovi clienti aziendali, in modo cento per cento legale.",
            "Cerca su Google, Registro Imprese, fonti pubbliche autorizzate.",
            "Per ogni azienda: mail, telefono, ruolo, settore e punteggio di affinità.",
            "Esporta dove serve: nei sistemi dello studio, in Excel, in CSV.",
        ],
    },

    # =============== SINTESI + METODO + CHIUSURA ===============
    {
        "id": "21", "title": "Cinque progetti, una visione",
        "big": "5",
        "caption": "Per ogni snodo del lavoro, uno strumento per chi consiglia e chi opera.",
        "cue": "Voce piena. 'Specifici. Italiani. Pensati per voi.'",
        "bullets": [
            "Ogni passaggio chiave ha il suo strumento AI dedicato.",
            "Strumenti specifici per consulenti, imprese e persone che lavorano.",
            "Non una scatola magica. Cinque progetti che si tengono insieme.",
        ],
    },
    {
        "id": "22", "title": "Come lo facciamo davvero",
        "big": "BMAD",
        "caption": "Un metodo semplice. Una mossa alla volta, provata con chi la userà.",
        "cue": "Calma. 'Niente effetti speciali. Niente promesse vuote.'",
        "bullets": [
            "Costruire, misurare, aggiustare, mettere in funzione.",
            "Una modifica alla volta, provata con consulenti, aziende, lavoratori.",
            "Niente effetti speciali. Niente promesse impossibili.",
            "Si avanza un passo per volta, con i piedi per terra.",
        ],
    },
    {
        "id": "23", "title": "L'era dell'AI inizia da voi",
        "big": "ADESSO",
        "caption": "Un sistema che cerca innovazione: consulenti, aziende, lavoratori, insieme.",
        "cue": "Voce calda. Pausa 3s prima di 'Grazie'.",
        "bullets": [
            "Anno zero. Adesso. Per chi consiglia, chi produce, chi lavora.",
            "Cinque progetti pronti. Una visione condivisa da tutto il sistema.",
            "L'AI non sostituisce nessuno. Rende protagonisti tutti.",
            "Entriamo insieme nella nuova era del lavoro italiano.",
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


def find_scene_lottie(scene_id: str) -> Path | None:
    """Trova animazione Lottie JSON per una scena (priorità sopra la foto)."""
    sid = scene_id.lower()
    lottie_dir = DECK_DIR / "assets" / "lottie"
    candidates = list(lottie_dir.glob(f"scene_{sid}.json"))
    return candidates[0] if candidates else None


def find_realistic_lottie(slide_id: str) -> Path | None:
    """Trova animazione Lottie JSON per una slide realistic."""
    lottie_dir = DECK_DIR / "assets" / "lottie"
    candidates = list(lottie_dir.glob(f"slide_{slide_id}.json"))
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
  <title>Dalla Scrivania all'Algoritmo. Rocco Di Tolla.</title>
  
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
  <script src="https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie.min.js"></script>
  <script src="js/synth_audio.js"></script>
  <script src="js/lottie_init.js"></script>
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
        <aside class="notes"><div class="cue-card">🎯 CUE: $cue</div>$notes</aside>
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
          <p class="r-caption" data-anim="caption">$caption</p>
        </div>
        <aside class="notes"><div class="cue-card">🎯 CUE: $cue</div>$notes</aside>
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
    lottie_path = find_scene_lottie(scene["id"])
    svg_anim_path = find_scene_animation_svg(scene["id"])
    photo_path = find_scene_photo(scene["id"])
    ambient, ambient_db = find_ambient_for_scene(scene["id"])
    notes = extract_speech_for(f"SCENA {scene['id']}")

    # Priorità: video MP4 > Lottie JSON > SVG procedurale animato (preferito,
    # racconta la storia con disegni dedicati) > Foto AI (fallback solo se SVG
    # mancante) > placeholder testuale.
    if video_path:
        rel_video = video_path.relative_to(DECK_DIR)
        body = f'''
        <video data-autoplay class="full-bleed-video"
               src="{rel_video}"
               preload="auto" playsinline></video>'''
    elif lottie_path:
        rel_lottie = lottie_path.relative_to(DECK_DIR)
        body = f'''
        <div class="full-bleed-lottie" data-lottie="{rel_lottie}"></div>'''
    elif svg_anim_path:
        # SVG procedurale: racconta la storia con animazioni dedicate
        svg_inline = inline_svg_content(svg_anim_path)
        body = f'''
        <div class="full-bleed-svg" data-anim-scene="{scene["id"]}">
          {svg_inline}
        </div>'''
        # Scene SVG: NON aggiungiamo overlay foto-style sopra (vignette/dust).
        # Le SVG hanno gia i propri overlay narrativi dentro.
        return STORY_SLIDE_TEMPLATE.substitute(
            id=scene["id"],
            title=scene.get("title", ""),
            caption=scene.get("caption", ""),
            cue=scene.get("cue", ""),
            body=body,
            notes=notes or f"[Speech per scena {scene['id']} non trovato in docs/04_SPEECH_SCRIPT.md]",
        )
    elif photo_path:
        # AI photo background (Pollinations) + overlay SVG specifico per scena.
        rel_photo = photo_path.relative_to(DECK_DIR)
        # Overlay dedicato per la scena (animazioni vere: lampi/onde/glow/particelle).
        # Fallback: vignette + dust generico se la scena non ha overlay dedicato.
        scene_overlay = SCENE_OVERLAYS.get(scene["id"].upper())
        if scene_overlay:
            overlay_html = f'<div class="photo-overlay">{scene_overlay}</div>'
        else:
            overlay_html = f'''
        <div class="photo-overlay">
          <svg viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid slice" class="photo-overlay-svg">
            <defs>
              <radialGradient id="vig_{scene["id"]}" cx="50%" cy="50%" r="78%">
                <stop offset="60%" stop-color="#000" stop-opacity="0"/>
                <stop offset="100%" stop-color="#000" stop-opacity="0.45"/>
              </radialGradient>
            </defs>
            <rect width="1920" height="1080" fill="url(#vig_{scene["id"]})" pointer-events="none"/>
          </svg>
        </div>'''
        body = f'''
        <div class="full-bleed-photo" style="background-image: url('{rel_photo}');"></div>
        {overlay_html}'''
    else:
        body = f'''
        <div class="placeholder-slide">
          <div class="placeholder-icon">⚠️</div>
          <h2>Scena {scene["id"]}. {scene["title"]}</h2>
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
        cue=scene.get("cue", ""),
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
    lottie_path = find_realistic_lottie(slide["id"])
    photo_path = find_realistic_photo(slide["id"])
    svg_anim_path = find_realistic_animation_svg(slide["id"])
    notes = extract_speech_for(f"SLIDE {slide['id']}")

    # Priorità slide realistic: PNG manuale > Lottie > SVG procedurale (preferito) > Foto AI
    if image_path:
        rel = image_path.relative_to(DECK_DIR)
        image_block = f'<div class="illustration"><img src="{rel}" alt="" /></div>'
    elif lottie_path:
        rel = lottie_path.relative_to(DECK_DIR)
        image_block = f'<div class="illustration lottie-illustration" data-lottie="{rel}"></div>'
    elif svg_anim_path:
        svg_inline = inline_svg_content(svg_anim_path)
        image_block = f'<div class="illustration svg-anim">{svg_inline}</div>'
    elif photo_path:
        rel = photo_path.relative_to(DECK_DIR)
        image_block = f'<div class="illustration photo-ai"><img src="{rel}" alt="" /></div>'
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
        caption=slide.get("caption", ""),
        cue=slide.get("cue", ""),
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
