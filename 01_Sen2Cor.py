import os
import glob as g
from tqdm import tqdm

# SBD for wando
# SCG for gwangneung
path1 = '/share/forest/LAI/Data/Sentinel-2/L1C/52SBD/'
path2 = '/share/forest/LAI/Data/Sentinel-2/L1C/52SCG/'

L1_list_52SBD = g.glob(path1 + '*L1C' + '*.SAFE')
L1_list_52SCG = g.glob(path2 + '*L1C' + '*.SAFE')

outpath1 = '/share/forest/LAI/user/jwlee/result/240206/'
outpath2 = '/share/forest/LAI/user/jwlee/result/240206/'
# os.makedirs(outpath1)
# os.makedirs(outpath2)

# cmd = '/home/jslee/Sen2Cor-02.11.00-Linux64/bin/L2A_Process ' + L1_list_52SDE[i] + ' --resolution 20 --output_dir '+ outpath  
# os.system(cmd)

for i in tqdm(range(len(L1_list_52SBD))):
    cmd = '/home/jwlee/Sen2Cor-02.11.00-Linux64/bin/L2A_Process ' + L1_list_52SBD[i] + ' --resolution 10 --output_dir '+ outpath1    
    os.system(cmd)

for i in tqdm(range(len(L1_list_52SCG))):
    cmd = '/home/jwlee/Sen2Cor-02.11.00-Linux64/bin/L2A_Process ' + L1_list_52SCG[i] + ' --resolution 10 --output_dir '+ outpath2    
    os.system(cmd)