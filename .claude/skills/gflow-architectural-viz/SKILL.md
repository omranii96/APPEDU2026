---
name: gflow-architectural-viz
description: Produce photorealistic architectural renders, walkthrough videos, before/after transformations, and real estate marketing. Use when the user wants interior or exterior renders, real estate marketing, walkthrough videos, or design presentations.
type: flexible
version: 1.1.1
foundation: false
consumes: [gflow-brand-identity]
tools: [gflow-cli]
---

# Architectural Viz

Produces photorealistic architectural renders, walkthrough videos, before/after transformations, and real estate marketing assets.

Read `references/quality-gate.md` (mandatory, motion and anti-slop rules) before building.

## When to Use
Interior and exterior renders, real estate marketing, walkthrough videos, design presentations.

## Workflow

1. **Project brief** - capture building type, style (modern, classical, organic), location, and time of day.
2. **Verify session** - run `gflow doctor`. Pick one Flow project for the whole run and pass the same `--project <name>` plus `--no-headed` on every gflow command (reuse `--project <brand>` if a brand exists); split assets across projects only if the user explicitly asks.
3. **Exterior establishing shots** - `gflow image --model imagen-4 --ratio 16:9`.
4. **Interior scenes** - generate interiors with a consistent design language.
5. **Walkthrough video** - `gflow video --model veo-3.1-quality --duration 15`.
6. **Extended walkthrough (optional)** - for a longer continuous tour, grow the walkthrough with `gflow extend --media-id <clip>` (ids via `gflow media list`), repeating `--prompt "the camera continues into <next space>"` per room or area (about 7-8s each, 148s cap) and `--add-clip` to append other rendered walkthrough clips; continue later with `--scene <id>` from `gflow scene list`.
7. **Before/after transformations** - `gflow edit image` on base renders.
8. **Upscale** - upscale presentation shots with `--upscale 4k`.
9. **Deliver** - render set plus walkthrough video plus presentation deck assets.

## Domain Quality Checks
- Lighting realism: match time-of-day, orientation, and climate to the location.
- Material fidelity: concrete reads as concrete, glass as glass, no plastic sheen.
- Human-figure scale references and proportional furniture.
- Architect-standard camera angles: standing, bird's eye, worm's eye.
- Natural color grading, no HDR-overprocessed look.

## Inheriting brand
Inherit the brand system via `--project <brand>` (from gflow-brand-identity) so palette, signage, and presentation styling carry through the renders and deck.
