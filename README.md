# BREEZE
## Bioclimatic Route Evaluation for Environmental haZard avoidancE

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![QGIS 3.28](https://img.shields.io/badge/QGIS-3.28-green.svg)](https://qgis.org/)

Code accompanying the paper *BREEZE: Bioclimatic Route Evaluation for Environmental haZard avoidancE* (Huang, Manoli, Bou-Zeid & Llaguno-Munitxa, *Computers, Environment and Urban Systems*, in press).

---

## Citation

If you use BREEZE in your research, please cite:

```bibtex
@article{Huang2027BREEZE,
  title     = {{BREEZE}: Bioclimatic Route Evaluation for Environmental haZard avoidancE},
  author    = {Huang, Yen-Shuo and Manoli, Gabriele and Bou-Zeid, Elie and Llaguno-Munitxa, Maider},
  journal   = {Computers, Environment and Urban Systems},
  volume    = {132},
  pages     = {102540},
  year      = {2027},
  issn      = {0198-9715},
  doi       = {10.1016/j.compenvurbsys.2026.102540},
  url       = {https://www.sciencedirect.com/science/article/pii/S0198971526001420}
}
```

The dynamic exposure method builds on:

```bibtex
@article{huang2025dynamic,
  title   = {Towards Dynamic Urban Environmental Exposure Assessments: A Case Study of the Brussels Capital Region},
  author  = {Huang, Yen-Shuo and Llaguno-Munitxa, Maider and Manoli, Gabriele},
  journal = {Journal of Physics: Conference Series},
  volume  = {3140},
  number  = {12},
  pages   = {122002},
  year    = {2025},
  doi     = {10.1088/1742-6596/3140/12/122002}
}
```

---

## Paper ↔ code map

File names are prefixed with the paper section they implement. Appendices A–C are in the paper's Supplementary material.

| Paper section | Content | Code |
|---|---|---|
| 2.1 / Suppl. Appendix A | DSM/DTM pre-processing, removal of non-building objects (vehicles) | `2.1.1_AppA_DSM_object_removing.ipynb` |
| 2.1 / Suppl. Appendix B | 7-class UMEP LULC by multi-source voting | `2.1.2_AppB_LULC_preprocessing.ipynb` |
| 2.1 | Building volume (GHS-BUILT-V) on the 1 km grid | `2.1.3_Static_dataset_2_nc.ipynb` |
| 2.2 | UrbClim meteorology → NetCDF | `2.2.1_Meteorological _dataset_2_nc.ipynb` |
| 2.2 | DSM resampling and per-grid clipping | `2.2.2_DSM_split_1km.ipynb` |
| 2.2 / 2.6 | UrbClim regridding 100 m → 1 km | `2.2.3_UrbClim_100m_2_1km.ipynb` |
| 2.2 / Suppl. Appendix C | Meteorological forcing files for SOLWEIG and comparison with reference data | `2.2.4_UrbClim1km_2_epw.ipynb` |
| 2.2 / 2.6 | SOLWEIG T<sub>mrt</sub> → UTCI on HPC | `SOLWEIG.py`, `SOLWEIG.sh` |
| 2.2 | UTCI mosaicking, heat/cold degree hours, clipping | `2.2.6_UTCI_postprocessing.ipynb` |
| 2.3 | AQI computation (python-aqi) | *not in this repository* |
| 2.4 | Segmentation, zonal statistics, Spearman correlation, k-means clustering, dynamic vs static exposure | *not  in this repository* |
| 2.5 | Avoidance route mapping application (OpenRouteService + Mapbox GL JS) | [Available here](https://yenshuohuang.github.io/#breeze) |

---

## Repository structure

```
BREEZE/
├── 2.1.1_AppA_DSM_object_removing.ipynb     # 2.1 / Appendix A — vehicle removal from DSM
├── 2.1.2_AppB_LULC_preprocessing.ipynb      # 2.1 / Appendix B — multi-source LULC for UMEP
├── 2.1.3_Static_dataset_2_nc.ipynb          # 2.1 — building volume to NetCDF
├── 2.2.1_Meteorological _dataset_2_nc.ipynb # 2.2 — UrbClim meteorology to NetCDF
├── 2.2.2_DSM_split_1km.ipynb                # 2.2 — DSM resampling & per-grid clipping (QGIS)
├── 2.2.3_UrbClim_100m_2_1km.ipynb           # 2.2 — UrbClim regridding (100 m → 1 km)
├── 2.2.4_UrbClim1km_2_epw.ipynb             # 2.2 — UrbClim → EPW / SOLWEIG forcing
├── SOLWEIG.py                               # 2.2 — HPC SOLWEIG runner + UTCI computation
├── SOLWEIG.sh                               # 2.2 — SLURM job array (one task per 1 km cell)
├── 2.2.6_UTCI_postprocessing.ipynb          # 2.2 — merging, degree hours, clipping
├── BREEZE_release_description.md
├── LICENSE
└── README.md
```

Input data are not distributed (see [Data](#data)).

---

## Workflow

The pipeline currently in the repository produces the UTCI-based heat and cold stress layers (Sections 2.1–2.2):

```
[Raw data]
    │
    ├─ DSM / DTM (0.5 m)
    │   ├─► 2.1.1_AppA_DSM_object_removing.ipynb
    │   │       ↓ clean vegetation DSM (vehicles removed by circularity filter)
    │   └─► 2.2.2_DSM_split_1km.ipynb  (QGIS)
    │           ↓ resampled DSMs (2 m), clipped per 1 km cell
    │
    ├─ ESA WorldCover + building/vegetation DSMs + impervious surfaces
    │   └─► 2.1.2_AppB_LULC_preprocessing.ipynb
    │           ↓ 7-class UMEP LULC
    │
    ├─ GHS-BUILT-V
    │   └─► 2.1.3_Static_dataset_2_nc.ipynb
    │           ↓ building volume per 1 km cell
    │
    ├─ UrbClim (100 m, hourly) + CAMS-RAD
    │   ├─► 2.2.1_Meteorological _dataset_2_nc.ipynb
    │   ├─► 2.2.3_UrbClim_100m_2_1km.ipynb
    │   └─► 2.2.4_UrbClim1km_2_epw.ipynb
    │           ↓ SOLWEIG forcing per 1 km cell (incl. 8-h day/night windows)
    │
    └─ all of the above ──► SOLWEIG.py + SOLWEIG.sh  (HPC)
                               ↓ Tmrt → UTCI rasters (2 m, 730 time steps)
                           2.2.6_UTCI_postprocessing.ipynb
                               ↓ city-wide UTCI, heat (> 26 °C) and cold (< 9 °C) degree hours
```
---

## Notebook descriptions

### `2.1.1_AppA_DSM_object_removing.ipynb` — DSM object removal (Section 2.1, Suppl. Appendix A)
Removes non-building objects, mainly parked vehicles, that are misread as vegetation in the DSM. Building footprints are clipped from the DSM − DTM raster, objects between 0.4 and 2 m in height are extracted, and the circularity of each object is computed tile by tile to keep memory use manageable. Objects with circularity between 0.22 and 0.66 on impervious surfaces are masked out. Repeat until the vegetation profile is clean.

**Inputs:** `DSM-DTM_50cm.tif`, `UrbISBuildings_04000.gpkg`, `Impermeables_clipped.tif`
**Outputs:** `DSM-DTM_50cm_vegetation_without_cars.tif`, `Circularity_brussels.tif`

### `2.1.2_AppB_LULC_preprocessing.ipynb` — LULC generation (Section 2.1, Suppl. Appendix B)
Produces the seven UMEP land cover classes (Paved, Buildings, Evergreen trees, Deciduous trees, Grass, Bare soil, Water) by combining a global product with local high-resolution layers (building DSM, vegetation DSM, impervious surfaces) through a pixel-based voting algorithm. ESA WorldCover 10 m is the product used in the paper; a CORINE Land Cover 2012 variant is also included.

**Inputs:** `WorldCover_LULC_Brussels.tif` (or CLC 2012), building/vegetation DSMs, impervious surface raster
**Outputs:** `WorldCover_Brussels_11bands.nc`, `CLC_2012_Brussels_14bands.nc`, `LULC_UMEP_*.tif` per grid cell

### `2.1.3_Static_dataset_2_nc.ipynb` — Building volume (Section 2.1)
Reprojects and aggregates the multitemporal GHS-BUILT-V R2023A rasters onto the 1 km ETRS89-LAEA grid (epochs 2005–2020; 2010 is used for the 2011 case study).

**Inputs:** `GHS_BUILT_V_E*_GLOBE_R2023A_4326_3ss_V1_0.tif`
**Outputs:** `Building_volume_brussels.nc`

### `2.2.1_Meteorological _dataset_2_nc.ipynb` — Meteorology to NetCDF (Section 2.2)
Reads monthly UrbClim files (air temperature, relative humidity, wind speed, 100 m, hourly), extracts the BCR domain and writes annual NetCDF time series. Also inspects the UrbClim rural/urban and land/sea masks.

**Inputs:** `tas_Brussels_UrbClim_YYYY_MM_v1.0.nc`, `russ_*`, `sfcWind_*`
**Outputs:** `Air_temp_brussels_YYYY.nc`, `RH_brussels_YYYY.nc`, `Wind_brussels_YYYY.nc`

### `2.2.2_DSM_split_1km.ipynb` — DSM resampling and clipping (Section 2.2)
Run in the **QGIS Python console**. Resamples the ground, ground + building and vegetation DSMs from 0.5 m to the SOLWEIG resolution (2 m in the paper) and clips them to each 1 km cell of the EEA reference grid (`CELLCODE` of the form `1kmExxxxNxxxx`). The paper notes that ~15 m is the coarsest resolution that still captures street-canyon effects; resolution trades accuracy against computing cost.

**Inputs:** `DSM_50cm_ground.tif`, `DSM_50cm_ground_building.tif`, `DSM-DTM_50cm_vegetation_without_cars.tif`, EEA ETRS89 grid
**Outputs:** `Ground_<CELLCODE>.tif`, `Ground_Building_<CELLCODE>.tif`, `Vegetation_<CELLCODE>.tif`, `CELLCODE_<CELLCODE>.gpkg`

### `2.2.3_UrbClim_100m_2_1km.ipynb` — UrbClim regridding (Section 2.2 / 2.6)
Upscales UrbClim from 100 m to the 1 km ETRS89-LAEA grid (EPSG:4326 → EPSG:3035) for computational efficiency, as described in Section 2.6, and plots annual mean fields to check alignment with the masks.

**Inputs:** `Air_temp_brussels_YYYY.nc`, `RH_brussels_YYYY.nc`, `Wind_brussels_YYYY.nc`
**Outputs:** regridded NetCDF files at 1 km

### `2.2.4_UrbClim1km_2_epw.ipynb` — SOLWEIG forcing (Section 2.2, Suppl. Appendix C)
Combines the 1 km UrbClim meteorology with CAMS-RAD radiation (GHI, DNI, DHI) into EPW / SOLWEIG text files per grid cell, and compares the meteorology against reference data. Several temporal variants are produced:
- full hourly series;
- coldest and hottest day (the hottest day is used for the routing demonstration);
- **8-h day (8–16 h) and night (16–24 h) averages** — the 730 time steps used in the main analysis;
- monthly 8-h averages and an alternative day/night window.

**Outputs:** `meteo_<CELLCODE>_*.txt` per grid cell

### `SOLWEIG.py` + `SOLWEIG.sh` — SOLWEIG and UTCI on HPC (Section 2.2 / 2.6)
`SOLWEIG.py` starts QGIS/UMEP headlessly, runs SOLWEIG for one 1 km cell to obtain T<sub>mrt</sub> at 2 m, clips results to the cell with GDAL, and converts T<sub>mrt</sub> to UTCI with `pythermalcomfort` using the matching air temperature, humidity and wind (wind floored at 0.5 m/s).

`SOLWEIG.sh` submits a SLURM job array of 178 tasks (`0-177`, one per cell, max 20 concurrent, 7 GB each) and loads QGIS 3.28.1, pythermalcomfort and rasterio. Cluster-specific settings (partition, excluded nodes, module paths) must be adapted to your HPC.

**Outputs:** `UTCI_<timestep>_clipped.tif` per grid cell

### `2.2.6_UTCI_postprocessing.ipynb` — UTCI post-processing (Section 2.2)
1. Mosaic the 178 per-cell rasters into city-wide UTCI for each of the 730 time steps.
2. Accumulate monthly and annual **heat stress** (degree hours above UTCI 26 °C) and **cold stress** (degree hours below UTCI 9 °C) per pixel.
3. Clip to the BCR boundary (QGIS console required for steps 2–3).

**Outputs:** `heat_stress_YYYY.tif`, `cold_stress_YYYY.tif` (annual and monthly)

---

## Installation

### Prerequisites

| Component | Version | Purpose |
|---|---|---|
| Python | ≥ 3.8 | Scripting |
| QGIS | 3.28.1 LTR | Hosts UMEP; needed for `2.2.2_DSM_split_1km.ipynb` and clipping in `2.2.6_UTCI_postprocessing.ipynb` |
| UMEP | latest | SOLWEIG, SVF, wall height/aspect |
| SLURM | — | HPC scheduling for `SOLWEIG.sh` |

### Python dependencies

```bash
pip install numpy pandas rasterio netCDF4 pythermalcomfort \
            scikit-learn scipy matplotlib cartopy pyproj \
            python-aqi statsmodels metpy geopandas opencv-python
```

For the routing application (Section 2.5): `pip install requests shapely openrouteservice`, plus an OpenRouteService API key and a Mapbox access token.

### QGIS / UMEP

Install UMEP as a QGIS plugin following the [UMEP documentation](https://umep-docs.readthedocs.io/en/latest/Getting_Started.html). Run `2.2.2_DSM_split_1km.ipynb` and the clipping cells of `2.2.6_UTCI_postprocessing.ipynb` in the QGIS Python console or a QGIS-enabled Python environment.

For headless HPC use, load the modules listed in `SOLWEIG.sh` and put the UMEP plugin on `PYTHONPATH`:

```bash
export PYTHONPATH=$PYTHONPATH:/path/to/QGIS/share/qgis/python/plugins/
export PYTHONPATH=$PYTHONPATH:$HOME/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
export QT_QPA_PLATFORM=offscreen
```

---

## Data

Input data for the BCR case study (year 2011) are **not included** because of size and licensing. All sources are listed in Table 1 of the paper.

| Dataset | Resolution | Period used | Source |
|---|---|---|---|
| Day/night population density | 1 km | monthly, 2011 | [Batista e Silva et al. 2020](https://doi.org/10.1038/s41467-020-18344-5) |
| Social deprivation (BIMD) | 724 statistical units | 2011 | [Otavova et al. 2023](https://doi.org/10.1016/j.sste.2023.100587) |
| Bike routes (MOBIGIS) | vector | 2025 | [Brussels Mobility](https://data.mobility.brussels/mobigis/fr/) |
| UrbClim meteorology (T, RH, wind) | 100 m, hourly | 2011 | [Copernicus CDS](https://doi.org/10.24381/cds.c6459d3a) |
| CAMS-RAD solar radiation (GHI, DNI, DHI) | point, hourly | 2011 | [Urraca et al. 2024](https://doi.org/10.1016/j.rse.2024.114472) |
| Air pollution (NO₂, PM₂.₅, PM₁₀, O₃; EXPANSE) | 100 m, monthly | 2011 | [Shen et al. 2022](https://doi.org/10.1016/j.envint.2022.107485) |
| MODIS NDVI (MOD13Q1 V061) | 250 m, 16-day | 2011 | [NASA LP DAAC](https://doi.org/10.5067/MODIS/MOD13Q1.061) |
| DTM | 0.5 m | 2021 | [Brussels Regional Informatics Center](https://datastore.brussels/web/data/dataset/1d7bd49d-fe83-4388-af85-6f5dc8ec7909) |
| DSM (UrbIS) | 0.5 m | 2021 | [Brussels Regional Informatics Center](https://datastore.brussels/web/data/dataset/8c2d921e-6a53-11ed-bfb5-010101010000) |
| Building parcels (UrbIS) | vector | 2024 | [Brussels Regional Informatics Center](https://datastore.brussels/web/data/dataset/2cf42541-1813-11ef-8a81-00090ffe0001) |
| ESA WorldCover v200 | 10 m | 2021 | [Zanaga et al. 2022](https://doi.org/10.5281/zenodo.7254221) |
| Impervious surfaces | 1 m | 2022 | [data.gov.be](https://data.gov.be/en/datasets/f8ea1c8f-44a2-4b48-9b24-083acf9c35e3) |
| GHS-BUILT-V R2023A | 100 m | 2010 | [Pesaresi & Politis 2023](https://doi.org/10.1080/17538947.2024.2390454) |
| EEA reference grid (ETRS89-LAEA) | 1 km | — | [EEA reference grids](https://www.eea.europa.eu/data-and-maps/data/eea-reference-grids-2) |
| CORINE Land Cover 2012 (optional) | 100 m | 2012 | [Copernicus Land Service](https://land.copernicus.eu/pan-european/corine-land-cover) |

Expected directory layout:

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

## License

MIT License — see [LICENSE](LICENSE).

---

## Acknowledgements

This work was supported by the Fonds de la Recherche Scientifique (F.R.S.-FNRS, Belgium), Weave programme, grant T.0137.23, and the Swiss National Science Foundation (SNSF), Weave/Lead Agency scheme, grant 213995.

Simulations were run on the Manneback HPC cluster (UCLouvain, Belgium).

BREEZE relies on:
- [UMEP](https://umep-docs.readthedocs.io/) and [SOLWEIG](https://doi.org/10.1007/s00484-008-0162-7)
- [pythermalcomfort](https://doi.org/10.1016/j.softx.2020.100578)
- [python-aqi](https://pypi.org/project/python-aqi/)
- [OpenRouteService](https://openrouteservice.org/) and [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/)
- [Copernicus Climate Change Service](https://cds.climate.copernicus.eu/) (UrbClim, ERA5) and [ESA WorldCover](https://doi.org/10.5281/zenodo.7254221)

## Contact

- Yen-Shuo Huang — yen-shuo.huang@uclouvain.be
- Maider Llaguno-Munitxa (corresponding author) — maider.llaguno@uclouvain.be

Contributions and adaptations to other cities are welcome: please open an issue or a pull request.