import numpy as np
import pyvista as pv

# _______________________________ constants ______________________________________

r = 0.1
g_h = 0.7
g_v = 0.64 
A = 3 * r / 2
B = g_h / (2 * np.pi)
C = g_h / 4
D = (g_v + 2* r)/ 2
E = r
F = E
R = 0.3

N_POINTS = 300      # samples along the centerline (more = smoother tube)
N_SIDES = 24        # sides of the tube cross-section
SHOW_EDGES = False  # True to draw the mesh wireframe like the matplotlib version

# _______________________________ geometry _______________________________________

# Parameter along the curve
t = np.linspace(-np.pi / 2, np.pi / 2, N_POINTS)

# Centerline of one strand, and its mirror image (x -> -x)
X0 = -A * np.sin(2 * t) + B * t - C
Y0 = D * np.sin(t)
Z0 = E * np.cos(2 * t) + F

strand_0 = np.column_stack([X0, Y0, Z0])
strand_1 = np.column_stack([-X0, Y0, Z0])


def make_tube(points, radius=r, n_sides=N_SIDES):
    """Closed-ended tube of a given radius around a polyline."""
    line = pv.lines_from_points(points)
    return line.tube(radius=radius, n_sides=n_sides, capping=True)


tube_0 = make_tube(strand_0)
tube_1 = make_tube(strand_1)

# Each "stitch" is the pair of strands, translated and coloured.
stitches = {
    "lightblue": (0.0,   0.0,      "lightblue", 1.0),
    "yellow":    (-g_h,  0.0,      "yellow",    1.0),
    "orange":    (+g_h,  0.0,      "orange",    1.0),
    "darkgreen": (0.0,   -g_v / 2, "darkgreen", 1.0),
    "red":       (-g_h,  -g_v / 2, "red",       1.0),
    "pink":      (+g_h,  -g_v / 2, "pink",      1.0),
}


# _______________________________ scene __________________________________________

def build_plotter(off_screen=False):
    pl = pv.Plotter(off_screen=off_screen, window_size=(1000, 800))
    pl.set_background("white")

    for name, (dx, dy, color, opacity) in stitches.items():
        for tube in (tube_0, tube_1):
            pl.add_mesh(
                tube.translate((dx, dy, 0.0), inplace=False),
                color=color,
                opacity=opacity,
                smooth_shading=True,
                show_edges=SHOW_EDGES,
                edge_color="k",
                line_width=0.5,
                specular=0.0,
            )

    pl.show_bounds(
        bounds=(-1.4, 1.4, -1.4, 1.4, -0.7, 0.7),
        xtitle="x [cm]", ytitle="y [cm]", ztitle="z [cm]",
        color="black", grid="back", location="outer",
    )
    pl.add_axes()
    return pl

def record_custom_spline_path(filename="stitches_custom.gif", n_frames=300, fps=30,
                               hold_frames=30):
    """Animation that locks on the first (high isometric) view for a moment,
    then glides along a smooth spline path through the rest of the waypoints.

    hold_frames : how many frames to hold still on the opening isometric view
                  before the camera starts moving (at fps=30, 30 frames = 1 second).
    """
    pl = build_plotter(off_screen=True)
    
    if filename.endswith(".gif"):
        pl.open_gif(filename, fps=fps)
    else:
        pl.open_movie(filename, framerate=fps)

    # Key camera waypoints pushed outward (radius ~ 3.2+ units)
    # The target center of the stitches is near (0, -0.16, 0.1)
    target = (0.0, -0.16, 0.1)

    key_points = np.array([
        [3.0, 3.0, 2.2],    # High isometric view
        [0.0, 3.5, 0.5],    # Front view (safe distance outside bounds)
        [-3.0, 2.5, -1.8],  # Low-angle view looking up
        [-3.2, -3.2, 0.5],  # Rear/side angle
        [3.0, 3.0, 2.2]     # Smooth loop back to start
    ])

    # --- 1. Lock the camera on the opening high isometric view -------------
    pl.camera_position = [key_points[0], target, (0, 0, 1)]
    for _ in range(hold_frames):
        pl.write_frame()

    # --- 2. Glide smoothly through the remaining waypoints ------------------
    # Generate smooth curved camera path through waypoints
    path = pv.Spline(key_points, n_points=n_frames)
    
    for point in path.points:
        pl.camera_position = [
            point,   # Camera location
            target,  # Focal point (center of mass of the stitches)
            (0, 0, 1)
        ]
        pl.write_frame()

    pl.close()
    print(f"Animation saved to {filename}")


# _______________________________ main ___________________________________________

if __name__ == "__main__":
    # 1. Open Interactive Viewer (Close the window when you're done viewing)
    print("Opening interactive window. Close the window to generate the GIF...")
    pl = build_plotter()
    pl.camera_position = "iso"
    pl.enable_trackball_style()  # Allows free 360-degree rotation
    pl.show()

    # 2. Render and save the orbital animation GIF after the interactive window is closed
    print("Generating orbit animation...")
    try:
        record_custom_spline_path("stitches_showcase.gif", n_frames=180, fps=30)
    except ModuleNotFoundError:
        print("\n[Error] Missing animation library! Run: pip install imageio imageio-ffmpeg")
