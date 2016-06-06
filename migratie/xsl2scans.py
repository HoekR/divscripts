# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 16:48:07 2015

@author: rik
"""
import csv
from operator import itemgetter


def ind(l, l2):
    result = [] 
    nb = 0
    ne = -1
    for i in l2:
        ne = l.index(i)
        r = l[nb:ne]
        result.append(r)
        nb = ne
    result.append(l[nb:-1])
    return result


def relpers2scan(flin):
    """link person identifier to scans numbers
    example of flin: /home/rik/Dropbox/Link to emigrantenkaarten/bak_nw_south_wales_bew.csv
    """
    flin = open(flin)
    reader = csv.DictReader(flin)
    scans = []
    for i in reader:
        try:
            scans.append([int(i['imagenr']), i['id_persoon'], i['aant']])
        except ValueError:
            try:
                scans.append([int(i['imagenr']), i['prs_uuid'], i['aant']])
            except ValueError:
                print i
    scans.sort(key=itemgetter(0))
#    iterscans = iter(scans)
    lst = [i[0] for i in scans]
    m = max(lst)
    #vn = 1 # 1 based scan numbering numbers
    scanlist = range(min(lst),m + 2)
#    print scanlist[-1]
#    item = iterscans.next()
    nwscans = []
    nb = 0
    ne = -1
    for i in scans:
        ne = scanlist.index(i[0]) + 1
        r = scanlist[nb:ne]
        for item in r:
            nwscans.append([item, i[1], i[2]])
        nb = ne
    for item in scanlist[nb:-1]:
        nwscans.append([item, i[1], i[2]])
    return nwscans
#    while vn < m + 1:
#            if vn > m:
#                import pdb; pdb.set_trace()
#            try:
#                if vn <= item[0] + 1:
#                    nwscans.append([vn, item[1], item[2]])
#                    if vn == item[0] + 1:
#                        item = iterscans.next()
#                    vn += 1
#            except StopIteration:
#                nwscans.append([vn+1, item[1], item[2]])
        
    
    
#    scans.sort(key=itemgetter(0))
    

def scansout(flout, scans):
    """write scans to file"""
    fileout = open(flout, 'w')
    writer = csv.writer(fileout)
    writer.writerow(['scan_nr', 'id_persoon', 'opmerkingen'])
    for i in scans:
        writer.writerow(i)
    fileout.close()
    return "written to {flout}".format(flout=flout)


def main(flin, flout):
    scans = relpers2scan(flin)
    x = scansout(flout, scans)
    print x
"""pth = "NL-HaNA_2.05.159_27_"
flout = open('nwsouthwales.sql', 'w')
for i in scans:
    flout.write(templ % (i[0], i[1], pth + i[2]))
flout.close()"""