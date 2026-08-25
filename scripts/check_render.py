#!/usr/bin/env python3
"""Check essential properties in a rendered, self-contained Reveal deck."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("usage: check_render.py HTML [COLOR]", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"rendered HTML not found: {path}", file=sys.stderr)
        return 1

    html = path.read_text(encoding="utf-8")
    errors: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require('navigationMode: "grid"' in html or "navigationMode: 'grid'" in html, "Reveal grid navigation is absent")
    require("--sinew-color-profile:" in html, "color profile marker is absent")
    require("{{< include" not in html, "an include shortcode was not resolved")
    require("openai" not in html.lower(), "unexpected injected provider text found")

    deck = (ROOT / "deck.qmd").read_text(encoding="utf-8")
    includes = re.findall(r"^\{\{<\s+include\s+([^ >]+)\s*>\}\}$", deck, re.MULTILINE)
    expected_level1 = sum(Path(include).name == "_00-section.qmd" for include in includes)
    expected_level2 = len(includes) - expected_level1

    level1 = re.findall(
        r'<section\b[^>]*class="[^"]*\blevel1\b[^"]*\bsection-slide\b[^"]*"[^>]*>',
        html,
    )
    level2 = re.findall(
        r'<section\b[^>]*class="[^"]*\bslide\s+level2\b[^"]*"[^>]*>',
        html,
    )
    require(
        len(level1) == expected_level1,
        f"expected {expected_level1} horizontal stack dividers, found {len(level1)}",
    )
    require(
        len(level2) == expected_level2,
        f"expected {expected_level2} vertical content slides, found {len(level2)}",
    )
    require(
        not re.search(r'<section class="slide level2">\s*(?:<!--.*?-->\s*)?</section>', html, re.DOTALL),
        "blank content slide detected before first stack",
    )
    require(
        not re.search(r'<section\b[^>]*class="[^"]*\bslide\s+level2\b[^"]*\bstack\b', html),
        "content panels created an accidental nested Reveal stack",
    )
    require(html.count('class="algorithm-caption"') == 18, "expected two algorithm captions in every style column")
    require("numberAlgorithmCaptions" in html, "automatic algorithm numbering script is absent")

    if len(sys.argv) == 3:
        color = sys.argv[2]
        require(
            f'--sinew-color-profile: "{color}"' in html,
            f"expected color marker {color}",
        )

    if '--sinew-gallery: "runtime"' in html:
        require(
            "sinewGalleryStyle" in html and 'window.Reveal.on("slidechanged"' in html,
            "runtime gallery style switcher is absent",
        )
        for preview in (
            "origami",
            "paper",
            "high-contrast",
            "blueprint",
            "scholar",
            "unmasked",
            "the-give",
            "the-meeting",
            "movement",
        ):
            require(
                f'data-style-preview="{preview}"' in html,
                f"gallery style column marker is absent: {preview}",
            )

    if errors:
        print(f"Render check failed for {path}:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(f"Render check passed: {path}")
    print(f"  horizontal_stacks={len(level1)} vertical_content_slides={len(level2)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
