# Changelog

## Unreleased

- Centered slide content vertically by default and added named layout primitives (`.split-layout`, `.split-layout-reverse`, `.split-layout-connector`, `.split-layout-footer`, `.card-strip-3/5/12`, `.full-bleed-figure`, `.full-bleed-title`, `.diagram-flow`) for column, connector, card-strip, full-bleed, and flow-diagram shapes.
- Fixed figure/caption sizing so the caption box shrinks to the rendered image width instead of stretching to the column, and figures fill available space without hand-tuned `max-height` values.
- Made a video, GIF, or the new missing-evidence placeholder a full citizen of the `Figure N` sequence: any content wrapped in a `#fig-` fenced div with the caption as its trailing paragraph gets a real number, a `#fig-` id, and working `@fig-` cross-references.
- Added a managed video component: playback starts on slide enter and stops on slide leave, autoplay is muted by default with a `data-sinew-autoplay="false"` opt-out, and an optional trim window loops between `data-sinew-start`/`data-sinew-end` without cutting the source file.
- Extended click-to-zoom to video, GIFs, and placeholders alongside images; a zoomed video keeps its trim window and playback position.
- Added `.missing-evidence`, a numbered, cross-referenceable placeholder for a slide's intentionally unfilled evidence slot, with a dashed border, hatch fill, and a DOM-text "MISSING EVIDENCE" label so it stays unmistakable in grayscale.
- Added `.plate`, a light backing card for untouched artwork, mixed per color profile from that profile's own accent token.
- Added `template/scripts/make_transparent.py` (white-background-to-alpha PNG conversion, Pillow-based, with a documented residual limitation on near-maximally-saturated ink) and `template/requirements-imaging.txt`.
- Added `template/scripts/generate_demo_media.py` and synthetic demo media under `template/assets/media/` for exercising the new evidence types.
- Switched to numeric IEEE citations as the project default (`styles/citations/ieee.csl`); `chicago-author-date.csl` is bundled as the documented author-year alternative. Both are vendored from the official CSL project under CC BY-SA 3.0.
- Changed the shipped `navigation-mode` from `grid` to `default` for delivery decks so a forward Space walk reaches every slide instead of only the ones a row-preserving jump happened to land on; the zero-config gallery keeps `grid` for its own style-to-style comparison.
- Changed `slide-number` from `h.v` to `c` (sequential, depth-first), with `h.v` left as a one-line opt-back-in.
- Added `template/scripts/check_overflow.py`, a headless-browser overflow gate that measures actual slide geometry and exits 2 (not 0) when it cannot run.
- Split `validate.py` into universal and gallery-only checks so it runs on a scaffolded deck instead of crashing, derived extension paths from the matched manifest so a namespaced install validates correctly, and added lints for empty/unresolved citation keys, double captions, hand-numbered captions, structured-results table conventions, a single `#refs` target, and affiliation-mark provenance.
- Updated `check_render.py` to assert the correct Reveal navigation mode for both the gallery and a delivery render.

## 1.1.0  -  2026-08-25

- Added required Q1-Q9 research-question and H1-H9 research-hypothesis lists, with an optional non-color-only primary-item highlight and examples in every visual style.
- Retained two large research group panels while removing per-statement row boxes; per-item identity now lives in the Q/H labels, with a filled-label and text-weight primary highlight.
- Added bare Q/H reference shortcodes, stable algorithm references, and profile-aware hover/focus previews for figure, table, algorithm, question, and hypothesis links.
- Added a keyboard-accessible fullscreen inspector for every rendered figure, table, and captioned algorithm.
- Added owner-supplied KAIST and Interactive Robotic Systems Laboratory affiliation marks on every slide, preserving PNG transparency while giving dark profiles a light plate derived from their own palette.
- Simplified figure, table, and algorithm inspection to click-to-open and click-to-close without visible controls; removed fixed-width fullscreen caps and made captions viewport-responsive.
- Re-typeset math in cloned cross-reference previews and widened table hover cards for legible columns.
- Replaced accidental proportional algorithm type in unmasked, the give, the meeting, and movement with four profile-matched monospace stacks.
- Switched Reveal math rendering from the incompatible MathJax 2 loader to Quarto's KaTeX browser path so dollar-delimited table arrows render reliably.

## 1.0.0  -  2026-08-25

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
