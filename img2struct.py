# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 14:40:05 2013

@author: rik
"""
from lxml import etree
from lxml import html
from lxml.html.clean import Cleaner
import lxml.html.soupparser as soupparser
from lxml.cssselect import CSSSelector
import copyhelper
from copyhelper import cont, writedoc
import os, marshal
bdir = '/home/rik/Dropbox/jos compendium'



#namespaces
class XmlNs(object):
    def __init__(self, key, url):
        self.__name__ = key
        self.url = url
        self.ns = '{{{url}}}'.format(url=self.url)

nsmap={'wp':"http://wordpress.org/export/1.2/",
        'excerpt':"http://wordpress.org/export/1.2/excerpt/",
        'content':"http://purl.org/rss/1.0/modules/content/"}
wp = XmlNs('wp', "http://wordpress.org/export/1.2/").ns
content = XmlNs('content', "http://purl.org/rss/1.0/modules/content/").ns


def pmeta(key, val):
    """for making a wordpress meta key"""
    pm = etree.Element(wp+'postmeta')
    k = etree.SubElement(pm, wp+'meta_key')
    k.text = key
    v = etree.SubElement(pm, wp+'meta_value')
    v.text = etree.CDATA(val)
    return pm
    
#get wp ids from file
wpidsfl = open('wpids.mrs')
wpids = marshal.load(wpidsfl)
wpidsfl.close()

#base is a boilerplate from wordpress export
doc = etree.parse(bdir + '/boilerplate_import.xml')
root = doc.getroot()
channel = root.find('channel')

#todo: parsing in commandline values
bld = soupparser.parse("/home/rik/Dropbox/jos compendium/jos/out/biografieen2.html")
broot = bld.getroot()

fl = open("/home/rik/Dropbox/jos compendium/jos/nin/2beeldmateriaal.html")
txt = fl.read()
ch = copyhelper.choptext(txt, ['Algemeen', '2a', '2b', '2c', '2d'])

def convert_imgs(broot=broot,
                hfdst=[],
                categories=[],
                rectype='biografie',
                startnr=10,
                log=''):
    s = CSSSelector('img')
    imgs = s(broot)
    #imgs.reverse()
    i = startnr
    for img in imgs:
        p = img.getparent()
        try:
            while p.tag != 'p':
                p = p.getparent()
            ind = broot.index(p)
        except AttributeError:
            print etree.tostring(img), img.getparent().tag
            ind = broot.index(img)
#        tr = TR()
        imlink = img.get('src')
        try:
            ilink = os.path.splitext(os.path.basename(imlink))[0].lower()
            ilink = ilink.replace('%20','')
            imid = wpids[ilink]
        except KeyError:
            imid = '0'
            print ilink, 'niet aangetroffen'
            

        lnk = broot[ind+2]
        a = lnk.find('a')
        try:
            ref = a.get('href')
        except AttributeError:
            print ilink, 'missende link', lnk.tag, etree.tostring(lnk)
            ref = ''
#        resize(img)
        #print img.get('height'), img.get('width')
#        dv = A(img, href=ref, target="_blank")
#        tr.append(TD(dv))
        desc=cont(broot[ind+1],'div')#description
#        t.append(tr)
        

        if desc.find('i') is not None:
            ttl = etree.Element('title')
            ii = desc.findall('i')
            ttl.text = ''
            for e in ii:
                ttl.text += e.text
            ttl = ''.join(ttl.itertext())
        else:
            ttl = ''.join(desc.itertext())
        ttl = ttl.replace('\n', ' ')
        ttl = ttl.replace('\t', ' ')
        template = etree.Element('item')
        title = etree.SubElement(template, 'title')
        title.text=ttl
        dsc = etree.Element(content+'encoded')
        template.append(dsc)
        desc = etree.tostring(desc)
        desc = desc.replace('\n', ' ')
        desc = desc.replace('\t', ' ')        
        c = etree.CDATA(desc)
        dsc.text = c
        
        #not sure if the following is necessary, but it publishes items immediately
        status = etree.Element(wp+'status')
        status.text = 'publish'
        template.append(status)
        
        posttype = etree.Element(wp+'post_type')
        posttype.text = rectype
        template.append(posttype)    
        for categ in categories:
#            import pdb; pdb.set_trace()
            category = etree.Element('category')
            category.set('domain', "periode" )
            category.set('nicename', categ)
            category.text = categ
            template.append(category)
        try:
            link = ref
        except:
            print html.tostring(a), 'geen link'
    
        lnk = pmeta('url', link)
        template.append(lnk)
        tn = pmeta('_thumbnail_id', imid)
        template.append(tn)
        volgnr = pmeta('order', u'%s' % i)
        template.append(volgnr)
        channel.append(template)
        log.write('%s - %s\n' %(i, ttl))
        i+=10

    return root, i
        
def writeout(fl, flout, hfdst=[], categories=[], rectype=""):
    ch = writedoc(fl, categories)
    log = open('blog'+hfdst[0]+ '.txt', 'wb')
    startnr = 10
    for key in categories:
        log.write('\n\n%s\n\n' % key)
        bld = soupparser.fromstring(ch[key])
        x = convert_imgs(broot=bld, 
                         hfdst=hfdst, 
                         categories=[key],
                         rectype=rectype,
                         startnr=startnr,
                         log=log)
        startnr = x[1]
    out = open(bdir + '/' + rectype + key +'.xml', 'wb')
    out.write(etree.tostring(x[0], encoding="unicode"))
    print 'written', bdir + '/' + rectype + key +'.xml'
    out.close()
    log.close()



