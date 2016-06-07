# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 12:49:19 2016

@author: rikhoekstra
"""
import os, fnmatch

def recursive_glob(treeroot, pattern):
    results = []
    for base, dirs, files in os.walk(treeroot):
        goodfiles = fnmatch.filter(files, pattern)
        results.extend(os.path.join(base, f) for f in goodfiles)
    return results