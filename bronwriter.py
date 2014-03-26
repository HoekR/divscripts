# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 12:26:32 2013

@author: rik
"""
from lxml import html
from lxml.html.builder import *

doc = html.parse('/home/rik/Dropbox/jos compendium/jos/nin/2bronnen.html')
root = doc.getroot()
body = root.body

h = HTML(HEAD(TITLE("brontest")),
)
b =  BODY( CLASS("main"))

from copy import deepcopy
def cont(el):
    res = SPAN() #what else
    try:
        res.text = el.text or ''
    except AttributeError:
        res.txt = 'dummy'
    try:
        for child in el.iterchildren():
            res.append(deepcopy(child))
    except AttributeError:
        pass
    try:
        res.tail = (el.tail or '')
    except AttributeError:
        pass
    return res


links = body.iterlinks()
for link in links:
    p = link[0].getparent()
    while p.tag != 'p':
        p = p.getparent() #go up in hierarchy to p element
    i2 = cont(p.getprevious()) #text in paragraph before
    dv = A(i2, href=link[2], target="_blank")
    b.append(DIV(dv))

h.append(b)

outdoc = html.tostring(h)

outdoc = outdoc.replace('\n', ' ')
outdoc = outdoc.replace('\t', ' ')
outdoc = outdoc.replace('<div', '\n <div')
outdoc = outdoc.replace('<em><i>', ' <em>')
outdoc = outdoc.replace('</i></em>', '</em> ')


flout = open("/home/rik/Dropbox/jos compendium/jos/nout/bronnen2.html", "wb")
flout.write(outdoc)
flout.close()