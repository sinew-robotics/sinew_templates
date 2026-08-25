#!/usr/bin/env python3
"""Generate the same illustrative learning curve in every Sinew style."""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
STYLE_DIR = ROOT / "styles/matplotlib"
OUTPUT_DIR = ROOT / "assets/figures"
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


def curve(start: float, gain: float, rate: float, steps: list[int]) -> list[float]:
    return [start + gain * (1.0 - math.exp(-step / rate)) for step in steps]


def render(style: str) -> None:
    plt.style.use(
        [
            "default",
            str(STYLE_DIR / "sinew-slides.mplstyle"),
            str(STYLE_DIR / f"sinew-{style}.mplstyle"),
        ]
    )

    steps = list(range(0, 101, 5))
    force_aware = curve(30.0, 56.0, 30.0, steps)
    pose_only = curve(28.0, 38.0, 34.0, steps)
    force_band = [5.0 - 1.5 * step / 100.0 for step in steps]
    pose_band = [5.5 - 1.0 * step / 100.0 for step in steps]

    fig, ax = plt.subplots(figsize=(11.6, 5.8))
    first_color, second_color = plt.rcParams["axes.prop_cycle"].by_key()["color"][:2]

    ax.fill_between(
        steps,
        [value - band for value, band in zip(force_aware, force_band)],
        [value + band for value, band in zip(force_aware, force_band)],
        color=first_color,
        alpha=0.16,
        linewidth=0,
    )
    ax.fill_between(
        steps,
        [value - band for value, band in zip(pose_only, pose_band)],
        [value + band for value, band in zip(pose_only, pose_band)],
        color=second_color,
        alpha=0.14,
        linewidth=0,
    )
    ax.plot(
        steps,
        force_aware,
        color=first_color,
        marker="o",
        markevery=2,
        label="Force-aware",
    )
    ax.plot(
        steps,
        pose_only,
        color=second_color,
        linestyle="--",
        marker="s",
        markevery=2,
        label="Pose-only",
    )

    ax.set_xlabel("Training steps (x1000)")
    ax.set_ylabel("Success rate (%)")
    ax.set_xlim(0, 100)
    ax.set_ylim(20, 92)
    ax.legend(loc="lower right", frameon=True)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        OUTPUT_DIR / f"gallery-{style}.svg",
        format="svg",
        metadata={
            "Title": f"Illustrative learning curves in the {style} style",
            "Description": "Force-aware and pose-only illustrative learning curves.",
            "Creator": "sinew_templates",
            "Date": None,
        },
    )
    plt.close(fig)


def main() -> None:
    for style in STYLES:
        render(style)
    print(f"Generated {len(STYLES)} gallery plots in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
