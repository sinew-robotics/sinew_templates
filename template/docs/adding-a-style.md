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
- [ ] Define robust heading, body, and monospace stacks without a required CDN.
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
- [ ] Keep `_00-section.qmd` through `_09-references.qmd`; update every title and `data-style-preview` value.
- [ ] Give the table a unique `#tbl-gallery-<slug>` identifier.
- [ ] Give the local references slide the stable target `#references-<slug>`.
- [ ] Add a unique bibliography key such as `sinew<StyleName><Year>` to `references.bib`, linking to the public profile source.
- [ ] Cite that key in `_08-citations.qmd` and set it as `data-style-key` in `_09-references.qmd`.
- [ ] Append all ten includes to `deck.qmd` in the intended horizontal order.
- [ ] Add the slug to `styles/gallery/columns.html`.
- [ ] Mirror every profile token and font stack in `styles/gallery/columns.css` so runtime preview matches standalone rendering.
- [ ] Add any restrained style-specific gallery component rules needed for geometry or depth.

The column must keep the same guidance -> problem -> algorithm -> plot -> table -> conclusion -> generation -> citations -> references sequence. Do not add gallery-comparison narration to individual slides.

## 5. Register validation and documentation

- [ ] Add the slug to `COLORS` and its citation key to `STYLE_CITATION_KEYS` in `scripts/validate.py`.
- [ ] Add the slug to `STYLES` in `scripts/check_contrast.py`.
- [ ] Add the slug to `colors` in `scripts/render-styles.sh`.
- [ ] Add the slug to the gallery preview list in `scripts/check_render.py`.
- [ ] Add the profile to the style table in the repository `README.md`.
- [ ] Add a provenance/adaptation section to `docs/styles.md`.
- [ ] Add an `Unreleased` changelog entry.

## 6. Advance the version

A new visual profile is a user-visible feature, so advance the minor version in `_extensions/sinew/_extension.yml`:

- `0.3.0-dev` becomes `0.4.0-dev`;
- `1.0.0` becomes `1.1.0-dev`.

- [ ] Update the manifest `version` in the same pull request.
- [ ] Rebase before merge and resolve version conflicts so the merged value advances exactly once from current `main`.
- [ ] Keep the `-dev` suffix during review; removing it and creating a tag belong to the later release process.
- [ ] Mention the proposed version in the pull-request summary.

## 7. Run local quality gates

```bash
python3 scripts/validate.py
python3 scripts/check_contrast.py
scripts/render-styles.sh
quarto render --cache-refresh
scripts/check-render.sh _site/index.html
```

- [ ] Inspect the new standalone style and combined runtime-gallery column.
- [ ] Inspect 16:9, common widescreen, and ultrawide browser windows.
- [ ] Hover and keyboard-focus citations; confirm the hover card follows the style.
- [ ] Activate citations; confirm they open the local references slide.
- [ ] Verify figures, tables, algorithms, code, and references have no clipping or scrollbars.
- [ ] Test with the network disabled and with reduced motion enabled.
- [ ] Confirm `git diff --check` and inspect the final diff for generated or private files.

## 8. Open and review the pull request

- [ ] Push `style/<slug>` and open a pull request into `main`.
- [ ] Complete `.github/pull_request_template.md` and attach the requested screenshots.
- [ ] Download `sinew-gallery-pr-<number>` from the CI run and open `index.html` locally.
- [ ] Wait for approval and every required check.
- [ ] Update the branch if `main` moves, then re-run the checks.
- [ ] Merge only through the pull request and delete the branch afterward.

`main` deploys the reviewed gallery to GitHub Pages. Pull requests receive downloadable demos but do not replace the public site.
