'''
Haiku scoring functions.
'''



import haikuhandler
import similarity_checker
import operator
import wordmc

'''
Reads a haiku file and returns scores 
for each haiku based on wordtype structure.
'''
def scoring_test1(haiku_to_evaluate = "generated_100_haiku-goal_oriented.txt"):
    '''
    Read a haiku text file into a dictionary. 
    These are the haiku which will be scored.
    '''
    generated_haiku_dict = haikuhandler.json_from_text(file_name = haiku_to_evaluate)
    '''
    Read another haiku text file into a dictionary. 
    These are the "good" haiku which are used in evaluation.
    Default file is "top18.txt".
    '''
    goal_haiku_dict = haikuhandler.json_from_text()
    
    '''
    Create a pool of all word type substrings in
    haiku the evaluation is based on.
    '''
    goal_wt_ss_pool = {}
    for i in range(0,20):
        goal_wt_ss_pool[i] = []
    for key, goal_haiku in goal_haiku_dict.items():
        goal_haiku_wto = similarity_checker.haiku_to_word_type_order(goal_haiku['genotype_form'])
        goal_haiku_ss_pools = similarity_checker.pool_substrings(goal_haiku_wto)
        for ss_len, ss_list in goal_haiku_ss_pools.items():
            goal_wt_ss_pool[ss_len] = goal_wt_ss_pool[ss_len] + ss_list
    clean_goal_pool = {}
    for gss_len, gss in goal_wt_ss_pool.items():
        clean_goal_pool[gss_len] = list(set(gss))
        
    '''
    Calculate score for each generated haiku.
    '''
    wto_scores = []
    for gkey, generated_haiku in generated_haiku_dict.items():
        #print(generated_haiku)
        wto_score = similarity_checker.score_wto(generated_haiku['genotype_form'], clean_goal_pool)
        wto_scores.append([gkey, wto_score])
        
    '''
    Print top scoring poems.
    '''
    sorted_scores = sorted(wto_scores, key=operator.itemgetter(1), reverse=True)
    for i in range(0,10):
        j = i+1
        good_haiku_key = sorted_scores[i][0]
        good_haiku = generated_haiku_dict[good_haiku_key]['lines']
        print("Number ", j, " haiku is: ")
        print(good_haiku)
    '''
    Also return sorted (haiku index, haiku score) pairs.
    '''
    return sorted_scores

'''
Reads a haiku file and returns scores 
for each haiku based on wordpair occurrences.
'''
def scoring_test2(haiku_to_evaluate = "generated_100_haiku-goal_oriented.txt", corpus = "alice.txt"):
    '''
    Read a haiku text file into a dictionary. 
    These are the haiku which will be scored.
    '''
    generated_haiku_dict = haikuhandler.json_from_text(file_name = haiku_to_evaluate)
    
    '''
    Create 1st order Markov chain from corpus.
    '''
    wmc = wordmc.WordMC(text_file = corpus, highest_order = 2)
    
    markov = wmc.getWord_mc(order = 1)
    #print(markov)
    '''
    Score each poem.
    '''
    scores = []
    
    for key, haiku in generated_haiku_dict.items():
        score = [key, similarity_checker.score_wpo(haiku['genotype_form'], markov1 = markov)]    
        scores.append(score)
    
    '''
    Print top scoring poems.
    '''
    sorted_scores = sorted(scores, key=operator.itemgetter(1), reverse=True)
    for i in range(0,10):
        j = i+1
        good_haiku_key = sorted_scores[i][0]
        good_haiku = generated_haiku_dict[good_haiku_key]['lines']
        print("Number ", j, " haiku is: ")
        print(good_haiku)
     
    '''
    Also return sorted (haiku index, haiku score) pairs.
    '''
    return sorted_scores
    
        
        
        
        
        