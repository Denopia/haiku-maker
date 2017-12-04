# -*- coding: utf-8 -*-
import json
import math

pos_tag_groups = {'nouns': ['NN','NNS','NNP','NNPS'],
                  'verbs': ['VB','VBD','VBG','VBN','VBP','VBZ','MD'],
                  'adjectives': ['JJ','JJR','JJS']}

"""
Checks how similar haiku's part-of-speech
transitions are to existings 'good' haiku
poems' pos transitions.
"""
def evaluate_pos_transitions(haiku):
    distances = []
    return distances

"""
Calculates the overall part-of-speech difference
compared to existing 'good' haiku poems.
The lower the score, the closer poem's pos composition
is to a known poem's pos composition.
"""
def evaluate_overall_pos_structure(haiku):
    all_tags = count_all_pos_tags(haiku)
    grouped_tags = count_tag_groups(all_tags)
    with open('fhptg.json') as json_data:
        known_pos_groups = json.load(json_data)
    distances = calc_pos_group_distance(grouped_tags, known_pos_groups)
    
    print(distances)
    print(min(distances))
    return distances

"""
Calculates the actual distances between pos group
count vectors.
"""
def calc_pos_group_distance(tags, known_tags):
    distances = []
    newlist = tag_group_counts_as_list(tags)
    oldlists = []
    for key, otags in known_tags.items():
        oldlists.append(tag_group_counts_as_list(otags))
    for oldlist in oldlists:
        dist = 0
        for i in range(0,len(oldlist)):
            dist = dist + (oldlist[i]-newlist[i])**2
        distances.append(math.sqrt(dist))
    return distances

"""
Transforms tag group dictionaries to
vectors of tag group counts.
"""
def tag_group_counts_as_list(tag_groups):
    v = []
    for key, val in tag_groups.items():
        v.append(val)
    total = v[0]
    for i in range(0,len(v)):
        v[i] = v[i]/total
    return v
    
"""
Groups pos tags.
"""
def count_tag_groups(tags):
    groups = {'all':0, 'nouns':0, 'verbs':0, 'adjectives':0, 'others':0}
    for tag, count in tags.items():
        if (tag in pos_tag_groups['nouns']):
            groups['nouns'] = groups['nouns'] + count
        elif (tag in pos_tag_groups['verbs']):
            groups['verbs'] = groups['verbs'] + count
        elif (tag in pos_tag_groups['adjectives']):
            groups['adjectives'] = groups['adjectives'] + count
        else:
            groups['others'] = groups['others'] + count
        groups['all'] = groups['all'] + count
    return groups
   
"""
Counts pos tag occurences in poem.
'haiku' argument must be in the 
form of haiku genotype.
"""
def count_all_pos_tags(haiku):
    pos_tags = {}
    for key, value in haiku.items():
        line = value
        for wts in line:
            if pos_tags.get(wts[1], 0) == 0:
                pos_tags[wts[1]] = 0
            pos_tags[wts[1]] = pos_tags[wts[1]] + 1
    return pos_tags
    