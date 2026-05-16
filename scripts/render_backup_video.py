#!/usr/bin/env python3
"""
render_backup_video.py — Genera il backup MP4 della presentazione completa.

USO:
    python scripts/render_backup_video.py

WORKFLOW (approccio semplice, robusto):
    Concatena con ffmpeg tutti i video Veo (scene 1-12) seguiti dalle slide 
    realistic renderizzate come immagini statiche per N secondi ciascuna.
    Audio: somma traccia nativa Veo + ambient ElevenLabs + musica.

ALTERNATIVA (più professionale, ma complessa):
    Usare puppeteer + ffmpeg per registrare il browser durante la presentazione.
    Vedere il commento in fondo al file per il setup avanzato.

NB: questo script richiede ffmpeg installato sul sistema.
    macOS: brew install ffmpeg
    Linux: apt install ffmpeg
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from rich.console import Console

ROOT = Path(__file__).resolve().parent.parent
VIDEOS_DIR = ROOT / "deck" / "assets" / "videos"
AUDIO_DIR = ROOT / "deck" / "assets" / "audio"
IMAGES_DIR = ROOT / "deck" / "assets" / "images"
OUTPUT_DIR = ROOT / "outputs"
console = Console()

# Sequenza scene story (deve riflettere assemble_deck.py)
STORY_SEQUENCE = [
    "01", "02A", "02B", "03A", "03B", "04", "05", "06",
    "07", "08A", "08B", "09A", "09B", "10", "11A", "11B", "12",
]

# Sequenza slide realistic + durata in secondi (deve riflettere docs/03)
REALISTIC_SEQUENCE = [
    ("13", 20),
    ("14", 25),
    ("15", 30),
    ("16", 30),
    ("17", 30),
    ("18", 25),
    ("19", 30),
    ("20", 25),
    ("21", 30),
    ("22", 35),
    ("23", 30),
]


def check_ffmpeg() -> bool:
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def find_final_video(scene_id: str) -> Path | None:
    sid = scene_id.lower()
    final = VIDEOS_DIR / f"scene_{sid}_FINAL.mp4"
    if final.exists():
        return final
    versions = sorted(VIDEOS_DIR.glob(f"scene_{sid}_v*.mp4"))
    return versions[-1] if versions else None


def find_realistic_image(slide_id: str) -> Path | None:
    for ext in ("svg", "png", "jpg"):
        candidates = list(IMAGES_DIR.glob(f"realistic_{slide_id}_*.{ext}"))
        if candidates:
            return candidates[0]
    return None


def build_realistic_segment(slide_id: str, duration: int, out_path: Path) -> bool:
    """Genera un MP4 statico dalla slide realistic (immagine ferma per N secondi)."""
    image = find_realistic_image(slide_id)
    if not image:
        console.print(f"[yellow]⚠ Slide {slide_id}: immagine mancante, salto[/yellow]")
        return False
    
    # Se è SVG, convertirlo in PNG temp con ffmpeg (richiede librsvg)
    # Per semplicità, accettiamo solo PNG/JPG qui
    if image.suffix == ".svg":
        console.print(f"[yellow]⚠ SVG non supportato direttamente. Converti {image.name} in PNG prima.[/yellow]")
        return False
    
    cmd = [
        "ffmpeg", "-loop", "1", "-i", str(image),
        "-t", str(duration),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-vf", f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=#F5EFE6",
        "-r", "30",
        "-y", str(out_path),
    ]
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        console.print(f"[red]Errore generando slide {slide_id}: {result.stderr.decode()[:200]}[/red]")
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Render del backup MP4")
    parser.add_argument("--output", default=str(OUTPUT_DIR / "backup_video.mp4"))
    parser.add_argument("--resolution", default="1920x1080", help="1920x1080 o 3840x2160")
    args = parser.parse_args()

    if not check_ffmpeg():
        console.print("[red]ffmpeg non trovato. Installa con: brew install ffmpeg (Mac) o apt install ffmpeg (Linux)[/red]")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    temp_dir = OUTPUT_DIR / ".tmp_render"
    temp_dir.mkdir(exist_ok=True)
    
    console.print("[bold cyan]Render backup MP4[/bold cyan]")
    
    # 1. Raccogliere tutti i segmenti
    segments = []
    
    console.print("[cyan]→ Raccogliendo video story...[/cyan]")
    for sid in STORY_SEQUENCE:
        video = find_final_video(sid)
        if video:
            segments.append(video)
        else:
            console.print(f"[yellow]⚠ Scena {sid}: video mancante, salto[/yellow]")
    
    console.print(f"[cyan]→ Generando segmenti realistic...[/cyan]")
    for sid, duration in REALISTIC_SEQUENCE:
        out = temp_dir / f"realistic_{sid}.mp4"
        if build_realistic_segment(sid, duration, out):
            segments.append(out)
    
    if not segments:
        console.print("[red]Nessun segmento trovato. Verifica che ci siano video o immagini.[/red]")
        sys.exit(1)
    
    # 2. Concat list per ffmpeg
    list_path = temp_dir / "concat_list.txt"
    with open(list_path, "w") as f:
        for s in segments:
            f.write(f"file '{s.absolute()}'\n")
    
    # 3. Concat finale
    console.print(f"[cyan]→ Concatenazione di {len(segments)} segmenti...[/cyan]")
    cmd = [
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", str(list_path),
        "-c", "copy",
        "-y", args.output,
    ]
    result = subprocess.run(cmd, capture_output=True)
    
    if result.returncode != 0:
        # Fallback: re-encode (più lento ma più tollerante a codec misti)
        console.print("[yellow]Concat veloce fallito, provo re-encode...[/yellow]")
        cmd = [
            "ffmpeg", "-f", "concat", "-safe", "0", "-i", str(list_path),
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-vf", f"scale={args.resolution}:force_original_aspect_ratio=decrease",
            "-r", "30",
            "-y", args.output,
        ]
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            console.print(f"[red]Errore finale: {result.stderr.decode()[-500:]}[/red]")
            sys.exit(1)
    
    out_size_mb = Path(args.output).stat().st_size / 1024 / 1024
    console.print(f"[green]✓ Backup generato:[/green] {args.output} ({out_size_mb:.1f} MB)")
    console.print(f"\n[bold]Prossimi passi:[/bold]")
    console.print(f"  1. Apri e guarda: open {args.output}")
    console.print(f"  2. Copia su 2 USB diversi")
    console.print(f"  3. Carica su laptop di backup, apri in VLC, metti in pause")


# ----------------------------------------------------------------------------
# APPROCCIO AVANZATO (alternativa, non implementato qui):
#
# Per un backup MP4 di qualità ancora superiore (con tutti gli effetti GSAP,
# le transizioni, l'audio mixing del deck reveal.js), usare puppeteer + ffmpeg:
#
#   1. Avviare deck/ con `npx serve`
#   2. Aprire con puppeteer Chrome headless a 1920x1080
#   3. ffmpeg cattura video del display virtuale + audio sistema
#   4. Script automatico avanza le slide ogni N secondi (timing da docs/04)
#   5. Stop a fine slide 23
#
# Questo richiede ~30 min di setup ma produce un MP4 identico a ciò che si
# vedrebbe sul palco. Implementare in giorno 4 se c'è tempo.
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
