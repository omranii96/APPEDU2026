---
name: gflow-brand-identity
description: Establish a complete brand visual system (colors, typography, imagery style, tone) and configure a Google Flow project so all downstream generation inherits the brand DNA. Use when the user wants brand guidelines, a visual identity, or a consistent look across all their creative output. Foundation skill consumed by every production skill via --project.
type: flexible
version: 1.0.1
foundation: true
tools: [gflow-cli]
---

# Brand Identity System

Foundation skill. Produces a brand guide plus a configured Flow project whose agent instructions enforce the brand look on every downstream generation.

Read `references/quality-gate.md` and apply it throughout. Use `assets/brand-template.yaml` as the brand guide structure.

## When to Use
Setting up a brand's visual language before producing any campaign, site, or content.

## Workflow

1. **Gather the brief** - industry, values, target audience, mood/adjectives, competitor references, any existing assets. One question at a time if thin.
2. **Verify tooling** - `gflow doctor`; if it fails, have the user run `gflow auth login`. Run every other gflow command with `--project <brand>` and `--no-headed` so all brand assets land in the one brand project.
3. **Mood exploration** - generate distinct visual directions:
   `gflow image --id brand-mood --prompt "<mood board concept>" --model imagen-4 --outputs 4 --out ./brand/<name>`
   Produce 3-4 genuinely different directions (not variations of one).
4. **Select direction** - present options, user picks. This locks the palette and mood.
5. **Build the system** - generate: logo concepts, a color palette board, and a pattern/texture set, all in the chosen direction.
6. **Scope a Flow project** - use `--project <brand>` for all brand work so assets stay grouped.
7. **Configure the agent** - encode the brand into persistent instructions:
   `gflow agent instruction add --text "All imagery uses <palette/mood/style descriptors>. Avoid <anti-patterns>."`
   `gflow agent settings --image-model imagen-4 --image-ratio 16:9`
8. **Deliver** - fill `assets/brand-template.yaml` with the decided values, export the asset library, and note: "Downstream skills inherit this brand via `--project <brand>`."

## Domain Quality Checks
- Exactly one accent color, derived from the chosen mood.
- Logo reads at small sizes; works on light and dark.
- Mood directions presented were genuinely distinct, not near-duplicates.

## Outputs Consumed By
All ten production skills via `--project <brand>` and the configured agent instructions.
