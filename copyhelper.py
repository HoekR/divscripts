# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 12:50:53 2013

@author: rik
"""
from lxml import etree, html
from copy import deepcopy

def cont(el,target):
    res = etree.Element(target)
    res.text = el.text or ''
    for child in el.iterchildren():
        res.append(deepcopy(child))
    res.tail = (el.tail or '')
    return res

def stringify_children(node):
    from lxml.etree import tostring
    from itertools import chain
    parts = ([node.text] +
            list(chain(*([tostring(c,encoding="utf-8")] for c in node.getchildren()))) +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))

def choptext(txt, pargr):
    """usage: ch = copyhelper.choptext(txt, ['Algemeen', '2a', '2b', '2c', '2d'])
    ch.keys()
    for key in ch.keys():
    print ch[key][:100] eigenlijk html.parse"""
    i=0
    out = {}
    end = 0
    pd = [txt.find(item+'.') for item in pargr]
    pd.append(len(txt))
    pds = zip(pd, pd[1:])
    #print pds
    d = dict((item, v) for item, v in zip(pargr, pds))
    for item in d.keys():
        out[item] = txt[d[item][0]:d[item][1]]
    return out

def writedoc(doc, categorien=[]):
    d = open(doc)
    txt = d.read()
    d.close()
    ch=choptext(txt, pargr=categorien)
#    for key in ch.keys():
#        frg = html.fromstring(ch[key])
#        categ = [categorien]
#        categ.append(key)
#        print categ
    return ch
#        boeken2struct.writeout(frg, '/'+key+'.xml', categ)