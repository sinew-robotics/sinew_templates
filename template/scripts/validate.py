#!/usr/bin/env python3
"""Static validation for a Sinew deck (stdlib only).

This script runs in two modes:

- UNIVERSAL checks (always run): meaningful for any deck built on this
  template. They are derived from the deck manifest (deck.qmd) and the
  files it actually includes, and never assume a specific slide filename.
  New checks that apply to any deck belong in `validate_repository()` or
  `validate_manifest_and_slides()` (the latter already walks whatever
  deck.qmd includes, so per-slide checks such as caption/label conventions
  belong in `validate_images`, `validate_tables`, or
  `validate_research_lists`, or a new sibling method called from the same
  loop).
- GALLERY checks (run only inside this repository's nine-style gallery):
  style coverage across the nine `_quarto-color-*.yml` profiles, the
  STYLE_CITATION_KEYS map, the fourteen-file style-column contract, and the
  intro column's specific files. These hardcode paths that only exist in
  this repository's own gallery demo and would crash on any scaffolded
  deck, which renames or deletes the gallery slides on first use. New
  gallery-specific checks belong in `validate_gallery_repository()`,
  `validate_profiles()`, or `validate_styles()`.

Mode is auto-detected from the tree (see `detect_gallery_mode`): gallery
mode runs whenever `_quarto-gallery.yml` or `styles/gallery/` is present
-- the gallery-only scaffolding a real delivery deck has no reason to
keep, per docs/architecture.md ("an internal repository-tour layer...
should not be added to a normal talk command") -- regardless of how many
color profiles or style-named _slides folders happen to remain, so a
partial/broken gallery still fails loudly instead of silently reading as
a deck, while a real deck that legitimately keeps one or more color
profiles still reaches deck mode. `--mode gallery` or `--mode deck`
overrides detection.
"""

from __future__ import annotations

import argparse
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
DARK_COLORS = {"origami", "blueprint"}
SPECIALIZED_ALGORITHM_FONT_COLORS = {"unmasked", "the-give", "the-meeting", "movement"}
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
# Native Quarto cross-reference ID prefixes (@fig-..., @tbl-..., ...) share
# the "@key" citation syntax but are never bibliography citations; see
# docs/architecture.md and docs/citations.md.
QUARTO_XREF_PREFIXES = re.compile(r"^(?:fig|tbl|eq|sec|lst|thm|lem|cor|prp|cnj|def|exm|exr)-")
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

GALLERY_SKIP_NOTE = (
    "gallery-only checks SKIPPED (style coverage across the nine color profiles, "
    "the STYLE_CITATION_KEYS map, the fourteen-file style-column contract, and the "
    "intro column's specific files): neither _quarto-gallery.yml nor styles/gallery/ "
    "is present, so this tree does not carry the gallery's own internal-tour "
    "scaffolding. This is expected for a deck scaffolded from this template, even "
    "one that keeps one or more of its own color-*.yml profiles. Pass --mode "
    "gallery to force these checks."
)


def detect_gallery_mode() -> bool:
    """True whenever this tree carries gallery INTENT, so a partial or
    broken gallery still fails loudly (naming the specific missing piece
    via the existing per-name checks in validate_profiles/validate_styles),
    while a real delivery deck that legitimately keeps a subset of the
    scaffolding still reaches deck mode.

    A COUNT of profiles kept or style-named _slides folders kept cannot
    distinguish those two cases: a broken gallery can be missing any
    subset, and a real deck legitimately keeps at least the one color
    profile it selected (docs/authoring.md/AGENTS.md: "Select exactly one
    color-* profile for the deck") and, especially early on, sometimes
    more than one while deciding, or a _slides folder that happens to
    share a style's name by coincidence. Counting profiles/columns is what
    made both the AND version (the original P0: any deletion silently
    dropped to deck mode) and the OR version (every single-profile
    delivery deck: nineteen spurious gallery-only failures) wrong.

    Instead this keys on the one thing a real deck has no reason to keep
    and the gallery repo cannot function without: the gallery-only
    scaffolding itself, `_quarto-gallery.yml` and `styles/gallery/`. Per
    docs/architecture.md, "the gallery metadata is an internal
    repository-tour layer... not a second visual-style profile and should
    not be added to a normal talk command" -- no delivery deck has a
    reason to keep either, so their presence is intent, not a count.
    """
    return (ROOT / "_quarto-gallery.yml").is_file() or (ROOT / "styles/gallery").is_dir()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("auto", "gallery", "deck"),
        default="auto",
        help="Override automatic gallery-vs-deck detection (default: auto).",
    )
    return parser.parse_args(argv)


class Validation:
    def __init__(self, mode: str = "auto") -> None:
        self.errors: list[str] = []
        self.notes: list[str] = []
        self.mode = mode
        self.gallery_mode = False

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)

    def resolve_gallery_mode(self) -> bool:
        if self.mode == "gallery":
            return True
        if self.mode == "deck":
            return False
        return detect_gallery_mode()

    def run(self) -> int:
        gallery_mode = self.resolve_gallery_mode()
        self.gallery_mode = gallery_mode

        self.validate_repository()
        self.validate_manifest_and_slides()

        if gallery_mode:
            self.validate_gallery_repository()
            self.validate_profiles()
            self.validate_styles()
        else:
            self.notes.append(GALLERY_SKIP_NOTE)

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
        print(f"  mode={'gallery' if gallery_mode else 'deck'}")
        if gallery_mode:
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
        if self.gallery_mode:
            self.require(
                (ROOT / "docs/agent-templates/AGENTS.template.md").is_file(),
                "copyable AGENTS template is missing",
            )
            self.require(
                (ROOT / "docs/agent-templates/CLAUDE.template.md").is_file(),
                "copyable CLAUDE template is missing",
            )
        elif not (ROOT / "docs/agent-templates/AGENTS.template.md").is_file() and not (
            ROOT / "docs/agent-templates/CLAUDE.template.md"
        ).is_file():
            self.notes.append(
                "docs/agent-templates/*.template.md not found: fine if this deck already "
                "copied them out to its own AGENTS.md/CLAUDE.md and deleted the source "
                "per README ('Use as a starter'); only a problem if that copy never happened."
            )
        # Filename-agnostic provenance backstop (any deck's own affiliation
        # marks, not just this repo's KAIST/IRIS demo marks -- see AGENTS.md
        # file/edit hygiene, "protected assets"): whatever marks a deck ships,
        # their provenance/license/reuse constraints must be recorded.
        branding_dir = ROOT / "assets/branding"
        if branding_dir.is_dir():
            branding_files = [p for p in branding_dir.iterdir() if p.is_file() and p.name != "README.md"]
            if branding_files:
                self.require(
                    (branding_dir / "README.md").is_file(),
                    "assets/branding contains marks but no README.md documenting their provenance",
                )
        # deck.qmd's YAML unconditionally sets `bibliography: references.bib` (see
        # deck.qmd), so this file is load-bearing for the actual Quarto/citeproc
        # render, not just this validator's own citation-key cross-check -- keep
        # it a hard requirement in every mode, even for a deck that cites nothing.
        self.require((ROOT / "references.bib").is_file(), "references.bib is missing")
        # extension_path.parent resolves whichever install layout matched above:
        # the in-repo source (_extensions/sinew/) or Quarto's namespaced remote
        # install (_extensions/<org>/sinew/, e.g. sinew-robotics/sinew/), which is
        # what `quarto use template sinew-robotics/sinew_templates/template` --
        # this repository's primary documented install path -- actually produces.
        # Hardcoding _extensions/sinew/ here previously false-failed on every
        # deck scaffolded that way.
        extension_root = extension_path.parent if extension_path is not None else EXTENSION_MANIFEST_CANDIDATES[0].parent
        core_theme = extension_root / "theme/core.scss"
        runtime = extension_root / "theme/captions.html"
        reference_shortcodes = extension_root / "research-references.lua"
        self.require(core_theme.is_file(), "core theme is missing")
        self.require(runtime.is_file(), "post-body runtime is missing")
        self.require(reference_shortcodes.is_file(), "research reference shortcodes are missing")
        if core_theme.is_file():
            core_source = core_theme.read_text(encoding="utf-8")
            for marker in (
                ".research-questions",
                ".research-hypotheses",
                'content: "Q" counter(sinew-research-question)',
                'content: "H" counter(sinew-research-hypothesis)',
                ".sinew-reference",
                ".institution-lockup",
                ".sinew-fullscreen-dialog",
            ):
                self.require(marker in core_source, f"core theme is missing required component: {marker}")
        if runtime.is_file():
            runtime_source = runtime.read_text(encoding="utf-8")
            for marker in (
                "labelResearchStatements",
                "installInstitutionLockups",
                "wireSinewReferences",
                "registerReferencePreview",
                "buildQuartoCrossReferencePreview",
                "typesetClonedMath",
                "buildEvidenceInspector",
                "sinew-evidence-inspector",
                "sinewClickExpand",
                "clickClosesEvidence",
                "showModal",
            ):
                self.require(marker in runtime_source, f"evidence inspector runtime is missing: {marker}")
        legacy_profiles = sorted(ROOT.glob("_quarto-conf-*.yml"))
        self.require(not legacy_profiles, f"conference profiles must not be present: {legacy_profiles}")
        legacy_markers = sorted((ROOT / "styles/conferences").glob("*.css"))
        self.require(not legacy_markers, f"conference marker CSS must not be present: {legacy_markers}")

        if extension_path is not None:
            extension = extension_path.read_text(encoding="utf-8")
            self.require("link-citations: true" in extension, "citation links must be enabled")
            self.require("citations-hover: true" in extension, "citation hover previews must be enabled")
            self.require(
                "html-math-method: katex" in extension,
                "KaTeX is required for reliable dollar-delimited math in Reveal",
            )
            self.require(
                "shortcodes:" in extension and "research-references.lua" in extension,
                "research reference shortcodes must be contributed by the extension",
            )

        if reference_shortcodes.is_file():
            shortcode_source = reference_shortcodes.read_text(encoding="utf-8")
            for marker in ('["q"]', '["h"]', '["alg"]', "sinew-reference", "algorithm-"):
                self.require(marker in shortcode_source, f"research reference shortcode is missing: {marker}")

    def validate_gallery_repository(self) -> None:
        """Gallery-only: paths and content that only exist in this repo's
        nine-style demo (the intro column and gallery switcher UI), plus the
        per-style bibliography-coverage cross-check that depends on the
        intro column's citation slide. Run only when detect_gallery_mode()
        (or --mode gallery) is true; a scaffolded deck renames or deletes
        these files on first use.
        """
        self.require((ROOT / "_quarto-gallery.yml").is_file(), "default gallery profile is missing")
        self.require((ROOT / "_slides/01-intro/_03-citations.qmd").is_file(), "citation example slide is missing")
        self.require((ROOT / "_slides/01-intro/_04-references.qmd").is_file(), "bibliography slide is missing")
        intro_section = ROOT / "_slides/01-intro/_00-section.qmd"
        self.require(intro_section.is_file(), "intro divider slide is missing")
        if intro_section.is_file():
            intro_source = intro_section.read_text(encoding="utf-8")
            self.require(
                'class="institution-lockup"' in intro_source,
                "intro divider slide lacks the affiliation lockup",
            )
        self.require(
            (ROOT / "styles/gallery/gallery.css").is_file(),
            "default gallery marker CSS is missing",
        )
        # The KAIST/IRIS marks are this repository's own owner-supplied
        # affiliation marks (see AGENTS.md file/edit hygiene: "protected
        # assets"), not a naming contract any downstream deck must keep, so
        # this check stays gallery-only rather than universal.
        for logo_name in ("kaist_logo.png", "iris_logo.png"):
            self.require(
                (ROOT / f"assets/branding/{logo_name}").is_file(),
                f"affiliation mark is missing: {logo_name}",
            )
        self.require(
            (ROOT / "assets/branding/README.md").is_file(),
            "affiliation-mark provenance note is missing",
        )

        citations_path = ROOT / "_slides/01-intro/_03-citations.qmd"
        references_path = ROOT / "_slides/01-intro/_04-references.qmd"
        bibliography_path = ROOT / "references.bib"
        # Guarded the same way as the intro_section block above: reachable via
        # --mode gallery forced on a tree that is not actually the gallery, in
        # which case the presence self.require() calls above already recorded
        # the specific missing file(s); skip the cross-check instead of a raw
        # FileNotFoundError traceback.
        if citations_path.is_file() and references_path.is_file() and bibliography_path.is_file():
            citation_source = citations_path.read_text(encoding="utf-8")
            reference_source = references_path.read_text(encoding="utf-8")
            bibliography = bibliography_path.read_text(encoding="utf-8")
            citation_keys = set(re.findall(r"@([A-Za-z0-9_.:+#$/-]+)", citation_source))
            bibliography_keys = set(re.findall(r"^@[A-Za-z]+\{([^,]+),", bibliography, re.MULTILINE))
            self.require(len(citation_keys) >= 5, "citation example must exercise at least five references")
            self.require(
                citation_keys <= bibliography_keys, "every example citation key must exist in references.bib"
            )
            self.require(
                set(STYLE_CITATION_KEYS.values()) <= bibliography_keys,
                "every visual profile must have its own bibliography record",
            )
            self.require("{#refs}" in reference_source, "bibliography slide must provide the citeproc #refs target")
            self.require(
                "references-slide" in reference_source, "bibliography slide must activate two-column styling"
            )
            self.require(
                "global-references-slide" in reference_source,
                "shared bibliography must be marked as the global citeproc source",
            )

    def validate_profiles(self) -> None:
        """Gallery-only: style coverage across the nine color profiles and
        the gallery switcher UI. Called only when gallery mode is active.
        """
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

        # Guarded (like the intro-column block in validate_gallery_repository):
        # reachable via --mode gallery forced on a tree that only partially
        # matches the gallery shape, where these files may genuinely be
        # missing; self.require() below records that as a normal failure
        # instead of a raw FileNotFoundError traceback.
        gallery_path = ROOT / "_quarto-gallery.yml"
        columns_html_path = ROOT / "styles/gallery/columns.html"
        columns_css_path = ROOT / "styles/gallery/columns.css"
        self.require(gallery_path.is_file(), "default gallery profile is missing")
        self.require(columns_html_path.is_file(), "gallery column switcher markup is missing")
        self.require(columns_css_path.is_file(), "gallery column runtime CSS is missing")
        gallery = gallery_path.read_text(encoding="utf-8") if gallery_path.is_file() else ""
        columns_html = columns_html_path.read_text(encoding="utf-8") if columns_html_path.is_file() else ""
        columns_css = columns_css_path.read_text(encoding="utf-8") if columns_css_path.is_file() else ""
        if gallery:
            self.require('gallery-mode: "runtime-style-preview"' in gallery, "gallery runtime metadata is missing")
            self.require("styles/gallery/columns.css" in gallery, "gallery profile does not load column styles")
            self.require("styles/gallery/columns.html" in gallery, "gallery profile does not load column switching")
        if columns_css:
            self.require(
                columns_css.count("--sinew-logo-plate:") == len(DARK_COLORS) + 1
                and "--sinew-logo-plate: transparent;" in columns_css,
                "gallery CSS must reset logo plates and override them for dark profiles only",
            )
            self.require(
                columns_css.count("--sinew-algorithm-font:") >= len(SPECIALIZED_ALGORITHM_FONT_COLORS),
                "gallery CSS must mirror every specialized algorithm font",
            )

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
            if columns_html:
                self.require(f'"{name}"' in columns_html, f"gallery switcher does not register {name}")
            if columns_css:
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

        bibliography_path = ROOT / "references.bib"
        bibliography_keys: set[str] = set()
        if bibliography_path.is_file():
            bibliography_keys = set(
                re.findall(r"^@[A-Za-z]+\{([^,]+),", bibliography_path.read_text(encoding="utf-8"), re.MULTILINE)
            )

        # Universal single-global-#refs check (AGENTS.md/CLAUDE.md: "Preserve
        # the single global #refs source"). Any deck built on this template
        # can rename or relocate its bibliography slide, so this looks for
        # whichever included file provides it rather than the gallery's
        # fixed _slides/01-intro/_04-references.qmd path.
        refs_target_files: list[Path] = []
        any_citation_used = False

        # Universal deck-wide id uniqueness for @fig-.../@tbl-.../{{< alg
        # ... >}} targets. A duplicate id silently breaks cross-references
        # (Quarto/Sinew resolve to whichever matching id comes first, with
        # no error), so this is checked for every deck, not just the
        # gallery -- and the gallery is exactly where it is easiest to
        # introduce by accident, since nine near-identical style columns
        # each define their own #fig-media-<style>-*, #fig-placeholder-
        # <style>, #tbl-gallery-<style>, and #algorithm-gallery-<style>-*
        # ids from the same template.
        object_id_pattern = re.compile(r"\{#((?:fig|tbl|algorithm)-[\w-]+)")
        object_id_files: dict[str, list[str]] = {}

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

            if "{#refs}" in text:
                refs_target_files.append(rel)
            used_keys = set(re.findall(r"@([A-Za-z0-9_.:+#$/-]+)", text))
            cross_reference_keys = {key for key in used_keys if QUARTO_XREF_PREFIXES.match(key)}
            if used_keys - cross_reference_keys:
                any_citation_used = True
            for object_id in object_id_pattern.findall(text):
                object_id_files.setdefault(object_id, []).append(str(rel))

            self.validate_images(path, text)
            self.validate_tables(path, text)
            self.validate_research_lists(path, text)
            self.validate_citations(path, text, bibliography_keys)
            self.validate_figure_captions(path, text)
            self.validate_hand_numbered_captions(path, text)

        self.require(
            len(refs_target_files) <= 1,
            f"only one slide may provide the citeproc #refs target: {refs_target_files}",
        )
        if any_citation_used:
            self.require(
                len(refs_target_files) == 1,
                "a deck with citations must include exactly one {#refs} bibliography slide",
            )
        duplicate_object_ids = {
            object_id: files for object_id, files in object_id_files.items() if len(files) > 1
        }
        self.require(
            not duplicate_object_ids,
            f"duplicate figure/table/algorithm id(s) across the deck: {duplicate_object_ids}",
        )

    def validate_citations(self, path: Path, text: str, bibliography_keys: set[str]) -> None:
        """Catch two ways a citation silently fails to become a visible
        marker: an empty key (`[@]`, `[@key1; @]`) renders as nothing with
        no warning from Quarto, and a key with no matching references.bib
        entry drops that citation from the rendered bibliography without
        erroring the build. See docs/citations.md.
        """
        rel = path.relative_to(ROOT)
        self.require(
            re.search(r"@(?![A-Za-z0-9_.:+#$/-])", text) is None,
            f"empty citation key [@] in {rel}",
        )
        used_keys = set(re.findall(r"@([A-Za-z0-9_.:+#$/-]+)", text))
        # @fig-..., @tbl-..., @eq-..., etc. are native Quarto cross-references
        # to figures/tables/equations/sections, not bibliography citations;
        # see docs/architecture.md ("Use native @fig-... and @tbl-...
        # cross-references"). Only genuine citation keys are checked against
        # references.bib.
        cross_reference_keys = {key for key in used_keys if QUARTO_XREF_PREFIXES.match(key)}
        missing_keys = sorted(used_keys - bibliography_keys - cross_reference_keys)
        self.require(
            not missing_keys,
            f"citation key(s) not found in references.bib in {rel}: {missing_keys}",
        )

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

    def validate_figure_captions(self, path: Path, text: str) -> None:
        """Catch a figure that carries both a Markdown bracket caption AND
        an adjacent `.figcap` block. core.scss groups `figcaption` (which
        Quarto auto-renders from a non-empty bracket caption on a labeled
        image) and `.figcap` under one shared caption-styling selector, so
        using both stacks two overlapping "Figure N:" captions that can run
        off-slide. Detail belongs in fig-alt or the bracket caption -- pick
        one, never both. An empty bracket caption `![]` is not a double
        caption (the .figcap is then the only caption); a bracket caption
        followed by an unrelated `.source` line is not a double caption
        either, since `.source` is a distinct convention (see
        docs/figures-and-tables.md) and this only looks for `.figcap`.
        """
        rel = path.relative_to(ROOT)
        image_pattern = re.compile(r"!\[(.*?)\]\(([^)]+)\)(?:\{([^}]*)\})?", re.DOTALL)
        matches = list(image_pattern.finditer(text))
        for index, match in enumerate(matches):
            caption = match.group(1).strip()
            if not caption:
                continue
            window_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            window = text[match.end() : window_end]
            self.require(
                re.search(r"\.figcap\b", window) is None,
                f"double caption in {rel}: image {match.group(2)} has a bracket caption AND "
                "a following .figcap for the same figure; use one or the other, not both",
            )

    def validate_tables(self, path: Path, text: str) -> None:
        rel = path.relative_to(ROOT)
        separator = re.search(r"^\|(?:[^\n]*\|)+\n\|\s*:?-+", text, re.MULTILINE)
        if separator:
            self.require(
                re.search(r"^:\s+.+\{#tbl-[^}]+\}\s*$", text, re.MULTILINE) is not None,
                f"table needs a caption and #tbl- label in {rel}",
            )
            # A structured result table (metric-direction arrows in its
            # headings, plus at least one labeled "Ours:" row) must use the
            # real conventions instead of hand-formatting the same shape:
            # .structured-results for the Total-column rule and .ours-last-N
            # to highlight the proposed-method block. A deck that manually
            # bolds its best values without either loses the Total-column
            # separator and the highlighted-block treatment, and is liable
            # to drift from the documented convention slide to slide.
            has_direction_arrows = "$\\uparrow$" in text or "$\\downarrow$" in text
            has_ours_row = re.search(r"^\|\s*Ours:", text, re.MULTILINE) is not None
            if has_direction_arrows and has_ours_row:
                self.require(
                    ".structured-results" in text,
                    f"structured result table lacks .structured-results styling in {rel}",
                )
                self.require(
                    re.search(r"\.ours-last-[1-4]\b", text) is not None,
                    f"structured result table lacks a highlighted .ours-last-N block for its Ours: rows in {rel}",
                )

    def validate_hand_numbered_captions(self, path: Path, text: str) -> None:
        """Flag a hand-typed "Fig. N" / "Figure N" / "Table N" / "Algorithm
        N" instead of the automatic forms (@fig-..., @tbl-..., {{< alg >}},
        or the unnumbered **Algorithm.** caption prefix Sinew numbers
        itself). Hand-numbering silently collides the moment two slides
        pick the same number.

        Two tiers, because "this deck's own hand-numbered caption" and "a
        prose reference to a number in someone else's paper" cannot always
        be told apart cleanly:

        - A hard error only for the unambiguous shape: a BOLD label at the
          start of a line, e.g. "**Fig. 6.**" or "**Algorithm 2.**". This
          is specifically what a hand-typed caption identifier looks like
          (it mimics Sinew's own generated bold `Figure N`/`Algorithm N`
          output -- compare the correct, unnumbered `**Algorithm.**`
          prefix documented in AGENTS.md, which Sinew turns into a live
          numbered `Algorithm N`). A reference to another paper's figure
          is prose, not a bolded line-start label, so this shape does not
          plausibly occur there.
        - A note (not a failure) for the same words appearing anywhere
          else in the slide, e.g. "adapted from Figure 3 of [@smith2025]".
          That may well be a legitimate reference to someone else's
          figure; telling it apart from a hand-numbered reference to this
          deck's own figure from source text alone is not reliable, so
          this stays advisory rather than blocking.
        """
        rel = path.relative_to(ROOT)
        pattern = re.compile(r"\b(?:Fig\.|Figure|Table|Algorithm)\s+\d+\b")
        bold_label_pattern = re.compile(r"^\s*\*\*(?:Fig\.|Figure|Table|Algorithm)\s+\d+\.?\*\*", re.MULTILINE)

        bold_labels = bold_label_pattern.findall(text)
        if bold_labels:
            self.require(
                False,
                f"hand-numbered caption label in {rel}: {bold_labels[0].strip()} -- use the "
                "automatic @fig-.../@tbl-.../{{< alg >}} forms or the unnumbered **Algorithm.** "
                "prefix instead of typing the number",
            )

        all_matches = {match.group(0) for match in pattern.finditer(text)}
        bold_matches = {match.group(0) for label in bold_labels for match in [pattern.search(label)] if match}
        advisory_matches = sorted(all_matches - bold_matches)
        if advisory_matches:
            self.notes.append(
                f"hand-typed figure/table/algorithm number in {rel}: {advisory_matches} -- "
                "if this refers to THIS deck's own figure/table/algorithm, use "
                "@fig-.../@tbl-.../{{< alg >}} instead; if it refers to another paper's "
                "figure (e.g. \"adapted from Figure 3 of [@key]\"), no change needed"
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
        """Gallery-only: per-style CSS token completeness, matplotlib
        overlays, gallery plot assets, and the fourteen-file style-column
        content contract (algorithm/plot/table/citation slides keyed by
        style name). Called only when gallery mode is active.
        """
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
            if name in SPECIALIZED_ALGORITHM_FONT_COLORS:
                self.require(
                    "--sinew-algorithm-font:" in source and "monospace" in source,
                    f"{path.name} must define a genuine monospace algorithm font stack",
                )
            if name in DARK_COLORS:
                self.require(
                    "--sinew-logo-plate:" in source
                    and "var(--sinew-ink)" in source
                    and "var(--sinew-accent)" in source,
                    f"{path.name} must derive a light logo plate from its own palette",
                )
            else:
                self.require(
                    "--sinew-logo-plate:" not in source,
                    f"{path.name} is light and must leave transparent logos unbacked",
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
            # Fourteen files (docs/adding-a-style.md section 4 is the
            # authoritative list): _05a-media.qmd, _05b-placeholder.qmd, and
            # _05c-layout.qmd sit between _05-table.qmd and _06-conclusion.qmd.
            expected_slide_names = {
                "_00-section.qmd",
                "_01-guidelines.qmd",
                "_02-problem.qmd",
                "_03-research.qmd",
                "_03-algorithm.qmd",
                "_04-plot.qmd",
                "_05-table.qmd",
                "_05a-media.qmd",
                "_05b-placeholder.qmd",
                "_05c-layout.qmd",
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
            section_path = folder / "_00-section.qmd"
            algorithm_path = folder / "_03-algorithm.qmd"
            plot_path = folder / "_04-plot.qmd"
            table_path = folder / "_05-table.qmd"
            media_path = folder / "_05a-media.qmd"
            placeholder_path = folder / "_05b-placeholder.qmd"
            layout_path = folder / "_05c-layout.qmd"
            generate_path = folder / "_07-generate.qmd"
            citation_path = folder / "_08-citations.qmd"
            references_path = folder / "_09-references.qmd"
            self.require(research_path.is_file(), f"research framing slide missing for {name}")
            self.require(algorithm_path.is_file(), f"algorithm slide missing for {name}")
            self.require(plot_path.is_file(), f"plot slide missing for {name}")
            self.require(table_path.is_file(), f"table slide missing for {name}")
            self.require(media_path.is_file(), f"media slide missing for {name}")
            self.require(placeholder_path.is_file(), f"placeholder slide missing for {name}")
            self.require(layout_path.is_file(), f"layout slide missing for {name}")
            self.require(generate_path.is_file(), f"generation slide missing for {name}")
            self.require(citation_path.is_file(), f"citation slide missing for {name}")
            self.require(references_path.is_file(), f"local references slide missing for {name}")
            if section_path.is_file():
                section_source = section_path.read_text(encoding="utf-8")
                self.require(
                    'class="institution-lockup"' in section_source,
                    f"divider slide lacks the affiliation lockup for {name}",
                )
                for logo_name in ("kaist_logo.png", "iris_logo.png"):
                    self.require(
                        f"assets/branding/{logo_name}" in section_source,
                        f"divider slide lacks {logo_name} for {name}",
                    )
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
                self.require(
                    f"#algorithm-gallery-{name}-method" in algorithm_source,
                    f"method algorithm lacks a stable reference target for {name}",
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
            if media_path.is_file():
                media_source = media_path.read_text(encoding="utf-8")
                for media_id in (
                    f"#fig-media-{name}-photo",
                    f"#fig-media-{name}-clip",
                    f"#fig-media-{name}-gif",
                ):
                    self.require(media_id in media_source, f"media slide lacks a stable id {media_id} for {name}")
            if placeholder_path.is_file():
                placeholder_source = placeholder_path.read_text(encoding="utf-8")
                self.require(
                    f"#fig-placeholder-{name}" in placeholder_source,
                    f"placeholder slide lacks a stable id #fig-placeholder-{name} for {name}",
                )
                self.require(
                    ".missing-evidence" in placeholder_source,
                    f"placeholder slide does not use the missing-evidence pattern for {name}",
                )
            if layout_path.is_file():
                self.require(
                    ".split-layout-connector" in layout_path.read_text(encoding="utf-8"),
                    f"layout slide does not demonstrate the split-layout-connector primitive for {name}",
                )
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
                self.require(
                    f"#algorithm-gallery-{name}-render" in generate_source,
                    f"generation algorithm lacks a stable reference target for {name}",
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
                for reference_source in (
                    f"@fig-gallery-{name}",
                    f"@tbl-gallery-{name}",
                    f"{{{{< alg algorithm-gallery-{name}-method >}}}}",
                    "{{< q 1 >}}",
                    "{{< h 1 >}}",
                ):
                    self.require(
                        reference_source in citation_source,
                        f"citation slide lacks internal reference {reference_source} for {name}",
                    )
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
    args = parse_args(sys.argv[1:])
    raise SystemExit(Validation(mode=args.mode).run())
