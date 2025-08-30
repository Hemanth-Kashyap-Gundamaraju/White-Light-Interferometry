# White Light Interferometry
To simulate the vertical scanning white-light interferometer we need to understand the setup and Physics behind it
### Optical Setup: White-Light Interferometer

- A **broadband light source** (e.g., LED or halogen) is split by a beamsplitter into two optical paths:

  1. **Reference arm**  
     The beam reflects from a flat reference mirror. The mirror is mounted on a translation stage (often piezo-driven), so its position can be scanned by a distance *s*.  

  2. **Sample arm**  
     The beam reflects from the test surface, whose local height at each pixel is *z(x,y)*.

- After reflection, the two beams recombine at the beamsplitter and interfere on the detector (camera).

- The relative delay between the two arms determines the **Optical Path Difference (OPD)**:

  $$
  \text{OPD}(x,y,s) = 2 \,[z(x,y) - s]
  $$

  The factor of 2 accounts for the round trip of the light.

- Because the source is broadband, interference fringes only appear when the OPD is within the **coherence length** of the source.  
  As the reference mirror is scanned, each pixel records a modulated intensity signal (a *fringe packet*) that is centered when:

  $$
  s \approx z(x,y)
  $$