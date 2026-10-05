import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from scipy.integrate import quad

# _______________________________ curve length ___________________________________

# def arc_length_3d(x_expr, y_expr, z_expr, t_sym, a, b):
#     # Exact symbolic derivatives
#     dx = sp.diff(x_expr, t_sym)
#     dy = sp.diff(y_expr, t_sym)
#     dz = sp.diff(z_expr, t_sym)
#  
#     speed_expr = sp.sqrt(dx**2 + dy**2 + dz**2)
#     # Turn into a fast numerical function
#     speed_func = sp.lambdify(t_sym, speed_expr, modules="numpy")
#  
#     length, abs_err = quad(speed_func, a, b)
#     return length, abs_err
# 
# Parametro lungo la curva
t = np.linspace(-np.pi/2, np.pi/2, 100)

# Costanti
r = 0.1
g_h = 0.7
g_v = 0.64 
A = 3 * r / 2
B = g_h / (2 * np.pi)
C = g_h / 4
D = (g_v + 2 * r) / 2
E = r 
F = E
R = 0.3

# Curva centrale (X0, Y0, Z0)
X0 = -A * np.sin(2 * t) + B * t - C
Y0 = D * np.sin(t)
Z0 = E * np.cos(2 * t) + F

X1 = -X0
Y1 = Y0
Z1 = Z0

X0P = -X0
Y0P = Y0
Z0P = -Z0

X1P = X0
Y1P = Y0
Z1P = -Z0

# Calcoliamo le derivate (vettore tangente) usando np.gradient
dX = np.gradient(X0, t)
dY = np.gradient(Y0, t)
dZ = np.gradient(Z0, t)

dX1 = np.gradient(X1, t)
dY1 = np.gradient(Y1, t)
dZ1 = np.gradient(Z1, t)

############### P ##################

dXP = np.gradient(X0P, t)
dYP = np.gradient(Y0P, t)
dZP = np.gradient(Z0P, t)

dX1P = np.gradient(X1P, t)
dY1P = np.gradient(Y1P, t)
dZ1P = np.gradient(Z1P, t)
###################################

# Normalizziamo il vettore tangente T
mag = np.sqrt(dX**2 + dY**2 + dZ**2)
Tx, Ty, Tz = dX/mag, dY/mag, dZ/mag

mag1 = np.sqrt(dX1**2 + dY1**2 + dZ1**2)
Tx1, Ty1, Tz1 = dX1/mag1, dY1/mag1, dZ1/mag1

############### P ##################
magP = np.sqrt(dXP**2 + dYP**2 + dZP**2)
TxP, TyP, TzP = dXP/magP, dYP/magP, dZP/magP

mag1P = np.sqrt(dX1P**2 + dY1P**2 + dZ1P**2)
Tx1P, Ty1P, Tz1P = dX1P/mag1P, dY1P/mag1P, dZ1P/mag1P
###################################

# Troviamo un vettore normale N ortogonale alla tangente (usando il prodotto vettoriale con l'asse Z)
Nx = -Ty
Ny = Tx
Nz = np.zeros_like(Tx)
magN = np.sqrt(Nx**2 + Ny**2 + Nz**2)
Nx, Ny, Nz = Nx/magN, Ny/magN, Nz/magN

Nx1 = -Ty1
Ny1 = Tx1
Nz1 = np.zeros_like(Tx1)
magN1 = np.sqrt(Nx1**2 + Ny1**2 + Nz1**2)
Nx1, Ny1, Nz1 = Nx1/magN1, Ny1/magN1, Nz1/magN1

############### P ##################

NxP = -TyP
NyP = TxP
NzP = np.zeros_like(TxP)
magNP = np.sqrt(NxP**2 + NyP**2 + NzP**2)
NxP, NyP, NzP = NxP/magNP, NyP/magNP, NzP/magNP

Nx1P = -Ty1P
Ny1P = Tx1P
Nz1P = np.zeros_like(Tx1P)
magN1P = np.sqrt(Nx1P**2 + Ny1P**2 + Nz1P**2)
Nx1P, Ny1P, Nz1P = Nx1P/magN1P, Ny1P/magN1P, Nz1P/magN1P
###################################

# Vettore binormale B = T x N
Bx = Ty * Nz - Tz * Ny
By = Tz * Nx - Tx * Nz
Bz = Tx * Ny - Ty * Nx

Bx1 = Ty1 * Nz1 - Tz1 * Ny1
By1 = Tz1 * Nx1 - Tx1 * Nz1
Bz1 = Tx1 * Ny1 - Ty1 * Nx1

############### P ##################

BxP = TyP * NzP - TzP * NyP
ByP = TzP * NxP - TxP * NzP
BzP = TxP * NyP - TyP * NxP

Bx1P = Ty1P * Nz1P - Tz1P * Ny1P
By1P = Tz1P * Nx1P - Tx1P * Nz1P
Bz1P = Tx1P * Ny1P - Ty1P * Nx1P
###################################

# 2. Secondo parametro per la sezione circolare del tubo (theta da 0 a 2*pi)
theta = np.linspace(0, 2 * np.pi, 20)
T_grid, Theta_grid = np.meshgrid(t, theta)

# Ripetiamo i vettori centrali per adattarli alla griglia 2D (tramite broadcasting o tile)
X0_m = np.tile(X0, (len(theta), 1))
Y0_m = np.tile(Y0, (len(theta), 1))
Z0_m = np.tile(Z0, (len(theta), 1))

Nx_m = np.tile(Nx, (len(theta), 1))
Ny_m = np.tile(Ny, (len(theta), 1))
Nz_m = np.tile(Nz, (len(theta), 1))

Bx_m = np.tile(Bx, (len(theta), 1))
By_m = np.tile(By, (len(theta), 1))
Bz_m = np.tile(Bz, (len(theta), 1))

############### P ##################

X0_mP = np.tile(X0P, (len(theta), 1))
Y0_mP = np.tile(Y0P, (len(theta), 1))
Z0_mP = np.tile(Z0P, (len(theta), 1))

Nx_mP = np.tile(NxP, (len(theta), 1))
Ny_mP = np.tile(NyP, (len(theta), 1))
Nz_mP = np.tile(NzP, (len(theta), 1))

Bx_mP = np.tile(BxP, (len(theta), 1))
By_mP = np.tile(ByP, (len(theta), 1))
Bz_mP = np.tile(BzP, (len(theta), 1))
###################################

######################################################

X0_m1 = np.tile(X1, (len(theta), 1))
Y0_m1 = np.tile(Y1, (len(theta), 1))
Z0_m1 = np.tile(Z1, (len(theta), 1))

Nx_m1 = np.tile(Nx1, (len(theta), 1))
Ny_m1 = np.tile(Ny1, (len(theta), 1))
Nz_m1 = np.tile(Nz1, (len(theta), 1))

Bx_m1 = np.tile(Bx1, (len(theta), 1))
By_m1 = np.tile(By1, (len(theta), 1))
Bz_m1 = np.tile(Bz1, (len(theta), 1))

############### P ##################

X0_m1P = np.tile(X1P, (len(theta), 1))
Y0_m1P = np.tile(Y1P, (len(theta), 1))
Z0_m1P = np.tile(Z1P, (len(theta), 1))

Nx_m1P = np.tile(Nx1P, (len(theta), 1))
Ny_m1P = np.tile(Ny1P, (len(theta), 1))
Nz_m1P = np.tile(Nz1P, (len(theta), 1))

Bx_m1P = np.tile(Bx1P, (len(theta), 1))
By_m1P = np.tile(By1P, (len(theta), 1))
Bz_m1P = np.tile(Bz1P, (len(theta), 1))
###################################

# Superficie tridimensionale del tubo
X = X0_m + r * (np.cos(Theta_grid) * Nx_m + np.sin(Theta_grid) * Bx_m)
Y = Y0_m + r * (np.cos(Theta_grid) * Ny_m + np.sin(Theta_grid) * By_m)
Z = Z0_m + r * (np.cos(Theta_grid) * Nz_m + np.sin(Theta_grid) * Bz_m)

X11 = X0_m1 + r * (np.cos(Theta_grid) * Nx_m1 + np.sin(Theta_grid) * Bx_m1)
Y11 = Y0_m1 + r * (np.cos(Theta_grid) * Ny_m1 + np.sin(Theta_grid) * By_m1)
Z11 = Z0_m1 + r * (np.cos(Theta_grid) * Nz_m1 + np.sin(Theta_grid) * Bz_m1)

############### P ##################
XP = X0_mP + r * (np.cos(Theta_grid) * Nx_mP + np.sin(Theta_grid) * Bx_mP)
YP = Y0_mP + r * (np.cos(Theta_grid) * Ny_mP + np.sin(Theta_grid) * By_mP)
ZP = Z0_mP + r * (np.cos(Theta_grid) * Nz_mP + np.sin(Theta_grid) * Bz_mP)

X11P = X0_m1P + r * (np.cos(Theta_grid) * Nx_m1P + np.sin(Theta_grid) * Bx_m1P)
Y11P = Y0_m1P + r * (np.cos(Theta_grid) * Ny_m1P + np.sin(Theta_grid) * By_m1P)
Z11P = Z0_m1P + r * (np.cos(Theta_grid) * Nz_m1P + np.sin(Theta_grid) * Bz_m1P)
###################################

# Visualizzazione 3D
fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim3d(-1.4, 1.4)
ax.set_ylim3d(-1.4, 1.4)
ax.set_zlim3d(-1.4, 1.4)
ax.set_xlabel("x [cm]")
ax.set_ylabel("y [cm]")
ax.set_zlabel("z [cm]")

# Disegna la superficie tubolare
ax.plot_surface(X, Y, Z, color='lightblue', edgecolor='k', linewidth=0.1, alpha=0.5)
ax.plot_surface(X11, Y11, Z11, color='lightblue', edgecolor='k', linewidth=0.1, alpha=0.5)
"""
ax.plot_surface(XP - g_h, YP, ZP, color='yellow', edgecolor='k', linewidth=0.1, alpha=0.5)
ax.plot_surface(X11P - g_h, Y11P, Z11P, color='yellow', edgecolor='k', linewidth=0.1, alpha=0.5)
"""
ax.plot_surface(X - g_h, Y, Z, color='yellow', edgecolor='k', linewidth=0.1, alpha=0.5)
ax.plot_surface(X11 - g_h, Y11, Z11, color='yellow', edgecolor='k', linewidth=0.1, alpha=0.5)

ax.plot_surface(X + g_h, Y, Z, color='orange', edgecolor='k', linewidth=0.1, alpha=0.9)
ax.plot_surface(X11 + g_h, Y11, Z11, color='orange', edgecolor='k', linewidth=0.1, alpha=0.9)

ax.plot_surface(X, Y - g_v/2, Z, color='darkgreen', edgecolor='k', linewidth=0.1, alpha=0.9)
ax.plot_surface(X11, Y11 - g_v/2, Z11, color='darkgreen', edgecolor='k', linewidth=0.1, alpha=0.9)

ax.plot_surface(X - g_h, Y - g_v/2, Z, color='red', edgecolor='k', linewidth=0.1, alpha=0.9)
ax.plot_surface(X11 - g_h, Y11 - g_v/2, Z11, color='red', edgecolor='k', linewidth=0.1, alpha=0.9)

ax.plot_surface(X + g_h, Y - g_v/2, Z, color='pink', edgecolor='k', linewidth=0.1, alpha=0.9)
ax.plot_surface(X11 + g_h, Y11 - g_v/2, Z11, color='pink', edgecolor='k', linewidth=0.1, alpha=0.9)


# r
ax.plot([1.1, 1.1], [-0.32 - r, -0.32], [0, 0], linewidth=1)
ax.text(1.1, -0.32 - r/2, 0.05, "r")
# g_h
ax.plot([-0.345 + g_h, 0.345 + g_h], [0.5, 0.5], [r, r], linewidth=1)
ax.text(g_h, 0.5, r+0.05, "w")
#g_v
ax.plot([1.1, 1.1], [-0.32 + r, 0.32 + r], [r, r], linewidth=1)
ax.text(1.1, r, r+0.05, "h")
# h
ax.plot([1.1, 1.1], [0.5, 0.5], [-r, 3*r], linewidth=1)
ax.text(1.1, 0.55, 0.0, "d")

plt.show()


# t1 = sp.symbols("t", real=True)
# X0_sym = -A * sp.sin(2 * t1) + B * t1 - C
# Y0_sym = D * sp.sin(t1)
# Z0_sym = E * sp.cos(2 * t1) + F
# 
# L, err = arc_length_3d(X0_sym, Y0_sym, Z0_sym, t1, -np.pi/2, np.pi/2)
# L_old = 3*np.pi*R
# L_new = 2*np.pi*R + g_h

# print(f"Arc length ≈ {2*L:.6f}  (estimated error ≈ {err:.2e})")
# print(f"Old model 3PiR = {L_old:.6f}")
# print(f"New model 2PiR + g_h =  {L_new:.6f}")

 