This project was completed as part of the OELP (Open‑Ended Laboratory Project) under the guidance of Dr. Arvind Ajoy during the Fall Semester of 2025 at IIT Palakkad

# White‑Light Interferometry (WLI) Simulation

This repository contains a complete simulation workflow for **White‑Light Interferometry (WLI)**, including synthetic heightmap generation, broadband interference modeling, fringe visualization, and surface height reconstruction.  
The simulation is implemented primarily in a **Jupyter Notebook**, with an auxiliary Python script for generating synthetic surface heightmaps using noise‑based methods.

This project was completed as part of the **Open‑Ended Laboratory Project (OELP)** under the guidance of **Dr. Arvind Ajoy**, **IIT Palakkad**, during the **Fall Semester of 2025**.

---

## Overview

White‑light interferometry uses the short coherence length of broadband light to perform **high‑resolution surface profiling**.  
This project simulates the essential behaviour of a Michelson‑type interferometer using:

- a heightmap representing the sample surface,
- a broadband spectral model,
- a reference mirror scan,
- and an added linear tilt for fringe visibility.

Outputs include interferograms, fringe waveforms, and reconstructed surface heightmaps.

---

## Useful Links

https://www.researchgate.net/publication/339084730_Mirau-based_line-field_confocal_optical_coherence_tomography
https://www.researchgate.net/publication/258294713_Low_coherent_Linnik_interferometer_optimized_for_use_in_nano-measuring_machines
https://www.researchgate.net/figure/Michelson-a-and-Mirau-b-interference-objectives-incorporating-a-microscope-objective_fig2_339084730
https://youtu.be/v8gaEqHa1r0?si=nAGZB5FYdhIW1oze
https://www.youtube.com/watch?v=YxO5l2tML7o
https://www.youtube.com/playlist?list=PLZ2ps__7DhBa5xCmncgH7kPqLqMBq7xlu
https://www.youtube.com/watch?v=yMeRAg61_Wc

---

## Theory

- White Light Interferometry works on the principle of wave interference between a reference beam and the beam reflected off the sample, the changes in path length due to height variations cause a path difference which can be calculated using the interference patterns recorded by the camera.
- To improve precision, we use a Mirau Objective (alternatively a Michelson Objective) which has the reference mirror as well as a beam splitter within the microscope objective to prevent large path differences
- White light consists of a broad spectrum of wavelengths, therefore it's coherence length is low. Due to this, the interference patterns are only generated when the path difference is extremely small (with the coherence length). To solve for this, we attach our sample on high precision optical rails which allow for adjusting the sample over the optical axis to scan across the surface of the sample. The intensity at each pixel gives us the necessary information to reverse engineer the height of the sample at that point.
- At each pixel, the position of maximum fringe contrast (the “coherence peak”) is recorded. This peak indicates the point where the two beams have equal optical path length. The vertical position of this coherence peak corresponds to the height of the sample surface at that point.

# Calculation of Intensity
- We computed the optical path difference OPD = 2·(z − s) for each mirror position.
- We applied a Gaussian coherence envelope γ(OPD) = exp(−OPD²/(2·Lc²)), and formed the interference phase φ(λ) = 2π·OPD/λ.
- The spectrally-integrated intensity is then I(y,x,s) = Σλ S(λ)·[1 + V0·cos(φ(λ))] (with S(λ) a Gaussian or measured source spectrum), which produces short fringe packets centred where s ≈ z.
