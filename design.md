# Design — YIYOL (yiyol.com)

A locked design system for this site. Every page redesign reads this file before
emitting code. Do not regenerate per page — extend or amend this file when the
system needs to grow.

Established 2026-08-18 by `hallmark redesign`, starting from `index.html` and
extended across the site. Where this file and the Hallmark references disagree,
**this file wins**.

## Genre

**modern-minimal.** B2B industrial-AI platform. Precise, engineered, calm —
"instrument panel, not marketing template." Never warm, never playful, never editorial.

## Macrostructure families

Pages within a family share the family's shape; they vary only in component
archetypes.

- **Marketing / home** — Split Studio. Alternating diptychs; every claim paired
  with a proof column. Varies: hero archetype, enrichment tier.
- **Section pages** (`solutions/`, `products/`, `company/`, `contact/`) — Split
  Studio entered through a tab rail. Page head → hairline tab rail → tab panels of
  alternating diptychs → closing CTA. Varies: which components fill the panels.
- **Content pages** (`blog/`) — Long Document. Prose-led, single measure column,
  inline section heads. No marketing structure.

## Theme — Cobalt, anchored on the YIYOL brand cyan

Axes: **paper band** light · **display style** grotesk-sans · **accent hue** cool 226.

The brand cyan `#00b4d8` measures **2.46:1 on white** — below WCAG AA for both text
and UI. It is preserved at full strength as `--color-accent-bright`, used **only on
the graphite band and the footer**, where it measures 8.64:1. On light ground the
accent deepens within the same hue family to `--color-accent`.

| token | value | contrast |
| --- | --- | --- |
| `--color-paper` | `oklch(99% 0.004 240)` | — |
| `--color-paper-2` | `oklch(97.4% 0.006 240)` | — |
| `--color-ink` | `oklch(23% 0.024 250)` | 16.36:1 on paper |
| `--color-ink-2` | `oklch(41% 0.020 248)` | 8.51:1 on paper |
| `--color-muted` | `oklch(53% 0.018 248)` | 5.11:1 on paper · 4.59:1 on paper-3 |
| `--color-rule` | `oklch(92% 0.008 248)` | — |
| `--color-accent` | `oklch(50% 0.135 226)` | 5.36:1 on paper · white-on-it 5.52:1 |
| `--color-graphite` | `oklch(20.5% 0.022 252)` | the one dark band |
| `--color-accent-bright` | `oklch(76% 0.130 218)` | 8.64:1 on graphite |
| `--color-focus` | `oklch(50% 0.135 226)` | — |
| `--color-bright-hair` | `oklch(76% 0.130 218 / 0.30)` | accent hairline on graphite |
| `--shadow-dark` | `0 8px 24px oklch(0% 0 0 / 0.40)` | elevation on the graphite ground |

Full set in [`assets/css/tokens.css`](assets/css/tokens.css). **No rule anywhere may
inline a colour** — every value references a named token.

## Typography

- **Display** — Space Grotesk 600, roman. Tracking `-0.025em`. Never italic.
- **Body** — Inter 400/500.
- **Mono** — JetBrains Mono 400/500, uppercase, tracking `0.06em`. Labels, specs,
  status, numerals. This is the theme's machine-readout voice.
- **Korean** — Noto Sans KR inside every stack. `word-break: keep-all` on headings
  and body so Korean wraps on word boundaries, not syllables. This is not optional;
  without it Korean headlines break mid-word.
- Three families total. A fourth is slop.

## Spacing and measure

4-point named scale (`--space-4xs` … `--space-3xl`) in `tokens.css`. Pages must use
named tokens (`var(--space-md)`), never raw values.

**Body text fills its container** — `--measure: 100%`. The classic 45-75 character
measure was capping prose at ~56 % of the shell while tables and grids ran the
full width, and that mismatch read as broken rather than as margin. Width wins
here by decision, not by oversight.

Still capped, because they are composition rather than running text:
display headings (`15ch` / `18ch`), the footer tagline (`34ch`), form fields
(`44rem`), and the article reading column (`52rem`).

## Motion

- Easings: `--ease-out` / `--ease-in` / `--ease-in-out`. Never the browser default `ease`.
- **Three primitives site-wide, no more:** reveal fade+rise (`.sv-fade`, 600 ms),
  accent underline grow on links, arrow nudge on typographic CTAs.
- Reduced-motion: opacity-only, ≤150 ms. Focus rings never animate.

## Microinteractions stance

- Silent success over celebratory toasts.
- Optimistic update + Undo over confirmation dialogs.
- Hover delay 800 ms; focus delay 0 ms.
- Every interactive element ships all eight states. Form fields additionally ship
  error and success with a text message, never colour alone.

## Nav and footer — shared, identical on every page

- **Nav: N1b** — wordmark left · centred 4-link cluster · language + one filled CTA
  right · transparent at rest, frosts on scroll (`.is-stuck`). Current section
  carries `.nav-active`.
- **Footer: Ft1 Mast-headed** — wordmark + tagline anchoring a band, inline link row
  beside, hairline rule, then address / registration / licence in mono, then copyright.
- **Banned:** N1a (wordmark + right link pile + button), Ft3 (4 link columns +
  social row + tiny copyright). Both are the AI fingerprints this system replaced.

## Staged progressions carry intensity, never a second hue

When a page shows an ordered sequence — a roadmap, a maturity ladder, a
data-vs-system split — the stages are told apart by **treatment on the one
accent**: filled (now) → outlined (next) → dashed (future) → neutral (past).
Introducing a hue per stage is how `nox/intro*` ended up shipping violet and
pink, and the two calculators a blue and a green. One accent per page holds even
when the content is genuinely staged.

## CTA voice

- **Primary** — filled `--color-accent`, `--radius-ctl` (6px), verb + object
  ("문제 상담하기"), never "자세히 보기" alone, never "click here".
- **Secondary** — typographic link: word + `→` + 1px underline. Not a second button.
- **One button per closing CTA section.** The repetition is the call to action.

## Section rhythm

- Section heads are **left-aligned, single column**, heading directly under any label.
  Centred section heads are banned — they were the site's primary AI tell.
- **Eyebrows default OFF.** At most one decorative eyebrow per page. Mono column
  keys, list labels, and ordinal numerals are functional and don't count.
- Tag-left / heading-right (hanging header) is banned outright.
- Structure comes from hairlines and one graphite band per page, never from cards
  with icons on top.
- **Inside a panel, blocks have their own rhythm.** A prose subhead (`.sv-prose h3`)
  sits at `--text-lg` with `--space-xl` above it and its paragraph tight beneath;
  two blocks in one panel are parted by `.sv-stack`. A run of h3 + p pairs with no
  rhythm collapses into one undifferentiated slab — that was `company/`'s defect.

## Per-page allowances

- Marketing pages MAY use enrichment — Tier-A pure CSS or Tier-B hand-built SVG only.
- Section pages MUST NOT use hero enrichment; the tab rail and the content carry them.
- Content pages: typography only.
- **No icon libraries.** Font Awesome is removed site-wide. Decorative icons are
  dropped; meaningful glyphs are inline SVG or text (`→`).
- **No re-drawn chrome** — no fake browser bars, phone frames, or terminal windows.
- **No invented metrics.** Every number on the site is a real product spec.

## What pages MUST share

The wordmark · the accent and its ≤5 %-per-viewport budget · the three font
families · the CTA voice · the nav and footer archetypes · the left-aligned
section-head rhythm · `tokens.css`.

## What pages MAY differ on

Macrostructure within the family · which component archetypes fill a section ·
enrichment (marketing pages only) · the presence of a graphite band.

## Variants

### `product-dark` — the NOX product microsite

Pages: `nox-nvr.html`, `nox-nvr-embed.html`, `nox/intro.html`, `nox/intro-en.html`,
`nox/nis-security.html`, `nox/partner.html`, `nox/specifications/index.html`.

These are **bespoke product pages**, not template pages. They carry hand-built
work the corporate layer has no equivalent for — an SVG rack chassis with
hot-swap bays and LED states, a taegeuk mark, a 60 KB specification matrix. A
wholesale conversion to the light system would delete that work, so the variant
is registered here rather than overridden per page.

**What the variant changes from the base system**

- **Canvas is dark.** `--color-graphite` family instead of paper; ink roles invert
  to `--color-on-dark` / `--color-on-dark-2`.
- **Accent is `--color-accent-bright`** (the brand cyan at full strength, 8.64:1 on
  graphite) — *not* the deepened light-ground accent.
- Product pages MAY keep a bespoke hero composition and hand-built SVG/CSS art.

**What the variant does NOT change — these still bind**

- The three font families, and `word-break: keep-all` for Korean.
- Nav N1b and footer Ft1, in their dark skin. **Every product page carries them**;
  a product page with no way back to the site is a navigation defect, not a style.
- One accent per page. Mint, indigo, and violet accents are not permitted — they
  read as three different companies.
- Every universal slop gate: no gradient text, no emoji icons, no icon library,
  no `transition: all`, no re-drawn chrome, no invented metrics.
- Contrast thresholds, measured against the *dark* ground.

`nox-nvr-embed.html` is the one exception to the nav/footer rule: it is
`Disallow`ed in `robots.txt` and exists to be iframed, so it ships the styling
without the site chrome.

**Preserved illustration.** The 2U chassis on `nox-nvr*` — the inline SVG and the
`buildBays` script that draws its eight drive trays — keeps literal colour
values. Those are faceplate, handle and LED **materials of a rendered object**,
not theme surfaces, and tokenising them would flatten the drawing. The region is
marked `PRESERVED ILLUSTRATION` in the source and is the only place on the site
where a raw colour is allowed outside `tokens.css`. Everything that *frames* the
drawing — grounds, type, buttons, badges — is tokenised. The `.entart` diagrams
are **not** covered by this: they draw with `currentColor` and follow the page
accent. The taegeuk mark is a national-flag device, so its red/blue pair is fixed
by meaning and is declared as `--taegeuk-red` / `--taegeuk-blue` in the page root.

**`nox/index.html` — redirect interstitial.** Registered here as an exception
rather than a variant page. It `meta refresh`es at 0s, so it is essentially never
painted; it therefore loads **`tokens.css` only** — no webfonts, no `site.css`,
no `dark.css`, and no nav/footer. Pulling four font families and three
stylesheets for a ~100ms view was pure waste.

Implemented by `assets/css/dark.css`, loaded after `site.css` on these pages.

## Diversification is INVERTED here

This is a system-managed site. Consecutive pages **must** share theme, accent, and
type pairing. Variety lives in macrostructure and archetype choice, not theme.
A page that drifts from this file is the defect.

## Stylesheet architecture

| file | scope | loaded by |
| --- | --- | --- |
| `assets/css/tokens.css` | tokens only | every page |
| `assets/css/site.css` | base type, nav, footer, buttons, links, motion | every page |
| `assets/css/page.css` | section-page component skin (`.sv-*` vocabulary) | section pages |
| `assets/css/home.css` | home-only components | `index.html` |
| `assets/css/blog.css` | Long Document prose + post index + legal documents | `blog/`, `privacy.*.html` |
| `assets/css/dark.css` | `product-dark` variant — chrome skin + residual contrast remediation | `nox-nvr*.html`, `nox/*` |
Shared scripts: `assets/js/i18n.js` (language + mobile menu) and
`assets/js/yiyol-tabs.js` (sub-nav tabs + scroll reveal). Both were previously
named after an unrelated site; see § Naming.

`blog.css` ends with a **legacy variable bridge** that aliases the retired
`style.css` names (`--text-primary`, `--bg-dark`, `--accent-color`, …) onto the
locked tokens. The two calculator pages keep their own `calc-*` widget CSS —
that is working functionality, not a visual layer — and the bridge is what lets
those rules resolve against the new system without being rewritten. **The
carve-out covers layout and behaviour only, not colour:** their palettes are
tokenised like every other page, and the blue/green data-vs-system coding they
shipped is now the fill-vs-outline treatment described above.

Load order is always tokens → site → (page \| home \| blog).

## Naming

Nothing in this codebase carries another company's name. The stylesheet and
script that shipped as `surv.css` / `surv-tabs.js` — and whose header read
*"surv.co.kr-style light theme"* — is deleted; the script is now `yiyol-tabs.js`.
Both retired stylesheets are deleted and stay recoverable in git history at
`HEAD:assets/css/surv.css` and `HEAD:assets/css/style.css`.

Two things deliberately still contain the letters `surv`:

- **`surveillance` / `survives`** — ordinary English, and `surveillance` is core
  product vocabulary. 30 occurrences, all correct.
- **An external URL** in a blog post (`cybernews.com/…/cameras-surveilling-world/`).
  Rewriting it would break the citation.

The `sv-` class prefix on the section pages is the same abbreviation and has not
been renamed — see the note in `page.css`.

## Exports

See [`assets/css/tokens.css`](assets/css/tokens.css) for the canonical `:root` block.
Regenerate Tailwind `@theme`, DTCG `tokens.json`, and shadcn/ui variables from it
when a consuming project needs them.
