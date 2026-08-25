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

Run `git status`, `quarto --version`, and `python3 template/scripts/validate.py` before substantial edits. Preserve user changes. Never create `.beads` in this repository; use an external planning workspace if the user requests Beads.

## Non-negotiable evidence rules

- Do not fabricate or "fill in" results, uncertainty, seeds, sample sizes, settings, citations, licenses, or conference rules.
- Do not upgrade preliminary/hypothetical results into findings.
- Do not hide a claim-changing limitation only in speaker notes.
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
- Use the required semantic research lists: `<ol class="research-questions">` for Q1-Q9 and `<ol class="research-hypotheses">` for H1-H9. Never type Q/H identifiers manually or exceed nine items per list. Use `.is-highlighted` on at most one primary item in each list and connect every item to evidence or an unresolved result.
- Code must wrap and fit without horizontal or vertical scrollbars.
- Preserve visible vertical separation between adjacent panels, code blocks, evidence groups, and generation steps.

Do not introduce filesystem auto-discovery or a custom composition filter unless the user explicitly requests behavior the built-in include manifest cannot express.

## Visual evidence contract

Figures need alt text, visible caption, axes/units, statistics/uncertainty, `n`/seeds, scope/status, and source/license. Use color plus markers/dashes/labels. Rendered `Figure N` and `Table N` identifiers are bold while caption prose remains normal weight. Put `.algorithm-caption` directly beneath procedural code and inside the same column or container. Begin it with `**Algorithm.**`; Sinew renders a globally numbered, bold `Algorithm N` identifier. State scope and evidence status, and caption procedural shell blocks too. Tables are semantic, compact, and captioned above. Structured result tables put `$\uparrow$`/`$\downarrow$` in metric headings, `Total` last behind a strong rule, bold the best value per metric, and place the labeled `Ours:` rows last in a highlighted `.ours-last-N` block. Define every convention in the caption. Preserve and test the fullscreen inspector on every figure, table, and captioned algorithm with pointer, keyboard, Escape/Close, focus return, and active-profile styling. Videos disclose domain/speed/conditions, include failures when relevant, and work offline.

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
