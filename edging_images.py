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
    


from functools import partial
from multiprocessing.pool import Pool


def crns(fls):
    corners = {}
    for i in fls:
        image = ndi.imread(i)
        grimage = rgb2gray(image)
        corners[i] = len(corner_peaks(corner_harris(grimage),min_distance=2))
    return corners

import os
from argparse import ArgumentParser

def main():
    """main"""
    parser = ArgumentParser(description="""
    detects edges for directory of images. 
    Writes number of edges
    per file to csv file in directory""",
                            prog="edging_images.py")
    parser.add_argument("-p", "--path", required=True, 
                        help="""path to store images.  
                                If path does not exist it will be created """)

    #try:
    args = parser.parse_args()
    path = os.path.join(args.path, '*.jpg' )
    fls = glob.glob(path)
    corners = partial(crns, fls)
    with Pool(8) as p:
        p.map(crns, fls)
    outpath = os.path.join(args.path, 'edges.csv')
    import csv
    w = csv.writer(open(outpath, 'w'))
    w.writerow(['file', 'corners'])
    for corner in corners.items():
        out = [os.path.basename(corner[0]), corner[1]]
        w.writerow(out)
    
#    except:
#        parser.print_help()


if __name__ == "__main__":
    main()