# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 12:51:08 2015

@author: rik
"""

import Image
import ImageDraw

img = Image.new("RGB", (400,400), "white")
draw = ImageDraw.Draw(img)

coords = [(100,70), (220, 310), (200,200)]
dotSize = 2

for (x,y) in coords:
    draw.rectangle([x,y,x+dotSize-1,y+dotSize-1], fill="black")

img.show()