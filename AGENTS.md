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

Keep any task tracker outside this repository; a parent-level or external planning workspace that references this repo satisfies the intent, Beads included. Do not initialize Beads or add `.beads` inside this template/project, and do not create ad hoc TODO files as a substitute for the user's tracker.

## Truthfulness and evidence

- Never invent experimental results, sample sizes, seeds, intervals, baselines, citations, artifact links, hardware settings, participant details, or conference rules.
- If a needed figure does not exist yet, use `.missing-evidence` instead of inventing, substituting, or approximating one, and instead of skipping the slide. Do not attach a superficially similar clip from a different run/checkpoint, and do not attach one artifact's citation to another's footage. Nest it inside the figure div, with the caption as the outer div's trailing paragraph:

  ```markdown
  ::: {#fig-lift-rollout}
  ::: {.missing-evidence}
  Rollout video of the certified lift policy. No clip of this policy exists on disk yet.
  :::

  Caption text, as for any figure.
  :::
  ```

  That gets it `Figure N`, a working `#fig-...` id, `@fig-...` cross-references, and the fullscreen inspector like any other figure. It renders a dashed danger-bordered box with a diagonal hatch and a real DOM-text "MISSING EVIDENCE" label (deliberately DOM text, not CSS `::before`, so assistive technology exposes it), and stays unmistakable in grayscale. `validate.py` reports every placeholder still present; that report is an open-work list, not noise to clear by deleting the slide.
- Under-scoping a real number is as dangerous as fabricating one: distrust a bare number, checkpoint name, or filename and re-derive its exact population and conditions before citing it. A metric's scope must never be narrower than the claim it sits under (examples: two checkpoints sharing a step number but not a run; a run cited as strongest that actually ran the loosest gate; a lift figure missing the caveat that narrows what it appears to cover; a headline tolerance figure that was the only tolerance at which the behavior worked; a rollout video whose filename/caption oversells what it shows). Open each evidence-bearing slide source with an HTML comment naming the exact run id(s) and source script(s), plus a "DO NOT confuse with X" line for anything plausibly conflated with it.
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
- Give a fenced div opener (`::: {...}`) a blank line above it whenever the preceding line is list content (`- item`); otherwise Pandoc absorbs the fence into the list item as literal text with no render error pointing at the file or line. A fenced div needs at least 3 colons; `::` is not a valid fence marker and renders as literal text instead of a div.
- Quarto's fenced-div warning ("This usually indicates a problem with a fenced div in the document") never names a file or line. Treat it as a signal to re-check every include touched in the change, not a location. Require zero `^[WARNING]` lines in `quarto render` output before treating a render as clean, and grep rendered HTML for `<p>:+` to catch a fence left as literal text.

Core narrative belongs at the first vertical index in each stack. Optional detail may go lower. Announce vertical navigation during live delivery and provide a linear/scroll/PDF artifact for sharing.

## Slide writing

- Use only printable ASCII characters available on a standard US keyboard in slide SOURCE. This is machine-checkable: permit ASCII 0x20-0x7E plus newline and tab, and reject all other characters. `validate.py` enforces this on source files.
- RENDERED visible text is held to a different, narrower rule, because the toolchain legitimately introduces non-ASCII that no author typed: Pandoc smart typography turns an authored `--` into an en dash and straight quotes into curly ones, and Quarto's cross-reference machinery emits non-breaking spaces (`Figure 1`). Those are permitted. What is never permitted in rendered visible text is decorative Unicode: arrows, math glyphs, emoji, box-drawing, and symbol characters. Replace those with words or ASCII equivalents at the source. Do not try to reach pure ASCII in the rendered output -- removing the non-breaking spaces would break cross-reference spacing, and disabling smart typography degrades every deck built from this template to buy nothing that projection safety needs. En dashes and curly quotes exist in every standard font; a decorative arrow or math glyph is what actually fails on an unknown projector.
- Do not paste Unicode arrows, multiplication signs, bullets, daggers, smart quotes, dashes, or Unicode math symbols.
- Write mathematics with Quarto/Pandoc dollar delimiters: `$...$` inline and `$$...$$` for display math. Use ASCII LaTeX commands inside the delimiters.
- `#` divider title: short subtopic.
- `##` content title: complete-sentence claim supported by the slide.
- One primary idea/evidence object per slide.
- Minimize prose; the speaker carries explanation.
- Avoid topic labels such as "Results," "Method," and "Ablation" as content titles.
- Avoid marketing language, hero metrics, all caps, underline, italics-for-emphasis, and color-only emphasis.
- Present research questions only as `<ol class="research-questions">` and hypotheses only as `<ol class="research-hypotheses">` inside their semantic research blocks. Sinew generates Q1-Q9 and H1-H9; never type identifiers into item text, never exceed nine items in one list, and split longer sets across slides. Keep exactly two large group panels, one for all questions and one for all hypotheses. Keep individual statement rows unboxed; only Q/H labels are bounded. Use `.is-highlighted` on at most one primary item per list and map every item to evidence or an explicitly unresolved result.
- Reference those statements only with `{{< q N >}}` and `{{< h N >}}`. Keep one canonical list pair per logical deck when possible; same-stack targets take priority and an out-of-stack reference must have exactly one deck-wide match. Never hand-build Q/H links or silently renumber identifiers already used in prose, notes, or discussion.
- Use `.kicker` for the role, `.figcap` for visible evidence detail, `.source` for provenance, `.panel`/`.evidence-card` for bounded content, and `ol.takeaways` for the close.
- Use `.hot` only for a rare warning/error, never as the sole data encoding.
- Keep caveats on the projected slide when they materially bound the claim; do not bury them only in notes. `.notes` is the default home for pacing/caveats, but on explicit user request you may remove notes from slide sources entirely and archive them to an external timestamped doc instead, preserving the caveats, provenance, and do-not-say warnings they carried. Wherever notes live, the rule above does not move: a claim-changing limitation still belongs on the projected slide.
- A slide that overflows its frame is a defect, not a style preference. `quarto render` succeeding and the HTML validating do not mean content fit; text pushed below the fold produces no error, so screenshot/visually inspect every slide, not spot checks. Default budgets, not hard limits (state and justify a deliberate exception): 3 bullets per list, 10 words per bullet, 60 body words per slide, 5 table rows, 1-line captions, 2 nesting levels. `template/scripts/check_overflow.py` measures this in headless Chrome and is a required gate; it divides out Reveal's fit-to-window transform, so it is viewport-invariant. Exit 2 means it did not run, which is not a pass. It catches content escaping the frame, not content that merely crowds, so still inspect visually.
- Attributes written on a `#`/`##` heading (`# Title {.foo}`) land on the enclosing `<section>`, not the heading element: `h1.foo` matches nothing, `.foo h1` works.
- Quarto's crossref pass wraps every numbered `#fig-` object -- image, video, GIF, `.missing-evidence` alike -- in an outer `div.quarto-float` BEFORE the real `<figure>`. So a layout container's `> figure` child selector matches nothing at all, and the grid/flex child you actually need to style is that wrapper. A pre-existing `.card-strip-N > figure { align-self: stretch }` was silently unreachable for exactly this reason, leaving each figure at its own content height and its caption up to 192px out of line with its neighbours. Reaching a figure's own children from a strip means passing the layout down through the wrapper (subgrid works; `display: contents` on the `<figure>` does not, because that figure carries `tabindex`, `role="button"`, and the fullscreen-inspector wiring, and removing its box removes its interactive semantics in several browsers).
- A `:not(:has(...))` argument carrying an attribute selector outranks a bare class selector on specificity, regardless of source order. This bit a real rule: `figure:not(:has(img[style^="width"], video[style^="width"])) { width: fit-content }` exists to shrink an image figure to its image, but it silently matched every figure with no `<img>`/`<video>` at all and beat a later, more specific-looking `figure:has(...) { width: 100% }` rule meant for exactly those figures, rendering them at 75-84% of their column. When two rules disagree, confirm which actually wins with CDP `CSS.getMatchedStylesForNode`; do not assume source order decides. Related: a container with `width: 100%` and horizontal padding needs `box-sizing: border-box`, or its border box is exactly the padding wider than its parent and bleeds out the anchored edge -- a fixed, content-independent overrun that looks like a mysterious constant.
- `.metric strong { display: block }` puts any bold text inside a `.metric` span on its own line. Keep the metric value in plain text; do not pair `**bold value**, trailing text` inside `.metric`, or the comma and trailing text end up orphaned on the next line.
- Put figure detail in `fig-alt`, not inside the `![...]` brackets. `.reveal figcaption` and `.reveal .figcap` share the same visible caption styling, so a long bracket caption plus a separate `.figcap` produces two visually stacked captions. Use a short bracket caption or `.figcap`, never both on the same figure.
- An empty citation key `[@]` is not recognized as a citation and renders as literal visible bracket text on the slide, with no warning. Treat any bare `[@]` in a diff as a defect to fix, not a rendering artifact to ignore.
- Put each `.algorithm-caption` directly beneath its procedural code and inside the same column or container. Start the source with `**Algorithm.**`; Sinew converts it to a globally numbered, bold `Algorithm N` identifier at render time. State inputs/outputs or scope and evidence status/provenance. Caption procedural shell blocks the same way. Keep algorithm bodies and captions in the profile's genuine monospace `--sinew-algorithm-font`; never let them inherit proportional display type or programming ligatures that replace literal ASCII sequences.
- Give every referenced algorithm caption a stable `#algorithm-...` ID and cite it with `{{< alg algorithm-id >}}`. Reference figures and tables with native `@fig-...` and `@tbl-...`; never hard-code rendered object numbers.
- Put long derivations, full tables, and secondary ablations in vertical backup slides.
- Code must wrap and fit inside its allocated region without horizontal or vertical scrollbars.
- Preserve visible vertical separation between adjacent panels, code blocks, evidence groups, and generation steps.

## Layout

Full primitive markup and worked examples live in `template/docs/authoring.md`, "## Layout"; this section states the rule, not a second copy of that documentation.

- Reach for a named layout primitive, never hand-rolled inline styles or a per-slide CSS file. Two real decks failed this way and it was the single largest source of avoidable rework in the evidence: one wrapped every two-column slide in nested `{width="42%"}`/inline-`style` divs just to right-align and cap media; the other gave 21 of its own content slides individual CSS files, roughly 2500 lines and about 55 distinct hand-written `grid-template-columns` declarations, reinventing the same two-column-plus-connector-lane shape 21 times.
- The dominant shape is two columns, text left / media right (12 of 28 content slides on one measured deck, 16 of 34 on another): use `.split-layout`. Swap sides with `.split-layout-reverse`, not raw column reordering -- it swaps DOM order and the fr ratio so reading order stays reading order. Other named primitives: `.split-layout-connector` (text | `.connector-lane` | media), `.split-layout-footer` (two-column row plus one full-width row, exactly three direct children), `.card-strip-3`/`.card-strip-5`/`.card-strip-12`, `.full-bleed-figure`, `.full-bleed-title` (the 22ch title-width escape hatch), `.top-aligned` (opt a dense reference/appendix slide out of default vertical centering), and `.diagram-flow`/`.diagram-step`/`.diagram-arrow` for a no-JS/no-SVG pipeline diagram.
- Column widths do not need hand-tuned percentages: use a round split (50/50, 60/40) and let the theme's gutter show the gap. Quarto ships `div.columns { display: initial }`, and `initial` for `display` resolves to the CSS-wide initial value `inline`, not the div's normal block default, so `align-items`/`gap` on a plain `.columns` block never had a box to apply to -- that is why old percentage-tuning advice never actually worked. Slides are vertically centered by default and `.column` uses `vertical-align: middle`; do not try `display: flex` on `.column` to fix this, it fights Quarto's inline-block sizing and has dropped media below text on a real deck.

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

Figures and video commonly have non-standard resolutions and aspect ratios: always render at native resolution, never trim or crop to fit a slot, and never leave empty letterbox/pillarbox borders. No `object-fit: cover` (it crops). No fixed-ratio padded box (it letterboxes). No hand-tuned per-slide `max-height` in px/em -- one real deck ended up with four different ad hoc values (215px, 255px, 300px, 340px) across slides; the theme sizes figures automatically (`template/docs/authoring.md`, "Figures, sizing, and captions"). If a figure looks too small or too large, that means the slide has too much competing content, not that the figure needs a manual size.

Artwork with a white background that clashes with the deck surface has two fixes, not one: `{.plate}` on the image adds a light backing plate whose color derives from the active profile's own palette, and is the required treatment for vivid/saturated artwork or any source whose pixels must not be altered; `template/scripts/make_transparent.py` strips the white instead, for neutral line art you own the source of. `template/docs/figures-and-tables.md` documents which one to pick -- do not restate that choice here, use it.

Once artwork is transparent -- whether it started that way or was stripped by `make_transparent.py` above -- give it `.plate` by default. Transparent artwork has no background of its own, so it inherits whatever slide surface it lands on, and that failure is profile-dependent: measured on this repository's own demo asset, the same ink comes out at roughly 1.1-1.2:1 contrast against `origami` and `blueprint` but 19.7:1 against `movement`. An author who checks a deck against one profile and later switches gets no warning that transparent art has gone illegible. `.plate` also leaves the source pixels untouched, which independently matters for adapted third-party figures under provenance or license constraints. Skip `.plate` only as a deliberate, checked opt-out: the artwork is meant to sit directly on the slide surface, and it has been verified against the profile actually in use, not just the one being rendered in the moment.

Every rendered figure, table, and captioned algorithm must retain the Sinew fullscreen inspector without visible `Expand` or fullscreen `Close` buttons. Click evidence to open it and click the fullscreen evidence to close it; Enter/Space opens from keyboard focus and Escape closes. Test focus return, active-profile inheritance, viewport scaling for every evidence type, caption scaling, and suppression of Reveal navigation while open. Fullscreen inspection never excuses overflow on the original slide.

Every in-text figure, table, algorithm, Q, and H reference must retain its profile-aware hover/focus preview and direct hyperlink to the original target. Cloned math must be typeset, and table previews must be wide enough for legible columns. Test pointer, keyboard focus, activation, same-column routing, automatic labels, and unresolved-target handling. Q/H links remain bare labels without permanent boxes.

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
- To show an excerpt of a video, set `data-sinew-start` and `data-sinew-end` (seconds, both optional and independent) and let it loop between them; the trim window is implemented with a `timeupdate` handler, not a `#t=` media fragment, because end-point support for fragments is inconsistent across browsers. Do not re-encode or cut the source file; the source stays whole on disk and the deck shows only the window. A zoomed/fullscreen clip keeps the same trim window and resumes at the position the fullscreen view left off.
- Every `<video>` in a slide gets managed playback automatically, no class needed: playback is driven by Reveal's `slidechanged`/`ready` events, playing on slide enter and pausing/resetting on leave. This deliberately replaces native `autoplay`, which fires on page load rather than when the audience reaches the slide; opt a specific video out with `data-sinew-autoplay="false"`. Muted is the default -- sound-on is simply omitting `muted` -- and browsers block unmuted autoplay outside a click gesture, so an unmuted video stays paused with visible controls rather than silently failing; do not treat that as a bug to work around.

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
- Treat affiliation marks as protected assets: add them only with explicit authorization, record provenance/reuse constraints, preserve transparency, aspect ratio, and alt text, and verify that the compact lockup appears on every slide in every selected profile. Keep the marks unbacked on light profiles; on dark profiles, use a light backing color derived from that profile's own palette rather than generic white.
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
python3 template/scripts/check_overflow.py template/_site/index.html
```

After profile/theme/core changes:

```bash
template/scripts/render-styles.sh
quarto render template --cache-refresh
template/scripts/check-render.sh template/_site/index.html gallery
python3 template/scripts/check_overflow.py template/_site/index.html
```

The plain gallery render must contain one horizontal column for every `_quarto-color-*.yml` profile without editing source or supplying a profile argument.

Then manually inspect:

- title + one content slide in each color profile;
- both 1600x900 and 1920x1080 layouts;
- gallery (`navigation-mode: grid`): vertical/horizontal navigation, including the deliberate row-preserving left/right jump between style columns; a forward Space walk does NOT visit every slide here by design -- see `docs/architecture.md`, "Slide numbering";
- delivery (`color-*` profile, `navigation-mode: default`): vertical/horizontal navigation and full linear Space traversal across every slide in document order;
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
