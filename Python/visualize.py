"""
visualize.py
------------
Draws the node/spring network of a StitchGrid (optionally after
relaxation) so you can visually sanity-check that each pattern's
topology looks structurally distinct -- e.g. rib should look
"columned", garter should look "ridged" (via node coloring), etc.
"""

import matplotlib.pyplot as plt
from physics import relax


def plot_swatch(grid, ax=None, positions=None, title=None):
    if positions is None:
        positions, _ = relax(grid, pinned={0: tuple(grid.rest_pos[0])})
    if ax is None:
        fig, ax = plt.subplots(figsize=(5, 5))

    colors = {"K": "#4C72B0", "P": "#DD8452"}
    for i, j, rest, k, kind in grid.springs:
        style = "-" if kind in ("row", "col") else ("--" if kind == "shear" else ":")
        lw = 1.6 if kind in ("row", "col") else (0.5 if kind == "shear" else 2.2)
        color = "gray" if kind != "cable_cross" else "green"
        ax.plot([positions[i, 0], positions[j, 0]],
                 [positions[i, 1], positions[j, 1]],
                 style, lw=lw, color=color, alpha=0.7, zorder=1)

    flat_grid = grid.grid.flatten()
    ax.scatter(positions[:, 0], positions[:, 1],
               c=[colors[t] for t in flat_grid], s=25, zorder=2,
               edgecolors="black", linewidths=0.3)

    ax.set_title(title or grid.pattern_name)
    ax.set_aspect("equal")
    ax.invert_yaxis()
    return ax
