#!/usr/bin/python
__author__ = "Ehsan Kourkchi"
__copyright__ = "Copyright 02-11-2020"
__version__ = "v1.0"
__status__ = "Production"

import sys
import os
import subprocess
from math import *
import numpy as np
import scipy.ndimage
import random
import requests
from io import BytesIO
from PIL import Image

###############################

def converIMAGE(img_arr, angle=0., scale=1., size=64):
    
    if scale<1.:
        scale=1


    img_rot = scipy.ndimage.rotate(img_arr, -angle)

    N = img_rot.shape
    d = N[0]
    p =  int(d/scale)
    d1 = int(d/2-p/2)
    d2 = int(d1 + p)

    imgut = img_rot[d1:d2, d1:d2, :]

    img = Image.fromarray(imgut, 'RGB').resize((size,size))

    
    return img

###############################
if len(sys.argv)==7:
    RA  = sys.argv[1]
    Dec = sys.argv[2]
    npix = sys.argv[3]
    scale = float(sys.argv[4])
    angle = float(sys.argv[5])
    pix  = sys.argv[6]
    
    url = "http://skyserver.sdss.org/dr12/SkyserverWS/ImgCutout/getjpeg?TaskName=Skyserver.Explore.Image&ra="+RA+"&dec="+Dec+"&scale="+pix+"&width="+npix+"&height="+npix;
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img_arr = np.asarray(img)
elif len(sys.argv)==4:
    if sys.argv[1]=='local':
        scale = float(sys.argv[2])
        angle = float(sys.argv[3])
        upfile = './tmp.jpg'
        img = Image.open(upfile)
        img_arr = np.asarray(img)
        
        if len(img_arr.shape) == 2:
            img_arr = np.stack((img_arr,)*3, axis=-1)
        elif len(img_arr.shape) == 1:
            print("error")
            sys.exit()
        
        if len(img_arr.shape) == 3 and img_arr.shape[2]>3:
            img_arr = img_arr[:,:,0:3]            
    else: 
        print("error")
        sys.exit()
else:
    print("error")
    sys.exit()


nx, ny, _ = img_arr.shape
if ny<nx:
    d1 = int(nx/2-ny/2)
    d2 = int(ny + d1)
    img_arr = img_arr[d1:d2, :, :]
elif nx<ny:
    d1 = int(ny/2-nx/2)
    d2 = int(nx + d1)
    img_arr = img_arr[:, d1:d2, :]    
    #print("size")
    #sys.exit()    

###############################
if scale!=0:
    img = converIMAGE(img_arr, angle=angle, scale=scale, size=512)
    img.save('../inclination/galaxies/pgc0_d25x2_rot_gri.jpg', "JPEG")
else:
    img = converIMAGE(img_arr, angle=angle, scale=1, size=512)
    img.save('./tmp.jpg', "JPEG")    


print("success")
