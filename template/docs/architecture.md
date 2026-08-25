# Architecture

The public repository targets its `template/` subdirectory for starter and extension installation. After `quarto use template sinew-robotics/sinew_templates/template`, that subdirectory becomes the new presentation root, so all paths below are project-root-relative.

## Two products in one repository

1. `_extensions/sinew/` is the reusable custom format. `quarto add` installs only this layer.
2. The repository root is a project starter. `quarto use template` copies `deck.qmd`, slide files, color profiles, styles, plotting overlays, and assets.

This division keeps the format reusable in an existing project while giving new talks an opinionated academic workflow.

## Composition

`deck.qmd` is the deterministic manifest. Built-in include shortcodes are preferable to directory discovery because order is visible in review, a renamed slide does not silently change the talk, and no custom preprocessing is required.

With `slide-level: 2`:

- `#` creates a horizontal stack and its divider slide;
- `##` creates vertical slides within that stack.

Do not use level-3 or deeper headings inside slide files. Pandoc can emit nested section tags for nested headings, and Reveal can interpret those sections as additional stacks rather than ordinary slide content. Use bold inline labels, `.kicker`, `.eyebrow`, definition lists, or semantic containers instead.

Folders encode subtopics for authors; the level-1 and level-2 headings encode the structure Reveal consumes. One underscore-prefixed source file owns exactly one slide and contains no YAML.

## One visual-style axis

The starter has one mutually exclusive profile group:

```yaml
profile:
  default: [gallery, color-origami]
  group:
    - [color-origami, color-paper, color-high-contrast, color-blueprint,
       color-scholar, color-unmasked, color-the-give, color-the-meeting,
       color-movement]
```

Every delivery build selects exactly one `color-*` profile. That profile owns its color CSS, font stacks, syntax-highlighting choice, and machine-readable visual-style metadata. It does not own timing, upload, branding, or event rules.

The `gallery` metadata is an internal repository-tour layer. It loads the local Reveal event handler that previews a different visual treatment as the active gallery column changes. It is not a second visual-style profile and should not be added to a normal talk command.

A profile name typo can be silently ignored by Quarto, so validation checks the expected style marker in rendered HTML:

```css
--sinew-color-profile: "origami";
```

Render one style with `quarto render --profile color-origami`. Render every supported style independently with `scripts/render-styles.sh`; profiles are not combined.

## Styling API

`_extensions/sinew/theme/core.scss` owns semantic components and layout. Color profiles populate `--sinew-*` custom properties and font stacks. The public component surface is intentionally small:

- `.kicker` / `.eyebrow`
- `.figcap` / `.source`
- `.panel` / `.evidence-card`
- `.metric-row` / `.metric`
- `.tag`, `.hot`, `.ok`
- `ol.takeaways`
- `.section-slide`

New visual styles should target these roles and tokens, not sample-slide IDs.

## Plot-style pairing

Static figures do not inherit Reveal CSS. Each color profile therefore has a matching `styles/matplotlib/sinew-<style>.mplstyle` overlay. Compose the common `sinew-slides.mplstyle` first and the selected style overlay last. `scripts/generate_gallery_plots.py` exercises every overlay with the same illustrative chart so palette, text, grid, legend, marker, and line behavior can be compared.

## Delivery research boundary

`docs/conferences/` contains dated background research about event logistics. Those files are not profiles, do not merge into Quarto metadata, and do not alter the deck. Authors must verify the exact current event, edition, track, and artifact requirements separately from style selection.

## Resource policy

`embed-resources: true` is the offline-safe default. If a talk adds MP4 video, test the target browser: some browser/media combinations do not decode video from data URIs. In that case set `embed-resources: false`, ship the generated dependency directory and assets, and present over a local HTTP server.

Do not use remote font imports in delivery-critical decks. Bundle licensed fonts or specify robust system fallbacks and test on the presentation machine.
