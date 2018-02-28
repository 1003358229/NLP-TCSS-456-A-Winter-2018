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



'''reading info that are not printed'''
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



'''open files'''
documents = []
path = 'D:/HOME/TCSS456/NLP-TCSS-456-A-Winter-2018/*.txt'
files = glob.glob(path)
for name in files:
    try:
        with open(name,'r',encoding="utf-8-sig") as file:
            documents.append(file.read().lower())
            print(name)
##            break
            pass
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
##pprint(documents)
print('1----------------------------------------------------------------------------------------------------------------')
print(len(documents))
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
##pprint(stem_documents)
print('6----------------------------------------------------------------------------------------------------------------')



'''remove words that appear only once'''
#to be done



'''token count and token to id'''
dictionary = corpora.Dictionary(stem_documents)
##print(dictionary)
print('7----------------------------------------------------------------------------------------------------------------')
##print(dictionary.token2id)
print('8----------------------------------------------------------------------------------------------------------------')



##'''not sure but seem useful'''
##new_doc = "I love computer interaction"
##new_vec = dictionary.doc2bow(new_doc.lower().split())
##print(new_vec)



'''coinvert to token count and token id'''
corpus = [dictionary.doc2bow(document) for document in stem_documents]
##pprint(corpus)
print('9----------------------------------------------------------------------------------------------------------------')



'''TF-IDF'''
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
##for doc in corpus_tfidf:
##    print(doc)
print('10----------------------------------------------------------------------------------------------------------------')



'''LSI topics'''
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=5)
##lsi.print_topics(2)
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



'''find similar'''
index = similarities.MatrixSimilarity(lsi[corpus])
f = open("D:/HOME/TCSS456/NLP-TCSS-456-A-Winter-2018/21.txt",encoding="utf-8-sig")
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
