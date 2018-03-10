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
import os


'''reading info that are not printed'''
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


'''read generated files'''
if (os.path.exists("D:/HOME/TCSS456/NLP-TCSS-456-A-Winter-2018/2017/tmp/dictionary.dic")):
    dictionary = corpora.Dictionary.load('D:/HOME/TCSS456/NLP-TCSS-456-A-Winter-2018/2017/tmp/dictionary.dic')
    corpus = corpora.MmCorpus('D:/HOME/TCSS456/NLP-TCSS-456-A-Winter-2018/2017/tmp/corpus.cop')
    print("Used files generated")
else:
    print("Please generate data set")

##print(list(corpus))
##print(dictionary)
##print(dictionary.token2id)

'''TF-IDF'''
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
##for doc in corpus_tfidf:
##    print(doc)
print('10----------------------------------------------------------------------------------------------------------------')



'''LSI topics'''
'''need to be more than 2(3 or more)'''
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)
##lsi.print_topics(5)
print('11----------------------------------------------------------------------------------------------------------------')



'''LSI larger means more related'''
corpus_lsi = lsi[corpus_tfidf]
##for doc in corpus_lsi:
##    print(doc)
print('12----------------------------------------------------------------------------------------------------------------')



'''LDA topics does not seem as good'''
##lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=2)
##lda.print_topics(2)
##print('13----------------------------------------------------------------------------------------------------------------')


'''display file names'''
count = 0;
path = 'D:/HOME/TCSS456/NLP-TCSS-456-A-Winter-2018/2017/*.txt'
files = glob.glob(path)
for name in files:
    try:
        txt_name = name.split('\\')
        print(count,'=',txt_name[-1])
        count = count + 1
        pass
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
print('13.1----------------------------------------------------------------------------------------------------------------')

'''find similar'''
index = similarities.MatrixSimilarity(lsi[corpus])
f = open("D:/HOME/TCSS456/NLP-TCSS-456-A-Winter-2018/2017/21. I'm The One.txt",encoding="utf-8")
query = f.read()
query_bow = dictionary.doc2bow(query.lower().split())
##pprint(query_bow)
print('14----------------------------------------------------------------------------------------------------------------')
query_lsi = lsi[query_bow]
##pprint(query_lsi)
print('15----------------------------------------------------------------------------------------------------------------')
sims = index[query_lsi]
##pprint(list(enumerate(sims)))
print('16----------------------------------------------------------------------------------------------------------------')
sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
pprint(sort_sims)
print('17----------------------------------------------------------------------------------------------------------------')
