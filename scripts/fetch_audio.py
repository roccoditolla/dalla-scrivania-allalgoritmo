#!/usr/bin/env python3
"""
fetch_audio.py — Scarica SFX e ambient da Pixabay (primario) e Freesound (fallback).

USO:
    python scripts/fetch_audio.py --all                # scarica tutto il config
    python scripts/fetch_audio.py --id 01_ocean_dawn   # solo un audio
    python scripts/fetch_audio.py --source freesound --id 08_compass_shimmer
    python scripts/fetch_audio.py --preview            # mostra cosa scaricherebbe senza scaricare

WORKFLOW:
    1. Legge prompts/audio/audio_search.json
    2. Per ogni entry, cerca su Pixabay con i query terms
    3. Se non trova nulla di buono, fallback su Freesound (filtro CC0/CC-BY)
    4. Mostra a Rocco i top 3 risultati con metadati
    5. Rocco sceglie quale scaricare (o "skip")
    6. Salva l'MP3 in deck/assets/audio/<filename>

NB: Pixabay è preferito perché:
    - Licenza permissiva (no attribuzione richiesta)
    - Sicuro per uso commerciale
    - API illimitata e veloce
    
    Freesound è fallback per suoni specifici (es. shimmer magici)
    che Pixabay potrebbe non avere. Filtriamo per CC0 (zero hassle).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm, Prompt

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "prompts" / "audio" / "audio_search.json"
AUDIO_DIR = ROOT / "deck" / "assets" / "audio"
load_dotenv(ROOT / ".env")
console = Console()

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "").strip()
FREESOUND_API_KEY = os.getenv("FREESOUND_API_KEY", "").strip()


def search_pixabay(query: str, min_duration: int = 0, max_duration: int = 30, limit: int = 10) -> list[dict]:
    """Cerca SFX su Pixabay. Ritorna lista di {id, name, url, duration, downloads}."""
    if not PIXABAY_API_KEY:
        console.print("[red]PIXABAY_API_KEY non trovata in .env[/red]")
        return []
    
    url = "https://pixabay.com/api/"
    params = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "media_type": "music",  # Pixabay tratta SFX e music in modo simile
        "per_page": limit,
    }
    
    try:
        # Pixabay ha endpoint diversi per audio vs music vs sound_effects
        # Proviamo sound_effects prima
        sfx_url = "https://pixabay.com/api/sound-effects/"
        r = requests.get(sfx_url, params=params, timeout=15)
        if r.status_code == 200:
            data = r.json()
            return [
                {
                    "id": h.get("id"),
                    "name": h.get("tags", "").split(",")[0][:60].strip(),
                    "url": h.get("audio", h.get("preview_url", "")),
                    "duration": h.get("duration", 0),
                    "downloads": h.get("downloads", 0),
                    "source": "pixabay",
                }
                for h in data.get("hits", [])
                if min_duration <= h.get("duration", 0) <= max_duration
            ]
    except Exception as e:
        console.print(f"[yellow]Pixabay SFX endpoint error: {e}[/yellow]")
    
    return []


def search_freesound(query: str, min_duration: int = 0, max_duration: int = 30, limit: int = 10) -> list[dict]:
    """Cerca su Freesound filtrando CC0/CC-BY. Ritorna lista di {id, name, url, duration, license}."""
    if not FREESOUND_API_KEY:
        console.print("[yellow]FREESOUND_API_KEY non trovata, salto fallback Freesound.[/yellow]")
        return []
    
    url = "https://freesound.org/apiv2/search/text/"
    params = {
        "query": query,
        "filter": f"duration:[{min_duration} TO {max_duration}] license:(\"Creative Commons 0\" OR \"Attribution\")",
        "sort": "rating_desc",
        "fields": "id,name,previews,duration,license,username",
        "page_size": limit,
        "token": FREESOUND_API_KEY,
    }
    
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            data = r.json()
            return [
                {
                    "id": h.get("id"),
                    "name": h.get("name", "")[:60],
                    "url": h.get("previews", {}).get("preview-hq-mp3", ""),
                    "duration": h.get("duration", 0),
                    "downloads": 0,
                    "license": h.get("license", ""),
                    "author": h.get("username", ""),
                    "source": "freesound",
                }
                for h in data.get("results", [])
            ]
    except Exception as e:
        console.print(f"[yellow]Freesound error: {e}[/yellow]")
    
    return []


def download_audio(url: str, dest: Path) -> bool:
    try:
        r = requests.get(url, timeout=30, stream=True)
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        console.print(f"[red]Download fallito: {e}[/red]")
        return False


def show_results_and_pick(results: list[dict], target_filename: str) -> dict | None:
    """Mostra una tabella e chiede a Rocco quale scegliere."""
    if not results:
        console.print("[yellow]Nessun risultato trovato.[/yellow]")
        return None
    
    table = Table(title=f"Risultati per: {target_filename}")
    table.add_column("#", style="cyan", no_wrap=True)
    table.add_column("Source")
    table.add_column("Name", style="green")
    table.add_column("Durata", justify="right")
    table.add_column("Popolarità/License")
    
    for i, r in enumerate(results[:5], 1):
        pop = f"{r['downloads']} dl" if r["source"] == "pixabay" else r.get("license", "")
        table.add_row(
            str(i),
            r["source"],
            r["name"],
            f"{r['duration']:.1f}s",
            pop,
        )
    
    console.print(table)
    
    choice = Prompt.ask(
        "Quale scegli? (1-5, 'skip' per saltare, 'preview N' per ascoltare)",
        default="1",
    )
    
    if choice.lower() == "skip":
        return None
    if choice.lower().startswith("preview"):
        try:
            idx = int(choice.split()[1]) - 1
            console.print(f"[cyan]Apri questo URL per ascoltare:[/cyan]")
            console.print(results[idx]["url"])
            return show_results_and_pick(results, target_filename)
        except (IndexError, ValueError):
            return show_results_and_pick(results, target_filename)
    
    try:
        idx = int(choice) - 1
        return results[idx] if 0 <= idx < len(results) else None
    except ValueError:
        return None


def fetch_one(entry: dict, force_source: str | None = None) -> bool:
    """Scarica un singolo audio. Ritorna True se ha avuto successo."""
    target_path = AUDIO_DIR / entry["filename"]
    
    if target_path.exists():
        if not Confirm.ask(f"{entry['filename']} esiste già. Sovrascrivo?", default=False):
            console.print(f"[dim]  skip[/dim]")
            return False
    
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    
    console.print(f"\n[bold cyan]Cercando: {entry['id']}[/bold cyan]")
    console.print(f"[dim]Query: {entry['query']}[/dim]")
    
    # Strategia: Pixabay prima, Freesound se non trova
    results = []
    
    if force_source != "freesound":
        results = search_pixabay(
            entry["query"],
            min_duration=entry.get("min_duration", 0),
            max_duration=entry.get("max_duration", 30),
        )
    
    if not results or force_source == "freesound":
        results.extend(search_freesound(
            entry["query"],
            min_duration=entry.get("min_duration", 0),
            max_duration=entry.get("max_duration", 30),
        ))
    
    chosen = show_results_and_pick(results, entry["filename"])
    if not chosen:
        return False
    
    console.print(f"[cyan]Scaricando da {chosen['source']}...[/cyan]")
    if download_audio(chosen["url"], target_path):
        size_kb = target_path.stat().st_size / 1024
        console.print(f"[green]✓ Salvato: {target_path.name} ({size_kb:.1f} KB)[/green]")
        
        # Se Freesound, ricordiamo l'attribuzione
        if chosen["source"] == "freesound":
            attr_path = AUDIO_DIR / "ATTRIBUTIONS.md"
            with open(attr_path, "a") as f:
                f.write(
                    f"\n- **{entry['filename']}** — by {chosen.get('author', 'n/a')} "
                    f"on Freesound, license: {chosen.get('license', 'CC')}"
                )
            console.print(f"[dim]  Attribuzione aggiunta in ATTRIBUTIONS.md[/dim]")
        
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Scarica SFX da Pixabay/Freesound")
    parser.add_argument("--id", help="ID singolo (es. 01_ocean_dawn)")
    parser.add_argument("--all", action="store_true", help="Scarica tutti")
    parser.add_argument("--source", choices=["pixabay", "freesound"], help="Forza una sorgente")
    parser.add_argument("--preview", action="store_true", help="Mostra cosa farebbe senza scaricare")
    args = parser.parse_args()

    if not args.id and not args.all:
        console.print("[red]Usa --id <ID> oppure --all[/red]")
        sys.exit(1)

    if not CONFIG_PATH.exists():
        console.print(f"[red]Config non trovato: {CONFIG_PATH}[/red]")
        sys.exit(1)

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    entries = config["audio_items"]
    
    if args.id:
        entries = [e for e in entries if e["id"] == args.id]
        if not entries:
            console.print(f"[red]ID '{args.id}' non trovato.[/red]")
            console.print("Disponibili:")
            for e in config["audio_items"]:
                console.print(f"  - {e['id']}")
            sys.exit(1)

    console.print(f"[bold]Target: {len(entries)} audio[/bold]")
    
    if args.preview:
        for e in entries:
            console.print(f"  → {e['id']} | query: '{e['query']}' | dur: {e.get('min_duration', 0)}-{e.get('max_duration', 30)}s")
        return

    success = 0
    for e in entries:
        if fetch_one(e, force_source=args.source):
            success += 1
        time.sleep(0.3)  # rate limit gentile
    
    console.print(f"\n[bold]{success}/{len(entries)} audio scaricati[/bold]")


if __name__ == "__main__":
    main()
