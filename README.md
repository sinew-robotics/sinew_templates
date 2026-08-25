# sinew_templates

[![Build and deploy gallery](https://github.com/domrachev03/sinew_templates/actions/workflows/pages.yml/badge.svg)](https://github.com/domrachev03/sinew_templates/actions/workflows/pages.yml)

An academic Quarto/Reveal.js presentation starter for robotics and machine-learning research. Sinew uses one selectable visual-style profile for palette, type, surfaces, syntax highlighting, and plot tokens:

```bash
quarto render --profile color-origami
```

The [live gallery](https://domrachev03.github.io/sinew_templates/) has one introduction column and one column for each of the nine visual styles. Move right between styles and down through the guidance -> problem -> algorithm -> plot -> table -> conclusion -> generation sequence. Runtime gallery code previews the style represented by each column. A real talk selects exactly one `color-*` profile for the whole deck. Local output is `_site/index.html`.

## What is included

- An installable `sinew-revealjs` custom format under `_extensions/sinew/`.
- A starter project with one slide per underscore-prefixed `.qmd` file.
- Folder-backed horizontal subtopics and vertical evidence stacks using Reveal's 2D grid.
- Nine visual profiles: Origami, paper, high contrast, blueprint, scholar, unmasked, the give, the meeting, and movement.
- Semantic figure, table, evidence, metric, source, and takeaway styles.
- A common projected-figure overlay, one matching Matplotlib overlay per visual style, and a plot generator.
- Human documentation plus comprehensive `AGENTS.md` and `CLAUDE.md` operating rules.
- Structural validation and an all-styles rendering script.

The researched venue pages are background delivery guidance only. They do not configure Quarto and do not define visual styles. Verify the exact current event instructions separately before delivery; see [venue and event delivery research](docs/conferences/README.md).

## Requirements

- Quarto `>=1.5.0` (tested with 1.9.38)
- A modern browser
- Python 3.10+ only for validation and optional plot generation
- Optional plotting stack: Matplotlib and SciencePlots 2.2.2

## Use this repository now

```bash
quarto preview
quarto preview --profile color-origami
quarto render --profile color-high-contrast
```

Open `_site/index.html`. The starter embeds resources by default, so it works offline unless you add non-embedded media or remote fonts.

Use arrow keys for the two-dimensional narrative:

- left/right: change subtopic;
- up/down: move within a subtopic;
- Space: traverse every slide linearly;
- `O`: overview; `S`: speaker view; `F`: fullscreen.

Quarto warns that vertical slides are unfamiliar and can be skipped. The template keeps arrow controls visible, uses `navigation-mode: grid`, and recommends putting the required talk path at vertical index 1, with drill-down detail below.

## Use as a starter after publishing to GitHub

```bash
quarto use template domrachev03/sinew_templates
```

Quarto copies the project scaffold and bundled extension. `deck.qmd` has a stable name because project starter files named `template.qmd` are automatically renamed, which would break an explicit render target.

Quarto deliberately excludes root `README.md`, `LICENSE`, `AGENTS.md`, and `CLAUDE.md` from starter copies. Copy the shipped agent templates after scaffolding:

```bash
cp docs/agent-templates/AGENTS.template.md AGENTS.md
cp docs/agent-templates/CLAUDE.template.md CLAUDE.md
```

If those docs were excluded by your distribution workflow, copy them from the source repository.

## Add only the format to an existing Quarto project

After this repository has a GitHub remote:

```bash
quarto add domrachev03/sinew_templates
```

Then use `format: sinew-revealjs`. Color profile files are part of the starter layer, not the extension-only install; copy one profile and its CSS or add equivalent project metadata.

## Multi-file 2D authoring

`deck.qmd` is an ordered manifest. A folder is one horizontal stack; its level-1 divider and level-2 content slides are separate files:

```text
deck.qmd
_slides/
  01-intro/
    _00-section.qmd     # # Introduction {.section-slide}
    _01-navigation.qmd  # ## A full-sentence supported claim
    _02-selection.qmd
  02-method/
    _00-section.qmd
    _01-status.qmd
```

The manifest includes each file explicitly:

```markdown
{{< include _slides/01-intro/_00-section.qmd >}}

{{< include _slides/01-intro/_01-navigation.qmd >}}
```

Keep includes on their own lines with blank lines around them. Included content is textually inserted; asset paths resolve relative to `deck.qmd`, not the included file. Included files contain no YAML.

Do not use level-3 or deeper headings inside a slide. Pandoc can emit nested section tags for them, and Reveal may interpret those tags as additional slide stacks. Use bold inline labels, `.kicker`, `.eyebrow`, or a semantic container instead.

See [authoring](docs/authoring.md) for slide anatomy, speaker notes, references, computations, media, and safe grid use.

## Visual styles

| Color profile | Intent |
|:--|:--|
| `color-origami` | Dark workbench adapted from the local Origami segmentation viewer |
| `color-paper` | Warm light surface for general academic talks |
| `color-high-contrast` | Minimal motion, high-contrast projection and accessibility fallback |
| `color-blueprint` | Deep-blue technical drawing surface with a cyan signal color |
| `color-scholar` | Spacious editorial surface with serif headings and purple accents |
| `color-unmasked` | Monochrome structure with exposed rules and square geometry |
| `color-the-give` | Periwinkle and mint surfaces with gentle depth |
| `color-the-meeting` | Coral and teal signals meeting in violet |
| `color-movement` | Charged white, scarlet motion, green wake, and condensed display type |

Select exactly one profile for a deck. Render and verify every style with:

```bash
scripts/render-styles.sh
```

Outputs go to a fresh external temporary directory so Quarto cannot recursively copy prior builds as project resources. Set `SINEW_BUILD_DIR=/absolute/path` to retain them at a known location outside the project.

Generate the matching illustrative Matplotlib figure for all styles with:

```bash
python3 scripts/generate_gallery_plots.py
```

Each plot composes `sinew-slides.mplstyle` with `sinew-<style>.mplstyle`. See [figures and tables](docs/figures-and-tables.md) before applying the palette to real evidence.

## Documentation

- [Research record](docs/research-notes.md): authoritative sources and hard-rule versus house-default labels.
- [Venue and event delivery research](docs/conferences/README.md): dated background guidance and re-verification procedure; not render configuration.
- [Authoring](docs/authoring.md): multi-file grid workflow and slide structure.
- [Figures and tables](docs/figures-and-tables.md): captions, alt text, statistics, SciencePlots, exports, robotics media.
- [Styles](docs/styles.md): token contract, Origami provenance, fonts, adding new styles.
- [Accessibility](docs/accessibility.md): WCAG-oriented HTML baseline and manual checks.
- [Architecture](docs/architecture.md): extension/starter boundaries and profile merge design.
- [Agent workflow](AGENTS.md): evidence and quality gates for automated authors.

## Validate

```bash
python3 scripts/validate.py
python3 scripts/check_contrast.py
scripts/check-render.sh _site/index.html
```

The validator checks style coverage, included slide ownership/order, heading levels, figure alt text, captions, placeholder disclosures, and absence of `.beads`. The render check verifies the selected style marker and nested Reveal sections in generated HTML.

## Continuous delivery

Every push and release tag runs structural and contrast validation, renders all nine standalone styles, builds the combined gallery, and checks the generated Reveal hierarchy. Successful non-pull-request builds deploy `_site/` to GitHub Pages. The workflow is defined in [`.github/workflows/pages.yml`](.github/workflows/pages.yml).

## Status and scope

This repository is an academic authoring system, not an official event template. Delivery rules change by event, edition, track, and presentation type; consult current official instructions instead of expecting a visual profile to encode them.
