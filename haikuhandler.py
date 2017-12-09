# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 23:37:29 2017

@author: mlein
"""

import json
import nltk
import pronouncing
from nltk.corpus import wordnet
#import pos_evaluator

"""
Creates a dictionary of haiku poems from text file.
Haiku keys are just numbered indexes.
Each haiku is also a dictionary with fields:
    - lines
    - tokenized_lines
    - pos_tags
    - syllable_counts
    - genotype_form


Argument 'file_name' is the name of the 
txt file with existing haiku poems.

Argument 'output_file_name' is the name
of the output json file.

Argument 'write' determines if a json file is written.

Each line of txt file must have exactly one
line of haiku. There must also be an empty 
line between the last line of a haiku and 
the first line of another haiku.

example usage: json_from_text("famous_haiku_poems.txt", True, "fhpj.json")
"""

def json_from_text(file_name = "top18.txt", write = False, output_file_name = 'haiku_test.json'):
    f = open(file_name, "r", encoding="utf-8")
    haiku_poems = f.read()
    f.close()
    
    haiku_poems = haiku_poems.lower()
    haiku_poems = haiku_poems.replace("’","'")
    haiku_poems = haiku_poems.replace("-"," ")
    haiku_poems = haiku_poems.replace(","," ")
    haiku_poems = haiku_poems.replace("!"," ")
    haiku_poems = haiku_poems.replace("?"," ")
    haiku_poems = haiku_poems.replace("."," ")
    haiku_poems = haiku_poems.replace(":"," ")
    haiku_poems = haiku_poems.rstrip()
    
    haiku_list = haiku_poems.split("\n\n")
    
    hd = {}
    hid = 0
    
    for haiku in haiku_list:
        #haiku = haiku.rstrip()
        poem = {}
        tokenized_lines = []
        pos_tags = []
        syllable_counts = []
        
        lines = haiku.split("\n")
        for line in lines:
            just_tags = []
            syllable_count = []
            just_words = []
            tokenized_line = nltk.word_tokenize(line)
            words_and_tags = nltk.pos_tag(tokenized_line)
            for word, tag in words_and_tags:
                if wordnet.synsets(word):
                    pro_list = pronouncing.phones_for_word(word)
                    if (len(pro_list) > 0 and word != "'s"):
                        syllable_count.append(pronouncing.syllable_count(pro_list[0]))
                    elif (word == "'s"):
                        #special case, adding "'s" to a word doesn't increase syllable count
                        syllable_count.append(0)
                    else:
                        #if syllables can't be counted, indicate error as -999
                        syllable_count.append(-999)
                    just_tags.append(tag)
                    just_words.append(word)
            pos_tags.append(just_tags)
            syllable_counts.append(syllable_count)
            tokenized_lines.append(just_words)
            
        poem["lines"] = lines
        poem["tokenized_lines"] = tokenized_lines
        poem["pos_tags"] = pos_tags
        poem["syllable_counts"] = syllable_counts
        poem["genotype_form"] = {}
        
        
        l1 = []
        for ind in range(0, len(poem["tokenized_lines"][0])):
            word_tuple = (poem["tokenized_lines"][0][ind],
                          poem["pos_tags"][0][ind],
                          poem["syllable_counts"][0][ind])
            l1.append(word_tuple)
        poem["genotype_form"]["L1"] = l1
        
        l2 = []
        for ind in range(0, len(poem["tokenized_lines"][1])):
            word_tuple = (poem["tokenized_lines"][1][ind],
                          poem["pos_tags"][1][ind],
                          poem["syllable_counts"][1][ind])
            l2.append(word_tuple)
        poem["genotype_form"]["L2"] = l2
        
        l3 = []
        for ind in range(0, len(poem["tokenized_lines"][2])):
            word_tuple = (poem["tokenized_lines"][2][ind],
                          poem["pos_tags"][2][ind],
                          poem["syllable_counts"][2][ind])
            l3.append(word_tuple)
        poem["genotype_form"]["L3"] = l3
        
        hd[hid] = poem
        hid = hid + 1
      
    if(write):
        with open(output_file_name, 'w') as outfile:  
            json.dump(hd, outfile, indent=4)
    return hd
