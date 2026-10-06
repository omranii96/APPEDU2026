---
name: motion-design-hyperframes
description: Know-how for making agency-grade motion design videos (launch, promo, explainer, 30 to 60 s, voice-over) with HyperFrames (HTML + GSAP rendered to MP4) and the 5-step motion-design method. Use when the user asks for a motion design, an animated launch or promo video, a HyperFrames composition, a storyboard for an animated film, or asks about HyperFrames or the motion-design-claude-code method.
---

# Motion design with HyperFrames

The full synthesis (in French) is `docs/motion-design/README.md`. Read it before planning or writing any composition.
Sources: https://github.com/heygen-com/hyperframes (engine, Apache 2.0) and
https://github.com/cblain100-prog/motion-design-claude-code (method, MIT).

## How to work

1. **Workspace.** Films are not built in this repository. Clone the method repository (it pins HyperFrames 0.8.82 and
   ships the audited HeyGen skills), follow its `AGENTS.md`, and create each film with
   `bash .claude/skills/motion-design/scripts/new-project.sh <project> --fonts` (README § 7). Ask before installing
   anything large (Whisper, Chromium).
2. **Follow the 5 gated steps** (README § 2): script, voice (the user makes it on ElevenLabs; never ask for a key),
   storyboard (3 directions with styleframes, then `frame.md` and `STORYBOARD.md`), animation (pilot frame, then one
   sub-agent per sequence), music and sound effects. Stop for the user's approval after each one.
3. **Write the storyboard before animating**, with the 10 laws and the 15-point grid (README § 4): an event every 0.5
   to 1 s, a camera that never stops, a bridge object at every seam, elements that land too big and blurred, three
   depth levels, one thing to look at at a time, subtitles word by word at the bottom center.
4. **Respect the composition contract** (README § 1.2) and the render pitfalls (README § 5): one paused timeline
   registered after build, transforms only, everything inside `<template>` for sub-compositions, `opacity: 0` and
   `immediateRender: false` for anything that enters after t=0, no clocks or unseeded randomness.
5. **Check the real render** before saying it is done: `npx hyperframes check`, snapshots at every key image and
   seam, then the MP4 itself (black frames, freezes, duration, -16 LUFS).

## Guardrails

- Never run `npx hyperframes feedback`, `publish`, `cloud`, `lambda`, `cloudrun`, `auth`, `upgrade`, `skills update`,
  or `npx skills add` unless the user explicitly asks for that command. Keep telemetry off
  (`HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_SKIP_SKILLS=1 HYPERFRAMES_NO_UPDATE_CHECK=1`).
- Nothing leaves the machine (no upload, no publication) without an explicit request.
- Music is CC0, never generated; sound effects come from the `media-use` skill assets; fonts are OFL.
- When mixing the pinned method (0.8.82) with a newer HyperFrames, apply the differences in README § 6
  (`check` instead of `validate`, `--quality delivery`, `Math.floor` repeat counts).
