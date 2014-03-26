# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 10:48:06 2013

@author: rik
"""
from lxml import html
from lxml.html.builder import *

doc = html.parse("/home/rik/Dropbox/jos compendium/jos/nin/2beeldmateriaal.html")
root = doc.getroot()
body = root.body
d = body.find('div')
if not d:
    d = body

imgs = body.xpath('.//img')
print '%s images' % (len(imgs))

h = HTML(HEAD())
b =  BODY( CLASS("main"))
t = TABLE()

#l = list(p.itersiblings())
from copy import deepcopy
def cont(el):
    res = TD()
    res.text = el.text or ''
    for child in el.iterchildren():
        res.append(deepcopy(child))
    res.tail = (el.tail or '')
    return res

def resize(img, wdef=200):
    h = int(img.get('height'))
    w = float(img.get('width'))
    print 'h, w: ', h, w
#    if h < w:
    nh = wdef/w * h
    print 'nh: %0d ' % nh
    img.set('height', "%0d" % nh)
    img.set('width', "%s" % wdef)

    

    
for img in imgs:
    p = img.getparent()
    while p.tag != 'p':
        p = p.getparent()
    try:
        i = d.index(p)
    except AttributeError:
        print img.getparent().tag
    tr = TR()
    lnk = d[i+2]
    a = lnk.find('a')
    try:
        ref = a.get('href')
    except AttributeError:
        print 'missende link'
        ref = ''
    resize(img)
    #print img.get('height'), img.get('width')
    dv = A(img, href=ref, target="_blank")
    tr.append(TD(dv))
    tr.append(cont(d[i+1]))#description
    t.append(tr)
 
style = """<style><!--
.entry-content td {vertical-align: middle;}
a img {border: 1px solid #DDDDDD;
    padding: 6px;}
--></style>"""   
b.append(t)
h.append(b)

outdoc = html.tostring(h)

outdoc = outdoc.replace('\n', ' ')
outdoc = outdoc.replace('<t', '\n <t')
outdoc = outdoc.replace('<em><i>', ' <em>')
outdoc = outdoc.replace('</i></em>', '</em> ')
outdoc = outdoc.replace('src="', 'src="http://compendium1813.huygens.knaw.nl/wp-content/uploads/2013/07/')



flout = open("/home/rik/Dropbox/jos compendium/jos/nout/beeldmateriaal2.html", "wb")
flout.write(outdoc)
flout.close()