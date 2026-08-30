#!/usr/bin/env python3
"""Convert a raster image to PNG and strip its white background to alpha.

Behaviour target: https://remove-white-background.imageonline.co/ (a single
tolerance knob that turns near-white pixels transparent, source image
otherwise unmodified). This script never touches the input file; it always
writes a new PNG at an explicit output path.

Dependencies: Pillow only (stdlib otherwise). Pillow is intentionally kept
optional for the deck as a whole -- install it with:

    python3 -m pip install -r template/requirements-imaging.txt

Alpha formula
-------------
For every pixel, compute two things from its RGB channels:

    d = 255 - min(r, g, b)                  (distance from pure white)
    spread = max(r, g, b) - min(r, g, b)    (distance from gray/neutral)

`d` is 0 for pure white and grows for any colored or dark pixel. `spread` is
0 for a perfectly neutral pixel (r == g == b: white, gray, or black) and
grows for a hued one.

`--tolerance` (0-100) sets a background cutoff:

    cutoff = tolerance / 100 * 255

Pixels at or below the cutoff are fully transparent (background), including
an off-white or JPEG-noisy canvas that never quite hits exact 255. Above the
cutoff, alpha ramps linearly up to fully opaque, over a feather band whose
WIDTH depends on a saturation RATIO, not on spread alone and not on
tolerance:

    ratio = spread / max(d, 1)

    feather(ratio) = FEATHER_WIDE    if ratio <= RATIO_LOW
    feather(ratio) = FEATHER_NARROW  if ratio >= RATIO_HIGH
    feather(ratio) = linear interpolation between the two, in between

    alpha(d, ratio) = 0        if d <= cutoff
    alpha(d, ratio) = 255      if d >= cutoff + feather(ratio)
    alpha(d, ratio) = round((d - cutoff) * 255 / feather(ratio))  otherwise

Why ratio, not spread alone
------------------------------
An earlier version of this gate used bare `spread` (see git history / task
report for the superseded SPREAD_LOW/SPREAD_HIGH constants). It fixed
antialiasing on NEUTRAL ink but reproduced the original white-fringe defect
on COLORED ink: a blue or red disc, antialiased the same way as the neutral
case below, left 200+ boundary pixels fully opaque at colors far paler than
the true ink at every documented tolerance -- e.g. (198, 208, 242) at
composited luminance 208.6 against a true ink luminance of 61.6, a visible
pale-lavender halo on a dark slide.

The reason: bare `spread` grows to nearly its full value very early in a
saturated ink's blend (a ink whose channels drop at different rates reaches
high `spread` well before it reaches high `d`), so the "is this pale
content or a fading edge" gate mistook a still-fading saturated-ink pixel
for deliberate pale content and switched to a narrow feather. The RATIO
`spread / d` is close to constant along any single ink's straight blend
line from white to full ink (both grow together), so it does not have this
early-spread problem: it stays low for less-saturated inks (matplotlib's
default blue, ratio ~0.67; a typical "web blue" #0066CC, ratio ~0.8) and
only approaches 1 for a NEARLY OR FULLY saturated ink (one channel at or
near 0), or for a genuinely pale, hue-only pixel like pale yellow
(255, 255, 200), which also has ratio 1 (both d and spread equal 55 there).

RATIO_LOW=0.85, RATIO_HIGH=0.99, FEATHER_WIDE=160, and FEATHER_NARROW=16
were chosen by sweeping candidate thresholds against a continuous
white-to-ink blend for five ink saturations (matplotlib blue #1F77B4, web
blue #0066CC, a moderate blue (30,60,220), a vivid blue (10,30,240), and
pure blue (0,0,255)), plus pale yellow/cyan preservation and the solid dark
no-background/JPEG-black cases, at every documented tolerance. Measured
result on the actual antialiased blue/red discs: worst-case fringe
composite luminance dropped from roughly 188-222 (bare-spread gate) to
roughly 67-118 across tolerance 5-25 -- a large, verified improvement, not
a full fix; see "Known residual limitations" below for what is left.

Solid, clearly dark or saturated content (a photo's dark region, a filled
logo) is unaffected: its distance from white is far beyond any
tolerance-plus-feather combination in the documented tolerance range, so it
always lands past the ramp at alpha 255.

Known residual limitations
------------------------------
Two distinct, bounded residuals remain, both inherent to any model that
looks at one pixel's color in isolation (no neighboring-pixel information):

1. Near-maximally-saturated ink (ratio close to or at 1 -- a pure or
   near-pure primary color such as (0, 0, 255)) is mathematically
   indistinguishable, at the single-pixel level, from deliberately authored
   pale content of a matching hue: both can produce the identical (d,
   spread) pair. Pale yellow (255, 255, 200) and a 21.6%-covered pure-blue
   antialiasing pixel (200, 200, 255) have exactly the same d=55, spread=55,
   ratio=1 -- there is no per-pixel test that tells them apart, since one
   genuinely must stay opaque (pale yellow, on the reviewer's own verified
   requirement) and the other genuinely must fade. Given that conflict,
   this tool keeps pale-content preservation (the documented, tested
   requirement) and accepts that a purely or nearly saturated ink's
   antialiasing residue still shows a partial, reduced fringe (see the
   measured luminance range above for pure blue/red, which stays close to
   the pre-fix numbers since ratio=1 always selects FEATHER_NARROW). This
   is not a bug to tune away: it is unavoidable without spatial or
   neighborhood reasoning (recognizing that genuine antialiasing forms a
   1-3px monotonic transition between two flat plateaus, which a
   deliberately authored solid pale fill does not) -- out of scope here.
   If a source uses fully saturated primary-color line art and the residual
   fringe is visible, mute the ink color slightly before stripping (ratio
   well under 0.85 clears the ramp cleanly), or use the light-plate
   approach instead (see template/docs/figures-and-tables.md).
2. Independent of color, a small number of moderately-covered NEUTRAL
   boundary pixels (mid-gray, not pale -- brightest measured survivor had
   min channel 82 out of 255) still round to fully opaque at low tolerance
   on the measured antialiased-disc case, fading out gradually as tolerance
   rises and disappearing entirely only around tolerance 40, past the
   documented range. Genuinely pale survivors (min channel > 140) are fully
   eliminated at every tolerance from 5 to 40 on the same case -- this
   residual is a moderate-gray edge staying a little too solid, not the
   reported near-white halo. FEATHER_WIDE cannot be widened further to
   close this gap without eroding the no-background/JPEG-black-preservation
   margin at the high end of the documented tolerance range; see the task
   report for the tradeoff data.

Color decontamination
----------------------
An antialiased or JPEG-noisy edge pixel is itself a blend of the ink color
and the white background it sat on, so simply adding alpha to it still
leaves a pale, washed-out edge (a "white halo") once it is composited onto
a dark slide. Each partially transparent pixel is un-premultiplied against
white to recover the underlying ink color, using a COVERAGE ESTIMATE
derived from `d` alone, decoupled from the display alpha:

    coverage = d / 255
    channel' = clamp(255 + (channel - 255) / coverage, 0, 255)

This assumes the darkest achievable ink channel is 0 (i.e. recovers toward
whatever primary/near-black color the observed blend is most consistent
with); it is exact for genuinely black or maximally saturated ink and a
reasonable default otherwise, since the true ink color cannot be recovered
from a single flattened pixel without more information (see "Known
residual limitations" above). This formula is provably always in [0, 255]
for any input -- see the derivation in the task report -- so the clamp
should never actually trigger on ordinary input; it is kept as a safety net
and a warning is printed (with a count) if it ever does, since that would
mean the estimate broke down for that image.

An earlier version used the DISPLAY alpha (the tolerance-and-feather-ramped
value) as the coverage estimate instead of `d`. That is wrong: display
alpha has cutoff subtracted from it for opacity purposes, and dividing by
that smaller, offset quantity here over-corrects the recovered color past
the valid range, silently relying on the clamp to paper over it. Measured
bug: a neutral gray(80)-to-white gradient (a stand-in for a soft drop
shadow) decontaminated to solid black past its midpoint at tolerance 15,
with pre-clamp values going as low as -13.5 -- not float noise, a genuine
formula error. Using `d` directly instead of the display alpha removes the
error by construction rather than by clamping around it.

Enclosed white regions
-----------------------
By default every pixel within tolerance of white becomes transparent,
including white fully enclosed by artwork (the inside of a letter "O", a
white-filled box in a diagram). Pass --keep-largest-region to protect those:
a flood fill (8-connected) runs from the image border through
background-candidate pixels only; only pixels reachable from the border are
made transparent, and enclosed background-colored pixels are forced back to
fully opaque so they render as solid white. The default is OFF because most
callers stripping a background want every white pixel gone (the common
"logo on white" case has no enclosed white to protect); turn it on when the
artwork uses white fill as a deliberate interior color and punching through
it would look wrong.

Other input handling
----------------------
- EXIF orientation (common on camera JPEGs) is applied on load, so a
  sideways or upside-down photo is processed and saved the way it displays,
  not the way the raw buffer is stored.
- If the source already has transparency (an alpha channel, or a GIF/PNG
  "transparency" palette entry), it is flattened onto a white canvas before
  background detection, since white-detection needs an opaque RGB image to
  work from. This discards the original alpha; a warning is printed to
  stderr when it happens. If the source's existing transparency should be
  preserved instead of re-derived, this tool is the wrong one to use on it.
- An animated GIF is only ever read on its first frame; a warning is
  printed to stderr and the remaining frames are silently unused.
- The script refuses to write the output on top of the input path, even
  with --force, since "never modifies the input" must hold unconditionally.

Performance
-----------
--keep-largest-region adds a full-image flood fill on top of the per-pixel
ramp and decontamination pass. On a 6000x4000 photo-scale source, the plain
pass measured consistently around 4.5-4.7s across repeated runs. With
--keep-largest-region, measurements varied by source and machine: about
14.6-14.9s across three repeated runs here, and roughly 20s reported
independently on different content -- flood-fill cost depends on the
background region's boundary complexity, not just pixel count, so treat
15-20s as the budget on photo-scale sources rather than a single number.
"""

from __future__ import annotations

import argparse
import glob
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    from PIL import Image, ImageChops, ImageFilter, ImageOps
except ImportError:
    print(
        "make_transparent.py requires Pillow, which is not installed.\n"
        "Install it with:\n"
        "    python3 -m pip install -r template/requirements-imaging.txt\n"
        "Pillow is optional for the deck itself; only this script needs it.",
        file=sys.stderr,
    )
    raise SystemExit(1)


RASTER_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff", ".gif"}
NEIGHBOR_OFFSETS = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))

# Feather-width gating by saturation ratio (spread relative to distance, not
# spread alone); see "Alpha formula" in the module docstring for what these
# mean and how they were chosen.
RATIO_LOW = 0.85
RATIO_HIGH = 0.99
FEATHER_WIDE = 160
FEATHER_NARROW = 16

# Decontamination is spatially gated: only pixels within this many pixels
# (8-connected / chebyshev distance) of a fully-transparent pixel are
# un-premultiplied against white. See "Color decontamination" in the module
# docstring for why, and the task report for the measurement this value is
# derived from: on the vjepa2-abstract-new.png worked example, every
# genuine antialiasing residual pixel measured (the documented curved
# z-circle boundary pixel, and every other non-fill red-hued
# partially-transparent pixel belonging to the same box) sits at chebyshev
# distance 1-3 from the nearest fully-transparent pixel, while all but 4 of
# 1629 pale-pink interior fill pixels sit at distance 4 or more (the
# distribution has a hard gap: no fill pixel at distance 2 or 3 at all).
# Radius 3 catches the former population and spares the latter.
DECONTAMINATION_RADIUS = 3


def feather_for_ratio(spread: int, distance: int) -> float:
    """Ramp width for a pixel with the given spread/distance saturation ratio."""
    ratio = spread / max(distance, 1)
    if ratio <= RATIO_LOW:
        return FEATHER_WIDE
    if ratio >= RATIO_HIGH:
        return FEATHER_NARROW
    fraction = (ratio - RATIO_LOW) / (RATIO_HIGH - RATIO_LOW)
    return FEATHER_WIDE + (FEATHER_NARROW - FEATHER_WIDE) * fraction


def build_alpha_lut_2d(cutoff: float) -> list[list[int]]:
    """Build the [distance][spread] -> alpha lookup table for a background cutoff.

    Distance <= cutoff is fully transparent (background). Above the cutoff,
    alpha ramps linearly up to fully opaque over a feather band whose width
    depends on the spread/distance saturation ratio (see feather_for_ratio)
    -- never snapping a pixel to opaque before its feather band ends. See
    "Alpha formula" in the module docstring.
    """
    lut: list[list[int]] = []
    for distance in range(256):
        row = []
        for spread in range(256):
            if distance <= cutoff:
                row.append(0)
                continue
            feather = feather_for_ratio(spread, distance)
            full_opacity_point = cutoff + feather
            if distance >= full_opacity_point:
                row.append(255)
            else:
                row.append(min(255, round((distance - cutoff) * 255.0 / feather)))
        lut.append(row)
    return lut


def distance_and_spread(rgb_image: "Image.Image") -> tuple["Image.Image", "Image.Image"]:
    """Return mode-L images of d = 255 - min(r, g, b) and spread = max - min."""
    red, green, blue = rgb_image.split()
    max_image = ImageChops.lighter(ImageChops.lighter(red, green), blue)
    min_image = ImageChops.darker(ImageChops.darker(red, green), blue)
    distance_image = ImageChops.invert(min_image)
    spread_image = ImageChops.subtract(max_image, min_image)
    return distance_image, spread_image


def compute_raw_alpha(
    distance_image: "Image.Image", spread_image: "Image.Image", lut2d: list[list[int]]
) -> "Image.Image":
    """Look up alpha for every pixel from its (distance, spread) pair."""
    distance_data = distance_image.getdata()
    spread_data = spread_image.getdata()
    alpha_data = [lut2d[distance][spread] for distance, spread in zip(distance_data, spread_data)]
    result = Image.new("L", distance_image.size)
    result.putdata(alpha_data)
    return result


def flood_fill_reachable(candidate_bytes: bytes, width: int, height: int) -> bytearray:
    """Mark background-candidate pixels reachable from the image border."""
    visited = bytearray(width * height)
    queue: deque[int] = deque()

    def seed(index: int) -> None:
        if candidate_bytes[index] and not visited[index]:
            visited[index] = 1
            queue.append(index)

    for x in range(width):
        seed(x)
        seed((height - 1) * width + x)
    for y in range(height):
        seed(y * width)
        seed(y * width + (width - 1))

    while queue:
        index = queue.popleft()
        y, x = divmod(index, width)
        for dx, dy in NEIGHBOR_OFFSETS:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                neighbor = ny * width + nx
                if candidate_bytes[neighbor] and not visited[neighbor]:
                    visited[neighbor] = 1
                    queue.append(neighbor)

    return visited


def protect_enclosed_regions(
    raw_alpha: "Image.Image", width: int, height: int
) -> "Image.Image":
    """Force alpha back to 255 on background-colored pixels not reachable from the border."""
    alpha_bytes = raw_alpha.tobytes()
    candidate_bytes = bytes(0 if value == 255 else 255 for value in alpha_bytes)
    reachable = flood_fill_reachable(candidate_bytes, width, height)
    protect = bytes(
        255 if candidate_bytes[index] and not reachable[index] else 0
        for index in range(width * height)
    )
    protect_mask = Image.frombytes("L", (width, height), protect)
    opaque = Image.new("L", (width, height), 255)
    return Image.composite(opaque, raw_alpha, protect_mask)


def build_near_background_mask(alpha_image: "Image.Image", radius: int) -> "Image.Image":
    """Return a mode-L mask, 255 within `radius` (chebyshev) of a fully-transparent
    pixel, 0 elsewhere.

    A square `(2*radius + 1)`-wide max-filter over the "is this pixel fully
    transparent" mask is exactly one round of 8-connected dilation by
    `radius` -- the same neighborhood `NEIGHBOR_OFFSETS`/flood-fill use
    elsewhere in this file, just computed in one pass instead of a BFS. See
    `DECONTAMINATION_RADIUS` for why 3 is the right radius, and "Color
    decontamination" in the module docstring for why this mask exists.
    """
    background = alpha_image.point(lambda value: 255 if value == 0 else 0)
    size = 2 * radius + 1
    return background.filter(ImageFilter.MaxFilter(size))


def decontaminate(
    rgb_image: "Image.Image",
    alpha_image: "Image.Image",
    distance_image: "Image.Image",
    source_path: Path,
) -> "Image.Image":
    """Un-premultiply edge-pixel colors against a white matte.

    Uses a coverage estimate derived from `distance_image` (d / 255), NOT
    from the display alpha -- the display alpha has a tolerance-controlled
    cutoff subtracted from it for opacity purposes, and dividing by that
    offset quantity here over-corrects colors past the valid range. d / 255
    is provably always in [0, 1], so the recovered channel is always in
    [0, 255] with no clamping needed on ordinary input; see "Color
    decontamination" in the module docstring. The clamp stays as a safety
    net, but triggering it is now unexpected, so it is counted and reported.

    This is spatially gated (see `build_near_background_mask` and
    `DECONTAMINATION_RADIUS`): only a partially-transparent pixel within
    `DECONTAMINATION_RADIUS` of an actual fully-transparent pixel is
    un-premultiplied. A partially-transparent pixel far from any
    fully-transparent pixel was never actually composited against the
    background -- its fractional alpha comes entirely from the tolerance
    ramp reading its own color as insufficiently far from white, not from a
    real white/ink blend -- so treating it as a faded edge and reconstructing
    it toward saturated ink is wrong; its source color is left untouched.
    """
    rgb_data = rgb_image.getdata()
    alpha_data = alpha_image.getdata()
    distance_data = distance_image.getdata()
    near_background_data = build_near_background_mask(
        alpha_image, DECONTAMINATION_RADIUS
    ).getdata()
    output = []
    clamp_hits = 0
    for (red, green, blue), alpha, distance, near_background in zip(
        rgb_data, alpha_data, distance_data, near_background_data
    ):
        if alpha == 0 or alpha == 255 or not near_background:
            output.append((red, green, blue))
            continue
        coverage = distance / 255.0
        new_pixel = []
        for channel in (red, green, blue):
            raw = 255 + (channel - 255) / coverage
            rounded = round(raw)
            # Compare the ROUNDED value, not the raw float: this formula is
            # provably in [0, 255] up to float noise on the order of 1e-14,
            # which rounds to a valid integer on its own. Only count a clamp
            # hit when rounding still lands outside the valid range -- that
            # is the real signal that the coverage estimate broke down.
            if rounded < 0 or rounded > 255:
                clamp_hits += 1
            new_pixel.append(min(255, max(0, rounded)))
        output.append(tuple(new_pixel))
    if clamp_hits:
        print(
            f"warning: {source_path}: decontamination clamp triggered on {clamp_hits} "
            "channel value(s); the coverage estimate may be inaccurate for this image",
            file=sys.stderr,
        )
    result = Image.new("RGB", rgb_image.size)
    result.putdata(output)
    return result


def flatten_existing_alpha(image: "Image.Image", source_path: Path) -> "Image.Image":
    """Composite any existing transparency onto white before background detection."""
    if image.mode in ("RGBA", "LA") or "transparency" in image.info:
        print(
            f"warning: {source_path}: existing transparency was flattened onto white "
            "before background detection; the original alpha channel is discarded",
            file=sys.stderr,
        )
        image = image.convert("RGBA")
        background = Image.new("RGBA", image.size, (255, 255, 255, 255))
        image = Image.alpha_composite(background, image)
    return image.convert("RGB")


def warn_if_animated(image: "Image.Image", source_path: Path) -> None:
    if getattr(image, "is_animated", False) and getattr(image, "n_frames", 1) > 1:
        print(
            f"warning: {source_path}: animated image ({image.n_frames} frames); "
            "only the first frame is processed, the rest are dropped",
            file=sys.stderr,
        )


def make_transparent(
    source_path: Path, tolerance: float, keep_largest_region: bool
) -> "Image.Image":
    """Load one raster image and return an RGBA image with white stripped to alpha."""
    if not 0.0 <= tolerance <= 100.0:
        raise ValueError(f"tolerance must be within 0..100, got {tolerance}")

    cutoff = tolerance / 100.0 * 255.0
    lut2d = build_alpha_lut_2d(cutoff)

    with Image.open(source_path) as opened:
        opened.load()
        warn_if_animated(opened, source_path)
        oriented = ImageOps.exif_transpose(opened)
        rgb_image = flatten_existing_alpha(oriented, source_path)

    width, height = rgb_image.size
    distance_image, spread_image = distance_and_spread(rgb_image)
    raw_alpha = compute_raw_alpha(distance_image, spread_image, lut2d)

    if keep_largest_region:
        final_alpha = protect_enclosed_regions(raw_alpha, width, height)
    else:
        final_alpha = raw_alpha

    decontaminated_rgb = decontaminate(rgb_image, final_alpha, distance_image, source_path)
    result = decontaminated_rgb.convert("RGBA")
    result.putalpha(final_alpha)
    return result


def resolve_inputs(input_arg: str) -> tuple[list[Path], bool]:
    """Resolve the input argument to a list of files, and whether it is a batch."""
    path = Path(input_arg)
    if path.is_dir():
        files = sorted(
            candidate
            for candidate in path.iterdir()
            if candidate.is_file() and candidate.suffix.lower() in RASTER_EXTENSIONS
        )
        return files, True

    matches = sorted(Path(match) for match in glob.glob(input_arg, recursive=True))
    matches = [match for match in matches if match.is_file()]
    if matches and (len(matches) > 1 or any(character in input_arg for character in "*?[")):
        return matches, True

    if path.is_file():
        return [path], False

    return [], False


def resolve_output_path(output_dir: Path, source: Path) -> Path:
    return output_dir / (source.stem + ".png")


def process_one(
    source: Path,
    destination: Path,
    tolerance: float,
    keep_largest_region: bool,
    force: bool,
) -> None:
    if source.resolve() == destination.resolve():
        raise ValueError(
            f"refusing to write output over the input file (even with --force): {source}"
        )
    if destination.exists() and not force:
        raise FileExistsError(
            f"refusing to overwrite existing file without --force: {destination}"
        )
    result = make_transparent(source, tolerance, keep_largest_region)
    destination.parent.mkdir(parents=True, exist_ok=True)
    result.save(destination, format="PNG")
    print(f"wrote {destination} ({result.width}x{result.height}, RGBA)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="make_transparent.py",
        description=(
            "Convert a raster image to PNG and strip its white background to "
            "transparency, with a graded alpha ramp so antialiased edges do "
            "not keep a white fringe."
        ),
        epilog=(
            "Examples:\n"
            "  python3 template/scripts/make_transparent.py logo.jpg "
            "-o template/assets/figures/logo.png --tolerance 15\n"
            "  python3 template/scripts/make_transparent.py 'raw/*.png' "
            "-o out_dir --tolerance 10 --keep-largest-region\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "input",
        help=(
            "Source image path, a directory of raster images (batch mode), "
            "or a glob pattern such as 'raw/*.jpg' (batch mode)."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        help=(
            "Output PNG path for a single input, or an output directory when "
            "input resolves to more than one file. Always explicit; never "
            "derived from the input name."
        ),
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=12.0,
        help=(
            "How far from pure white still counts as background, as a "
            "percentage of the 0-255 channel range (0-100). 0 removes only "
            "exact (255, 255, 255) pixels; higher values widen the graded "
            "alpha ramp and catch more near-white pixels. Clean vector/PNG "
            "line art, including antialiased edges: 5-15. Lossy JPEG "
            "sources (compression pushes white down to roughly 240-254): "
            "10-25, higher for noisier compression. Do not go far past "
            "25-30. Default: 12."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing output file. Refused by default.",
    )
    parser.add_argument(
        "--keep-largest-region",
        dest="keep_largest_region",
        action="store_true",
        help=(
            "Protect white pixels enclosed inside the artwork (the inside of "
            "a letter O, a white-filled box) from being punched through: "
            "only background-colored pixels reachable from the image border "
            "are made transparent. Off by default, so an enclosed white "
            "region is stripped along with the rest of the background; turn "
            "this on when white interior fill must stay solid."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not 0.0 <= args.tolerance <= 100.0:
        parser.error(f"--tolerance must be within 0..100, got {args.tolerance}")

    sources, is_batch = resolve_inputs(args.input)
    if not sources:
        parser.error(f"no raster input matched: {args.input}")

    output_arg = Path(args.output)

    if is_batch:
        if output_arg.exists() and not output_arg.is_dir():
            parser.error(f"--output must be a directory for batch input: {output_arg}")
        if not output_arg.exists() and output_arg.suffix.lower() in RASTER_EXTENSIONS:
            parser.error(
                f"--output looks like a file ({output_arg}) but input resolved to "
                f"{len(sources)} file(s); pass a directory for batch input"
            )
        failures = 0
        for source in sources:
            destination = resolve_output_path(output_arg, source)
            try:
                process_one(
                    source, destination, args.tolerance, args.keep_largest_region, args.force
                )
            except (FileExistsError, OSError, ValueError) as error:
                print(f"error: {source}: {error}", file=sys.stderr)
                failures += 1
        if failures:
            print(f"{failures} of {len(sources)} file(s) failed", file=sys.stderr)
            return 1
        return 0

    source = sources[0]
    try:
        process_one(source, output_arg, args.tolerance, args.keep_largest_region, args.force)
    except (FileExistsError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
