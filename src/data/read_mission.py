import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as et


def readctdlog(missionname,mdir):    # get list of files
    ctdfiles=os.path.join(mdir,'*'+missionname+'*.xml')
    flelist=glob.glob(ctdfiles)
    # for each file, read to pandas dataframe and concatenate
    for count, files in enumerate(flelist):
        if count==0:
            ctdf=pd.read_xml(files)
        else:
            df=pd.read_xml(files,names=None)
            ctdf=pd.concat([ctdf,df],ignore_index=True)
    # save as .csv file
    os.makedirs('data/ctd-files', exist_ok=True)  
    ctdf.to_csv(os.path.join('data/ctd-files',missionname+'CTDdata.csv'))   

    return ctdf