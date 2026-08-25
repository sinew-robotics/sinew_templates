# Figures, tables, and robotics media

## Evidence standard

A visual is ready only when an unfamiliar expert can answer:

- What is compared?
- On which task/population/data split?
- What do axes, units, markers, bands, and symbols mean?
- How many trials, episodes, participants, environments, or seeds support it?
- What aggregation and uncertainty are shown?
- Is the claim descriptive, predictive, or causal?
- Is the result simulated, real-world, retrospective, or prospective?
- What source and license apply?

## Figures

Prefer SVG for plots/diagrams and PNG/JPEG for photos, camera frames, heatmaps, and dense raster sensor data. Avoid screenshots of plots: source vectors/raster exports preserve size, contrast, and typography.

Quarto syntax:

```markdown
![Finding-oriented caption](assets/figures/result.svg){
  #fig-result
  width="82%"
  fig-alt="Line plot of success versus training steps. The solid circle-marked method reaches 80% around twice as early as the dashed square-marked baseline."
}
```

For a complex chart, add a detailed prose/table equivalent in the slide, appendix, or linked handout. Alt text identifies the important structure and finding; the caption states conditions, statistics, and provenance. Do not repeat identical text in both.

### Plot content

- Put units in axes.
- Use a meaningful zero/baseline; disclose truncation.
- Direct-label curves when possible.
- Combine color with dash, marker, hatch, position, or text.
- Define bands/error bars and report `n`/seeds.
- Use consistent scales across comparison panels.
- Use perceptually uniform sequential maps (`viridis`, `cividis`, `magma`, `inferno`) for ordered magnitude.
- Use a diverging map only when the center has meaning.
- Do not use a categorical rainbow for ordered values.
- Show failure cases when they bound the robotics claim.

## SciencePlots and Matplotlib

Install reproducibly:

```bash
python -m pip install -r requirements-plotting.txt
```

SciencePlots 2.x requires an explicit import. Layer styles from general to specific, with Sinew last:

```python
from pathlib import Path

import matplotlib.pyplot as plt
import scienceplots

ROOT = Path(__file__).resolve().parents[1]
STYLE = "origami"  # Match the deck's one selected color-* profile.
plt.style.use([
    "science",
    "no-latex",
    "notebook",
    "bright",
    str(ROOT / "styles/matplotlib/sinew-slides.mplstyle"),
    str(ROOT / f"styles/matplotlib/sinew-{STYLE}.mplstyle"),
])

fig, ax = plt.subplots(figsize=(10, 5.5), constrained_layout=True)
ax.plot(x, ours, marker="o", label="Proposed")
ax.plot(x, baseline, marker="s", linestyle="--", label="Baseline")
ax.set(xlabel="Training steps", ylabel="Success rate (%)")
ax.legend(frameon=False)
fig.savefig(ROOT / "assets/figures/result.svg")
```

`science + ieee` targets paper-column width and publication typography. It is not a projected-slide style. `notebook` plus the common Sinew overlay gives projected dimensions; the final per-style overlay supplies surfaces, ink, grid, legend, and data-cycle colors. Adapt final figure size to the slide.

The committed overlay uses 18 pt base/axis labels, 16 pt ticks/legend, 2.5 pt lines, 8 pt markers, TrueType PDF text (`pdf.fonttype: 42`), and SVG glyph paths for deterministic appearance. These are Sinew defaults, not conference mandates.

For editable/searchable SVG text, use `svg.fonttype: none` only when fonts are available or embedded on the presentation machine. Matplotlib documents that path mode is more consistent across machines but not editable. For Korean/CJK, explicitly add Noto Sans CJK/Source Han Sans and run a glyph test; SciencePlots' legacy CJK helpers are deprecated.

### Match figures to the selected visual style

Static figures do not automatically inherit Reveal CSS. Choose one of these reproducible policies:

1. Use a neutral white plot surface that meets contrast in every deck.
2. Export the figure with the overlay matching the deck's one selected `color-*` profile.
3. Generate SVG from a shared palette manifest, preserving the exact token mapping.

Do not make a plot transparent unless every text, grid, and data color remains legible on the selected background.

Sinew provides one overlay per style:

- `sinew-origami.mplstyle`
- `sinew-paper.mplstyle`
- `sinew-high-contrast.mplstyle`
- `sinew-blueprint.mplstyle`
- `sinew-scholar.mplstyle`
- `sinew-unmasked.mplstyle`
- `sinew-the-give.mplstyle`
- `sinew-the-meeting.mplstyle`
- `sinew-movement.mplstyle`

Use `movement` for the public Sinew style even though its design-source route slug is `motion`.

Generate the repository's same illustrative learning curve in every style with:

```bash
python3 scripts/generate_gallery_plots.py
```

The generator composes Matplotlib `default`, the common projected-slide overlay, and the per-style overlay in that order. Outputs are `assets/figures/gallery-<style>.svg`. They exercise visual integration only: their fictional curves and spread are labeled illustrative and are not evidence. When generating a real result, preserve the selected overlay order but replace the example data and metadata with traceable inputs.

## Tables

Use semantic Markdown/HTML, not an image. Sinew uses an academic booktabs-like treatment: strong top/bottom rules, one header rule, and restrained row separators. Structured result tables add one strong vertical rule before the final `Total` column. Table captions appear above; figure captions appear below.

```markdown
::: {.structured-results .ours-last-2}
| Method | Success (%) $\uparrow$ | Peak force (N) $\downarrow$ | Recovery (%) $\uparrow$ | Total $\uparrow$ |
|:--|--:|--:|--:|--:|
| Behavioral cloning | 61.0 | **8.2** | 49.0 | 55.0 |
| Diffusion policy | 76.0 | 10.8 | 65.0 | 70.0 |
| Ours: contact objective | 82.0 | 9.6 | 74.0 | 78.0 |
| Ours: contact + recovery | **86.0** | 9.1 | **81.0** | **84.0** |

: Illustrative placeholder, not experimental evidence. Fictional metrics over 100 fictional trials per method. Arrows show preferred direction; bold marks the best value per metric. The highlighted final two rows are proposed methods. {#tbl-main}
:::
```

- Keep one header row; avoid nested headers on projected slides.
- Put units in headings.
- Use ASCII LaTeX `$\uparrow$` and `$\downarrow$` to mark higher-is-better and lower-is-better metrics.
- Align numbers by decimal intent and use consistent precision.
- Avoid reporting more precision than measurement/evaluation supports.
- Put `Total` last and wrap the table in `.structured-results` for its strong separator.
- Bold the best value in each metric column and define bold in the caption.
- Put proposed methods in the final contiguous rows, prefix their names with `Ours:`, and select `.ours-last-1`, `.ours-last-2`, `.ours-last-3`, or `.ours-last-4` to highlight them. The text label and caption preserve meaning without color.
- Use a figure instead if the audience should see trend/shape rather than exact values.
- Move full benchmark tables to a vertical appendix slide or handout.

## Captions

Sinew renders the automatic `Figure N` and `Table N` identifier in bold while leaving the descriptive caption at normal weight. Do not type the identifier manually. Put a visible `.algorithm-caption` directly beneath procedural code and inside the same column or container. Start it with `**Algorithm.**`; Sinew renders that source label as a globally numbered, bold `Algorithm N` identifier. State scope, inputs/outputs, and evidence status or provenance. Procedural shell blocks need the same treatment.

A strong caption includes:

1. content/metric;
2. task/population/scope;
3. aggregation and uncertainty;
4. number of trials/seeds/samples;
5. source/status when reused, adapted, preliminary, or illustrative.

Examples:

- **Result.** Median task success over 384 evaluation episodes; bands are 95% bootstrap intervals over episodes; one training seed. Simulation only.
- **Adapted from Smith et al. (2025), Fig. 3.** Architecture redrawn; colors and annotations changed. Used under CC BY 4.0.
- **Illustrative placeholder - not evidence.** Replace values and source before release.

## Robotics video

- Label real/simulation, playback speed, controller/policy, task, and evaluation condition.
- Show representative failures when they qualify the claim.
- Keep experimental sound only when informative and explain it.
- Caption speech and provide a transcript for released recordings.
- Add `poster` fallback and controls; avoid unpausable autoplay lasting over five seconds.
- Ship local media. Test codec, resolution, seeking, and muted playback offline.
- If `embed-resources: true` fails for MP4 in the target browser, set it to false and serve the deck plus assets over local HTTP.

## Truthfulness gate

Illustrative values are labeled in the starter. An agent must never replace them with plausible numbers, reconstruct missing uncertainty, or infer experimental settings. Stop and request the evidence or mark the slide preliminary/missing.
