#!/usr/bin/env python3
"""Generate synthetic demo media assets for the v1.2.0 gallery slides.

Every asset under `template/assets/media/` is synthesized locally by this
script: no image, photo, clip, or logo is downloaded or copied in from a
third party. Everything is drawn with Pillow (plus the stdlib `random` and
`math` modules) or produced by shelling out to ffmpeg on frame sources this
script generates itself.

Outputs:

- demo-diagram.png            clean line-art block-and-arrow pipeline on
                               white, the kind of figure make_transparent.py
                               is meant to process.
- demo-diagram-transparent.png  the same diagram after running it through
                               `template/scripts/make_transparent.py`.
- demo-photo.jpg               a synthetic raster "photograph" (gradient +
                               grain + fiducial-like blobs) standing in for
                               a camera frame.
- demo-clip.mp4                a short H.264 clip at a deliberately
                               non-standard resolution, with a black first
                               second (frame 0 included) before content
                               starts, matching a real recorder artifact
                               this asset set exists to catch.
- demo-clip-poster.jpg         a poster frame pulled from demo-clip.mp4 at
                               t >= 1s (never frame 0, which is black).
- demo-loop.gif                a small looping animated GIF at a resolution
                               different from the mp4's.

Every random source below is seeded through local `random.Random(seed)`
instances (never the shared global `random` state), so running this
script twice produces byte-identical files. Frame generation is pure
Pillow: gradients are built from small 1-D ramps and expanded with
`Image.resize`, per-pixel noise comes from `random.Random.randbytes` fed
through `Image.frombytes`, and phase-dependent color mapping is done with
a 256-entry `Image.point` lookup table (the only per-pixel-shaped math,
sin/cos included, ever costs 256 evaluations, not width*height). ffmpeg is
used only to encode/mux/extract, and every ffmpeg command is printed
before it runs.

Dependencies: Pillow (see template/requirements-imaging.txt) and the
ffmpeg/ffprobe binaries -- nothing else; matching `make_transparent.py`,
numpy/matplotlib are deliberately not used. The script exits with a clear
message instead of a traceback if Pillow or ffmpeg is missing.
"""

from __future__ import annotations

import argparse
import math
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "assets/media"
MAKE_TRANSPARENT = ROOT / "scripts/make_transparent.py"

SEED = 20260830

FPS = 24
VIDEO_SIZE = (848, 480)   # non-standard: not 1920x1080 or 1280x720
GIF_SIZE = (240, 160)     # non-standard, and distinct from VIDEO_SIZE
BLACK_SECONDS = 1.0
CONTENT_SECONDS = 4.0

# Chosen empirically against the current (spread-gated feather) make_transparent.py
# by sweeping tolerance 5..25 on demo-diagram.png and measuring, for each value:
# (a) alpha==255 pixels whose source color is still near-white (min channel >= 200)
#     -- the specific "pale halo stuck opaque" bug this tool was reworked to fix:
#     zero at every tolerance tested, 5 through 25;
# (b) alpha==255 pixels in the documented residual mid-gray band (90 <= min < 200,
#     mostly title-text antialiasing at y=33-38) -- 144 px at tolerance 5, 33 px at
#     8, 0 px at 10 and every value tested above it.
# 12 is comfortably above the empirical clearing point (10) while staying inside
# the tool's documented "clean vector/PNG line art" band (5-15). See
# template/assets/media/README.md for the full sweep table and the dark/light
# composite luminance proof.
DIAGRAM_TOLERANCE = 12.0

try:
    from PIL import Image, ImageChops, ImageDraw, ImageFont
except ImportError:
    print(
        "generate_demo_media.py requires Pillow, which is not installed.\n"
        "Install it with:\n"
        "    python3 -m pip install -r template/requirements-imaging.txt",
        file=sys.stderr,
    )
    raise SystemExit(1)


def require_ffmpeg() -> None:
    missing = [tool for tool in ("ffmpeg", "ffprobe") if shutil.which(tool) is None]
    if missing:
        print(
            "generate_demo_media.py requires "
            + " and ".join(missing)
            + " on PATH, and none was found.\n"
            "Install ffmpeg (which provides ffprobe) and re-run.",
            file=sys.stderr,
        )
        raise SystemExit(1)


def run(cmd: list[str]) -> None:
    """Run a subprocess command, printing it first for reproducibility."""
    print("+ " + " ".join(cmd))
    subprocess.run(cmd, check=True)


MONOSPACE_CANDIDATES = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
    "/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf",
)


def load_mono_font(size: int) -> "ImageFont.FreeTypeFont | ImageFont.ImageFont":
    for candidate in MONOSPACE_CANDIDATES:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


# --------------------------------------------------------------------------
# demo-diagram.png: clean line-art block-and-arrow pipeline
# --------------------------------------------------------------------------

PIPELINE_STAGES = ("CAMERA", "ENCODER", "POLICY NET", "ACTUATOR", "ROBOT ARM")


def draw_arrow(
    draw: "ImageDraw.ImageDraw",
    start: tuple[int, int],
    end: tuple[int, int],
    width: int = 3,
    head: int = 10,
) -> None:
    draw.line([start, end], fill="black", width=width)
    dx, dy = end[0] - start[0], end[1] - start[1]
    length = max((dx * dx + dy * dy) ** 0.5, 1e-6)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    tip = end
    left = (end[0] - ux * head + px * head * 0.6, end[1] - uy * head + py * head * 0.6)
    right = (end[0] - ux * head - px * head * 0.6, end[1] - uy * head - py * head * 0.6)
    draw.polygon([tip, left, right], fill="black")


def make_diagram(path: Path) -> None:
    width, height = 1200, 480
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    label_font = load_mono_font(18)
    caption_font = load_mono_font(15)

    box_w, box_h = 170, 90
    mid_y = 170
    gap = (width - len(PIPELINE_STAGES) * box_w) // (len(PIPELINE_STAGES) + 1)

    centers: list[tuple[int, int]] = []
    x = gap
    for stage in PIPELINE_STAGES:
        top_left = (x, mid_y - box_h // 2)
        bottom_right = (x + box_w, mid_y + box_h // 2)
        draw.rectangle([top_left, bottom_right], outline="black", width=3)
        text_bbox = draw.textbbox((0, 0), stage, font=label_font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        center = (x + box_w // 2, mid_y)
        draw.text(
            (center[0] - text_w // 2, center[1] - text_h // 2 - text_bbox[1]),
            stage,
            fill="black",
            font=label_font,
        )
        centers.append(center)
        x += box_w + gap

    for (cx1, _), (cx2, _) in zip(centers[:-1], centers[1:]):
        start = (cx1 + box_w // 2, mid_y)
        end = (cx2 - box_w // 2, mid_y)
        draw_arrow(draw, start, end)

    feedback_y = mid_y + box_h // 2 + 110
    last_cx = centers[-1][0]
    first_cx = centers[0][0]
    down_from = (last_cx, mid_y + box_h // 2)
    down_to = (last_cx, feedback_y)
    left_to = (first_cx, feedback_y)
    up_to = (first_cx, mid_y + box_h // 2)

    draw.line([down_from, down_to], fill="black", width=3)
    draw.line([down_to, left_to], fill="black", width=3)
    draw_arrow(draw, left_to, up_to)

    caption = "STATE FEEDBACK"
    caption_bbox = draw.textbbox((0, 0), caption, font=caption_font)
    caption_w = caption_bbox[2] - caption_bbox[0]
    mid_x = (first_cx + last_cx) // 2
    draw.text(
        (mid_x - caption_w // 2, feedback_y - 26),
        caption,
        fill="black",
        font=caption_font,
    )

    title = "FIG. DEMO PIPELINE (SYNTHETIC, FOR MEDIA-CONTRACT DEMO ONLY)"
    title_font = load_mono_font(16)
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((width - title_w) // 2, 30), title, fill="black", font=title_font)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG")


def make_diagram_transparent(source: Path, destination: Path) -> None:
    if destination.exists():
        destination.unlink()
    run(
        [
            sys.executable,
            str(MAKE_TRANSPARENT),
            str(source),
            "-o",
            str(destination),
            "--tolerance",
            str(DIAGRAM_TOLERANCE),
            "--force",
        ]
    )


# --------------------------------------------------------------------------
# Shared pure-Pillow gradient/noise/vignette helpers
# --------------------------------------------------------------------------


def lerp_color(start: tuple[float, ...], end: tuple[float, ...], t: float) -> tuple[int, ...]:
    return tuple(int(round(a + (b - a) * t)) for a, b in zip(start, end))


def vertical_gradient(
    width: int, height: int, stops: list[tuple[float, tuple[int, int, int]]]
) -> "Image.Image":
    """A width x height RGB image that varies only by row, per piecewise-linear stops.

    `stops` is a list of (t, color) pairs with t in [0, 1], non-decreasing.
    Two consecutive stops sharing the same t produce a hard seam (used here
    for the horizon line). Built as a 1-pixel-wide column (one lerp per row,
    O(height) Python) and expanded to full width with a native resize.
    """
    column = Image.new("RGB", (1, height))
    pixels = column.load()
    for y in range(height):
        t = y / (height - 1) if height > 1 else 0.0
        for (t0, color0), (t1, color1) in zip(stops, stops[1:]):
            if t0 <= t <= t1:
                local_t = 0.0 if t1 == t0 else (t - t0) / (t1 - t0)
                pixels[0, y] = lerp_color(color0, color1, local_t)
                break
    return column.resize((width, height))


def seeded_noise_plane(seed: int, width: int, height: int) -> "Image.Image":
    """A width x height L image of uniform 0..255 noise from a seeded RNG."""
    data = random.Random(seed).randbytes(width * height)
    return Image.frombytes("L", (width, height), data)


def compress_to_signed_band(plane: "Image.Image", amplitude: int) -> "Image.Image":
    """Remap a 0..255 L plane onto 128 +/- amplitude via a 256-entry LUT.

    Combine the result with a base image using
    `ImageChops.add(base, banded, scale=1.0, offset=-128)`, which yields
    `base + (banded - 128)`, i.e. base plus a small signed delta -- without
    attenuating base the way a naive `ImageChops.add(base, noise, scale=k)`
    would (that divides *both* operands by k, not just the noise term).
    """
    span = 2 * amplitude
    lut = [128 + round((value - 127.5) / 255.0 * span) for value in range(256)]
    return plane.point(lut)


def radial_vignette(width: int, height: int, floor: float = 0.55, falloff: float = 0.35) -> "Image.Image":
    """An RGB image whose value encodes a 0..255 multiplier for ImageChops.multiply."""
    plane = Image.new("L", (width, height))
    pixels = plane.load()
    cx, cy = (width - 1) / 2.0, (height - 1) / 2.0
    max_radius = math.hypot(cx, cy)
    for y in range(height):
        dy = (y - cy) / max_radius
        for x in range(width):
            dx = (x - cx) / max_radius
            radius = math.hypot(dx, dy)
            multiplier = 1.0 - falloff * max(radius - 0.25, 0.0)
            multiplier = min(1.0, max(floor, multiplier))
            pixels[x, y] = round(multiplier * 255)
    return Image.merge("RGB", (plane, plane, plane))


# --------------------------------------------------------------------------
# demo-photo.jpg: synthetic raster "photograph"
# --------------------------------------------------------------------------


def make_photo(path: Path) -> None:
    width, height = 640, 480

    # Sky-to-ground gradient: cool gray-blue above a horizon, warmer below.
    horizon = 0.55
    sky_top = (60, 74, 96)
    sky_bottom = (146, 158, 172)
    ground_top = (94, 88, 78)
    ground_bottom = (48, 44, 40)
    base = vertical_gradient(
        width,
        height,
        [(0.0, sky_top), (horizon, sky_bottom), (horizon, ground_top), (1.0, ground_bottom)],
    )

    # Sensor grain: seeded noise, compressed to a small signed band, added
    # without attenuating the base gradient underneath it.
    noise = seeded_noise_plane(SEED, width, height)
    banded = compress_to_signed_band(noise, amplitude=10)
    banded_rgb = Image.merge("RGB", (banded, banded, banded))
    grained = ImageChops.add(base, banded_rgb, scale=1.0, offset=-128)

    # Vignette.
    vignette = radial_vignette(width, height)
    image = ImageChops.multiply(grained, vignette)

    draw = ImageDraw.Draw(image)
    blob_specs = [
        (0.30, 0.62, 26, (196, 64, 58)),
        (0.52, 0.58, 20, (74, 158, 96)),
        (0.70, 0.66, 30, (214, 178, 64)),
    ]
    for fx, fy, radius_px, color in blob_specs:
        cx_px, cy_px = fx * width, fy * height
        draw.ellipse(
            [cx_px - radius_px, cy_px - radius_px, cx_px + radius_px, cy_px + radius_px],
            fill=color,
            outline=(20, 20, 20),
            width=2,
        )

    label_font = load_mono_font(16)
    draw.text((16, 16), "SYNTHETIC FRAME (DEMO ONLY)", fill=(240, 240, 240), font=label_font)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    image.save(path, format="JPEG", quality=85, optimize=True)


# --------------------------------------------------------------------------
# demo-clip.mp4: black frame 0, content from t=1s, non-standard resolution
# --------------------------------------------------------------------------


def diagonal_ramp(width: int, height: int) -> "Image.Image":
    """An L image encoding (x_norm + y_norm) / 2 * 255, built from two 1-D ramps.

    A width-tall row ramp and a height-tall column ramp are each built with
    an O(width)/O(height) Python loop, expanded to full size with a native
    resize (constant along the other axis, so the resize is exact), and
    combined with ImageChops.add(scale=2.0) to average them -- no
    width*height Python loop involved.
    """
    row = Image.new("L", (width, 1))
    row_pixels = row.load()
    for x in range(width):
        row_pixels[x, 0] = round((x / (width - 1)) * 255) if width > 1 else 0
    row_full = row.resize((width, height))

    column = Image.new("L", (1, height))
    column_pixels = column.load()
    for y in range(height):
        column_pixels[0, y] = round((y / (height - 1)) * 255) if height > 1 else 0
    column_full = column.resize((width, height))

    return ImageChops.add(row_full, column_full, scale=2.0)


def sweep_color_luts(phase: float) -> tuple[list[int], list[int], list[int]]:
    """Per-channel 256-entry LUTs mapping a diagonal_ramp value to a warm/teal color.

    The sin wave (a per-frame constant-cost 256-point table, not a
    width*height computation) drives a teal<->amber blend tied to `phase`.
    """
    teal = (32.0, 96.0, 104.0)
    amber = (196.0, 120.0, 40.0)
    luts: tuple[list[int], list[int], list[int]] = ([], [], [])
    for value in range(256):
        fraction = value / 255.0
        wave = 0.5 + 0.5 * math.sin(2 * math.pi * (fraction - phase * 1.3))
        for channel in range(3):
            mixed = teal[channel] * (1 - wave) + amber[channel] * wave
            luts[channel].append(int(round(mixed)))
    return luts


def render_video_frame(index: int, ramp: "Image.Image", size: tuple[int, int]) -> "Image.Image":
    width, height = size
    t = index / FPS

    if t < BLACK_SECONDS:
        return Image.new("RGB", size, "black")

    content_t = t - BLACK_SECONDS
    content_span = max(CONTENT_SECONDS, 1e-6)
    phase = min(1.0, max(0.0, content_t / content_span))

    # Deterministic warm-to-teal diagonal sweep tied to phase.
    red_lut, green_lut, blue_lut = sweep_color_luts(phase)
    base = Image.merge(
        "RGB",
        (ramp.point(red_lut), ramp.point(green_lut), ramp.point(blue_lut)),
    )

    # Per-frame seeded grain so it looks like a live sensor, not a flat gradient.
    noise = seeded_noise_plane(SEED + index, width, height)
    banded = compress_to_signed_band(noise, amplitude=8)
    banded_rgb = Image.merge("RGB", (banded, banded, banded))
    image = ImageChops.add(base, banded_rgb, scale=1.0, offset=-128)

    draw = ImageDraw.Draw(image)
    # A moving marker square, deterministic function of phase.
    marker_size = 46
    margin = marker_size
    cx = margin + phase * (width - 2 * margin)
    cy = height / 2 + 60 * math.sin(2 * math.pi * phase)
    draw.rectangle(
        [cx - marker_size / 2, cy - marker_size / 2, cx + marker_size / 2, cy + marker_size / 2],
        fill=(240, 240, 240),
        outline=(20, 20, 20),
        width=3,
    )

    label_font = load_mono_font(16)
    draw.text((16, 16), "SYNTHETIC CLIP (DEMO ONLY)", fill=(250, 250, 250), font=label_font)

    return image


def make_video(path: Path) -> None:
    total_frames = int(round((BLACK_SECONDS + CONTENT_SECONDS) * FPS))
    ramp = diagonal_ramp(*VIDEO_SIZE)

    with tempfile.TemporaryDirectory(prefix="sinew-demo-clip-") as tmp:
        tmp_dir = Path(tmp)
        for index in range(total_frames):
            frame = render_video_frame(index, ramp, VIDEO_SIZE)
            frame.save(tmp_dir / f"frame_{index:04d}.png", format="PNG")

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        if path.exists():
            path.unlink()
        run(
            [
                "ffmpeg",
                "-y",
                "-framerate",
                str(FPS),
                "-i",
                str(tmp_dir / "frame_%04d.png"),
                "-frames:v",
                str(total_frames),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-crf",
                "28",
                "-preset",
                "medium",
                "-movflags",
                "+faststart",
                "-an",
                str(path),
            ]
        )


def make_poster(video_path: Path, poster_path: Path) -> None:
    if poster_path.exists():
        poster_path.unlink()
    run(
        [
            "ffmpeg",
            "-y",
            "-ss",
            "1.5",
            "-i",
            str(video_path),
            "-frames:v",
            "1",
            "-update",
            "1",
            "-q:v",
            "3",
            str(poster_path),
        ]
    )


# --------------------------------------------------------------------------
# demo-loop.gif: small looping animation, resolution distinct from the mp4
# --------------------------------------------------------------------------


def render_gif_frame(index: int, frame_count: int, size: tuple[int, int]) -> "Image.Image":
    width, height = size
    image = Image.new("RGB", size, (18, 22, 30))
    draw = ImageDraw.Draw(image)

    phase = index / frame_count
    angle = 2 * math.pi * phase
    cx, cy = width / 2, height / 2
    orbit_radius = min(width, height) * 0.30
    dot_radius = 12

    dot_x = cx + orbit_radius * math.cos(angle)
    dot_y = cy + orbit_radius * math.sin(angle)

    draw.ellipse(
        [cx - orbit_radius - dot_radius, cy - orbit_radius - dot_radius,
         cx + orbit_radius + dot_radius, cy + orbit_radius + dot_radius],
        outline=(90, 100, 120),
        width=2,
    )
    draw.ellipse(
        [dot_x - dot_radius, dot_y - dot_radius, dot_x + dot_radius, dot_y + dot_radius],
        fill=(230, 150, 60),
        outline=(255, 255, 255),
        width=2,
    )

    label_font = load_mono_font(12)
    draw.text((8, 8), "DEMO LOOP", fill=(220, 220, 220), font=label_font)

    return image


def make_gif(path: Path) -> None:
    frame_count = 8
    frames = [render_gif_frame(index, frame_count, GIF_SIZE) for index in range(frame_count)]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    frames[0].save(
        path,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=140,
        loop=0,
        disposal=2,
        optimize=True,
    )


# --------------------------------------------------------------------------

ASSET_NAMES = ("diagram", "diagram-transparent", "photo", "video", "poster", "gif")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help="Directory to write generated assets into (default: template/assets/media).",
    )
    parser.add_argument(
        "--only",
        action="append",
        choices=ASSET_NAMES,
        help=(
            "Regenerate only this asset (repeatable, e.g. --only photo --only gif). "
            "Default: regenerate all six. 'diagram-transparent' requires "
            "demo-diagram.png to already exist on disk if 'diagram' is not also "
            "selected; 'poster' requires demo-clip.mp4 the same way for 'video'. "
            "Use this to avoid disturbing an asset you did not mean to touch -- "
            "each full run overwrites every file, which is how "
            "demo-diagram-transparent.png ended up regenerated by accident against "
            "an in-flux make_transparent.py during v1.2.0 development."
        ),
    )
    args = parser.parse_args(argv)

    require_ffmpeg()

    targets = set(args.only) if args.only else set(ASSET_NAMES)

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    diagram_path = output_dir / "demo-diagram.png"
    diagram_transparent_path = output_dir / "demo-diagram-transparent.png"
    photo_path = output_dir / "demo-photo.jpg"
    video_path = output_dir / "demo-clip.mp4"
    poster_path = output_dir / "demo-clip-poster.jpg"
    gif_path = output_dir / "demo-loop.gif"

    print(f"Generating demo media into {output_dir} (targets: {', '.join(sorted(targets))})")

    written: list[Path] = []

    if "diagram" in targets:
        make_diagram(diagram_path)
        print(f"wrote {diagram_path} ({diagram_path.stat().st_size} bytes)")
        written.append(diagram_path)

    if "diagram-transparent" in targets:
        if not diagram_path.is_file():
            parser.error(
                f"--only diagram-transparent requires {diagram_path} to already "
                "exist; run with --only diagram first (or omit --only)."
            )
        make_diagram_transparent(diagram_path, diagram_transparent_path)
        print(
            f"wrote {diagram_transparent_path} "
            f"({diagram_transparent_path.stat().st_size} bytes)"
        )
        written.append(diagram_transparent_path)

    if "photo" in targets:
        make_photo(photo_path)
        print(f"wrote {photo_path} ({photo_path.stat().st_size} bytes)")
        written.append(photo_path)

    if "video" in targets:
        make_video(video_path)
        print(f"wrote {video_path} ({video_path.stat().st_size} bytes)")
        written.append(video_path)

    if "poster" in targets:
        if not video_path.is_file():
            parser.error(
                f"--only poster requires {video_path} to already exist; run with "
                "--only video first (or omit --only)."
            )
        make_poster(video_path, poster_path)
        print(f"wrote {poster_path} ({poster_path.stat().st_size} bytes)")
        written.append(poster_path)

    if "gif" in targets:
        make_gif(gif_path)
        print(f"wrote {gif_path} ({gif_path.stat().st_size} bytes)")
        written.append(gif_path)

    total_bytes = sum(p.stat().st_size for p in written)
    print(f"Total ({len(written)} file(s) written this run): {total_bytes} bytes "
          f"({total_bytes / (1024 * 1024):.3f} MiB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
