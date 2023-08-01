# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 22:22:56 2022

@author: SA03JH
Processes jpg images from GAVIA AUV Grasshopper camera

Corrects illumination by divinding by average image and normalisation
Extracts metadata using exiftool.exe (must be in path) and converts to decimal coords


"""
import os  
import glob 
import skimage
from skimage import io
from skimage import filters
from scipy import ndimage
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import exiftool
import numpy, PIL
from PIL import Image
import re

#Path to process with two \\ at end, eg path=r"T:\Nicol\20190720141751\\"
path=r"C:\Data\Gavia Images\20230120123513\\"
#Output folder eg "\12052022\\"
#save_folder="\20230120123513_Proc\\"
save_folder='20230120123513_Proc'
#Image Enhancement method, 'CLAHE' or 'AverageSubtraction'
ImageEnhancement='AverageSubtraction'
#outpath
outpath=os.path.join(path,save_folder)

#Makes save folder
try: 
    #os.mkdir(path+save_folder) 
    os.mkdir(os.path.join(path,save_folder))
except OSError as error: 
    print(error)
    
    
 #liests files   
files=glob.glob(path+'*.jpg')



# Assuming all images are the same size, get dimensions of first image
#w,h=Image.open(files[0]).size
h,w,d=(io.imread(files[0])).shape

N=len(files)
# Create a numpy array of floats to store the average (assume RGB images)
arr=numpy.zeros((h,w,3),numpy.float)

# Build up average pixel intensities, casting each image as an array of floats
for im in files:
    #imarr=numpy.array(Image.open(im),dtype=numpy.float)
    imarr=numpy.array(io.imread(im),dtype=numpy.float)
    arr=arr+imarr/N

# Round values in array and cast as 8-bit integer
arr1=numpy.array(numpy.round(arr),dtype=numpy.uint8)

# Generate, save and preview final image
out=Image.fromarray(arr1,mode="RGB")
out.save(os.path.join(outpath,"Average.png"))
#out.show()


df = pd.DataFrame(columns=['Image_Name','path', 'altitude', 'depth','heading','lat','lon','pitch','roll','surge','sway'])



loopy=range(len(files))

with exiftool.ExifToolHelper() as et:
        metadata = et.get_metadata(files)

for i in loopy:
    file=files[i]
    files1 = [file]
    print('processing image  '+file)

    #with exiftool.ExifToolHelper() as et:
    #    metadata = et.get_metadata(files1)
        
        
    #for d in metadata:
    #    print("{:20.20} {:20.20}".format(d["SourceFile"],
    #                                     d["EXIF:DateTimeOriginal"]))
    
    comment=metadata[i]['File:Comment']
    altitude = re.search('<altitude>(.*)</altitude>', comment).group(1)
    depth = re.search('<depth>(.*)</depth>', comment).group(1)
    heading = re.search('<heading>(.*)</heading>', comment).group(1)
    lat = re.search('<lat>(.*)</lat>', comment).group(1)
    lon = re.search('<lon>(.*)</lon>', comment).group(1)
    pitch = re.search('<pitch>(.*)</pitch>', comment).group(1)
    roll = re.search('<roll>(.*)</roll>', comment).group(1)
    surge = re.search('<surge>(.*)</surge>', comment).group(1)
    sway = re.search('<sway>(.*)</sway>', comment).group(1)
    
    
    signlat = 1
    if lat[-1] == "S":
        signlat = -1    
    lenlat = len(lat)
    latCor = signlat * (float(lat[:2]) + float(lat[2:lenlat-2])/60.0)
    
    signlon=1
    if lon[-1] == "W":
        signlon = -1
    lenlon = len(lon)
    lonCor = signlon * (float(lon[:3]) + float(lon[3:lenlon-2])/60.0)
    
    
    #im1=numpy.array(Image.open(file),dtype=numpy.float)
  
    
    if ImageEnhancement=="AverageSubtraction":
        im1=numpy.array(io.imread(file),dtype=numpy.float)
        imcor=im1-arr
        out2=skimage.exposure.rescale_intensity(imcor, out_range='uint8')
    if ImageEnhancement=="CLAHE":
        im1=numpy.array(io.imread(file))
        #imcor=out2 = skimage.exposure.equalize_adapthist(im1, kernel_size=64)
        imcor=out2 = skimage.exposure.equalize_adapthist(im1)
        out2=skimage.exposure.rescale_intensity(imcor, out_range='uint8')
    

    #
    
    io.imsave(os.path.join(path,save_folder, os.path.basename(file)),out2)

    #df.loc[i] = [os.path.basename(file),file,altitude,depth,heading,latCor,lonCor,str(float(pitch)+270),roll,surge,sway]
    df.loc[i] = [os.path.basename(file),file,altitude,str(-float(depth)),heading,latCor,lonCor,pitch,roll,surge,sway]
    
    
df.to_csv(os.path.join(path,save_folder,'coords.csv'))