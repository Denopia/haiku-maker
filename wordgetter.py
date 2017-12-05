#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 11:08:30 2017
@author: ittobor

"""
#import worddominator
from worddom import WordDom
import random
import json
import operator
import random

'''
Randomly select key from dict.
'''
def __rndDictVal(dict):
    rndi = random.randint(0,len(dict.keys())-1)
    retval = list(dict.keys())[rndi]
    return retval

'''
Get word_dict and randomly selecting a word from it.
Input parameter word_type and syllable_count can be used to guide to find a
random word. Since it cannot be quaranteed that the a word from given word_type
and/or given syllable_count can be found, the function tries to find shorter
from same word_type. If not found then word_type is chosen new at random.
'''
def getAword(word_dom, word_type=None, syllable_count=None):
    
    wd = word_dom
    word_type_markov = wd.getWordTypesMC()
    word_dict = wd.getWordsDict() #word_dict = worddominator.wordDominator()
#    print(len(word_dict.keys()), type(word_dict.keys()))

    # store original syllable_count to be used if word_type will be changed
    og_sc = syllable_count
    ok_wt = False
    ok_sc = False
    word = None

    # Both 'matches' by word_type and syllable_count has to be found
    # 10 searches for both --> if not found exception raised
    while ok_wt == False or ok_sc == False:    

        # randomly selecting word_type if none is given
        if word_type is None:
            word_type = __rndDictVal(word_dict)
        else:
            word_type = choose_next_word_type(word_type, word_type_markov)
        # search by word_type
        c_wts = 0
        word_type_words = {}
        while ok_wt == False:
            c_wts = c_wts + 1
            if word_type in word_type:
                word_type_words = word_dict[word_type]
                ok_wt = True
            else:
                if c_wts > 10:
                    raise Exception('Cannot find any good word_types')
                word_type = __rndDictVal(word_dict)
        
#        print(word_type, '\n', json.dumps(word_type_words, indent=2))
        
        # return original syllable_count (if word_type was changed)
        syllable_count = og_sc
        
        # randomly selecting syllable_count if none is given
        if syllable_count is None:
            syllable_count = __rndDictVal(word_type_words)
#        print(syllable_count)
    
        # search by syllable_count
        c_scs = 0
        while ok_sc == False:
            c_scs = c_scs + 1
            if syllable_count > 0 and syllable_count in word_type_words:
                rint = random.randint(0,len(word_type_words[syllable_count])-1)
                word = word_type_words[syllable_count][rint]
                ok_sc = True
            else:
                if c_scs > 10:
                    raise Exception('Cannot find any good syllable lengths')
                if syllable_count > 0:
                    syllable_count = syllable_count - 1
                else:
                    ok_wt = False
                    ok_sc = False
                    word_type = None
                    break
#    print(word)
    
    return (word, word_type, syllable_count)


def choose_next_word_type(word_type, word_type_markov):
    possible_word_types = word_type_markov.get(word_type)
    sorted_pwt = sorted(possible_word_types.items(), key=operator.itemgetter(1), reverse=True)
    cdf = []
    cumulative_sum = 0.0
    for c, prob in sorted_pwt:
        cumulative_sum += prob
        cdf.append([c, cumulative_sum])
    cdf[-1][1] = 1.0
    rnd = random.random()
    cp = cdf[0][1]
    i = 0
    while rnd > cp:
        i += 1
        cp = cdf[i][1]
    next_word_type = cdf[i][0]
    
    return next_word_type
'''
Some tests to see what random finds according to syllable length.
And for a some word_type. 
'''
#print("wt, sc, random: ", getAword())
#print("sb=1, wt random: ", getAword(syllable_count=1))
#print("sb=2, wt random: ", getAword(syllable_count=2))
#print("sb=3, wt random: ", getAword(syllable_count=3))
#print("sb=4, wt random: ", getAword(syllable_count=4))
#print("sb=5, wt random: ", getAword(syllable_count=5))
#print("sb=1, wt=VBN: ", getAword(word_type='VBN', syllable_count=1))
#print("sb=2, wt=VBN: ", getAword(word_type='VBN', syllable_count=2))
#print("sb=3, wt=VBN: ", getAword(word_type='VBN', syllable_count=3))