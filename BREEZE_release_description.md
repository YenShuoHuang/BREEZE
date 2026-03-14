## BREEZE v1.0.0 — Initial Release

This is the first public release of **BREEZE (Bioclimatic Route Evaluation for Environmental haZard avoidancE)**, accompanying the paper:

> *BREEZE: Bioclimatic Route Evaluation for Environmental haZard avoidancE*, Huang Y.-S., Llaguno-Munitxa M., Manoli G. (under review, Sustainable Cities and Society)

---

### What's Included

| File | Description |
|------|-------------|
| `2_2_1_AppA_DSM_object_removing.ipynb` | Vehicle removal from DSM using circularity filter (Appendix A) |
| `2_2_2_AppB_LULC_preprocessing.ipynb` | Multi-source LULC generation for UMEP (Appendix B) |
| `2_2_3_Static_dataset_2_nc.ipynb` | GHS Built-up Volume to NetCDF on 1km grid (Section 2.2) |
| `2_3_1_Meteorological_dataset_2_nc.ipynb` | UrbClim meteorological data consolidation to NetCDF (Section 2.3) |
| `2_3_2_DSM_split_1km.ipynb` | DSM resampling and per-grid clipping in QGIS (Section 2.3) |
| `2_3_3_UrbClim_100m_2_1km.ipynb` | UrbClim meteorological regridding 100m -> 1km (Section 2.3) |
| `2_3_4_UrbClim1km_2_epw.ipynb` | Meteorological data conversion to EPW format for SOLWEIG (Section 2.3) |
| `SOLWEIG.py` | HPC batch SOLWEIG runner and UTCI computation (Section 2.3) |
| `SOLWEIG.sh` | SLURM job array script for HPC deployment (Section 2.3) |
| `2_3_6_UTCI_postprocessing.ipynb` | UTCI merging, heat/cold degree hours accumulation, boundary clipping (Section 2.3) |
| `2_6_Avoidance_Routing.ipynb` | Avoidance route mapping web application with dual UTCI thresholds (Section 2.6) |

---

### Case Study

Applied to the **Brussels-Capital Region (BCR)**, Belgium, for the year 2011:
- 178 grid cells at 1 km x 1 km
- UTCI simulated at 2 m spatial resolution across 730 time steps
- Soft mobility network segmented into 50 m segments with 7 m buffer
- 9 route segment clusters identified for urban intervention planning
- Dual UTCI thresholds: moderate heat stress (> 26 °C) and strong heat stress (> 32 °C)

---

### Requirements

- Python >= 3.8
- QGIS 3.28.1 with UMEP plugin
- pythermalcomfort, rasterio, netCDF4, geopandas, opencv-python, openrouteservice
- SLURM-based HPC cluster (for city-scale SOLWEIG runs)

See `README.md` for full installation instructions, data sources, and step-by-step usage guide.

---

### Related Publication

If you use this code, please cite:

Huang, Y.-S., Llaguno-Munitxa, M., Manoli, G. (2025). Towards Dynamic Urban Environmental Exposure Assessments: A Case Study of the Brussels Capital Region. *Journal of Physics: Conference Series*, 3140(12), 122002. https://doi.org/10.1088/1742-6596/3140/12/122002
