#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 11:14:47 2017
@author: ittobor

WordDom is a class that holds the words_dict and the word_types_mc (word type based markov chain).
During initalization textfile can be given or alice.txt will be looked for.
words_dict and word_types_mc will be generated from the textfile.

words_dict is a python dictionary for grouped words from the text:
at first level grouped by word_type and on seconde level grouped by syllable lenghts.

word_type
    - 0
    - 1
        - word
        - word
    - 2
        - word
        - word
    .
    .
    .

word_types_mc is a markov chain generated from the text based on word_types

NOT TESTED: New text files can be added to extend words_dict and word_types_mc 

('CC','Coordinating conjunction'),
('CD','Cardinal number'),
('DT','Determiner'),
('EX','Existential there'),
('FW','Foreign word'),
('IN','Preposition or subordinating conjunction'),
('JJ','Adjective'),
('JJR','Adjective, comparative'),
('JJS','Adjective, superlative'),
('LS','List item marker'),
('MD','Modal'),
('NN','Noun, singular or mass'),
('NNS','Noun, plural'),
('NNP','Proper noun, singular'),
('NNPS','Proper noun, plural'),
('PDT','Predeterminer'),
('POS','Possessive ending'),
('PRP','Personal pronoun'),
('PRP$','Possessive pronoun'),
('RB','Adverb'),
('RBR','Adverb, comparative'),
('RBS','Adverb, superlative'),
('RP','Particle'),
('SYM','Symbol'),
('TO','to'),
('UH','Interjection'),
('VB','Verb, base form'),
('VBD','Verb, past tense'),
('VBG','Verb, gerund or present participle'),
('VBN','Verb, past participle'),
('VBP','Verb, non-3rd person singular present'),
('VBZ','Verb, 3rd person singular present'),
('WDT','Wh-determiner'),
('WP','Wh-pronoun'),
('WP$','Possessive wh-pronoun'),
('WRB','Wh-adver')
"""
import nltk
from nltk.corpus import wordnet
import pronouncing
import json

class WordDom:
    
    def __readTextFile(self, text_file='alice.txt'):
        self.text_raw = None
        self.tok_text = None
        self.pos_text = None
        with open(text_file, 'r', encoding='utf8') as f:
            self.text_raw = f.read()

    def __init__(self, text_file='alice.txt'):
        print('__init__')
        self.tag_list = [
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
        self.text_raw = None
        self.tok_text = None
        self.pos_text = None
        self.words_dict = {}

        self.__readTextFile(text_file)
        self.__addTo()
            
    def __addTo(self):
        self.tok_text = nltk.word_tokenize(self.text_raw)
        self.pos_text = nltk.pos_tag(self.tok_text)
    
        for word, tag in self.pos_text:
            if tag in self.tag_list:
                if wordnet.synsets(word):
                    
                    if tag not in self.words_dict:
                        self.words_dict[tag] = {}
                    
                    word = word.lower()
                    
                    pro_list = pronouncing.phones_for_word(word)
                    if (len(pro_list)>0):
                        sy_count = pronouncing.syllable_count(pro_list[0])
                    else:
                        sy_count = 0
                        
                    if sy_count not in self.words_dict[tag]:
                        self.words_dict[tag][sy_count] = []
                    
                    if word not in self.words_dict[tag][sy_count]:
                        self.words_dict[tag][sy_count].append(word)
                                

    def addText(self, text_file="alice.txt"):
        if text_file:
            self.__readTextFile(text_file)
        self.__addTo()

    def printWordsDict(self):
        print("words_dict\n",json.dumps(self.words_dict, indent=2))

    def printSelected(self, word_type=None, syllable_count=None, word=None):
        keylist = list(self.words_dict.keys())
        result = {}
        for k in keylist:
            toadd_k = True
            if k is not word_type:
                if word_type is not None:
                    toadd_k = False
            
            if toadd_k == True:
                sl_list = self.words_dict[k]
                for sl in list(sl_list.keys()):
                    toadd_sl = True
                    if sl is not syllable_count:
                        if syllable_count is not None:
                            toadd_sl = False
                    
                    if toadd_sl == True:
                        if word is not None:
                            if word in sl_list[sl]:
                                if k not in result:
                                    result[k] = {}
                                result[k][sl] = list().append(word)
                        else:
                            if k not in result:
                                result[k] = {}
                            result[k][sl] = sl_list[sl]
        print("print select\n",json.dumps(result, indent=2))
    
    def clearWordsDict(self):
        self.words_dict = {}

    def getWordsDict(self):
        return self.words_dict
    
    def getWordTypesList(self):
        return self.tag_list