# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 10:18:04 2017

@author: rikhoekstra
"""
import os
import re
from ConfigParser import ConfigParser
import argparse
from lxml import etree
#from collections import Counter
from lxml.cssselect import CSSSelector
from unicodecsv import DictWriter



def sel_personen(term='resolutie p persoon', id="", fls=[], options=[], what='persoon'):
    """count index terms"""
    sel = CSSSelector(', '.join(options))
    rows = []
    result = []
    for fl in fls:
        try:
            doc = etree.parse(fl)
            root = doc.getroot()
            if what == 'persoon':
                res = find_personen(term, root)
            elif what == 'text':
                res = find_text(term, root)
            result.extend(res)
        except (IOError, etree.XMLSyntaxError):
            pass
    ress = [find_parent(p, 'resolutie') for p in result]
    for r in ress:
        z = find_parent(r, 'zittingsdag')
        idx = r.getparent().index(r)
        dag = "{d}-{m}-{y}".format(d=z.get('dag'),m=z.get('maand'),y=z.get('jaar'))
        x = sel(r)
        for p in x:
            trm = re.sub('[\\n\\t]','', p.text.strip())
            row = {'element': trm,
                   'type': p.tag,
                   'id': p.get('idnr'),
                   'zittingsdag': dag,
                   'resolutie': idx}
            rows.append(row)
    return rows

def find_personen(term, root):
    templ = """{term}[idnr="{idnr}"]""".format(term=term, idnr=id)
    selector = CSSSelector(templ)
    res = selector(root)
    return res

def find_text(term, root):
    result = root.xpath('resolutie[contains(.,term)]')
    return result
    
def find_parent(element, parent):
    """find specific parent element of element.
    """
    parenttag = element.getparent()
    while parenttag.tag != parent:
        parenttag = parenttag.getparent()
    return parenttag

def write2csv(flout, rows):
    flout = open(flout, 'w')
    w = DictWriter(flout, ['resolutie', 'zittingsdag', 'type', 'id', 'element'])
    w.writerows(rows)
    flout.close()
    print ("output written to %s" % flout.name)

def main(indir):
    fls = []

    for root, dirs, files in os.walk(indir):
        if root.find('schelling') == -1:
            fls.extend([os.path.join(root, f) for f in files if f.find('.xml')>-1])
    opts = []
    opts = [o for o in cp.options('options') if cp.get('options', o) == 'True']
    rows = sel_personen(id=args['persnr'], fls=fls, options=opts)
    return rows


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-o', '--optionfile',
                    help="ifile with options. Default ./persoon_parser.ini",
                    default="./persoon_parser.ini"
                    )
    ap.add_argument('-p', '--persnr',
                help="person id of the person to search")
                
    ap.add_argument('-t', '--text',
                help="text to search. Note: text is exact")
    args = vars(ap.parse_args())

    cp = ConfigParser()
    cp.read(args['optionfile'])
    basedir = cp.get('base', 'basedir')
    indir = os.path.join(basedir, cp.get('input', 'indir'))
    outfile = os.path.join(basedir, cp.get('output', 'outfile'))
    rows = main(indir)
    write2csv(outfile, rows)
