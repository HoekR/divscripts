#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 14:41:03 2018

@author: rikhoekstra


from https://gist.github.com/nkt1546789/e9fc84579b9c8356f1e5
"""

def create_cooccurrence_matrix(filename,tokenizer,window_size):
    vocabulary={}
    data=[]
    row=[]
    col=[]
    for sentence in codecs.open(filename,"r","utf-8"):
        sentence=sentence.strip()
        tokens=[token for token in tokenizer(sentence) if token!=u""]
        for pos,token in enumerate(tokens):
            i=vocabulary.setdefault(token,len(vocabulary))
            start=max(0,pos-window_size)
            end=min(len(tokens),pos+window_size+1)
            for pos2 in xrange(start,end):
                if pos2==pos: 
                    continue
                j=vocabulary.setdefault(tokens[pos2],len(vocabulary))
                data.append(1.); row.append(i); col.append(j);
    cooccurrence_matrix=sparse.coo_matrix((data,(row,col)))
    return vocabulary,cooccurrence_matrix