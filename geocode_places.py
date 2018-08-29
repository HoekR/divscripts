#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 16:10:22 2018

@author: rikhoekstra
"""
import geocoder

infl = open('/Users/rikhoekstra/surfdrive/workshop_datascopes/datasets_dag2/bewerkte_bestanden/13_geo.csv')
r = csv.DictReader(infl, delimiter=";")
rows = [row for row in r]
places  =[row['sorteerwoord'] for row in rows]

res = []

for p in places:
    g = geocoder.google(p, key="AIzaSyCReTbCP4DY1PUWtw-eR2C2razxRWLjw8I")
    res.append({p: g.geojson})
    
for row in res:
    result[list(row.keys())[0]] = row[list(row.keys())[0]]

nrows = {rw['trefwoord']: len(rw['verwijzing'].split(','))}
nresult = []

for item in nrows:
    ires = {'keyword': item}
    ires['aantal'] = nrows.get(item)
    if result.get(item):
        for i in result.get(item).get('features'):
            if i.get('properties').get('country', '') != 'US':
                pr = i.get('properties')
                for k in ['country','county','lat','lng']:
                    ires[k] = pr.get(k, '')
    nresult.append(ires)



for item in nresult:
    if item['keyword'] == 'Batavia':
        x = item
   
     
list(x.keys())
w = csv.DictWriter(outfl, list(x.keys()))
w.writerows(nresult)
outfl.close()
outfl = open('/Users/rikhoekstra/surfdrive/workshop_datascopes/datasets_dag2/bewerkte_bestanden/13_geo_extended.csv', 'w')
w = csv.DictWriter(outfl, list(x.keys()), delimiter='\t')
w.writeheader()
w.writerows(nresult)
outfl.close()

indonesia = [row for row in nresult if row.get('country')=='ID']
len(indonesia)
india = [row for row in nresult if row.get('country')=='IN']
len(india)