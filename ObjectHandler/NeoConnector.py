from neo4jrestclient.client import GraphDatabase

__author__ = 'moiz'
from py2neo import Graph, Node,authenticate




class Neo4jConnector:
    _graph_connection = None

    def __init__(self, connectionString=None):
        # set up authentication parameters
        authenticate("localhost:7474", "neo4j", "123")

        self.connectionString = "http://localhost:7474/db/data/"
        self._graph_connection = Graph(connectionString)
        self.error_file = open("Dump/log/dberror.txt", "a")
        return


    def createNodes(self, wikiPage):
        print ("creating node %s" %wikiPage.getTitle())
        try:
            if self._graph_connection is not None:
                alice = Node("article2",name = wikiPage.title,content= wikiPage.getContent())
                self._graph_connection.create(alice)
            else:
                self.error_file.write("create node failed: connection not avaialable".encode('utf-8'))
                print 'create node failed: connection not avaialable'
            return
        except Exception, e:
                self.error_file.write('Search failed: {%s} { %s } \n' % (wikiPage.getTitle(), e.message))
                print 'create node failed: %s %s' % (e.message,e.args)
                pass



class NeoRestConnector:
    _graph_connection = None

    def __init__(self, connectionString=None):
        self.connectionString = connectionString
        self.db = GraphDatabase("http://localhost:7474", username="neo4j", password="123")
        self.error_file = open("Dump/log/restdberror.txt", "a")
        return


    def createNodes(self, wikiPage):
        print ("creating node %s" %wikiPage.getTitle())
        try:
            label = self.db.labels.create("article")
            node = self.db.nodes.create(name = wikiPage.getTitle())
            label.add(node)
            return
        except Exception, e:
                self.error_file.write('Search failed: {%s} { %s } \n' % (wikiPage.getTitle(), e.message))
                print 'create node failed: %s' % e.message
                pass

    def __del__(self):
        return
