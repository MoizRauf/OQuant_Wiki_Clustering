import Algo
from Algo.ClusteringAlgo import LDA, Tfif

__author__ = 'moiz'

# represents a wikipedia page containing title, content
class WikiPage:
    tags =None
    topicMatrix=None
    def __init__(self, title, content):
        self.title = title
        self.content = content
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

    def setTags(self,tag):
        self.tags=tag
        return

    def getTags(self):
        return self.tags

    def setTopicmatrix(self,topicMatrix):
        self.topicMatric= topicMatrix
        return

    def getTopicMatrix(self):
        return self.topicMatrix


