# Figures, tables, and robotics media

## Evidence standard

A visual is ready only when an unfamiliar expert can answer:

- What is compared?
- On which task/population/data split?
- What do axes, units, markers, bands, and symbols mean?
- How many trials, episodes, participants, environments, or seeds support it?
- What aggregation and uncertainty are shown?
- Is the claim descriptive, predictive, or causal?
- Is the result simulated, real-world, retrospective, or prospective?
- What source and license apply?

## Figures

Prefer SVG for plots/diagrams and PNG/JPEG for photos, camera frames, heatmaps, and dense raster sensor data. Avoid screenshots of plots: source vectors/raster exports preserve size, contrast, and typography.

Quarto syntax:

```markdown
![Finding-oriented caption](assets/figures/result.svg){
  #fig-result
  width="82%"
  fig-alt="Line plot of success versus training steps. The solid circle-marked method reaches 80% around twice as early as the dashed square-marked baseline."
}
```

For a complex chart, add a detailed prose/table equivalent in the slide, appendix, or linked handout. Alt text identifies the important structure and finding; the caption states conditions, statistics, and provenance. Do not repeat identical text in both.

### Plot content

- Put units in axes.
- Use a meaningful zero/baseline; disclose truncation.
- Direct-label curves when possible.
- Combine color with dash, marker, hatch, position, or text.
- Define bands/error bars and report `n`/seeds.
- Use consistent scales across comparison panels.
- Use perceptually uniform sequential maps (`viridis`, `cividis`, `magma`, `inferno`) for ordered magnitude.
- Use a diverging map only when the center has meaning.
- Do not use a categorical rainbow for ordered values.
- Show failure cases when they bound the robotics claim.

### White backgrounds: strip them or plate them

Two different fixes exist for artwork that assumes a white page and clashes with the deck surface. Pick the one that matches the source, not habit.

Strip the white background with `template/scripts/make_transparent.py` when:

- the source is clean line art or a vector-style diagram (a plot export, an SVG rasterized to PNG, a hand-drawn schematic) and it should sit directly on the slide surface with no visible box;
- white in the source is genuinely background, not content.

Use a light plate behind the untouched artwork instead when:

- the source is a photo, a screenshot, or a JPEG with compression noise, where per-pixel background detection is unreliable;
- white in the source has meaning (a filled box, a callout, content you must not alter);
- provenance rules require the original pixels to stay untouched (an adapted/reused external figure).

Install Pillow first; it is optional for the deck as a whole:

```bash
python3 -m pip install -r template/requirements-imaging.txt
```

Worked example -- a line-art diagram exported as PNG on a white canvas:

```bash
python3 template/scripts/make_transparent.py \
  raw/architecture.png \
  -o assets/figures/architecture.png \
  --tolerance 10
```

Any Pillow-readable raster (JPEG, PNG, WEBP, BMP, TIFF, GIF) is accepted; the output is always PNG. `--tolerance` (0-100, default 12) sets how far from pure white still counts as background. It drives a graded alpha ramp, not a hard cutoff, and the ramp's width adapts to whether a pixel looks neutral (an antialiasing residue) or genuinely hued (real content close to white), so antialiased edges do not keep a white fringe while a pale colored highlight is not faded away by mistake. Guidance, re-measured against the current formula: clean vector/PNG line art, including antialiased edges, typically needs 5-15; lossy JPEG sources (whose "white" runs 240-254, not exact 255) typically need 10-25, higher for noisier compression. Raise it if a pale fringe or off-white residue survives; lower it if artwork color is being eaten. Do not go far past 25-30: at very high tolerance the tool starts treating genuinely dark, non-background content as partly transparent too (see the alpha-formula section of the script's module docstring for the exact tradeoff and the measurements behind these numbers). Caveat -- very saturated or vivid ink colors (close to a pure primary such as (0, 0, 255)): a genuinely faded edge pixel of such ink can be indistinguishable, pixel by pixel, from deliberately authored pale content of the same hue, so a partial fringe can still survive at any tolerance -- this is a proven limit of judging one pixel's own color in isolation, not a tuning gap; see "Known residual limitations" in the script's module docstring for the measured numbers and the exact counterexample. Two ways out, and which to prefer depends on whether the source is yours to edit:
- If you own the source (your own plot/diagram export): mute the ink color slightly before stripping -- moving it off a pure primary is normally enough to clear the ramp cleanly (see the ratio threshold in the docstring). Prefer this when a small color tweak is acceptable and you want the artwork sitting directly on the slide surface with no visible box.
- If you do not own the source, or the vivid color is deliberate and must not change (a brand color, a reused figure): do not strip it at all. Use `.plate` instead -- see "A third path: plate it instead of stripping or leaving it white" below. This is also the better default for vivid/saturated artwork generally, independent of the fringe issue: a plate does not touch the pixels, so there is nothing to get wrong.

Caveat -- enclosed white regions: by default every white-ish pixel is stripped, including white fully enclosed by artwork (the inside of a letter O, a white-filled box in a diagram). If the source relies on that interior white staying solid, add `--keep-largest-region`; it strips only background reachable from the image border and leaves enclosed white pixels opaque. Render both variants and inspect before choosing; either can be correct depending on the source. This flag adds a full-image flood fill on top of the normal pass; budget for it on photo-scale sources (about 4.5-4.7s without it versus roughly 15-20s with it, measured on a 6000x4000 image -- flood-fill cost depends on the background region's boundary complexity, not just pixel count, so treat that as a range rather than a fixed number).

Caveat -- animated GIF: only the first frame is read; the tool prints a warning and drops the rest. Extract the frame you want first if that is not the one you need.

Caveat -- source already has transparency: an input PNG/GIF with its own alpha channel is flattened onto white before background detection (white-detection needs an opaque image to work from), and the original alpha is discarded with a warning. If the source's existing transparency must be preserved as-is, this tool is the wrong one for it.

Batch mode accepts a directory or a glob:

```bash
python3 template/scripts/make_transparent.py 'raw/*.png' -o assets/figures --tolerance 10
```

The script never modifies the input and refuses to overwrite an existing output without `--force`.

#### A third path: plate it instead of stripping or leaving it white

Stripping and plating are not always interchangeable, even for artwork that would otherwise qualify for stripping. Measured case: a clean black-ink line-art diagram, transparent, on a dark profile's near-black surface -- WCAG contrast of the ink against the surface comes out around 1.1-1.2:1, effectively invisible, because stripping the background does nothing to the ink color itself. That is not a defect in `make_transparent.py` (it is proven clean: no white halo, no residual brightness) -- it is a property of black ink on a dark surface that transparency alone cannot fix.

That measurement is also why plating is now the default for any transparent artwork, not a special-case fix reached for only after a contrast failure is caught. Transparent art has no background of its own -- it inherits whatever slide surface it lands on -- and the failure above is profile-dependent: the same asset measures roughly 1.1-1.2:1 against `origami` and `blueprint` (both dark-toned surfaces) but 19.7:1 against `movement` (a light surface). An author who builds and checks a deck against one profile, then later switches profiles, gets no warning that their transparent art has gone illegible. Give every transparent PNG `.plate` by default -- whether it started transparent or was just produced by `make_transparent.py` above -- and treat leaving one unplated as a deliberate, checked opt-out, not the baseline.

`.plate` puts a light backing card behind the untouched artwork instead:

```markdown
![Architecture diagram.](assets/figures/architecture-transparent.png){.plate #fig-architecture}
```

```css
.plate img,
.plate video {
  padding: 0.5em 0.6em;
  border-radius: var(--sinew-radius, 6px);
  background: var(--sinew-plate, color-mix(in srgb, white 88%, var(--sinew-accent) 12%));
}
```

Note the selector targets the media element, not `.plate` itself: Pandoc attaches `.plate` to the outer figure wrapper, which also contains the caption, and backing that wrapper directly was tried and rejected -- verified illegible pale-caption-on-pale-plate on a dark profile before this was scoped to the image/video only.

`--sinew-plate` is never a literal white: it is mixed from the active color profile's own `--sinew-accent`, so every profile gets a distinct, palette-derived plate automatically, with no per-profile file to edit -- the same "derive it from this profile's palette, never generic white" rule the dark-profile `.institution-lockup` plate already follows for logos (`--sinew-logo-plate`), just mixed toward white instead of toward ink so the result stays reliably light on both dark-toned and light-toned profiles. A profile may still set `--sinew-plate` directly for a hand-tuned value.

`.plate` is the default for transparent artwork, not a conditional fix reached for only when contrast measurably fails. Apply it whenever:

- (the default case) the artwork is transparent, full stop -- do not wait to measure a contrast failure before adding `.plate`; the point of the default is to remove the trap of a profile switch nobody re-checked;
- the artwork's own ink/line color is low contrast against the active profile's surface once transparent (measured, not assumed -- check the actual profile, not just "dark profiles in general") -- this is the strongest single justification if the default is ever questioned;
- the source should not be touched at all (see the two bullets above under "Use a light plate ... instead");
- the artwork uses very saturated or vivid ink close to a pure primary color and you do not want to (or cannot) mute it -- `make_transparent.py` can leave a partial fringe on that class of ink for a proven, single-pixel-color reason (see the caveat above), and a plate sidesteps it entirely by never touching the pixels.

Skip `.plate` only as a deliberate opt-out: the artwork is meant to sit directly on the slide surface with no visible box, and it has been checked against the profile actually in use (not just the profile happening to be rendered at the time) and confirmed to contrast comfortably there.

## SciencePlots and Matplotlib

Install reproducibly:

```bash
python -m pip install -r requirements-plotting.txt
```

SciencePlots 2.x requires an explicit import. Layer styles from general to specific, with Sinew last:

```python
from pathlib import Path

import matplotlib.pyplot as plt
import scienceplots

ROOT = Path(__file__).resolve().parents[1]
STYLE = "origami"  # Match the deck's one selected color-* profile.
plt.style.use([
    "science",
    "no-latex",
    "notebook",
    "bright",
    str(ROOT / "styles/matplotlib/sinew-slides.mplstyle"),
    str(ROOT / f"styles/matplotlib/sinew-{STYLE}.mplstyle"),
])

fig, ax = plt.subplots(figsize=(10, 5.5), constrained_layout=True)
ax.plot(x, ours, marker="o", label="Proposed")
ax.plot(x, baseline, marker="s", linestyle="--", label="Baseline")
ax.set(xlabel="Training steps", ylabel="Success rate (%)")
ax.legend(frameon=False)
fig.savefig(ROOT / "assets/figures/result.svg")
```

`science + ieee` targets paper-column width and publication typography. It is not a projected-slide style. `notebook` plus the common Sinew overlay gives projected dimensions; the final per-style overlay supplies surfaces, ink, grid, legend, and data-cycle colors. Adapt final figure size to the slide.

The committed overlay uses 18 pt base/axis labels, 16 pt ticks/legend, 2.5 pt lines, 8 pt markers, TrueType PDF text (`pdf.fonttype: 42`), and SVG glyph paths for deterministic appearance. These are Sinew defaults, not conference mandates.

For editable/searchable SVG text, use `svg.fonttype: none` only when fonts are available or embedded on the presentation machine. Matplotlib documents that path mode is more consistent across machines but not editable. For Korean/CJK, explicitly add Noto Sans CJK/Source Han Sans and run a glyph test; SciencePlots' legacy CJK helpers are deprecated.

### Match figures to the selected visual style

Static figures do not automatically inherit Reveal CSS. Choose one of these reproducible policies:

1. Use a neutral white plot surface that meets contrast in every deck.
2. Export the figure with the overlay matching the deck's one selected `color-*` profile.
3. Generate SVG from a shared palette manifest, preserving the exact token mapping.

Do not make a plot transparent unless every text, grid, and data color remains legible on the selected background.

Sinew provides one overlay per style:

- `sinew-origami.mplstyle`
- `sinew-paper.mplstyle`
- `sinew-high-contrast.mplstyle`
- `sinew-blueprint.mplstyle`
- `sinew-scholar.mplstyle`
- `sinew-unmasked.mplstyle`
- `sinew-the-give.mplstyle`
- `sinew-the-meeting.mplstyle`
- `sinew-movement.mplstyle`

Use `movement` for the public Sinew style even though its design-source route slug is `motion`.

Generate the repository's same illustrative learning curve in every style with:

```bash
python3 scripts/generate_gallery_plots.py
```

The generator composes Matplotlib `default`, the common projected-slide overlay, and the per-style overlay in that order. Outputs are `assets/figures/gallery-<style>.svg`. They exercise visual integration only: their fictional curves and spread are labeled illustrative and are not evidence. When generating a real result, preserve the selected overlay order but replace the example data and metadata with traceable inputs.

## Tables

Use semantic Markdown/HTML, not an image. Sinew uses an academic booktabs-like treatment: strong top/bottom rules, one header rule, and restrained row separators. Structured result tables add one strong vertical rule before the final `Total` column. Table captions appear above; figure captions appear below.

```markdown
::: {.structured-results .ours-last-2}
| Method | Success (%) $\uparrow$ | Peak force (N) $\downarrow$ | Recovery (%) $\uparrow$ | Total $\uparrow$ |
|:--|--:|--:|--:|--:|
| Behavioral cloning | 61.0 | **8.2** | 49.0 | 55.0 |
| Diffusion policy | 76.0 | 10.8 | 65.0 | 70.0 |
| Ours: contact objective | 82.0 | 9.6 | 74.0 | 78.0 |
| Ours: contact + recovery | **86.0** | 9.1 | **81.0** | **84.0** |

: Illustrative placeholder, not experimental evidence. Fictional metrics over 100 fictional trials per method. Arrows show preferred direction; bold marks the best value per metric. The highlighted final two rows are proposed methods. {#tbl-main}
:::
```

- Keep one header row; avoid nested headers on projected slides.
- Put units in headings.
- Use ASCII LaTeX `$\uparrow$` and `$\downarrow$` to mark higher-is-better and lower-is-better metrics.
- Align numbers by decimal intent and use consistent precision.
- Avoid reporting more precision than measurement/evaluation supports.
- Put `Total` last and wrap the table in `.structured-results` for its strong separator.
- Bold the best value in each metric column and define bold in the caption.
- Put proposed methods in the final contiguous rows, prefix their names with `Ours:`, and select `.ours-last-1`, `.ours-last-2`, `.ours-last-3`, or `.ours-last-4` to highlight them. The text label and caption preserve meaning without color.
- Use a figure instead if the audience should see trend/shape rather than exact values.
- Move full benchmark tables to a vertical appendix slide or handout.

## Captions

Sinew renders the automatic `Figure N` and `Table N` identifier in bold while leaving the descriptive caption at normal weight. Do not type the identifier manually. Put a visible `.algorithm-caption` directly beneath procedural code and inside the same column or container. Start it with `**Algorithm.**`; Sinew renders that source label as a globally numbered, bold `Algorithm N` identifier. State scope, inputs/outputs, and evidence status or provenance. Procedural shell blocks need the same treatment. Both algorithm code and caption use `--sinew-algorithm-font`; it must resolve to genuine monospace type, with ligatures disabled so ASCII sequences are not replaced visually.

Every rendered figure, table, and captioned algorithm supports viewport-filling, profile-aware inspection without visible `Expand` or fullscreen `Close` buttons. Click evidence to open it and click the fullscreen evidence to close it. Focused evidence opens with Enter or Space and closes with Escape. Every evidence type may upscale to the available viewport on ultrawide displays; figures preserve aspect ratio, tables preserve semantic columns, and algorithms preserve wrapped code. Captions scale with the expanded evidence. The expanded view clones the rendered evidence and caption, removes duplicate IDs and code-copy controls, and does not alter the source object.

Reference a figure with native Quarto `@fig-...` syntax and a table with `@tbl-...`. Give each `.algorithm-caption` a stable `#algorithm-...` ID and reference it with `{{< alg algorithm-name >}}`. All three render as automatically labeled hyperlinks with profile-aware hover/focus previews of the original object. Preview clones must rerun KaTeX for dollar-delimited math. Table previews use a wider card and larger table text than prose previews. Activation returns to the original object; fullscreen inspection remains a separate action at the source slide. Never hard-code object numbers in prose.

The inspector is a legibility aid, not an overflow strategy. The original projected object must still fit its slide without scrollbars. Test each evidence type with pointer, Tab, Enter/Space, Escape, and second-click dismissal. Verify absence of visible controls, caption legibility, and scaling at ordinary and ultrawide viewport sizes. Confirm that Reveal navigation does not move while the dialog is open and that the active color profile remains intact.

A strong caption includes:

1. content/metric;
2. task/population/scope;
3. aggregation and uncertainty;
4. number of trials/seeds/samples;
5. source/status when reused, adapted, preliminary, or illustrative.

Examples:

- **Result.** Median task success over 384 evaluation episodes; bands are 95% bootstrap intervals over episodes; one training seed. Simulation only.
- **Adapted from Smith et al. (2025), Fig. 3.** Architecture redrawn; colors and annotations changed. Used under CC BY 4.0.
- **Illustrative placeholder - not evidence.** Replace values and source before release.

## Any embedded object as a real Figure N (E2)

`![Caption](path){#fig-id}` only covers plain images. Video, an animated GIF, and the missing-evidence placeholder below are not Pandoc images, but they still need to land on the exact same `Figure N` sequence as every image figure -- one shared, document-order counter, with `@fig-...` cross-references that resolve to the right number automatically, not a separately maintained count that can drift out of sync.

Quarto's own crossref engine already does this correctly for arbitrary content: wrap the object in a fenced div whose id starts with `fig-`, with the caption as the div's own trailing paragraph, instead of image bracket syntax:

```markdown
::: {#fig-approach-clip}
<video src="assets/media/demo-clip.mp4" muted playsinline loop controls
       poster="assets/media/demo-clip-poster.jpg"></video>

Real-robot insertion attempt, one representative trial. 2x playback.
:::
```

This renders exactly like a native image figure: the same `<figure class="quarto-float quarto-float-fig">` wrapper, the same numbered `figcaption.quarto-float-caption` that Sinew already bolds into `**Figure N**`, and a `@fig-approach-clip` reference anywhere in the deck resolves to the correct live number without any extra markup or runtime renumbering pass. It also means the object automatically gets Sinew's click/Enter-Space/Escape fullscreen inspector, because that inspector already targets every `section.slide figure` generically. Verified: a scratch three-figure deck mixing a plain image figure, a video figure div, and a placeholder figure div numbered them 1, 2, 3 in document order, and every `@fig-...` reference to all three resolved to the matching live number -- see "Verification" in the handoff notes for the exact render checked.

The same pattern applies to a GIF (`<img src="assets/media/demo-loop.gif">` inside the div) and to the missing-evidence placeholder documented below. Do not hand-write a `Figure N:` prefix in any of these captions; Sinew generates it the same way it does for image figures.

## Robotics video

- Label real/simulation, playback speed, controller/policy, task, and evaluation condition.
- Show representative failures when they qualify the claim.
- Keep experimental sound only when informative and explain it.
- Caption speech and provide a transcript for released recordings.
- Add `poster` fallback and controls; avoid unpausable autoplay lasting over five seconds.
- Ship local media. Test codec, resolution, seeking, and muted playback offline.
- If `embed-resources: true` fails for MP4 in the target browser, set it to false and serve the deck plus assets over local HTTP.

### The video component

Author a `<video>` by hand inside a `#fig-` div, as shown above -- there is no shortcode. Sinew's runtime drives playback from Reveal's own slide-enter/slide-leave events, not the browser's native `autoplay` attribute: native autoplay fires the instant the page loads, so a clip on a slide the audience has not reached yet is already finished by the time they see it. Concretely:

- On slide enter: seeks to the trim start (see below, default 0) and plays, unless opted out.
- On slide leave: pauses and seeks back to the trim start, so the next entry starts fresh instead of resuming mid-clip or showing a frozen last frame.

Defaults and options, all ordinary HTML on the `<video>` element:

| Attribute | Default behavior | Opt out |
|:--|:--|:--|
| `muted playsinline loop controls` | autoplay on slide entry, muted, inline (no fullscreen takeover on mobile), loops, native controls visible | omit `loop` for a one-shot clip |
| autoplay-on-entry | on | `data-sinew-autoplay="false"` for manual start only |
| sound | off (`muted`) | omit `muted` for sound on -- **warning:** browsers block unmuted autoplay outside a direct user gesture, so an unmuted video entered by Reveal navigation (not a click) will not start playing on its own; it stays paused with its visible controls for the viewer to start manually. Do not rely on unmuted autoplay working. |
| `poster` | none | set to a still frame; see the black-frame-0 trap below |

### Trim window: optional start and end, looping between them (sinew-6lb.5)

`data-sinew-start` and `data-sinew-end` are both optional and independent (seconds, floating point). Set one, both, or neither:

```html
<video src="assets/media/demo-clip.mp4" muted playsinline loop controls
       data-sinew-start="1" data-sinew-end="4"></video>
```

This is how an author shows an excerpt without cutting the source file, which is what makes the "ship local media, never trim the file" rule practical. The runtime seeks to `data-sinew-start` on slide entry and, via a `timeupdate` listener, seeks back to `data-sinew-start` whenever playback reaches `data-sinew-end` -- a real loop between the two bounds, not just a starting offset. This is a JS-driven loop rather than a `#t=start,end` Media Fragment URL: fragment end-point support is inconsistent across browsers, so the `timeupdate` handler is the authoritative mechanism; a `#t=` fragment on the `src` is still fine to add for a no-JS fallback (print/PDF export) but is not required.

A zoomed clip (below) keeps the same trim window: the fullscreen clone gets its own `timeupdate` handler with the same bounds, so opening/closing the inspector never drops or shifts the excerpt.

### Zooming a video (E3, sinew-6lb.1)

A video figure gets the exact same click-to-open, Enter/Space-from-focus, Escape-to-close, click-fullscreen-content-to-close contract as every other figure -- with one adjustment specific to video: a click that lands on the `<video>` element itself (its native control bar, its play/pause hit area) does not trigger zoom, only a click elsewhere in the figure does (its caption, its padding). This is deliberate: `controls` are on by default, and a control-free zoom gesture must not fight the viewer's ability to scrub or pause the clip with its own controls.

Playback semantics settled for zoom, because there is no browser-native behavior to fall back on (a cloned `<video>` does not carry over its source's current playback position or listeners): the fullscreen clone picks up the original video's current timestamp and play/paused state -- **continuing at the same timestamp**, not restarting -- and the original pauses for as long as the dialog is open, so only one copy is ever decoding or audible. Closing the dialog hands state back the other way: the clone's final timestamp and play/paused state are written back to the original slide video, so playback resumes seamlessly instead of jumping back to wherever it was when the zoom opened. Reveal navigation is suppressed for the whole time the dialog is open (same mechanism already used for every other evidence type), so the audience cannot accidentally advance slides while a zoomed clip is playing.

### Native resolution always (sinew-6lb.4)

No `object-fit: cover`, no fixed-ratio padded box, no letterbox bars, no cropping, for video, GIF, or image alike -- the same `object-fit: contain` plus auto width/height rule that already keeps image figures at native aspect ratio (see "Figures, sizing, and captions" in `authoring.md`) applies identically to `<video>`, on the slide and inside the fullscreen inspector. Tested against the deliberately non-standard `demo-clip.mp4` (848x480, not 16:9 or 4:3) and `demo-loop.gif` (240x160): both render at their own aspect ratio with no bars and no crop, at ordinary and ultrawide viewport widths.

### Traps that cost a real deck (sinew-6lb.3)

- **MPEG-4 Part 2 renders as a black rectangle in every current browser.** `ffprobe -show_streams clip.mp4` and check `codec_name=mpeg4` with `profile=Simple Profile` -- that is the failure signature. Re-encode to H.264 with `+faststart`:

  ```bash
  ffmpeg -i input.mp4 -c:v libx264 -pix_fmt yuv420p -movflags +faststart -c:a aac output.mp4
  ```

  `demo-clip.mp4` in `template/assets/media/` is a worked example of a correctly encoded clip (`codec_name=h264`, `pix_fmt=yuv420p`, `+faststart`); see `template/assets/media/README.md` for its exact `ffprobe` output.

- **Frame 0 is black in many simulator recordings.** Pick a `poster` from a frame at or after roughly t = 1s, never frame 0, and verify visually:

  ```bash
  ffmpeg -ss 1.5 -i clip.mp4 -frames:v 1 -update 1 -q:v 3 poster.jpg
  ```

  `demo-clip.mp4` is deliberately built this way (black through t < 1s, real content from t = 1s) specifically so this trap has a fixture to test against; `demo-clip-poster.jpg` is its correctly chosen t = 1.5s poster.

- **`embed-resources: true` turns a remote embed into a dead snapshot.** It base64-inlines local files correctly, but an `<iframe>` or similar remote embed gets inlined as a frozen `data:text/html` snapshot of whatever it fetched at render time -- not a live embed. Mark any element that must stay a live remote fetch with `data-external="1"` so the render step knows to leave it alone (or set `embed-resources: false` and ship the deck as a directory instead).

- **Test the rendered deck over HTTP, not `file://`.** A `file://` open produced a plugin/console error for video playback that did not reproduce once the same build was served over local HTTP (`python3 -m http.server` from the render output directory, or Quarto's own preview server). Treat a `file://` smoke test as insufficient for any slide with a video, GIF, or other embedded media; verify over HTTP before signing off.

## Missing evidence placeholder (E5, sinew-80f.1)

`.missing-evidence` marks a slide's evidence slot as intentionally, visibly unfilled instead of leaving a blank space or reaching for a plausible-looking stand-in number -- the same truthfulness discipline as the illustrative-placeholder labels below, made impossible to mistake for real evidence rather than merely labeled as not-evidence in caption prose.

It is authored as the same kind of figure div as video and GIF above, so it is a full citizen of the shared `Figure N` sequence: it gets a real number, a `#fig-` id, `@fig-...` cross-references, and the fullscreen inspector, exactly like any other figure.

```markdown
::: {#fig-recovery-ablation}
::: {.missing-evidence}
Contact-recovery ablation pending re-run after sensor recalibration.

Tracking: SINEW-4821
:::

What this figure will show once the re-run completes: recovery rate
versus perturbation magnitude, compared against the current policy.
:::
```

Sinew injects the "MISSING EVIDENCE" label as real text (not CSS-generated content, which some assistive tech does not expose) directly above whatever reason/tracking-id text the author writes inside `.missing-evidence`. Three independent, non-color signals keep it unmistakable for real evidence in every visual profile and in grayscale: a dashed border (shape), a diagonal hatch fill (pattern/texture, not a flat tint), and the label text itself -- never color alone. Keep the reason short and specific (what is missing and why), and include a tracking id when one exists so a reviewer can follow up.

## Truthfulness gate

Illustrative values are labeled in the starter. An agent must never replace them with plausible numbers, reconstruct missing uncertainty, or infer experimental settings. Stop and request the evidence or mark the slide preliminary/missing.
