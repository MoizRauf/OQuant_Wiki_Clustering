from Algo.ClusteringAlgo import Tfif, LDA, HierarchalCluster
from ObjectHandler.NeoConnector import Neo4jConnector
from Util.NLPHelper import NERTagging, POSTagging

__author__ = 'moiz'

from ObjectHandler.Crawler import WikiCrawler
try:
    error_file = open("Dump/log/mainerror.txt", "a")

    storageHandler= Neo4jConnector()
    tfAlgo = Tfif()
    LdaAlgo = LDA(5,80)


    print("welcome to wiki clustering ")
    crawler = WikiCrawler(2)
    #crawl 10 documents
    docList=[]
    docList=crawler.crawl()
    dict={}
    for document in docList:
        #tfAlgo.analyze(document.getContent())
        document.setLDA(LdaAlgo.analyze(document.getTitle(), document.getContent(),document.getID()))
        dict[document.getTitle()]=document.getLDA()

    cAlgo = HierarchalCluster(dict.keys())
    count= len(dict)

    temp=cAlgo.calculate_simMatrix(count , dict)
    cAlgo.create_hierarchy(temp)

    LdaAlgo.__del__()
     #self.storageHandler.createNodes(page)
except Exception, e:
                error_file.write('Search failed:{ %s } \n' % ( e))
                print 'main failed: %s' % e.message
                pass