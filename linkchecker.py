# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 13:41:25 2013

@author: rik
"""

import datetime, urllib2, re
 
url='http://google.com/search?' # Set web search URL
hits={'link':'http://www.inghist.nl/'}
 
# Generate web search term
hits['web search term']=urllib2.quote('link:'+hits['link'])
 
# Execute web search
urlstr='%sq=%s'%(url,hits['web search term'])
url=urllib2.Request(urlstr)
url.add_header('User-Agent','')
url=urllib2.urlopen(url).read()
 
# Store date and time of web search
hits['datetimeutc']=datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
 
# Parse web search results to determine hits
hits['hits']=re.search('Results <b>1</b> - <b>10</b> of about <b>(?P<hits>.+?)</b>',url)
if hits['hits']!=None:
    hits['hits']=hits['hits'].group('hits')
    hits['hits']=hits['hits'].replace(',','')
    hits['hits']=int(hits['hits'])
else:
    hits['hits']=0
 
print hits['hits']