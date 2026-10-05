import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from mpl_toolkits.mplot3d import Axes3D
import sympy as sp
from scipy.integrate import quad

# ---------------- 1D fit ----------------------
# n of stitches constant
"""
n_fixed = 10         # sts

def fitR(R, J):
    return n_fixed * 2 * np.pi * R + n_fixed * J
    # this way, J holds the tension and the extra amount between two stitches

# needles radii
x_R = np.array([2.25, 2.5, 2.75, 3, 3.25, 3.5])         # [mm]
y_R = np.array([213, 247, 263, 265, 296, 296])          # [mm]
g_v_arr = np.array([5.0, 5.0, 5.0, 5.3, 5.6, 6.3])
g_h_arr = np.array([6.5, 7.0, 7.0, 7.9, 7.9, 8.0])
r_arr = np.array([1.0, 1.0, 1.0, 1.5, 1.5, 1.5])
# ----- error porpagation -----
sigma_rulerR = 1.0                                       # [mm]
sigma_markerR = 2.0                                      # [mm]
sigma_segR = np.sqrt(sigma_markerR**2 + sigma_rulerR**2)
# kR = np.arange(1, 6)
# sigma_cumR = sigma_segR * np.sqrt(kR)
sigma_R = sigma_segR * np.sqrt(n_fixed / 5)
needle_R = np.full(x_R.size, n_fixed)

"""
# ---------------- 1D fit ------------------
# R constant, the number of stitches changes
R_fixed = 3           # mm

def fitN(N, J):
    return N * 2 * np.pi * R_fixed + N * J

# number of stitches 
x_N = np.array([5, 10, 15, 20, 25, 30, 35])             # [sts]
x_N = np.linspace(5, 35, 7)                             # [sts]
y_N = np.array([127, 256, 387, 525, 652, 786, 914])     # [mm]

# ----- error porpagation -----
sigma_ruler = 1.0                                       # [mm]
sigma_marker = 2.0                                      # [mm]
sigma_seg = np.sqrt(sigma_marker**2 + sigma_ruler**2)
k = np.arange(1, 8)
sigma_cum = sigma_seg * np.sqrt(k)
needle_N = np.full(x_N.size, R_fixed)


#________________________________________________________________________________________

r = 1
g_h = 7
g_v = 6.4
A = 3 * r / 2
B = g_h / (2 * np.pi)
C = g_h / 4
D = (g_v + 2*r)/ 2 
E = r 
F = E
R = 3

#______________________________________________________________________________________________________________________
# ---------- uncertainty on the parametric curve ----------
# same curve as before, but as a plain function of the parameters
def stitch_length(g_h, g_v, r):
    A = 3 * r / 2
    B = g_h / (2 * np.pi)
    D = (g_v + 2*r)/ 2
    E = r
    f = lambda t: np.sqrt((-2*A*np.cos(2*t) + B)**2      # dx/dt
                          + (D*np.cos(t))**2             # dy/dt
                          + (-2*E*np.sin(2*t))**2)       # dz/dt
    return 2 * quad(f, -np.pi/2, np.pi/2)[0]

params = {'g_h': g_h, 'g_v': g_v, 'r': r}
sigmas = {'g_h': 0.5, 'g_v': 0.5, 'r': 0.5}      # [mm] 

# contribution of each parameter to the length of ONE stitch (central difference)
contrib = {}
for name, s in sigmas.items():
    hi = dict(params); hi[name] += s
    lo = dict(params); lo[name] -= s
    contrib[name] = (stitch_length(**hi) - stitch_length(**lo)) / 2
    print(f"{name}: ±{s} -> ±{abs(contrib[name]):.3f} mm per stitch")

# independent parameters add in quadrature
sigma_L = np.sqrt(sum(c**2 for c in contrib.values()))
print(f"total: {stitch_length(**params):.3f} ± {sigma_L:.3f} mm per stitch")

# the same stitch is repeated N times, so the error is fully correlated: it grows as N, not sqrt(N)
sigma_curve = x_N * sigma_L

# ---------- parametric curve for each needle (own gauge each) ----------
sigmas_R = {'g_h': 0.1, 'g_v': 0.2, 'r': 0.1}      # [mm] PLACEHOLDERS

"""
def curve_with_error(g_h, g_v, r, sig):
    p = {'g_h': g_h, 'g_v': g_v, 'r': r}
    var = 0
    for name, s in sig.items():
        hi = dict(p); hi[name] += s
        lo = dict(p); lo[name] -= s
        var += ((stitch_length(**hi) - stitch_length(**lo)) / 2) ** 2
    return stitch_length(**p), np.sqrt(var)

L_R = np.zeros(x_R.size)
sigma_L_R = np.zeros(x_R.size)
for i in range(x_R.size):
    L_R[i], sigma_L_R[i] = curve_with_error(g_h_arr[i], g_v_arr[i], r_arr[i], sigmas_R)
    print(f"R={x_R[i]:.2f}: curve {L_R[i]:.2f} ± {sigma_L_R[i]:.2f} mm/stitch,  "
          f"2piR+g_h {2*np.pi*x_R[i] + g_h_arr[i]:.2f},  data {y_R[i]/n_fixed:.2f}")

arc_lengths_R = n_fixed * L_R
sigma_curve_R = n_fixed * sigma_L_R
"""
#____________________________________________________________________________________________________________________--

def arc_length_3d(x_expr, y_expr, z_expr, t_sym, a, b):
    # Exact symbolic derivatives
    dx = sp.diff(x_expr, t_sym)
    dy = sp.diff(y_expr, t_sym)
    dz = sp.diff(z_expr, t_sym)
 
    speed_expr = sp.sqrt(dx**2 + dy**2 + dz**2)
    # Turn into a fast numerical function
    speed_func = sp.lambdify(t_sym, speed_expr, modules="numpy")
 
    length, abs_err = quad(speed_func, a, b)
    return length, abs_err

t1 = sp.symbols("t", real=True)
X0_sym = -A * sp.sin(2 * t1) + B * t1 - C
Y0_sym = D * sp.sin(t1)
Z0_sym = E * sp.cos(2 * t1) + F

L, err = arc_length_3d(X0_sym, Y0_sym, Z0_sym, t1, -np.pi/2, np.pi/2)
print(f"Length L = {2*L:.3f}")

arc_lengths = np.zeros(x_N.size)
model_old = np.zeros(x_N.size)
model_new = np.zeros(x_N.size)
# model_oldR = np.zeros(x_R.size)
# model_newR = np.zeros(x_R.size)

for l in range(0, x_N.size):
    arc_lengths[l] = 2*L * x_N[l]
    model_old[l] = 3*np.pi*R * x_N[l]
    model_new[l] = (2*np.pi*R + g_h) * x_N[l]
    #print(f"Parametric lengths: {arc_lengths[l]:.4f}")
"""
for n in range(0, x_R.size):
    model_oldR[n] = n_fixed * 3 * np.pi * x_R[n]
    model_newR[n] = (2*np.pi*x_R[n] + g_h_arr[n]) * n_fixed

# --- Plot both fits ---

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

Rfit = np.linspace(min(x_R), max(x_R), 200)
axes[0].errorbar(x_R, y_R, yerr=sigma_R, fmt='o', ms=2, capsize=3, label='data')
nfit = np.linspace(0, x_R.max(), 100)
axes[0].errorbar(x_R, arc_lengths_R, yerr=sigma_curve_R, fmt='x', color='orange', ms=4, mew=2, capsize=3, label='parm. curve')
axes[0].errorbar(x_R, model_newR, yerr=sigma_R, fmt = 'x', ms=2, capsize=3, color='red', label='2piR + g_h')
axes[0].errorbar(x_R, model_oldR, yerr=sigma_R, fmt = 'x', ms=2, capsize=3, color='green', label='3piR')
# axes[0].plot(Rfit, fitR(Rfit, J_R), '-', label=f'fit: J={J_R:.3f}')
axes[0].set_xlabel('R [mm]'); axes[0].set_ylabel('y [mm]'); axes[0].set_title('Stitch Length vs needle radius (N fixed)')
axes[0].legend(loc='best')

# compatibility with the data (curve error and data error combined)
z = (y_N - arc_lengths) / np.sqrt(sigma_cum**2 + sigma_curve**2)
print("deviation data vs curve [sigma]:", np.round(z, 2))
"""
fig, axes = plt.subplots(1, 1, figsize=(6,4.5))

nfit = np.linspace(min(x_N), max(x_N), 200)
# axes.plot(x_N, y_N, 'o', label='data', markersize=8)
axes.errorbar(x_N, y_N, yerr=sigma_cum, fmt='o', ms=10, capsize=3, label='data')
# nfit = np.linspace(0, x_N.max(), 100)
# L1 = stitch_length(**params)
# axes.plot(nfit, L1 * nfit, color='orange', label='parm. curve')
# axes.fill_between(nfit, (L1 - sigma_L) * nfit, (L1 + sigma_L) * nfit, color='orange', alpha=0.2)
axes.errorbar(x_N, arc_lengths, yerr=sigma_curve, fmt='x', color='orange', ms=10, mew=3, capsize=3, label='parm. curve')
# axes.errorbar(0, 0, fmt='ko', ms=4)      # optional: mark the origin
axes.set_xlim(0, 37)

axes.errorbar(x_N, model_old, yerr=sigma_cum, fmt='x', ms=10, capsize=3, label='3piR', color='green')
axes.errorbar(x_N, model_new, yerr=sigma_cum, fmt='x', ms=10, capsize=3, label='2piR + g_h', color='red')
# axes.plot(x_N, arc_lengths, 'x', label='parm. curve', color='orange', markersize=6, markeredgewidth=2)
# axes.plot(x_N, model_old, 'x', label='3piR', color='green', markersize=6, markeredgewidth=2)
# axes.plot(x_N, model_new, 'x', label='2piR + g_h', color='red', markersize=6, markeredgewidth=2)
# axes[1].plot(nfit, fitN(nfit, J_N), '-', label=f'fit: J={J_N:.3f}')
axes.set_xlabel('n sts'); axes.set_ylabel('y [mm]'); axes.set_title('Stitches length vs knitted stitches (R fixed)')
axes.legend(loc='best')

plt.tight_layout()
plt.show()


# ------------------------- 2D fit ----------------------------
""" 
def fit2D(X, J):
    R, N = X
    # equivalent to writing
    # R = X[0]
    # N = X[1]
    return N *( 2 * np.pi * R + J)

# Combine into one dataset of 13 points total
R_data = np.concatenate([x_R, needle_N])
n_data = np.concatenate([needle_R, x_N])
y_data = np.concatenate([y_R, y_N])

X_data = np.vstack((R_data, n_data))  # shape (2, 13)

params_2D, cov_2D = curve_fit(fit2D, X_data, y_data)
J_2D = params_2D[0]
errJ_2D = np.sqrt(cov_2D[0, 0])

print(f"2D fit: J = {J_2D:.4f} ± {errJ_2D:.4f}")

# 3D plot for the 2D surface
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(R_data, n_data, y_data, color='red', label='data')

# build a surface grid for the fitted model
R_grid = np.linspace(R_data.min(), R_data.max(), 30)
n_grid = np.linspace(n_data.min(), n_data.max(), 30)
R_mesh, n_mesh = np.meshgrid(R_grid, n_grid)
y_mesh = n_mesh * 2 * np.pi * R_mesh + n_mesh * J_2D

ax.plot_surface(R_mesh, n_mesh, y_mesh, alpha=0.4, cmap='viridis')

ax.set_xlabel('R [mm]')
ax.set_ylabel('n [sts]')
ax.set_zlabel('y [mm]')
plt.show()
"""