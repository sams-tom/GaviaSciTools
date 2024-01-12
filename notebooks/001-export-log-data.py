import os
import matplotlib.pyplot as plt
import pandas as pd
import glob
import cmocean as cmo
import seawater as sw
import sys

sys.path.append('../')
import src.data.export_log_data as efuncs
import src.data.read_functions as rfuncs


# root dir
rootpath = os.path.dirname(os.getcwd())

# log files directory
logdir=os.path.join('e:','ECOWind-accelerate','master','files','log')

savedir=os.path.join('e:','ECOWind-accelerate','master','files','processed-log-data')

os.makedirs(savedir, exist_ok=True)  

files=glob.glob(logdir+'\*ctd*')

if files:
# determine if files are zipped. If yes, unzip, if no, continue
    ctdfiles=os.path.join(logdir,'*ctd-slocum*.xml.gz')    
    import gzip, shutil
    flelist=glob.glob(ctdfiles)
    for i in flelist:
        with gzip.open(i, 'r') as f_in, open( i[:-3], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

files=glob.glob(logdir+'\*sbp*')
if files:
    # determine if files are zipped. If yes, unzip, if no, continue
    files=os.path.join(logdir,'*sbp*.xml.gz')    
    import gzip, shutil
    flelist=glob.glob(files)
    for i in flelist:
        with gzip.open(i, 'r') as f_in, open( i[:-3], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
                
files=glob.glob(logdir+'\*gps*')
if files:    
    # determine if files are zipped. If yes, unzip, if no, continue
    files=os.path.join(logdir,'*gps-*.xml.gz')    
    import gzip, shutil
    flelist=glob.glob(files)
    for i in flelist:
        with gzip.open(i, 'r') as f_in, open( i[:-3], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

files=glob.glob(logdir+'\*nav*')
if files: 
# determine if files are zipped. If yes, unzip, if no, continue
    navfiles=os.path.join(logdir,'*navigator*.xml.gz')    
    import gzip, shutil
    flelist=glob.glob(navfiles)
    for i in flelist:
        with gzip.open(i, 'r') as f_in, open( i[:-3], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

files=glob.glob(logdir+'\*aanderaa*')
# determine if files are zipped. If yes, unzip, if no, continue
if files: 
    files=os.path.join(logdir,'*aanderaa*.xml.gz')    
    import gzip, shutil
    flelist=glob.glob(files)
    for i in flelist:
        with gzip.open(i, 'r') as f_in, open( i[:-3], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
