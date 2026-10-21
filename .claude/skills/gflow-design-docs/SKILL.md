---
name: gflow-design-docs
description: Build pitch decks, mood boards, and creative briefs with embedded AI visuals, output as HTML, PDF-ready, or Markdown with assets. Use when the user needs a pitch deck, mood board, creative brief, or style guide.
type: flexible
version: 1.0.1
foundation: false
consumes: [gflow-brand-identity]
tools: [gflow-cli]
---

# Design Docs

Builds pitch decks, mood boards, and creative briefs with embedded AI visuals. Outputs self-contained HTML, PDF-ready layouts, or Markdown plus an assets folder.

Read `references/quality-gate.md` (mandatory, motion and anti-slop rules) before building.

## When to Use
Pitch decks, mood boards, creative briefs, style guides.

## Workflow

1. **Doc brief** - capture type (deck, moodboard, or brief), audience, and brand context.
2. **Verify session** - run `gflow doctor`. Pick one Flow project for the whole run and pass the same `--project <name>` plus `--no-headed` on every gflow command (reuse `--project <brand>` if a brand exists); split assets across projects only if the user explicitly asks.
3. **Generate section illustrations** - `gflow image` per section (use `--project <brand>` if a brand exists).
4. **Build the document** - clear typographic hierarchy on a 12-column grid with generous py-24+ spacing between sections.
5. **Apply the brand system** - if a gflow-brand-identity run exists, apply its colors, fonts, and logo placement.
6. **Output** - self-contained HTML or Markdown plus an assets folder.
7. **Copy audit** - ban filler verbs, em-dashes, and generic claims in all copy.

## Domain Quality Checks
- Display + body font pairing, not Inter alone.
- One focal point per spread with a clear reading path.
- Generous white space.
- No filler verbs in copy.

## Inheriting the brand
Inherit the brand system via `--project <brand>` so colors, fonts, and logo placement match the brand.
