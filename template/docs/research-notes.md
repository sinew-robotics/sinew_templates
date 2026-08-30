# Research record

Last researched: **2026-08-25** (Asia/Seoul); the CSL and Reveal-source entries below were added and inspected on 2026-08-30. The event-delivery pages under "Event delivery evidence" were not re-checked on 2026-08-30 and keep their original 2026-08-25 verification.

This file is the evidence record behind the template. Labels have precise meanings:

- **Required**: explicitly stated by the cited conference edition or standard.
- **Recommended by source**: advice from the cited authority, not a hard submission rule.
- **Sinew default**: a house decision for legibility, reproducibility, or workflow.
- **Unknown / pending**: do not infer a rule from an earlier edition.

## Quarto and Reveal.js

Primary documentation reviewed:

- [Starter templates](https://quarto.org/docs/extensions/starter-templates.html): repositories are copied except hidden/common GitHub/AI configuration files; `template.qmd` is specially renamed.
- [Custom formats](https://quarto.org/docs/extensions/formats.html): formats live under `_extensions/<name>/_extension.yml`; a repository can support both `quarto add` and `quarto use template`.
- [Includes](https://quarto.org/docs/authoring/includes.html): include shortcodes textually insert `.qmd`; included paths resolve from the main document; underscore prefixes prevent standalone rendering.
- [Reveal vertical slides](https://quarto.org/docs/presentations/revealjs/advanced.html#vertical-slides): level-1/level-2 headings create 2D stacks with `vertical` or `grid` navigation. Quarto warns vertical content is often missed.
- [Project profiles](https://quarto.org/docs/projects/profiles.html): profile groups enforce mutually exclusive selections; profile-specific `metadata-files` are unsupported.
- [Reveal themes](https://quarto.org/docs/presentations/revealjs/themes.html): custom SCSS themes and additional CSS are supported.
- [Figures](https://quarto.org/docs/authoring/figures-and-layout.html): `fig-alt`, captions, sizing, and figure layout.
- [Cross-references](https://quarto.org/docs/authoring/cross-references.html): stable `#fig-...` and `#tbl-...` targets render automatic labels and hyperlinks; Quarto also reserves `#alg-...` for theorem-style algorithm blocks.
- [Shortcode extensions](https://quarto.org/docs/extensions/shortcodes.html): an extension contributes Lua shortcodes from `_extension.yml`, and each shortcode returns Pandoc AST nodes.
- `document-slides.yml` schema (`/opt/quarto/share/schema/document-slides.yml` in a local Quarto 1.9.38 install): documents `slide-number: c` as "Flattened slide number" and `h.v` as "Horizontal . vertical slide number", confirming the meaning of both settings independent of observed behavior.
- Reveal's own source, `reveal/dist/reveal.esm.js` (vendored per-render under `deck_files/libs/revealjs/dist/`; inspected 2026-08-30 at `/opt/quarto/share/formats/revealjs/reveal/dist/reveal.esm.js` in the same local Quarto 1.9.38 install): traced directly, not inferred from behavior alone, to confirm what `navigation-mode` and `slide-number: c` actually do -- the `next()`/`right()`/`left()` depth-first and row-preservation logic, the keyboard handler's `linear`-vs-`default` branch for Up/Down, and the PDF exporter's separate flat auto-increment counter that ignores the configured `slideNumber` format. Findings, measured slide sequences, and the exact quoted lines are recorded in `docs/architecture.md`, "Slide numbering" -- that section is the primary write-up; this entry records that the underlying vendor source was actually opened and read, not assumed from Quarto's own documentation.

Architecture decisions derived from those sources:

- Use a stable `deck.qmd`, not `template.qmd`.
- Use built-in includes rather than a filesystem-discovery filter.
- Keep exactly one visual `color-*` profile active for a normal deck.
- Keep event logistics out of render metadata and verify them separately for the exact delivery context.
- Ship root agent rules and separately named copyable templates because Quarto excludes `AGENTS.md` and `CLAUDE.md` from starter copies.
- Keep caption-below-code algorithms on Sinew's `#algorithm-...` targets and `alg` shortcode rather than Quarto's theorem-style `#alg-...` block; use shortcodes for Q/H statement references because CSS-generated list labels do not exist in the source AST.

## Event delivery evidence

The following is dated background research for authors preparing delivery. These notes are not Quarto profiles, do not select a style, and do not alter a render. Re-open the current official page for the exact edition, track, and artifact before relying on any item.

### ICRA 2026

Source: [Paper Presentation Instructions](https://2026.ieee-icra.org/contribute/paper-presentation-instructions/).

- **Required:** strict 10-minute oral slot; 16:9 slides; own laptop over HDMI; test beforehand and carry USB backup.
- **Recommended by source:** speak for no more than 7 minutes and leave at least 3 minutes for questions.
- The presenter page publishes no mandatory author slide template, palette, font, or logo.

Separate artifact rules: [Final Author Instructions](https://2026.ieee-icra.org/contribute/final-author-instructions/) specify graphical abstract, optional slide PDF, and non-attending-author video formats. These are not the live-slide style rules.

ICRA also publishes a [brand identity guide](https://2026.ieee-icra.org/about/brand-identity-and-guidelines/). It defines branding use, but the author presenter instructions do not require every author to adopt it. Sinew therefore treats branded styling as a separate, explicit design decision rather than conference compliance.

### RSS 2026

Source: [Presenter Information](https://roboticsconference.org/information/presentationInstructions/).

- **Required:** every accepted paper has a four-minute plenary oral plus poster; submit a self-advancing video no longer than 240 seconds; exactly 1920x1080 MPEG-4 named `Paper_X.m4v`; presenter speaks live while it plays.
- **Required:** no narration/audio except experimental sound needed for understanding, barring an explicitly approved remote exception.
- The page publishes no mandatory palette, font, logo, or slide template.

### IROS 2026

Current public source reviewed: [instructions for speakers unable to travel](https://2026.ieee-iros.org/attend/instructions-for-speakers-who-experience-travel-difficulties-and-cannot-attend/).

- The page distinguishes 3-minute lightning slots and focused presentations with 9 minutes speaking plus 2 minutes of questions.
- Remote-recording guidance uses 2:45 and 9:30 safe lengths, H.264, and a roughly quarter-screen speaker portrait beside slides.
- **Unknown:** complete general presenter workflow, live-slide aspect ratio, and any general upload details were not yet available in the reviewed source.
- **Do not reuse:** IROS 2025's five-minute centralized-upload workflow as a 2026 rule.

### CoRL 2026

Current source: [Instruction for Authors](https://2026.corl.org/contributions/instruction-for-authors).

- It states that every accepted paper receives a poster and selected papers receive an oral spotlight.
- **Unknown / pending:** the reviewed 2026 material did not publish presenter timing, upload, or visual requirements.

Historical comparison only: [CoRL 2025 Instruction for Presentations](https://2025.corl.org/contributions/instruction-for-presentations) used 8 minutes + 2 minutes Q&A for orals and a mandatory 60-second 1080p MP4 spotlight with a five-second title frame. Sinew intentionally does not encode those as 2026 rules.

### ICML 2026

Sources: [Presenter Instructions](https://icml.cc/Conferences/2026/PresenterInstructions), [Author Instructions](https://icml.cc/Conferences/2026/AuthorInstructions), and standing [Accessible Papers and Talks](https://icml.cc/Conferences/2023/AccessiblePapersAndTalks) guidance linked by current conference materials.

- **Required:** 15-minute oral slot; plan to speak for 12 minutes; own laptop over full-size HDMI; no physical laser pointer.
- The presenter page publishes no mandatory aspect ratio, palette, font, logo, or slide template.
- **ICML expectation:** clear, simple, uncrowded visuals; large sans-serif fonts; high contrast; do not rely on color alone; describe important visuals; verbally communicate visual content.

## Cross-event conclusion

No reviewed evidence supports venue-branded visual themes as general presentation requirements. Event instructions govern duration, aspect ratio, artifacts, AV, and accessibility. The one selected visual profile governs palette, fonts, surfaces, code, charts, and component styling. These concerns remain separate.

Only ICRA 2026 explicitly mandates 16:9 live slides among the reviewed presenter pages. RSS fixes 16:9 indirectly through its 1920x1080 mandatory video. Rules vary by edition and presentation type, so delivery documentation records its source and verification date without becoming render configuration.

## Adapted design sources

Four visual profiles were adapted from design-source system pages inspected on 2026-08-25:

| Sinew style | Design-source route | Adapted visual ideas |
|:--|:--|:--|
| `unmasked` | `/systems/unmasked/system.html` | Monochrome construction, exposed rules, square geometry, sans display with serif reading text |
| `the-give` | `/systems/give/system.html` | Periwinkle and mint surfaces, rounded forms, gentle depth, mixed display/reading type |
| `the-meeting` | `/systems/meeting/system.html` | Coral and teal voices joined by violet on a cool porcelain ground |
| `movement` | `/systems/motion/system.html` | Charged white, scarlet motion, green wake, condensed display type, directional diagonals |

The movement source slug is `motion`; the Sinew-facing name remains `movement`. The available source material did not provide a canonical public URL, owner, or license. Those gaps must be resolved before claiming endorsement or redistribution permission.

All four adaptations replace remote font dependencies with explicit offline fallbacks, strengthen small text/rules for projection, retain non-color series encodings, and map source colors into the full Sinew semantic token contract. Matching Matplotlib overlays reproduce surface, ink, grid, legend, and data-cycle roles using dependable installed fonts. Detailed per-style changes and known typography differences are recorded in [visual styles](styles.md).

## Citation style (CSL)

Both bundled CSL files (`styles/citations/ieee.csl`, the project default, and
`styles/citations/chicago-author-date.csl`, the documented author-year
alternative) were verified against their upstream source, license, and
vendoring date before being committed. Full provenance -- upstream commit,
`<info>`-block author of record, the CC BY-SA 3.0 license declared both in
each file's own `<rights>` element and in the upstream repository's README,
and the inspection/vendoring date -- is recorded once, in
[citations.md](citations.md), "CSL provenance", rather than duplicated here.
That record exists and both files' licenses were confirmed compatible with
redistribution in this repository before vendoring.

## Scientific visualization and accessibility

Primary sources:

- [SciencePlots](https://github.com/garrettj403/SciencePlots): composable Matplotlib styles; `import scienceplots` before `plt.style.use`; `science + ieee` targets paper column dimensions, not projected slides; `bright` is documented as color-blind safe.
- [SciencePlots FAQ](https://github.com/garrettj403/SciencePlots/wiki/FAQ): use `no-latex` without a TeX installation; CJK helpers are deprecated in favor of maintained font tooling.
- [Matplotlib fonts](https://matplotlib.org/stable/users/explain/text/fonts.html): PDF font embedding/subsetting; `svg.fonttype` path versus text tradeoff; fallback fonts for non-Latin glyphs.
- [WCAG 2.2 use of color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color): color must not be the sole information channel.
- [WCAG 2.2 non-text contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast): meaningful graphical objects generally need 3:1 contrast against adjacent colors for conformance.
- [WAI complex images](https://www.w3.org/WAI/tutorials/images/complex/): charts need a short text alternative plus a detailed textual equivalent or adjacent explanation.
- [IEEE Author Center graphics](https://conferences.ieeeauthorcenter.ieee.org/write-your-paper/improve-your-graphics/): consistent typography, embedded fonts, and line/color differentiation. These are publication recommendations, not oral-slide rules.

Sinew defaults based on these sources are documented in [figures and tables](figures-and-tables.md) and [accessibility](accessibility.md).
