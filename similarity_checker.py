# -*- coding: utf-8 -*-

import haikuhandler as hh
from operator import itemgetter

'''
Gives score to a single haiku.
Argument haikugt must be genotype haiku.
Returns a dictionary of scores.
Gives score in all possible categories.

Keys:   - wto (word type order score)
        - wp  (word pair score)
        - ...
'''
def score_single_haiku(haikugt):
    
    score = {}
    score['wto'] = score_wto(haikugt)
    '''
    other scoring function calls
    '''

'''
Scores wordt type order based on
good word type orders.
Argument 'haiku' is a genotype haiku.
Argument 'goal_ss_pool_dict' is a
dictionary of all wordtype substrings
of good poems. Dictionary key is the
length of the substrings and value is
a list containing all different substrings
of that length which appear in good poems.
Returns a score between 0 and 1, 0 being
the worst and 1 the best possible score.
'''
def score_wto(haiku, goal_ss_pool_dict):
    haiku_wto = haiku_to_word_type_order(haiku)
    haiku_ss_pool_dict = pool_substrings(haiku_wto)
    for key, ss_list in sorted(haiku_ss_pool_dict.items(), reverse = True):
        for gss in goal_ss_pool_dict[key]:
            for ss in ss_list:
                if ss == gss:
                    return key/len(haiku_wto)
    return 0.0
    
'''
Creates a list containing all wordtypes
in a haiku in order.

Argument 'haiku' is a genotype haiku
'''  
def haiku_to_word_type_order(haiku):
    wto = []
    for word_tuple in haiku['L1']:
        wto.append(word_tuple[1])
    for word_tuple in haiku['L2']:
        wto.append(word_tuple[1])
    for word_tuple in haiku['L2']:
        wto.append(word_tuple[1])
    return wto

'''
Creates a dictionary of all wordtype
substrings in a haiku.
Argument 'haiku_wto' is a list of
wordtypes appearing in the haiku in order.
'''
def pool_substrings(haiku_wto):
    ss_pool = {}
    for i in range(0,20):
        ss_pool[i] = []
    for a in range(0, len(haiku_wto)):
        for b in range(a, len(haiku_wto)):
            key = b-a+1
            ss = substring_from_list(a, b, haiku_wto)
            ss_pool[key].append(ss)
            
    return ss_pool
            
'''
Simple function. Just builds a string
from index a to b using wordtypes in
list 'haiku_wto'.
'''
def substring_from_list(a, b, haiku_wto):
    ss = ""
    for i in range(a,b+1):
        ss = ss + haiku_wto[i] + " "
    ss = ss[0:-1]
    return ss
