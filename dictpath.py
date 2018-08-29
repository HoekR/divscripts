# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 10:59:18 2017

@author: rikhoekstra
"""
from collections import OrderedDict, MutableMapping
struct = {'a':1, 
            'b': {'c':2, 'd':3},
            'e': ['f', 'g'],
            'h': [{'i':4, 'j':5}, {'k':6, 'l':7}],
            'm': {'n': [{'o':8, 'p':9}]}
}

class DictPath(object):
    def __init__(self,  dictionary):
        self.dictionary = dictionary
        self.results = []
        self.dpth = self.triage('', self.dictionary, results=[])
        
        
    def new_prefix(self, oldprefix, addition, sep='/'):
        addition = '%s' % addition        
        newprefix = sep.join([oldprefix, addition])
        return newprefix
        
    def keys2path(self, prefix, dictionary):
        results = []        
        for key in dictionary.keys():
            tprefix = self.new_prefix(prefix, key)
            res = dictionary[key]
            res = self.triage(results, tprefix, res)
#            result = [(tprefix, res)]
            results.extend(res)
        if not isinstance(results, list):
            results = [results]
        return results
        
    def triage(self, prefix, ob, results=[]): 
        results = results
        if isinstance(ob, MutableMapping):
            result = self.keys2path(prefix, ob)
        elif isinstance(ob, list):
            for item in ob:
                nr = '%s' % ob.index(item)
                prefix = self.new_prefix(prefix, nr)
                result = self.triage(results, prefix, item)
        else:
            result = [(prefix, ob)]
        if not isinstance(results, list):
            results = [results]
        results.extend(result)
        return results



def inflate(d, sep="_"):
    items = dict()
    for k, v in d.items():
        keys = k.split(sep)
        sub_items = items
        for ki in keys[:-1]:
            try:
                sub_items = sub_items[ki]
            except KeyError:
                sub_items[ki] = dict()
                sub_items = sub_items[ki]
            
        sub_items[keys[-1]] = v

    return items
    
    