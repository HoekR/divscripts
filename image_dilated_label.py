# -*- coding: utf-8 -*-
"""
Created on Tue May 10 21:26:41 2016

@author: rikhoekstra
"""

"""
===================
Label image regions
===================

This example shows how to segment an image with image labelling. The following
steps are applied:

1. Thresholding with automatic Otsu method
2. Close small holes with binary closing
3. Remove artifacts touching image border
4. Measure image regions to filter small objects

"""
#import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import ndimage as ndi
from skimage import io
from skimage.filters import threshold_otsu
from skimage.filters import gaussian_filter
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.measure import find_contours
from skimage.morphology import closing, square, dilation
from skimage.measure import regionprops
from skimage.color import label2rgb
from skimage.feature import corner_harris,corner_peaks
from skimage.feature import canny
from skimage import img_as_float


def redilate(im, n=1):
    for i in range(5):
        im = img_as_float(dilation(im, square(n)))
        i += 1
    return im

im = io.imread('/Users/rikhoekstra/Downloads/test3.jpg')
from skimage.color import rgb2gray
img = rgb2gray(im)
img = gaussian_filter(img, sigma=3.5)
#
## apply threshold
#thresh = threshold_otsu(image)
#bw = closing(image > thresh, square(3))
#
##bw = corner_peaks(corner_harris(image),min_distance=2)
#
## remove artifacts connected to image border
#cleared = bw.copy()
##clear_border(cleared)

image = canny(img)

#image = corner_peaks(corner_harris(img),min_distance=2)
#import numpy as np
#image=image.astype( np.float64)
nim = redilate(image, 5)
contours = find_contours(image, 0.8, fully_connected='low', positive_orientation='high')

# label image regions
lbl = label(nim)
labeled = label2rgb(lbl, im)



fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(60, 60))
ax.imshow(labeled)

for region in regionprops(lbl):

    # skip small images
    if region.area < 100:
        continue

    # draw rectangle around segmented coins
    minr, minc, maxr, maxc = region.bbox
    rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                              fill=False, edgecolor='blue', linewidth=2)
    print region.area
    ax.add_patch(rect)



plt.show()
