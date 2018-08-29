# -*- coding: utf-8 -*-
"""
Created on Thu May 12 16:29:16 2016

@author: rikhoekstra
"""

"""
===============
Contour finding
===============

``skimage.measure.find_contours`` uses a marching squares method to find
constant valued contours in an image.  Array values are linearly interpolated
to provide better precision of the output contours.  Contours which intersect
the image edge are open; all others are closed.

The `marching squares algorithm
<http://www.essi.fr/~lingrand/MarchingCubes/algo.html>`__ is a special case of
the marching cubes algorithm (Lorensen, William and Harvey E. Cline. Marching
Cubes: A High Resolution 3D Surface Construction Algorithm. Computer Graphics
(SIGGRAPH 87 Proceedings) 21(4) July 1987, p. 163-170).

"""
import numpy as np
import matplotlib.pyplot as plt

from skimage import measure
from skimage import io



# Construct some test data
#x, y = np.ogrid[-np.pi:np.pi:100j, -np.pi:np.pi:100j]
#r = np.sin(np.exp((np.sin(x)**3 + np.cos(y)**2)))

im = io.imread('/Users/rikhoekstra/Downloads/test.jpg')
from skimage.color import rgb2gray
image = rgb2gray(im)



# Find contours at a constant value of 0.8
contours = measure.find_contours(image, 0.8)
#from skimage import morphology
#cleaned = morphology.remove_small_objects(contours, 21)
# Display the image and plot all contours found
fig, ax = plt.subplots()
ax.imshow(image, interpolation='nearest', cmap=plt.cm.gray)

for n, contour in enumerate(contours):
    ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()
