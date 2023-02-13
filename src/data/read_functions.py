import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as et

# sbe19plus data
def concat_ascii_data(ddir):
    fls=glob.glob(ddir)
    # concantenate the dat files
    for i,nme in enumerate(fls):
        data=pd.read_fwf(nme)
        if i==0:
            alldata=data
        else:
            alldata=pd.concat([alldata,data])

    alldata=alldata[['Sal00', 'DepSM','PrdM','Tv290C']]
    
    return alldata



### GAVIA CTD data
def readctdlog(missionname,ldir,processedpath):    # get list of files
    ctdfiles=os.path.join(ldir,'*ctd-slocum*.xml')
    flelist=glob.glob(ctdfiles)
    # determine if files are zipped. If yes, unzip, if no, continue
    if not flelist:
        ctdfiles=os.path.join(ldir,'*ctd-slocum*.xml.gz')    
        import gzip, shutil
        flelist=glob.glob(ctdfiles)
        for i in flelist:
            with gzip.open(i, 'r') as f_in, open( i[:-3], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    # for each file, read to pandas dataframe and concatenate
    for count, files in enumerate(flelist):
        if count==0:
            ctdf=pd.read_xml(files)
        else:
            df=pd.read_xml(files,names=None)
            ctdf=pd.concat([ctdf,df],ignore_index=True)
    # save as .csv file
    ctdf.to_csv(os.path.join(processedpath,missionname+'CTDdata.csv'))   

    return ctdf


# NAV LOG IS MORE COMPLEX XML THAT CANT BE READ BY THE PANDAS READ_XML SO NEED TO EXTRACT VARIABLES THEN MERGE WITH DATASTE CREATED BY READ_XML
def readnavlog(missionname,ldir,processedpath):    # get list of files
    navfiles=os.path.join(ldir,'*navigator*.xml')
    flelist=glob.glob(navfiles)
    # determine if files are zipped. If yes, unzip, if no, continue
    if not flelist:
        navfiles=os.path.join(ldir,'*navigator*.xml.gz')    
        import gzip, shutil
        flelist=glob.glob(navfiles)
        for i in flelist:
            with gzip.open(i, 'r') as f_in, open( i[:-3], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    # for each file, read to pandas dataframe and concatenate
    for count, files in enumerate(flelist):
        if count==0:
            rtdf=pd.read_xml(files)
            tree = et.parse(files)
            root = tree.getroot()

            drheading = []
            drpitch=[]
            droll=[]
            drlat = []
            drlon=[]
            heading=[]
            pitch=[]
            roll=[]
            depth=[]
            lat=[]
            lon=[]

            for node in root.findall("./entry/dead-reckoning-orientation/heading"):
                drheading.append(node.text)

            for node in root.findall("./entry/dead-reckoning-orientation/pitch"):
                drpitch.append(node.text)

            for node in root.findall("./entry/dead-reckoning-orientation/roll"):
                droll.append(node.text)

            for node in root.findall("./entry/dead-reckoning-position/lon"):
                drlon.append(node.text)

            for ptch in root.findall("./entry/dead-reckoning-position/lat"):
                drlat.append(ptch.text)

            for node in root.findall("./entry/orientation/heading"):
                heading.append(node.text)

            for node in root.findall("./entry/orientation/pitch"):
                pitch.append(node.text)

            for node in root.findall("./entry/orientation/roll"):
                roll.append(node.text)

            for node in root.findall("./entry/position/depth"):
                depth.append(node.text)

            for node in root.findall("./entry/position/lat"):
                lat.append(node.text)

            for ptch in root.findall("./entry/position/lon"):
                lon.append(ptch.text)    

            nddf = pd.DataFrame(
                                   list(zip(drheading, drpitch, droll,drlat,drlon,heading, pitch, roll,depth,lat, lon)), 
                                   columns=['DRHeading', 'DRPitch', 'DRRoll','DRLat','DRLon','Heading','Pitch','Roll','Depth','Lat','Lon'])  
            nvdf=pd.concat([rtdf, nddf], axis=1)

        else:
            rtdf=pd.read_xml(files,names=None)
            tree = et.parse(files)
            root = tree.getroot()

            drheading = []
            drpitch=[]
            droll=[]
            drlat = []
            drlon=[]
            heading=[]
            pitch=[]
            roll=[]
            depth=[]
            lat=[]
            lon=[]

            for node in root.findall("./entry/dead-reckoning-orientation/heading"):
                drheading.append(node.text)

            for node in root.findall("./entry/dead-reckoning-orientation/pitch"):
                drpitch.append(node.text)

            for node in root.findall("./entry/dead-reckoning-orientation/roll"):
                droll.append(node.text)

            for node in root.findall("./entry/dead-reckoning-position/lon"):
                drlon.append(node.text)

            for ptch in root.findall("./entry/dead-reckoning-position/lat"):
                drlat.append(ptch.text)

            for node in root.findall("./entry/orientation/heading"):
                heading.append(node.text)

            for node in root.findall("./entry/orientation/pitch"):
                pitch.append(node.text)

            for node in root.findall("./entry/orientation/roll"):
                roll.append(node.text)

            for node in root.findall("./entry/position/depth"):
                depth.append(node.text)

            for node in root.findall("./entry/position/lat"):
                lat.append(node.text)

            for ptch in root.findall("./entry/position/lon"):
                lon.append(ptch.text)    

            nddf = pd.DataFrame(
                                   list(zip(drheading, drpitch, droll,drlat,drlon,heading, pitch, roll,depth,lat, lon)), 
                                   columns=['DRHeading', 'DRPitch', 'DRRoll','DRLat','DRLon','Heading','Pitch','Roll','Depth','Lat','Lon'])  
            df=pd.concat([rtdf, nddf], axis=1)

            nvdf=pd.concat([nvdf,df],ignore_index=True)            
                 
    labels = ['build-number',
                'build-tag',
                'calculate-magnetic-deviation',
                'max-valid-depth', 
                'dvl-timeout',
                'gps-timeout',
                'gps-validation-enabled',
                'veto-use-water-velocity',
                'station-keeping-enabled',
                'sound-velocity-timeout',
                'temperature-timeout',
                'seanav-timeout',
                'use-pressure',
                'max-allowed-variance',
                'pressure-timeout',
                'compass-timeout',
                'dead-reckoning-sog-timeout',
                'variance-exceeded-warning-level',
                'max-dead-reckoning-distance',
                'pressure-depth-conversion',
                'use-water-velocity',
                'density-abort-limit',
                'gps-variance',
                'lbl-variance',
                'revolutions-bias',
                'revolutions-scale',
                'dvl-bias',
                'dvl-scale',
                'gyro-bias',
                'control-rate',
                'motor-default',
                'stationary-radius',
                'stationary-p',
                'stationary-idle',
                'stationary-depth-timeout',
                'estimate-speed',
                'detect-ins-type',
                'ins-detect-timeout',
                'override-propulsion-ip',
                'send-nav-device-data',
                'observe-timer-on',
                'predict-timer-on',
                'passthrough-udp-actuator',
                'binary-log',
                'broadcast-interface',
                'broadcast-enable',
                'broadcast-frequency',
                'broadcast-navigation-message',
                'broadcast-ins-enabled',
                'broadcast-depth-message',
                'broadcast-sound-velocity-message',
                'rate',
                'control-priority',
                'control-priority-time',
                'idle-status',
                'last-command-elapsed',
                'maxWarningLevel',
                'pilot-status',
                'valid',
                'zero-altitude']
    
    nvdf=nvdf.drop(labels, axis=1)    
    nvdf["Lat"]=nvdf["Lat"].astype(str).str.replace('N', '')
    nvdf["Lon"]=nvdf["Lon"].astype(str).str.replace('W', '')
    nvdf["DRLat"]=nvdf["DRLat"].astype(str).str.replace('N', '')
    nvdf["DRLon"]=nvdf["DRLon"].astype(str).str.replace('W', '')
    
    
    # CONVERT DATA TO NUMERIC 
    cols=[i for i in nvdf.columns if i not in ["time","timestamp"]]
    for col in cols:
        nvdf[col]=pd.to_numeric(nvdf[col],errors='ignore',downcast='float')    
    
    # DOESNT WORK WITH LAT LONG (JUTS NOW) SO CONVERT TO FLOAT AGAIN!!
    nvdf["Lat"]=nvdf["Lat"].astype(float)
    nvdf["Lon"]=nvdf["Lon"].astype(float)
    nvdf["DRLat"]=nvdf["DRLat"].astype(float)
    nvdf["DRLon"]=nvdf["DRLon"].astype(float)
    
    # save as .csv file
    newstr = missionname.replace("_", "-")
    nvdf.to_csv(os.path.join(processedpath,newstr+'NAVdata.csv')) 
    
    return nvdf



### GPS data
def readgpslog(missionname,ldir,processedpath):    # get list of files
    files=os.path.join(ldir,'*gps-*.xml')
    flelist=glob.glob(files)
    # determine if files are zipped. If yes, unzip, if no, continue
    if not flelist:
        files=os.path.join(ldir,'*gps-*.xml.gz')    
        import gzip, shutil
        flelist=glob.glob(files)
        for i in flelist:
            with gzip.open(i, 'r') as f_in, open( i[:-3], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    # for each file, read to pandas dataframe and concatenate
    for count, fles in enumerate(flelist):
        if count==0:
            gpdf=pd.read_xml(fles)
        else:
            df=pd.read_xml(fles,names=None)
            gpdf=pd.concat([gpdf,df],ignore_index=True)
    # save as .csv file
    os.makedirs('data/nav-files', exist_ok=True)  
    gpdf.to_csv(os.path.join(processedpath,missionname+'GPSdata.csv'))     
    return gpdf

### SBP data
def readsbplog(missionname,ldir,processedpath):    # get list of files
    files=os.path.join(ldir,'*sbp*.xml')
    flelist=glob.glob(files)
    # determine if files are zipped. If yes, unzip, if no, continue
    if not flelist:
        files=os.path.join(ldir,'*sbp*.xml.gz')    
        import gzip, shutil
        flelist=glob.glob(files)
        for i in flelist:
            with gzip.open(i, 'r') as f_in, open( i[:-3], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    # for each file, read to pandas dataframe and concatenate
    for count, fles in enumerate(flelist):
        if count==0:
            sbpdf=pd.read_xml(fles)
        else:
            df=pd.read_xml(fles,names=None)
            sbpdf=pd.concat([sbpdf,df],ignore_index=True)
    # save as .csv file
    sbpdf.to_csv(os.path.join(processedpath,missionname+'SBPdata.csv'))       
    return sbpdf

### AANDERAA data
def readaandlog(missionname,ldir,processedpath):    # get list of files
    files=os.path.join(ldir,'*aanderaa*.xml')
    flelist=glob.glob(files)
    # determine if files are zipped. If yes, unzip, if no, continue
    if not flelist:
        files=os.path.join(ldir,'*aanderaa*.xml.gz')    
        import gzip, shutil
        flelist=glob.glob(files)
        for i in flelist:
            with gzip.open(i, 'r') as f_in, open( i[:-3], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    # for each file, read to pandas dataframe and concatenate
    for count, fles in enumerate(flelist):
        if count==0:
            aandf=pd.read_xml(fles)
        else:
            df=pd.read_xml(fles,names=None)
            aandf=pd.concat([aandf,df],ignore_index=True)
    # save as .csv file
    aandf.to_csv(os.path.join(processedpath,missionname+'aanderaadata.csv'))   
    return aandf