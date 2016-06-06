# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 13:15:34 2015

@author: rik
"""
import csv
import re

def handle(func, infile='sibajak__.csv', outfile='', nwfld='', fld='Item title'):
    inf = open(infile)
    flout = open(outfile,'w')
    r = csv.DictReader(inf)
    r.fieldnames.append(nwfld)
    w = csv.DictWriter(flout, r.fieldnames)
    w.writeheader()
    for row in r:
        txt = row[fld]
        nwval = func(txt)
        try:
            row[nwfld] = nwval
        except AttributeError:
            pass
        w.writerow(row)
    inf.close()
    flout.close()


class PatterMatcher(object):
    def __init__(self):
        self.patterns = {}
        pat = "(([0-9]+[th]?) ([january|february|march|april|may|june|july|august|september|october|november|december]+) ([0-9]+))"
        self.add_pattern(name='datepattern', pattern=re.compile(pat))
                    
    def add_pattern(self, name='', pattern=''):
        self.patterns[name] = pattern
        



def normalize(t):
    nt = t.split('/')
    if re.search('[0-9]+', nt[-1]):
        return ''
    else:
        nt[-1] = re.sub('van[ de]+r?','',nt[-1])