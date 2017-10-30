import dicom
import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
import csv

# indicate path to image data
PathDicom = "C:\\Users\\David\\Documents\\CT\\CT_data\Images"
lstFilesDICOM = []
# read all images in path
for dirName, subdirList, fileList in os.walk(PathDicom):
  for filename in fileList:
    lstFilesDICOM.append(os.path.join(dirName, filename))

# read first image in order to find image dimensions and pixel spacing
a = dicom.read_file(lstFilesDICOM[0])

# get pixel dimensions
PixelDims = (int(a.Rows), int(a.Columns), len(lstFilesDICOM))
PixelSpacing = (float(a.PixelSpacing[0]), float(a.PixelSpacing[1]), float(a.SliceThickness))
print('PixelSpacing:')
print(PixelSpacing)


# create a np array for storing the pixel intensities
dicomArray = np.zeros(PixelDims, dtype=a.pixel_array.dtype)
print(dicomArray.shape)

# read in all dicom images
for filenameDICOM in lstFilesDICOM:
  ds = dicom.read_file(filenameDICOM)
  # store raw image data
  dicomArray[:, :, lstFilesDICOM.index(filenameDICOM)] = ds.pixel_array

# convert to Hounsfield Units 
intercept = a.RescaleIntercept
slope = a.RescaleSlope  
dicomArray = dicomArray*slope + intercept

# plot one of the images
plt.figure()
#plt.pcolormesh(x,y,np.flipud(dicomArray[:,:,33]))
plt.imshow(dicomArray[:,:,50], cmap='gray')
plt.hold(True)

# import contour of coronary vessel
with open('C:\\Users\\David\\Documents\\CT\\contour1.txt') as csvfile:
  contour = csv.reader(csvfile)
  x= []
  y= []
  for row in contour:
    x.append(int(row[0]))
    y.append(int(row[1]))
	
# plot contour on vessel
plt.plot(x,y, 'r', linewidth=1)
plt.show()  

# simple thresholding (200 <= HU >= 600)
arrayThresh = dicomArray.copy()
arrayThresh[arrayThresh < 200] = 0
arrayThresh[arrayThresh > 600] = 0
arrayThresh[arrayThresh > 0] = 1

plt.figure()
#plt.pcolormesh(x,y,np.flipud(dicomArray[:,:,33]))
plt.imshow(arrayThresh[:,:,50], cmap='gray')
plt.hold(True)
plt.show()  