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
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, square
from skimage.measure import regionprops
from skimage.color import label2rgb
from skimage.feature import corner_harris,corner_peaks


im = io.imread('/Users/rikhoekstra/Downloads/test.jpg')
from skimage.color import rgb2gray
image = rgb2gray(im)

# apply threshold
thresh = threshold_otsu(image)
bw = closing(image > thresh, square(3))

#bw = corner_peaks(corner_harris(image),min_distance=2)

# remove artifacts connected to image border
cleared = bw.copy()
#clear_border(cleared)

# label image regions
label_image = label(cleared)
image_label_overlay = label2rgb(label_image, im)

fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(60, 60))
ax.imshow(image_label_overlay)

for region in regionprops(label_image):

    # skip small images
    if region.area < 50:
        continue

    # draw rectangle around segmented coins
    minr, minc, maxr, maxc = region.bbox
    rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                              fill=False, edgecolor='red', linewidth=2)
    ax.add_patch(rect)

plt.show()
