## BREEZE v1.0.0 — Initial Release

This is the first public release of **BREEZE (Bioclimatic Route Evaluation for Environmental haZard avoidancE)**, accompanying the paper:

> *BREEZE: Bioclimatic Route Evaluation for Environmental haZard avoidancE*, Huang Y.-S., Llaguno-Munitxa M., Manoli G. (under review, Sustainable Cities and Society)

---

### What's Included

| File | Description |
|------|-------------|
| `2_2_AppA_DSM_preprocessing.ipynb` | DSM/DTM pre-processing and vehicle removal (Appendix A) |
| `2_2_AppB_LULC_preprocessing.ipynb` | Multi-source LULC generation for UMEP (Appendix B) |
| `2_3_UrbClim_100m_2_1km.ipynb` | UrbClim meteorological regridding 100m → 1km (Section 2.3) |
| `2_3_UrbClim1km_2_epw.ipynb` | Meteorological data conversion to EPW format (Section 2.3) |
| `SOLWEIG.py` | HPC batch SOLWEIG runner and UTCI computation (Section 2.3) |
| `SOLWEIG.sh` | SLURM job array script for HPC deployment (Section 2.3) |
| `2_3_UTCI_postprocessing.ipynb` | UTCI merging, heat/cold degree hours accumulation, segment extraction (Section 2.3) |
| `2_6_Avoidance_Routing.ipynb` | Avoidance route mapping web application (Section 2.6) |

---

### Case Study

Applied to the **Brussels-Capital Region (BCR)**, Belgium, for the year 2011:
- 178 grid cells at 1 km × 1 km
- UTCI simulated at 2 m spatial resolution across 730 time steps
- Soft mobility network segmented into 50 m segments with 7 m buffer
- 9 route segment clusters identified for urban intervention planning

---

### Requirements

- Python ≥ 3.8
- QGIS 3.28.1 with UMEP plugin
- pythermalcomfort, rasterio, netCDF4, geopandas, openrouteservice
- SLURM-based HPC cluster (for city-scale SOLWEIG runs)

See `README.md` for full installation instructions, data sources, and usage guide.

---

### Related Publication

If you use this code, please cite:

Huang, Y.-S., Llaguno-Munitxa, M., Manoli, G. (2025). Towards Dynamic Urban Environmental Exposure Assessments: A Case Study of the Brussels Capital Region. *Journal of Physics: Conference Series*, 3140(12), 122002. https://doi.org/10.1088/1742-6596/3140/12/122002
