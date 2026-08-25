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
    expected_style_columns = max(expected_level1 - 1, 0)
    bibliography_source = (ROOT / "references.bib").read_text(encoding="utf-8")
    bibliography_keys = set(re.findall(r"^@[A-Za-z]+\{([^,]+),", bibliography_source, re.MULTILINE))
    cited_keys: list[str] = []
    for include in includes:
        source_path = ROOT / include
        if source_path.is_file():
            source_keys = re.findall(r"@([A-Za-z0-9_.:+#$/-]+)", source_path.read_text(encoding="utf-8"))
            cited_keys.extend(key for key in source_keys if key in bibliography_keys)

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
    require(
        html.count('class="algorithm-caption"') == 2 * expected_style_columns,
        "expected two algorithm captions in every style column",
    )
    require(
        html.count('class="research-questions"') == expected_style_columns,
        "expected one Q1-Q9 research-question list in every style column",
    )
    require(
        html.count('class="research-hypotheses"') == expected_style_columns,
        "expected one H1-H9 research-hypothesis list in every style column",
    )
    highlighted_statements = re.findall(r'<li\b[^>]*class="[^"]*\bis-highlighted\b[^"]*"', html)
    require(
        len(highlighted_statements) == 2 * expected_style_columns,
        "expected one highlighted question and hypothesis in every style column",
    )
    require(
        html.count('class="institution-lockup"') == expected_level1,
        "expected one affiliation lockup on every divider slide",
    )
    require(
        len(re.findall(r'id="algorithm-gallery-[^"]+-(?:method|render)"', html)) == 2 * expected_style_columns,
        "expected stable IDs on both algorithms in every style column",
    )
    require(
        len(re.findall(r'<a\b[^>]*class="quarto-xref"', html)) == 2 * expected_style_columns,
        "expected one figure and one table cross-reference in every style column",
    )
    require(
        len(re.findall(r'<a\b[^>]*\bsinew-algorithm-reference\b', html)) == expected_style_columns,
        "expected one algorithm reference in every style column",
    )
    require(
        len(re.findall(r'<a\b[^>]*\bsinew-reference-question\b', html)) == expected_style_columns,
        "expected one Q reference in every style column",
    )
    require(
        len(re.findall(r'<a\b[^>]*\bsinew-reference-hypothesis\b', html)) == expected_style_columns,
        "expected one H reference in every style column",
    )
    require(
        html.count('class="math inline"') >= 4 * expected_style_columns,
        "expected dollar-delimited table metric directions",
    )
    require(
        "window.katex" in html and "katex.render" in html,
        "expected Quarto's KaTeX browser runtime",
    )
    require("numberAlgorithmCaptions" in html, "automatic algorithm numbering script is absent")
    require("installInstitutionLockups" in html, "all-slide affiliation runtime is absent")
    require("labelResearchStatements" in html, "accessible Q/H identifier script is absent")
    require("wireSinewReferences" in html, "internal reference routing script is absent")
    require("buildQuartoCrossReferencePreview" in html, "figure/table reference preview script is absent")
    require("registerReferencePreview" in html, "profile-aware internal reference preview script is absent")
    require("buildEvidenceInspector" in html, "fullscreen evidence inspector script is absent")
    require("clickClosesEvidence" in html, "click-to-close evidence inspector is absent")
    require("typesetClonedMath" in html, "cloned preview math typesetting is absent")
    require('dialog.id = "sinew-evidence-inspector"' in html, "fullscreen evidence dialog is absent")
    citation_links = re.findall(r'<a\b[^>]*\brole="doc-biblioref"', html)
    require(
        len(citation_links) == len(cited_keys),
        f"expected {len(cited_keys)} linked in-slide citations, found {len(citation_links)}",
    )
    require(
        html.count('class="csl-entry"') == len(set(cited_keys)),
        f"expected {len(set(cited_keys))} unique bibliography entries",
    )
    require('class="references csl-bib-body hanging-indent"' in html, "citeproc bibliography is absent")
    require("references-slide" in html, "styled references slide is absent")
    require(
        html.count('class="style-references"') == expected_style_columns,
        "expected one local references container in every style column",
    )
    require("buildStyleBibliographies" in html, "local citation routing script is absent")
    require(
        "window.document.querySelectorAll('a[role=\"doc-biblioref\"]')" in html,
        "interactive citation preview script is absent",
    )
    core_candidates = list(ROOT.glob("_extensions/**/theme/core.scss"))
    require(bool(core_candidates), "Sinew core theme source is absent")
    if core_candidates:
        core = core_candidates[0].read_text(encoding="utf-8")
        require(
            '.tippy-box[data-theme~="light-border"]' in core,
            "profile-aware citation hover styling is absent",
        )
        require(
            ".sinew-reference-preview" in core and ".sinew-reference-hypothesis" in core,
            "profile-aware internal reference styling is absent",
        )
        require(
            '[data-theme~="sinew-table"]' in core,
            "large table-reference preview styling is absent",
        )

    requested_mode = sys.argv[2] if len(sys.argv) == 3 else None
    if requested_mode and requested_mode != "gallery":
        require(
            f'--sinew-color-profile: "{requested_mode}"' in html,
            f"expected color marker {requested_mode}",
        )

    gallery_runtime = '--sinew-gallery: "runtime"' in html
    if requested_mode == "gallery":
        require(gallery_runtime, "zero-config render did not activate the runtime gallery")

    gallery_profile_count = 0
    if gallery_runtime:
        require(
            "sinewGalleryStyle" in html and 'window.Reveal.on("slidechanged"' in html,
            "runtime gallery style switcher is absent",
        )
        profile_names = {
            profile.stem.removeprefix("_quarto-color-")
            for profile in ROOT.glob("_quarto-color-*.yml")
        }
        gallery_profile_count = len(profile_names)
        require(
            len(profile_names) == expected_style_columns,
            "the zero-config gallery does not contain one column per color profile",
        )
        for preview in sorted(profile_names):
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
    if gallery_runtime:
        print(f"  zero_config_gallery_profiles={gallery_profile_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
