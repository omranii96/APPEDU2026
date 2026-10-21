# Component Taxonomy & States

Canonical inventory of what a complete UI contains — derived from component.gallery's design-system
taxonomy (which real design systems actually ship) and checklist.design's structure. Use as the
inventory checklist in step 1 of the build workflow: when a page needs X, these are the candidates.

## Core controls

Button (primary/secondary/ghost/destructive/link), Input field, Checkbox, Radio, Toggle/Switch,
Select, Slider, Date picker, Searchbar, Textarea, Combobox/autocomplete, Stepper/counter.

## Navigation

Tabs, Breadcrumb, Dropdown menu, Accordion, Drawer, Sidebar, Pagination, Command palette,
Context menu, Stepper (multi-step), Tab bar (mobile).

## Feedback & status

Toast, Banner, Modal/Dialog, Tooltip, Popover, Skeleton, Spinner, Empty state, Error state,
Inline validation, Notifications (in-app), Progress indicator, Status badge, Alert/Inline callout.

## Data display

Table, Card, Badge, Avatar, Icon, Stat/number, Timeline, Feed, Kanban, Chart/graph, Code block,
Single-item detail view, Search results.

## Layout & structure

Grid, Container, Section, Spacing system, Divider, Page header, Footer, Sticky header, Hero,
Logo cloud, Testimonial, Pricing table, Feature list, Team grid, FAQ (accordion), CTA band,
Gallery/carousel, Masonry.

## Flows (cross-page sequences)

Onboarding, Login/Signup, Checkout, Settings, Password reset, Account deletion, Subscription
cancel, Media upload, Form submit, 2FA verification, Empty-first-run.

## AI-native / agent-interface components (from Beautiful UI's catalog)

For agent products (chat, coding agents, automation UIs) — generic libraries don't cover these;
they are the difference between "app with a chat box" and a real agent interface:

| Component | Requirements |
|---|---|
| Streaming text | Token/code output streaming in line by line; monospace for code; stable line count (no layout jump); stop button |
| Thinking state | Reasoning indicator (shimmer / pixel-grid loader + elapsed time in tabular figures); reduced-motion freezes the visual, timer still ticks |
| Tool-call chips | Tool calls & code edits as compact, collapsible chips — what ran, what changed, expand for detail |
| Approval card | Human-in-the-loop approval: what's being approved, cost/impact, allow / deny / always-allow |
| Agent task rows | Live status list: queued → running (progress) → failed / completed; retry on failure |
| Confidence suggestion | Agent suggestion + confidence meter + accept / decline actions |
| HITL question | Agent asks a clarifying question before acting — inline, blocking, with quick-answer options |
| Chat panel | Message list + composer; reasoning replies tabbed vs final answer; streaming cursor |
| Live status chips | Status chips that reorganize live data — indicate change (flash / transition), keep context |
| Paged insights | Scrub-ready live charts; pagination for long agent results |

Extra states for these: **streaming** (partial output), **interrupted/stopped** (partial + resume),
**tool-error** (failed call with retry), **approval-pending** (blocking, human away).

## Required state set (apply to every interactive component)

| State | Requirement |
|---|---|
| default | Resting appearance, meets contrast (4.5:1 text, 3:1 UI) |
| hover | Visible affordance change (bg, border, shadow, scale ≤1.02) |
| active/pressed | Distinct from hover (darker bg / translate-y) |
| focus-visible | Keyboard ring — NEVER `outline: none` without replacement |
| disabled | 40–50% opacity or muted, still legible, not focusable |
| loading | Skeleton preferred over spinner (reduces layout shift); button keeps width |
| empty | Icon + title + explanation + action (never a bare "No data") |
| error | Inline, near the field, with fix hint; input gets error border |
| success | Confirmation (toast, check, inline note) |

## Verification criterion

Every component used in the output has at least: default + hover + focus-visible + disabled +
loading (if async) + empty (if data-driven) + error (if user input). Grep the final code for
`disabled=`, `aria-`, and loading/empty branches; if a data-driven component lacks empty/error
branches, it is incomplete.
