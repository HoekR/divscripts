# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 21:41:22 2015

@author: rik
"""
import os
import os.path
import csv
import lxml.html.soupparser as soupparser
from lxml.cssselect import CSSSelector
from lxml import etree
import re

def table2csv(table):
    """tablerows to csv rows from html table. 
    May have to extend td selector for th using 
    something like re.compile('t[dh]')?"""
    trselector = CSSSelector('tr')
    tdselector = CSSSelector('td')
    trs = trselector(table)
    rows = []
    for item in trs:
        row = []
        pat = re.compile('(B=[0-9]+)')
        for i in tdselector(item):
            td = etree.tostring(i, method='html', encoding='utf8')
            if td.find('ViewImage.aspx')>-1:
                td = pat.search(td).group()
            else:
                td = etree.tostring(i, method='text', encoding='utf8')
                td = td.strip()
            row.append(td)
        rows.append(row)
    return rows

def selecttable(doc, sexpr):
    """table from (html) doc element"""
#    tableselector = CSSSelector('table') 
    tableselector = CSSSelector(sexpr)
    tables = tableselector(doc)
    table = tables[0] # or what
    return table

def write_csv(outfile, rows):
    """write rows to csv file"""
    flout = open(outfile, 'w')
    w = csv.writer(flout)
    w.writerows(rows)
    flout.close()

def concat_csv(fls=[], outfl='', fieldnames=[]):
    """assuming the same fields (maybe a subset 
    but then fieldnames should begiven)
    get fieldnames from file, then use DictWriter
    to concatenate all files to outfile"""
    if not fieldnames:
        fl = open(fls[0])
        r = csv.reader(fl)
        fieldnames = r.next()
        fl.close()
  
    outfile = open(outfl, 'wb')
    w = csv.DictWriter(outfile, fieldnames)
    w.writeheader()
    for fin in fls:
        if fin != outfl:
            fl = open(fin)       
            r = csv.DictReader(fl)
#        import pdb; pdb.set_trace()
            try:
                [w.writerow(row) for row in r]
            except ValueError:
                print fl
    outfile.close()        
    

def main(basedir='', outdir='', infile='', outfile='', sexpr='.SearchResults'):
    """basic setup from directory"""
    os.chdir(basedir)  
    if not outfile:
        outfile = os.path.splitext(infile)[0] + '.csv'
    doc = soupparser.parse(infile)
    table = selecttable(doc, sexpr)
    rows = table2csv(table)
    write_csv(outfile,rows)