# Production Build Playbook

How to orchestrate this skill with the rest of the agent's design skills to build a
production-grade website — great UI, purposeful animation, consistent components, proper
light/dark mode. The pipeline is **taste → craft → verify**: one driver skill per phase, spot
tools loaded only when their trigger applies. Loading everything at once is skill soup; loading
the right thing per phase is a workflow.

Skills named below are widely available (see **Appendix — Getting the skills** for where each
comes from and how to install a missing one).

## Phase 0 — Grounding (only when researching)

- `web-research-retrieval` / `software-product-research` — competitor look, tool/license evaluation.
- **Output:** constraints + references. Then stop researching; research is not building.

## Phase 1 — Plan

- `plan` — write `.hermes/plans/<name>.md` with batch Q&A and explicit open questions with
  defaults. Multi-step UI work gets a plan before code.
- Lock the design decisions here: design-language choice, component inventory, theme strategy.
- **Output:** a plan that names the direction so the build phase doesn't wander.

## Phase 2 — Design language (taste layer — get this right first; everything inherits it)

- **`claude-design` — the driver**: scope the brief, generate 2–3 directions, avoid AI-design slop.
- `popular-web-designs` — 54 real design systems as HTML/CSS; pick a visual vocabulary
  (e.g. Notion-like warm minimal for productivity apps).
- `design-md` — optional formal DESIGN.md token spec; **Refero Styles** (see
  `free-ui-libraries-audit.md`) provides real products' DESIGN.md files to adapt.
- `antislop-design` — run on the chosen direction *before* building, not after.
- **Output:** a locked token set — color roles, type scale, spacing, radius, borders — as CSS
  variables, both themes.

## Phase 3 — Build (craft layer)

- **`ui-component-sourcing` (this skill) — the driver**: the 10-step design-angles workflow in
  SKILL.md, the sourcing matrix (Tier A/B only), `workflows.md` for transform tasks.
- `shadcn-app-frontend` — shadcn/ui + Next.js conventions when that's the stack.
- `themeable-ui-skins` — only when the product needs multiple skins, not just light/dark.
- **Output:** pages built on the base layer + tokens; flair only from legal sources.

## Phase 4 — Polish (the "feels expensive" layer)

- `ui-component-sourcing` → `motion.md` — every micro-interaction gets a number
  (100–200ms micro, 200–400ms transitions, 40–80ms staggers); 60fps.design as the
  "what good looks like" gallery.
- `humanizer` — copy and microcopy, strip AI-isms.
- **Output:** purposeful motion + real-sounding copy.

## Phase 5 — QA (verify layer — production-grade is won here)

- **`ui-component-sourcing` → `design-qa.md`** — the checklist pass (website / web app / mobile /
  design system / flows).
- `ui-layout-review` — measured grid balance: equal-height cards per row, no dead space.
- `ui-state-review` — unreachable controls, dead handlers, missing states.
- `design-critique` / `impeccable` — one holistic critique against the tokens.
- `adversarial-ux-test` — a hostile-user pass on the critical flows.
- Browser QA: `auth-gated-webapp-qa`, `browser-toolset-verification`.
- Code: `code-review-and-quality` / `requesting-code-review`.
- **Output:** a fix list → iterate → re-run the measured gates until they pass.

## Phase 6 — Ship

- `release-readiness-checker` — pre-release checklist.
- Conventional commits; keep the audit dates honest.

## Craft rules (the short version)

| Concern | Rule |
|---|---|
| Animation | Purpose rule: direct attention or give feedback, never decoration. Numbers from `motion.md`. Reduced-motion is a gate. |
| Spacing | 4/8px token scale, no magic numbers; grids measured via `getBoundingClientRect`, not eyeballed. |
| Borders | `border-border` token (low alpha), radius from the scale, hover = border-color shift, focus = ring (never `outline: none`). |
| Light/dark | Token swap only — no hex in components. Verify computed styles in BOTH themes (white-on-white is a classic failure). `workflows.md` dark-mode-image for rasters. |
| Consistency | One base layer (shadcn), one icon set (Lucide), one token set. Sourced flair adapts to tokens, never the reverse. `workflows.md` refactor-to-components prevents drift. |

## Appendix — Getting the skills

### Hermes Agent

Most skills referenced above are **bundled** with Hermes Agent (builtin/official) — nothing to do.
For anything missing:

```bash
hermes skills search "<name>"        # browse skills.sh / official / GitHub / ClawHub / ...
hermes skills install <identifier>   # e.g. owner/repo/skill-path, or a direct SKILL.md URL
hermes skills check && hermes skills update   # keep hub-installed skills current
```

Manual GitHub install (used when a skill isn't on the hub): copy the skill's whole directory
(`SKILL.md` + its `references/`/`scripts/` tree — never just SKILL.md) into
`<skills-root>/<category>/<skill-name>/`, then start a **new session** (the skill loader caches
at session start). See the `install-github-skill` skill for the full procedure.

### Other harnesses (Claude Code, Cursor, Codex, OpenCode)

- `npx skills add <gh-owner>/<repo>` (skills.sh ecosystem) — installs into ~/.claude, ~/.codex, .cursor.
- `npx impeccable install` — Impeccable's own installer for those harnesses.
- Manual: copy the `SKILL.md` + `references/` tree into your harness's skills directory.

### This skill

Clone this repo and copy `SKILL.md` + `references/` into your agent's skills directory, or
`hermes skills install` from the repo identifier once published. A new session is required for
the skill to be visible.

## Verification

- Every phase's completion criterion is met (each phase above ends with a checkable output).
- The QA gates pass in both themes and at 375/768/1280px.
- No Tier C (paid) code in the output; audit dates kept honest.
