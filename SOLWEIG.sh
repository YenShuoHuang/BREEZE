#!/bin/bash
#SBATCH --job-name=S_%A%a.txt
#SBATCH --error=S_err.txt
#SBATCH --output=S_out.txt
#SBATCH --partition=Def
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=7G
#SBATCH --exclude=mb-skg006,mb-skg005
#SBATCH --array=0-177%20  # Limit to 20 simultaneous tasks  # Assuming f_list with 0-177 elements

module load releases/2021b
module  --ignore_cache load QGIS/3.28.1-foss-2021b
module --ignore_cache load matplotlib/3.4.3-foss-2021b
module --ignore_cache load pythermalcomfort/2.8.10-foss-2021b
module --ignore_cache load rasterio/1.3.10-foss-2021b

export QT_QPA_PLATFORM=offscreen
export DISPLAY=0.0 
export QTWEBENGINE_DISABLE_SANDBOX=1

mkdir /tmp/$SLURM_JOB_ID
export XDG_RUNTIME_DIR=/tmp/$SLURM_JOB_ID

export PYTHONPATH=$PYTHONPATH:/opt/sw/arch/easybuild/2021b/software/QGIS/3.28.1-foss-2021b/lib/qgis/
export PYTHONPATH=$PYTHONPATH:/opt/sw/arch/easybuild/2021b/software/QGIS/3.28.1-foss-2021b/share/qgis/python/plugins/
export PYTHONPATH=$PYTHONPATH:$HOME/.local/share/QGIS/QGIS3/profiles/default/python/plugins/

srun python3 SOLWEIG.py $SLURM_ARRAY_TASK_ID