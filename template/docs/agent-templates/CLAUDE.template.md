# Claude instructions for this Sinew presentation

Rename this file to `CLAUDE.md` and follow `AGENTS.md` completely.

## Highest-risk rules

- Scientific truth outranks polish. Never fabricate results, uncertainty, settings, citations, licenses, or delivery rules.
- Keep citations backed by `references.bib`. Preserve the single global `#refs` source, generated per-style reference views, profile-aware hover/focus cards, local citation jumps, external DOI/URL links, and two-column scrollbar-free layout. Split overfull references rather than shrinking or scrolling them.
- Keep illustrative/preliminary content labeled and claim boundaries visible.
- Verify the exact event edition, track, presentation type, and artifact using current official sources. Event research files are dated background guidance, not profiles.
- Activate exactly one `color-*` profile. It owns visual style only; never place event logistics or invented branding in it.
- Slide source and visible text use only printable ASCII from a standard US keyboard. This is machine-checkable: permit ASCII 0x20-0x7E plus newline and tab, and reject all other characters.
- Use `$...$` or `$$...$$` with ASCII LaTeX commands for math, never pasted Unicode math glyphs.
- `deck.qmd` is the ordered manifest; one include equals one slide; `#` is horizontal and `##` is vertical; included files have no YAML.
- Never use level-3 or deeper headings inside slides. Pandoc can emit nested section tags that Reveal treats as stacks; use bold labels or semantic containers.
- Every content title is a supported full-sentence claim with one primary evidence object.
- Use `<ol class="research-questions">` for Q1-Q9 and `<ol class="research-hypotheses">` for H1-H9. Never type identifiers manually or exceed nine items in one list. Keep exactly two large group panels, one for questions and one for hypotheses. Keep statement rows unboxed; only Q/H labels are bounded. Use `.is-highlighted` on at most one primary item per list and map each item to evidence or an unresolved result.
- Use `{{< q N >}}` and `{{< h N >}}` for in-text statement references. Preserve established numbering and verify preview plus navigation to the same-stack or unique deck-wide target.
- Code must wrap and fit without horizontal or vertical scrollbars.
- Preserve visible vertical separation between adjacent panels, code blocks, evidence groups, and generation steps.
- Figures need alt text, caption, units, uncertainty/sample/seeds, non-color encodings, scope, and provenance.
- Rendered `Figure N` and `Table N` identifiers are bold. Put `.algorithm-caption` directly beneath procedural code and inside its column or container. Begin with `**Algorithm.**`; Sinew renders a globally numbered, bold `Algorithm N` identifier. Caption procedural shell blocks too. Keep algorithms in the profile's genuine monospace font and disable programming ligatures so literal ASCII stays visible.
- Use native `@fig-...`/`@tbl-...` references and stable `#algorithm-...` captions with `{{< alg algorithm-id >}}`; verify automatic labels and profile-aware preview/navigation for figure, table, algorithm, Q, and H links.
- Preserve and test the control-free fullscreen inspector on every figure, table, and captioned algorithm. Click evidence to open and click fullscreen evidence to close; Enter/Space opens and Escape closes. Verify focus return, active-profile inheritance, ultrawide scaling for every evidence type, scaled captions, and Reveal navigation suppression.
- Structured result tables are semantic and captioned above; use `$\uparrow$`/`$\downarrow$` in metric headings, put `Total` last behind a strong rule, bold the best per metric, and place labeled `Ours:` rows last in a highlighted `.ours-last-N` block. Define the conventions in the caption. Videos disclose domain, speed, and conditions and work offline.
- Apply accessibility to CSS, figures, media, artifacts, and live narration. Automated checks are insufficient.
- Do not add `.beads`, remote tracking, secrets, private data, or remote font dependencies.
- Preserve user changes; do not commit or push without permission.

## Workflow

Read the project docs, the selected color profile, and any relevant delivery-research file. Inspect every included slide and run the validator before editing. Use the built-in include manifest; do not add slide auto-discovery unless explicitly requested.

For plots, apply the common Sinew slide overlay and then the matching per-style Matplotlib overlay. Do not use publication-sized `ieee` directly. Keep plot source and data provenance.

For a new style, follow `docs/adding-a-style.md`; work on `style/<slug>`, advance the minor development version, add the complete index/citation/reference column, and use a reviewed pull request. Review the CI gallery artifact before merge.

Validate with:

```bash
python3 scripts/validate.py
quarto render --profile color-<style>
scripts/check-render.sh _site/index.html
```

After style/profile/core changes, run `scripts/render-styles.sh`, then run `quarto render --cache-refresh` and `scripts/check-render.sh _site/index.html gallery`. The plain render must include every registered style without edits or a profile argument. Visually inspect representative outputs offline. Handoff must state the selected visual profile, delivery context verified separately, evidence changes, artifact path, checks/results, source freshness, unresolved risks, and git status.
