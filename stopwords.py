'''
Created on 2018-01-01

@author: Ozan Tepe
'''

from nltk.corpus import stopwords

en_stoplist = set(stopwords.words('english'))
'''
my_stoplist = set([
    '',
])


en_stoplist.union(my_stoplist)
'''

my_stopwords = en_stoplist

