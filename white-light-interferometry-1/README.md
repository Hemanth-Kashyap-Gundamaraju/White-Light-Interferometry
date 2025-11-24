### Project Structure
```
WhiteLightInterferometry/
│
├── wli_simulator.py
└── heightmap.csv  # This file should be generated using the HeightMapGenerator.py
```

### `wli_simulator.py`
```python
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

# WLI Simulation Parameters
lambda0 = 600.0   # central wavelength (nm)
Lc = 100.0        # coherence length (nm)
s_range = np.linspace(-300, 300, 200)  # reference mirror scan (nm)

# Convert height to nm scale
def _to_nm(z_surface, scale=100.0):
    return scale * z_surface

# Expand for broadcasting
def _expand_for_broadcast(z_surface_nm, s_range):
    z_exp = z_surface_nm[:, :, np.newaxis]         # (y, x, 1)
    s_exp = s_range[np.newaxis, np.newaxis, :]     # (1, 1, s)
    return z_exp, s_exp

# Compute Optical Path Difference (OPD)
def _compute_opd(z_exp, s_exp):
    return 2 * (z_exp - s_exp)

# Compute Degree of Coherence (Gaussian envelope)
def _compute_gamma(OPD, Lc):
    return np.exp(-(OPD**2) / (2 * Lc**2))

# Compute Interferogram Intensity
def _compute_intensity(gamma, OPD, lambda0):
    return 1 + gamma * np.cos((2 * np.pi / lambda0) * OPD)

# Simulate a White Light Interferogram
def simulate_interferogram(z_surface, lambda0=600.0, Lc=100.0, s_range=None):
    if s_range is None:
        s_range = np.linspace(-300, 300, 200)

    z_surface_nm = _to_nm(z_surface)
    z_exp, s_exp = _expand_for_broadcast(z_surface_nm, s_range)
    OPD = _compute_opd(z_exp, s_exp)

    # Degree of coherence
    gamma = _compute_gamma(OPD, Lc)
    
    # Compute intensity
    I = _compute_intensity(gamma, OPD, lambda0)
    
    return I, s_range

# Main execution
if __name__ == "__main__":
    try:
        heightmap = load_heightmap("heightmap.csv")
        print("Loaded heightmap.csv")
    except FileNotFoundError:
        print("Heightmap file not found. Please generate it first.")
        exit()

    # Run Simulation
    I, s_range = simulate_interferogram(heightmap, lambda0, Lc, s_range)

    # Visualization
    fig = plt.figure(figsize=(6, 9))
    
    # Intensity Pattern
    ax1 = fig.add_subplot(311)
    ax1.imshow(I[:, :, len(s_range) // 2], cmap='jet')
    ax1.set_title('Intensity Pattern')
    ax1.axis('off')

    # Annotations
    s1 = "Central Wavelength: 600 nm"
    s2 = "Coherence Length: 100 nm"
    ax2 = fig.add_subplot(312)
    ax2.axis('off')
    ax2.text(0.0, 0.6, s1, fontsize=12, fontweight='bold')
    ax3 = fig.add_subplot(313)
    ax3.axis('off')
    ax3.text(0.0, 0.5, s2, fontsize=12)

    plt.tight_layout()
    plt.show()
```

### Instructions to Run the Project
1. **Generate the Heightmap**: Before running the `wli_simulator.py`, ensure that you have generated the `heightmap.csv` using the `HeightMapGenerator.py` script.
2. **Run the Simulation**: Execute the `wli_simulator.py` script in your Python environment. This will load the heightmap, simulate the interferogram, and display the intensity pattern along with the annotations.

### Additional Notes
- Make sure you have the required libraries installed (`numpy`, `matplotlib`, `pandas`).
- You can customize the annotations and the appearance of the plots as needed.