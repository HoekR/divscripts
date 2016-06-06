# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 16:20:22 2014

@author: rik
"""

from lxml import html, etree
import lxml.html.clean as clean
try:
    import lxml.html.soupparser as soupparser
except ImportError:
    pass
import os
from argparse import ArgumentParser
#from lxml.html.clean import clean_html
import subprocess
import os
import uuid
from glob import glob


"""
http://stackoverflow.com/questions/7470333/remove-certain-attributes-from-html-tags"""

def cleaner(instring='', infile='', outfile='', soup=True):
    '''clean html'''
    if instring:
        doc = instring
    else:
        fl = open(infile)
        doc = fl.read()
        fl.close()
    for element in ['span', 'div', 'font', 'u']:
        doc = doc.replace("%s>" % element, "%s> " % element)
    if soup:
        doc = soupparser.fromstring(doc)
    else: #fallback
        doc = html.fromstring(doc)

#    safe_attrs = clean.defs.safe_attrs
    clean.defs.safe_attrs = frozenset(['href', 'alt', 'id', 'src', 'width', 'height'])
    c = clean.Cleaner(scripts=True, 
                embedded=True, 
                meta=True, 
                style=True, 
                remove_tags = ['span', 'div', 'font', 'u'],
                safe_attrs_only=True)
    c.safe_attrs=frozenset(['href', 'alt', 'id', 'src', 'width', 'height']) #this seems to work no it doesnt
    d2 = c.clean_html(doc)
    #ps = 
    #for p in ps:
    #	if p.find('a'):#
    #		if p.find('a').find('img'):
    #			print ok
    d2 = squash_paragraph_attributes(d2)    
    if outfile:
        flout = open(outfile, 'wb')
        flout.write(html.tostring(d2, method="html", encoding='utf-8', pretty_print=True))
        flout.close()
    else:
        return  etree.tostring(d2, method="html", encoding='utf-8')
def squash_paragraph_attributes(doc):
    for p in doc.xpath('//p'):
        for np in p.xpath('.//p'):
            p.attrib.update(dict(np.attrib))
    return doc

def recurse(basedir, outdir):
    '''recurse over directory'''
    if not os.path.exists(outdir):
            os.mkdir(outdir)
    print outdir
    for infile in glob(basedir+'/*.html'):
        outfile = os.path.splitext(os.path.basename(infile))[0] + '.html'
        outfile = os.path.join(outdir, outfile)
        cleaner(infile=infile, outfile=outfile)
        print 'cleaned %s -> %s' %( infile, outfile)

def main():
    """main"""
    usage = "usage: %prog [args] arg"
    parser = ArgumentParser(usage)
    parser.add_argument("-r", "--recurse", dest="recurse", action="store_true",
                      help="""clean all files""")
    parser.add_argument("-f", "--filename", dest="filename",
                      help="specify csv filename as input")
    parser.add_argument("-b", "--basedir", dest="basedir",
                        help="specify basic directory")
    parser.add_argument("-o", "--outdir", dest="outdir",
                        help="specify destination directory")
    parser.add_argument("-x", "--outfile", dest="outfile",
                      help="""destination filename""")
    parser.add_argument("-s", "--soup", dest="soup", action="store_true",
                      help="""destination filename""")
                      
                    
    

    args = parser.parse_args()
        
    
    
    if not args.basedir:
        args.basedir = "."

    if not args.outdir or args.outdir=="":
        args.outdir = "."
    
    if args.recurse:
       recurse(basedir=args.basedir, 
                outdir=args.outdir)
    else:
        infile = os.path.join(args.basedir, args.filename)
        outfile = os.path.join(args.outdir, args.outfile)
        if args.soup == True:
            cleaner(infile, outfile, soup=True)
        else:
            cleaner(infile, outfile, soup=False)           
        

if __name__ == "__main__":
    main()