#!/usr/bin/env python3
"""Static validation for the Sinew starter source tree (stdlib only)."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DECK = ROOT / "deck.qmd"
EXTENSION_MANIFEST_CANDIDATES = (
    ROOT / "_extensions/sinew/_extension.yml",
    ROOT / "_extensions/sinew-robotics/sinew/_extension.yml",
)
COLORS = (
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
STYLE_CITATION_KEYS = {
    "origami": "sinewOrigami2026",
    "paper": "sinewPaper2026",
    "high-contrast": "sinewHighContrast2026",
    "blueprint": "sinewBlueprint2026",
    "scholar": "sinewScholar2026",
    "unmasked": "sinewUnmasked2026",
    "the-give": "sinewTheGive2026",
    "the-meeting": "sinewTheMeeting2026",
    "movement": "sinewMovement2026",
}
REQUIRED_TOKENS = (
    "--sinew-bg",
    "--sinew-panel",
    "--sinew-panel-raised",
    "--sinew-ink",
    "--sinew-muted",
    "--sinew-line",
    "--sinew-line-strong",
    "--sinew-accent",
    "--sinew-accent-contrast",
    "--sinew-danger",
    "--sinew-success",
    "--sinew-data-1",
    "--sinew-data-2",
    "--sinew-data-3",
    "--sinew-data-4",
    "--sinew-data-5",
)


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.notes: list[str] = []

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)

    def run(self) -> int:
        self.validate_repository()
        self.validate_profiles()
        self.validate_manifest_and_slides()
        self.validate_styles()

        if self.notes:
            print("Sinew validation notes:")
            for note in self.notes:
                print(f"  - {note}")

        if self.errors:
            print("Sinew validation failed:", file=sys.stderr)
            for error in self.errors:
                print(f"  - {error}", file=sys.stderr)
            return 1

        print("Sinew validation passed.")
        print(f"  styles={len(COLORS)}")
        return 0

    def validate_repository(self) -> None:
        self.require(DECK.is_file(), "deck.qmd is missing")
        ascii_sources = sorted(
            {
                DECK,
                *ROOT.glob("_quarto*.yml"),
                *ROOT.rglob("*.md"),
            }
        )
        for path in ascii_sources:
            if not path.is_file():
                continue
            source = path.read_text(encoding="utf-8")
            non_ascii = sorted({character for character in source if ord(character) > 127})
            self.require(
                not non_ascii,
                f"slide metadata and authoring instructions must use standard-keyboard ASCII in {path}; found {non_ascii}",
            )
        beads = [path for path in ROOT.rglob(".beads") if ".git" not in path.parts]
        self.require(not beads, f".beads must stay outside the template: {beads}")
        extension_path = next((path for path in EXTENSION_MANIFEST_CANDIDATES if path.is_file()), None)
        self.require(extension_path is not None, "extension manifest is missing")
        self.require(
            (ROOT / "docs/agent-templates/AGENTS.template.md").is_file(),
            "copyable AGENTS template is missing",
        )
        self.require(
            (ROOT / "docs/agent-templates/CLAUDE.template.md").is_file(),
            "copyable CLAUDE template is missing",
        )
        self.require((ROOT / "_quarto-gallery.yml").is_file(), "default gallery profile is missing")
        self.require((ROOT / "references.bib").is_file(), "references.bib is missing")
        self.require((ROOT / "_slides/01-intro/_03-citations.qmd").is_file(), "citation example slide is missing")
        self.require((ROOT / "_slides/01-intro/_04-references.qmd").is_file(), "bibliography slide is missing")
        self.require(
            (ROOT / "styles/gallery/gallery.css").is_file(),
            "default gallery marker CSS is missing",
        )
        core_theme = ROOT / "_extensions/sinew/theme/core.scss"
        runtime = ROOT / "_extensions/sinew/theme/captions.html"
        self.require(core_theme.is_file(), "core theme is missing")
        self.require(runtime.is_file(), "post-body runtime is missing")
        if core_theme.is_file():
            core_source = core_theme.read_text(encoding="utf-8")
            for marker in (
                ".research-questions",
                ".research-hypotheses",
                'content: "Q" counter(sinew-research-question)',
                'content: "H" counter(sinew-research-hypothesis)',
                ".sinew-fullscreen-dialog",
            ):
                self.require(marker in core_source, f"core theme is missing required component: {marker}")
        if runtime.is_file():
            runtime_source = runtime.read_text(encoding="utf-8")
            for marker in ("labelResearchStatements", "buildEvidenceInspector", "sinew-evidence-inspector", "showModal"):
                self.require(marker in runtime_source, f"evidence inspector runtime is missing: {marker}")
        legacy_profiles = sorted(ROOT.glob("_quarto-conf-*.yml"))
        self.require(not legacy_profiles, f"conference profiles must not be present: {legacy_profiles}")
        legacy_markers = sorted((ROOT / "styles/conferences").glob("*.css"))
        self.require(not legacy_markers, f"conference marker CSS must not be present: {legacy_markers}")

        if extension_path is not None:
            extension = extension_path.read_text(encoding="utf-8")
            self.require("link-citations: true" in extension, "citation links must be enabled")
            self.require("citations-hover: true" in extension, "citation hover previews must be enabled")

        citation_source = (ROOT / "_slides/01-intro/_03-citations.qmd").read_text(encoding="utf-8")
        reference_source = (ROOT / "_slides/01-intro/_04-references.qmd").read_text(encoding="utf-8")
        bibliography = (ROOT / "references.bib").read_text(encoding="utf-8")
        citation_keys = set(re.findall(r"@([A-Za-z0-9_.:+#$/-]+)", citation_source))
        bibliography_keys = set(re.findall(r"^@[A-Za-z]+\{([^,]+),", bibliography, re.MULTILINE))
        self.require(len(citation_keys) >= 5, "citation example must exercise at least five references")
        self.require(citation_keys <= bibliography_keys, "every example citation key must exist in references.bib")
        self.require(
            set(STYLE_CITATION_KEYS.values()) <= bibliography_keys,
            "every visual profile must have its own bibliography record",
        )
        self.require("{#refs}" in reference_source, "bibliography slide must provide the citeproc #refs target")
        self.require("references-slide" in reference_source, "bibliography slide must activate two-column styling")
        self.require(
            "global-references-slide" in reference_source,
            "shared bibliography must be marked as the global citeproc source",
        )

    def validate_profiles(self) -> None:
        base = (ROOT / "_quarto.yml").read_text(encoding="utf-8")
        expected_names = set(COLORS)
        profile_names = {
            path.stem.removeprefix("_quarto-color-")
            for path in ROOT.glob("_quarto-color-*.yml")
        }
        self.require(
            profile_names == expected_names,
            f"color profile files and registered styles differ: files={sorted(profile_names)} registered={sorted(expected_names)}",
        )
        self.require(
            "default: [gallery, color-origami]" in base,
            "zero-config rendering must activate the gallery and a base color profile",
        )

        gallery = (ROOT / "_quarto-gallery.yml").read_text(encoding="utf-8")
        columns_html = (ROOT / "styles/gallery/columns.html").read_text(encoding="utf-8")
        columns_css = (ROOT / "styles/gallery/columns.css").read_text(encoding="utf-8")
        self.require('gallery-mode: "runtime-style-preview"' in gallery, "gallery runtime metadata is missing")
        self.require("styles/gallery/columns.css" in gallery, "gallery profile does not load column styles")
        self.require("styles/gallery/columns.html" in gallery, "gallery profile does not load column switching")

        for name in COLORS:
            profile_name = f"color-{name}"
            path = ROOT / f"_quarto-{profile_name}.yml"
            self.require(path.is_file(), f"missing color profile: {profile_name}")
            self.require(profile_name in base, f"{profile_name} missing from profile group")
            if path.is_file():
                source = path.read_text(encoding="utf-8")
                self.require(
                    f"styles/colors/{name}.css" in source,
                    f"{profile_name} does not include its color CSS",
                )
            self.require(f'"{name}"' in columns_html, f"gallery switcher does not register {name}")
            self.require(
                f'data-sinew-gallery-style="{name}"' in columns_css,
                f"gallery runtime CSS does not mirror {name}",
            )

    def validate_manifest_and_slides(self) -> None:
        if not DECK.is_file():
            return
        deck = DECK.read_text(encoding="utf-8")
        closing_yaml = deck.find("\n---", 4)
        self.require(deck.startswith("---\n"), "deck.qmd must start with YAML")
        self.require(closing_yaml >= 0, "deck.qmd YAML is not closed")

        includes = re.findall(r"^\{\{<\s+include\s+([^ >]+)\s*>\}\}$", deck, re.MULTILINE)
        self.require(bool(includes), "deck.qmd has no include manifest")
        self.require(len(includes) == len(set(includes)), "deck.qmd includes a slide more than once")

        first_include = deck.find("{{< include")
        if closing_yaml >= 0 and first_include >= 0:
            preamble = deck[closing_yaml + 4 : first_include]
            visible = re.sub(r"<!--.*?-->", "", preamble, flags=re.DOTALL).strip()
            self.require(not visible, "body content before the first include creates an extra slide")

        included_paths = [ROOT / include for include in includes]
        for path in included_paths:
            self.require(path.is_file(), f"included slide does not exist: {path.relative_to(ROOT)}")

        slide_files = sorted((ROOT / "_slides").glob("**/*.qmd"))
        included_resolved = {path.resolve() for path in included_paths if path.exists()}
        orphaned = [path.relative_to(ROOT) for path in slide_files if path.resolve() not in included_resolved]
        self.require(not orphaned, f"slide files are not included: {orphaned}")

        previous_folder: str | None = None
        seen_folders: set[str] = set()
        for path in included_paths:
            if not path.is_file():
                continue
            rel = path.relative_to(ROOT)
            self.require(path.name.startswith("_"), f"included slide must be underscore-prefixed: {rel}")
            self.require("_slides" in path.parts, f"included content is outside _slides: {rel}")
            folder = path.parent.name
            if folder != previous_folder:
                self.require(folder not in seen_folders, f"stack folder is split in the manifest: {folder}")
                seen_folders.add(folder)
                previous_folder = folder

            text = path.read_text(encoding="utf-8")
            self.require(not text.startswith("---\n"), f"included slide contains YAML: {rel}")
            non_ascii = sorted({character for character in text if ord(character) > 127})
            self.require(
                not non_ascii,
                f"slide source must use standard-keyboard ASCII in {rel}; found {non_ascii}",
            )
            headings = re.findall(r"^(#{1,2})\s+(.+)$", text, re.MULTILINE)
            self.require(len(headings) == 1, f"slide must contain exactly one level-1/2 heading: {rel}")
            self.require(
                re.search(r"^#{3,6}\s+", text, re.MULTILINE) is None,
                f"nested headings create nested Reveal sections; use bold labels inside a slide: {rel}",
            )
            if headings:
                expected = "#" if path.name == "_00-section.qmd" else "##"
                self.require(headings[0][0] == expected, f"wrong heading level in {rel}; expected {expected}")
                if expected == "##":
                    title = re.sub(r"\s+\{.*\}\s*$", "", headings[0][1]).strip()
                    self.require(len(title.split()) >= 5, f"content title is too topic-like to be a claim: {rel}")

            self.require(
                not re.search(r"\b(?:TODO|FIXME|TBD)\b", text, re.IGNORECASE),
                f"unresolved TODO/FIXME/TBD in {rel}",
            )
            for phrase in (
                "identical pseudocode",
                "identical data",
                "same claim in every column",
                "shared story",
                "appearance only",
                "matching plot",
            ):
                self.require(
                    phrase not in text.lower(),
                    f"remove gallery-comparison meta-copy from {rel}: {phrase}",
                )

            self.validate_images(path, text)
            self.validate_tables(path, text)
            self.validate_research_lists(path, text)

    def validate_images(self, path: Path, text: str) -> None:
        rel = path.relative_to(ROOT)
        image_pattern = re.compile(r"!\[(.*?)\]\(([^)]+)\)(?:\{([^}]*)\})?", re.DOTALL)
        for caption, target, attrs in image_pattern.findall(text):
            attrs = attrs or ""
            decorative = re.search(r'fig-alt\s*=\s*""', attrs) is not None
            self.require(
                decorative or re.search(r'fig-alt\s*=\s*"[^"]+"', attrs) is not None,
                f"informative image lacks fig-alt in {rel}: {target}",
            )
            self.require(
                decorative or bool(caption.strip()),
                f"informative image lacks a Markdown caption in {rel}: {target}",
            )
            asset = ROOT / target.split("#", 1)[0]
            if not re.match(r"^(?:https?:|data:|/)", target):
                self.require(asset.exists(), f"image asset does not exist in {rel}: {target}")

    def validate_tables(self, path: Path, text: str) -> None:
        rel = path.relative_to(ROOT)
        separator = re.search(r"^\|(?:[^\n]*\|)+\n\|\s*:?-+", text, re.MULTILINE)
        if separator:
            self.require(
                re.search(r"^:\s+.+\{#tbl-[^}]+\}\s*$", text, re.MULTILINE) is not None,
                f"table needs a caption and #tbl- label in {rel}",
            )

    def validate_research_lists(self, path: Path, text: str) -> None:
        rel = path.relative_to(ROOT)
        for list_class, prefix in (("research-questions", "Q"), ("research-hypotheses", "H")):
            pattern = re.compile(
                rf'<ol\b[^>]*class="[^"]*\b{re.escape(list_class)}\b[^"]*"[^>]*>(.*?)</ol>',
                re.DOTALL,
            )
            for body in pattern.findall(text):
                items = re.findall(r"<li\b([^>]*)>(.*?)</li>", body, re.DOTALL)
                self.require(
                    1 <= len(items) <= 9,
                    f"{list_class} must contain one to nine items in {rel}",
                )
                highlighted = sum(
                    re.search(r"\bis-highlighted\b", attributes) is not None
                    for attributes, _ in items
                )
                self.require(
                    highlighted <= 1,
                    f"{list_class} may highlight at most one primary item in {rel}",
                )
                for _, item_body in items:
                    visible = re.sub(r"<[^>]+>", "", item_body).strip()
                    self.require(
                        re.match(rf"{prefix}[1-9]\b", visible, re.IGNORECASE) is None,
                        f"do not type generated {prefix} identifiers into item text in {rel}",
                    )

    def validate_styles(self) -> None:
        for name in COLORS:
            path = ROOT / f"styles/colors/{name}.css"
            self.require(path.is_file(), f"missing color stylesheet: {path.relative_to(ROOT)}")
            if not path.is_file():
                continue
            source = path.read_text(encoding="utf-8")
            for token in REQUIRED_TOKENS:
                self.require(token in source, f"{path.name} missing token {token}")
            self.require(
                f'--sinew-color-profile: "{name}"' in source,
                f"{path.name} missing profile marker",
            )
            self.require(
                (ROOT / f"styles/matplotlib/sinew-{name}.mplstyle").is_file(),
                f"missing Matplotlib style for {name}",
            )
            self.require(
                (ROOT / f"assets/figures/gallery-{name}.svg").is_file(),
                f"missing gallery plot for {name}",
            )

        style_folders = sorted((ROOT / "_slides").glob("[0-9][0-9]-*"))[1:]
        self.require(len(style_folders) == len(COLORS), "the gallery must contain one column per style")
        for name, folder in zip(COLORS, style_folders):
            self.require(folder.name.endswith(name), f"style column order mismatch for {name}: {folder.name}")
            expected_slide_names = {
                "_00-section.qmd",
                "_01-guidelines.qmd",
                "_02-problem.qmd",
                "_03-research.qmd",
                "_03-algorithm.qmd",
                "_04-plot.qmd",
                "_05-table.qmd",
                "_06-conclusion.qmd",
                "_07-generate.qmd",
                "_08-citations.qmd",
                "_09-references.qmd",
            }
            actual_slide_names = {path.name for path in folder.glob("*.qmd")}
            self.require(
                actual_slide_names == expected_slide_names,
                f"style column must contain the complete demo sequence, including research framing, for {name}",
            )
            research_path = folder / "_03-research.qmd"
            algorithm_path = folder / "_03-algorithm.qmd"
            plot_path = folder / "_04-plot.qmd"
            table_path = folder / "_05-table.qmd"
            generate_path = folder / "_07-generate.qmd"
            citation_path = folder / "_08-citations.qmd"
            references_path = folder / "_09-references.qmd"
            self.require(research_path.is_file(), f"research framing slide missing for {name}")
            self.require(algorithm_path.is_file(), f"algorithm slide missing for {name}")
            self.require(plot_path.is_file(), f"plot slide missing for {name}")
            self.require(table_path.is_file(), f"table slide missing for {name}")
            self.require(generate_path.is_file(), f"generation slide missing for {name}")
            self.require(citation_path.is_file(), f"citation slide missing for {name}")
            self.require(references_path.is_file(), f"local references slide missing for {name}")
            if research_path.is_file():
                research_source = research_path.read_text(encoding="utf-8")
                self.require(
                    research_source.count('<ol class="research-questions">') == 1,
                    f"research framing slide must contain one question list for {name}",
                )
                self.require(
                    research_source.count('<ol class="research-hypotheses">') == 1,
                    f"research framing slide must contain one hypothesis list for {name}",
                )
                self.require(
                    research_source.count('class="is-highlighted"') == 2,
                    f"research framing slide must demonstrate one primary item in each list for {name}",
                )
                self.require(
                    "Illustrative placeholder" in research_source,
                    f"research framing example must disclose illustrative status for {name}",
                )
            if algorithm_path.is_file():
                algorithm_source = algorithm_path.read_text(encoding="utf-8")
                self.require(
                    "```text" in algorithm_source,
                    f"algorithm slide lacks pseudocode for {name}",
                )
                self.require(".algorithm-caption" in algorithm_source, f"algorithm slide lacks a caption for {name}")
                self.require("**Algorithm.**" in algorithm_source, f"algorithm caption lacks its bold label for {name}")
                self.require(
                    algorithm_source.find(".algorithm-caption") < algorithm_source.find('::: {.column width="30%"}'),
                    f"algorithm caption must stay inside the code column for {name}",
                )
            if plot_path.is_file():
                self.require(
                    f"assets/figures/gallery-{name}.svg" in plot_path.read_text(encoding="utf-8"),
                    f"plot slide does not use the matching style asset for {name}",
                )
            if table_path.is_file():
                table_source = table_path.read_text(encoding="utf-8")
                self.require("| Method |" in table_source, f"table slide lacks the method comparison for {name}")
                self.require("$\\uparrow$" in table_source, f"table slide lacks higher-is-better arrows for {name}")
                self.require("$\\downarrow$" in table_source, f"table slide lacks lower-is-better arrows for {name}")
                self.require("| Total $\\uparrow$ |" in table_source, f"table slide must put Total last for {name}")
                self.require(".structured-results" in table_source, f"table slide lacks total-column styling for {name}")
                self.require(".ours-last-2" in table_source, f"table slide lacks proposed-row highlighting for {name}")
                self.require(table_source.count("| Ours:") == 2, f"table slide must end with two proposed methods for {name}")
                self.require("**" in table_source, f"table slide lacks bold best values for {name}")
                self.require(f"#tbl-gallery-{name}" in table_source, f"table slide lacks a unique label for {name}")
            if generate_path.is_file():
                generate_source = generate_path.read_text(encoding="utf-8")
                self.require("```bash" in generate_source, f"generation slide lacks its command block for {name}")
                self.require(
                    ".algorithm-caption" in generate_source,
                    f"generation command block lacks an algorithm caption for {name}",
                )
                self.require(
                    "**Algorithm.**" in generate_source,
                    f"generation command caption lacks its bold label for {name}",
                )
            if citation_path.is_file():
                citation_source = citation_path.read_text(encoding="utf-8")
                style_key = STYLE_CITATION_KEYS[name]
                self.require(f"@{style_key}" in citation_source, f"citation slide lacks style source for {name}")
                for shared_key in ("alley2013", "scienceplots2021", "wcag2023"):
                    self.require(
                        f"@{shared_key}" in citation_source,
                        f"citation slide lacks shared source {shared_key} for {name}",
                    )
                self.require(".citation-help" in citation_source, f"citation interaction help is missing for {name}")
            if references_path.is_file():
                references_source = references_path.read_text(encoding="utf-8")
                style_key = STYLE_CITATION_KEYS[name]
                self.require(
                    f'data-style-key="{style_key}"' in references_source,
                    f"local references do not identify the style source for {name}",
                )
                self.require(
                    f"#references-{name}" in references_source,
                    f"local references slide lacks its stable target for {name}",
                )
                self.require(
                    ".style-references" in references_source,
                    f"local references container is missing for {name}",
                )

if __name__ == "__main__":
    raise SystemExit(Validation().run())
