---
name: gflow-editorial-design
description: Create article illustrations, cover art, photo essays, and visual narratives with art-directed AI photography. Use when the user wants magazine layouts, article illustration, cover art, photo essays, or editorial features.
type: flexible
version: 1.1.1
foundation: false
consumes: [gflow-brand-identity]
tools: [gflow-cli]
---

# Editorial Design

Produces article illustrations, cover art, photo essays, and visual narratives with art-directed AI photography.

Read `references/quality-gate.md` (mandatory, motion and anti-slop rules) before building.

## When to Use
Magazine layouts, article illustration, cover art, photo essays, editorial features.

## Workflow

1. **Editorial brief** - capture article topic, tone, publication style, and visual references.
2. **Verify session** - run `gflow doctor`. Pick one Flow project for the whole run and pass the same `--project <name>` plus `--no-headed` on every gflow command (reuse `--project <brand>` if a brand exists); split assets across projects only if the user explicitly asks.
3. **Shot list** - define hero, supporting, detail, and atmosphere shots.
4. **Art direction** - set lighting, angle, color treatment, and concept per shot.
5. **Generate** - `gflow image --model imagen-4 --outputs 4` per shot.
6. **Curate and upscale** - select the best frames and upscale heroes with `--upscale 4k`.
7. **Motion pieces** - generate `gflow video` clips for digital editorial.
8. **Longer motion pieces (optional)** - if a digital feature calls for a longer sequence, extend a clip with `gflow extend --media-id <clip>` plus repeated `--prompt "<what happens next>"` (about 7-8s per extend) or `--add-clip` to combine rendered clips into one piece.
9. **Deliver** - image set plus art-direction notes and layout suggestions.

## Domain Quality Checks
- Every image has a concept and intent, not decoration.
- Images form a visual narrative when read in sequence.
- Text-image relationship is considered (overlap, inset, or flow).
- Push past generic AI photorealism toward deliberate editorial direction.
- Consistent visual treatment across the article or issue.

## Inheriting brand
Inherit the brand system via `--project <brand>` (from gflow-brand-identity) so palette, type pairing, and tone carry through the editorial.
