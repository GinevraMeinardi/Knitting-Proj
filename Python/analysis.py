"""
analysis.py
-----------
Runs the stretch test for every stitch pattern in both directions,
builds a results table, and produces comparison plots:
  1. Stress-strain curves per pattern/direction
  2. Bar chart of effective elastic modulus per pattern/direction
  3. A grid of swatch topology renderings

Run this file directly: `python analysis.py`
Outputs land in ./output/
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from stitches import StitchGrid
from experiment import stretch_test, estimate_modulus
from visualize import plot_swatch

OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)

PATTERNS = {
    "stockinette": dict(),
    "garter": dict(),
    "rib_1x1": dict(pattern="rib", n=1, m=1),
    "rib_2x2": dict(pattern="rib", n=2, m=2),
    "seed": dict(),
    "cable": dict(),
}

ROWS, COLS = 12, 12
STRAINS = np.linspace(0.0, 0.35, 8)


def build_grid(name, kwargs):
    pattern = kwargs.pop("pattern", name)
    return StitchGrid(pattern, ROWS, COLS, **kwargs)


def run_all():
    curve_records = []
    modulus_records = []
    grids = {}

    for name, kwargs in PATTERNS.items():
        kwargs = dict(kwargs)
        grid = build_grid(name, kwargs)
        grids[name] = grid
        for direction in ["horizontal", "vertical"]:
            df = stretch_test(grid, direction=direction, strains=STRAINS)
            df["pattern"] = name
            df["direction"] = direction
            curve_records.append(df)
            modulus_records.append(dict(
                pattern=name, direction=direction,
                modulus=estimate_modulus(df)
            ))
            print(f"{name:12s} {direction:10s} modulus={modulus_records[-1]['modulus']:.3f}")

    curves = pd.concat(curve_records, ignore_index=True)
    moduli = pd.DataFrame(modulus_records)
    curves.to_csv(os.path.join(OUT, "stress_strain_curves.csv"), index=False)
    moduli.to_csv(os.path.join(OUT, "elastic_moduli.csv"), index=False)
    return grids, curves, moduli


def plot_curves(curves):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    for ax, direction in zip(axes, ["horizontal", "vertical"]):
        sub = curves[curves.direction == direction]
        for pattern, g in sub.groupby("pattern"):
            ax.plot(g.strain, g.stress, marker="o", label=pattern)
        ax.set_title(f"{direction} stretch")
        ax.set_xlabel("strain")
        ax.legend(fontsize=8)
    axes[0].set_ylabel("stress (arb. units)")
    fig.suptitle("Stress-strain curves by stitch pattern")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "stress_strain_curves.png"), dpi=150)
    plt.close(fig)


def plot_moduli(moduli):
    fig, ax = plt.subplots(figsize=(9, 5))
    pivot = moduli.pivot(index="pattern", columns="direction", values="modulus")
    pivot = pivot.reindex(PATTERNS.keys())
    pivot.plot(kind="bar", ax=ax)
    ax.set_ylabel("effective elastic modulus (stress/strain, arb. units)")
    ax.set_title("Elastic modulus by stitch pattern and direction\n(lower = stretchier)")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "elastic_moduli.png"), dpi=150)
    plt.close(fig)


def plot_topologies(grids):
    fig, axes = plt.subplots(2, 3, figsize=(14, 9))
    for ax, (name, grid) in zip(axes.flatten(), grids.items()):
        plot_swatch(grid, ax=ax, title=name)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "swatch_topologies.png"), dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    grids, curves, moduli = run_all()
    plot_curves(curves)
    plot_moduli(moduli)
    plot_topologies(grids)
    print("\nDone. See ./output/ for CSVs and PNGs.")
    print("\nSummary (lower modulus = stretchier):")
    print(moduli.pivot(index="pattern", columns="direction", values="modulus").round(3))
