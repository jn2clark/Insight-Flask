# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 11:03:50 2015

@author: jesseclark

A couple of functions for use with the app

"""

import cPickle 
from random import shuffle
import gensim
from random import randint

def get_htags_tweets(model,hashtable,sterm):
    # query the model
    modelout = model.most_similar(sterm,topn=1000)
    # get words, htags and cosine sim
    words,htags,csim = get_words_hashtags(modelout,nreturn=10)
    # generate search urls  
    the_urls = hashtag_url_gen(htags)
    
    # get the tweets - debugging here
    print(sterm)
    print(htags)
    # get a random tweet to display from those available
    tweets = [hashtable[key][randint(0,len(hashtable[key])-1)][0] for key in htags]
    
    print(tweets)
    
    # no make a dict to hold the htags, urls's etc
    val = 0
    htag_tweets = []
    for result,url,word,tweet in zip(htags,the_urls,words,tweets):
        val+=1
        htag_tweets.append(dict(name=result, web=url,name2 = word,tweets=tweet,orig=sterm,rank=val))
    
    return htag_tweets

def get_suggestions():
    # put the suggested searches here    
    return ['#food','baseball','#travel','cats',"New York",'#dogs',
            'bikes','#datascience','art','San Francisco','#coffee','climate change','#running']

def load_model(fname):
    print(fname)
    print("\n Loading model and hashtable (make sure they match!)...")
    # name of the model to use

    # this one is pretty good
    modelname = 'USmodel-n500-mc15-w10-i10-d5Rand-mem'
                
    hashtablename = fname+'USAhtable-short-d5.pkl'#'USAhtable-short.pkl'

    #modelname = 'USmodel-n500-mc50-w10-i10-ng5-d10Rand-mem'
    #modelname = 'USmodel-n500-mc15-w10-i10-ng5-d10Rand-mem'
    #hashtablename = fname+'USAhtable-short-d10.pkl'#'USAhtable-short.pkl'
    
    #modelname = 'USmodel-n500-mc15-w10-i10-ng5-d10Rand-mem'

    
    # this looks pretty god too
    #modelname = 'USmodel-n500-mc15-w10-i10-ng5-d10Rand-mem'

    model = gensim.models.Word2Vec.load(fname+modelname)
    # save memory
    model.init_sims(replace=True)
    
   
    hashtable = load_object(hashtablename)
    print("\n Finished...")
    return model,hashtable
    
def get_words_hashtags(modelout,nreturn=100):
    # get the words and hastags from the word2vec output
    words = [word[0] for word in modelout if '#' not in word[0]]
    hashtags = [word[0] for word in modelout if '#' in word[0]]
    numbers = [word[1] for word in modelout]
    return words[:nreturn],hashtags[:nreturn],numbers[:nreturn]
    
def hashtag_url_gen(hashtags):
    # generate a search url for twitter based on the returned hashtags
    base_url = 'https://twitter.com/search?q=%23'#'https://twitter.com/hashtag/'
    not_base ='&src=typd'
    urls = [base_url+hashtag[1:]+not_base for hashtag in hashtags]
    return urls


def load_object(fname):
    # load a pickled object
    # load it again
    with open(fname, 'rb') as fid:
        clf = cPickle.load(fid)    
    return clf