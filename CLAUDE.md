# Claude instructions for Sinew decks

Follow `AGENTS.md` completely. This file restates the highest-risk requirements for Claude-family agents and adds a concrete workflow; it does not weaken `AGENTS.md`.

## Objective

Create auditable academic robotics/ML presentations. Scientific truth, readable evidence, accessibility, delivery compliance, and reproducible rendering outrank decorative polish.

## Required startup

Read, in order:

1. `AGENTS.md`
2. `README.md`
3. `template/docs/research-notes.md`
4. relevant `template/docs/conferences/<event>.md` when preparing for that delivery context
5. `template/docs/authoring.md`
6. `template/docs/figures-and-tables.md`
7. `template/docs/accessibility.md`
8. `template/deck.qmd`, exactly one selected `template/_quarto-color-*.yml` file, and included slides

Run `git status`, `quarto --version`, and `python3 template/scripts/validate.py` before substantial edits. Preserve user changes. Keep the planning workspace outside this repository -- a parent-level or external tracker, including Beads, is fine. Never create `.beads` inside this repo.

## Non-negotiable evidence rules

- Do not fabricate or "fill in" results, uncertainty, seeds, sample sizes, settings, citations, licenses, or conference rules.
- If a needed figure does not exist yet, use `.missing-evidence` -- never invent, substitute, or approximate one, and never skip the slide instead. Nest it inside the `#fig-...` div, with the caption as that div's trailing paragraph:
  ```markdown
  ::: {#fig-lift-rollout}
  ::: {.missing-evidence}
  Rollout video of the certified lift policy. No clip of this policy exists on disk yet.
  :::

  Caption text, as for any figure.
  :::
  ```
  It renders a dashed danger-bordered box with a real DOM-text "MISSING EVIDENCE" label (not CSS `::before`, so assistive tech exposes it) and is numbered like a real figure (`Figure N`, `#fig-...`, cross-referenceable) so nothing renumbers when the real asset lands; `validate.py` reports every placeholder present.
- Distrust a bare number, checkpoint name, or filename; re-derive its exact population and conditions before citing it. Under-scoping a real number (conflated checkpoints, the loosest-gated run cited as strongest, a dropped tolerance/rotation caveat, a video whose filename oversells its content) is as dangerous as fabricating one, and a metric's scope must never be narrower than the claim it sits under. Open evidence-bearing slide sources with an HTML comment naming the exact run id(s)/script(s) and a "DO NOT confuse with X" line.
- Do not upgrade preliminary/hypothetical results into findings.
- Do not hide a claim-changing limitation only in speaker notes. `.notes` is the default home for caveats, but on explicit user request they may be archived to an external timestamped doc instead; wherever notes live, a claim-changing limitation still belongs on the projected slide.
- Label every template/illustrative number until replaced by traceable evidence.
- Verify citations using primary papers or official sources. A URL/title that merely looks plausible is not enough.
- Keep citations backed by `template/references.bib`. Preserve the single global `#refs` source, generated per-style reference views, profile-aware hover/focus cards, local citation jumps, external DOI/URL links, and two-column scrollbar-free layout. Split overfull references rather than shrinking or scrolling them.
- Distinguish real robot from simulation and success from cherry-picked demonstration.
- Include representative failures when the conclusion depends on robustness.

If supplied evidence cannot support the requested headline, propose a narrower truthful headline and explain the gap.

## Visual-style selection and delivery research

Activate exactly one visual profile:

```bash
quarto render template --profile color-origami
```

Venue and event documents are dated background guidance, not profiles or visual identities. Before delivery, open the current official presenter instructions for the exact edition, track, presentation type, and artifact. Do not reuse older-edition rules or put logistics in a color profile.

Color profiles own palette, fonts, surfaces, syntax highlighting, and chart tokens only. Preserve provenance and projection/accessibility changes in `template/docs/styles.md`.

## Slide/file contract

- Slide source and visible text use only printable ASCII characters from a standard US keyboard. This is machine-checkable: permit ASCII 0x20-0x7E plus newline and tab, and reject every other character. Replace decorative Unicode symbols with words or ASCII equivalents.
- Write math with `$...$` or `$$...$$` and ASCII LaTeX commands; do not paste Unicode math glyphs.
- `template/deck.qmd` is the explicit order in this repository.
- One included file equals one slide.
- `#` divider files form horizontal stacks; `##` files form vertical slides.
- Never use level-3 or deeper headings in a slide. Pandoc can emit nested section tags that Reveal treats as stacks; use bold inline labels, `.kicker`, `.eyebrow`, or semantic containers.
- Included files have no YAML.
- Asset paths resolve from `deck.qmd`.
- No body content before the first include; it creates a blank slide.
- Required narrative stays at the first vertical index; detail/backups go below.
- Every content title is a supported full-sentence claim.
- Use the required semantic research lists: `<ol class="research-questions">` for Q1-Q9 and `<ol class="research-hypotheses">` for H1-H9. Never type Q/H identifiers manually or exceed nine items per list. Keep exactly two large group panels, one for questions and one for hypotheses. Keep statement rows unboxed; only Q/H labels are bounded. Use `.is-highlighted` on at most one primary item in each list and connect every item to evidence or an unresolved result.
- Use `{{< q N >}}` and `{{< h N >}}` for every in-text statement reference. Keep one canonical list pair where possible, preserve established numbering, and verify hover/focus preview plus navigation to the correct local or unique deck-wide target.
- Code must wrap and fit without horizontal or vertical scrollbars.
- Preserve visible vertical separation between adjacent panels, code blocks, evidence groups, and generation steps.
- Give a fenced div opener a blank line above it when the preceding line is list content, or Pandoc absorbs it into the list item as literal text with no file/line pointer. A fence needs at least 3 colons; `::` renders as literal text. Quarto's fenced-div warning names no file or line -- require zero `^[WARNING]` lines in `quarto render` output and grep rendered HTML for `<p>:+` to catch a fence left as literal text.
- A slide that overflows its frame is a defect, not a style preference; render success and valid HTML do not mean content fit. Default budgets, not hard limits: 3 bullets per list, 10 words per bullet, 60 body words per slide, 5 table rows, 1-line captions, 2 nesting levels. No automated overflow gate exists yet -- visually inspect every slide.
- Heading attributes (`# Title {.foo}`) land on the enclosing `<section>`, not the heading: `h1.foo` matches nothing, `.foo h1` works. `.metric strong { display: block }` puts bold text on its own line, so a `**bold**, trailing text` pattern inside `.metric` orphans the comma; keep metric values plain text. Put figure detail in `fig-alt`, not the `![...]` brackets -- a long bracket caption plus a separate `.figcap` produces two stacked captions since both share the same caption styling. An empty `[@]` citation key renders as literal visible bracket text with no warning; treat it as a defect.
- Reach for a named layout primitive (`.split-layout`, `.split-layout-reverse`, `.split-layout-connector`, `.split-layout-footer`, `.card-strip-3`/`-5`/`-12`, `.full-bleed-figure`, `.full-bleed-title`, `.top-aligned`, `.diagram-flow`/`.diagram-step`/`.diagram-arrow`; full detail in `template/docs/authoring.md`, "## Layout") -- never hand-rolled inline styles or a per-slide CSS file; two real decks each burned an avoidable rework pass reinventing the same shapes that way. `.split-layout` (text left, media right) is the dominant shape; use `.split-layout-reverse` to swap sides rather than reordering columns by hand. Use a round column split (50/50, 60/40); Quarto's `div.columns { display: initial }` resolves to `inline`, so hand-tuned percentages and `align-items`/`gap` on plain `.columns` never had a box to apply to. Do not try `display: flex` on `.column` -- it fights Quarto's inline-block sizing and has dropped media below text on a real deck.

Do not introduce filesystem auto-discovery or a custom composition filter unless the user explicitly requests behavior the built-in include manifest cannot express.

## Visual evidence contract

Keep algorithm bodies and captions in the profile's genuine monospace `--sinew-algorithm-font`. Disable programming ligatures so literal ASCII sequences remain visible, and verify the selected face in both the standalone profile and gallery column.

Figures need alt text, visible caption, axes/units, statistics/uncertainty, `n`/seeds, scope/status, and source/license. Use color plus markers/dashes/labels. Rendered `Figure N` and `Table N` identifiers are bold while caption prose remains normal weight. Put `.algorithm-caption` directly beneath procedural code and inside the same column or container. Begin it with `**Algorithm.**`; Sinew renders a globally numbered, bold `Algorithm N` identifier. State scope and evidence status, and caption procedural shell blocks too. Tables are semantic, compact, and captioned above. Structured result tables put `$\uparrow$`/`$\downarrow$` in metric headings, `Total` last behind a strong rule, bold the best value per metric, and place the labeled `Ours:` rows last in a highlighted `.ours-last-N` block. Define every convention in the caption. Preserve and test the control-free fullscreen inspector on every figure, table, and captioned algorithm: click to open and close, Enter/Space opens from focus, and Escape closes. Test focus return, active-profile styling, ultrawide scaling for every evidence type, and responsive captions. Cross-reference previews must typeset cloned math and give tables enough width for legible columns. Videos disclose domain/speed/conditions, include failures when relevant, and work offline.

Figures and video commonly have non-standard resolutions: always render at native resolution/aspect ratio, never crop/trim to fit a slot, and never leave letterbox/pillarbox borders. No `object-fit: cover`, no fixed-ratio padded box, no hand-tuned per-slide `max-height` (a real deck ended up with four different ad hoc px values across slides before the theme started sizing figures automatically -- see `template/docs/authoring.md`, "Figures, sizing, and captions"). To show a video excerpt, set `data-sinew-start`/`data-sinew-end` (seconds) and let it loop between them (implemented via `timeupdate`, not a `#t=` media fragment, since fragment end-point support is inconsistent across browsers); do not re-encode or cut the source file. Every slide video gets managed playback automatically -- play on Reveal slide-enter, pause/reset on leave, replacing native `autoplay` which fires on page load instead -- opt out per video with `data-sinew-autoplay="false"`. Muted is the default; an unmuted video stays paused with visible controls when the browser blocks unmuted autoplay, which is expected, not a bug.

White-background artwork that clashes with the deck surface: use `{.plate}` (a palette-derived backing plate) for vivid/saturated art or any source whose pixels must not be altered; use `template/scripts/make_transparent.py` for neutral line art you own the source of. `template/docs/figures-and-tables.md` documents the choice.

Use native `@fig-...` and `@tbl-...` cross-references. Give referenced algorithm captions stable `#algorithm-...` IDs and use `{{< alg algorithm-id >}}`. Verify automatic labels, profile-aware hover/focus previews, direct target navigation, and no hard-coded object numbers.

For Python plots, import SciencePlots and compose `science + no-latex + notebook + bright`, then `template/styles/matplotlib/sinew-slides.mplstyle`, then the matching `template/styles/matplotlib/sinew-<style>.mplstyle`. Do not use publication-sized `ieee` directly for projector slides. Keep plot-generation code/data provenance.

## Style changes

Follow `template/docs/adding-a-style.md` completely. Work on `style/<slug>` from current `main`, advance the minor development version, and use a reviewed pull request; never merge a style directly into `main`. Extract roles/tokens from a reference, not application selectors. A visual profile must define every Sinew token, robust offline font fallbacks, a matching Matplotlib overlay, a complete gallery column, and its own citation/reference entry. Document source/owner/license/date and changes made for projection/accessibility. Review the CI gallery artifact before merge.

Do not add conference logos or remote fonts without explicit authorization, official assets/usage rights, and offline tests.

## Accessibility

Do not rely on color alone; supply short/detailed alternatives for complex charts; use semantic structures; meet documented contrast targets when claiming conformance; avoid flashing/unpausable movement; caption speech; test reduced motion, keyboard, high-contrast, scroll/print, and live narration.

An automated axe/validator pass is necessary but insufficient.

## Completion gates

Run:

```bash
python3 template/scripts/validate.py
quarto render template --profile color-<style>
template/scripts/check-render.sh template/_site/index.html
```

For theme/profile/core changes run `template/scripts/render-styles.sh`, then run `quarto render template --cache-refresh` and `template/scripts/check-render.sh template/_site/index.html gallery`. The plain render must include every registered style without source edits or a profile argument. Inspect representative outputs visually and offline. Verify the event's final PDF/video/upload artifact separately.

At handoff, state the chosen visual profile, separately verified delivery context, changed claims/evidence, artifact path, exact checks/results, source freshness, unresolved risks, and git status. Do not commit or push without explicit authority.
