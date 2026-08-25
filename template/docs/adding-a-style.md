# New visual style TODO

Use this checklist for every new visual profile. A style is incomplete until it renders as a standalone deck, appears as a full gallery column, has a plot overlay and citable source, advances the extension version, and passes pull-request review.

## 1. Start a branch and provenance record

- [ ] Update local `main` with `git pull --ff-only`.
- [ ] Create `style/<slug>` from `main`; use lowercase ASCII and hyphens.
- [ ] Record source URL or route, owner, license, inspection date, and reviewed screens/components in `docs/styles.md`.
- [ ] State what was extracted, what was deliberately changed for projection/accessibility, and which protected assets were excluded.
- [ ] Confirm that fonts and assets are licensed for redistribution or replace them with offline fallbacks.

Do not place `.beads` or private network URLs in the template. A source record is not permission to redistribute its assets.

## 2. Implement the delivery profile

- [ ] Copy `styles/colors/paper.css` to `styles/colors/<slug>.css`.
- [ ] Set `--sinew-color-profile: "<slug>"` and every required `--sinew-*` token.
- [ ] Define robust heading, body, and monospace stacks without a required CDN. Set `--sinew-algorithm-font` to a genuine monospace stack that fits the profile; never reuse a proportional display face for algorithm bodies or captions.
- [ ] Check text, muted text, links, rules, statuses, and all five data colors with `scripts/check_contrast.py`.
- [ ] Add `_quarto-color-<slug>.yml` with the new CSS and syntax-highlighting choice.
- [ ] Append `color-<slug>` to the single profile group in `_quarto.yml`.

Profiles own palette, typography, surfaces, syntax highlighting, and plot tokens. They do not encode event rules or alter the evidence narrative.

## 3. Add the figure style

- [ ] Copy a nearby `styles/matplotlib/sinew-<name>.mplstyle` to `styles/matplotlib/sinew-<slug>.mplstyle`.
- [ ] Preserve the same data-color order as the CSS and add marker/dash redundancy.
- [ ] Add `<slug>` to `scripts/generate_gallery_plots.py`.
- [ ] Generate `assets/figures/gallery-<slug>.svg`.
- [ ] Inspect labels, legends, grayscale separation, transparent surfaces, and projected size.

## 4. Add a complete index column

- [ ] Copy one complete numbered folder under `_slides/` to the next available folder, such as `11-<slug>/`.
- [ ] Keep the complete 11-slide file set from `_00-section.qmd` through `_09-references.qmd`, including `_03-research.qmd` as well as `_03-algorithm.qmd`; update every title and `data-style-preview` value.
- [ ] Give the table a unique `#tbl-gallery-<slug>` identifier.
- [ ] Give both algorithm captions stable `#algorithm-gallery-<slug>-method` and `#algorithm-gallery-<slug>-render` identifiers.
- [ ] Give the local references slide the stable target `#references-<slug>`.
- [ ] Add a unique bibliography key such as `sinew<StyleName><Year>` to `references.bib`, linking to the public profile source.
- [ ] Cite that key in `_08-citations.qmd` and set it as `data-style-key` in `_09-references.qmd`.
- [ ] Append all eleven includes to `deck.qmd` in the intended horizontal order.
- [ ] Add the slug to `styles/gallery/columns.html`.
- [ ] Mirror every profile token and font stack in `styles/gallery/columns.css` so runtime preview matches standalone rendering.
- [ ] Add any restrained style-specific gallery component rules needed for geometry or depth.

The column must keep the same guidance -> problem -> research framing -> algorithm -> plot -> table -> conclusion -> generation -> citations -> references sequence. Do not add gallery-comparison narration to individual slides.

## 5. Register validation and documentation

- [ ] Add the slug to `COLORS` and its citation key to `STYLE_CITATION_KEYS` in `scripts/validate.py`.
- [ ] Add the slug to `STYLES` in `scripts/check_contrast.py`.
- [ ] Add the slug to `colors` in `scripts/render-styles.sh`.
- [ ] Run `scripts/check_render.py`; it discovers `_quarto-color-*.yml` files automatically and must find one rendered column per profile.
- [ ] Add the profile to the style table in the repository `README.md`.
- [ ] Add a provenance/adaptation section to `docs/styles.md`.
- [ ] Add an `Unreleased` changelog entry.

## 6. Preserve every prior review catch

These are acceptance notes from regressions found while developing the existing profiles. Treat each item as part of the style contract, even if the copied column currently looks correct.

### Style and content boundaries

- [ ] Keep the profile event-neutral. Do not add conference profiles, conference names, venue colors, logos, timing, or upload rules to the visual-style axis.
- [ ] Preserve the complete repeated story in every column: divider, guidance, problem, research framing, algorithm, plot, table, conclusion, generation, citations, and references.
- [ ] Keep the evidence content and slide order structurally equivalent across styles; only the visual treatment and style-specific source citation change.
- [ ] Remove gallery-comparison meta-copy such as "identical pseudocode," "identical data," "same claim," "shared story," "appearance only," or similar notes from visible slides.
- [ ] Keep one Q1-Q9 question list, one H1-H9 hypothesis list, one algorithm, one style-specific plot, one structured table, and one local citation/reference example in every column.
- [ ] Keep the local reference example wired to `@fig-gallery-<slug>`, `@tbl-gallery-<slug>`, `{{< alg algorithm-gallery-<slug>-method >}}`, `{{< q 1 >}}`, and `{{< h 1 >}}`.

### Keyboard characters, spacing, and overflow

- [ ] Use only printable ASCII from a standard US keyboard in slide source and visible text. Do not paste Unicode arrows, bullets, multiplication signs, smart quotes, dashes, daggers, or math glyphs.
- [ ] Put mathematical notation inside dollar delimiters with ASCII LaTeX commands. Metric directions use `$\uparrow$` and `$\downarrow$`, never Unicode arrow characters.
- [ ] Keep visible vertical gaps between adjacent content groups, especially on the copied problem, research framing, algorithm/evidence, and generation slides (`_02`, both `_03` slides, and `_07`).
- [ ] Make the final checklist/highlight block contain every bullet completely; preserve its padding, wrapping, and width.
- [ ] Keep code, `pre`, syntax wrappers, and copy-button wrappers free of horizontal and vertical scrollbars. Wrap short code and split long examples instead of scrolling or shrinking.

### Responsive and ultrawide backgrounds

- [ ] Keep section-divider backgrounds full bleed through the Reveal viewport/background layer. Do not size a background only to the centered 16:9 content canvas.
- [ ] Inspect an ultrawide viewport and confirm both outer edges use the same intended background as the center.
- [ ] Keep substantive content inside the 1600x900 safe canvas while allowing only decorative backgrounds to extend beyond it.
- [ ] Check common widescreen and ultrawide layouts for clipped headings, cards, navigation controls, and footers.

### Figures and plots

- [ ] Remember that Reveal CSS does not recolor a static plot. Add and apply the matching Matplotlib overlay, then regenerate the profile-specific SVG.
- [ ] Match the CSS data-color order, while retaining marker, dash, direct-label, or shape redundancy so color is never the only encoding.
- [ ] Keep the figure caption below the figure with a bold generated `Figure N` identifier and normal-weight descriptive text.
- [ ] Verify axes, units, legends, labels, line weights, grayscale separation, transparent surfaces, and projected font size.

### Structured result tables

- [ ] Put `$\uparrow$` or `$\downarrow$` in every reference metric heading according to direction.
- [ ] Keep `Total` as the final column and separate it with the strong vertical rule.
- [ ] Bold the best result independently in each metric column.
- [ ] Put only the final contiguous `Ours:` rows in the `.ours-last-N` highlight block.
- [ ] Keep baselines such as Behavior Cloning and Diffusion Policy visually identical and unhighlighted; a strong metric value may be bold without highlighting the row.
- [ ] Keep the caption above the table, with a bold generated `Table N` identifier, and state the arrow, best-value, total-column, and proposed-row conventions.

### Algorithms and procedural code

- [ ] Give algorithms a deliberate, profile-appropriate monospace stack through `--sinew-algorithm-font`; verify both code and caption use it in standalone and gallery renders.
- [ ] Place the algorithm caption immediately below its code and inside the same code column/container, never beneath an adjacent right-hand block.
- [ ] Start the caption with `**Algorithm.**`; the runtime must produce a bold, sequential `Algorithm N` label.
- [ ] Number and caption the generation command block on `_07-generate.qmd` as an algorithm too.
- [ ] Confirm both procedural blocks fit without scrollbars and that their captions stay attached at all checked viewports.

### Research questions and hypotheses

- [ ] Preserve `<ol class="research-questions">` and `<ol class="research-hypotheses">`; CSS counters must render Q1-Q9 and H1-H9 without identifiers typed into item text.
- [ ] Keep each list to one through nine items. Split longer sets across explicit slides rather than producing Q10/H10 or shrinking the slide.
- [ ] Keep exactly two large research panels, one around all questions and one around all hypotheses. Keep statement rows unboxed; the Q/H identifier is the only per-statement bounded shape.
- [ ] Use `.is-highlighted` on at most one primary question and one primary hypothesis. Keep its filled/thicker identifier and text weight so emphasis is not color-only.
- [ ] Let questions inherit the profile accent and hypotheses inherit the profile success color. Do not add slide-local color overrides.
- [ ] Map every question/hypothesis to evidence or visibly mark it unresolved, and keep illustrative gallery wording labeled as a placeholder.
- [ ] Reference questions and hypotheses only with `{{< q N >}}` and `{{< h N >}}`. Keep the rendered inline labels bare, with no permanent box or pill, and preserve keyboard-visible underline/weight.

### Fullscreen evidence inspection

- [ ] Preserve click-to-open and click-to-close interaction for figures, tables, and captioned algorithms without visible `Expand` or fullscreen `Close` controls.
- [ ] Test click, second-click dismissal, Enter/Space activation, Escape, and focus return for every evidence type.
- [ ] Confirm the dialog inherits the active profile, prevents Reveal navigation while open, removes duplicate IDs/copy controls from clones, and lets every evidence type and its caption upscale on ultrawide viewports without distortion or scrollbars.
- [ ] Keep the original evidence legible on its slide; fullscreen inspection is not a workaround for overflow.

### Citations and references

- [ ] Give the style its own BibTeX key and stable public profile URL; do not cite a private network route.
- [ ] Preserve exactly one global `#refs` citeproc source and one generated `.style-references` view per style. Do not hand-copy bibliography prose or duplicate `ref-*` IDs.
- [ ] Keep references in two columns, keep each entry unsplit, and remove every reference scrollbar. Reduce/split scope instead of shrinking illegibly.
- [ ] Verify pointer hover and keyboard focus. The Tippy card must inherit the current profile's surface, ink, border, accent, radius, and font stack.
- [ ] Hover/focus the figure, table, method algorithm, Q1, and H1 links; confirm each preview contains the correct original object or statement and inherits the active profile. Confirm cloned math renders and the table card is wide enough to read every column.
- [ ] Activate bibliography citations and confirm they route to the local `#references-<slug>` slide. Activate internal references and confirm they route to the original figure, table, algorithm, question, or hypothesis in the same column.
- [ ] Confirm DOI/project links are actionable and open in a new tab with `noopener`.

### Affiliation marks

- [ ] Preserve the canonical `.institution-lockup` on the divider example and the all-slide replication runtime unless the presentation owner explicitly removes or replaces the affiliations.
- [ ] Keep logo aspect ratios, informative alt text, source transparency, and recorded authorization/provenance. Light profiles leave the lockup unbacked; dark profiles define a light plate from their own palette rather than generic white. Do not recolor protected marks.
- [ ] Confirm both marks remain legible without clipping on every slide across light, dark, 16:9, and ultrawide backgrounds.

### Repository and demo integrity

- [ ] Do not commit `_site`, `_build`, `.quarto`, private URLs, machine-specific paths, protected source assets, secrets, or `.beads`.
- [ ] Run the zero-config `quarto render` and confirm the demo contains exactly one horizontal column for every `_quarto-color-*.yml` profile, with no source edits or profile argument.
- [ ] Run each standalone color profile as well; the combined demo passing does not prove a delivery profile passes.
- [ ] Review the pull-request demo artifact before merge, then verify the public Pages build after merge.

## 7. Advance the version

A new visual profile is a user-visible feature, so advance the minor version in `_extensions/sinew/_extension.yml`:

- `0.3.0-dev` becomes `0.4.0-dev`;
- `1.0.0` becomes `1.1.0-dev`.

- [ ] Update the manifest `version` in the same pull request.
- [ ] Rebase before merge and resolve version conflicts so the merged value advances exactly once from current `main`.
- [ ] Keep the `-dev` suffix during review; removing it and creating a tag belong to the later release process.
- [ ] Mention the proposed version in the pull-request summary.

## 8. Run local quality gates

```bash
python3 scripts/validate.py
python3 scripts/check_contrast.py
scripts/render-styles.sh
quarto render --cache-refresh
scripts/check-render.sh _site/index.html gallery
```

- [ ] Inspect the new standalone style and combined runtime-gallery column.
- [ ] Confirm plain `quarto render` includes every registered style without edits or a profile argument.
- [ ] Inspect 16:9, common widescreen, and ultrawide browser windows.
- [ ] Hover and keyboard-focus citations; confirm the hover card follows the style.
- [ ] Activate citations; confirm they open the local references slide.
- [ ] Hover/focus and activate the figure, table, algorithm, Q1, and H1 links on the citation slide; confirm previews and original-target routes.
- [ ] Verify figures, tables, algorithms, code, and references have no clipping or scrollbars.
- [ ] Activate the fullscreen inspector for a figure, table, and both algorithm types in the new profile.
- [ ] Test with the network disabled and with reduced motion enabled.
- [ ] Confirm `git diff --check` and inspect the final diff for generated or private files.

## 9. Open and review the pull request

- [ ] Push `style/<slug>` and open a pull request into `main`.
- [ ] Complete `.github/pull_request_template.md` and attach the requested screenshots.
- [ ] Download `sinew-gallery-pr-<number>` from the CI run and open `index.html` locally.
- [ ] Wait for approval and every required check.
- [ ] Update the branch if `main` moves, then re-run the checks.
- [ ] Merge only through the pull request and delete the branch afterward.

`main` deploys the reviewed gallery to GitHub Pages. Pull requests receive downloadable demos but do not replace the public site.
