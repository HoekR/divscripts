# -*- coding: utf-8 -*-
"""
Created on Mon May 13 10:00:04 2013

@author: rik
"""
import re, os, shutil, glob

def repllink(matchob):
    p = matchob
    descr = p.group(1)
    link = p.group(2)
    result = '<li><a href="{link}">{descr}</a></li>'.format(link=link, descr=descr)
    return result

def replhdr(matchob):
    level = 2
    p = matchob
    g = p.group(1)
    if g == '===':
        level = 1
    result = '<h{l}>{hdr}</h{l}>'.format(hdr=p.group(2), l=level)
    return result


def subtext(txt):
    txt = re.sub('(===)(.*)===', replhdr, txt)
    txt = re.sub('(==)([\w\s\.,]*)==', replhdr, txt)
    txt = re.sub('\{(.*)\}[\s,.]*\[(.*)\]', repllink, txt)
    return txt


