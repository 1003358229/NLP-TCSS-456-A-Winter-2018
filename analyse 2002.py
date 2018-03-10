import nltk
import string
import gensim
from pprint import pprint
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.stem import SnowballStemmer
from gensim import corpora, models, similarities
import logging
import glob
import errno
import re



'''reading info that are not printed'''
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



'''open files'''
documents = []
path = 'D:/HOME/TCSS456/NLP-TCSS-456-A-Winter-2018/2002/*.txt'
files = glob.glob(path)
count = 0;
for name in files:
    try:
        with open(name,'r',encoding="utf-8") as file:
            documents.append(file.read().lower())
            txt_name = name.split('\\')
            print(count,'=',txt_name[-1])
            count = count + 1
            pass
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
##pprint(documents)
print('1----------------------------------------------------------------------------------------------------------------')
print('number of documents =',len(documents),'=', count)
print('1.1--------------------------------------------------------------------------------------------------------------')



'''tokenize lines'''
tokenize_documents = [[word for word in document.lower().split()] for document in documents]
##print(tokenize_documents)
print('2----------------------------------------------------------------------------------------------------------------')



'''filter out stop words'''
stop_words = set(stopwords.words('english'))
stop_words_documents = [[word for word in document if word not in stop_words] for document in tokenize_documents]
##pprint(stop_words_documents)
print('3----------------------------------------------------------------------------------------------------------------')



'''remove punctuations'''
punctuations = list(string.punctuation)
punctuations_documents = [[word for word in document if word not in punctuations] for document in stop_words_documents]
##pprint(punctuations_documents)
print('4----------------------------------------------------------------------------------------------------------------')



'''remove empty'''
empty = []
empty.append('')
empty_documents = [document for document in punctuations_documents if document != []]
##pprint(empty_documents)
print('5----------------------------------------------------------------------------------------------------------------')



'''use snowball stemmer'''
snowball_stemmer = SnowballStemmer("english")
stem_documents = [[snowball_stemmer.stem(word) for word in document]for document in empty_documents]
##print(stem_documents)
print('6----------------------------------------------------------------------------------------------------------------')



'''token count and token to id'''
'''should save this'''
dictionary = corpora.Dictionary(stem_documents)
file = open('D:/HOME/TCSS456/NLP-TCSS-456-A-Winter-2018/2002/tmp/dictionary.dic','w')
dictionary.save('D:/HOME/TCSS456/NLP-TCSS-456-A-Winter-2018/2002/tmp/dictionary.dic')
file.close()
##print(dictionary)
print('7----------------------------------------------------------------------------------------------------------------')
##print(dictionary.token2id)
print('8----------------------------------------------------------------------------------------------------------------')



'''coinvert to token count and token id'''
'''should save this'''
corpus = [dictionary.doc2bow(document) for document in stem_documents]
file = open('D:/HOME/TCSS456/NLP-TCSS-456-A-Winter-2018/2002/tmp/corpus.cop','w')
corpora.MmCorpus.serialize('D:/HOME/TCSS456/NLP-TCSS-456-A-Winter-2018/2002/tmp/corpus.cop', corpus)
file.close()
##print(corpus)
print('9----------------------------------------------------------------------------------------------------------------')



