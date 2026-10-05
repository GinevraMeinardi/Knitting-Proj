import numpy as np 
import matplotlib.pyplot as plt
import math

np.random.seed(0)  # reproducible control points for this demo


# coordinates for our bezier curve
x = np.random.random_sample((3,))
y = np.random.random_sample((3,))
z = np.random.random_sample((3,))

# number of points in my curve
CELLS = 100
# other useful variables
nCPTS = np.size(x,0)
n = nCPTS - 1       # number of segments
i = 0               # control point counter
t = np.linspace(0,1,CELLS)   # parameter
b = []                       # empty matrix for Bernestein polynomial

xBezier = np.zeros((1,CELLS))
yBezier = np.zeros((1,CELLS))
zBezier = np.zeros((1,CELLS))

# Binomial Coefficients
def Ni(n,i):
    return np.math.factorial(n) / (np.math.factorial(i) * np.math.factorial(n-i))

# Bernstein Basis Polynomial
def basisFunction(n,i,t):
    J = np.array(Ni(n,i) * ( t**i ) * (1 - t) ** (n - i ))
    return J

# Main Loop
for k in range(0, nCPTS):
    b.append(basisFunction(n, k, t))
    
    # Bezier curve calculation
    xBezier = basisFunction(n, k, t) * x[k] + xBezier
    yBezier = basisFunction(n, k, t) * y[k] + yBezier
    zBezier = basisFunction(n, k, t) * z[k] + zBezier
    i += 1

# plotting
fig = plt.figure(figsize=(12, 5))
ax2 = fig.add_subplot(1, 2, 2, projection="3d")
ax2.plot(xBezier[0], yBezier[0], zBezier[0], color="crimson", linewidth=2, label="Bezier curve")
ax2.scatter(x, y, z, color="black", s=40, label="control points")
ax2.plot(x, y, z, color="gray", linestyle="--", linewidth=1)  # control polygon
ax2.set_title("Actual 3D Bezier curve")
ax2.legend()

plt.tight_layout()
plt.show()