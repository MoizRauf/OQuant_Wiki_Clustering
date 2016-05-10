from Algo.ClusteringAlgo import Tfif, LDA, HierarchalCluster
from ObjectHandler.NeoConnector import Neo4jConnector
from Util.NLPHelper import NERTagging, POSTagging

__author__ = 'moiz'

from ObjectHandler.Crawler import WikiCrawler
try:
    error_file = open("Dump/log/mainerror.txt", "a")

    storageHandler= Neo4jConnector()




    print("welcome to wiki clustering ")

    #crawl pages from wikipedia
    crawler = WikiCrawler(3)
    docList=[]
    for i in range(0,1):
        pages=[]
        pages= crawler.crawl()
        for page in pages:
            docList.append(page)

    #crawl 10 documents


    dict={}
    #get topic distribution based out of LDA
    for document in docList:
        LdaAlgo = LDA(6,80)
        #LdaAlgo.train(docList)
        resDict={}
        resDict= LdaAlgo.analyze(document.getTitle(), document.getContent())

        #document.setTags(resDict['word_list'])

        document.setTopicmatrix(resDict['topicMatrix'])

        dict[document.getTitle()]=resDict['word_list']
        resDict =None
        LdaAlgo.__del__()

    clusterAlgo = LDA(6,80)
    #calculate similarity against all documents
    sim_Score= clusterAlgo.get_sim_score(dict)
    hirAlgo = HierarchalCluster(dict.keys())
    hirAlgo.create_hierarchy(sim_Score)


     #self.storageHandler.createNodes(page)
except Exception, e:
                error_file.write('Search failed:{ %s } \n' % ( e))
                print 'main failed: %s' % e.message
                pass