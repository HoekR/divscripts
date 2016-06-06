# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 13:25:49 2015

@author: rik
"""

l = [1, 3, 5, 9, 13, 15, 17]
lst = iter(l)
vn = 0
nwlst = []

item = lst.next()
vn=0
while vn < max(l)+1:
    if vn <= item + 1:
        nwlst.append([vn, item])
        if vn == item +1:
            try:
                item = lst.next()
            except StopIteration:
                break
    vn += 1

nwlst.append([item, vn+1])
#    else:
#        print vn, item
#        break
print nwlst