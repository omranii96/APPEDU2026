---
name: gflow-character-pipeline
description: Create consistent, reusable characters with defined visual identity, personality and voice using Google Flow. Use when the user wants to design a character, mascot, or recurring persona that should appear consistently across images and videos. Foundation skill, its characters are consumed by gflow-cinema-production, gflow-music-video, gflow-game-assets, gflow-social-content, and gflow-immersive-web.
type: flexible
version: 1.0.1
foundation: true
tools: [gflow-cli]
---

# Character Pipeline

Foundation skill. Produces a named, reusable Flow character with consistent visual identity. Downstream skills reference it via `gflow ... --character <name>`.

Read `references/quality-gate.md` and apply it to every generated image. Read `references/character-models.md` for model selection.

## When to Use
Creating a mascot, protagonist, recurring host, or any persona that must look the same across many generations.

## Workflow

1. **Gather the brief** - ask for: name, role/archetype, key visual traits, personality, intended use, and a voice direction. Ask one question at a time if the brief is thin.
2. **Verify tooling** - run `gflow doctor`. If it fails, stop and have the user run `gflow auth login`. Run every other gflow command in this run with the same `--project <name>` and `--no-headed` so all character assets land in one Flow project.
3. **Concept exploration** - generate 4-8 concept variations:
   `gflow image --id char-concept --prompt "<detailed character description>" --model nano-banana-pro --outputs 6 --out ./characters/<name>`
4. **Select direction** - present the variations, let the user pick the strongest. Iterate if needed.
5. **Create the character** - register it in Flow with the chosen reference images:
   `gflow character create --name "<name>" --prompt "<refined description>" --description "<personality>" --voice "<voice>" --model nano-banana-pro --image ./characters/<name>/<selected>.png`
6. **Validate consistency** - generate 2-3 test scenes placing the character in different settings; confirm the identity holds. Regenerate the character with better references if it drifts.
7. **Deliver** - output a character reference sheet (the selected images), the registered character name, and a usage note: "Reference this character downstream with `--character <name>`."

## Domain Quality Checks
- Silhouette is distinct and readable at thumbnail scale.
- Identity holds across at least 3 different poses/settings.
- Color palette and key features are consistent across all references.

## Outputs Consumed By
gflow-cinema-production, gflow-music-video, gflow-game-assets, gflow-social-content, gflow-immersive-web, gflow-editorial-design (via `--character <name>`).
