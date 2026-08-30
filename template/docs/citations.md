# Citations

Sinew renders citations through Quarto/Pandoc citeproc and a bundled CSL
(Citation Style Language) file. This document is authoritative for citation
style selection, the global-numbering semantics of the per-style reference
views, the provenance of the bundled CSL files, guidance for citing your
own unpublished work, and the citation lint rules.

## The two styles

| Style | In-text form | CSL file | Status |
|:--|:--|:--|:--|
| Numeric (IEEE) | `[1]` | `styles/citations/ieee.csl` | Default |
| Author-year (Chicago author-date) | `(Alley 2013)` | `styles/citations/chicago-author-date.csl` | Documented option |

The default is set project-wide in `_quarto.yml`:

```yaml
csl: styles/citations/ieee.csl
```

Every profile and render (`quarto render template`, any `--profile
color-*`, and the zero-config gallery) inherits this. Citation style is a
bibliography/document concern, not a visual axis: it is not one of the
`color-*` profiles, and switching it does not touch palette, fonts,
surfaces, or plot tokens. See `docs/architecture.md` for what a color
profile does and does not own.

### Switching to author-year

Add one line to `deck.qmd`'s YAML front matter:

```yaml
csl: styles/citations/chicago-author-date.csl
```

This is a document-level override of the project default and applies to
the whole deck (there is no per-style-column citation setting). To go back
to numeric, remove the line or point it back at `styles/citations/ieee.csl`.

Quarto's YAML schema rejects `csl: null` and `csl: ""` as a way to fall
back to Pandoc's built-in default citeproc style, so if you want author-year
behavior you must point `csl:` at an explicit author-date CSL file, as
above, rather than trying to unset the key.

Both styles were rendered and verified against this repository's own
nine-style gallery deck (`quarto render template --profile color-origami`,
then `template/scripts/check-render.sh`), including in-text markers, the
global bibliography, and every per-style cloned reference view.

## Global-numbering semantics of the per-style reference views

This deck has one authoritative citeproc bibliography (`#refs`, on the
intro column's references slide) and nine per-style `.style-references`
containers that each clone a subset of that bibliography's entries (see
`docs/architecture.md`, "Citation views"). A numeric CSL numbers entries by
order of first citation across the *whole rendered document*, not per
column. This has one direct consequence: a citation marker's number is a
property of the deck, not of the column it is viewed from, so it must stay
identical everywhere that citation appears. A cloned per-style view
therefore keeps the entry's global number rather than renumbering `1..n`
locally, which would make the same marker mean different things in
different columns.

Left unmanaged, this means the entries visible in a four-entry style column
can appear in a document-order-looking but visually arbitrary sequence
(for example `[7] [2] [15] [3]`), because the clone script
(`buildStyleBibliographies()` in `_extensions/sinew/theme/captions.html`)
appends entries in the literal order listed in that container's
`data-reference-keys` attribute. To keep the numbers reading as intentional
rather than broken, `data-reference-keys` in every
`_slides/<NN>-<style>/_09-references.qmd` file is ordered ascending by each
key's global citation number, not by topic or alphabetically. In this
deck's gallery, the four keys shared across all nine style columns
(`alley2013`, `scienceplots2021`, `wcag2023`, plus that column's own
`sinewX2026` provenance record) sort to `alley2013 scienceplots2021
wcag2023 sinewX2026`, which is why every gallery style column's local
bibliography currently reads:

```text
[1] Alley ...
[4] Garrett, SciencePlots ...
[5] World Wide Web Consortium, WCAG 2.2 ...
[6] Sinew Templates, <style> visual profile ...   (number varies per column, 6-14)
```

If you add or reorder citations, re-derive each column's ascending order
from the rendered global numbers (or from first-citation order in
`deck.qmd`'s include sequence) rather than guessing; do not assume the
literal order already in the file is still correct after an edit.

This ordering is content in the `_slides/*/_09-references.qmd` files, not
runtime behavior in `captions.html`. `captions.html` itself is
citation-style-agnostic: it clones entries by `id="ref-<key>"` and never by
citation number, so it needed no change for either style, and any future
change to it should preserve that property.

## CSL provenance

Both CSL files are vendored locally under `template/styles/citations/` for
offline, no-remote-fetch delivery (a hard repository rule). They are
byte-preserved exactly as published upstream; `template/scripts/validate.py`
does not scan `.csl` files for the printable-ASCII rule that applies to
Markdown/YAML/slide sources; that rule intentionally does not need a listed
exemption because its file-selection glob (`*.md` and `_quarto*.yml`) never
matches a `.csl` path, but if that glob is ever broadened to be more
inclusive, `.csl` paths must be excluded rather than mangled.

### `styles/citations/ieee.csl`

- Title: "IEEE Reference Guide version 11.29.2023"
- Source: `https://raw.githubusercontent.com/citation-style-language/styles/master/ieee.csl`
- Project: the official CSL styles repository, `citation-style-language/styles`
  (the canonical distribution point for CSL styles used by Zotero, Mendeley,
  Pandoc, and Quarto)
- Author of record (per the file's own `<info>` block): Michael Berkowitz,
  with contributors including Julian Onions, Rintze Zelle, Stephen Frank,
  Sebastian Karcher, Giuseppe Silano, Patrick O'Brien, Brenton M. Wiernik,
  and Oliver Couch
- License: CC BY-SA 3.0 (Creative Commons Attribution-ShareAlike 3.0
  Unported), declared both in the file's own `<rights
  license="http://creativecommons.org/licenses/by-sa/3.0/">` element and in
  the repository's README ("All styles in this repository are released
  under the Creative Commons Attribution-ShareAlike 3.0 Unported license")
- Upstream commit at time of vendoring: `1ccf4696be22ea0b55f83cc9163bde3061fddb0a`
  ("IEEE: Use three-letter abbreviations for months (#7979)"), dated
  2026-01-07
- Inspection/vendoring date: 2026-08-30
- Not modified from the upstream file.

### `styles/citations/chicago-author-date.csl`

- Title: "Chicago Manual of Style 18th edition (author-date)"
- Source: `https://raw.githubusercontent.com/citation-style-language/styles/master/chicago-author-date.csl`
- Project: the official CSL styles repository, `citation-style-language/styles`
- Author of record (per the file's own `<info>` block): Andrew Dunning
- License: CC BY-SA 3.0 (Creative Commons Attribution-ShareAlike 3.0
  Unported), declared both in the file's own `<rights>` element and the
  repository README, same as above
- Upstream commit at time of vendoring: latest on `master` as of
  2026-08-30 (`<updated>2025-02-09T00:00:00+00:00</updated>` in the file's
  own metadata)
- Inspection/vendoring date: 2026-08-30
- Not modified from the upstream file.

A source reference is provenance, not permission to redistribute protected
assets; both files above carry an explicit open license from their
publisher, so no separate reuse authorization is required.

## Citing your own unpublished work

Half of an academic talk is often the author's own unreleased system, run,
or result. That material has no bibliography entry to cite, and it must
never borrow one that belongs to someone else's work.

**Hard rule: a citation to a third party must never be attached to your own
material.** A caption, claim, or figure describing your own unpublished
run, system, or result must not carry `[@someone-elses-key]` merely because
that person's paper is topically related (a baseline you compared against,
a method you built on, a system with a similar name). A concrete near-miss
this rule exists to prevent: a caption read "State expert from OmniReset
`[@yin2026omnireset]`" over a clip that was actually the author's own run,
not footage from the OmniReset paper. The citation implied the clip came
from someone else's published work when it did not.

The correct pattern:

- Label unpublished internal work in prose, not with a citation marker:
  "Ours (unpublished)", "our system", "internal run, not yet published",
  or similar plain-language framing directly in the caption or claim.
- If you are citing prior published work for comparison or as a baseline
  *and separately* showing your own unpublished result, keep the two
  visually and textually distinct: cite the published work where it
  actually appears (its own figure, its own claim), and mark your own
  material as your own wherever it appears, even in the same slide.
- If your own work has since been published or preprinted, add its own
  `references.bib` entry (a `@misc` or `@unpublished`-style BibTeX entry is
  fine for a preprint or internal report) and cite that, rather than
  reusing someone else's key.
- Do not fabricate a citation key for your own work just to get a `[N]`
  marker; an uncited "Ours (unpublished)" label is correct and preferred
  over an invented bibliography entry. See `AGENTS.md` and
  `CLAUDE.md`'s evidence rules: fabricating citations is a hard violation
  regardless of citation style.

## Lint rules

`template/scripts/validate.py` (`validate_citations`, called from the
universal per-included-file loop in `validate_manifest_and_slides`) checks
every included slide source for:

- **Empty citation keys.** `[@]`, `[@key1; @]`, or any other `@` not
  immediately followed by a valid citation-key character renders as
  nothing in the output, silently, with no warning from Quarto. The check
  flags the slide file so the empty citation is caught before render
  rather than by someone noticing a gap in a bibliography later.
- **Citation keys missing from `references.bib`.** Any `@key` used in a
  slide that has no matching entry in `references.bib` silently drops that
  citation from the rendered bibliography rather than failing the build.
  Native Quarto cross-references (`@fig-...`, `@tbl-...`, `@eq-...`,
  `@sec-...`, and similar reserved prefixes; see `docs/architecture.md`)
  use the same `@key` syntax but are not bibliography citations, and are
  excluded from this check.

Both checks are universal (they run for any deck built on this template,
not just this repository's nine-style gallery) because they operate on
whatever `deck.qmd` actually includes and on `references.bib`, neither of
which is gallery-specific.
