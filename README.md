# BREEZE 🌬️
## Bioclimatic Route Evaluation for Environmental haZard avoidancE

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![QGIS 3.28](https://img.shields.io/badge/QGIS-3.28-green.svg)](https://qgis.org/)

> A multi-dimensional environmental exposure assessment framework for urban soft mobility routes, integrating thermal comfort modeling, air quality assessment, dynamic population weighting, and personalized avoidance routing.

---

## 📖 Overview

BREEZE is a comprehensive framework that evaluates environmental hazard exposure (heat stress, cold stress, air pollution, and greenery) along urban soft mobility networks (pedestrian paths, cycling lanes). It serves two complementary purposes:

1. **City-scale urban planning** — identifying high-exposure hotspots and priority intervention zones using dynamic population weighting.
2. **Citizen-oriented navigation** — personalised route optimisation that minimises individual environmental exposure based on user-declared health sensitivities.

The framework is demonstrated on the **Brussels-Capital Region (BCR)** as a case study and is designed to be transferable to other urban contexts.

**Associated paper:**  
> *BREEZE: Bioclimatic Route Evaluation for Environmental haZard avoidancE* (under review)

---

## 🗂️ Repository Structure

```
BREEZE/
│
├── 2_2_AppA_DSM_preprocessing.ipynb     # Appendix A: DSM/DTM pre-processing & SVF computation
├── 2_2_AppB_LULC_preprocessing.ipynb    # Appendix B: Multi-source LULC dataset generation
├── 2_3_UrbClim_100m_2_1km.ipynb         # Section 2.3: UrbClim downscaling (100m → 1km grids)
├── 2_3_UrbClim1km_2_epw.ipynb           # Section 2.3: UrbClim data → EPW format for SOLWEIG
├── SOLWEIG.py                            # Section 2.3: HPC batch SOLWEIG runner + UTCI computation
├── SOLWEIG.sh                            # SLURM job array script for HPC deployment
├── 2_6_Avoidance_Routing.ipynb          # Section 2.6: Avoidance route mapping web application
│
├── data/                                 # (Not included — see Data section below)
│   ├── DSM/                             # Digital Surface/Terrain Models per 1km grid
│   ├── meteorology/                     # UrbClim NetCDF files & EPW outputs
│   └── LULC/                            # Land Use/Land Cover datasets
│
└── README.md
```

The notebook numbering corresponds to the sections and appendices in the paper.

---

## 🔄 Workflow

The full pipeline proceeds in the following order:

```
[Raw Data]
    │
    ├─ DSM/DTM (0.5m) ──► 2_2_AppA_DSM_preprocessing.ipynb
    │                          ↓ Building DSM, Vegetation DSM, Wall Height/Aspect, SVF
    │
    ├─ ESA WorldCover ──► 2_2_AppB_LULC_preprocessing.ipynb
    │   + Building DSM          ↓ 7-class LULC (UMEP-compatible, 10m)
    │   + Impervious surfaces
    │
    ├─ UrbClim NetCDF ──► 2_3_UrbClim_100m_2_1km.ipynb
    │                          ↓ Regridded meteorology at 1km × 1km
    │                      2_3_UrbClim1km_2_epw.ipynb
    │                          ↓ EPW-format meteorological input per grid cell
    │
    └─ All above ────────► SOLWEIG.py + SOLWEIG.sh  (HPC)
                               ↓ Tmrt rasters → UTCI rasters (2m resolution, 730 time steps)
                           2_6_Avoidance_Routing.ipynb
                               ↓ Segment-level exposure aggregation + web routing application
```

---

## 📓 Notebook Descriptions

### `2_2_AppA_DSM_preprocessing.ipynb` — DSM/DTM Pre-processing
Implements **Appendix A** of the paper. Pre-processes raw LiDAR-derived Digital Surface Model (DSM) and Digital Terrain Model (DTM) data to extract:
- **Building DSM** (DSM minus DTM, buildings only)
- **Vegetation DSM** (vegetation heights)
- **Ground DSM** (terrain)

Applies the multi-level morphological active contour (MMAC) algorithm to remove misclassified parked vehicles from the vegetation layer. Prepares inputs for UMEP's Urban Geometry tools (Wall Height/Aspect, Sky View Factor).

**Key inputs:** Raw DSM (0.5 m), DTM (0.5 m), Building parcels vector  
**Key outputs:** `Ground_Building_*.tif`, `Vegetation_*.tif`, `Ground_*.tif`, `Wall_height_*.tif`, `Wall_aspect_*.tif`, `SVF_*.tif`

---

### `2_2_AppB_LULC_preprocessing.ipynb` — LULC Dataset Generation
Implements **Appendix B** of the paper. Generates a 7-category LULC map compatible with the UMEP toolbox (Paved, Buildings, Evergreen trees, Deciduous trees, Grass, Bare soil, Water) by fusing:
- ESA WorldCover 10 m (base layer)
- Building DSM (0.5 m → 2 m)
- Vegetation DSM (0.5 m → 2 m)
- Impervious surfaces (1 m → 2 m)

Uses a **pixel-based weighted voting algorithm** with rejection mechanism to resolve conflicts across data sources and produce the final 10 m LULC map.

**Key inputs:** `WorldCover_LULC_Brussels.tif`, building/vegetation DSMs, impervious surface raster, UrbClim grid extents  
**Key outputs:** `LULC_UMEP_*.tif` per 1 km grid

---

### `2_3_UrbClim_100m_2_1km.ipynb` — UrbClim Regridding (100 m → 1 km)
Implements **Section 2.3** pre-processing step. Reads UrbClim NetCDF files (air temperature, relative humidity, wind speed at 100 m resolution) and regrids them to the 1 km × 1 km ETRS89-LAEA grid used for SOLWEIG simulations. Handles coordinate reprojection between EPSG:4326 and EPSG:3035. Produces per-grid annual NetCDF files.

**Key inputs:** UrbClim NetCDF files (`tas_Brussels_UrbClim_YYYY_MM_v1.0.nc`, etc.)  
**Key outputs:** Regridded NetCDF files (`Air_temp_brussels_YYYY.nc`, etc.) per grid cell

---

### `2_3_UrbClim1km_2_epw.ipynb` — Meteorological Data → EPW Format
Implements **Section 2.3** pre-processing step. Converts regridded UrbClim meteorological data and CAMS-RAD solar radiation data into the EPW (EnergyPlus Weather) text format required by SOLWEIG. Handles:
- 8-hour temporal averaging (daytime 8–16h, nighttime 16–24h)
- Solar radiation variable extraction (GHI, DNI, DHI)
- Validation against ground station observations (Brussels Airport, Uccle)

**Key inputs:** Regridded UrbClim NetCDF, CAMS-RAD solar radiation point data  
**Key outputs:** `meteo_<CELLCODE>_DoY80_264_hourly.txt` per 1 km grid cell

---

### `SOLWEIG.py` + `SOLWEIG.sh` — HPC SOLWEIG Runner & UTCI Computation
Implements **Section 2.3** UTCI computation at city scale. Designed for HPC deployment via SLURM job arrays.

`SOLWEIG.py`:
- Initialises QGIS/UMEP headlessly on the compute node
- Runs the **SOLWEIG** model (Solar Long Wave Environmental Irradiance Geometry) to produce Tmrt rasters at 2 m resolution for 730 time steps (365 days × 2 periods)
- Clips outputs to each 1 km grid boundary using GDAL
- Converts Tmrt rasters to **UTCI** using `pythermalcomfort`, reading matched meteorological conditions from the EPW file
- Handles minimum wind speed thresholds and cleans auxiliary files

`SOLWEIG.sh`:
- SLURM batch script submitting a job array (0–177, one per 1 km grid cell)
- Limits to 20 simultaneous tasks; requests 7 GB RAM per task
- Loads required modules: QGIS 3.28.1, pythermalcomfort, rasterio

**Key outputs:** `UTCI_<timestep>_clipped.tif` rasters per grid cell (2 m resolution)

---

### `2_6_Avoidance_Routing.ipynb` — Avoidance Route Mapping Application
Implements **Section 2.6** of the paper. Builds the interactive web-based avoidance routing application. Pipeline steps:
1. **Segment-level exposure aggregation** — reads UTCI and AQI rasters, computes mean exposure per 50 m soft mobility segment within a 7 m buffer
2. **IDW heatmap generation** — produces smooth 10 m × 10 m exposure surfaces (heat, air pollution, greenery) via Inverse Distance Weighting
3. **Avoidance routing** — integrates with the OpenRouteService API to optimise routes by avoiding segments exceeding UTCI 26 °C or AQI 50, based on user-defined avoidance rates
4. **HTML web application** — generates a self-contained interactive map (Mapbox GL) with:
   - Colour-coded exposure heatmap overlays
   - Direct vs optimised route comparison
   - Cumulative exposure history visualisation
   - Configurable user scenarios (heat-sensitive, respiratory-sensitive)

**Key inputs:** UTCI rasters, AQI data, bike route network (GeoJSON), NDVI, SVF layers  
**Key outputs:** Self-contained HTML interactive map

---

## ⚙️ Installation

### Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | ≥ 3.8 | Core scripting |
| QGIS | 3.28.1 (LTR) | UMEP plugin host |
| UMEP | Latest | SOLWEIG, SVF, Wall geometry |
| SLURM | — | HPC job scheduling (for `SOLWEIG.sh`) |

### Python Dependencies

```bash
pip install numpy pandas rasterio netCDF4 pythermalcomfort \
            scikit-learn scipy matplotlib cartopy pyproj \
            python-aqi statsmodels metpy
```

For the routing notebook additionally:
```bash
pip install requests geopandas shapely openrouteservice
```

### QGIS / UMEP Setup

UMEP must be installed as a QGIS plugin. Follow the [official UMEP installation guide](https://umep-docs.readthedocs.io/en/latest/Getting_Started.html).

For **headless HPC use**, load the appropriate modules (see `SOLWEIG.sh`) and ensure the UMEP plugin path is on `PYTHONPATH`:

```bash
export PYTHONPATH=$PYTHONPATH:/path/to/QGIS/share/qgis/python/plugins/
export PYTHONPATH=$PYTHONPATH:$HOME/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
export QT_QPA_PLATFORM=offscreen
```

---

## 📦 Data

The input data used in the BCR case study are **not included** in this repository due to size and licensing constraints. The table below lists all required datasets with links to their sources.

| Dataset | Resolution | Source |
|---------|-----------|--------|
| Digital Surface Model (DSM) | 0.5 m | [Brussels UrbIS](https://datastore.brussels/web/data/dataset/8c2d921e-6a53-11ed-bfb5-010101010000) |
| Digital Terrain Model (DTM) | 0.5 m | [Brussels BRIC](https://datastore.brussels/web/data/dataset/1d7bd49d-fe83-4388-af85-6f5dc8ec7909) |
| Building parcels | Vector | [Brussels UrbIS Parcels](https://datastore.brussels/web/data/dataset/2cf42541-1813-11ef-8a81-00090ffe0001) |
| Impervious surfaces | 1 m | [data.gov.be](https://data.gov.be/en/datasets/f8ea1c8f-44a2-4b48-9b24-083acf9c35e3) |
| ESA WorldCover LULC | 10 m | [ESA WorldCover 2021](https://doi.org/10.5281/zenodo.7254221) |
| GHS Built-up Volume | 100 m | [GHS-BUILT-V R2023A](https://doi.org/10.1080/17538947.2024.2390454) |
| UrbClim meteorology | 100 m, hourly | [Copernicus CDS](https://doi.org/10.24381/cds.c6459d3a) |
| CAMS-RAD solar radiation | Point | [CAMS radiation service](https://doi.org/10.1016/j.rse.2024.114472) |
| MODIS NDVI (MOD13Q1) | 250 m, 16-day | [NASA LP DAAC](https://doi.org/10.5067/MODIS/MOD13Q1.061) |
| Air pollution (EXPANSE) | 100 m, monthly | [Shen et al. 2022](https://doi.org/10.1016/j.envint.2022.107485) |
| Daytime/nighttime population | 1 km | [Batista e Silva et al. 2020](https://doi.org/10.1038/s41467-020-18344-5) |
| Bike routes | Vector | [MOBGIS Brussels](https://data.mobility.brussels/mobigis/fr/) |
| Social deprivation (BIMD) | Statistical units | [Otavova et al. 2023](https://doi.org/10.1016/j.sste.2023.100587) |

Expected data directory structure:
```
data/
├── DSM/
│   └── <CELLCODE>/
│       ├── Ground_Building_<CELLCODE>.tif
│       ├── Vegetation_<CELLCODE>.tif
│       ├── Ground_<CELLCODE>.tif
│       ├── Wall_height_<CELLCODE>.tif
│       ├── Wall_aspect_<CELLCODE>.tif
│       └── svfs.zip
├── meteorology/
│   └── Brussels/
│       ├── Air_temp_brussels/
│       ├── Relative_humidity_brussels/
│       └── Wind_speed_brussels/
├── LULC/
│   └── WorldCover_LULC_Brussels.tif
└── routes/
    └── bike_routes_BCR.geojson
```

---

## 🚀 Usage

### Step 1 — Pre-process DSM/DTM
Open and run `2_2_AppA_DSM_preprocessing.ipynb`. Update the path variables at the top of the notebook to point to your raw DSM and DTM files.

### Step 2 — Generate LULC
Open and run `2_2_AppB_LULC_preprocessing.ipynb`. Ensure the voting weights in the configuration section match your local data availability.

### Step 3 — Regrid UrbClim meteorology
Run `2_3_UrbClim_100m_2_1km.ipynb` followed by `2_3_UrbClim1km_2_epw.ipynb` to produce the EPW text files for each 1 km grid cell.

### Step 4 — Run SOLWEIG on HPC
Submit the SLURM job array:
```bash
sbatch SOLWEIG.sh
```
Adjust `--array=0-177` to match the number of grid cells in your study area, and update paths in `SOLWEIG.py` to your HPC scratch directory.

For a **local test** on a single grid cell:
```bash
python3 SOLWEIG.py 0
```

### Step 5 — Build the routing application
Open `2_6_Avoidance_Routing.ipynb`. Configure your OpenRouteService API key and the paths to the aggregated UTCI/AQI segment data, then run all cells to generate the interactive HTML map.

---

## 🧮 Key Methods

### Dynamic Exposure Assessment
Exposure is computed separately for daytime (8–16h) and nighttime (16–24h) windows and weighted by population:

```
Exp_dynamic = Δt × Factor_8-16 × Pop_day  +  Δt × Factor_16-24 × Pop_night
Exp_static  = 2Δt × Factor_8-24 × Pop_static
```

### Thermal Comfort — UTCI
Computed using **SOLWEIG** (for Tmrt at 2 m resolution) + **pythermalcomfort** (for UTCI from Tmrt, air temperature, wind speed, and relative humidity). Heat stress is defined as UTCI > 26 °C; cold stress as UTCI < 9 °C.

### Air Quality — AQI
Individual pollutant AQI values (NO₂, PM₂.₅, PM₁₀, O₃) are computed from concentration data using standard EU/US breakpoints. The overall AQI is `max(AQI_NO2, AQI_PM2.5, AQI_PM10, AQI_O3)`. Air pollution stress is defined as AQI > 50.

### Route Segmentation
Soft mobility networks are divided into **50 m segments** with a **7 m buffer** (14 m total width). Environmental variables are spatially averaged within each buffered segment. Segments with > 35% building coverage or < 10 m² area are excluded.

### Cluster Analysis
K-means clustering (k determined by silhouette score) on annual average segment indicators (excluding highly collinear pairs, |ρ| > 0.8 by Spearman correlation) identifies homogeneous route segment types for targeted urban intervention.

### Avoidance Routing
Segments exceeding exposure thresholds are marked as avoidance segments. The OpenRouteService API is called with user-defined avoidance rates to return optimised routes that minimise time spent in high-stress corridors.

---

## 📊 Results Summary (BCR Case Study)

- **178** 1 km × 1 km grid cells covering the BCR
- **730** time steps (365 days × 2 periods) at **2 m** spatial resolution
- **9 route segment clusters** identified; priority clusters: heat-stressed open streets/plazas (cluster 5), air-polluted inner boulevards (cluster 4), cold/green peripheral segments (cluster 1)
- Dynamic population weighting doubled estimated heat exposure in peak-stress clusters compared to static methods
- Avoidance routing reduced strong heat stress (UTCI > 32 °C) by **up to 20%** with < 1 min extra travel time
- Avoidance routing reduced air pollution stress by **up to 36%** with < 2 min extra travel time

---

## ⚠️ Known Limitations

- Air pollution data (EXPANSE) lacks intraday temporal variation; AQI exposure fluctuations are primarily driven by population dynamics.
- Traffic signal delays at intersections are not accounted for in routing.
- Wind speed is assumed uniform per 1 km grid; micro-scale wind variations are not modelled.
- Population data do not distinguish vulnerable sub-groups (elderly, children); no school/care-home weighting applied.
- Synergistic effects between simultaneous stressors are not modelled.
- Routing assumes outdoor travel only; indoor/semi-indoor passages (e.g., arcades) are excluded.

---

## 📚 Citation

If you use BREEZE in your research, please cite the associated paper (citation to be updated upon publication):

```bibtex
@article{breeze2025,
  title   = {{BREEZE}: Bioclimatic Route Evaluation for Environmental {haZard} avoidancE},
  author  = {Huang, Ye-Sheng and Llaguno-Munitxa, Mikel and Manoli, Gabriele},
  journal = {under review},
  year    = {2025}
}
```

Related work from the same research group:
```bibtex
@article{huang2025dynamic,
  title   = {Towards Dynamic Urban Environmental Exposure Assessments: A Case Study of the Brussels Capital Region},
  author  = {Huang, Y.-S. and Llaguno-Munitxa, M. and Manoli, G.},
  journal = {Journal of Physics: Conference Series},
  volume  = {3140},
  number  = {12},
  pages   = {122002},
  year    = {2025},
  doi     = {10.1088/1742-6596/3140/12/122002}
}
```

---

## 🤝 Contributing

Contributions and adaptations for other cities are welcome. Please open an issue to discuss proposed changes, or submit a pull request.

When adapting to a new city:
- Ensure your DSM/DTM spatial resolution is between 0.5–10 m for adequate SOLWEIG accuracy
- A 7-category LULC compatible with UMEP is required (see `2_2_AppB_LULC_preprocessing.ipynb`)
- Meteorological input can be substituted with ERA5 reanalysis or local station data processed through UWG if UrbClim is unavailable for your region

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

This work uses:
- [UMEP](https://umep-docs.readthedocs.io/) — Urban Multi-scale Environmental Predictor
- [SOLWEIG](https://doi.org/10.1007/s00484-008-0162-7) — Solar and LongWave Environmental Irradiance Geometry model
- [pythermalcomfort](https://doi.org/10.1016/j.softx.2020.100578) — Python thermal comfort library
- [OpenRouteService](https://openrouteservice.org/) — Open-source routing engine
- [Copernicus Climate Change Service](https://cds.climate.copernicus.eu/) — UrbClim and ERA5 data
- [ESA WorldCover](https://doi.org/10.5281/zenodo.7254221) — Global land cover

Simulations were performed on the **Lucia HPC cluster** (UCLouvain).
