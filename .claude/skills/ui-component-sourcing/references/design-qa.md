# Design QA Checklists

Distilled from checklist.design's 110 checklists (by surface type). Run the relevant one as a
QA gate before showing UI. Fix every item; an unchecked box is a defect, not a note.

## Website (landing/marketing pages)

- Hero: headline states the value prop in ≤8 words; one clear CTA; subhead ≤2 sentences.
- Navigation: logo → home; links match page IDs; CTA visible without scrolling (on desktop);
  mobile nav has hamburger with aria-expanded; active link indicated.
- Pricing: plans named clearly; the recommended plan is visually emphasized; every plan has a CTA;
  toggle (monthly/yearly) updates prices; "save X%" badge only on yearly.
- Testimonials: real names + context (role/company); avatar or initial; no fake metrics.
- Footer: nav mirrors main nav; contact/legal links present; copyright year current.
- Forms (contact/newsletter): labels visible (not placeholder-only); error + success states;
  submit disabled while sending; no data lost on validation error.
- 404: friendly message, link home, search box if site is large.
- Content: real copy, no lorem ipsum; headings are actual headings (h1 once, sequential h2/h3).

## Web app

- Empty states for every data view: icon + explanation + primary action ("Create your first project").
- Loading: skeletons matching final layout shape; no layout jump on load.
- Errors: inline, near the field, with a fix hint; toast for global failures with retry.
- Settings: changes saved with confirmation (toast) or explicit Save; destructive actions
  (delete account) require confirm + typed input for irreversible ones.
- Onboarding: progress shown; skip available; every step's purpose stated.
- Billing: current plan + renew date visible; upgrade/downgrade paths obvious; invoice download.
- Notifications: opt-in/out per channel; badge counts cleared on view.
- Table views: sortable columns indicated; empty-filter state ("no results for 'x' — clear filters").
- Long-running tasks: progress %, cancel option, completion notification.

## Mobile

- Touch targets ≥ 44×44px; no hover-only affordances (mobile has no hover).
- Tab bar: 3–5 items max; active tab indicated; content scrolls under with safe-area padding.
- Back behavior: system back exits screens in reverse order; no dead-end screens.
- Keyboard: inputs not obscured; return key advances; dismiss on scroll.
- Paywall: value stated before price; restore-purchase path present; no dark patterns (no
  misleading close buttons).
- Orientation: layout survives rotation; no horizontal scroll on the main flow.
- Gesture hints: swipeable elements show affordance (peek of next card, dots, handle).

## Design system / components

- Every component: default, hover, active, focus-visible, disabled, loading, empty, error states.
- Colors: all roles defined as tokens; contrast 4.5:1 body / 3:1 large & UI; no raw hex in usage.
- Typography: scale set (display → caption); line-height ≥1.5 for body; text truncation has
  tooltip/title when needed.
- Spacing: consistent scale (4/8px base); no magic numbers; grids align to columns.
- Focus-visible rings on ALL interactive elements — nothing is `outline: none` without replacement.
- Both themes: no white-on-white, no invisible borders, no contrast failures (flip and check).

## Flows

- Login: error on wrong credentials is specific but not revealing; password reset reachable;
  session expiry handled gracefully.
- Checkout: cart summary visible; payment errors inline; confirmation screen with order id;
  loading state on submit (no double-submit).
- Signup: progress clarity; email verified; error recovery keeps entered data.
- Delete account: confirm twice / type-to-confirm; explains consequences; offers export first.
- Form submit: validation on blur or submit; success feedback; server errors mapped to fields.
- Password reset: link expiry communicated; new password rules stated; confirm-password match.

## Verification

Run the relevant checklist against the built page; every item passes or is consciously out of
scope for that page (state which). Report the pass list with the UI, not "looks good".
