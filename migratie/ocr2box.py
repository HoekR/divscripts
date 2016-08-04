# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 16:23:58 2015

@author: rik

from https://github.com/jflesch/pyocr
"""
import os
import sys
from PIL import Image


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


def im2fl(flin, flout, verbose=True):
    """image to linebox file"""
    parse2string(flin, flout)
#    floutt = open(flout, 'wb')
#    floutt.write(outstr)
#    floutt.close()
    print "{flin} written to {flout}".format(flin=flin, flout=flout)

def in2out(indir, flin, outdir):
    flout = os.path.splitext(flin)[0] + '.txt'
    out=(os.path.join(indir, flin), os.path.join(outdir, flout))
    return out
 
def recurse(indir, outname="out", tl=im2fl):
    """perform on indir outdir is indir+/out"""
    from multiprocessing.pool import Pool
    try:
        os.mkdir(os.path.join(indir, outname))
    except OSError:
        pass
    outdir = os.path.join(indir, outname)
    fls = [x for x in os.listdir(indir) if x.find('jpg')!=-1]
    fls2 = [in2out(indir, flin, outdir) for flin in fls] 
    pool = Pool(8)
    pool.map(tl, fls2)
    
        

