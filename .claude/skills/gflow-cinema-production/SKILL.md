---
name: gflow-cinema-production
description: Run a full short-film pipeline from storyboard to assembled clips with AI-generated scenes and consistent characters. Use when the user wants a short film, narrative video, branded story content, or a trailer.
type: flexible
version: 1.1.1
foundation: false
consumes: [gflow-brand-identity, gflow-character-pipeline]
tools: [gflow-cli]
---

# Cinema Production

Drives a full short-film pipeline from script breakdown and storyboard through per-scene video to assembled, numbered clips.

Read `references/quality-gate.md` (mandatory, motion and anti-slop rules) before building.

## When to Use
Short films, narrative video, branded story content, trailers.

## Workflow

1. **Script breakdown** - decompose the script into scenes, characters, locations, and mood per beat.
2. **Verify session** - run `gflow doctor`. Pick one Flow project for the whole run and pass the same `--project <name>` plus `--no-headed` on every gflow command (reuse `--project <brand>` if a brand exists); split assets across projects only if the user explicitly asks.
3. **Storyboard key frames** - `gflow image --model imagen-4 --ratio 16:9` for one or more key frames per scene.
4. **Approval gate** - present the storyboard; the user approves or requests revisions before any video renders.
5. **Per-scene video** - `gflow video --model veo-3.1-quality --duration 8 --ratio 16:9` for each approved scene.
6. **Character continuity** - pass `--character <name>` (from gflow-character-pipeline) so faces, wardrobe, and voice stay consistent across scenes.
7. **Transitions** - bridge scenes with `gflow video --start-frame <a> --end-frame <b>` so cuts flow rather than jump.
8. **Batch render** - render the full sequence via `gflow batch <file.yaml>`.
9. **Scene assembly** - chain the clips into one continuous film with `gflow extend`. Find the opening clip's id via `gflow media list`, start the scene with `gflow extend --media-id <id>`, then repeat `--prompt "<what happens next>"` per story beat (each extend adds roughly 7-8 seconds; a scene caps at 148 seconds, about 20 extends) and `--add-clip <media-id or name>` to append already-rendered scene clips in story order. The first run prints a scene id; continue the same timeline in later runs with `--scene <id>` (list existing scenes via `gflow scene list`). When the steps finish, the combined scene video downloads at full quality.
10. **Deliver** - numbered clips, the combined scene video, an assembly/edit guide, and the storyboard document.

## Domain Quality Checks
- Shot variety ratio: mix wide, medium, close-up, and detail shots across each sequence.
- Color-grade consistency across scenes.
- Character continuity holds across every scene.
- Pacing varies by emotional beat, not a uniform rhythm.
- Extend prompts describe what happens next inside the running shot (continuing motion, light, and subject), never a fresh scene description, so the extension reads as one take.
- Aspect ratio locked per project (16:9 or 2.35:1).

## Inheriting characters and brand
Inherit characters via `--character <name>` (from gflow-character-pipeline) and the brand system via `--project <brand>` so wardrobe, palette, and tone carry through the whole film.
