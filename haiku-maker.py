#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 14:55:36 2017

@author: ittobor
"""

from worddom import WordDom
from wordmc import WordMC
import scoring_tests
import json, random, operator

line1 = 'L1'
line2 = 'L2'
line3 = 'L3'

print_on = False


'''
Idea of how 'model' from estimator(?) could direct the search for convenient
structure.
NOT-IN-USE
'''
haiku_model = {
            "L1":[('VBN',2), ('VBN',3)],
            "L2":[('VBN',2), ('VBN',3), ('VBN',3)],
            "L3":[('VBN',2), ('VBN',3)]
        }



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
def getAword(word_dom, word_mc=None, prev_word_type=None, prev_prev_word_type=None, syllable_count=None):
    
    word_dict = word_dom.getWordsDict()
    if word_mc is not None:
        word_type_markov1 = word_mc.getWord_type_mc(order=1)
        word_type_markov2 = word_mc.getWord_type_mc(order=2)
    
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
        if prev_word_type is None:
            word_type = __rndDictVal(word_dict)
        else:
            word_type = choose_next_word_type(prev_word_type, prev_prev_word_type, word_type_markov1, word_type_markov2)
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

def choose_next_word_type(prev_word_type, prev_prev_word_type, word_type_markov1, word_type_markov2):
    if prev_prev_word_type is None:
        #Sprint("2nd is None")
        possible_word_types = word_type_markov1.get(prev_word_type, None)
        if possible_word_types is None:
            #print("No 1st order types")
            return 'NN'
    else:
        key = prev_prev_word_type + " " + prev_word_type
        possible_word_types = word_type_markov2.get(key, None)
        if possible_word_types is None:
            #print("No 2nd order types")
            possible_word_types = word_type_markov1.get(prev_word_type, None)
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
    
    return next_word_type.split(" ")[-1]

def createLine(syllable_count, word_dom, word_mc=None, prev_word_type=None, prev_prev_word_type=None):
    if print_on:
        print("-- CREATE LINE --")
    line_ok = False
    ret_line = []
    sc = syllable_count
    ic = 0
    while line_ok == False:

        ic = ic + 1

        if ic > 25:
            word = getAword(word_dom = word_dom, word_mc = word_mc, syllable_count=sc)
        else:
            word = getAword(word_dom = word_dom, word_mc = word_mc, prev_word_type = prev_word_type, prev_prev_word_type = prev_prev_word_type)

        if print_on:
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
def generateHaiku(word_dom, word_mc=None, haiku_model=None):
    
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

    if print_on:
        print("haiku genotype \n", json.dumps(haiku_genotype, indent=2))
    
    return haiku_genotype

def writeHaikuListToFile(haiku_list, out_filename='generated_n_haiku.txt'):
        with open(out_filename, 'w') as f:
            for i in range(len(haiku_list)):

                haiku_genotype = haiku_list[i]

                L1 = []
                for word, word_type, syllable_count in haiku_genotype[line1]:
                    L1.append(word)
                L2 = []
                for word, word_type, syllable_count in haiku_genotype[line2]:
                    L2.append(word)
                L3 = []
                for word, word_type, syllable_count in haiku_genotype[line3]:
                    L3.append(word)
                    haiku = " ".join(L1) + "\n" + " ".join(L2) + "\n" + " ".join(L3) + "\n\n"

                f.write(haiku)

def writeScoreListToFile(scores, topN=1, out_filename='scores_n_haiku.txt'):
        with open(out_filename, 'w') as f:
            for i in range(topN):
                score = str(scores[i][0]) + ' ' + str(scores[i][1]) + '\n'
                f.write(score)

def generateMultipleHaiku(word_dom, word_mc=None, nb_haiku=10): 
    haiku_list = [] 
    for _ in range(nb_haiku):
        haiku_genotype = generateHaiku(word_dom = word_dom, word_mc = word_mc)
        haiku_list.append(haiku_genotype)
    
    return haiku_list

def pickTopNHaiku(haiku_list, scores, topN=1):
    top_haiku_list = []
    top_scores = scores[0:topN]
    for score in top_scores:
        top_haiku_list.append(haiku_list[score[0]])
    return top_haiku_list
    
def main():
    nb_haiku = 10000
    nb_learnings = 10
    nb_topN = int(nb_haiku*0.10)
    
    '''
    First 100 batch randomly and score
    '''
    in_filename = 'nat_coo_sma.txt'
    
    out_filename_1_prefix = in_filename.split('.')[0] + '_generated_' + str(nb_haiku)
    out_filename_2_prefix = in_filename.split('.')[0] + '_top_' + str(nb_topN) + '_haiku_of_' + str(nb_haiku)
    out_filename_3_prefix = in_filename.split('.')[0] + '_top_' + str(nb_topN) + '_scores_of_'  + str(nb_haiku)
    
    word_dom = WordDom(in_filename)
    
    word_mc = None

    haiku_list = []
    haiku_list = generateMultipleHaiku(word_dom=word_dom, word_mc=word_mc, nb_haiku=nb_haiku)
    
    out_filename = out_filename_1_prefix + '.txt'
    writeHaikuListToFile(haiku_list, out_filename)
    
    scores = scoring_tests.scoring_test1(haiku_to_evaluate=out_filename)
    if print_on:
        print("-- GOT SCORES (total: " + str(len(scores)) + ')')
        print(scores[0:10])
    out_filename_3 = out_filename_3_prefix + '.txt'
    writeScoreListToFile(scores, nb_topN, out_filename_3)
    
    top_haiku_list = pickTopNHaiku(haiku_list, scores, topN=nb_topN)

    if print_on:
        print("top haiku genotypes \n", json.dumps(top_haiku_list, indent=2))
    
    out_filename_2 = out_filename_2_prefix + '.txt'
    writeHaikuListToFile(top_haiku_list, out_filename_2)

    '''
    Generate 100 batch N times, and learn based on previous score
    '''    
    if nb_learnings > 0:
        for i in range(nb_learnings):
            word_mc = WordMC(out_filename_2, highest_order=2)
            #print(word_dom.getWordsDict().keys())
            haiku_list = generateMultipleHaiku(word_dom=word_dom, word_mc=word_mc, nb_haiku=nb_haiku)
    
            out_filename = out_filename_1_prefix + '_' + str(int(i+1)) + '.txt'
            writeHaikuListToFile(haiku_list, out_filename)
    
            scores = scoring_tests.scoring_test1(haiku_to_evaluate=out_filename)
            if print_on:
                print("-- GOT SCORES (total: " + str(len(scores)) + ')')
                print(scores[0:10])
                
            out_filename_3 = out_filename_3_prefix + '_' + str(int(i+1)) + '.txt'
            writeScoreListToFile(scores, nb_topN, out_filename_3)
    
            top_haiku_list = pickTopNHaiku(haiku_list, scores, topN=nb_topN)

            if print_on:
                print("top haiku genotypes \n", json.dumps(top_haiku_list, indent=2))
    
            out_filename_2 = out_filename_2_prefix + '_' + str(int(i+1)) + '.txt'
            writeHaikuListToFile(top_haiku_list, out_filename_2)

#    '''
#    Second 100 batch guided by word_type markov_chains created from topN from first round
#    '''
#    word_mc = WordMC(out_filename_2, highest_order=2)
#    
#    haiku_list = generateMultipleHaiku(word_dom=word_dom, word_mc=word_mc, nb_haiku=nb_haiku)
#    
#    out_filename='generated_n_haiku_2.txt'
#    writeHaikuListToFile(haiku_list, out_filename)
#    
#    scores = scoring_tests.scoring_test1(haiku_to_evaluate=out_filename)
#    print("-- GOT SCORES: ", len(scores))
#    print(scores[0:10])
#    
#    top_haiku_list = pickTopNHaiku(haiku_list, scores, topN=0.25)
#
#    if print_on:
#        print("top haiku genotypes \n", json.dumps(top_haiku_list, indent=2))
#    
#    out_filename_2 ='top_n_generated_haiku_2.txt'
#    writeHaikuListToFile(top_haiku_list, out_filename_2)
#
#    '''
#    Third 100 batch guided by word_type markov_chains created from topN from second round
#    '''
#    word_mc = WordMC(out_filename_2, highest_order=2)
#    
#    haiku_list = generateMultipleHaiku(word_dom=word_dom, word_mc=word_mc, nb_haiku=nb_haiku)
#    
#    out_filename='generated_n_haiku_3.txt'
#    writeHaikuListToFile(haiku_list, out_filename)
#    
#    scores = scoring_tests.scoring_test1(haiku_to_evaluate=out_filename)
#    print("-- GOT SCORES: ", len(scores))
#    print(scores[0:10])
#    
#    top_haiku_list = pickTopNHaiku(haiku_list, scores, topN=0.25)
#
#    if print_on:
#        print("top haiku genotypes \n", json.dumps(top_haiku_list, indent=2))
#    
#    out_filename_2 ='top_n_generated_haiku_3.txt'
#    writeHaikuListToFile(top_haiku_list, out_filename_2)
#
#    '''
#    Fourth 100 batch guided by word_type markov_chains created from topN from second round
#    '''
#    word_mc = WordMC(out_filename_2, highest_order=2)
#    
#    haiku_list = generateMultipleHaiku(word_dom=word_dom, word_mc=word_mc, nb_haiku=nb_haiku)
#    
#    out_filename='generated_n_haiku_4.txt'
#    writeHaikuListToFile(haiku_list, out_filename)
#    
#    scores = scoring_tests.scoring_test1(haiku_to_evaluate=out_filename)
#    print("-- GOT SCORES: ", len(scores))
#    print(scores[0:10])
#    
#    top_haiku_list = pickTopNHaiku(haiku_list, scores, topN=0.25)
#
#    if print_on:
#        print("top haiku genotypes \n", json.dumps(top_haiku_list, indent=2))
#    
#    out_filename_2 ='top_n_generated_haiku_4.txt'
#    writeHaikuListToFile(top_haiku_list, out_filename_2)
#    
#    '''
#    Fifth 100 batch guided by word_type markov_chains created from topN from second round
#    '''
#    word_mc = WordMC(out_filename_2, highest_order=2)
#    
#    haiku_list = generateMultipleHaiku(word_dom=word_dom, word_mc=word_mc, nb_haiku=nb_haiku)
#    
#    out_filename='generated_n_haiku_5.txt'
#    writeHaikuListToFile(haiku_list, out_filename)
#    
#    scores = scoring_tests.scoring_test1(haiku_to_evaluate=out_filename)
#    print("-- GOT SCORES: ", len(scores))
#    print(scores[0:10])
#    
#    top_haiku_list = pickTopNHaiku(haiku_list, scores, topN=0.25)
#
#    if print_on:
#        print("top haiku genotypes \n", json.dumps(top_haiku_list, indent=2))
#    
#    out_filename_2 ='top_n_generated_haiku_5.txt'
#    writeHaikuListToFile(top_haiku_list, out_filename_2)

main()