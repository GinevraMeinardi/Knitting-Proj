"""
physics.py
----------
Relaxes a StitchGrid's spring network to mechanical equilibrium by
minimizing total spring potential energy, subject to optional pinned
(boundary-condition) node positions. This is used both to find the
fabric's natural rest shape and to simulate a stretch test (pin two
edges and pull them apart, then measure the resulting tension).
"""

import numpy as np
from scipy.optimize import minimize


def spring_energy(positions_flat, springs, n_nodes):
    pos = positions_flat.reshape(n_nodes, 2)
    energy = 0.0
    for i, j, rest, k, kind in springs:
        d = np.linalg.norm(pos[i] - pos[j])
        energy += 0.5 * k * (d - rest) ** 2
    return energy


def spring_energy_and_grad(positions_flat, springs, n_nodes):
    pos = positions_flat.reshape(n_nodes, 2)
    energy = 0.0
    grad = np.zeros_like(pos)
    for i, j, rest, k, kind in springs:
        vec = pos[i] - pos[j]
        d = np.linalg.norm(vec)
        if d < 1e-9:
            continue
        diff = d - rest
        energy += 0.5 * k * diff ** 2
        f = k * diff * (vec / d)
        grad[i] += f
        grad[j] -= f
    return energy, grad.flatten()


def relax(grid, pinned=None, tol=1e-7, maxiter=2000):
    """
    grid: a StitchGrid
    pinned: dict {node_index: (x, y)} of nodes held fixed in place.
    Returns: (equilibrium_positions (n_nodes,2), total_energy)
    """
    pinned = pinned or {}
    n = grid.n_nodes
    x0 = grid.rest_pos.copy()
    for i, (px, py) in pinned.items():
        x0[i] = [px, py]
    x0 = x0.flatten()

    pinned_idx = np.array(sorted(pinned.keys()), dtype=int)
    free_mask = np.ones(n, dtype=bool)
    free_mask[pinned_idx] = False

    def unpack(free_vals):
        pos = x0.reshape(n, 2).copy()
        pos[free_mask] = free_vals.reshape(-1, 2)
        return pos

    def objective(free_vals):
        pos = unpack(free_vals)
        e, g = spring_energy_and_grad(pos.flatten(), grid.springs, n)
        g2d = g.reshape(n, 2)
        return e, g2d[free_mask].flatten()

    x0_free = x0.reshape(n, 2)[free_mask].flatten()
    res = minimize(objective, x0_free, jac=True, method="L-BFGS-B",
                    options=dict(maxiter=maxiter, ftol=tol))
    final_pos = unpack(res.x)
    final_energy = spring_energy(final_pos.flatten(), grid.springs, n)
    return final_pos, final_energy


def reaction_force_on_pinned(grid, positions, pinned_idx):
    """Sum of |spring force| pulling on a set of pinned nodes -- this is
    what a force gauge would read if it were holding those nodes in place."""
    pos = positions
    force = np.zeros((grid.n_nodes, 2))
    for i, j, rest, k, kind in grid.springs:
        vec = pos[i] - pos[j]
        d = np.linalg.norm(vec)
        if d < 1e-9:
            continue
        f = k * (d - rest) * (vec / d)
        force[i] -= f
        force[j] += f
    return sum(np.linalg.norm(force[idx]) for idx in pinned_idx)
