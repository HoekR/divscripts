# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 15:21:34 2013

@author: rik
"""
import bio2struct, bron2struct

ind = os.path.join("/home/rik/Dropbox/jos compendium", outdir, '*[Bb]iogra*.html')

for fl in glob.glob(ind):
    h = os.path.basename(fl)[0]
    bio2struct.writeout(fl, '', hfdst=[h], categories=['Algemeen', h+'a', h+'b', h+'c', h+'d', h+'e'], rectype="biografie")
    
ind = os.path.join("/home/rik/Dropbox/jos compendium", outdir, '*[Bb]iogra*.html')
for fl in glob.glob(ind):
    h = os.path.basename(fl)[0]
    bio2struct.writeout(fl, '', hfdst=[h], categories=['Algemeen', h+'a', h+'b', h+'c', h+'d', h+'e'], rectype="biografie")
    
    