---
name: gflow-music-video
description: Build visual narratives for music with performance scenes, abstract visuals, story-driven sequences, and lyric imagery, produced as shot-by-shot clips to edit together. Use when the user wants a music video, lyric video, performance visuals, or abstract music visuals.
type: flexible
version: 1.1.1
foundation: false
consumes: [gflow-brand-identity, gflow-character-pipeline]
tools: [gflow-cli]
---

# Music Video

Builds visual narratives for music (performance scenes, abstract visuals, story-driven sequences, lyric video imagery) as shot-by-shot clips to edit together.

Read `references/quality-gate.md` (mandatory, motion and anti-slop rules) before building.

## When to Use
Music videos, lyric videos, performance visuals, abstract music visuals.

## Workflow

1. **Music brief** - capture genre, tempo and BPM, mood arc, lyric themes, and visual references.
2. **Verify session** - run `gflow doctor`. Pick one Flow project for the whole run and pass the same `--project <name>` plus `--no-headed` on every gflow command (reuse `--project <brand>` if a brand exists); split assets across projects only if the user explicitly asks.
3. **Structure breakdown** - map song sections (verse, chorus, bridge) to visual treatments.
4. **Performer character** - `gflow character create` if the video is narrative.
5. **Key-frame stills** - `gflow image` per section.
6. **Approval gate** - the user approves the visual direction per section.
7. **Per-section clips** - `gflow video --duration <matched to section length>`.
8. **Transitions** - bridge sections with `gflow video --start-frame <a> --end-frame <b>`.
9. **Batch render** - render the full video via `gflow batch <file.yaml>`.
10. **Assemble the cut** - build one continuous video with `gflow extend`: start from the opening clip (`gflow extend --media-id <id>`, ids via `gflow media list`), chain `--prompt "<what happens next>"` per musical beat (each extend adds roughly 7-8 seconds, scene cap 148 seconds) and append the section clips in song order with `--add-clip <media-id or name>`. Reuse the printed scene id with `--scene <id>` (see `gflow scene list`) to keep extending the same timeline across runs; the combined scene video downloads when done.
11. **Deliver** - numbered clips mapped to timestamps, the combined scene video, plus an edit guide.

## Domain Quality Checks
- Shot pacing mapped to musical structure.
- Mood escalation that builds with musical energy.
- Color storytelling: palette shifts between sections.
- Performer consistency via Flow characters.
- Every visual motivated by lyrical or musical content, no random abstract defaults.
- Aspect ratio 16:9 or 9:16.

## Inheriting characters and brand
Inherit the performer via `--character <name>` (from gflow-character-pipeline) and the look via `--project <brand>` (from gflow-brand-identity) so the performer and palette stay consistent across every clip.
