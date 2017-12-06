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

'''
Simply chooses fitting syllable length words for each of the haiku lines.
Uses wordgetter to make the selection randomly.

Returns a dict with three keys, one per line.

Each key contains a list of tuples. A tuple is (word, word_type, syllable_count).

Usage of a haiku_model not implemented yet.
  
'''
def selectWords(wd, mc, haiku_model=None):
#    wd = WordDom('alice.txt')
#    mc = WordTypeMC('top18.txt')
#    print("haiku model used \n", json.dumps(haiku_model, indent=2))

    haiku_genotype = {
            "L1":[],
            "L2":[],
            "L3":[]
            }
    
    '''
    generate line1
    '''
    ok_l1 = False
    sc_l1 = 5
    '''
    previous word types
    '''
    prev_word_type = None
    prev_prev_word_type = None
    while ok_l1 == False:
        word = wordgetter.getAword(prev_word_type = prev_word_type, prev_prev_word_type = prev_prev_word_type, word_dom = wd, word_mc = mc)
        print("L1 ", word)
        
        len_w = word[2]
        
        if len_w <= sc_l1:
           haiku_genotype['L1'].append(word)
           sc_l1 = sc_l1 - len_w
           prev_prev_word_type = prev_word_type
           prev_word_type = word[1]
        
        if sc_l1 == 0:
            ok_l1 = True

    '''
    generate line2
    '''
    ok_l2 = False
    sc_l2 = 7
    while ok_l2 == False:
        word = wordgetter.getAword(prev_word_type = prev_word_type, prev_prev_word_type = prev_prev_word_type, word_dom = wd, word_mc = mc)
        print("L2 ",word)
        
        len_w = word[2]
        
        if len_w <= sc_l2:
           haiku_genotype['L2'].append(word)
           sc_l2 = sc_l2 - len_w
           prev_prev_word_type = prev_word_type
           prev_word_type = word[1]
        
        if sc_l2 == 0:
            ok_l2 = True

    '''
    generate line3
    '''
    ok_l3 = False
    sc_l3 = 5
    while ok_l3 == False:
        word = wordgetter.getAword(prev_word_type = prev_word_type, prev_prev_word_type = prev_prev_word_type, word_dom = wd, word_mc = mc)
        print("L3 ",word)
        
        len_w = word[2]
        
        if len_w <= sc_l3:
           haiku_genotype['L3'].append(word)
           sc_l3 = sc_l3 - len_w
           prev_prev_word_type = prev_word_type
           prev_word_type = word[1]
        
        if sc_l3 == 0:
            ok_l3 = True

    print("haiku genotype \n", json.dumps(haiku_genotype, indent=2))
    
    return haiku_genotype

def generateNHaiku(nb=10):
    wd = WordDom('alice.txt')
    mc = WordTypeMC('top18.txt')
    
    
    with open('generated_haiku_100.txt', 'w') as f:
        for _ in range(nb):
            haiku_genotype = selectWords(wd = wd, mc = mc)
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
generateNHaiku(nb=2)
#selectWords()
#selectWords(haiku_model)