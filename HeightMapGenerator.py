import csv
import noise
import numpy as np
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# #Perlin Noise
# # Parameters
# width = 100                                                         # number of x points
# height = 100                                                        # number of y points
# scale = 50.0                                                        # zoom factor for noise
# octaves = 4                                                         # layers of detail (more octaves = more detail)
# persistence = 0.5                                                   # amplitude multiplier for each layer (more persistence = rougher terrain (small details are strong), less persistence = smoother terrain (fine details are faint))
# lacunarity = 2.0                                                    # frequency multiplier for each layer (more lacunarity = chaotic, noisy terrain, less lacunarity = smoother, gradual terrain)
# base = random.randint(0, 100000)                                    # random seed for noise

# # Generate heightmap using 3D Perlin noise
# heightmap = np.zeros((height, width))

# for y in range(height):
#     for x in range(width):
#         z_val = noise.pnoise3(
#             x / scale,
#             y / scale,
#             0.5,                # fixed z-slice of 3D noise
#             octaves=octaves,
#             persistence=persistence,
#             lacunarity=lacunarity,
#             repeatx=width,
#             repeaty=height,
#             base=base
#         )
#         # Normalize result to [0,1]
#         heightmap[y][x] = (z_val + 0.5)

# print("Parameters used: width =", width, "height =", height, "scale =", scale, "octaves =", octaves, "persistence =", persistence, "lacunarity =", lacunarity, "base =", base)



# #Worley Noise
# # Parameters
# width = 100
# height = 100
# num_points = 30                        # number of random feature points
# distance_metric = "F2"              # options: "F1", "F2", "F2-F1"

# # Generate random feature points inside the grid
# feature_points = np.random.rand(num_points, 2) * [width, height]

# # Worley noise calculation
# heightmap = np.zeros((height, width))
# for y in range(height):
#     for x in range(width):
#         # Distances to all feature points
#         distances = np.sqrt(((feature_points - [x, y])**2).sum(axis=1))
#         distances.sort()  # sort from nearest to farthest

#         if distance_metric == "F1":
#             value = distances[0]            # nearest point
#         elif distance_metric == "F2":
#             value = distances[1] if len(distances) > 1 else distances[0]
#         elif distance_metric == "F2-F1":
#             if len(distances) > 1:
#                 value = distances[1] - distances[0]
#             else:
#                 value = 0
#         else:
#             raise ValueError("Invalid distance_metric, use 'F1', 'F2', or 'F2-F1'")

#         heightmap[y, x] = value

# # Normalize to [0,1]
# heightmap = (heightmap - heightmap.min()) / (heightmap.max() - heightmap.min())



#Simplex FBM Noise
# Parameters
width = 150
height = 150
scale = 100.0                           # zoom factor
octaves = 6                             # number of layers
persistence = 0.5                       # amplitude falloff
lacunarity = 2.0                        # frequency multiplier
base = random.randint(0, 100000)        # random seed

# Generate FBM heightmap using Simplex noise
heightmap = np.zeros((height, width))

for y in range(height):
    for x in range(width):
        nx = x / scale
        ny = y / scale

        # snoise2 handles FBM internally if octaves>1
        z_val = noise.snoise2(nx, ny,
                        octaves=octaves,
                        persistence=persistence,
                        lacunarity=lacunarity,
                        repeatx=width,
                        repeaty=height,
                        base=base)
        # Normalize to [0,1]
        heightmap[y][x] = (z_val + 1) / 2.0






# Save CSV with headers z,x,y
with open("heightmap.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["z", "x", "y"])
    for y in range(height):
        for x in range(width):
            z = heightmap[y][x]
            writer.writerow([z, x, y])

print("Heightmap saved to heightmap.csv")



# -------------------------------
# Visualization using matplotlib
# -------------------------------

X, Y = np.meshgrid(range(width), range(height))
Z = heightmap

fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(121, projection="3d")

ax.plot_surface(X, Y, Z, cmap="viridis", linewidth=0, antialiased=False)


# ax.set_title("3D Perlin Noise Heightmap")
# ax.set_title(f"3D Worley Noise ({distance_metric}) Heightmap")
ax.set_title("3D Simplex FBM Noise Heightmap")

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z (height)")



# 2D heatmap
ax2 = fig.add_subplot(122)
heatmap_plot = ax2.imshow(Z, cmap="viridis", origin="lower")

# ax2.set_title(f"2D Perlin Noise)")
# ax2.set_title(f"2D Worley Noise ({distance_metric})")
ax2.set_title("2D Simplex FBM Noise")

plt.colorbar(heatmap_plot, ax=ax2, fraction=0.046, pad=0.04)


plt.show()
