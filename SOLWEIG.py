from qgis.core import (
    QgsApplication,
    QgsProcessingFeedback,
    QgsProcessingContext,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransformContext
)
import sys
import subprocess
import os 
import shutil
import numpy as np
import pandas as pd
from pythermalcomfort.models import utci
import rasterio
import random
import time


QgsApplication.setPrefixPath(os.getenv('EBROOTQGIS'), True)
qgs = QgsApplication([], False)
qgs.initQgis()

from qgis.analysis import QgsNativeAlgorithms
from qgis import processing
from processing.core.Processing import Processing 
Processing.initialize()

# Enable processing tools
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
from processing_umep.processing_umep_provider import ProcessingUMEPProvider
umep_provider = ProcessingUMEPProvider()
QgsApplication.processingRegistry().addProvider(umep_provider)
print('Hello QGIS!')
#print a list of provided plugins
#for alg in qgs.processingRegistry().algorithms():
#    print(alg.id(), "->", alg.displayName())
# Define parameters for the algorithm
f_list = ['1kmE3930N3097', '1kmE3929N3101', '1kmE3929N3102', '1kmE3926N3103', '1kmE3921N3102', '1kmE3931N3096', '1kmE3931N3095', '1kmE3931N3094', '1kmE3931N3093', '1kmE3931N3090', '1kmE3930N3096', '1kmE3930N3095', '1kmE3930N3094', '1kmE3930N3093', '1kmE3930N3091', '1kmE3930N3090', '1kmE3929N3100', '1kmE3929N3099', '1kmE3929N3098', '1kmE3929N3097', '1kmE3929N3096', '1kmE3929N3095', '1kmE3929N3094', '1kmE3929N3093', '1kmE3929N3092', '1kmE3929N3091', '1kmE3929N3090', '1kmE3929N3089', '1kmE3928N3103', '1kmE3928N3102', '1kmE3928N3101', '1kmE3928N3100', '1kmE3928N3099', '1kmE3928N3098', '1kmE3928N3097', '1kmE3928N3096', '1kmE3928N3095', '1kmE3928N3094', '1kmE3928N3093', '1kmE3928N3092', '1kmE3928N3091', '1kmE3928N3090', '1kmE3928N3089', '1kmE3927N3103', '1kmE3927N3102', '1kmE3927N3101', '1kmE3927N3100', '1kmE3927N3099', '1kmE3927N3098', '1kmE3927N3097', '1kmE3927N3096', '1kmE3927N3095', '1kmE3927N3094', '1kmE3927N3093', '1kmE3927N3092', '1kmE3927N3091', '1kmE3927N3090', '1kmE3927N3089', '1kmE3926N3102', '1kmE3926N3101', '1kmE3926N3100', '1kmE3926N3099', '1kmE3926N3098', '1kmE3926N3097', '1kmE3926N3096', '1kmE3926N3095', '1kmE3926N3094', '1kmE3926N3093', '1kmE3926N3092', '1kmE3926N3091', '1kmE3926N3090', '1kmE3926N3089', '1kmE3926N3088', '1kmE3925N3102', '1kmE3925N3101', '1kmE3925N3100', '1kmE3925N3099', '1kmE3925N3098', '1kmE3925N3097', '1kmE3925N3096', '1kmE3925N3095', '1kmE3925N3094', '1kmE3925N3093', '1kmE3925N3092', '1kmE3925N3091', '1kmE3925N3090', '1kmE3925N3089', '1kmE3925N3088', '1kmE3924N3102', '1kmE3924N3101', '1kmE3924N3100', '1kmE3924N3099', '1kmE3924N3098', '1kmE3924N3097', '1kmE3924N3096', '1kmE3924N3095', '1kmE3924N3094', '1kmE3924N3093', '1kmE3924N3092', '1kmE3924N3091', '1kmE3924N3090', '1kmE3924N3089', '1kmE3923N3102', '1kmE3923N3101', '1kmE3923N3100', '1kmE3923N3099', '1kmE3923N3098', '1kmE3923N3097', '1kmE3923N3096', '1kmE3923N3095', '1kmE3923N3094', '1kmE3923N3093', '1kmE3923N3092', '1kmE3923N3091', '1kmE3923N3090', '1kmE3923N3089', '1kmE3922N3102', '1kmE3922N3101', '1kmE3922N3100', '1kmE3922N3099', '1kmE3922N3098', '1kmE3922N3097', '1kmE3922N3096', '1kmE3922N3095', '1kmE3922N3094', '1kmE3922N3093', '1kmE3922N3092', '1kmE3922N3091', '1kmE3922N3090', '1kmE3922N3089', '1kmE3921N3101', '1kmE3921N3100', '1kmE3921N3099', '1kmE3921N3098', '1kmE3921N3097', '1kmE3921N3096', '1kmE3921N3095', '1kmE3921N3094', '1kmE3921N3093', '1kmE3921N3092', '1kmE3921N3091', '1kmE3921N3090', '1kmE3921N3089', '1kmE3920N3101', '1kmE3920N3100', '1kmE3920N3099', '1kmE3920N3098', '1kmE3920N3097', '1kmE3920N3096', '1kmE3920N3095', '1kmE3920N3094', '1kmE3920N3093', '1kmE3920N3092', '1kmE3919N3099', '1kmE3919N3098', '1kmE3919N3097', '1kmE3919N3096', '1kmE3919N3095', '1kmE3919N3094', '1kmE3919N3093', '1kmE3918N3096', '1kmE3918N3095', '1kmE3918N3094', '1kmE3918N3093', '1kmE3917N3095', '1kmE3917N3094', '1kmE3916N3094', '1kmE3924N3088', '1kmE3923N3088', '1kmE3920N3090', '1kmE3920N3091', '1kmE3917N3093', '1kmE3916N3095', '1kmE3917N3096', '1kmE3918N3097', '1kmE3918N3099', '1kmE3919N3100','1kmE3919N3092']
#f_list = ['1kmE3930N3097', '1kmE3926N3103', '1kmE3921N3102', '1kmE3931N3094', '1kmE3930N3096', '1kmE3930N3095', '1kmE3916N3094', '1kmE3924N3088', '1kmE3923N3088', '1kmE3920N3090', '1kmE3920N3091', '1kmE3917N3093', '1kmE3916N3095', '1kmE3917N3096', '1kmE3918N3097', '1kmE3918N3099', '1kmE3919N3100', '1kmE3919N3092']
#f_list = ['1kmE3921N3102', '1kmE3929N3100', '1kmE3929N3099', '1kmE3929N3098']

#f_list = ['1kmE3929N3102', '1kmE3931N3094', '1kmE3930N3094', '1kmE3928N3093']

#mon_list = ['Jan_', 'Feb_', 'Mar_', 'Apr_', 'May_', 'Jun_', 'Jul_', 'Aug_', 'Sep_', 'Oct_', 'Nov_', 'Dec_']
#month = 'July'
delete_file = False
count_file = True
run_wall = False
run_SVF = False
run_SOLWEIG = True
run_utci = True
run_threshold = 30 #report if the number of files is lower than threshold
metero_type = ''

# Get the SLURM_ARRAY_TASK_ID from the command-line arguments
task_id = int(sys.argv[1])

# Select the item from the list corresponding to the task ID
current_f_item = f_list[task_id]

# Your processing logic using `current_f_item`
print(f"Processing item: {current_f_item}")
newpath = r'/globalscratch/ucl/loci/yehuang/results_'



if count_file == True:
    print(len(f_list))
    out_list = []
    for fileName in f_list:
        if not os.path.exists(newpath+fileName):
            os.makedirs(newpath+fileName)
        o = [s for s in os.listdir(newpath+fileName) if s.endswith('tif')]
        o = [s for s in o if s.startswith('UTCI')]
        if len(o)<run_threshold:
            out_list.append(fileName)
    print(out_list)

    print(len(out_list))

if delete_file == True:

    #remove files
    for name in [current_f_item]:
        shutil.rmtree(newpath+name)
        print(name+" done")

for data in [current_f_item]:
    if run_wall == True:
        #run wall
        params = {
            'INPUT': os.getenv('HOME')+'/data/DSM/'+data+'/Ground_Building_'+data+'.tif',
            'INPUT_LIMIT': 3,
            'OUTPUT_ASPECT': os.getenv('HOME')+'/data/DSM/'+data+'/Wall_aspect_'+data+'.tif',
            'OUTPUT_HEIGHT': os.getenv('HOME')+'/data/DSM/'+data+'/Wall_height_'+data+'.tif'
        }
    
        processing.run("umep:Urban Geometry: Wall Height and Aspect", params)
    if run_SVF == True:
        #run SVF
        params = {
            'INPUT_DSM': os.getenv('HOME')+'/data/DSM/'+data+'/Ground_Building_'+data+'.tif',
            'INPUT_CDSM': os.getenv('HOME')+'/data/DSM/'+data+'/Vegetation_'+data+'.tif',
            'OUTPUT_DIR': os.getenv('HOME')+'/data/DSM/'+data+'/',
            'OUTPUT_FILE': os.getenv('HOME')+'/data/DSM/'+data+'/SVF_'+data+'.tif'
        }
    
        processing.run("umep:Urban Geometry: Sky View Factor", params)
    if run_SOLWEIG == True:
        a = random.randint(1, 60)
        time.sleep(a)
        if not os.path.exists('/globalscratch/ucl/loci/yehuang/results_'+data):
            os.makedirs('/globalscratch/ucl/loci/yehuang/results_'+data)
        org = [s for s in os.listdir(newpath+data) if s.endswith('.tif')]#list all the tif files under a path
        org = [s for s in org if  s.endswith('clipped.tif')]
        if len(org) > run_threshold:
            break
        else:
            #run SOLWEIG
            print('SOLWEIG ', os.getenv('HOME')+'/data/metero/meteo_'+data+'_DoY80_264_hourly.txt')#os.getenv('HOME')+'/data/metero/meteo_'+data+'_'+month+metero_type+'.txt')

            params = {
                'ABS_L' : 0.95, 
                'ABS_S' : 0.7, 
                'ACTIVITY' : 80, 
                'AGE' : 35, 
                'ALBEDO_GROUND' : 0.15, 
                'ALBEDO_WALLS' : 0.2, 
                'CLO' : 0.9, 
                'CONIFER_TREES' : True, 
                'CYL' : True, 
                'EMIS_GROUND' : 0.95, 
                'EMIS_WALLS' : 0.9, 
                'HEIGHT' : 180, 
                'INPUTMET' : os.getenv('HOME')+'/data/metero/meteo_'+data+'_DoY80_264_hourly.txt', 
                'INPUT_ANISO' : os.getenv('HOME')+'/data/DSM/'+data+'/shadowmats.npz', #'/data/DSM/N166103_E145971/shadowmats.npz'
                'INPUT_ASPECT' : os.getenv('HOME')+'/data/DSM/'+data+'/Wall_aspect_'+data+'.tif', #'/data/DSM/N166103_E145971/Wall_aspect_N166103_E145971.tif',#
                'INPUT_CDSM' : os.getenv('HOME')+'/data/DSM/'+data+'/Vegetation_'+data+'.tif', #'/data/DSM/N166103_E145971/Vegetation_N166103_E145971.tif',#
                'INPUT_DEM' : os.getenv('HOME')+'/data/DSM/'+data+'/Ground_'+data+'.tif', #'/data/DSM/N166103_E145971/Ground_N166103_E145971.tif',#
                'INPUT_DSM' : os.getenv('HOME')+'/data/DSM/'+data+'/Ground_Building_'+data+'.tif', #'/data/DSM/N166103_E145971/Ground_Building_N166103_E145971.tif',
                'INPUT_HEIGHT' : os.getenv('HOME')+'/data/DSM/'+data+'/Wall_height_'+data+'.tif',  #'/data/DSM/N166103_E145971/Wall_height_N166103_E145971.tif',#
                'INPUT_LC' : None, 
                'INPUT_SVF' : os.getenv('HOME')+'/data/DSM/'+data+'/svfs.zip', #'/data/DSM/N166103_E145971/svfs.zip',#
                'INPUT_TDSM' : None, 
                'INPUT_THEIGHT' : 25, 
                'LEAF_END' : 300, 
                'LEAF_START' : 97, 
                'ONLYGLOBAL' : False, 
                'OUTPUT_DIR' : '/globalscratch/ucl/loci/yehuang/results_'+data, 
                'OUTPUT_KDOWN' : False, 
                'OUTPUT_KUP' : False, 
                'OUTPUT_LDOWN' : False, 
                'OUTPUT_LUP' : False, 
                'OUTPUT_SH' : False, 
                'OUTPUT_TMRT' : True, 
                'OUTPUT_TREEPLANTER' : False, 
                'POI_FIELD' : '', 
                'POI_FILE' : None, 
                'POSTURE' : 0, 
                'SAVE_BUILD' : True, 
                'SENSOR_HEIGHT' : 10, 
                'SEX' : 0, 
                'TRANS_VEG' : 3, 
                'USE_LC_BUILD' : False, 
                'UTC' : 0, 
                'WEIGHT' : 75 }
            
            processing.run("umep:Outdoor Thermal Comfort: SOLWEIG", params)
            org = [s for s in os.listdir(newpath+data) if s.endswith('.tif')]#list all the tif files under a path
            org = [s for s in org if not s.endswith('clipped.tif')]
            p = os.getenv('HOME')+'/data/DSM/'+data
            pp = '/' + 'CELLCODE_' + data + '.gpkg'
            for i in org: 
                #print(i) 
                params = {'INPUT': newpath+data+'/'+i,
                'MASK': p+pp,
                'NODATA': -999999999.0,
                'OUTPUT': newpath+data+'/'+i[:-4]+'_clipped.tif'}
                processing.run("gdal:cliprasterbymasklayer", params)
                os.remove(newpath+data+'/'+i)
            o = [s for s in os.listdir(newpath+data) if s.endswith('.aux.xml')]
            for i in o:
                os.remove(newpath+data+'/'+i)
            # All done
            print(data+" done")
'''
print(len(f_list))
newpath = r'/globalscratch/ucl/loci/yehuang/results_'
out_list = []
for fileName in f_list:
    o = [s for s in os.listdir(newpath+fileName) if s.endswith('tif')]
    if len(o)<60:
        out_list.append(fileName)
print(out_list)
    
print(len(out_list))


org = [s for s in os.listdir(newpath+f_list[0]) if s.endswith('.tif')]#list all the tif files under a path
org = [s for s in org if not s.startswith('UTCI')]#list all the tif files under a path
if "buildings_clipped.tif" in org:
    org.remove("buildings_clipped.tif")
if 'Tmrt_average_clipped.tif' in org:
    org.remove('Tmrt_average_clipped.tif')

print(len(org))
'''
def compute_utci_using_tmrt(tmrt_array, ta, va, rh):
    """Compute UTCI based on Tmrt using fixed sample values for demonstration."""
    assert isinstance(tmrt_array, np.ndarray), "tmrt_array must be a NumPy array"
    # Check shapes and values before calling the function
    #print(f"tmrt_array shape: {tmrt_array.shape}, ta: {ta}, va: {va}, rh: {rh}")
    utci_values = utci(tdb=np.full(tmrt_array.shape, ta), tr=tmrt_array, v=va, rh=rh)
    #print(f"utci_values shape: {utci_values.shape}")
    return utci_values

def process_raster(input_raster_path, output_raster_path, ta, va, rh):
    with rasterio.open(input_raster_path) as src:
        tmrt_data = src.read(1)  # Read the first band (assuming single-band raster)
        profile = src.profile
        if tmrt_data.size == 0:
            print(f"Warning: tmrt_data is empty for {input_raster_path}")
        
        utci_data = compute_utci_using_tmrt(tmrt_data, ta, va, rh)#.utci
        utci_data[tmrt_data == -999999999.0] = -999999999.0
        profile.update(dtype=rasterio.float32)

        with rasterio.open(output_raster_path, 'w', **profile) as dst:
            dst.write(utci_data, 1)

def find_meteo(fileName, txt):
    save_path = os.getenv('HOME')+'/data/metero/meteo_'+data+'_DoY80_264_hourly.txt' #os.getenv('HOME')+'/data/metero/meteo_'+fileName+'_July.txt' #os.getenv('HOME')+'/data/metero/meteo_'+fileName+'.txt', 
    print(save_path)
    df = pd.read_csv(save_path, sep=' ', skiprows=1, names=['%iy', 'id', 'it', 'imin', 'Q*', 'QH', 'QE', 'Qs', 'Qf', 'Wind', 'RH', 'Td', 'press', 'rain', 'Kdn', 'snow', 'ldown', 'fcld', 'wuh', 'xsmd', 'lai_hr', 'Kdiff', 'Kdir', 'Wd'])
    
    d, h = int(txt.split('_')[2]), int(txt.split('_')[3][:2])
    i_d = df.index[df['id'] == d].tolist()
    i_t = df.index[df['it'] == h].tolist()
    i = list(set(i_d).intersection(i_t))
    
    if len(i) == 0:
        print(f"No meteo data found for {fileName} at day {d}, hour {h}")
        return None, None, None
    
    temp, wind, RH = df.loc[i, 'Td'].astype('float').values[0], df.loc[i, 'Wind'].astype('float').values[0], df.loc[i, 'RH'].astype('float').values[0]
    return temp, wind, RH


if run_utci == True:
    for fileName in [current_f_item]:
        print(fileName)
        org = [s for s in os.listdir(newpath+fileName) if s.endswith('.tif')]#list all the tif files under a path
        org = [s for s in org if not s.startswith('UTCI')]#list all the tif files under a path
        if "buildings_clipped.tif" in org:
            org.remove("buildings_clipped.tif")
        if 'Tmrt_average_clipped.tif' in org:
            org.remove('Tmrt_average_clipped.tif')
        if "buildings.tif" in org:
            org.remove("buildings.tif")
        if 'Tmrt_average.tif' in org:
            org.remove('Tmrt_average.tif')
        for f in org:
            print('\t',f)
            input_raster = newpath + fileName + '/' + f
            output_raster = newpath + fileName + '/UTCI_' + f[5:]
            temp, wind_speed, humidity = find_meteo(fileName, f)
            
            if temp is None or wind_speed is None or humidity is None:
                continue
            
            if np.mean(wind_speed) < 0.5:
                wind_speed = 0.5

            process_raster(input_raster, output_raster, temp, wind_speed, humidity)
            os.remove(input_raster)
            # Clean auxiliary files
            aux_files = [s for s in os.listdir(newpath + fileName) if s.endswith('.aux.xml')]
            for i in aux_files:
                os.remove(newpath + fileName + '/' + i)
                
print("All done.")