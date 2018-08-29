# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 19:00:59 2016

@author: rikhoekstra
"""

import csv
import os
flin = open("/Users/rikhoekstra/surfdrive/emigratie/werkmateriaal/steekproef+edges.csv")
ref = open("/Users/rikhoekstra/surfdrive/emigratie/alledges.csv")
refcsv = csv.reader(ref)
refs = [row for row in refcsv]
refs = refs[1:]
indref = [rf[0] for rf in refs]

r = csv.reader(flin)
fledges = [row for row in r]

nims = []

for img in fledges[1:]:
    d = img[0].split('_')[-2]
    x = os.path.splitext(img[0])[0][-4:]
    ni = "_{:04d}{}".format(int(os.path.splitext(x)[0])+1, os.path.splitext(x)[1])
    nii = "_".join(img[0].split('_')[:3]) + ni + ".jpg"
    length = indref.index(nii)
    ll = refs[length][1]
    out = [nii, img[1], int(ll)]
    nims.append([img[0], img[1],  int(img[2])])
    nims.append(out)