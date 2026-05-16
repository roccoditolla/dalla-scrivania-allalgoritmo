#!/usr/bin/env python3
"""
fetch_music.py — Cerca e scarica musica royalty-free da Pixabay Music.

USO:
    python scripts/fetch_music.py                    # cerca tutti i brief
    python scripts/fetch_music.py --id main_theme    # solo uno
    python scripts/fetch_music.py --preview          # mostra senza scaricare

WORKFLOW:
    1. Legge prompts/music/music_search.json
    2. Per ogni brief, cerca su Pixabay Music API
    3. Mostra a Rocco i top 5 risultati (titolo, autore, durata, mood, genre)
    4. Rocco sceglie quale scaricare (può anche dire "preview N" per ottenere URL ascolto)
    5. Salva l'MP3 in deck/assets/audio/<filename>
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
CONFIG_PATH = ROOT / "prompts" / "music" / "music_search.json"
AUDIO_DIR = ROOT / "deck" / "assets" / "audio"
load_dotenv(ROOT / ".env")
console = Console()

PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "").strip()


def search_pixabay_music(query: str, min_duration: int = 30, max_duration: int = 240, limit: int = 10) -> list[dict]:
    """Cerca tracce musicali su Pixabay Music API."""
    if not PIXABAY_API_KEY:
        console.print("[red]PIXABAY_API_KEY non trovata in .env[/red]")
        return []
    
    # Pixabay Music è cercabile via /api/music/ endpoint
    url = "https://pixabay.com/api/music/"
    params = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "per_page": limit,
    }
    
    try:
        r = requests.get(url, params=params, timeout=20)
        if r.status_code == 200:
            data = r.json()
            results = []
            for h in data.get("hits", []):
                duration = h.get("duration", 0)
                if min_duration <= duration <= max_duration:
                    results.append({
                        "id": h.get("id"),
                        "name": (h.get("name") or h.get("tags", "untitled")).strip()[:60],
                        "url": h.get("audio") or h.get("audio_url", ""),
                        "duration": duration,
                        "tags": h.get("tags", ""),
                        "user": h.get("user", ""),
                        "downloads": h.get("downloads", 0),
                    })
            return results
        else:
            console.print(f"[yellow]Pixabay Music: status {r.status_code}[/yellow]")
            console.print(f"[dim]{r.text[:200]}[/dim]")
    except Exception as e:
        console.print(f"[red]Errore Pixabay: {e}[/red]")
    
    return []


def download_audio(url: str, dest: Path) -> bool:
    try:
        r = requests.get(url, timeout=60, stream=True)
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        console.print(f"[red]Download fallito: {e}[/red]")
        return False


def show_and_pick(results: list[dict], target_filename: str) -> dict | None:
    if not results:
        console.print("[yellow]Nessun risultato.[/yellow]")
        return None
    
    table = Table(title=f"Pixabay Music — per: {target_filename}")
    table.add_column("#", style="cyan")
    table.add_column("Nome / tags", style="green")
    table.add_column("Durata", justify="right")
    table.add_column("Autore")
    table.add_column("Download", justify="right")
    
    for i, r in enumerate(results[:5], 1):
        table.add_row(
            str(i),
            r["name"] or r["tags"][:50],
            f"{r['duration']:.0f}s",
            r["user"],
            f"{r['downloads']}",
        )
    
    console.print(table)
    
    choice = Prompt.ask(
        "Quale? (1-5 per scegliere, 'preview N' per URL ascolto, 'skip' per saltare)",
        default="1",
    )
    
    if choice.lower() == "skip":
        return None
    if choice.lower().startswith("preview"):
        try:
            idx = int(choice.split()[1]) - 1
            console.print(f"[cyan]Apri per ascoltare:[/cyan] {results[idx]['url']}")
            return show_and_pick(results, target_filename)
        except (IndexError, ValueError):
            return show_and_pick(results, target_filename)
    
    try:
        idx = int(choice) - 1
        return results[idx] if 0 <= idx < len(results) else None
    except ValueError:
        return None


def fetch_one(entry: dict) -> bool:
    target_path = AUDIO_DIR / entry["filename"]
    
    if target_path.exists():
        if not Confirm.ask(f"{entry['filename']} esiste già. Sovrascrivo?", default=False):
            return False
    
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    
    console.print(f"\n[bold cyan]Brief: {entry['id']}[/bold cyan]")
    console.print(f"[dim]Descrizione: {entry.get('description', '')}[/dim]")
    
    # Pixabay accetta una query semplice. Combiniamo i tags principali.
    queries = entry.get("search_queries", [entry.get("description", entry["id"])])
    
    all_results = []
    for q in queries:
        console.print(f"[dim]Searching: '{q}'[/dim]")
        results = search_pixabay_music(
            q,
            min_duration=entry.get("min_duration", 30),
            max_duration=entry.get("max_duration", 240),
        )
        all_results.extend(results)
        time.sleep(0.3)
    
    # Dedup
    seen = set()
    unique = []
    for r in all_results:
        if r["id"] not in seen:
            seen.add(r["id"])
            unique.append(r)
    
    chosen = show_and_pick(unique, entry["filename"])
    if not chosen:
        return False
    
    console.print(f"[cyan]Scaricando '{chosen['name']}'...[/cyan]")
    if download_audio(chosen["url"], target_path):
        size_kb = target_path.stat().st_size / 1024
        console.print(f"[green]✓ Salvato: {target_path.name} ({size_kb:.1f} KB)[/green]")
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Cerca/scarica musica da Pixabay Music")
    parser.add_argument("--id", help="ID brief specifico")
    parser.add_argument("--preview", action="store_true", help="Mostra senza scaricare")
    args = parser.parse_args()

    if not CONFIG_PATH.exists():
        console.print(f"[red]Config non trovato: {CONFIG_PATH}[/red]")
        sys.exit(1)

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    briefs = config["music_briefs"]
    
    if args.id:
        briefs = [b for b in briefs if b["id"] == args.id]
        if not briefs:
            console.print(f"[red]ID '{args.id}' non trovato.[/red]")
            sys.exit(1)
    
    if args.preview:
        for b in briefs:
            console.print(f"\n[bold]{b['id']}[/bold] → {b['filename']}")
            console.print(f"  Descrizione: {b.get('description', '')}")
            console.print(f"  Queries: {b.get('search_queries', [])}")
        return

    success = 0
    for b in briefs:
        if fetch_one(b):
            success += 1
    
    console.print(f"\n[bold]{success}/{len(briefs)} tracce scaricate[/bold]")


if __name__ == "__main__":
    main()
