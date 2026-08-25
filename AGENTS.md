# Sinew agent instructions

These rules apply to every automated agent creating, revising, reviewing, or rendering an academic presentation with this repository.

## Mission

Produce an evidence-led academic talk whose claims, figures, tables, citations, delivery logistics, and rendered artifacts are auditable. Prefer scientific clarity over visual novelty. A successful deck is legible in the room, honest about scope/uncertainty, usable offline, and reproducible by the next agent.

This repository is not an official event template.

## Instruction precedence

1. System/developer/user instructions.
2. Applicable repository instructions.
3. Current official event presenter requirements.
4. This file and Sinew documentation.
5. House defaults.

When sources conflict, do not silently choose. Record the conflict and ask when it changes the artifact materially.

## First actions

Before editing:

1. Read `README.md`, `template/docs/research-notes.md`, `template/docs/authoring.md`, and `template/docs/figures-and-tables.md`. Read the relevant `template/docs/conferences/<event>.md` only when preparing for that delivery context.
2. Inspect `template/_quarto.yml`, exactly one selected `template/_quarto-color-<style>.yml`, and `template/_extensions/sinew/_extension.yml`.
3. Inspect `template/deck.qmd` and every included file in order.
4. Check `git status`; preserve unrelated user changes.
5. Run `quarto --version`; require the version in the extension manifest.
6. Run `python3 template/scripts/validate.py` before and after meaningful changes.

Do not initialize Beads or add `.beads` anywhere inside this template/project. If durable task tracking is requested, keep it outside the repository. Do not create ad hoc TODO files as a substitute for the user's tracker.

## Truthfulness and evidence

- Never invent experimental results, sample sizes, seeds, intervals, baselines, citations, artifact links, hardware settings, participant details, or conference rules.
- Never infer a missing value from a plot unless the user explicitly requests digitization and the result is labeled approximate.
- Never transform "we plan," "we hypothesize," or "preliminary" into an established claim.
- Keep negative results and failure cases when they bound the conclusion.
- Label simulation versus real robot, offline versus online, benchmark versus deployment, and retrospective versus prospective evidence.
- Label illustrative/template values as illustrative. Do not remove that label until real evidence and provenance are supplied.
- If evidence is missing, narrow the title, mark the slide preliminary/missing, or stop and request the source. A polished false claim is a failed task.
- Verify references against primary papers/official sources. Do not cite a search-result snippet as the source.
- A citation is not permission to reuse a copyrighted visual. Record license/permission or redraw within allowed use.
- Use Pandoc citation keys backed by `template/references.bib`; never hand-format a second bibliography. Preserve `link-citations`, `citations-hover`, the single global `#refs` citeproc source, and each generated `.style-references` view. Verify that hover/focus cards inherit the active profile, citation activation stays in the current style column, external DOI/URL links work, and every references view remains two-column and scrollbar-free. Split overfull references instead of shrinking or scrolling them.

## Venue and event delivery research

Event rules are volatile data, not visual styles or render profiles.

- Select exactly one `color-*` profile for the deck.
- Confirm the exact event edition, track, presentation type, and required artifact.
- Open the official current presenter/author page before final delivery.
- Treat `template/docs/conferences/` as dated background guidance only; it never configures Quarto.
- Do not carry timing/upload rules from a prior year unless explicitly targeting that year.
- Do not invent event fonts, colors, logos, or slide templates.
- Do not bundle or place event logos without current official assets, permission, and usage rules.
- Verify fixed-timing video duration, dimensions, codec, audio, naming, and deterministic timing outside the style system.
- Apply current accessibility expectations, including non-color encodings and visual descriptions.

When current official instructions differ from the research notes, update the notes and delivery checklist. Do not add event metadata to a color profile.

## Multi-file 2D structure

`template/deck.qmd` is the ordered manifest in this repository. A scaffolded presentation places the same file at its project root.

- A subtopic folder maps to one horizontal stack.
- `_00-section.qmd` starts with one `#` heading and `.section-slide`.
- Every content file starts with exactly one `##` heading.
- Do not use level-3 or deeper headings inside slides. Pandoc can emit nested section tags and Reveal can treat them as additional stacks. Use bold inline labels, `.kicker`, `.eyebrow`, or semantic containers instead.
- One file represents one slide; do not hide multiple `##` headings in one included file.
- Included files contain no YAML.
- Include shortcodes stand alone with blank lines around them.
- Asset paths in included files resolve from `deck.qmd`; use project-root-relative paths.
- Do not place comments/prose between the document YAML and first include; that creates a blank slide.
- Update `deck.qmd` whenever adding, moving, renaming, or deleting a slide.
- Do not auto-discover/glob slide files: explicit order is a reviewable part of the talk.

Core narrative belongs at the first vertical index in each stack. Optional detail may go lower. Announce vertical navigation during live delivery and provide a linear/scroll/PDF artifact for sharing.

## Slide writing

- Use only printable ASCII characters available on a standard US keyboard in slide source and visible slide text. This is machine-checkable: permit ASCII 0x20-0x7E plus newline and tab, and reject all other characters.
- Do not paste Unicode arrows, multiplication signs, bullets, daggers, smart quotes, dashes, or Unicode math symbols.
- Write mathematics with Quarto/Pandoc dollar delimiters: `$...$` inline and `$$...$$` for display math. Use ASCII LaTeX commands inside the delimiters.
- `#` divider title: short subtopic.
- `##` content title: complete-sentence claim supported by the slide.
- One primary idea/evidence object per slide.
- Minimize prose; the speaker carries explanation.
- Avoid topic labels such as "Results," "Method," and "Ablation" as content titles.
- Avoid marketing language, hero metrics, all caps, underline, italics-for-emphasis, and color-only emphasis.
- Use `.kicker` for the role, `.figcap` for visible evidence detail, `.source` for provenance, `.panel`/`.evidence-card` for bounded content, and `ol.takeaways` for the close.
- Use `.hot` only for a rare warning/error, never as the sole data encoding.
- Keep caveats on the projected slide when they materially bound the claim; do not bury them only in notes.
- Put each `.algorithm-caption` directly beneath its procedural code and inside the same column or container. Start the source with `**Algorithm.**`; Sinew converts it to a globally numbered, bold `Algorithm N` identifier at render time. State inputs/outputs or scope and evidence status/provenance. Caption procedural shell blocks the same way.
- Put long derivations, full tables, and secondary ablations in vertical backup slides.
- Code must wrap and fit inside its allocated region without horizontal or vertical scrollbars.
- Preserve visible vertical separation between adjacent panels, code blocks, evidence groups, and generation steps.

## Figures

Every informative figure must have:

- a stable `#fig-...` label when referenced/numbered;
- nonempty `fig-alt` describing the meaningful finding;
- a visible caption with scope, metric, aggregation/uncertainty, sample/seeds, and status/source;
- readable axes, units, legend/direct labels, and abbreviations;
- color plus marker/dash/hatch/shape/text when series carry meaning;
- an honest baseline/scale and disclosed axis truncation;
- sufficient text, line, and object contrast on the plot surface;
- source/license/permission for reused/adapted visuals.

The rendered `Figure N` identifier is bold; keep the descriptive caption text at normal weight.

Prefer SVG for diagrams/line plots and raster formats for photos/dense images. Do not paste plots as screenshots. Keep the source script and data provenance. If a chart is complex, provide a detailed prose/table equivalent in the deck or handout.

Use SciencePlots as a layer, not a guarantee. Apply the selected style's Matplotlib overlay last:

```python
import scienceplots
import matplotlib.pyplot as plt

plt.style.use([
    "science", "no-latex", "notebook", "bright",
    "template/styles/matplotlib/sinew-slides.mplstyle",
    "template/styles/matplotlib/sinew-origami.mplstyle",
])
```

Replace `sinew-origami.mplstyle` with the overlay matching the one selected `color-*` profile. Do not use the SciencePlots `ieee` paper-column style directly for projected slides. Test CJK glyphs with maintained Noto/Source Han fonts. Export at final dimensions and verify fonts.

## Tables

- Use semantic Markdown/HTML, never screenshots.
- Use a caption above the table.
- Include population/task, metric/scope, and provenance in the caption.
- Put units in headings.
- Keep one simple header row and a small number of rows/columns.
- Use consistent, justified precision and tabular numerals.
- Put metric preference in the heading with ASCII LaTeX source: `$\uparrow$` for higher-is-better and `$\downarrow$` for lower-is-better. Define the convention in the caption.
- Put `Total` in the final column and separate it with the strong vertical rule supplied by `.structured-results`.
- Bold the best value in each metric column and state that convention in the caption. Do not add color-only best/worst encoding.
- Put the last N proposed-method rows in one contiguous block, label each method with `Ours:`, and highlight the block with `.ours-last-N`. The supported classes are `.ours-last-1` through `.ours-last-4`.
- Prefer plots for trends and tables for exact lookup.
- Move dense/full benchmark tables to backup/handout.

The rendered `Table N` identifier is bold; keep the descriptive caption text at normal weight.

## Robotics media

- State real/simulation, playback speed, task, policy/controller, and evaluation condition.
- Show representative failure cases when they qualify the claim.
- Keep media local; do not depend on Wi-Fi or streaming.
- Caption speech and provide a transcript for released recordings.
- Add controls/poster fallback unless a venue explicitly requires fixed autoplay.
- Explain meaningful experimental audio; otherwise the evidence must work muted.
- Test codec, seeking, loop, fullscreen, and offline playback in the target browser.
- If embedded MP4 fails as a data URI, set `embed-resources: false`, ship dependencies/assets, and serve over local HTTP.

## Accessibility

- Follow `template/docs/accessibility.md` and current venue-specific guidance.
- Do not rely on color alone.
- Keep normal text at least 4.5:1 and large text at least 3:1 when claiming WCAG AA; meaningful graphics generally need 3:1 non-text contrast.
- Use semantic headings/tables/lists/figures.
- Add short and detailed alternatives for complex visuals.
- Avoid flashing and unpausable motion.
- Respect reduced motion; test `color-high-contrast`.
- Verbally communicate important visual information and repeat audience questions.
- Test keyboard navigation, speaker view, fullscreen, print/scroll view, and released captions.

Automated accessibility checks do not validate statistical honesty, chart semantics, narration, projection conditions, or image-interior contrast.

## Style work

When adding an uploaded/reference style:

0. Follow `template/docs/adding-a-style.md` completely. Create `style/<slug>` from current `main`, advance the minor development version, open a pull request, review its CI gallery artifact, and merge only after approval and passing checks. Never add a style directly to `main`.

1. Record source path/URL, owner/license, and inspection date.
2. Extract semantic tokens; do not copy app-specific controls/navigation.
3. Map every Sinew token in `template/styles/colors/<name>.css`.
4. Provide explicit sans/mono fallback stacks and offline behavior.
5. Increase density/contrast/type for projection as needed and document changes.
6. Add only a `color-*` profile. Do not edit conference constraints.
7. Provide or document a matching Matplotlib palette.
8. Add the matching Matplotlib overlay and generator entry.
9. Add the complete index column, per-style bibliography record, citation slide, and local references slide.
10. Run `template/scripts/render-styles.sh`; inspect representative screenshots, citation hover cards, and grayscale.

The Origami source mapping is documented in `template/docs/styles.md` and `template/styles/colors/origami.css`. Preserve its academic adaptation unless the user asks to revise it.

## File/edit hygiene

- Use `rg`/`rg --files` for discovery.
- Preserve unrelated changes and existing assets.
- Do not edit generated `template/_site/`, `template/_build/`, `template/.quarto/`, or `*_files/` as source.
- Do not add secrets, private datasets, participant data, or machine-specific absolute paths to public artifacts/docs. The Origami local path is provenance documentation; replace it with a public source when publishing if needed.
- Do not add remote analytics, tracking, or third-party scripts.
- Do not add network font imports without explicit approval and offline fallback.
- Do not commit generated presentations unless the user asks for distributable artifacts.
- Do not commit or push without explicit authority.

## Validation and rendering

Minimum after source changes:

```bash
python3 template/scripts/validate.py
python3 template/scripts/check_contrast.py
quarto render template --profile color-origami
template/scripts/check-render.sh template/_site/index.html
```

After profile/theme/core changes:

```bash
template/scripts/render-styles.sh
```

Then manually inspect:

- title + one content slide in each color profile;
- both 1600x900 and 1920x1080 layouts;
- vertical/horizontal navigation and linear Space traversal;
- overflow, captions, table placement, citations, notes, and footer;
- offline behavior;
- required PDF/video artifact and font/media integrity;
- talk duration rehearsed aloud.

Do not report completion while validation fails. If a tool is unavailable, state which gate was not run and why.

## Handoff

Report:

- selected visual profile and separately verified delivery context;
- claims/evidence changed and any unresolved truth/provenance issue;
- files changed;
- exact validation/render commands and outcomes;
- generated artifact path;
- official delivery instructions' verification date and remaining delivery/export work;
- git status and whether anything was committed/pushed.
