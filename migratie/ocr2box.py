# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 16:23:58 2015

@author: rik

from https://github.com/jflesch/pyocr
"""
import os
import sys
import glob
from PIL import Image
import logging
import multiprocessing
from multiprocessing.pool import Pool
from argparse import ArgumentParser

import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'tesseract'
#
#langs = tool.get_available_languages()
#print("Available languages: %s" % ", ".join(langs))
#lang = langs[0]
#print("Will use lang '%s'" % (lang))
## Ex: Will use lang 'fra'
#
#txt = tool.image_to_string(
#    Image.open('test.png'),
#    lang=lang,
#    builder=pyocr.builders.TextBuilder()
#)
#word_boxes = tool.image_to_string(
#    Image.open('test.png'),
#    lang=lang,
#    builder=pyocr.builders.WordBoxBuilder()
#)
#line_and_word_boxes = tool.image_to_string(
#    Image.open('test.png'), lang=lang,
#    builder=pyocr.builders.LineBoxBuilder()
#)
#
## Digits - Only Tesseract
#digits = tool.image_to_string(
#    Image.open('test-digits.png'),
#    lang=lang,
#    builder=pyocr.tesseract.DigitBuilder()
#)

lang = 'nld'

def parseim(fl, lang='nld', tool=tool):
    flin = Image.open(fl)
    img = flin.convert('LA')
    line_boxes = tool.image_to_string(img, 
                                       lang=lang, 
                                       builder=pyocr.builders.LineBoxBuilder())
    return line_boxes

def parse2string(flin, flout, lang='nld', tool=tool):
    flin = Image.open(flin)
    img = flin.convert('LA')
    out = tool.image_to_string(img, 
                                       lang=lang, 
                                       builder=pyocr.builders.TextBuilder())
    out = out.encode('utf8')
    flout = open(flout, 'w')
    flout.write(out)



def write_boxes_to_string(line_box, verbose=True):
    """write lines and wordboxes to string"""
    out = u''
    template = "{w[0][0]},{w[0][1]} - {w[1][0]},{w[1][1]}"
    for word in line_box:
        out += "{w}----: ".format(w=line_box.index(word))
        out += template.format(w=word.position) + '\n'
        for box in word.word_boxes:
            out += '       ' + template.format(w=box.position) + '    '
            if verbose == True:
                out += box.content +'\n'
    out = out.encode('utf8')
    return out


def im2fl(fls=(), verbose=False):
    """image to linebox file"""
    
    flin = fls[0]
    flout = fls[1]
    parse2string(flin, flout)
#    floutt = open(flout, 'wb')
#    floutt.write(outstr)
#    floutt.close()
    if verbose == True:
        print "{flin} written to {flout}".format(flin=flin, flout=flout)

def in2out(indir, flin, outdir):
    flout = os.path.splitext(flin)[0] + '.txt'
    out=(os.path.join(indir, flin), os.path.join(indir, outdir, flout))
    return out

def recurse(indir, outname="out", tl=im2fl):
    """perform on indir outdir is indir+/out"""

    logging.info('%s started' % indir)
    try:
        os.mkdir(os.path.join(indir, outname))
    except OSError:
        logging.info('%s already existing' % indir)
    outdir = os.path.join(indir, outname)
    fls = glob.glob(os.path.join(indir, "*.jpg"))
    fls2 = []
    for flin in fls:
        out = in2out(indir, flin, outdir)
        if not os.path.exists(out[1]):
            fls2.append(out)
    poolsize = multiprocessing.cpu_count() * 4
    pool = multiprocessing.pool.Pool(poolsize, maxtasksperchild=4)
    pool.map(tl, fls2)
    pool.close()
    pool.join()
    logging.info('%s done' % indir)

def main():
    """main"""
    parser = ArgumentParser(description="""
    performs ocr on all images in directory""",
                            prog="ocr2box.py")
    parser.add_argument("-p", "--path", required=True, 
                        help="""root to retrieve images.  
                                If path does not exist it will be created """)

    #try:
    import pdb;pdb.set_trace()
    logging.basicConfig(filename='/home/rik/migrants/ocring.txt', 
                        format='%(asctime)s %(message)s',
                        level=logging.DEBUG)   
    args = parser.parse_args()
    rt = args.path
    for root, d, files in os.walk(rt):
        recurse(root)
    return "ready"

if __name__ == "__main__":
    main()
