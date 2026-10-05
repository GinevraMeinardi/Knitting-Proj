"""
stitches.py
-----------
Defines the topology of a knitted swatch as a mass-spring network.

MODELING APPROACH (read this first):
Each stitch is a node on a grid. Real knitted loops are 3D and interlock,
but we approximate the fabric as a 2D network of point masses connected by
springs, in the same spirit as classic cloth-simulation mass-spring models.

Two node "types" exist: Knit (K) and Purl (P). A purl stitch is a knit
stitch worked from the other side, so on any given face it appears as a
horizontal "bump". Physically (per general textile/knitting references)
this bump is:
  - shorter in the vertical direction than a knit loop's leg, and
  - wider in the horizontal direction than a knit loop's leg.

We encode that qualitative difference as spring rest-lengths and
stiffnesses. These constants are NOT calibrated to real fiber measurements
-- they are a deliberately simple, documented approximation whose purpose
is to produce the correct *qualitative* and *relative* behavior (e.g. "rib
stretches more horizontally than stockinette", "garter stretches more
vertically than stockinette"), which is exactly the kind of question this
project sets out to explore. Swap in better numbers as you learn more.

Spring types per unit cell:
  - ROW springs:  connect (r, c) -- (r, c+1)   [horizontal, "through" a row]
  - COL springs:  connect (r, c) -- (r+1, c)    [vertical, the loop "leg"]
  - SHEAR springs: connect (r, c) -- (r+1, c+1) and (r, c) -- (r+1, c-1)
                    [diagonal, resist the fabric shearing/racking]
"""

import numpy as np

# --- Physical parameters per node type -------------------------------------
# rest lengths are in arbitrary "stitch units"; stiffness in arbitrary units.
NODE_PARAMS = {
    "K": dict(row_rest=1.0, col_rest=1.0, k_row=8.0, k_col=10.0),
    "P": dict(row_rest=1.3, col_rest=0.7, k_row=6.0, k_col=8.0),
}
K_SHEAR = 2.0  # diagonal springs are intentionally soft (yarn can rack/shear)


def _junction(param_name, k_name, a, b):
    """Average a physical parameter between two (possibly different) node types."""
    pa, pb = NODE_PARAMS[a][param_name], NODE_PARAMS[b][param_name]
    ka, kb = NODE_PARAMS[a][k_name], NODE_PARAMS[b][k_name]
    return (pa + pb) / 2.0, (ka + kb) / 2.0


# --- Pattern generators: return an (rows, cols) grid of 'K'/'P' ------------

def stockinette(rows, cols):
    return np.full((rows, cols), "K")


def garter(rows, cols):
    grid = np.full((rows, cols), "K")
    grid[1::2, :] = "P"   # grid[start:stop:step] basically means: start at the BOR, go all the way and apply to every other row
    # the second argument allows you to select the column axis
    return grid


def rib(rows, cols, n=1, m=1):
    """n columns knit, m columns purl, repeating."""
    grid = np.full((rows, cols), "K")
    period = n + m
    for c in range(cols):
        if (c % period) >= n:
            grid[:, c] = "P"
    return grid


def seed(rows, cols):
    grid = np.full((rows, cols), "K")
    for r in range(rows):
        for c in range(cols):
            if (r + c) % 2 == 1:
                grid[r, c] = "P"
    return grid


def cable(rows, cols, cable_width=2, cable_spacing=6, cross_every=6):
    """
    Simplified cable: mostly stockinette, with periodic vertical bands of
    'C' columns. Cable columns get an extra pair of cross-tension springs
    every `cross_every` rows (representing the twist where stitches are
    physically crossed and re-tensioned), which locally stiffens the band.
    """
    grid = np.full((rows, cols), "K")
    cable_cols = []
    c = cable_spacing // 2
    while c + cable_width <= cols:
        cable_cols.append(list(range(c, c + cable_width)))
        c += cable_spacing
    return grid, cable_cols


# --- Build spring list from a K/P grid --------------------------------------

class StitchGrid:
    def __init__(self, pattern_name, rows, cols, **kwargs):
        self.pattern_name = pattern_name
        self.rows, self.cols = rows, cols
        self.cable_cols = []

        if pattern_name == "stockinette":
            self.grid = stockinette(rows, cols)
        elif pattern_name == "garter":
            self.grid = garter(rows, cols)
        elif pattern_name == "rib":
            self.grid = rib(rows, cols, **kwargs)
        elif pattern_name == "seed":
            self.grid = seed(rows, cols)
        elif pattern_name == "cable":
            self.grid, self.cable_cols = cable(rows, cols, **kwargs)
        else:
            raise ValueError(f"Unknown pattern: {pattern_name}")

        self.n_nodes = rows * cols
        self.rest_pos = self._rest_positions()
        self.springs = self._build_springs()

    def idx(self, r, c):
        return r * self.cols + c

    def _rest_positions(self):
        """Lay nodes out on an approximate rest grid (used as the solver's
        starting guess; true rest shape emerges from spring relaxation)."""
        pos = np.zeros((self.n_nodes, 2))
        x = 0.0
        col_x = [0.0]
        for c in range(1, self.cols):
            a, b = self.grid[0, c - 1], self.grid[0, c]
            # _junction returns a tuple so '_' means that the second argument returned is discarded
            row_rest, _ = _junction("row_rest", "k_row", a, b)
            col_x.append(col_x[-1] + row_rest)
        y = 0.0
        row_y = [0.0]
        for r in range(1, self.rows):
            a, b = self.grid[r - 1, 0], self.grid[r, 0]
            col_rest, _ = _junction("col_rest", "k_col", a, b)
            row_y.append(row_y[-1] + col_rest)
        for r in range(self.rows):
            for c in range(self.cols):
                pos[self.idx(r, c)] = [col_x[c], row_y[r]]
        return pos

    def _build_springs(self):
        """Each spring: (i, j, rest_length, stiffness, kind)"""
        springs = []
        g = self.grid

        # ROW springs
        for r in range(self.rows):
            for c in range(self.cols - 1):
                a, b = g[r, c], g[r, c + 1]
                rest, k = _junction("row_rest", "k_row", a, b)
                springs.append((self.idx(r, c), self.idx(r, c + 1), rest, k, "row"))

        # COL springs
        for r in range(self.rows - 1):
            for c in range(self.cols):
                a, b = g[r, c], g[r + 1, c]
                rest, k = _junction("col_rest", "k_col", a, b)
                springs.append((self.idx(r, c), self.idx(r + 1, c), rest, k, "col"))

        # SHEAR springs (diagonals)
        for r in range(self.rows - 1):
            for c in range(self.cols):
                if c + 1 < self.cols:
                    p0, p1 = self.rest_pos[self.idx(r, c)], self.rest_pos[self.idx(r + 1, c + 1)]
                    rest = np.linalg.norm(p1 - p0)
                    springs.append((self.idx(r, c), self.idx(r + 1, c + 1), rest, K_SHEAR, "shear"))
                if c - 1 >= 0:
                    p0, p1 = self.rest_pos[self.idx(r, c)], self.rest_pos[self.idx(r + 1, c - 1)]
                    rest = np.linalg.norm(p1 - p0)
                    springs.append((self.idx(r, c), self.idx(r + 1, c - 1), rest, K_SHEAR, "shear"))

        # Extra cable cross-tension springs
        if self.cable_cols:
            for band in self.cable_cols:
                for r in range(0, self.rows - 1, 6):
                    if r + 1 >= self.rows:
                        continue
                    left, right = band[0], band[-1]
                    p0, p1 = self.rest_pos[self.idx(r, left)], self.rest_pos[self.idx(r + 1, right)]
                    rest = np.linalg.norm(p1 - p0) * 0.8  # pulled tighter -> stiffer band
                    springs.append((self.idx(r, left), self.idx(r + 1, right), rest, K_SHEAR * 4, "cable_cross"))

        return springs
