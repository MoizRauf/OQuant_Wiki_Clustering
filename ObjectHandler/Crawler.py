from ObjectHandler.NeoConnector import Neo4jConnector, NeoRestConnector
from ObjectHandler.ORM import WikiPage

__author__ = 'moiz'
import wikipedia


class WikiCrawler:
    def __init__(self,crawlCount):
        self.error_file = open("Dump/log/error.txt", "a")
        self.crawlCount= crawlCount
        return

    def crawl(self):
        pagelist=[]
        for document in wikipedia.random(self.crawlCount):
            try:
                doc = wikipedia.page(document)
                #create document
                page = WikiPage(doc.title,doc.content)
                print("page title : %s \n" % page.getTitle())
                pagelist.append(page)

            except Exception, e:
                self.error_file.write('Search failed: {%s} { %s } \n' % (document, e))
                print 'Search failed: %s' % e

        return pagelist


    #writes data to file
    def writeToFile(self, document):
        try:
            print document

            fileName = "Dump/" + document.title
            text_file = open(fileName, "a")
            # html_str = ny.html()
            text_file.write('Title \n %s \n--------------------------\n' % document.title.encode('utf8'))
            text_file.write(
                'Original Title \n %s \n--------------------------\n' % document.original_title.encode('utf8'))
            text_file.write('Content \n %s \n--------------------------\n' % document.content.encode('utf8'))
            #text_file.write('Summary \n %s \n--------------------------\n' % document.summary.encode('utf8'))
            #text_file.write(html_str.encode('utf8'))

            text_file.close()
        except Exception, e:
            self.error_file.write('Search failed: {%s} { %s } \n' % (document, e))
            print 'Search failed: %s' % e
            pass
        return