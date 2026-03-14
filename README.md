# BREEZE
## Bioclimatic Route Evaluation for Environmental haZard avoidancE

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![QGIS 3.28](https://img.shields.io/badge/QGIS-3.28-green.svg)](https://qgis.org/)


---

## Overview

BREEZE is a comprehensive framework that evaluates environmental hazard exposure (heat stress, cold stress, air pollution, and greenery) along urban soft mobility networks (pedestrian paths, cycling lanes). It serves two complementary purposes:

1. **City-scale urban planning** — identifying high-exposure hotspots and priority intervention zones using dynamic population weighting.
2. **Citizen-oriented navigation** — personalised route optimisation that minimises individual environmental exposure based on user-declared health sensitivities.

The framework is demonstrated on the **Brussels-Capital Region (BCR)** as a case study and is designed to be transferable to other urban contexts.

**Associated paper:**
> *BREEZE: Bioclimatic Route Evaluation for Environmental haZard avoidancE* (under review)

---

## Repository Structure

```
BREEZE/
│
├── 2.2.1_AppA_DSM_object_removing.ipynb    # Section 2.2 / Appendix A: Vehicle removal from DSM
├── 2.2.2_AppB_LULC_preprocessing.ipynb     # Section 2.2 / Appendix B: Multi-source LULC generation
├── 2.2.3_Static_dataset_2_nc.ipynb         # Section 2.2: Static datasets (building volume) to NetCDF
├── 2.3.1_Meteorological_dataset_2_nc.ipynb # Section 2.3: UrbClim meteorological data to NetCDF
├── 2.3.2_DSM_split_1km.ipynb               # Section 2.3: DSM resampling & per-grid clipping (QGIS)
├── 2.3.3_UrbClim_100m_2_1km.ipynb          # Section 2.3: UrbClim regridding (100m -> 1km)
├── 2.3.4_UrbClim1km_2_epw.ipynb            # Section 2.3: UrbClim data -> EPW format for SOLWEIG
├── SOLWEIG.py                               # Section 2.3: HPC batch SOLWEIG runner + UTCI computation
├── SOLWEIG.sh                               # SLURM job array script for HPC deployment
├── 2.3.6_UTCI_postprocessing.ipynb         # Section 2.3: UTCI merging, stress accumulation & clipping
├── 2.6_Avoidance_Routing.ipynb             # Section 2.6: Avoidance route mapping web application
│
├── data/                                    # (Not included — see Data section below)
│   ├── DSM/                                # Digital Surface/Terrain Models per 1km grid
│   ├── meteorology/                        # UrbClim NetCDF files & EPW outputs
│   ├── LULC/                               # Land Use/Land Cover datasets
│   └── 3D_city/                            # Building volume and impervious surface datasets
│
└── README.md
```

The notebook numbering follows the section and appendix structure of the paper: the first digit refers to the paper section (2.2, 2.3, 2.6) and the second digit indicates the sequential step within that section.

---

## Workflow

The full pipeline proceeds in the following order:

```
[Raw Data]
    │
    ├─ DSM/DTM (0.5m)
    │   ├─► 2.2.1_AppA_DSM_object_removing.ipynb
    │   │       ↓ Clean vegetation DSM (vehicle removal, circularity filter)
    │   └─► 2.3.2_DSM_split_1km.ipynb  (QGIS)
    │           ↓ Resampled DSMs (2m), per-grid clipped rasters
    │
    ├─ ESA WorldCover + DSMs + Impervious surfaces
    │   └─► 2.2.2_AppB_LULC_preprocessing.ipynb
    │           ↓ 7-class UMEP-compatible LULC (10m)
    │
    ├─ GHS Built-up Volume
    │   └─► 2.2.3_Static_dataset_2_nc.ipynb
    │           ↓ Building volume NetCDF per 1km grid
    │
    ├─ UrbClim NetCDF (100m)
    │   ├─► 2.3.1_Meteorological_dataset_2_nc.ipynb
    │   │       ↓ Cleaned annual meteorological NetCDF files
    │   └─► 2.3.3_UrbClim_100m_2_1km.ipynb
    │           ↓ Regridded meteorology at 1km x 1km
    │       2.3.4_UrbClim1km_2_epw.ipynb
    │           ↓ EPW-format meteorological input per grid cell
    │
    └─ All above ────────► SOLWEIG.py + SOLWEIG.sh  (HPC)
                               ↓ Tmrt rasters -> UTCI rasters (2m, 730 time steps)
                           2.3.6_UTCI_postprocessing.ipynb
                               ↓ Merged city-wide UTCI, heat/cold degree hours, clipped outputs
                           2.6_Avoidance_Routing.ipynb
                               ↓ Segment-level exposure aggregation + web routing application
```

---

## Notebook Descriptions

### `2.2.1_AppA_DSM_object_removing.ipynb` — DSM Vehicle Removal
Implements **Appendix A** of the paper. Removes misclassified parked vehicles from the vegetation layer of the Digital Surface Model using a circularity-based filtering approach. Steps include clipping building footprints from the DSM-DTM difference raster, extracting vegetation profiles by height thresholds (0.4-2 m for vehicle-height objects), computing the circularity ratio for each object across spatial tiles (to manage memory), and masking out those with circularity between 0.22 and 0.66 on impermeable surfaces.

**Key inputs:** `DSM-DTM_50cm.tif`, `UrbISBuildings_04000.gpkg`, `Impermeables_clipped.tif`
**Key outputs:** `DSM-DTM_50cm_vegetation_without_cars.tif`, `Circularity_brussels.tif`

---

### `2.2.2_AppB_LULC_preprocessing.ipynb` — LULC Dataset Generation
Implements **Appendix B** of the paper. Generates a 7-category LULC map compatible with the UMEP toolbox (Paved, Buildings, Evergreen trees, Deciduous trees, Grass, Bare soil, Water) by fusing multiple data sources. Two base LULC products are supported: ESA WorldCover 10 m and CORINE Land Cover (CLC) 2012. A pixel-based weighted voting algorithm integrates building DSM, vegetation DSM, and impervious surface data to resolve conflicts and produce the final classification, saved as NetCDF on the 1 km x 1 km ETRS89-LAEA grid.

**Key inputs:** `WorldCover_LULC_Brussels.tif` or CLC 2012, building/vegetation DSMs, impervious surface raster
**Key outputs:** `WorldCover_Brussels_11bands.nc`, `CLC_2012_Brussels_14bands.nc`, `LULC_UMEP_*.tif` per grid

---

### `2.2.3_Static_dataset_2_nc.ipynb` — Static Datasets to NetCDF
Implements **Section 2.2** static data preparation. Reads the GHS Built-up Volume (GHS-BUILT-V) multitemporal raster dataset and reprojects and aggregates values onto the 1 km x 1 km ETRS89-LAEA grid. Produces a NetCDF file with building volume estimates for multiple epochs (2005, 2010, 2015, 2020).

**Key inputs:** `GHS_BUILT_V_E*_GLOBE_R2023A_4326_3ss_V1_0.tif` (multitemporal)
**Key outputs:** `Building_volume_brussels.nc`

---

### `2.3.1_Meteorological_dataset_2_nc.ipynb` — Meteorological Data to NetCDF
Implements **Section 2.3** meteorological pre-processing. Reads raw UrbClim monthly NetCDF files (air temperature, relative humidity, wind speed) at 100 m resolution, extracts values for the BCR domain, and saves annual time series as consolidated NetCDF files. Also inspects UrbClim auxiliary masks (rural/urban mask, land/sea mask) for quality control.

**Key inputs:** `tas_Brussels_UrbClim_YYYY_MM_v1.0.nc`, `russ_*`, `sfcWind_*`
**Key outputs:** `Air_temp_brussels_YYYY.nc`, `RH_brussels_YYYY.nc`, `Wind_brussels_YYYY.nc`

---

### `2.3.2_DSM_split_1km.ipynb` — DSM Resampling and Per-grid Clipping
Implements **Section 2.3** DSM preparation for SOLWEIG. Runs in the **QGIS Python console**. Resamples the cleaned DSM layers (ground, ground+building, vegetation) from 0.5 m to the target SOLWEIG resolution (e.g. 2 m) using GDAL with average resampling. Prepares 1 km x 1 km city mask vector files from the ETRS89 EEA reference grid, then clips the resampled DSM layers to each grid cell to produce the per-grid inputs required by SOLWEIG.

**Key inputs:** `DSM_50cm_ground.tif`, `DSM_50cm_ground_building.tif`, `DSM-DTM_50cm_vegetation_without_cars.tif`, EEA ETRS89 grid shapefile
**Key outputs:** `Ground_<CELLCODE>.tif`, `Ground_Building_<CELLCODE>.tif`, `Vegetation_<CELLCODE>.tif` per 1 km grid; `CELLCODE_<CELLCODE>.gpkg` mask vectors

---

### `2.3.3_UrbClim_100m_2_1km.ipynb` — UrbClim Regridding (100 m -> 1 km)
Implements **Section 2.3** meteorological regridding. Reads the consolidated annual UrbClim NetCDF files and regrids them from the native 100 m x 100 m UrbClim grid to the 1 km x 1 km ETRS89-LAEA grid. Handles coordinate reprojection between EPSG:4326 and EPSG:3035. Also visualises yearly average fields and verifies rural/urban mask alignment.

**Key inputs:** `Air_temp_brussels_YYYY.nc`, `RH_brussels_YYYY.nc`, `Wind_brussels_YYYY.nc`
**Key outputs:** Regridded per-variable NetCDF files at 1 km resolution

---

### `2.3.4_UrbClim1km_2_epw.ipynb` — Meteorological Data -> EPW Format
Implements **Section 2.3** SOLWEIG input preparation. Converts regridded UrbClim meteorological data and CAMS-RAD solar radiation into the EPW (EnergyPlus Weather) text format required by SOLWEIG. Includes validation against ERA5 for temperature, relative humidity, wind speed, and dew point. Produces multiple temporal variants of the input file:
- Full hourly EPW (all time steps)
- Coldest/hottest day subset
- 8-hour day/night averaged windows (daytime 8-16h, nighttime 16-24h) — used for the main analysis
- Monthly 8-hour averaged files

**Key inputs:** Regridded UrbClim NetCDF, CAMS-RAD solar radiation, ERA5 EPW for validation
**Key outputs:** `meteo_<CELLCODE>_DoY80_264_hourly.txt` and variant files per 1 km grid cell

---

### `SOLWEIG.py` + `SOLWEIG.sh` — HPC SOLWEIG Runner & UTCI Computation
Implements **Section 2.3** UTCI computation at city scale. Designed for HPC deployment via SLURM job arrays.

`SOLWEIG.py`:
- Initialises QGIS/UMEP headlessly on the compute node
- Runs the SOLWEIG model to produce Tmrt rasters at 2 m resolution for 730 time steps (365 days x 2 periods)
- Clips outputs to each 1 km grid boundary using GDAL
- Converts Tmrt rasters to UTCI using `pythermalcomfort`, reading matched meteorological conditions from the EPW file
- Handles minimum wind speed thresholds (0.5 m/s) and cleans auxiliary files

`SOLWEIG.sh`:
- SLURM batch script submitting a job array (0-177, one per 1 km grid cell)
- Limits to 20 simultaneous tasks; requests 7 GB RAM per task
- Loads required modules: QGIS 3.28.1, pythermalcomfort, rasterio

**Key outputs:** `UTCI_<timestep>_clipped.tif` rasters per grid cell (2 m resolution)

---

### `2.3.6_UTCI_postprocessing.ipynb` — UTCI Post-processing
Implements **Section 2.3** post-processing steps. Converts raw per-grid UTCI outputs from SOLWEIG into city-wide stress products. Three steps:

1. **Merge UTCI rasters** — mosaics all 178 per-grid `UTCI_*_clipped.tif` files into city-wide rasters using GDAL, for each of the 730 time steps.
2. **Compute heat and cold degree hours** — accumulates monthly and annual heat stress (UTCI > 26 °C) and cold stress (UTCI < 9 °C) as degree-hour totals per pixel.
3. **Clip to study boundary** — clips city-wide stress rasters to the BCR administrative boundary using QGIS processing tools.

Note: steps 2-3 require a QGIS console environment.

**Key inputs:** `UTCI_*_clipped.tif` per grid cell, BCR boundary polygon
**Key outputs:** City-wide annual/monthly heat and cold stress rasters (`heat_stress_YYYY.tif`, `cold_stress_YYYY.tif`)

---

### `2.6_Avoidance_Routing.ipynb` — Avoidance Route Mapping Application
Prior to this notebook, a series of QGIS operations are required but not included in this repository. These include creating buffer zones along soft mobility routes, splitting routes into segments of suitable length, and extracting raster values per segment using the Zonal Statistics function in QGIS. Implements **Section 2.6** of the paper. Builds the interactive web-based avoidance routing application with dual UTCI threshold analysis (26 °C and 32 °C). Pipeline steps:
1. **Segment-level exposure aggregation** — reads UTCI and AQI rasters, computes mean exposure per 50 m soft mobility segment within a 7 m buffer; supports dual UTCI thresholds and timeline data collection
2. **IDW heatmap generation** — produces smooth 10 m x 10 m exposure surfaces (heat, air pollution, greenery) via Inverse Distance Weighting with enforced common bounds
3. **Avoidance routing** — integrates with the OpenRouteService API; avoids segments exceeding UTCI 26 °C or 32 °C or AQI 50, based on user-defined avoidance rates and SVF threshold
4. **HTML web application** — generates a self-contained interactive map (Mapbox GL) with triple heatmap overlays (heat, air pollution, greenery), direct vs optimised route comparison with area-under-curve exposure calculation, and configurable user scenarios (heat-sensitive, respiratory-sensitive)

**Key inputs:** UTCI stress rasters, AQI data, bike route network (GeoJSON), NDVI, SVF layers
**Key outputs:** Self-contained HTML interactive map

---

## Installation

### Prerequisites

| Component | Version | Purpose |
|-----------|---------|---------|
| Python | >= 3.8 | Core scripting |
| QGIS | 3.28.1 (LTR) | UMEP plugin host; required for `2.3.2_DSM_split_1km.ipynb` and clipping steps |
| UMEP | Latest | SOLWEIG, SVF, Wall geometry |
| SLURM | — | HPC job scheduling (for `SOLWEIG.sh`) |

### Python Dependencies

```bash
pip install numpy pandas rasterio netCDF4 pythermalcomfort \
            scikit-learn scipy matplotlib cartopy pyproj \
            python-aqi statsmodels metpy geopandas opencv-python
```

For the routing notebook additionally:
```bash
pip install requests shapely openrouteservice
```

### QGIS / UMEP Setup

UMEP must be installed as a QGIS plugin. Follow the [official UMEP installation guide](https://umep-docs.readthedocs.io/en/latest/Getting_Started.html).

`2.3.2_DSM_split_1km.ipynb` and the clipping cells in `2.3.6_UTCI_postprocessing.ipynb` must be run inside the **QGIS Python console** or a QGIS-enabled Python environment.

For **headless HPC use**, load the appropriate modules (see `SOLWEIG.sh`) and ensure the UMEP plugin path is on `PYTHONPATH`:

```bash
export PYTHONPATH=$PYTHONPATH:/path/to/QGIS/share/qgis/python/plugins/
export PYTHONPATH=$PYTHONPATH:$HOME/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
export QT_QPA_PLATFORM=offscreen
```

---

## Data

The input data used in the BCR case study are **not included** in this repository due to size and licensing constraints. The table below lists all required datasets with links to their sources.

| Dataset | Resolution | Source |
|---------|-----------|--------|
| Digital Surface Model (DSM) | 0.5 m | [Brussels UrbIS](https://datastore.brussels/web/data/dataset/8c2d921e-6a53-11ed-bfb5-010101010000) |
| Digital Terrain Model (DTM) | 0.5 m | [Brussels BRIC](https://datastore.brussels/web/data/dataset/1d7bd49d-fe83-4388-af85-6f5dc8ec7909) |
| Building parcels | Vector | [Brussels UrbIS Parcels](https://datastore.brussels/web/data/dataset/2cf42541-1813-11ef-8a81-00090ffe0001) |
| Impervious surfaces | 1 m | [data.gov.be](https://data.gov.be/en/datasets/f8ea1c8f-44a2-4b48-9b24-083acf9c35e3) |
| ESA WorldCover LULC | 10 m | [ESA WorldCover 2021](https://doi.org/10.5281/zenodo.7254221) |
| CORINE Land Cover (CLC) 2012 | 100 m | [Copernicus Land Service](https://land.copernicus.eu/pan-european/corine-land-cover) |
| GHS Built-up Volume | 100 m | [GHS-BUILT-V R2023A](https://doi.org/10.1080/17538947.2024.2390454) |
| EEA reference grid (ETRS89) | 1 km | [EEA reference grids](https://www.eea.europa.eu/data-and-maps/data/eea-reference-grids-2) |
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
│   ├── DSM_50cm_ground.tif
│   ├── DSM_50cm_ground_building.tif
│   ├── DSM-DTM_50cm_vegetation_without_cars.tif
│   └── <CELLCODE>/
│       ├── Ground_<CELLCODE>.tif
│       ├── Ground_Building_<CELLCODE>.tif
│       ├── Vegetation_<CELLCODE>.tif
│       ├── Wall_height_<CELLCODE>.tif
│       ├── Wall_aspect_<CELLCODE>.tif
│       ├── svfs.zip
│       └── CELLCODE_<CELLCODE>.gpkg
├── meteorology/
│   └── Brussels/
│       ├── Air_temp_brussels/
│       ├── Relative_humidity_brussels/
│       └── Wind_speed_brussels/
├── LULC/
│   ├── WorldCover_LULC_Brussels.tif
│   └── WorldCover_Brussels_clipped.tif
├── 3D_city/
│   ├── GHS_BUILT_V_E*_GLOBE_R2023A_4326_3ss_V1_0.tif
│   └── Impermeables_extend.tif
└── routes/
    └── bike_routes_BCR.geojson
```
---

## Citation

If you use BREEZE in your research, please cite the associated paper (citation to be updated upon publication):

```bibtex
@article{breeze2025,
  title   = {{BREEZE}: Bioclimatic Route Evaluation for Environmental {haZard} avoidancE},
  author  = {Huang, Yen-Shuo and Manoli, Gabriele and Bou-Zeid, Elie and Llaguno-Munitxa, Maider},
  journal = {under review},
  year    = {2025}
}
```

Related work from the same research group:
```bibtex
@article{huang2025dynamic,
  title   = {Towards Dynamic Urban Environmental Exposure Assessments: A Case Study of the Brussels Capital Region},
  author  = {Huang, Yen-Shuo and Manoli, Gabriele and Llaguno-Munitxa, Maider},
  journal = {Journal of Physics: Conference Series},
  volume  = {3140},
  number  = {12},
  pages   = {122002},
  year    = {2025},
  doi     = {10.1088/1742-6596/3140/12/122002}
}
```

---

## Contributing

Contributions and adaptations for other cities are welcome. Please open an issue to discuss proposed changes, or submit a pull request.

When adapting to a new city:
- Obtain an ETRS89 EEA reference grid shapefile for your country from the EEA website to define the 1 km grid cells
- Ensure your DSM/DTM spatial resolution is between 0.5-10 m for adequate SOLWEIG accuracy
- A 7-category LULC compatible with UMEP is required (see `2.2.2_AppB_LULC_preprocessing.ipynb`)
- Meteorological input can be substituted with ERA5 reanalysis or local station data processed through UWG if UrbClim is unavailable for your region

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Acknowledgements

This work uses:
- [UMEP](https://umep-docs.readthedocs.io/) — Urban Multi-scale Environmental Predictor
- [SOLWEIG](https://doi.org/10.1007/s00484-008-0162-7) — Solar and LongWave Environmental Irradiance Geometry model
- [pythermalcomfort](https://doi.org/10.1016/j.softx.2020.100578) — Python thermal comfort library
- [OpenRouteService](https://openrouteservice.org/) — Open-source routing engine
- [Copernicus Climate Change Service](https://cds.climate.copernicus.eu/) — UrbClim and ERA5 data
- [ESA WorldCover](https://doi.org/10.5281/zenodo.7254221) — Global land cover

Simulations were performed on the **Manneback HPC cluster** (Belgium).
