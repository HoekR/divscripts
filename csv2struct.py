# -*- coding: utf-8 -*-
"""
Created on Sun Aug 25 13:19:15 2013

@author: rik
"""

##---(Thu Aug 22 08:54:48 2013)---
from lxml import etree
from lxml import html
import csv
#from copyhelper import cont
import datetime, marshal, os, re
bdir = '/home/rik/Dropbox/jos compendium'


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
    v.text = etree.CDATA(val)
    return pm

#base is a boilerplate from wordpress export
doc = etree.parse(bdir + '/boilerplate_import.xml')
root = doc.getroot()
channel = root.find('channel')
x = re.compile('(?P<begindag>[0-9]+) t\/m (?P<einddag>[0-9]+)')


def convert_csv(fl=''):
    """for csv files"""
    kal1 = csv.DictReader(open(fl), delimiter=';')
    log = open('csvlog', 'wb')
    for item in kal1:
        make_record(item, fn=kal1.fieldnames, log = log)
    log.close()
    
def make_record(row, fn = [], dag=None, log='', volgnr=1):
    for name in fn:
        if name not in ['DAG', 'MAAND', 'JAAR']:
            if row[name]:
               item = make_item(row, name)
               channel.append(item)


def make_dates(row):
    if x.match(row['DAG']):
        y = x.match(row['DAG'])
        bd = y.groupdict()['begindag']
        ed = y.groupdict()['einddag']
        dag = bd
        edate = ''.join((row['JAAR'], row['MAAND'].zfill(2),ed.zfill(2)))
    else:
        dag = row['DAG']
        edate = ''
    date = ''.join((row['JAAR'], row['MAAND'].zfill(2), dag.zfill(2)))
#    try:
    dte = pmeta('date', date)
    edte = pmeta('einddatum', edate)
    return dte, edte, dag


def make_item(row, name, volgnr=3):
#        if 'Wagram' in row[name]:
#            print etree.tostring(list(channel)[-1])

        template = etree.Element('item')
        try:
            dates = make_dates(row)
        except:
            print( row)
        pubdate = etree.Element(wp+'pubDate')
        pubdate.text = str(datetime.datetime.now())
        pubdate = template.append(pubdate)
        postdate = etree.Element(wp+'post_date')
        dtext= '-'.join((dates[2].zfill(2), row['MAAND'].zfill(2), row['JAAR']))
        postdate.text = str(datetime.datetime.strptime(dtext, '%d-%m-%Y'))
        template.append(postdate)
        postdategmt = etree.Element(wp+'post_date_gmt')
        postdategmt.text = str(datetime.datetime.strptime(dtext, '%d-%m-%Y'))
        template.append(postdategmt)
        ttl=u''
        ttl=row[name]
        title = etree.SubElement(template, 'title')
        title.text = u''+ttl
        dsc = etree.Element(content+'encoded')
        desc = ttl.replace('\n', ' ')
        desc = desc.replace('\t', ' ')
        c = etree.CDATA(u''+desc)
        dsc.text = c
        category = etree.Element('category')
        category.set('domain', "soort_gebeurtenis" )
        category.set('nicename', name)
        category.text = name
#        txt = '
        edte = dates[1]
        for val in [dsc, dte, edte, category]:
            template.append(val)
        if 'Wagram' in row[name]:
            print (etree.tostring(list(channel)[-1]))
#            txt += '\t' + ' '.join(val.itertext())
#        log.write(txt+'\n')
            
        #not sure if the following is necessary, but it publishes items immediately
        status = etree.Element(wp+'status')
        status.text = 'publish'
        template.append(status)
        
        posttype = etree.Element(wp+'post_type')
        posttype.text = 'hist_events'
        template.append(posttype)
        volgnr='%s' % volgnr
        category = etree.Element('category')
        category.set('domain', "periode" )
        category.set('nicename', volgnr)
        category.text = volgnr
        template.append(category)

        return template


##make rest more configurable
#for fl in ['/home/rik/Dropbox/jos compendium/KALENDARIUM1815.csv', 
#           '/home/rik/Dropbox/jos compendium/KALENDARIUM181415.csv',
#           '/home/rik/Dropbox/jos compendium/KALENDARIUM.csv', 
#           '/home/rik/Dropbox/jos compendium/KALENDARIUM1814.csv', 
#           '/home/rik/Dropbox/jos compendium/KALENDARIUM1813-1815.csv', 
#           '/home/rik/Dropbox/jos compendium/KALENDARIUM1813.csv']
convert_csv(fl='KALENDARIUM181314.csv') 

out = open(bdir + '/kalendarium18131814.xml', 'wb')
out.write(etree.tostring(doc, encoding="utf-8", pretty_print=True))
out.close()