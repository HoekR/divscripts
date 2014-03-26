# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 13:19:15 2013

@author: rik
"""

##---(Thu Aug 22 08:54:48 2013)---
from lxml import etree
from lxml import html
from copyhelper import cont
import datetime, marshal, os
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
bld = html.parse("/home/rik/Dropbox/jos compendium/jos/nout/beeldmateriaal2.html")
body = bld.getroot().body

#this is rather specific for image html files generated from word
table = body.find('table')
trs = table.findall('tr')
for tr in trs:
    tds = tr.findall('td')
    a = tds[0].find('a')
    link = a.get('href')
    img = a.find('img')
    imlink = img.get('src')
    try:
        imid = wpids[os.path.splitext(os.path.basename(imlink))[0].lower()]
    except KeyError:
        imid = '0'
        print imlink, 'niet aangetroffen'
        
    desc = cont(tds[1], 'p')
    if tds[1].find('i') is not None:
        ttl = etree.Element('title')
        ii = tds[1].findall('i')
        ttl.text = ''
        for i in ii:
            ttl.text += i.text
    else:
        ttl = desc

    template = etree.Element('item') #, nsmap)
    template.append(ttl)
    dsc = etree.Element(content+'encoded')
    c = etree.CDATA(etree.tostring(desc))
    dsc.text = c
    template.append(dsc)
    
    #not sure if the following is necessary, but it publishes items immediately
    status = etree.Element(wp+'status')
    status.text = 'publish'
    template.append(status)
    
    posttype = etree.Element(wp+'post_type')
    posttype.text = 'afbeelding'
    template.append(posttype)
    for categ in hfdst+categories:
#            import pdb; pdb.set_trace()
            category = etree.Element('category')
            category.set('domain', "periode" )
            category.set('nicename', categ)
            category.text = categ
            template.append(category)
    lnk = pmeta('url', link)
    template.append(lnk)  
    tn = pmeta('_thumbnail_id', imid)
    template.append(tn)

    channel.append(template)


out = open(bdir + '/wp_imgs_chap2.xml', 'wb')
out.write(etree.tostring(doc, encoding="unicode", pretty_print=True))
out.close()