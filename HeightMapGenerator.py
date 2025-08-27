import csv
import noise
import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameters
width = 100                                                         # number of x points
height = 100                                                        # number of y points
scale = 50.0                                                        # zoom factor for noise
octaves = 4                                                         # layers of detail (more octaves = more detail)
persistence = 0.5                                                   # amplitude multiplier for each layer (more persistence = rougher terrain (small details are strong), less persistence = smoother terrain (fine details are faint))
lacunarity = 2.0                                                    # frequency multiplier for each layer (more lacunarity = chaotic, noisy terrain, less lacunarity = smoother, gradual terrain)
base = random.randint(0, 100000)                                    # random seed for noise

# Generate heightmap using 3D Perlin noise
heightmap = np.zeros((height, width))

for y in range(height):
    for x in range(width):
        z_val = noise.pnoise3(
            x / scale,
            y / scale,
            0.5,                # fixed z-slice of 3D noise
            octaves=octaves,
            persistence=persistence,
            lacunarity=lacunarity,
            repeatx=width,
            repeaty=height,
            base=base
        )
        # Normalize result to [0,1]
        heightmap[y][x] = (z_val + 0.5)

# Write to CSV with headers z,x,y
with open("heightmap.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["z", "x", "y"])  # headers
    
    for y in range(height):
        for x in range(width):
            z = heightmap[y][x]
            writer.writerow([z, x, y])

print("Heightmap saved to heightmap.csv")
print("Parameters used: width =", width, "height =", height, "scale =", scale, "octaves =", octaves, "persistence =", persistence, "lacunarity =", lacunarity, "base =", base)

# -------------------------------
# Visualization using matplotlib
# -------------------------------
X, Y = np.meshgrid(range(width), range(height))
Z = heightmap

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")

ax.plot_surface(X, Y, Z, cmap="viridis", linewidth=0, antialiased=False)

ax.set_title("3D Noise Heightmap")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z (height)")

plt.show()
