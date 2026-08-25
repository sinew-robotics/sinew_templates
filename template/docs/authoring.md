# Authoring an academic deck

## Start from the paper's evidence, not its section headings

A talk is not a compressed paper. Build a claim map:

1. What should the audience believe or do differently at the end?
2. Which result is the strongest evidence for that change?
3. What problem and gap make that result matter?
4. What minimum method detail makes the evidence interpretable?
5. Which limitations bound the claim?

The required talk path should normally move horizontally through those questions. Vertical slides add evidence, ablations, derivations, qualitative cases, and backup detail within a subtopic.

## One file, one slide

Content slides start with exactly one level-2 heading:

```markdown
## Force feedback improves insertion under lateral disturbance

[Evaluation]{.kicker}

![...](assets/figures/disturbance.svg){
  #fig-disturbance
  fig-alt="Line plot ..."
}

::: {.figcap}
**Result.** Success over 384 trials; band is a 95% interval; three training seeds.
:::
```

Stack divider files start with exactly one level-1 heading:

```markdown
# Evaluation {.section-slide}

The evaluation isolates force information from data volume.
```

Included files have no YAML. Prefix files with `_` so project rendering ignores them as standalone inputs.

Do not use level-3 or deeper headings inside a slide. Pandoc can emit nested section tags for nested headings, and Reveal may interpret those tags as additional stacks. Use bold inline labels, `.kicker`, `.eyebrow`, definition lists, or semantic containers instead.

## Maintain the manifest

Add each file to `deck.qmd` in explicit order. Keep every include on its own line with a blank line before and after. Included-file asset paths resolve from `deck.qmd`; use `assets/...`, not paths relative to `_slides/<stack>/`.

Do not put prose, comments, or executable content between the closing YAML delimiter and the first include: Pandoc will turn pre-heading body content into an extra slide.

## Assertion-evidence slide anatomy

- **Title:** one full-sentence, falsifiable or bounded claim. Avoid topic labels such as "Results," "Architecture," or "Ablation."
- **Role label:** optional `.kicker` such as Motivation, Method, Evaluation, Limitation.
- **Evidence:** one primary figure, table, equation, short code excerpt, or qualitative panel.
- **Caption:** what is shown, population/task/condition, statistic and uncertainty, sample/seeds, and source.
- **Boundary:** simulation/real, preliminary/final, observed/causal, in-distribution/out-of-distribution.
- **Speaker notes:** interpretation, transitions, caveats, and likely questions - not facts the audience must see.

Keep visible vertical space between adjacent panels, code blocks, evidence groups, and generation steps. Proximity communicates grouping; accidental touching makes distinct ideas look like one component.

For table slides, keep one header row, include units in headings, align numeric columns, and provide a caption with scope, sample size, and evidence status. Use a unique `#tbl-...` label. For structured result tables, wrap the table in `.structured-results` plus `.ours-last-N`, put metric direction in headings with `$\uparrow$`/`$\downarrow$`, put `Total` last, bold the best per metric, and keep labeled `Ours:` rows last. The gallery demonstrates this after the plot slide in every style column.

Quarto-generated `Figure N` and `Table N` identifiers are bolded by the format; do not manually repeat them in caption prose. Put an `.algorithm-caption` directly beneath procedural code and inside the same column or container. Start it with `**Algorithm.**`; Sinew replaces that source label with a globally numbered, bold `Algorithm N` identifier. Then state inputs/outputs or scope and whether the procedure is illustrative, adapted, or traced to the research implementation. Treat a procedural shell block as an algorithm and caption it too.

The source project's quiet visual hierarchy, assertion headlines, one-evidence discipline, figure captions, and numbered takeaways are retained. Branding and app-specific UI are not.

## Research questions and hypotheses

Research questions and research hypotheses use required semantic list classes. Do not type `Q1`, `Q2`, `H1`, or `H2` into item text: Sinew generates Q1-Q9 and H1-H9 with CSS counters so identifiers remain consistent across every visual profile.

```markdown
:::: {.research-framing}
::: {.research-block .research-block-questions}
**Research questions**

<ol class="research-questions">
<li class="is-highlighted">Which observation resolves the stated uncertainty?</li>
<li>Under which condition does the effect fail?</li>
</ol>
:::

::: {.research-block .research-block-hypotheses}
**Research hypotheses**

<ol class="research-hypotheses">
<li class="is-highlighted">The proposed signal improves the primary outcome relative to the named baseline.</li>
<li>The effect persists under the stated distribution shift.</li>
</ol>
:::
::::
```

- Use one to nine items per list. Split a longer set across explicit slides instead of producing Q10/H10 or shrinking the slide.
- A question states an uncertainty the study can answer; a hypothesis states a falsifiable expected relation, direction, population/task, and comparison when known.
- Keep identifiers stable across the deck and map each question/hypothesis to visible evidence or a clearly marked unresolved result.
- Use `.is-highlighted` on at most one primary item per list. It adds weight, a thicker rule, and an inset line as well as profile color, so emphasis does not depend on color alone.
- Questions use the selected profile's accent role; hypotheses use its success role. Do not override those colors per slide.
- Keep illustrative examples labeled until paper-grounded wording and evidence replace them.

## Grid navigation without losing the audience

Quarto warns that audiences often miss vertical slides. Sinew mitigates, but does not eliminate, that risk.

- Put the core story at the first vertical position of each horizontal stack.
- Say when you move down for detail and when you return to the main path.
- Keep controls enabled and use `O` overview during rehearsal.
- Share a linear PDF or `?view=scroll` version after the talk.
- For fixed-timing video, define one deterministic linear route and do not rely on live 2D choices.

## Text and typography

- Use printable ASCII characters from a standard US keyboard in slide source and visible slide text. Spell out or use ASCII equivalents for arrows and other decorative symbols.
- Write math with `$...$` inline or `$$...$$` for display math. Put ASCII LaTeX commands inside the delimiters instead of pasting Unicode math glyphs.
- Use sentence case.
- Prefer short declarative sentences and concrete verbs.
- Do not use all caps, underline, italics, or color as the sole emphasis channel.
- Keep body text at the theme default; do not solve overflow with `.smaller` unless the slide is a reference/appendix.
- Expand abbreviations on first use.
- Keep all visible slide text in the documented printable-ASCII set so glyph availability is deterministic.

## Equations

- Show only the expression needed for the claim.
- Define every symbol used on the slide.
- Use semantic color only if the same relation is repeated through labels/position.
- Reveal derivations across separate slides or fragments only when pacing is rehearsed.
- Put long proofs in a vertical backup stack.

## Code

- Show the interface or critical invariant, not an implementation dump.
- Keep syntax highlighting secondary to the logic.
- Crop to the lines discussed and use line highlighting.
- Wrap and size code so it fits without horizontal or vertical scrollbars. Split the example across slides if wrapping harms comprehension.
- Never include credentials, private URLs, participant data, or machine-specific paths in a public deck.

## Citations and provenance

Use `references.bib` and Pandoc citations such as `[@alley2013]`; do not hand-format a parallel reference list. Sinew enables `link-citations` and `citations-hover`, so every rendered citation must support a hover/focus preview. The hover card inherits the active profile's surface, ink, border, accent, typography, and radius tokens. Add a DOI or stable project URL to each BibTeX entry when one exists, then verify the rendered link with keyboard and pointer input.

Keep exactly one `::: {#refs}` target in `.global-references-slide`; it is the semantic citeproc source and must not be duplicated. Each gallery style has a `.style-references` container whose `data-reference-keys` selects entries from that global source. The Sinew runtime clones those entries with list semantics and rewrites citations in that horizontal stack to its local references slide. The original entries stay in the document for Quarto's previews. Do not hand-copy formatted entries or duplicate IDs.

Every global or local references view uses two columns without splitting an entry. Do not manually add `.smaller` or `.scrollable`; the theme overrides Quarto's automatic helpers so references remain fixed to the slide canvas. If a scoped view no longer fits legibly, reduce its key set, split the scope across additional explicit slides, or move the complete list to a handout instead of shrinking or scrolling it.

Only cited items appear by default. Use the documented Pandoc `nocite` metadata deliberately when the deck must list an uncited resource. Put a visible short source on the same slide as reused figures, video, datasets, or borrowed claims; a hover preview does not replace projected attribution. Confirm license/permission because citation is not reuse permission.

## Computation

Included executable `.qmd` files may contain cells, but every include in one document must use the same engine (Jupyter or knitr). Prefer a reproducible figure-generation script that writes to `assets/figures/`, then render the deck without expensive training/evaluation code.

Record the data snapshot, script, environment, and command that produced every result figure. Never generate a new metric from partial logs just to fill a slide.

## Speaker notes

```markdown
::: {.notes}
- 0:00-0:15: state the claim.
- 0:15-0:40: explain axes and uncertainty.
- 0:40-0:55: interpret; disclose limitation.
:::
```

Use notes for pacing and exact caveats. Run speaker view on the actual browser and verify the projector sees only the audience window.

## Before release

- Run `python3 scripts/validate.py`.
- Render the exact one selected `color-*` profile.
- Inspect at 1920x1080 and 1280x720.
- Check every slide in overview and linear traversal.
- Present once with network disabled.
- Export and inspect PDF/video when the venue requires it.
- Rehearse aloud to the hard slot with changeover margin.
- Reopen current official presenter instructions and compare every delivery constraint separately from the visual style.
