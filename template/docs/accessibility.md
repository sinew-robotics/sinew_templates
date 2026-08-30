# Accessibility baseline

Sinew aims for an accessible authoring baseline; it does not claim that arbitrary generated decks conform to WCAG. Accessibility depends on slide content, static figures, media, delivery, narration, and exported artifacts - not only CSS.

## Normative web criteria when claiming WCAG 2.2 AA

- [Non-text content](https://www.w3.org/TR/WCAG22/#non-text-content): informative visuals need equivalent text alternatives.
- [Use of color](https://www.w3.org/TR/WCAG22/#use-of-color): color cannot be the only information channel.
- [Contrast minimum](https://www.w3.org/TR/WCAG22/#contrast-minimum): normal text at least 4.5:1; large text at least 3:1.
- [Non-text contrast](https://www.w3.org/TR/WCAG22/#non-text-contrast): meaningful graphical objects and interface indicators generally need 3:1 against adjacent colors.
- [Info and relationships](https://www.w3.org/TR/WCAG22/#info-and-relationships): headings/table relationships must be programmatically available.
- [Captions prerecorded](https://www.w3.org/TR/WCAG22/#captions-prerecorded): prerecorded speech requires captions for AA.
- [Pause, stop, hide](https://www.w3.org/TR/WCAG22/#pause-stop-hide): automatically moving content lasting over five seconds needs controls, subject to the criterion's exceptions.

WAI's [complex-image tutorial](https://www.w3.org/WAI/tutorials/images/complex/) recommends a short alternative plus a detailed textual equivalent and adjacent summary for charts/diagrams.

## Authoring rules

### Images and plots

- Every informative image has nonempty `fig-alt`.
- Decorative images explicitly use empty alt text and carry no evidence.
- Complex plots have a short alt, visible takeaway, and detailed prose/table equivalent in the deck or handout.
- Lines use color plus marker/dash/direct label.
- Plot text, grid, and data contrast is checked inside the image, not inferred from theme CSS.
- An intentionally unfilled evidence slot uses `.missing-evidence`, never a blank gap or a plausible-looking stand-in. It never relies on its dashed border and hatch fill alone: the runtime injects a "MISSING EVIDENCE" label as real DOM text, not CSS-generated content, because some assistive technology does not expose generated content. It is a genuine numbered `Figure N` with a `#fig-` id, so it is reachable the same way as any other figure.

### Structure

- One level-1 divider per stack and one level-2 heading per content slide.
- Do not skip heading levels to make text smaller.
- Use semantic Markdown tables with captions and headers.
- Use real lists, figures, captions, and links rather than screenshots of text.
- Use the semantic research-question and research-hypothesis lists so Q1-Q9/H1-H9 remain textual as well as colored; the unboxed primary highlight also uses text weight and a filled identifier label.
- Use `{{< q N >}}` and `{{< h N >}}` for in-text statement references. The links retain visible Q/H text, underline, and weight without a permanent bounding box; hover and keyboard focus expose the original statement in a profile-aware preview.
- Keep native figure and table semantics in the authored source. The runtime makes figures, tables, and captioned algorithms focusable interactive objects because visible expand/close controls are intentionally suppressed: Enter or Space opens focused evidence and Escape closes it.

### Typography and language

- Large sans-serif body text; robust fallback stacks.
- Bold and spatial hierarchy rather than all caps/italic/underline/color-only emphasis.
- Expand abbreviations and explain symbols.
- Use plain, inclusive language and pronounce/read essential visual information aloud.
- Test non-Latin glyph coverage on the presentation machine and in PDF/video exports.

### Motion and media

- No flashing content.
- Sinew respects `prefers-reduced-motion`; `color-high-contrast` disables slide transitions.
- Videos have controls unless a venue requires immutable self-advancing playback.
- Spoken media has captions/transcript; meaningful experiment audio is described.
- Provide a still/poster fallback.
- The managed video component autoplays muted by default when Reveal enters its slide (`data-sinew-autoplay="false"` opts out for a manual start). Unmuted playback is an explicit author choice made by omitting `muted`; browsers block unmuted autoplay outside a user gesture, so an unmuted video entered by Reveal navigation typically stays paused with its own controls visible rather than throwing, which is expected. See `figures-and-tables.md` for the captions/transcript requirement on any video that carries speech.

### Live delivery

- Verbally state the finding shown by each visual.
- Read/describe axis meaning before interpreting trend.
- Repeat audience questions into the microphone.
- Use a screen-visible mouse pointer; avoid physical laser pointers in multi-screen/remote setups.
- Announce deliberate vertical navigation so the audience understands location.

## Contrast testing

Test at least these pairs for each color profile:

- ink/background;
- muted/background;
- link/background;
- focus/background;
- caption/background;
- data series/plot surface and series/series at overlaps;
- table rules/surface;
- danger and success text/surface.

CSS contrast tools cannot evaluate pixels in PNG/JPEG or every SVG path. Review figures separately and inspect a grayscale rendering.

## Automated and manual gates

Automated checks should cover missing alt/captions, semantic structure, duplicate IDs, profile markers, and gross overflow. `template/scripts/check_overflow.py` covers the last of those: it measures the actual rendered geometry of every slide in a headless browser and reports any element whose box extends past the deck's configured canvas, since neither render success nor valid HTML signals silent overflow on its own. Its exit code 2 means the gate did not run at all (no headless browser available), not that it passed; treat that as an unresolved check, not a pass. Quarto's Reveal format supports an `axe` audit option; use it in the release environment where browser automation is available.

`template/scripts/check_render.py` (run via `check-render.sh`) also scans rendered visible text for decorative Unicode -- arrows, math glyphs, emoji, box-drawing, and symbol characters that fail on an unknown projector. It strips `<script>`/`<style>`/comment blocks before stripping tags so it never flags non-ASCII living in inert library code, then allowlists only ASCII plus the toolchain's own smart-typography and non-breaking-space output (see AGENTS.md); anything else fails with the offending codepoint, an occurrence count, and a text excerpt.

Manual review still checks:

- whether alt text conveys the actual finding;
- whether a chart remains interpretable without color;
- whether projection and room lighting preserve contrast;
- whether speaker narration covers visual-only information;
- whether PDF/video exports retain tags, fonts, captions, and legibility;
- whether animations/media can be paused where required.
- whether every evidence inspector opens with pointer and keyboard, retains the active profile, traps Reveal navigation, restores focus, and closes when the fullscreen evidence is clicked; no evidence type may show expand/close controls. This now covers video and GIF alongside image, table, and algorithm evidence: a zoomed video keeps its trim window and playback position instead of restarting.
- whether cloned preview math is typeset and wide table previews retain legible headings, values, and navigation at browser zoom.
- whether figure, table, algorithm, Q, and H references expose previews on pointer hover and keyboard focus, then navigate to the correct original target when activated.

An automated "pass" is not evidence of statistical honesty, accessible chart semantics, or a comprehensible talk.
