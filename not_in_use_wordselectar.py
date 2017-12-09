#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 14:55:36 2017

@author: ittobor
"""

from worddom import WordDom
from wordmc import WordTypeMC
import wordgetter
import json

'''
Idea of how 'model' from estimator(?) could direct the search for convenient
structure.
'''
haiku_model = {
            "L1":[('VBN',2), ('VBN',3)],
            "L2":[('VBN',2), ('VBN',3), ('VBN',3)],
            "L3":[('VBN',2), ('VBN',3)]
        }



def createLine(syllable_count, word_dom, word_mc=None, prev_word_type=None, prev_prev_word_type=None):
    print("-- CREATE LINE --")
    line_ok = False
    ret_line = []
    sc = syllable_count
    ic = 0
    while line_ok == False:

        ic = ic + 1

        if ic > 25:
            word = wordgetter.getAword(word_dom = word_dom, word_mc = word_mc, syllable_count=sc)
        else:
            word = wordgetter.getAword(word_dom = word_dom, word_mc = word_mc, prev_word_type = prev_word_type, prev_prev_word_type = prev_prev_word_type)
        print(word)
        
        len_w = word[2]
        
        if len_w <= sc:
           ret_line.append(word)
           sc = sc - len_w
           if word_mc is not None:
               prev_prev_word_type = prev_word_type
               prev_word_type = word[1]
        
        if sc == 0:
            line_ok = True

    return ret_line

'''
Simply chooses fitting syllable length words for each of the haiku lines.
Uses wordgetter to make the selection randomly.

Returns a dict with three keys, one per line.

Each key contains a list of tuples. A tuple is (word, word_type, syllable_count).

Usage of a haiku_model not implemented yet.
  
'''
def selectWords(word_dom, word_mc, haiku_model=None):
#    wd = WordDom('alice.txt')
#    mc = WordTypeMC('top18.txt')
#    print("haiku model used \n", json.dumps(haiku_model, indent=2))

    line1 = 'L1'
    line2 = 'L2'
    line3 = 'L3'
    
    haiku_genotype = {
            line1:[],
            line2:[],
            line3:[]
            }

    '''
    generate line1
    '''
    line = createLine(syllable_count = 5, word_dom = word_dom, word_mc = word_mc)
    haiku_genotype[line1] = line
    

    '''
    generate line2
    '''
    line = createLine(syllable_count = 7, word_dom = word_dom, word_mc = word_mc)
    haiku_genotype[line2] = line


    '''
    generate line3
    '''
    line = createLine(syllable_count = 5, word_dom = word_dom, word_mc = word_mc)
    haiku_genotype[line3] = line


    print("haiku genotype \n", json.dumps(haiku_genotype, indent=2))
    
    return haiku_genotype

def generateNHaiku(nb=10):
    wd = WordDom('alice.txt')
#   mc = WordTypeMC('top18.txt')
    mc = None
    
    with open('generated_n_haiku.txt', 'w') as f:
        for _ in range(nb):
            haiku_genotype = selectWords(word_dom = wd, word_mc = mc)
            print("haiku genotype \n", json.dumps(haiku_genotype, indent=2))
            L1 = []
            for word, word_type, syllable_count in haiku_genotype['L1']:
                L1.append(word)
            L2 = []
            for word, word_type, syllable_count in haiku_genotype['L2']:
                L2.append(word)
            L3 = []
            for word, word_type, syllable_count in haiku_genotype['L3']:
                L3.append(word)
            haiku = " ".join(L1) + "\n" + " ".join(L2) + "\n" + " ".join(L3) + "\n\n"
            f.write(haiku)

'''
Some test to see how it works
'''
generateNHaiku(nb=100)
#selectWords()
#selectWords(haiku_model)
