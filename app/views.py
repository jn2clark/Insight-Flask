from flask import render_template, request
from app import app
import gensim
from AppFunctions import (get_words_hashtags,hashtag_url_gen,
                          load_object,load_model, get_suggestions,get_htags_tweets)
import os
from random import randint

# setup the global path to the model
dirc = os.path.dirname(__file__)
fname = os.path.join(dirc, 'data/')
# load the model and htbale
model,hashtable = load_model(fname)
# get the suggestion to use when no search is entered
rand_suggestions = get_suggestions()


@app.route('/')
def index():
    user = '' # fake user
    return render_template("index.html",title = 'Home',user = user)

@app.route('/output')
def results_output():
  
    # pull 'ID' from input field and store it
    sterm = request.args.get('ID')
    orig_sterm = sterm.replace(' ','+')
    print(sterm)

    # strip any excess whitespace and make lower case for the model
    sterm = sterm.lower().strip()    
    # empty results list/dict
    results = []

    # check to see if field is not empty
    if len(sterm) > 0:  
      
        # if more than 1 word, split it so the model can take it
        sterm = sterm.split(" ")
     
        # use a try here because if it is not in the model vocab it will error      
        try:         
            # how should the link open
            results = get_htags_tweets(model,hashtable,sterm)
            # what to do with opening a nw tab/window for the html
            new_tab = '"_blank"'
        except:
            # help the user if the field was empty
            suggestion = rand_suggestions[randint(0,len(rand_suggestions)-1)]
            # throw back an error to help the user
            the_result = 'You are too original! This has not been mentioned on twitter. Try another term like '+suggestion 
  
            # take care of the # in the string
            if suggestion[0] == '#':
                suggestion = '%23'+suggestion[1:]
            # take care of whitespace
            suggestion = suggestion.replace(' ','+')  
            results.append(dict(name=the_result, web='output?ID='+suggestion,name2 = ' ',tweets = ' ',orig = ' '))
            new_tab = '"_self"'
  
    else:
        # help the user if the field was empty
        suggestion = rand_suggestions[randint(0,len(rand_suggestions)-1)]
        the_result = "Looks like you didn't enter anything! Try "+suggestion 

        # take care of the # in the string
        if suggestion[0] == '#':
            suggestion = '%23'+suggestion[1:]              
        # take care of whitespace
        suggestion = suggestion.replace(' ','+')
          
        results.append(dict(name=the_result, web='output?ID='+suggestion,name2 = ' ',tweets = ' ',orig = ' '))
        new_tab = '"_self"'
      
    # return the results, tab_opening and original term
    return render_template("output.html",  results = results,ID=str(orig_sterm),new_tab = new_tab)#,the_urls = the_urls)
      
  
