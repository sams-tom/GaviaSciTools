import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import src.data.read_functions as rfuncs

def export_log_data(missionname,logdir,processedpath):

    files=glob.glob(logdir+'\*ctd*')
    if files:
    # read CTD data and convert to .csv format, output to data/ctd-files/
        ctdf=rfuncs.readctdlog(missionname,logdir,processedpath)

    files=glob.glob(logdir+'\*sbp*')
    if files:
        # read SBP data and convert to .csv format, output to data/sbp-files/
        sbpdf=rfuncs.readsbplog(missionname,logdir,processedpath)

    files=glob.glob(logdir+'\*gps*')
    if files:    
        # read GPS data and convert to .csv format, output to data/gps-files/
        gpdf=rfuncs.readgpslog(missionname,logdir,processedpath)

    files=glob.glob(logdir+'\*nav*')
    if files: 
        # read nav data and convert to .csv format, output to data/nav-files/
        nvdf=rfuncs.readnavlog(missionname,logdir,processedpath)

    files=glob.glob(logdir+'\*aanderaa*')
    if files: 
        # read aanderaa data and convert to .csv format, output to data/aanderaa-files/
        aandf=rfuncs.readaandlog(missionname,logdir,processedpath)

    return nvdf, ctdf, aandf, sbpdf, gpdf