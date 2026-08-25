# Style extension contract

Sinew has one visual-style axis. A presentation selects exactly one `color-*` profile, which owns palette, fonts, surfaces, syntax highlighting, and chart tokens. Timing, artifact, upload, and event requirements are not profiles and do not belong in style files.

## Add a color style

1. Copy `styles/colors/paper.css` to `styles/colors/<name>.css`.
2. Define every `--sinew-*` color token plus explicit sans, serif when used, and monospace fallback stacks.
3. Record source URL/path, source slug, owner/license when known, inspection date, extracted roles, and deliberate projection/accessibility adaptations.
4. Add `_quarto-color-<name>.yml` that contributes the CSS and a code highlight style.
5. Add `color-<name>` to the single profile group in `_quarto.yml`.
6. Add `styles/matplotlib/sinew-<name>.mplstyle`. Match plot surfaces, ink, grid, and data-cycle roles; document intentional font or color differences.
7. Add `<name>` to the style lists in `scripts/generate_gallery_plots.py` and `scripts/render-styles.sh`.
8. Run the plot generator, contrast checks, and all-style renders.

```bash
python3 scripts/generate_gallery_plots.py
python3 scripts/check_contrast.py
scripts/render-styles.sh
```

CSS variables are the public deck-styling API. Avoid selectors tied to a particular sample slide. Theme CSS may restyle semantic classes from `core.scss`, but it must not change slide meaning, order, or delivery metadata.

## Matplotlib pairing

Static plots do not inherit Reveal CSS. Compose the common projected-slide settings first and the selected palette overlay last:

```python
plt.style.use([
    "styles/matplotlib/sinew-slides.mplstyle",
    "styles/matplotlib/sinew-origami.mplstyle",
])
```

Available per-style overlays are `origami`, `paper`, `high-contrast`, `blueprint`, `scholar`, `unmasked`, `the-give`, `the-meeting`, and `movement`. The movement style is adapted from a design source whose route slug is `motion`; do not rename the Sinew profile or overlay to `motion`.

`scripts/generate_gallery_plots.py` renders the same explicitly illustrative chart in every style. Its values are not experimental evidence and must not be reused as results.
