#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 15:14:43 2015

@author: rik
"""

import marshal
import csv
import re
import os
#from itertools import chain
from collections import deque, defaultdict


def standard_run(basedir='',
                 fin='', 
                 fcomp='',
                 flout=''):
    """standard run 
    """
    os.chdir(basedir)
    x = setup_files(fin=fin, fcomp=fcomp)
    n = compare_names(x['nms'], x['nms2_expanded'])    
    fc = filter_compared(n,x['nms2_expanded'], x['nms_rev'])
    simplematched(fc, x['nms2_expanded'], x['nms_rev'], fl=flout)


pats = ['van ', 'de ', 'der ', 't ', 'den', 'ten']
#for item in nms:
#    name = ' '.join([item['prs_tussenvoegsel'], item['prs_achternaam']])
#    nwow = {'id':item['\xef\xbb\xbf"prs_id"'], 'name': name, 'gd': item['prs_geboortedatum'], 'aank' :item['aankomst']}
#    nms2.append(nwow)

def csv2mar(infl='/home/rik/Dropbox/Link to emigrantenkaarten/NT00335/NT00335_persoon.csv', 
            outfl='', pat=''):
    """pat should be shipname"""
    fl = open(infl)
    r = csv.DictReader(fl)
    outrows = deque()
    for rw in r:
        if rw['naam_vervoer'].lower().find(pat) > -1:
            outrows.append(rw)
    fl.close()
    if not outfl:
        outfl = pat + '.mar'
    ofl = open(outfl, 'w')
    outrows = list(outrows)
    marshal.dump(outrows, ofl)
    ofl.close()


def csv2rolls(infl='', outfl='', pat='nominal rolls'):
    """infl should be csv file with ship data"""
    fl = open(infl)
    r = csv.DictReader(fl)
    outrows = deque()
    for rw in r:
        if rw['Item title'].lower().find('nominal rolls') > -1:
            outrows.append(rw)

    ofl = open(outfl, 'w')
    w = csv.DictWriter(ofl, fieldnames=r.fieldnames)
    w.writeheader()
    w.writerows(outrows)
    ofl.close()
    return "written {outfl}".format(outfl=outfl) 




def setup_files( 
         fin='sibajak__.csv',
         fcomp=''
         ):
    """setup fin is infile in csv format
    fcomp is csv file for comparison"""

    flin = open(fin)
    r = csv.DictReader(flin)
    
    nms = {}
    nms_rev = {}
    #setup infile        
    for i in r:
        key = i['Control symbol']
        key = key.split('/')[-1]#for control symbols with prefixes
        if re.search('[0-9][0-9]+', key): #inconsistent barcodes
            key = i['Item title']
            if key.find('-')==-1: #inconsistent descriptions
                key = key[:100] #we do not need all this text
        nms[key] = i['Item barcode']#for faster lookup
        nms_rev[i['Item barcode']] = [i['Item title'].lower(), i['Digitised item']]#lower for inconsistency
        
    flin.close()
    
    #setup comparefile
    
    min = open(fcomp)
    d = marshal.load(min)
    min.close()
    nms2 = {}
    nms2_expanded = {i['\xef\xbb\xbf"prs_id"']:[
                                                i['prs_achternaam'], 
                                                i['prs_initialen'],
                                                i['prs_geboortedatum'],
                                                i['aankomst']
                                                ] for i in d}
    return {'nms':nms, 'nms2_expanded': nms2_expanded, 'nms_rev': nms_rev}
    
#for i in d:
#    key = i['prs_achternaam']
#    if nms2.has_key(key):
#        key = ' '.join([i['prs_achternaam'], i['prs_initialen']])
#    nms2[key.lower()] = i['\xef\xbb\xbf"prs_id"']
#nms3 = {i['prs_achternaam'].lower():i['\xef\xbb\xbf"prs_id"'] for i in d}



def compare_names(nms, nms2_expanded):
    nms4 = defaultdict(list)

    fnd = str.find # for speed
    for k in nms2_expanded.keys():
        i = nms2_expanded[k][0]
        il = i.lower()
        for j in nms.keys():
            jl = j.lower()
            if fnd(jl, il) > -1:
                nms4[k].append(nms[j])
    return nms4

def filter_compared(nms4, nms2_expanded, nms_rev, filename='matched.csv'):
    """filter down names and write to csv (TODO:change the writing?"""
    nms5 = defaultdict(list)
            
    nout = open(filename, 'w')
    #pickle.dump(nms4, nout)
    
    wr = csv.writer(nout)
    fnd = str.find
    for item in nms4.items():
        nm = nms2_expanded[item[0]]
        for i in item[1]:
            val = nms_rev[i][0]
            p = fnd(val, nm[0].lower())
            names = val[p+len(nm[0]):].strip()
            names = names.replace(',','')
            names = names.split(' ')
            names = [n[:1] for n in names if n[:1].isalpha() is True]
            ltrs = nm[1].split('.')
            fnames = names[:len(ltrs)-1]
    #        print fnames, len(ltrs), ltrs
            l = ''.join(ltrs).lower()
            y = ''.join(fnames)
            if y in l:
                nms5[item[0]].append(i)
            
    r = [[item[0]] + item[1] for item in nms5.items()]           
                
    wr.writerows(r)
    nout.close()
    return nms5

def simplematched(nms5,nms2_expanded, nms_rev, fl='sib_matched_s.csv'):
    """write simple matched items to file"""
    flout = open(fl, 'w')
    w = csv.writer(flout)

    for item in nms5.keys():
        if len(nms5[item]) == 1:
            rr1 = nms2_expanded[item]
            rr2 = [nms5[item][0]] + nms_rev[nms5[item][0]]
            row = rr1 + rr2
            w.writerow(row)
            
    flout.close()

