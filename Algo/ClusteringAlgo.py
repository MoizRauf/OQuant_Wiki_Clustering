__author__ = 'moiz'
from time import time

import gensim
from gensim import corpora, models, similarities
import numpy
from Util.NLPHelper import tokenize_and_stem, NERTagging, POSTagging
from scipy.cluster.hierarchy import ward, dendrogram
import matplotlib.pyplot as plt
import matplotlib as mpl

class LDA:
    def __init__(self, numTopic=None, passCount=None, wordCount=6):
        self.path='Algo/Model/'
        self.log_file = open("Dump/log/LDA_put.txt", "a")
        self.numTopic = numTopic
        self.passcount = passCount
        self.numWords= wordCount

        return
    def train(self,wiki_article):
        tokenizedtext=[]
        t0 = time()

        for wiki in wiki_article:
            # STEP 1 : create dictionary of raw text
            document= wiki.getTitle() + wiki.getContent()
            stem = tokenize_and_stem(document.lower())
            tokenizedtext.append(stem)

        dictionary = corpora.Dictionary(tokenizedtext)
        print dictionary
        dictionary.save(self.path+'source.dict') # store the dictionary, for future reference

        # convert dictionary to vector space
        corpus = [dictionary.doc2bow(t) for t in tokenizedtext]
        corpora.MmCorpus.serialize(self.path+'source.mm', corpus) # store to disk


        # Transform Text with TF-IDF
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=self.numTopic, id2word=dictionary,
                                                   passes=self.passcount)
        model_name = self.path+'model'
        ldamodel.save(model_name)

        # corpus tf-idf
        corpus_lda = ldamodel[corpus]

        # STEP 3 : Create similarity matrix of all files
        index = similarities.MatrixSimilarity(ldamodel[corpus])
        index.save(self.path+'source.index')
        index = similarities.MatrixSimilarity.load(self.path+'source.index')

        sims = index[corpus_lda]

        print "Done in %.3fs"%(time()-t0)

        return

    def analyze(self,title, content):
        tokenizedtext=[]
        t0 = time()
        document=title+content
        self.log_file.write('%s  \n' % (document.encode('utf-8')))
        # STEP 1 : create dictionary of raw text
        stem = tokenize_and_stem(document.lower())
        tokenizedtext.append(stem)
        dictionary = corpora.Dictionary(tokenizedtext)

        #dictionary.save(self.path+'tweets.dict') # store the dictionary, for future reference

        # convert dictionary to vector space
        corpus = [dictionary.doc2bow(t) for t in tokenizedtext]


        # generate LDA model
        self.log_file.write('Title \n num of topic: %d, passes : %d \n' % (self.numTopic, self.passcount) )

        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=self.numTopic, id2word=dictionary,
                                                   passes=self.passcount)
        model_name = self.path+title
        ldamodel.save(model_name)
        #print topic_words
        self.log_file.write(
            'Model \n %s \n--------------------------\n' % ldamodel.print_topics(self.numTopic,self.numWords))

        #topics_matrix = ldamodel.show_topics(formatted=False, num_words=self.numWords)
        topics_matrix= ldamodel.show_topics(self.numTopic,self.numWords)
        word_list=[]

        sparseDict={}
        #worst possible approach i could think of to get words
        dct = dict(topics_matrix)
        for key in dct:
            dct2= dct.get(key)
            splitList=dct2.split('+')
            for word in splitList:
                word1= word.split('*')[1].strip()
                #sparseDict[word1]= word.split('*')[0].strip()
                sparseDict[ word.split('*')[0].strip()]=word1
                #if word1 not in word_list:
                #    word_list.append(word1)

        return {'topicMatrix':topics_matrix, 'word_list':sparseDict }

    def get_sim_score(self,article_dict={}):
        sim_matrix= numpy.zeros(shape=(len(article_dict),len(article_dict)))
        i = 0

        for doc1 in article_dict:
            tags = ''
            #for tag in article_dict[doc1]:
            #    tags += tag.encode('utf-8')
            #    tags += ' '
            dense1 = gensim.matutils.sparse2full(article_dict[doc1], self.numTopic)
            j = 0
            for doc2 in article_dict:
            #    doc2_tag=''
            #    for tag2 in article_dict[doc2]:
            #        doc2_tag += tag2.encode('utf-8')
            #        doc2_tag += ' '
                dense2 = gensim.matutils.sparse2full(article_dict[doc2], self.numTopic)
                sim_val = numpy.sqrt(0.5 * ((numpy.sqrt(dense1) - numpy.sqrt(dense2))**2).sum())
                sim_matrix[i][j]=sim_val
                j+=1
            i+=1

        return sim_matrix

    def __del__(self):
        if  not self.log_file.closed:
            self.log_file.close()
        return

class HierarchalCluster:

    def __init__(self,title=[]):
        self.titles=title
        self.path='Algo/tmp/'
        return



    def create_hierarchy(self, sim_matrix):
        linkage_matrix = ward(sim_matrix)
        fig, ax = plt.subplots(figsize=(15, 20)) # set size
        ax = dendrogram(linkage_matrix, orientation="right", labels=self.titles);

        plt.tick_params(\
            axis= 'x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            top='off',         # ticks along the top edge are off
            labelbottom='off')

        plt.tight_layout() #show plot with tight layout

        #uncomment below to save figure
        plt.savefig('ward_clusters.png', dpi=200) #save figure as ward_clusters
        return
class Tfif:
    def __init__(self):
        # keywords have been extracted and stopwords removed.
        self.path='tmp/'

        return

    def analyze(self, document):
        tokenizedtext=[]
        t0 = time()

        # STEP 1 : create dictionary of raw text
        stem = tokenize_and_stem(document.lower())
        tokenizedtext.append(stem)
        dictionary = corpora.Dictionary(tokenizedtext)

        dictionary.save(self.path+'tweets.dict') # store the dictionary, for future reference

        # convert dictionary to vector space
        corpus = [dictionary.doc2bow(t) for t in tokenizedtext]


         # Transform Text with TF-IDF
        tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model


        # corpus tf-idf
        corpus_tfidf = tfidf[corpus]

        # STEP 3 : Create similarity matrix of all files
        index = similarities.MatrixSimilarity(tfidf[corpus])
        index.save(self.path+'deerwester.index')
        index = similarities.MatrixSimilarity.load(self.path+'deerwester.index')

        sims = index[corpus_tfidf]

        print "Done in %.3fs"%(time()-t0)

        print sims
        print list(enumerate(sims))
        sims = sorted(enumerate(sims), key=lambda item: item[1])
        print sims # print sorted (document number, similarity score) 2-tuples

    def analyze2(self):
        # read data from object helper

        #create nlphelper instance

        tokenizedtext=[]
        t0 = time()
        for text in self.tweets:
             # STEP 1 : create dictionary of raw text
            stem = tokenize_and_stem(text.lower())
            tokenizedtext.append(stem)

        dictionary = corpora.Dictionary(tokenizedtext)
        print dictionary
        dictionary.save(self.path+'tweets.dict') # store the dictionary, for future reference

        # convert dictionary to vector space
        raw_corpus = [dictionary.doc2bow(t) for t in tokenizedtext]
        corpora.MmCorpus.serialize(self.path+'tweets.mm', raw_corpus) # store to disk


        # STEP 2 : similarity between corpuses
        dictionary = corpora.Dictionary.load('../tmp/tweets.dict')
        corpus = corpora.MmCorpus(self.path+'tweets.mm')

        # Transform Text with TF-IDF
        tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model
        print tfidf

        # corpus tf-idf
        corpus_tfidf = tfidf[corpus]

        # STEP 3 : Create similarity matrix of all files
        index = similarities.MatrixSimilarity(tfidf[corpus])
        index.save(self.path+'deerwester.index')
        index = similarities.MatrixSimilarity.load(self.path+'deerwester.index')

        sims = index[corpus_tfidf]

        print "Done in %.3fs"%(time()-t0)

        # print sims
        # print list(enumerate(sims))
        # sims = sorted(enumerate(sims), key=lambda item: item[1])
        # print sims # print sorted (document number, similarity score) 2-tuples

        return

