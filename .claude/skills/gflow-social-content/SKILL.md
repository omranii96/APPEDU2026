---
name: gflow-social-content
description: Generate platform-optimized social posts, reels, and thumbnails in batch with a consistent aesthetic. Use when the user wants Instagram posts or reels, TikTok covers, YouTube thumbnails, LinkedIn banners, or a content campaign.
type: flexible
version: 1.1.1
foundation: false
consumes: [gflow-brand-identity, gflow-character-pipeline]
tools: [gflow-cli]
---

# Social Content

Produces platform-optimized social posts, reels, and thumbnails generated in batch with a consistent aesthetic.

Read `references/quality-gate.md` (mandatory, motion and anti-slop rules) before building.

## When to Use
Instagram posts and reels, TikTok covers, YouTube thumbnails, LinkedIn banners, content campaigns.

## Workflow

1. **Content brief** - capture platform, content pillar, campaign theme, and brand voice.
2. **Verify session** - run `gflow doctor`. Pick one Flow project for the whole run and pass the same `--project <name>` plus `--no-headed` on every gflow command (reuse `--project <brand>` if a brand exists); split assets across projects only if the user explicitly asks.
3. **Define the content batch** - plan the asset set (e.g. 5 posts, 3 stories, 2 reels covers).
4. **Generate the batch** - `gflow batch <file.yaml>` with platform-specific ratios per asset.
5. **Short-form video** - `gflow video --duration 5` for reels and TikTok covers.
6. **Longer reels (optional)** - when a reel needs more than one generation, extend it with `gflow extend --media-id <clip>` plus repeated `--prompt "<what happens next>"` (about 7-8s per extend) or `--add-clip` to stitch clips into one video; keep the result inside the platform's length limit.
7. **Brand consistency** - apply `--project <brand>` across the batch and use `gflow agent` to lock voice and treatment.
8. **Deliver** - organize output by platform folder plus a posting guide.

## Domain Quality Checks
- Platform-native ratios: 4:5 feed, 9:16 stories and reels, 16:9 YouTube.
- No premium-consumer beige/brass default palette unless the brand calls for it.
- Text-overlay safe zones respected so platform UI does not overlap key content.
- Batch visual consistency: same palette and treatment across every asset.
- Thumbnail legibility at 120px browse size.

## Inheriting characters and brand
Inherit recurring personas via `--character <name>` (from gflow-character-pipeline) and the brand system via `--project <brand>` (from gflow-brand-identity) so palette, voice, and treatment carry across every post.
