# Visual styles

Visual profiles are event-neutral. A deck selects exactly one `color-*` profile, which controls visual grammar only. Timing, upload, artifact, and event rules are verified separately and are never render profiles.

## Token contract

Every color profile defines:

```css
--sinew-bg
--sinew-panel
--sinew-panel-raised
--sinew-ink
--sinew-muted
--sinew-line
--sinew-line-strong
--sinew-accent
--sinew-accent-contrast
--sinew-danger
--sinew-success
--sinew-data-1 ... --sinew-data-5
```

It also sets explicit sans-serif and monospace stacks for Reveal headings/body/code. Use local/system fonts or bundle licensed webfonts. Do not import delivery-critical fonts from a remote CDN.

Core layout and components live in `_extensions/sinew/theme/core.scss`. Styles should not target sample-slide IDs or change the meaning/order of content.

The research-framing identity is part of that stable component layer. `.research-questions` uses `--sinew-accent`; `.research-hypotheses` uses `--sinew-success`; the Q/H identifier, item border, title rule, and optional `.is-highlighted` treatment inherit automatically in every profile. A profile must keep both semantic colors readable on its panel surfaces and must not replace the Q/H labels with color-only meaning.

The evidence inspector is also profile-neutral core UI. Its controls, fullscreen surface, rules, text, and focus state inherit the active profile tokens. Style-specific rules may refine geometry or depth, but must preserve the visible `Expand` control, keyboard focus, viewport fit, and dialog contrast.

Every adapted style record must state the inspected source route or URL, inspection date, owner/license when known, extracted visual roles, deliberate projection/accessibility changes, font fallback policy, and any mismatch between deck CSS and the Matplotlib overlay. A source reference is provenance, not permission to redistribute protected assets.

## Origami

Profile: `color-origami`

Source inspected on 2026-08-25: the Origami repository's `apps/tactile_segmentation_viewer/static/app.css` file. No application assets or selectors are redistributed; the profile maps observed semantic roles into Sinew's independent token and component system.

The relevant viewer tokens were:

| Role | Viewer token/value | Sinew adaptation |
|:--|:--|:--|
| Background | `--bg: #131416` | preserved |
| Panel | `--panel: #1b1d21` | preserved |
| Raised panel | `--panel-raised: #202329` | preserved |
| Line | `--line: #2b2e34` | preserved; strong line raised for projection |
| Ink | `--ink: #e6e6e6` | preserved |
| Muted | `--muted: #8d9198` | raised to `#a9adb4` for small projected captions |
| Focus | `--accent: #e8b64c` | preserved as amber accent |
| Model signal | `--model: #4cc2e8` | first data color |
| Status | danger/success/violet | retained as semantic/data options |
| Radius | `8px` | converted to a scale-relative radius |
| Fonts | system sans + system mono | preserved, enlarged for projection |

Also preserved conceptually: subtle grid, fine borders, compact evidence panels, amber focus, cyan model signal, and tabular monospace labels.

Deliberate changes:

- UI controls, sticky navigation, application panels, badges, and dense 13 px layout were not copied.
- Body type is 34 px on a 1600x900 reference canvas.
- Muted/caption color is brighter.
- Animations are reduced and respect `prefers-reduced-motion`.
- Data series require markers/dashes/direct labels in addition to color.
- The app's colors become semantic tokens; they are not assumed to be a complete categorical palette for arbitrary `n`.

This is an adaptation, not an official Origami product theme or conference requirement.

## Paper

Profile: `color-paper`

A warm light academic surface for well-lit rooms and print/PDF. It uses Source Sans/Helvetica/Arial fallbacks, deep ink, a blue link/accent, and adjusted Okabe-Ito-inspired data colors. It avoids pure white glare while retaining text contrast.

## High contrast

Profile: `color-high-contrast`

A white/black audit and fallback profile with minimal motion, thicker component borders, underlined links from the core theme, and a conservative sans stack. The profile is useful for accessibility inspection and unknown projectors. It does not guarantee accessibility of embedded figures or user-authored content.

## Blueprint

Profile: `color-blueprint`

A deep navy technical-drawing surface with cyan focus, a compact display-sans heading stack, visible construction grid, and bright data colors. It is a Sinew house style, not event branding.

## Scholar

Profile: `color-scholar`

A pale editorial surface with serif headings, sans-serif body text, purple focus, and restrained shadows. It demonstrates a visibly different academic voice while preserving the same semantic components. It is a Sinew house style, not event branding.

## Unmasked

Profile: `color-unmasked`

Reference inspected on 2026-08-25: design-source route `/systems/unmasked/system.html`. The repository was not given a canonical public URL, owner, or license for that reference. Resolve those fields before publishing the adaptation as an endorsed or redistributable theme.

Extracted ideas: true monochrome, visible construction rules, square geometry, heavy sans-serif display type, and serif reading text. Sinew adapts these ideas with a near-white `#f7f9fb` ground, black focus, layered grays, explicit danger/success colors, and square evidence components. Remote font dependencies were replaced with Public Sans/Arial and Source Serif/Georgia fallbacks. Muted text and rules were strengthened for projection. The Matplotlib overlay uses DejaVu Sans for dependable labels, so it matches the monochrome palette and rule weight rather than the deck's mixed serif/sans typography.

## The give

Profile: `color-the-give`

Reference inspected on 2026-08-25: design-source route `/systems/give/system.html`; the public style name is "the give." The repository was not given a canonical public URL, owner, or license for that reference.

Extracted ideas: periwinkle and mint surfaces, soft corners, gentle depth, Signika-like headings, and Faustina-like body text. Sinew reduces decorative depth, uses a darker periwinkle focus color with white contrast text, keeps table banding restrained, and supplies offline Trebuchet/Arial and Georgia fallbacks. The data cycle adds separable purple, green, rust, and blue roles and still requires markers/dashes. The Matplotlib overlay uses DejaVu Serif as an available approximation rather than claiming the design-source fonts are embedded.

## The meeting

Profile: `color-the-meeting`

Reference inspected on 2026-08-25: design-source route `/systems/meeting/system.html`; the public style name is "the meeting." The repository was not given a canonical public URL, owner, or license for that reference.

Extracted ideas: coral and teal voices meeting through violet, a cool porcelain ground, editorial serif headings, and restrained depth. Sinew darkens the signals used for small text/data, confines the brighter source colors to non-text decoration, uses violet as the focus seam, and replaces remote typography with Cormorant/Lora/Hanken-compatible system fallbacks. The Matplotlib overlay uses a DejaVu Serif fallback while preserving the coral/teal/violet data ordering.

## Movement

Profile: `color-movement`

Reference inspected on 2026-08-25: design-source route `/systems/motion/system.html`. The source slug is `motion`; the Sinew-facing style name and profile slug are deliberately `movement`. The repository was not given a canonical public URL, owner, or license for that reference.

Extracted ideas: charged white, scarlet motion, a green wake, condensed display type, and directional diagonal energy. Sinew uses darker scarlet and green for contrast, keeps the diagonal treatment on title/divider surfaces, makes progress animation conditional on `prefers-reduced-motion`, and provides Big Shoulders/Arial Narrow/Arial plus Lora/Georgia fallbacks. The Matplotlib overlay uses a dependable sans stack, thicker series lines, and the same scarlet/green-led cycle; marker and dash differences remain mandatory.

## Runtime gallery switching

The default repository gallery previews all nine styles in separate horizontal columns. `styles/gallery/columns.html` listens to Reveal's `ready` and `slidechanged` events; `styles/gallery/columns.css` mirrors the represented style tokens. A real render does not switch styles mid-talk: select exactly one visual profile with `--profile color-<name>`.

## Add a style from an uploaded reference

Follow the complete checkbox workflow in [New visual style TODO](adding-a-style.md). The summary below describes the design work; the TODO also covers gallery registration, per-style citations, versioning, CI demos, branches, and pull requests.

1. Establish provenance: original URL/path, owner/license, capture date, and which screens/components were reviewed.
2. Extract semantic roles rather than copying selectors: background, surface, ink, muted, rules, focus/accent, statuses, data cycle, type, radius, shadows, density.
3. Map to all Sinew tokens in `styles/colors/<name>.css`.
4. Remove application-specific navigation/control styles.
5. Increase typography/contrast for projection and provide offline font fallbacks.
6. Add `_quarto-color-<name>.yml` and add it to the single profile group in `_quarto.yml`.
7. Add `styles/matplotlib/sinew-<name>.mplstyle`; compose it after `sinew-slides.mplstyle` and document any typography/palette mismatch.
8. Add the style slug to `scripts/generate_gallery_plots.py` and `scripts/render-styles.sh`.
9. Run `python3 scripts/generate_gallery_plots.py` and `scripts/render-styles.sh`.
10. Inspect both common viewport sizes, grayscale, and network-disabled rendering; document accessibility and academic-figure/table adaptations.

Copy `styles/colors/paper.css` as the contract reference. A later style may define a different heading/body family, but the semantic class surface remains stable.

## Event branding

Do not add event colors or logos merely because a deck will be presented there. A separate opt-in `color-*` style is acceptable only when official assets and usage rules are cited, use is permitted, trademark constraints are followed, and the author deliberately requests it. Event logistics remain outside the visual-style system.
