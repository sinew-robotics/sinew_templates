# Changelog

## Unreleased

- Released nine selectable visual styles and a browser-based 2D gallery with one style per horizontal column.
- Standardized repeated guidance, problem, algorithm, plot, structured table, conclusion, and generation examples in every style.
- Added automatic bold numbering for figure, table, and algorithm captions, including procedural shell blocks.
- Added linked citation previews, profile-aware hover cards, a generated shared bibliography, and local references in every style column.
- Added structured result-table conventions: metric-direction arrows, a separated total column, bold best values, and highlighted final proposed-method rows.
- Added matching Matplotlib overlays, SciencePlots guidance, accessibility checks, agent instructions, and dated event-delivery research.
- Added a new-style TODO, branch/PR contribution rules, continuous validation, all-style rendering, pull-request demo artifacts, and GitHub Pages deployment for reviewed builds.
- Added explicit prior-review regression notes and zero-config checks that require plain `quarto render` to include every registered visual profile.

## 0.2.0  -  2026-08-25

- Simplified rendering to exactly one `color-*` profile per delivery deck.
- Replaced combination rendering with `scripts/render-styles.sh`, which validates every visual style independently.
- Expanded the gallery to nine visual styles and a shared guidance -> problem -> algorithm -> plot -> conclusion -> generation sequence.
- Added unmasked, the give, the meeting, and movement adaptations with documented design-source provenance; movement maps from the source slug `motion`.
- Added one Matplotlib overlay per visual style and `scripts/generate_gallery_plots.py` for comparable illustrative outputs.
- Reclassified venue/event research as dated background delivery guidance rather than render configuration.
- Prohibited level-3 and deeper slide headings because nested section tags can become unintended Reveal stacks.
- Required code to fit without scrollbars and adjacent content groups to retain visible vertical separation.
- Made patterned divider backgrounds full bleed on ultrawide displays while retaining the 16:9 content safe area.
- Made agent instruction files strictly ASCII-only and documented the machine-checkable character rule.

## 0.1.1  -  2026-08-25

- Replaced the default sample narrative with a multi-column visual-style gallery.
- Added neutral gallery metadata for runtime style previews.
- Made rendered grid validation derive its expected stack and slide counts from `deck.qmd`.
- Added runtime per-column style previews and repeated problem -> method -> evidence -> conclusion mini-decks.
- Added reusable `color-blueprint` and `color-scholar` visual profiles.
- Fixed ordered-list containment and wrapping inside highlighted generation checklists.

## 0.1.0  -  2026-08-25

- Added `sinew-revealjs` custom format and project starter.
- Added folder-backed multi-file 2D grid deck.
- Added dated delivery-research documents with sourced freshness metadata.
- Added Origami, paper, and high-contrast visual profiles.
- Added academic figure/table components, SciencePlots overlay, documentation, agent rules, and validation scripts.
