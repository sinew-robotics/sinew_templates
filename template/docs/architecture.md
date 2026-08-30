# Architecture

The public repository targets its `template/` subdirectory for starter and extension installation. After `quarto use template sinew-robotics/sinew_templates/template`, that subdirectory becomes the new presentation root, so all paths below are project-root-relative. Quarto may namespace a remotely installed extension as `_extensions/sinew-robotics/sinew/`; the format name remains `sinew-revealjs`, and the shipped validator accepts both the source and installed paths.

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

## Slide numbering

`slide-number: c` in `_extensions/sinew/_extension.yml` is the shipped default. This is Reveal's "flattened" format: the printed number is a single sequential counter (1, 2, 3, ...) equal to each slide's position in the deck source, walked depth-first (every horizontal stack in order, every vertical slide inside a stack in order), matching Reveal's own `getSlidePastCount()` computation (`reveal/dist/reveal.esm.js`, `case "c"` in the slide-number controller) and Quarto's own `document-slides.yml` schema, which documents `c` as "Flattened slide number". This was confirmed by rendering the deck and reading the live `.slide-number` element at each position with a scripted browser walk: numbering the deck's first stack (`01-intro`, 5 slides) followed by the second stack (`02-origami`, 11 slides) produced exactly `1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15`.

**Numbering is positional: a section divider counts as a slide.** `#` divider files are the first vertical slide (index 0) of their stack, so the first *content* slide in a stack is the second number in that stack, not the first. Observed: slide 1 is the deck's opening divider, slide 6 is the `02-origami` stack's divider, and slide 7 is that stack's first content slide. A deck built on an earlier `h.v`-numbered template exhibits the same fact under that scheme: the divider is `N.1`, so the first content slide is `N.2`. This has caused real confusion (a presenter reverse-engineering which slide a screenshot showed); say so explicitly when discussing a slide by number with someone unfamiliar with the deck.

**Opt back into the previous numbering.** Earlier decks built on this template used `h.v` (horizontal.vertical, e.g. "5.4") across 34 slides without reported confusion once presenters knew the divider-counts rule above. To restore it, set one line in `_extensions/sinew/_extension.yml`:

```yaml
slide-number: h.v
```

**Resolved: `c` matches forward Space-key order in a delivery deck.** An earlier revision of this document reported an open defect here: `navigation-mode: grid` made `c` diverge from what pressing Space actually reached. That has been fixed by changing the shipped default in `_extensions/sinew/_extension.yml` from `navigation-mode: grid` to `navigation-mode: default`. The rest of this section keeps the original trace and measurements, because they are the evidence for the fix and for why `navigation-mode: default` (not `linear`) was chosen; see also `_extensions/sinew/_extension.yml`, where the same reasoning is repeated as a comment next to the setting.

Root cause, traced in `reveal/dist/reveal.esm.js`: pressing Space always runs Reveal's depth-first route regardless of `navigation-mode` (the `next()` function tries a down-route within the current stack first, and only moves to the next stack, via the same internal function `right()` uses, when there is none left). What `navigation-mode` actually controls is what vertical row that next-stack move lands on: `right()` calls `Ye(c+1, "grid"===A.navigationMode?h:void 0)` and `left()` calls the mirror-image `Ye(c-1, "grid"===A.navigationMode?h:void 0)`, so `grid` mode passes the *current* row `h` in both, preserving it across the jump, while every other mode passes `void 0`, which resets to the target stack's own last-visited row (0 on a first visit). With `navigation-mode: grid` and stacks of unequal height, forward Space rides whichever row it last reached across every remaining stack instead of visiting every slide.

This was not hypothetical for this deck: `01-intro` has 5 slides but every topic stack (`02-origami` through `10-movement`) has 11. Under the old `navigation-mode: grid` default, a scripted forward Space walk from slide 1 (driven through real `Reveal.next()` calls in headless Chrome, not simulated) produced the number sequence `1, 2, 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 27, 38, 49, 60, 71, 82, 93, 104` and then stopped---only 20 of the deck's 104 slides reachable by pressing Space forward from the start. Under `navigation-mode: default`, the identical scripted walk against the identical deck instead produces `1, 2, 3, ..., 104`, every slide in order, confirmed by driving real `Reveal.next()` calls to completion.

**Why `default` and not `linear`.** Reveal has three navigation modes; `grid` was ruled out above. `linear` also resets the row on a stack change (same `void 0` branch as `default`), so it would fix forward Space too, but it was rejected because it changes what the *physical* arrow keys do: `reveal.esm.js`'s keyboard handler sets `h = "linear"===t.navigationMode || !hasHorizontalSlides() || !hasVerticalSlides()`, and when `h` is true, Up and Down stop calling `up()`/`down()` (move within the current stack) and instead call `prev()`/`next()` (the same depth-first route as Space/Shift+Space). Measured directly: starting at the bottom of the `01-intro` stack (indices `h=0,v=4`, no further down-route) and dispatching a physical Down-arrow `keydown`, `navigation-mode: default` correctly stays at `h=0,v=4` (no route), while `navigation-mode: linear` jumps to `h=1,v=0`---the next topic stack, not "down" in any sense a viewer watching the on-screen Down arrow would expect. That breaks the "up/down: move within a subtopic" contract in `README.md` and the vertical-evidence-stack model this template is built around, so `default` is the delivery setting; `linear` is not used anywhere in this repository.

**The gallery keeps `navigation-mode: grid` deliberately, and only there.** `_quarto-gallery.yml` (the internal repository-tour layer described above, not a visual-style profile) sets `navigation-mode: grid` for its own `format.sinew-revealjs` block. This overrides the extension's `default` setting when the `gallery` profile is active (Quarto's project-profile metadata takes precedence over an extension's format defaults; confirmed by rendering both `quarto render template` and `quarto render template --profile color-origami` and reading the emitted `Reveal.initialize({...})` config in each `_site/index.html`: `navigationMode: 'grid'` in the zero-config gallery build, `navigationMode: 'default'` in the single-profile delivery build). The row-preserving jump is exactly what the gallery wants: moving right lands on "the same slide type" in the next style column so columns are visually comparable. A scripted forward Space walk against the gallery build reproduces the same `1, 2, 3, 4, 5, 10, 11, ..., 104` sequence measured above---expected and unchanged, because the gallery is a tour layer, not the thing `README.md`'s "Space: traverse every slide linearly" promise describes.

**Scroll view (`?view=scroll`) and print PDF (`?print-pdf`) do not read the `c`/`h.v` format the same way as the standard view:**

- Scroll view renders a single live `.slide-number` overlay rather than one per slide, and in this deck it reported a value out of range for both formats tested (`c`: `115` against 104 real slides; `h.v`: `NaN`) alongside an inflated `getTotalSlides()`/section count (114, not 104)---a pre-existing Quarto/Reveal scroll-view DOM quirk, not something this change introduces or can fix from `_extension.yml`.
- Print PDF stamps a `.slide-number-pdf` element on every page and does survive numbering, but the exporter (`reveal.esm.js`, PDF layout code: `let v=1; ... e.innerHTML=v++`) always uses its own flat auto-incrementing counter and ignores the configured `slideNumber` format entirely. Both `c` and `h.v` renders produced identical printed pages numbered `1` through `104`. This means the `h.v` opt-back-in restores "horizontal.vertical" numbers on screen but not in exported PDFs, which will always show plain sequential page numbers.

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
- `.research-framing`, `.sinew-reference`, `.institution-lockup`
- `ol.takeaways`
- `.section-slide`

New visual styles should target these roles and tokens, not sample-slide IDs.

## Deck-level overrides vs. template changes

`quarto use template sinew-robotics/sinew_templates/template` copies the extension into the new presentation root; it does not symlink or otherwise share it with this repository or with any other scaffolded deck. Each scaffolded deck therefore gets its own on-disk copy of `_extensions/sinew/theme/core.scss` (and the rest of the extension), so editing a deck's copy touches only that deck. This means there is no per-file rule that forces one override route: both `core.scss` and a deck-local stylesheet are always available, and the choice is a judgment call the author has to make and record.

A real deck (`slides/dexreset/` in the private `orel/DexReset` repository, verified against its own checked-out copy, not reported secondhand) used both routes side by side and is a useful worked example of drawing that line:

- **`assets/deck-overrides.css`** for CSS that is inherently specific to that one deck's content and cannot be generalized: `vertical-align: middle` on `.column` for one slide's uneven-height split, `.center-figure` for centering one figure inside its own column, and an `img.plate` rule hand-written before `.plate` existed upstream. The file opens with a one-line header comment stating why it exists at all -- "kept here rather than in `_extensions/sinew/theme/core.scss` so the shared Sinew template is not modified by this deck" -- and every rule inside it carries its own comment explaining the specific layout problem it fixes.
- **Direct `core.scss` edits** for two things the deck's own style contract (`docs/DECK_STYLE.md`) explicitly framed as generic and reusable rather than one-off: `.diagram-flow`/`.diagram-step`/`.diagram-arrow` (a flex-row pipeline component, added under a comment banner reading "DexReset-local additions... generic, reusable primitives (not one-off widgets tied to a single slide)") and sizing rules for that deck's own two institution-lockup marks, each with a comment explaining why the two logos needed different heights to read at matching optical weight.

Both routes are legitimate; the distinguishing question is not "is this deck-specific" (the institution-lockup sizing above is deck-specific and still lives in `core.scss`, because it has nowhere else to go -- it targets a component `core.scss` itself defines) but "is this a generic, reusable primitive that could plausibly serve another deck, or a fix specific to this deck's own content and assets." A generic primitive belongs in `core.scss` because that is where every other generic component lives, styled with the profile's own tokens so it works in whichever color profile the deck selected; a content-specific fix belongs in a deck-local stylesheet so a future template update to `core.scss` (this deck does not track template changes automatically once scaffolded) does not have to reconcile against it.

That deck's `core.scss` also carried one undocumented edit: `ol.research-questions`/`ol.research-hypotheses` gap, minimum height, padding, and font size were changed to a denser, larger-text layout, with no comment explaining why -- the only edit in the file without one. This is the failure mode the rule below exists to prevent: reviewing that diff in isolation, there is no way to tell an intentional, considered change (a real projection-legibility fix, matching the pattern of every other edit in the file) from an accidental one, and no way to know whether reverting it during a template sync would be safe or would silently undo a fix someone needed.

**Require a rationale comment on every direct `core.scss` edit**, in the deck's own copy, stating what problem it solves and, if the rule is deck-specific rather than a generic primitive, why it could not live in a deck-local stylesheet instead. This is not paperwork: three of this deck's own generic `core.scss` additions -- `.diagram-flow`/`.diagram-step`/`.diagram-arrow`, a `.plate`-shaped light backing for untouched artwork, and an `h1.full-bleed-title`-style measure override -- independently anticipated primitives that v1.2.0 later shipped natively (see "Named layout primitives" above and `docs/figures-and-tables.md`, "A third path: plate it instead of stripping or leaving it white"). A rationale comment is what let this documentation sweep recognize those as upstream candidates instead of deck-specific noise; an undocumented edit like the Q/H density change cannot be told apart from an accident, whether the intent was to keep it local or to propose it upstream.

## Citation views

Pandoc citeproc generates one authoritative `#refs` list. Sinew keeps that list in `.global-references-slide` and uses `captions.html` to clone selected entries into each `.style-references` container after the document loads. The clones remove source IDs, preserve list roles, and remain derived from `references.bib`. Citation links inside a style stack are then routed to that stack's stable `#references-<style>` slide; Quarto hover previews continue to read the original `ref-<key>` entries.

The bundled `research-references.lua` shortcode extension emits semantic placeholders for `{{< q N >}}`, `{{< h N >}}`, and `{{< alg algorithm-id >}}`. The post-body runtime numbers algorithm captions, adds Q1-Q9/H1-H9 identifiers and accessible names, resolves those placeholders in the current horizontal stack or to one unique deck-wide statement, and supplies direct hyperlinks. It also registers native Quarto figure/table cross-references plus Sinew algorithm/Q/H references for profile-aware Tippy previews. Preview factories rerun KaTeX on unprocessed cloned math. Evidence-specific Tippy themes give tables a wider maximum than figures, algorithms, statements, or bibliography entries.

The same runtime registers figures, tables, and captioned algorithms with the evidence inspector. The native dialog stays inside `.reveal` so it inherits the currently active gallery/profile tokens while entering the browser top layer. It clones evidence only when opened, strips duplicate IDs, reruns math typesetting, traps Reveal key handling inside the dialog, and restores focus when closed. All three evidence types use the same control-free direct-interaction mode: the source object is keyboard focusable, a second click inside fullscreen content closes the dialog, and evidence-specific CSS uses the viewport while preserving each object's structure. Captions use viewport-responsive type.

`installInstitutionLockups()` treats the authored divider lockup as the canonical source and clones a compact decorative copy into every content slide at startup. Clones retain image alpha and aspect ratio, but use empty alternative text and `aria-hidden` because announcing identical affiliation marks on every slide would be redundant.

The Tippy `light-border` citation and internal-reference previews are restyled in `core.scss` using the same `--sinew-*` tokens as the active deck. In gallery mode, the hover surface therefore changes with the current column. In a standalone profile, it follows the single selected profile.

## Plot-style pairing

Static figures do not inherit Reveal CSS. Each color profile therefore has a matching `styles/matplotlib/sinew-<style>.mplstyle` overlay. Compose the common `sinew-slides.mplstyle` first and the selected style overlay last. `scripts/generate_gallery_plots.py` exercises every overlay with the same illustrative chart so palette, text, grid, legend, marker, and line behavior can be compared.

## Delivery research boundary

`docs/conferences/` contains dated background research about event logistics. Those files are not profiles, do not merge into Quarto metadata, and do not alter the deck. Authors must verify the exact current event, edition, track, and artifact requirements separately from style selection.

## Resource policy

`embed-resources: true` is the offline-safe default. If a talk adds MP4 video, test the target browser: some browser/media combinations do not decode video from data URIs. In that case set `embed-resources: false`, ship the generated dependency directory and assets, and present over a local HTTP server.

The Reveal format uses Quarto's KaTeX browser path for dollar-delimited math. Quarto keeps the TeX source in the generated HTML and the KaTeX runtime replaces it when the deck loads. This avoids the incompatible MathJax 2 loader previously seen in the gallery. Test every added LaTeX command in a browser because KaTeX and MathJax do not support exactly the same command surface.

Do not use remote font imports in delivery-critical decks. Bundle licensed fonts or specify robust system fallbacks and test on the presentation machine.
