# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 13:19:15 2013

@author: rik
"""

##---(Thu Aug 22 08:54:48 2013)---
from lxml import etree
from lxml import html
from lxml.html.clean import Cleaner
import lxml.html.soupparser as soupparser
from lxml.cssselect import CSSSelector
from copyhelper import cont, choptext, writedoc
import datetime, marshal, os, re
bdir = '/home/rik/Dropbox/jos compendium'


#get wp ids from file
wpidsfl = open('wpids.mrs')
wpids = marshal.load(wpidsfl)
wpidsfl.close()

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

#base is a boilerplate from wordpress export
doc = etree.parse(bdir + '/boilerplate_import.xml')
root = doc.getroot()
channel = root.find('channel')

#todo: parsing in commandline values
bld = soupparser.parse("/home/rik/Dropbox/jos compendium/jos/out/bibliografie2.html")
broot = bld.getroot()

def convert_bron(broot=broot, 
                 hfdst=[], 
                 categories=[], 
                 rectype="", 
                 startnr=10, 
                 log=''):
    """for bronnen files generated from word"""

    cleaner = Cleaner(remove_tags=['a']) #for stripping description
    selector = CSSSelector('li')
    items = [cont(el, 'div') for el in selector(broot)]
    i = startnr
    for item in items:
        #selector1 = CSSSelector('i')
        selector3 = CSSSelector('a')
        try:
            ttl = ' '.join([cont(el).itertext() for el in selector3(item)])
        except TypeError:
            ttl = " ".join(item.itertext())
        #import pdb;pdb.set_trace()
        ttl = ttl.replace('\n', ' ')
        ttl = ttl.replace('\t', ' ')
        template = etree.Element('item')
        title = etree.SubElement(template, 'title')
        dsc = etree.Element(content+'encoded')
        try:
            desc = html.fragment_fromstring(html.tostring(item))
            desc = cleaner.clean_html(desc)
            desc = html.tostring(desc)
        except TypeError:
            desc = item
        desc = desc.replace('\n', ' ')
        desc = desc.replace('\t', ' ')
        c = etree.CDATA(desc)
        dsc.text = c
        template.append(dsc)
        if ttl.strip() == '':
            ttl = item
            try:
                ttl = ' '.join(ttl.itertext())
            except AttributeError:
                pass
        title.text = ttl
        
        #not sure if the following is necessary, but it publishes items immediately
        status = etree.Element(wp+'status')
        status.text = 'publish'
        template.append(status)
        
        posttype = etree.Element(wp+'post_type')
        posttype.text = rectype
        template.append(posttype)
        for categ in categories:
#            import pdb; pdb.set_trace()
            if categ == 'Algemeen':
                categ = hfdst[0]
            category = etree.Element('category')
            category.set('domain', "periode" )
            category.set('nicename', categ)
            category.text = categ
            template.append(category)
        try:
            link = selector3(item)[0].get('href')
        except IndexError:
#            print html.tostring(item), 'geen link'
            link = u' '
        except TypeError:
            print item
            link = u' '
        try:
            lnk = pmeta('url', link)
        except TypeError:
            print html.tostring(item), 'uuuhhh geen link'    
            link = u' '
            lnk = pmeta('url', link)
        template.append(lnk)  
        volgnr = pmeta('order', u'%s' % i)
        template.append(volgnr)
        channel.append(template)
        log.write('%s - %s\n' %(i, ttl))
        i+=10

    return root, i

def writeout(fl, flout, hfdst=[], categories=[], rectype=""):
    ch = writedoc(fl, categories)
    log = open('blog.txt', 'wb')
    startnr = 10
    for key in categories:
        log.write('\n\n%s\n\n' % key)
        bld = soupparser.fromstring(ch[key])
        x = convert_bron(broot=bld, 
                         hfdst=hfdst, 
                         categories=[key],
                         rectype=rectype,
                         startnr=startnr,
                         log=log)
        startnr = x[1]
    out = open(bdir + '/' + rectype + hfdst[0] +'.xml', 'wb')
    out.write(etree.tostring(x[0], encoding="unicode"))
    print 'written', bdir + '/' + rectype + hfdst[0] + '.xml'
    out.close()
    log.close()


