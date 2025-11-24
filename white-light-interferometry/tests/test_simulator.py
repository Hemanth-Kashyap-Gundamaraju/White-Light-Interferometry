import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load heightmap from CSV
def load_heightmap(filename="heightmap.csv"):
    data = pd.read_csv(filename)
    max_x = int(data["x"].max()) + 1
    max_y = int(data["y"].max()) + 1
    Z = np.zeros((max_y, max_x))
    for _, row in data.iterrows():
        x = int(row["x"])
        y = int(row["y"])
        z = row["z"]
        Z[y, x] = z
    return Z

# Simulation parameters
lambda0 = 600.0  # central wavelength (nm)
Lc = 100.0       # coherence length (nm)
s_range = np.linspace(-300, 300, 200)  # reference mirror scan (nm)

# Convert height to nm scale
def to_nm(z_surface, scale=100.0):
    return scale * z_surface

# Expand for broadcasting
def expand_for_broadcast(z_surface_nm, s_range):
    z_exp = z_surface_nm[:, :, np.newaxis]  # (y, x, 1)
    s_exp = s_range[np.newaxis, np.newaxis, :]  # (1, 1, s)
    return z_exp, s_exp

# Compute optical path difference
def compute_opd(z_exp, s_exp):
    return 2 * (z_exp - s_exp)

# Compute degree of coherence
def compute_gamma(OPD, Lc):
    return np.exp(-(OPD**2) / (2 * Lc**2))

# Compute interferogram intensity
def compute_intensity(gamma, OPD, lambda0):
    return 1 + gamma * np.cos((2 * np.pi / lambda0) * OPD)

# Simulate the interferogram
def simulate_interferogram(z_surface, lambda0=600.0, Lc=100.0, s_range=None):
    if s_range is None:
        s_range = np.linspace(-300, 300, 200)

    z_surface_nm = to_nm(z_surface)
    z_exp, s_exp = expand_for_broadcast(z_surface_nm, s_range)
    OPD = compute_opd(z_exp, s_exp)

    gamma = compute_gamma(OPD, Lc)
    I = compute_intensity(gamma, OPD, lambda0)

    return I, s_range

# Main execution
if __name__ == "__main__":
    try:
        heightmap = load_heightmap("heightmap.csv")
        print("Loaded heightmap.csv")
    except FileNotFoundError:
        # Fallback to synthetic Gaussian surface
        size = 64
        x = np.linspace(-1, 1, size)
        X, Y = np.meshgrid(x, x)
        heightmap = 0.5 * np.exp(-(X**2 + Y**2) / 0.2)
        print("Using synthetic Gaussian surface")

    # Run the simulation
    I, s_range = simulate_interferogram(heightmap, lambda0, Lc)

    # Visualization
    fig = plt.figure(figsize=(6, 9))
    
    # Intensity pattern
    ax1 = fig.add_subplot(311)
    ax1.imshow(I[:, :, len(s_range) // 2], cmap='jet')
    ax1.set_title('Intensity Pattern')
    ax1.axis('off')

    # Additional text annotations
    ax2 = fig.add_subplot(312)
    ax2.axis('off')
    ax2.text(0.0, 0.6, "White Light Interferogram Simulation", fontsize=12, fontweight='bold')

    ax3 = fig.add_subplot(313)
    ax3.axis('off')
    ax3.text(0.0, 0.5, "Central Wavelength: 600 nm\nCoherence Length: 100 nm", fontsize=10)

    plt.tight_layout()
    plt.show()