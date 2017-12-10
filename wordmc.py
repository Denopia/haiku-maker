#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 11:14:47 2017
@author: ittobor

WordTypeMC is a class that generate and returns given order markov chain (word_types_mc).
During initalization textfile can be given or alice.txt will be looked for.
word_types_mc will be generated from the textfile.

word_types_mc is a markov chain generated from the text based on word_types

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
import json

class WordMC:
    
    def __readTextFile(self, text_file='alice.txt'):
        self.text_raw = None
        with open(text_file, 'r', encoding='utf8') as f:
            self.text_raw = f.read()

    def __init__(self, text_file='alice.txt', highest_order=1):
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
        self.print_on = True

        self.text_raw = None
        self.__readTextFile(text_file)
        
        self.word_mc_dict = {}
        self.word_type_mc_dict = {}

        i = 1
        for _ in range(highest_order):
            self.word_mc_dict[i] = self.__word_markov_chain(order=i)
            self.word_type_mc_dict[i] = self.__word_type_markov_chain(order=i)
            i = i + 1
            
        if self.print_on:
            print(self.word_mc_dict.keys())
            print(self.word_type_mc_dict.keys())
        
    def __initNewTextFile(self, text_file='alice.txt'):    
        # Read text file in
        self.__readTextFile(text_file)
        
    def __word_markov_chain(self, text=None, order=1):
        
        if text is not None:
            self.text_raw = text
        
        # Tokenize the text into sentences.
        sentences = nltk.sent_tokenize(self.text_raw)
    
        # Tokenize each sentence to words. Each item in 'words' is a list with
        # tokenized words from that list.
        tokenized_sentences = []
        for s in sentences:
            w = nltk.word_tokenize(s)
            tokenized_sentences.append(w)
    
        sanitized_sentences = []
        for ts in tokenized_sentences:
#            word_pos_sentence = nltk.pos_tag(ts)
            t_sentence = []
            for word in ts:
                if wordnet.synsets(word):
                    t_sentence.append(word)
            sanitized_sentences.append(t_sentence)
    
        # Now we are ready to create the state transitions. However, this time we
        # count the state transitions from each sentence at a time. And we also take
        # the order into account when coupling the states.
        transitions = {}
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
        word_mc = {}
        for pred, succ_counts in transitions.items():
            word_mc[pred] = {}
            for succ, count in succ_counts.items():
                word_mc[pred][succ] = count / totals[pred]
                
        return word_mc

    def __word_type_markov_chain(self, text=None, order=1):
        
        if text is not None:
            self.text_raw = text
        
        # Tokenize the text into sentences.
        sentences = nltk.sent_tokenize(self.text_raw)
    
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
        word_types_mc = {}
        for pred, succ_counts in transitions.items():
            word_types_mc[pred] = {}
            for succ, count in succ_counts.items():
                word_types_mc[pred][succ] = count / totals[pred]
                
        return word_types_mc
    
    def getWord_mc(self, order=1):
        return self.word_mc_dict[order]

    def getWord_type_mc(self, order=1):
        return self.word_type_mc_dict[order]