---
name: gflow-product-visuals
description: Produce studio-quality product photography and commercial imagery with lighting and composition inferred from the product type. Use when the user needs e-commerce shots, hero banners, lifestyle product scenes, or ad imagery.
type: flexible
version: 1.0.1
foundation: false
consumes: [gflow-brand-identity]
tools: [gflow-cli]
---

# Product Visuals

Generates studio-quality product photography and commercial imagery, reasoning lighting and composition from the product type.

Read `references/quality-gate.md` (mandatory, motion and anti-slop rules) before building.

## When to Use
E-commerce shots, hero banners, lifestyle product scenes, ad imagery.

## Workflow

1. **Product brief** - capture category, material, mood, and placement context.
2. **Verify session** - run `gflow doctor`. Pick one Flow project for the whole run and pass the same `--project <name>` plus `--no-headed` on every gflow command (reuse `--project <brand>` if a brand exists); split assets across projects only if the user explicitly asks.
3. **Infer the look** - reason lighting, backdrop, and composition from the product type rather than defaulting.
4. **Generate variations** - `gflow image --model imagen-4 --outputs 4` (use `--project <brand>` if a brand exists).
5. **Hero selection** - the user picks the winning direction before scaling up.
6. **Generate the full set** - studio, lifestyle, detail, and scale shots in the chosen direction.
7. **Upscale winners** - `gflow image ... --upscale 4k` on the selected hero frames.
8. **Export per platform** - produce platform-matched crops via `gflow batch <file.yaml>`.

## Domain Quality Checks
- Product-type reasoning: luxury = high-key soft light, tech = dramatic rim light, food = warm natural light.
- Color-temperature consistency across a batch.
- Aspect ratios matched to platform: 1:1 e-commerce, 4:5 Instagram, 16:9 hero.
- No generic flat-lay default.

## Inheriting the brand
Inherit the brand system via `--project <brand>` so palette, lighting, and styling match the brand.
