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


cleaner = Cleaner()

#get wp ids from file
#wpidsfl = open('wpids.mrs')
#wpids = marshal.load(wpidsfl)
#wpidsfl.close()

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
    if not val:
        val=''
    v.text = etree.CDATA(val)
    return pm

#base is a boilerplate from wordpress export
doc = etree.parse(bdir + '/boilerplate_import.xml')
root = doc.getroot()
channel = root.find('channel')

#todo: parsing in commandline values
bld = soupparser.parse("/home/rik/Dropbox/jos compendium/jos/out/biografieen2.html")
broot = bld.getroot()

def convert_bio(broot=broot,
                hfdst=[],
                categories=[],
                rectype='biografie',
                startnr=10,
                log=''):
    """for bronnen files generated from word"""
    selector = CSSSelector('li p')
    items = selector(broot)
    i = startnr
#    print len(items)
    for item in items:
        #selector1 = CSSSelector('i')
        selector1 = CSSSelector('a')
        a = item.find('a')
        ttl = u''+item.text_content()
        ttl = ttl.replace('\n\t', ' ')
        ttl = ttl.replace('\n', ' ')
        template = etree.Element('item')
        title = etree.SubElement(template, 'title')
        title.text = ttl
#        print 'ttl:', ttl
        dsc = etree.Element(content+'encoded')
        desc = html.fragment_fromstring(etree.tostring(item))
        desc = cleaner.clean_html(desc)
        desc = etree.tostring(desc,method="html")
        desc = desc.replace(u'\n', u' ')
        desc = desc.replace(u'\t', u' ')
        c = etree.CDATA(desc)
        dsc.text = c
        template.append(dsc)
        
        #not sure if the following is necessary, but it publishes items immediately
        status = etree.Element(wp+'status')
        status.text = 'publish'
        template.append(status)
        
        posttype = etree.Element(wp+'post_type')
        posttype.text = 'biografie'
        template.append(posttype)    
        for categ in categories:
#            import pdb; pdb.set_trace()
            category = etree.Element('category')
            category.set('domain', "periode" )
            if categ == 'Algemeen':
                categ = hfdst
            category.set('nicename', categ)
            category.text = categ
            template.append(category)
        try:
            link = a.get('href')
            lnk = pmeta('url', link)
        except (IndexError, TypeError, AttributeError):
            print html.tostring(item), 'geen link'
        try:
            tt = ttl.find(':')
            titel = ttl[:tt]
            ttb = titel.rfind(')')
            function = titel[ttb+2:].strip()
            bjr = titel.find('(')
            jaren = titel[bjr+1:ttb]
            jrs = jaren.split('-')
            try:
                beginjaar = jrs[0]
                djaar = jrs[1]
            except IndexError:
                beginjaar = ''
                djaar = ''
                if djaar == '':
                    print html.tostring(item), 'geen link'
            mo = titel[:bjr]
            fn = mo.find(',')
            lastname = mo[:fn]
            firstname = mo[fn+1:]
#            else:
#                gd = mo.groupdict()
#                firstname = u''+gd['voornamen']
#                lastname = u''+gd['achternaam']
            fn = pmeta('fullname', firstname)
            ln = pmeta('last_name', lastname)
            l = pmeta('life', beginjaar)
            d = pmeta('death_date', djaar)
            fu = pmeta('function', function)
            for att in [fn, ln, l, d, fu]:
                template.append(att)
        except AttributeError:
            print titel
        template.append(lnk)  
        channel.append(template)
        log.write('%s - %s\n' %(i, ttl))
        i+=10

    return root, i

def writeout(fl, flout, hfdst=[], categories=[], rectype="", startnr=10):
    ch = writedoc(fl, categories)
    log = open('biolog' + hfdst[0] +'.txt', 'wb')
    for key in categories:
        startnr = startnr
        log.write('\n\n%s\n\n' % key)
#        instr = ch[key].encode("utf-8")
        bld = soupparser.fromstring(ch[key])
        x = convert_bio(broot=bld, 
                         hfdst=hfdst, 
                         categories=[key],
                         rectype=rectype,
                         startnr=startnr,
                         log=log)
        startnr = x[1]
    out = open(bdir + '/' + rectype + '_'+key +'.xml', 'wb')
    out.write(etree.tostring(x[0], encoding='utf-8'))
    print 'written', bdir + '/' + rectype + '_' + key +'.xml'
    out.close()
    log.close()
