---
name: claude-club-motion-sites
description: Use when designing or building animated websites, landing pages, mobile apps, page sections, motion backgrounds, gradients, or design systems. Searches and applies the Claude Club library of 547 responsive motion recipes, including all 341 owner-authorized MotionSites prompts, matching HTML previews, imagery references, and reusable implementation patterns.
version: 1.0.0
author: Samin Yasar / Claude Club
license: MIT
metadata:
  hermes:
    tags: [web-design, animation, motion, landing-pages, mobile-apps, prompts, html]
    homepage: https://claude-club-sites.saminxd.chatgpt.site/
---

# Claude Club Motion Sites

## Overview

Use this library to move from a vague product idea to a specific, buildable motion direction. It contains **547 recipes**: 341 exact owner-authorized MotionSites prompts plus companion animated backgrounds, full-site templates, gradients, and a design-system recipe. Every recipe has a standalone responsive HTML implementation.

In this project the library root is `vendor/claude-club-motion-library/` (run `bash tools/motion-skills/fetch.sh libraries` once if it is missing). It contains:

- `library/library.json` — canonical searchable prompt catalog
- `library/manifest.json` — counts, filenames, and checksums
- `library/recipes/*.html` — 547 standalone implementations
- `skills/claude-club-motion-sites/references/recipe-index.json` — compact searchable index with media URLs
- `skills/claude-club-motion-sites/references/media-urls.txt` — complete imagery/video reference inventory
- `site/` — captured deployable site bundle

## When to Use

Use for:

- animated marketing sites, heroes, portfolios, SaaS pages, ecommerce, and launches
- mobile app screens and interaction concepts
- pricing, FAQ, CTA, feature, testimonial, footer, form, and dashboard sections
- motion backgrounds, gradients, and full-site visual systems
- finding a strong existing direction before coding from scratch

Do not use this as permission to copy third-party trademarks, logos, or copyrighted imagery. Replace brand-specific content and verify rights for external media before production use.

## Core Workflow

### 1. Search before choosing

From the repository root:

```bash
python3 skills/claude-club-motion-sites/scripts/search_library.py "luxury real estate hero" --limit 8
python3 skills/claude-club-motion-sites/scripts/search_library.py "pricing" --kind prompt --surface website
python3 skills/claude-club-motion-sites/scripts/search_library.py --list-kinds
```

Search title, category, tags, surface, pattern, and the full original prompt. Choose 3 candidates, not the first keyword hit. Completion criterion: each candidate has an ID and a stated reason it fits the product, audience, and interaction goal.

### 2. Inspect the exact source recipe

```bash
python3 skills/claude-club-motion-sites/scripts/search_library.py --id cc-prompt-181 --full
open library/recipes/cc-prompt-181-luxury-real-estate.html
```

Read the full prompt and run the HTML locally. Identify its layout, signature motion, visual assets, responsive behavior, and reduced-motion behavior. Completion criterion: the chosen direction is understood beyond its screenshot/title.

### 3. Adapt rather than blindly clone

Preserve the useful motion grammar while changing:

- copy, brand, information architecture, and CTA
- palette and typography where appropriate
- external media that is not owned or licensed
- interaction intensity for the actual audience and device

Keep one signature motion idea. Remove decorative effects that compete with reading or conversion. Completion criterion: the result feels specific to the new product rather than like a renamed template.

### 4. Build production structure

The HTML recipes are portable references, not a requirement to keep one-file architecture. Move production work into the project’s component system while preserving:

- semantic HTML and keyboard-accessible controls
- responsive behavior across phone and desktop
- `prefers-reduced-motion` handling
- GPU-friendly transforms/opacity where possible
- image dimensions, lazy loading, and appropriate formats
- no broken remote assets

Completion criterion: all interactions work with mouse, keyboard, and touch where relevant.

### 5. Verify visually and technically

Serve the result and inspect mobile and desktop sizes. Check console errors, overflow, contrast, focus states, reduced motion, and loading behavior. For a copied recipe:

```bash
python3 skills/claude-club-motion-sites/scripts/serve_recipe.py cc-prompt-181 --port 4173
```

Completion criterion: the requested page/section works in a real browser, not only as source code.

## Selection Heuristics

| Need | Prioritize |
|---|---|
| High-conversion SaaS | clear hierarchy, product proof, restrained motion, obvious CTA |
| Luxury/editorial | typography, pacing, negative space, material transitions |
| AI/futuristic | depth, grids, light fields, cursor response—without unreadable neon overload |
| Mobile app | touch targets, bottom navigation, compact hierarchy, gesture-safe motion |
| Portfolio/studio | project reveal, image choreography, memorable transition language |
| Background only | low CPU/GPU cost, low contrast behind copy, seamless loop |

## Imagery Workflow

Recipes preserve original media URLs. Inspect them for a selected recipe:

```bash
python3 skills/claude-club-motion-sites/scripts/search_library.py --id cc-prompt-001 --media
python3 skills/claude-club-motion-sites/scripts/fetch_media.py cc-prompt-001 --output ./reference-media
```

Treat downloaded media as reference material unless ownership/license is known. Keep attribution and source URLs when required. Prefer replacing fragile hotlinks with owned production assets.

## Working With Prompts

When using an `originalPrompt` with an AI coding agent:

1. Keep the prompt’s signature mechanic and concrete measurements.
2. Add the current project stack, path, and constraints.
3. State what must be changed (brand, copy, colors, assets).
4. Require real browser verification and reduced-motion support.
5. Do not let the agent stop after scaffolding.

A compact handoff:

```text
Use recipe <ID> as the visual/motion reference. Preserve <signature mechanic>.
Adapt it for <product and audience>. Replace all brand-specific copy and media.
Implement in <stack/path>. Keep responsive and reduced-motion behavior.
Run the app, verify phone + desktop, and report the tested URL and checks.
```

## Common Pitfalls

1. **Picking by title alone.** Search and inspect the full prompt and HTML.
2. **Combining too many recipes.** Use one primary direction and at most one supporting pattern.
3. **Publishing hotlinked imagery blindly.** Verify rights and availability or replace it.
4. **Motion over content.** Keep hierarchy and CTA legible before adding effects.
5. **Desktop-only QA.** Test narrow widths, touch behavior, and dynamic viewport height.
6. **Ignoring reduced motion.** Preserve a complete, attractive static state.
7. **Treating preview code as final architecture.** Refactor into the target stack and design system.

## Verification Checklist

- [ ] Searched the catalog and compared at least three candidates
- [ ] Chosen recipe ID and signature mechanic are documented
- [ ] Brand-specific copy and unlicensed imagery are replaced
- [ ] Mobile, desktop, keyboard, and touch behavior are checked
- [ ] `prefers-reduced-motion` produces a complete experience
- [ ] No console errors, broken assets, overflow, or inaccessible focus states
- [ ] Final artifact is run in a real browser and the tested result is reported
