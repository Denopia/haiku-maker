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
    
    def __readTextFile(self, text_file='alice.txt', text_file2 = "alice.txt"):
        self.text_raw = None
        self.tok_text = None
        self.pos_text = None
        with open(text_file, 'r', encoding='utf8') as f:
            self.text_raw = f.read()
        with open(text_file2, 'r', encoding='utf8') as f:
            self.text_raw_mc = f.read()

    def __init__(self, text_file='top18.txt', text_file2='top18.txt'):
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
        self.text_raw_mc = None
        self.tok_text = None
        self.pos_text = None
        self.words_dict = {}
        self.word_types_mc = {}
        self.word_types_mc2 = {}

        self.__readTextFile(text_file, text_file2)
        self.__addTo()
            
    def __addTo(self):
        self.tok_text = nltk.word_tokenize(self.text_raw)
        self.pos_text = nltk.pos_tag(self.tok_text)
    
        for word, tag in self.pos_text:
            if tag in self.tag_list:
                if wordnet.synsets(word):
                    
                    if tag not in self.words_dict:
                        self.words_dict[tag] = {}
                    
                    pro_list = pronouncing.phones_for_word(word)
                    if (len(pro_list)>0):
                        sy_count = pronouncing.syllable_count(pro_list[0])
                    else:
                        sy_count = 0
                        
                    if sy_count not in self.words_dict[tag]:
                        self.words_dict[tag][sy_count] = []
                    
                    if word not in self.words_dict[tag][sy_count]:
                        self.words_dict[tag][sy_count].append(word)

        # Tokenize the text into sentences.
        sentences = nltk.sent_tokenize(self.text_raw_mc)

        # Tokenize each sentence to words. Each item in 'words' is a list with
        # tokenized words from that list.
        tokenized_sentences = []
        for s in sentences:
            w = nltk.word_tokenize(s)
            tokenized_sentences.append(w)

        sanitized_sentences = []
        for ts in tokenized_sentences:
            word_pos_sentence = nltk.pos_tag(ts)
            pos_sentence = []
            #print(word_pos_sentence)
            for word, tag in word_pos_sentence:
                if tag in self.tag_list:
                    if wordnet.synsets(word):
                        pos_sentence.append(tag)
            sanitized_sentences.append(pos_sentence)

        # Now we are ready to create the state transitions. However, this time we
        # count the state transitions from each sentence at a time. And we also take
        # the order into account when coupling the states.
        transitions = {}
        order = 1
        for data in sanitized_sentences:
            for i in range(len(data)-order):
                pred = ' '.join(data[i:i+order])
                succ = ' '.join(data[i+1:i+1+order])         
                if pred not in transitions:
                    # Predecessor key is not yet in the outer dictionary, so we create
                    # a new dictionary for it.
                    transitions[pred] = {}
            
                if succ not in transitions[pred]:
                    # Successor key is not yet in the inner dictionary, so we start
                    # counting from one.
                    transitions[pred][succ] = 1.0
                else:
                    # Otherwise we just add one to the existing value.
                    transitions[pred][succ] += 1.0

        # Compute total number of successors for each state
        totals = {}
        for pred, succ_counts in transitions.items():
            totals[pred] = sum(succ_counts.values())

        # Compute the probability for each successor given the predecessor.
        #probs = {}
        for pred, succ_counts in transitions.items():
            self.word_types_mc[pred] = {}
            for succ, count in succ_counts.items():
                self.word_types_mc[pred][succ] = count / totals[pred]
                
        # Quick and ugly copy-paste for 2nd order markov
        transitions2 = {}
        order2 = 2
        for data2 in sanitized_sentences:
            for i in range(len(data2)-order2):
                pred2 = ' '.join(data2[i:i+order2])
                succ2 = ' '.join(data2[i+1:i+1+order2])         
                if pred2 not in transitions2:
                    # Predecessor key is not yet in the outer dictionary, so we create
                    # a new dictionary for it.
                    transitions2[pred2] = {}
            
                if succ2 not in transitions2[pred2]:
                    # Successor key is not yet in the inner dictionary, so we start
                    # counting from one.
                    transitions2[pred2][succ2] = 1.0
                else:
                    # Otherwise we just add one to the existing value.
                    transitions2[pred2][succ2] += 1.0

        # Compute total number of successors for each state
        totals2 = {}
        for pred2, succ_counts2 in transitions2.items():
            totals2[pred2] = sum(succ_counts2.values())

        # Compute the probability for each successor given the predecessor.
        #probs = {}
        for pred2, succ_counts2 in transitions2.items():
            self.word_types_mc2[pred2] = {}
            for succ2, count2 in succ_counts2.items():
                self.word_types_mc2[pred2][succ2] = count2 / totals2[pred2]
                
                

    def addText(self, text_file="alice.txt"):
        if text_file:
            self.__readTextFile(text_file)
        self.__addTo()

    def printWordsDict(self):
        print("words_dict\n",json.dumps(self.words_dict, indent=2))

    def printWordTypesMC(self):
        print("word_types_mc\n",json.dumps(self.word_types_mc, indent=2))
    
    def clearWordsDict(self):
        self.words_dict = {}
        
    def clearWordTypesMC(self):
        self.word_types_mc = {}
    
    def getWordsDict(self):
        return self.words_dict
    
    def getWordTypes1stMC(self):
        return self.word_types_mc
    
    def getWordTypes2ndMC(self):
        return self.word_types_mc2
    
    def getWordTypesList(self):
        return self.tag_list
