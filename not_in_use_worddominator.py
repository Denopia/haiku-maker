#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 11:14:47 2017

@author: ittobor
"""
import nltk
from nltk.corpus import wordnet
import pronouncing
import json

#('CC','Coordinating conjunction'),
#('CD','Cardinal number'),
#('DT','Determiner'),
#('EX','Existential there'),
#('FW','Foreign word'),
#('IN','Preposition or subordinating conjunction'),
#('JJ','Adjective'),
#('JJR','Adjective, comparative'),
#('JJS','Adjective, superlative'),
#('LS','List item marker'),
#('MD','Modal'),
#('NN','Noun, singular or mass'),
#('NNS','Noun, plural'),
#('NNP','Proper noun, singular'),
#('NNPS','Proper noun, plural'),
#('PDT','Predeterminer'),
#('POS','Possessive ending'),
#('PRP','Personal pronoun'),
#('PRP$','Possessive pronoun'),
#('RB','Adverb'),
#('RBR','Adverb, comparative'),
#('RBS','Adverb, superlative'),
#('RP','Particle'),
#('SYM','Symbol'),
#('TO','to'),
#('UH','Interjection'),
#('VB','Verb, base form'),
#('VBD','Verb, past tense'),
#('VBG','Verb, gerund or present participle'),
#('VBN','Verb, past participle'),
#('VBP','Verb, non-3rd person singular present'),
#('VBZ','Verb, 3rd person singular present'),
#('WDT','Wh-determiner'),
#('WP','Wh-pronoun'),
#('WP$','Possessive wh-pronoun'),
#('WRB','Wh-adver')



tag_list = [
        'CC',
        'CD',
        'DT',
        'EX',
        'FW',
        'IN',
        'JJ',
        'JJR',
        'JJS',
        'LS',
        'MD',
        'NN',
        'NNS',
        'NNP',
        'NNPS',
        'PDT',
        'POS',
        'PRP',
        'PRP$',
        'RB',
        'RBR',
        'RBS',
        'RP',
        'SYM',
        'TO',
        'UH',
        'VB',
        'VBD',
        'VBG',
        'VBN',
        'VBP',
        'VBZ',
        'WDT',
        'WP',
        'WP$',
        'WRB'
        ]

def wordDominator(text_file="alice.txt"):
    text_raw = None
    with open(text_file, 'r', encoding='utf8') as f:
        text_raw = f.read()
    
    tok_text = nltk.word_tokenize(text_raw)
    pos_text = nltk.pos_tag(tok_text)

#    print(len(text_raw))
#    print(len(tok_text))
#    print(len(pos_text))

    words_dict = {}
    for word, tag in pos_text:
        if tag in tag_list:
            if wordnet.synsets(word):
                
                if tag not in words_dict:
                    words_dict[tag] = {}
                
                pro_list = pronouncing.phones_for_word(word)
                if (len(pro_list)>0):
                    sy_count = pronouncing.syllable_count(pro_list[0])
                else:
                    sy_count = 0
                    
                if sy_count not in words_dict[tag]:
                    words_dict[tag][sy_count] = []
                
                if word not in words_dict[tag][sy_count]:
                    words_dict[tag][sy_count].append(word)
    #print(json.dumps(words_dict, indent=2))
    
    return words_dict

#wordDominator()
