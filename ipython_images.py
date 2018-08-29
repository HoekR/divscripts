# -*- coding: utf-8 -*-
"""
Created on Wed May 11 12:12:50 2016

@author: rikhoekstra
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
from skimage import feature
from skimage.color import rgb2gray
from skimage.feature import corner_harris,corner_peaks
import glob


# More pyplot!
def show_corners(corners,image,title=None):
    """Display a list of corners overlapping an image"""
    fig = plt.figure()
    plt.imshow(image)
    # Convert coordinates to x and y lists
    y_corner,x_corner = zip(*corners)
    plt.plot(x_corner,y_corner,'o') # Plot corners
    if title:
        plt.title(title)
    plt.xlim(0,image.shape[1])
    plt.ylim(image.shape[0],0) # Images use weird axes
    fig.set_size_inches(np.array(fig.get_size_inches()) * 1.5)
    plt.show()
    print "Number of corners:",len(corners)


def save_corners(corners,image,outnm='',title=None):
    """Display a list of corners overlapping an image"""
    fig = plt.figure()
    # Convert coordinates to x and y lists
    y_corner,x_corner = zip(*corners)
    plt.plot(x_corner,y_corner,'o') # Plot corners
    if title:
        plt.title(title)
    plt.xlim(0,image.shape[1])
    plt.ylim(image.shape[0],0) # Images use weird axes
    fig.set_size_inches(np.array(fig.get_size_inches()) * 1.5)
    plt.savefig(outnm)
    

fls = glob.glob('/Users/rikhoekstra/Downloads/*.jpg')



def crns(fls):
    corners = {}
    for i in fls:
        image = ndi.imread(i)
        grimage = rgb2gray(image)
        corners[i] = len(corner_peaks(corner_harris(grimage),min_distance=2))
    return corners



#import matplotlib.pyplot as plt
#import matplotlib.patches as mpatches
#
#from skimage.filters import threshold_otsu
#from skimage.segmentation import clear_border
#from skimage.measure import label
#from skimage.morphology import closing, square
#from skimage.measure import regionprops
#from skimage.color import label2rgb
#
#thresh = threshold_otsu(grim)
#bw = closing(grim > thresh, square(3))
#bw
#cleared = bw.copy()
#clear_border(cleared)
#label_image = label(cleared)
#image_label_overlay = label2rgb(label_image, image=grim)
#fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6,6)0
#)
#fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6,6))
#ax.imshow(image_label_overlay)
#for region in regionprops(label_image):
#    minr, minc, maxr, maxc = region.bbox
#    rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
#                              fill=False, edgecolor='red', linewidth=2)
#    ax.add_patch(rect)
#    
#plt.show()
#fig, ax = 
#fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6,6))
#ax.imshow(image_label_overlay)
#binary_image = np.where(grim > np.mean(grim),1.0,0.0)
#binary_image
#show_images(images=[grim,binary_image],
#            titles=["Grayscale","Binary"])
#def show_images(images,titles=None):
#    """Display a list of images"""
#    n_ims = len(images)
#    if titles is None: titles = ['(%d)' % i for i in range(1,n_ims + 1)]
#    fig = plt.figure()
#    n = 1
#    for image,title in zip(images,titles):
#        a = fig.add_subplot(1,n_ims,n) # Make subplot
#        if image.ndim == 2: # Is image grayscale?
#            plt.gray() # Only place in this blog you can't replace 'gray' with 'grey'
#        plt.imshow(image)
#        a.set_title(title)
#        n += 1
#    fig.set_size_inches(np.array(fig.get_size_inches()) * n_ims)
#    plt.show()
#    
#show_images(images=[grim,binary_image],
#            titles=["Grayscale","Binary"])
#from skimage.filter import gaussian_filter
#
#blurred_image = gaussian_filter(equalized_image,sigma=3)
#really_blurred_image = gaussian_filter(equalized_image,sigma=6)
#
#from skimage.exposure import equalize_hist
#
#equalized_image = equalize_hist(gray_image)

