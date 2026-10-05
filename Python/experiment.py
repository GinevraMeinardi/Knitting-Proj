"""
experiment.py
-------------
Simulates a "stretch test": pin one edge of the swatch, displace the
opposite edge by a controlled amount (the strain), let the interior
relax to equilibrium, and measure the reaction force needed to hold
that displacement. Repeating over a range of strains gives a
stress-strain curve, from which we estimate an effective elastic
modulus (like a fabric testing machine would).
"""

import numpy as np
import pandas as pd
from physics import relax, reaction_force_on_pinned


def stretch_test(grid, direction="horizontal", strains=None, verbose=False):
    """
    direction: 'horizontal' (pull left/right edges apart) or
               'vertical' (pull top/bottom edges apart)
    strains: iterable of fractional strains to test, e.g. 0.05 = 5% stretch
    Returns: pandas DataFrame with columns [strain, force, stress]
    """
    if strains is None:
        strains = np.linspace(0.0, 0.35, 8)

    rows, cols = grid.rows, grid.cols
    rest = grid.rest_pos

    if direction == "horizontal":
        left_idx = [grid.idx(r, 0) for r in range(rows)]
        right_idx = [grid.idx(r, cols - 1) for r in range(rows)]
        natural_span = rest[right_idx[0], 0] - rest[left_idx[0], 0]
        cross_section = rows  # force spread across this many "fibers"
    elif direction == "vertical":
        left_idx = [grid.idx(0, c) for c in range(cols)]     # 'left' = top edge here
        right_idx = [grid.idx(rows - 1, c) for c in range(cols)]
        natural_span = rest[right_idx[0], 1] - rest[left_idx[0], 1]
        cross_section = cols
    else:
        raise ValueError("direction must be 'horizontal' or 'vertical'")

    records = []
    for strain in strains:
        pinned = {}
        # left/top edge: pinned at rest position
        for i in left_idx:
            pinned[i] = tuple(rest[i])
        # right/bottom edge: displaced outward by strain * natural_span
        extra = strain * natural_span
        for i in right_idx:
            base = rest[i].copy()
            if direction == "horizontal":
                base[0] += extra
            else:
                base[1] += extra
            pinned[i] = tuple(base)

        pos, energy = relax(grid, pinned=pinned)
        force = reaction_force_on_pinned(grid, pos, right_idx)
        stress = force / cross_section
        records.append(dict(strain=strain, force=force, stress=stress))
        if verbose:
            print(f"  strain={strain:.3f}  force={force:.3f}  stress={stress:.4f}")

    return pd.DataFrame(records)


def estimate_modulus(df, n_points=3):
    """Effective elastic modulus = initial slope of stress vs strain
    (like Young's modulus), estimated by a linear fit over the first
    n_points of the curve (small-strain / 'linear-ish' regime)."""
    sub = df.iloc[:n_points]
    if sub["strain"].iloc[-1] == sub["strain"].iloc[0]:
        return np.nan
    slope, _ = np.polyfit(sub["strain"], sub["stress"], 1)
    return slope
