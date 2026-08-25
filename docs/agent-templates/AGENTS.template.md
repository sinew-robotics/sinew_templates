# Sinew presentation agent instructions

Rename this file to `AGENTS.md` in a scaffolded presentation project. These rules apply to agents creating, revising, reviewing, or rendering the deck.

## Mission and startup

Produce an evidence-led academic talk that is truthful, legible, accessible, reproducible, offline-safe, and compliant with the exact delivery context.

Before editing, read `README.md` when available, `docs/research-notes.md`, `docs/authoring.md`, `docs/figures-and-tables.md`, and `docs/accessibility.md`. Read a relevant event guide only as dated background delivery guidance. Inspect exactly one selected `_quarto-color-<style>.yml`, `deck.qmd`, and all included slides. Run `git status`, `quarto --version`, and `python3 scripts/validate.py`.

Do not create `.beads` inside the presentation project. Keep any requested Beads/task tracker outside it. Preserve unrelated user changes; do not commit or push without explicit authority.

## Evidence and citations

- Never invent results, intervals, seeds, sample sizes, baselines, settings, citations, licenses, or delivery rules.
- Keep illustrative values labeled. If evidence is absent, narrow the claim, mark it preliminary/missing, or request the source.
- Distinguish simulation/real robot, offline/online, benchmark/deployment, and observed/causal claims.
- Show failures/negative results when they bound the conclusion.
- Verify citations against primary papers/official sources. Citation is not reuse permission.

## Style and delivery boundary

Select exactly one `color-*` profile. It owns palette, fonts, surfaces, syntax highlighting, and chart tokens. Event documents are dated background delivery research, not profiles. Before final delivery, reopen official current instructions for the exact edition, track, presentation type, and artifact. Never place timing, upload, or branding rules in a color profile.

## Slide structure

- Slide source and visible text use only printable ASCII characters from a standard US keyboard. This is machine-checkable: every byte in slide text outside code-generated assets must be ASCII 0x20-0x7E, plus newline and tab.
- Replace Unicode arrows, multiplication signs, bullets, daggers, smart quotes, dashes, and math symbols with words, ASCII punctuation, or ASCII LaTeX commands.
- Write mathematics with `$...$` inline and `$$...$$` for display math, using ASCII LaTeX commands.
- `deck.qmd` is the explicit ordered manifest.
- One underscore-prefixed included file equals one slide and contains no YAML.
- `#` divider slides form horizontal stacks; `##` claim slides form vertical slides.
- Do not use level-3 or deeper headings inside a slide. Pandoc can emit nested section tags that Reveal treats as stacks. Use bold inline labels, `.kicker`, `.eyebrow`, or semantic containers instead.
- Includes stand alone with blank lines; assets resolve from `deck.qmd`.
- Do not put body content before the first include; it creates a blank slide.
- Put the required narrative at the first vertical index; optional detail goes below.
- Every content title is a complete-sentence claim supported by that slide.
- Use one primary evidence object per slide; minimize prose.
- Put claim-changing caveats on screen, not only in notes.
- Code must wrap and fit inside its allocated region without horizontal or vertical scrollbars.
- Preserve visible vertical separation between adjacent panels, code blocks, evidence groups, and generation steps.

## Figures, tables, and media

Figures require `fig-alt`, a visible caption, axes/units, aggregation/uncertainty, samples/seeds, scope/status, and source/license. Combine color with marker/dash/hatch/direct labels. Prefer SVG for charts and raster for photos/dense sensor data; never use plot screenshots.

Rendered `Figure N` and `Table N` identifiers are bold while caption prose stays normal weight. Put `.algorithm-caption` directly beneath procedural code and inside the same column or container. Begin its source with `**Algorithm.**`; Sinew renders a globally numbered, bold `Algorithm N` identifier. State scope and evidence status, and caption procedural shell blocks too.

For Python plots, import SciencePlots and compose `science`, `no-latex`, `notebook`, and a color-safe cycle, followed by `styles/matplotlib/sinew-slides.mplstyle` and the matching `styles/matplotlib/sinew-<style>.mplstyle`. The SciencePlots `ieee` style is paper-column sized and is not a projected-slide style.

Tables are semantic, compact, captioned above, unit-labeled, and consistently precise. Structured result tables put `$\uparrow$`/`$\downarrow$` in metric headings, `Total` last behind a strong rule, bold the best value per metric, and place labeled `Ours:` rows last in a highlighted `.ours-last-N` block. Define these conventions in the caption and never add color-only meaning. Videos label real/sim, speed, task, controller/policy, and condition; ship locally, caption speech, add controls/poster fallback, and show failures when relevant.

## Accessibility

Do not rely on color alone. Use semantic headings, tables, and figures; short and detailed text equivalents for complex graphics; documented contrast targets; no flashing or unpausable movement; reduced-motion support; captions/transcripts; and verbal descriptions in delivery. Test keyboard navigation, high contrast, common projector sizes, offline mode, scroll/PDF, and image-interior contrast.

## Style changes

Record a reference style's source, owner, license, date, and source slug. Extract semantic tokens rather than app controls. Define every Sinew token, robust offline font fallbacks, and a matching Matplotlib overlay. Add only one new `color-*` choice; do not mutate event rules. Add the style to `scripts/generate_gallery_plots.py` and `scripts/render-styles.sh`.

## Completion

Run:

```bash
python3 scripts/validate.py
quarto render --profile color-<style>
scripts/check-render.sh _site/index.html
```

For style/profile/core changes run `scripts/render-styles.sh`. Inspect visually, offline, and in the required PDF/video format. Report the selected visual profile, delivery context verified separately, evidence changes, artifact, checks, source freshness, unresolved risks, and git status.
