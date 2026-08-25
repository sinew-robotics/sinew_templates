# sinew_templates

[![Build and deploy gallery](https://github.com/sinew-robotics/sinew_templates/actions/workflows/pages.yml/badge.svg)](https://github.com/sinew-robotics/sinew_templates/actions/workflows/pages.yml)

An academic Quarto/Reveal.js presentation starter for robotics and machine-learning research. Render the zero-config demo with every included style:

```bash
quarto render template
```

No profile selection or source edit is required for the demo. Sinew also provides one selectable visual-style profile for delivery builds, covering palette, type, surfaces, syntax highlighting, and plot tokens.

The [live gallery](https://sinew-robotics.github.io/sinew_templates/) has one introduction column and one column for each of the nine visual styles. Move right between styles and down through the guidance -> problem -> algorithm -> plot -> table -> conclusion -> generation -> citations -> references sequence. Runtime gallery code previews the style represented by each column. A real talk selects exactly one `color-*` profile for the whole deck. Repository builds write `template/_site/index.html`.

The self-contained Quarto project lives in `template/`. It contains all `_quarto-color-*.yml` profiles, `deck.qmd`, `references.bib`, slides, styles, assets, scripts, documentation, and the bundled extension. Repository-level governance and CI stay at the top level.

## What is included

- An installable `sinew-revealjs` custom format under `template/_extensions/sinew/`.
- A starter project with one slide per underscore-prefixed `.qmd` file.
- Folder-backed horizontal subtopics and vertical evidence stacks using Reveal's 2D grid.
- Nine visual profiles: Origami, paper, high contrast, blueprint, scholar, unmasked, the give, the meeting, and movement.
- Semantic figure, table, evidence, metric, source, and takeaway styles.
- Profile-aware citation hover cards, a generated shared bibliography, and local two-column references in every style column.
- A common projected-figure overlay, one matching Matplotlib overlay per visual style, and a plot generator.
- Human documentation plus comprehensive `AGENTS.md` and `CLAUDE.md` operating rules.
- Structural validation and an all-styles rendering script.

The researched venue pages are background delivery guidance only. They do not configure Quarto and do not define visual styles. Verify the exact current event instructions separately before delivery; see [venue and event delivery research](template/docs/conferences/README.md).

## Requirements

- Quarto `>=1.5.0` (tested with 1.9.38)
- A modern browser
- Python 3.10+ only for validation and optional plot generation
- Optional plotting stack: Matplotlib and SciencePlots 2.2.2

## Use this repository now

```bash
quarto render template
quarto preview template
quarto preview template --profile color-origami
quarto render template --profile color-high-contrast
```

Open `template/_site/index.html`. The first command is the zero-config gallery and includes every registered style column. The starter embeds resources by default, so it works offline unless you add non-embedded media or remote fonts.

Use arrow keys for the two-dimensional narrative:

- left/right: change subtopic;
- up/down: move within a subtopic;
- Space: traverse every slide linearly;
- `O`: overview; `S`: speaker view; `F`: fullscreen.

Quarto warns that vertical slides are unfamiliar and can be skipped. The template keeps arrow controls visible, uses `navigation-mode: grid`, and recommends putting the required talk path at vertical index 1, with drill-down detail below.

## Use as a starter

```bash
quarto use template sinew-robotics/sinew_templates/template
quarto render
```

The plain render command produces the complete gallery immediately; do not edit `deck.qmd` or select a profile merely to see the shipped styles.

Quarto accepts a repository subdirectory as the template target. It copies the project scaffold from `template/` and installs its bundled extension into the new presentation root. `deck.qmd` keeps a stable name because project starter files named `template.qmd` are automatically renamed, which would break an explicit render target.

The starter target is the `template/` subdirectory, so repository-level `README.md`, `LICENSE`, `AGENTS.md`, and `CLAUDE.md` are not copied. Install the shipped presentation-specific agent guides after scaffolding:

```bash
cp docs/agent-templates/AGENTS.template.md AGENTS.md
cp docs/agent-templates/CLAUDE.template.md CLAUDE.md
```

If those docs were excluded by your distribution workflow, copy them from the source repository.

## Add only the format to an existing Quarto project

```bash
quarto add sinew-robotics/sinew_templates/template
```

Then use `format: sinew-revealjs`. Color profile files are part of the starter layer, not the extension-only install; copy one profile and its CSS or add equivalent project metadata.

## Multi-file 2D authoring

In the repository, `template/deck.qmd` is the ordered manifest. In a scaffolded presentation it is `deck.qmd`. A folder is one horizontal stack; its level-1 divider and level-2 content slides are separate files:

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

See [authoring](template/docs/authoring.md) for slide anatomy, speaker notes, references, computations, media, and safe grid use.

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
template/scripts/render-styles.sh
```

Outputs go to a fresh external temporary directory so Quarto cannot recursively copy prior builds as project resources. Set `SINEW_BUILD_DIR=/absolute/path` to retain them at a known location outside the project.

Generate the matching illustrative Matplotlib figure for all styles with:

```bash
python3 template/scripts/generate_gallery_plots.py
```

Each plot composes `sinew-slides.mplstyle` with `sinew-<style>.mplstyle`. See [figures and tables](template/docs/figures-and-tables.md) before applying the palette to real evidence.

## Documentation

- [Research record](template/docs/research-notes.md): authoritative sources and hard-rule versus house-default labels.
- [Venue and event delivery research](template/docs/conferences/README.md): dated background guidance and re-verification procedure; not render configuration.
- [Authoring](template/docs/authoring.md): multi-file grid workflow, citation behavior, and slide structure.
- [Figures and tables](template/docs/figures-and-tables.md): captions, alt text, statistics, SciencePlots, exports, robotics media.
- [Styles](template/docs/styles.md): token contract, Origami provenance, fonts, adding new styles.
- [Accessibility](template/docs/accessibility.md): WCAG-oriented HTML baseline and manual checks.
- [Architecture](template/docs/architecture.md): extension/starter boundaries and profile merge design.
- [New visual style TODO](template/docs/adding-a-style.md): end-to-end style, index, citation, version, branch, PR, and CI checklist.
- [Agent workflow](AGENTS.md): evidence and quality gates for automated authors.
- [Contributing](CONTRIBUTING.md): GitHub branch protection and pull-request workflow.

## Validate

```bash
python3 template/scripts/validate.py
python3 template/scripts/check_contrast.py
quarto render template --cache-refresh
template/scripts/check-render.sh template/_site/index.html gallery
```

The validator checks style coverage, included slide ownership/order, heading levels, figure alt text, captions, placeholder disclosures, and absence of `.beads`. The render check verifies the selected style marker and nested Reveal sections in generated HTML.

## Continuous delivery

Every push, pull request, and release tag runs structural and contrast validation, renders every standalone style, builds the combined gallery, and checks the generated Reveal hierarchy and bibliography. Pull requests receive a downloadable `sinew-gallery-pr-<number>` demo artifact for review. Successful non-pull-request builds deploy `template/_site/` to GitHub Pages. The workflow is defined in [`.github/workflows/pages.yml`](.github/workflows/pages.yml).

## Status and scope

This repository is an academic authoring system, not an official event template. Delivery rules change by event, edition, track, and presentation type; consult current official instructions instead of expecting a visual profile to encode them. The repository is currently a pre-release preview; v1.0.0 will be created only after review approval.
