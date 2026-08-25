#!/usr/bin/env python3
"""Check core CSS token contrast pairs against WCAG-oriented thresholds."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STYLES = (
    "origami",
    "paper",
    "high-contrast",
    "blueprint",
    "scholar",
    "unmasked",
    "the-give",
    "the-meeting",
    "movement",
)


def channel(value: int) -> float:
    normalized = value / 255
    return normalized / 12.92 if normalized <= 0.04045 else ((normalized + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    value = hex_color.removeprefix("#")
    red, green, blue = (int(value[index : index + 2], 16) for index in (0, 2, 4))
    return 0.2126 * channel(red) + 0.7152 * channel(green) + 0.0722 * channel(blue)


def contrast(first: str, second: str) -> float:
    high, low = sorted((luminance(first), luminance(second)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def main() -> int:
    failures: list[str] = []
    for style in STYLES:
        source = (ROOT / f"styles/colors/{style}.css").read_text(encoding="utf-8")
        tokens = dict(re.findall(r"(--sinew-[\w-]+):\s*(#[0-9a-fA-F]{6})", source))
        pairs = (
            ("ink", "--sinew-ink", "--sinew-bg", 4.5),
            ("muted text", "--sinew-muted", "--sinew-bg", 4.5),
            ("accent text", "--sinew-accent", "--sinew-bg", 4.5),
            ("danger text", "--sinew-danger", "--sinew-bg", 4.5),
            ("success text", "--sinew-success", "--sinew-bg", 4.5),
            ("strong rules", "--sinew-line-strong", "--sinew-bg", 3.0),
        )
        print(f"{style}:")
        for label, foreground, background, minimum in pairs:
            ratio = contrast(tokens[foreground], tokens[background])
            print(f"  {label:14} {ratio:.2f}:1 (minimum {minimum:.1f}:1)")
            if ratio < minimum:
                failures.append(f"{style} {label}: {ratio:.2f}:1 < {minimum:.1f}:1")
        for index in range(1, 6):
            token = f"--sinew-data-{index}"
            ratio = contrast(tokens[token], tokens["--sinew-panel"])
            print(f"  data-{index}/panel {ratio:.2f}:1 (minimum 3.0:1)")
            if ratio < 3.0:
                failures.append(f"{style} data-{index}/panel: {ratio:.2f}:1 < 3.0:1")

    if failures:
        print("Contrast check failed:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("Contrast check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
