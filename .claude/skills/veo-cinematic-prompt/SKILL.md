---
name: veo-cinematic-prompt
description: Writes and refines Google Veo 3.1 video generation prompts for the "Dalla Scrivania all'Algoritmo" cinematic presentation. Use this skill whenever the user wants to create a new Veo prompt, refine an existing scene prompt, debug a scene that didn't generate well, or assemble the final prompt string from a scene JSON. The skill knows the project's style bible, the storyboard, the BMAD methodology, and the cost constraints — invoke it for any task involving prompts/veo/*.json files or Veo video generation in this project.
---

# Veo Cinematic Prompt — Skill

## Cosa fa questa skill

Aiuta Rocco a creare e raffinare i prompt Veo 3.1 per il progetto "Dalla Scrivania all'Algoritmo".
Garantisce che ogni prompt:
1. Rispetti il DNA visivo definito in `prompts/veo/00_style_bible.md`
2. Segua la struttura JSON del progetto
3. Includa lo style DNA e il negative prompt
4. Sia accompagnato da costi stimati e criteri di accettazione

## Quando si attiva

- "Crea il prompt per la scena XX"
- "Migliora il prompt della scena 03A"
- "La scena 8 non viene bene, aggiusta il prompt"
- "Genera la versione assembled del prompt per la scena 5"
- L'utente apre o modifica un file in `prompts/veo/`

## Workflow

### 1. Leggere il contesto

Prima di scrivere QUALSIASI prompt:
- Leggere `prompts/veo/00_style_bible.md` per il DNA visivo
- Leggere `docs/02_STORYBOARD.md` alla sezione della scena richiesta
- Leggere `docs/05_VISUAL_GUIDE.md` per la palette
- Se la scena esiste già come JSON, leggere la versione corrente

### 2. Strutturare il JSON

Ogni scena segue questo schema (mai deviare):

```json
{
  "scene_id": "XX",
  "scene_title": "...",
  "narrative_role": "...",
  "duration_seconds": 6-8,
  "aspect_ratio": "16:9",
  "resolution": "1080p",
  "model": "veo-3.1-generate-001",
  "audio_generation": true,
  "negative_prompt_ref": "00_style_bible.md::NEGATIVE_PROMPT",
  "style_dna_ref": "00_style_bible.md::STYLE_DNA",
  "prompt_components": {
    "shot_type": "...",
    "subject": "...",
    "action": "...",
    "environment": "...",
    "camera_movement": "...",
    "lighting": "...",
    "mood": "...",
    "audio_hint": "..."
  },
  "assembled_prompt_preview": "...",
  "estimated_cost_usd": 6.0,
  "max_regenerations_allowed": 3,
  "acceptance_criteria": ["...", "..."]
}
```

### 3. Vincoli non negoziabili

Ogni prompt **DEVE**:
- Avere `shot_type` da vocabolario consentito (vedi style bible: wide, medium, close-up, macro)
- Avere `camera_movement` mono-direzionale e lento
- Specificare se l'arancione narrativo `#FF6B1A` è presente E perché (deve essere narrativo, mai decorativo)
- Avere personaggi mai con volti chiaramente visibili (silhouette, backlight, dal dietro, o solo mani)
- Includere un `audio_hint` coerente con l'atmosfera della scena
- Avere almeno 3 `acceptance_criteria` verificabili

### 4. Costruire l'assembled_prompt_preview

L'assembled prompt è la stringa che effettivamente arriva all'API Veo. Si costruisce così:

```
[SHOT TYPE] of [SUBJECT] [ACTION] in [ENVIRONMENT]. 
Camera: [CAMERA MOVEMENT]. 
Lighting: [LIGHTING]. 
Mood: [MOOD]. 
Audio: [AUDIO HINT]. 
[STYLE_DNA injected as full block] 
[NEGATIVE_PROMPT injected]
```

Inserire un campo `assembled_prompt_preview` nel JSON con questa stringa già montata, così Rocco può leggere e approvare il prompt finale **prima** che lo script Python lo mandi all'API.

### 5. Costo e regenerazioni

- Scene normali: `max_regenerations_allowed: 3`
- Scene WOW (3A, 5, 8A): `max_regenerations_allowed: 5`
- Tracciare il costo: ogni clip da 8s in quality mode costa $6.

### 6. Output finale

Dopo aver creato/aggiornato il JSON:
1. Mostrarlo a Rocco con `view` del file
2. Spiegare cosa è cambiato rispetto alla versione precedente (se applicabile)
3. **NON eseguire** `generate_scene.py` senza esplicita autorizzazione di Rocco
4. Aggiornare la tabella in `prompts/veo/README.md` con lo status della scena

## Esempi di buon prompt (riferimento)

Vedi:
- `prompts/veo/scene_01_open_sea.json` — esempio di apertura calma
- `prompts/veo/scene_03a_storm.json` — esempio di scena drammatica
- `prompts/veo/scene_05_horizon_island.json` — esempio di scena mystery
- `prompts/veo/scene_08a_compass_lights_up.json` — esempio di scena WOW critica

## Errori comuni da evitare

| Errore | Perché è sbagliato | Cosa fare invece |
|---|---|---|
| Prompt con "happy people smiling" | I volti vanno mai mostrati chiari | "people in silhouette, seen from behind" |
| "Bright orange sunset everywhere" | L'arancione è narrativo | Solo dove la storia lo richiede |
| "Fast camera zoom" | Niente movimenti veloci | "slow dolly", "slow crane" |
| Audio_hint troppo generico ("music") | Veo non genera musica | Sound design specifico |
| Mancanza di acceptance criteria | Senza criteri non si sa se è OK | Almeno 3 criteri verificabili |
| Prompt con neon, cyberpunk, sci-fi | Stile cartone mythic | Cartone painterly tradizionale |

## Regola d'oro

> Se un prompt non rispetterebbe il DNA stilistico, **non si scrive**. Si chiede chiarimenti a Rocco e si aggiorna lo style bible prima.
