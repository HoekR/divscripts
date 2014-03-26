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
from copyhelper import cont, writedoc
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
bld = soupparser.parse("/home/rik/Dropbox/jos compendium/jos/nin/2bronnen.html")
broot = bld.getroot()

def convert_bron( broot=broot, hfdst=[], categories=[]):
    """for bronnen files generated from word"""
    cleaner = Cleaner(remove_tags=['a']) #for stripping description
    selector = CSSSelector('li')
    items = [cont(el, 'div') for el in selector(broot)]
    i = 10
    for item in items:
        #selector1 = CSSSelector('i')
        selector3 = CSSSelector('a')
        try:
            ttl = ' '.join([cont(el) for el in selector3(item)])
        except TypeError:
            ttl = etree.tostring(item, method='text', encoding='unicode')
        ttl = ttl.replace('\n', ' ')
        ttl = ttl.replace('\t', ' ')
        template = etree.Element('item')
        title = etree.SubElement(template, 'title')
        title.text = ttl
        dsc = etree.Element(content+'encoded')
        desc = html.fragment_fromstring(html.tostring(item))
        desc = cleaner.clean_html(desc)
        desc = html.tostring(desc)
        desc = desc.replace('\n', ' ')
        desc = desc.replace('\t', ' ')
        c = etree.CDATA(desc)
        dsc.text = c
        template.append(dsc)
        
        #not sure if the following is necessary, but it publishes items immediately
        status = etree.Element(wp+'status')
        status.text = 'publish'
        template.append(status)
        
        posttype = etree.Element(wp+'post_type')
        posttype.text = 'bron'
        template.append(posttype)
        for categ in hfdst+categories:
#            import pdb; pdb.set_trace()
            category = etree.Element('category')
            category.set('domain', "periode" )
            category.set('nicename', categ)
            category.text = categ
            template.append(category)
#        category = etree.Element('category')
#        category.set('domain', "periode" )
#        category.set('nicename', "2-opstand-en-de-verdrijving-Fransen")
#        category.text = "2 opstand en de verdrijving Fransen"
#        template.append(category)
        try:
            link = selector3(item)[0].get('href')
        except IndexError:
            print html.tostring(item), 'geen link'
    
        lnk = pmeta('url', link)
        template.append(lnk)
        volgnr = pmeta('order', u'%s' % i)
        template.append(volgnr)
        channel.append(template)
        i+=10
        channel.append(template)
    return root

#convert_bron()

def writeout(fl, flout, hfdst=[], categories=[]):
    ch = writedoc(fl, categories)
    for key in ch.keys():
        bld = soupparser.fromstring(ch[key])
        x = convert_bron(broot=bld, hfdst=hfdst, categories=[key])
        out = open(bdir + '/' + 'bronnen' + hfdst[0] +'.xml', 'wb')
        out.write(etree.tostring(x, encoding="unicode"))
        print 'written', bdir + '/' + 'bronnen' + hfdst[0] +'.xml'
        out.close()
#
#out = open(bdir + '/wp_biblio_chap2.xml', 'wb')
#out.write(etree.tostring(doc, encoding="unicode", pretty_print=True))
#out.close()
        
