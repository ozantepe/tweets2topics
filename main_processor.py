'''
Created on 2017-12-29

@author: Ozan Tepe
'''

import os
import csv
import re
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
warnings.filterwarnings(action='ignore', category=DeprecationWarning)
import gensim
import pyLDAvis.gensim as gensimvis
import pyLDAvis

from gensim import corpora
from gensim.models import LdaModel
from nltk.stem.porter import PorterStemmer
from properties import username, tweets_path, userfile_path
from stopwords import my_stopwords

tweets = []
docs = []


def read_tweets():
    success = False
    
    # Read tweets from files
    if os.path.isdir(tweets_path):
        files = os.listdir(tweets_path)
        found = False
        for filename in files:
            if username in filename:
                found = True
                fullpath = os.path.join(tweets_path, filename)
                try:
                    with open(fullpath, 'r', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            tweets.append(row['text'])                        
                    success = True
                except:
                    print("Could not load tweets from csv file..")
                    raise
        if found == 0:
            print("Wrong username..")
        else:
            print("Tweets loaded for username " + username + " successfully..")
    else:
        print("Couldn't find file path..")
    
    return success


def process_tweets():
    global docs
    
    words = []
    texts = []
    
    # Creating classes for cleaning process
    stoplist = my_stopwords
    p_stemmer = PorterStemmer()
    
    # Regular expressions
    regex1 = r'[^a-zA-z]|http[s].*'
    regex2 = r'^(?!http.*$).*'
    compiled1 = re.compile(regex1)
    compiled2 = re.compile(regex2)
    
    for tweet in tweets:

        # Tokenization
        words.clear()
        tokens = tweet.lower().split(' ')
        for token in tokens:
            
            # Check if token does not start with 'http'
            if compiled2.match(token):
                
                # Remove non-alpha chars
                token = compiled1.sub("", token)
                
                # Discard token if it's a stop word
                if token not in stoplist:
                    if len(token) > 2:
                        words.append(token)
                    
        # Stemming
        texts.append([p_stemmer.stem(word) for word in words])
    
    # Calculate frequency of words 
    from collections import defaultdict
    frequency = defaultdict(int)
    for text in texts:
        for word in text:
            frequency[word] += 1
            
    # Remove words with frequency lower than 2 from each document
    docs = [[word for word in text if frequency[word] > 1] for text in texts]

    '''
    for doc in docs:
        print(doc)
    '''
    print("Preprocessing completed..")


def implement_lda():
    global docs
    
    if docs:
        
        if not os.path.isdir(userfile_path):
            os.mkdir(userfile_path)
        
        # Turn our tokenized documents into a id <-> term dictionary
        dictionary = corpora.Dictionary(docs)
        dictionary.save(os.path.join(userfile_path, username + '_dictionary.dict'))
        print("Dictionary saved..")
    
        # Convert tokenized documents into a document-term matrix
        doc_term_matrix = [dictionary.doc2bow(doc) for doc in docs]
        gensim.corpora.MmCorpus.serialize(os.path.join(userfile_path, username + '_corpus.mm'), doc_term_matrix)
        print("Corpus saved..")
        
        # Creating the object for LDA model using gensim library
        Lda = gensim.models.ldamodel.LdaModel
        
        # Running and Trainign LDA model on the document term matrix.
        ldamodel = Lda(doc_term_matrix, num_topics=10, id2word=dictionary, passes=10)
        '''
        for i in ldamodel.print_topics(): 
            for j in i: 
                print(j)
        '''
        ldamodel.save(os.path.join(userfile_path, username + '_topic.model'))
        print("LDA model saved..")
    
    else:
        print("There is no documents, could not save files..")


def show_results():    
    try: 
        
        # Load dictionary
        loaded_dict = gensim.corpora.Dictionary.load(os.path.join(userfile_path, username + '_dictionary.dict'))
        
        # Load corpus
        loaded_corpus = gensim.corpora.MmCorpus(os.path.join(userfile_path, username + '_corpus.mm'))
        
        # Load lda model
        loaded_model = LdaModel.load(os.path.join(userfile_path, username + '_topic.model'))
        
        # Visualization of results
        vis_data = gensimvis.prepare(loaded_model, loaded_corpus, loaded_dict)
        pyLDAvis.show(vis_data)
        
    except:
        print("Could not load files..")
        raise


if __name__ == '__main__':
    try:
        if read_tweets():
            process_tweets()
            implement_lda()
        show_results()
    except Exception:
        print("Something's wrong..")
