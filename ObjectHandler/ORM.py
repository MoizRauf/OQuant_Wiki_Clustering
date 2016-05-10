import Algo
from Algo.ClusteringAlgo import LDA, Tfif

__author__ = 'moiz'

# represents a wikipedia page containing title, content
class WikiPage:
    #---------Properties----------
    #nlp meta NER etc info
    #tfIf value
    #HDA value
    #ward value
    #--------------------------
    #TODO: reset this value based on the documents saved in the db
    pageCount = 0
    clusterValue = None

    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.pageCount += 1

        return

    def getContent(self):
        return self.content

    def getTitle(self):
        return self.title

    def getPageID(self):
        return self.pageCount

    #sets result value of tfif
    def setLDA(self, clusterValue):
        self.clusterValue = clusterValue
        return

    def getLDA(self):
        return self.clusterValue

    def getID(self):
        return self.pageCount


