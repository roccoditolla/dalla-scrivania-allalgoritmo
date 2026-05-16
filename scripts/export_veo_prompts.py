#!/usr/bin/env python3
"""
export_veo_prompts.py — Esporta i prompt Veo in formato pronto per Gemini app.

USO:
    python scripts/export_veo_prompts.py                  # tutti
    python scripts/export_veo_prompts.py --scene 01       # solo una scena
    python scripts/export_veo_prompts.py --batch dayN     # solo le scene del giorno N (1-5)

OUTPUT:
    outputs/veo_prompts_for_gemini.md  — markdown navigabile con tutti i prompt
    
WORKFLOW:
    1. Legge prompts/veo/00_style_bible.md per STYLE_DNA + NEGATIVE_PROMPT
    2. Per ogni scena: legge il JSON, assembla il prompt finale, lo formatta
    3. Genera un markdown con:
       - Titolo scena + ID + durata
       - Prompt copy-paste ready (in code block)
       - Negative prompt (in code block)
       - Acceptance criteria (checklist)
       - Spazio per appunti
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from rich.console import Console

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts" / "veo"
OUTPUTS_DIR = ROOT / "outputs"
console = Console()

# Sequenza scene ufficiale + giornate di lavoro suggerite
SCENE_SEQUENCE = [
    {"id": "01", "day": 1, "priority": "validation"},
    {"id": "02A", "day": 2, "priority": "normal"},
    {"id": "02B", "day": 2, "priority": "normal"},
    {"id": "03A", "day": 2, "priority": "wow_1"},
    {"id": "03B", "day": 2, "priority": "normal"},
    {"id": "04", "day": 3, "priority": "normal"},
    {"id": "05", "day": 1, "priority": "wow_2"},   # validation early
    {"id": "06", "day": 3, "priority": "normal"},
    {"id": "07", "day": 3, "priority": "setup_wow"},
    {"id": "08A", "day": 1, "priority": "wow_3_critical"},  # validation early
    {"id": "08B", "day": 3, "priority": "normal"},
    {"id": "09A", "day": 3, "priority": "normal"},
    {"id": "09B", "day": 3, "priority": "normal"},
    {"id": "10", "day": 4, "priority": "normal"},
    {"id": "11A", "day": 4, "priority": "normal"},
    {"id": "11B", "day": 4, "priority": "normal"},
    {"id": "12", "day": 4, "priority": "tricky"},
]


def load_style_bible() -> tuple[str, str]:
    """Estrae STYLE_DNA e NEGATIVE_PROMPT dal file 00_style_bible.md."""
    bible_path = PROMPTS_DIR / "00_style_bible.md"
    text = bible_path.read_text(encoding="utf-8")

    def extract_block(marker: str) -> str:
        start = text.find(f"## {marker}")
        if start == -1:
            return f"[{marker} block not found in style_bible.md]"
        block_start = text.find("```", start)
        block_end = text.find("```", block_start + 3)
        return text[block_start + 3 : block_end].strip()

    return extract_block("STYLE_DNA"), extract_block("NEGATIVE_PROMPT")


def find_scene_file(scene_id: str) -> Path | None:
    sid = scene_id.lower()
    candidates = list(PROMPTS_DIR.glob(f"scene_{sid}_*.json"))
    return candidates[0] if candidates else None


def assemble_prompt(scene_data: dict, style_dna: str) -> str:
    """Costruisce la stringa prompt finale per Gemini app."""
    p = scene_data["prompt_components"]
    return (
        f"{p['shot_type']} of {p['subject']} {p['action']} "
        f"in {p['environment']}. "
        f"Camera: {p['camera_movement']}. "
        f"Lighting: {p['lighting']}. "
        f"Mood: {p['mood']}. "
        f"Audio: {p['audio_hint']}. "
        f"\n\nStyle: {style_dna}"
    )


def format_scene_markdown(scene: dict, scene_data: dict, style_dna: str, negative: str) -> str:
    """Formatta una scena in markdown copy-paste ready."""
    full_prompt = assemble_prompt(scene_data, style_dna)
    
    priority_emoji = {
        "validation": "🎯",
        "wow_1": "🔥",
        "wow_2": "🔥",
        "wow_3_critical": "⭐⭐⭐",
        "setup_wow": "🌅",
        "tricky": "⚠️",
        "normal": "🎬",
    }.get(scene["priority"], "🎬")
    
    acceptance = scene_data.get("acceptance_criteria", [])
    acceptance_md = "\n".join(f"- [ ] {item}" for item in acceptance)
    
    critical_note = scene_data.get("_critical_note", "")
    critical_md = f"\n> ⚠️ **{critical_note}**\n" if critical_note else ""
    
    max_regen = scene_data.get("max_regenerations_allowed", 3)
    
    return f"""

---

## {priority_emoji} Scena {scene['id']} — {scene_data['scene_title']}

**Giorno consigliato:** {scene['day']}  
**Durata target:** {scene_data.get('duration_seconds', 8)}s  
**Aspect ratio:** {scene_data.get('aspect_ratio', '16:9')}  
**Max rigenerazioni:** {max_regen}  
**Ruolo narrativo:** {scene_data.get('narrative_role', '')}
{critical_md}

### 📋 Prompt da incollare in Gemini (Veo 3.1 Fast)

```
{full_prompt}
```

### 🚫 Negative prompt (da aggiungere se Gemini lo chiede o lo permette)

```
{negative}
```

### ✅ Acceptance criteria

{acceptance_md}

### 📝 Appunti dopo generazione

- Versione 1: ⬜ approvata ⬜ rigenerare
- Versione 2: ⬜ approvata ⬜ rigenerare
- Versione 3: ⬜ approvata ⬜ rigenerare

**File finale:** `deck/assets/videos/scene_{scene['id'].lower()}_FINAL.mp4`

"""


def main():
    parser = argparse.ArgumentParser(description="Esporta prompt Veo per Gemini app")
    parser.add_argument("--scene", help="ID scena specifica (es. 01)")
    parser.add_argument("--day", type=int, help="Esporta solo le scene di un giorno (1-5)")
    parser.add_argument("--output", default=str(OUTPUTS_DIR / "veo_prompts_for_gemini.md"))
    args = parser.parse_args()

    console.print("[bold cyan]Esportazione prompt Veo per Gemini app[/bold cyan]")
    
    style_dna, negative = load_style_bible()
    
    # Filtra scene
    target_scenes = SCENE_SEQUENCE
    if args.scene:
        target_scenes = [s for s in target_scenes if s["id"].lower() == args.scene.lower()]
    elif args.day:
        target_scenes = [s for s in target_scenes if s["day"] == args.day]
    
    if not target_scenes:
        console.print("[red]Nessuna scena trovata per i filtri specificati.[/red]")
        return
    
    # Header markdown
    md = f"""# Prompt Veo per Gemini App — Esportati

> Generato da `export_veo_prompts.py`  
> Scene incluse: {len(target_scenes)}  

## Come usare questo file

1. **Apri Gemini** (web app o mobile): https://gemini.google.com
2. **Verifica** che il modello sia su Veo 3.1 Fast (icona video, dovrebbe essere disponibile col tuo piano Pro)
3. **Per ogni scena** in ordine:
   - Copia il blocco "Prompt da incollare"
   - Incolla in Gemini
   - Aspetta ~60 secondi
   - Se ti piace: scarica MP4, rinomina come indicato, mettilo in `deck/assets/videos/`
   - Se non ti piace: usa il pulsante "rigenera" (1 tentativo del tuo daily quota)
4. **Limite Pro:** 3 video al giorno. Distribuisci le scene su 5 giorni.

## Tips per Veo 3.1 Fast

- L'audio nativo è incluso. Veo genera anche il sound dalla descrizione `Audio: ...`.
- Le scene con **volti chiari** vanno male su Veo. Tutti i nostri prompt evitano volti per design.
- Le scene con **molto movimento di camera** confondono Veo. I nostri prompt usano camere lente.
- Se Gemini propone di "ottimizzare" il prompt, **rifiuta** — il prompt è già curato.

---

# Le scene

"""
    
    for scene in target_scenes:
        scene_file = find_scene_file(scene["id"])
        if not scene_file:
            console.print(f"[yellow]⚠ Scena {scene['id']}: JSON non trovato[/yellow]")
            continue
        
        scene_data = json.loads(scene_file.read_text(encoding="utf-8"))
        md += format_scene_markdown(scene, scene_data, style_dna, negative)
    
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    
    console.print(f"[green]✓ Esportato:[/green] {out_path}")
    console.print(f"\n[bold]Prossimi passi:[/bold]")
    console.print(f"  1. Apri il file: open {out_path}")
    console.print(f"  2. Apri Gemini: https://gemini.google.com")
    console.print(f"  3. Incolla i prompt uno per uno, segui le acceptance criteria")
    console.print(f"  4. Salva gli MP4 in deck/assets/videos/ con il nome indicato")


if __name__ == "__main__":
    main()
