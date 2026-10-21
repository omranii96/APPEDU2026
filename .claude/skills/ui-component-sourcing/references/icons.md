# Icon Strategy

Condensed from the free-icon-resources audit (157 sources, CC0 list — full list:
github.com/noahelhadedy/free-icon-resources). Goal: pick icons that are free, MIT-ish, and
consistent — never hotlinked, never attribution-surprise.

## Default set (MIT, no attribution, bundle as SVG)

| Set | Count | Style |
|---|---|---|
| Lucide | 1,400+ | Stroke, consistent weight — default in shadcn/ui, use it unless there's a reason not to |
| Heroicons | — | Tailwind's outline + solid |
| Tabler | 5,800+ | Stroke-based |
| Phosphor | 9,000+ | 6 weights |
| Radix Icons | — | 15×15 crisp, matches shadcn/Radix |

## Specialized free (no attribution)

- Brand/logos: Simple Icons (SVG brand marks — check brand usage guidelines).
- Animated: use motion + Lucide strokes instead of animated icon libs (license surface shrinks).
- Emoji: Twemoji / OpenMoji (open licenses) if needed.
- Flags: Flagpack / flag-icons (MIT-ish).

## Attribution REQUIRED (avoid unless client provides)

Flaticon, Freepik, Vecteezy, The Noun Project (free tier = attribution), Icons8 (free = link
back), Font Awesome (free tier = attribution). Using these unattributed in a client project is
a license violation — default to the MIT sets above.

## Rules

1. **Bundle, never hotlink** — inline SVG components or local files; hotlinking breaks and leaks.
2. **One set per app** — mixing Lucide + Tabler + Phosphor looks inconsistent; pick one and stay.
3. **Size & stroke consistency** — same pixel grid (Lucide = 24px, stroke 2) everywhere; scale by
   size token, not ad-hoc.
4. **Decorative icons: `aria-hidden="true"`**; meaningful icons get `aria-label`/`title`.
5. **Icon buttons need accessible names** — visible label, `aria-label`, or `title` + `aria-labelledby`.
6. **Brand icons** (GitHub, X, Google): use official SVG paths from Simple Icons — never
   screenshot or scrape.

## Verification

- `search_files` the built code for `https://` image/icon URLs — none should exist for icons.
- Every icon button has an accessible name (grep `aria-label` next to icon-only buttons).
- All icons come from one set (one import source).
