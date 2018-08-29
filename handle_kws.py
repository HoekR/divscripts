# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 10:58:36 2016

@author: rikhoekstra
"""

import re

infl = '/Volumes/Elements/gm/out/257_pers.txt'

pat = re.compile('([A-Za-z]*)')

def handle(infl):
    kw = open(infl)
    pkw = kw.readlines()
    pkwa=[l.strip() for l in pkw]
    pers = [pat.findall(l) for l in pkwa]
    pp = [[i for i in l if i != ''] for l in pers]
    print("aantal %s" %len(pp))
    np = []
    for item in pp:
        if item != []:
            if len(item) > 2:
                if 'ook' in item[1:]:
                    item = item[:item.index('ook')]
                item = [item[0], ' '.join(item[1:])]
            if len (item) > 1:
                item = ', '.join(item)
            else: 
                item = item[0]
            np.append(item)
    return np
        