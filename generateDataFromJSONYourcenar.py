#! /usr/bin/env python

import sys
import json
import io
import codecs
from optparse import OptionParser
import networkx as nx
#from graph_tool import graph_draw, fruchterman_reingold_layout


class GraphBuilder(object):

    def __init__(self):

        self.data = None

        # Creating the graph
        #self.g = nx.DiGraph()

        self._citedAuthorIndex = {}


    #--------------------
    #   Nodes creation
    #--------------------
    def _createArticleNode(self, articleSubject, articleJsonData):
        # Creating the article Node, with corresponding attributes:
        #    - a date
        #    - a subject
        #    - an author
        #    - a source
        date = articleJsonData[u'created']\
          if (u'created' in articleJsonData)\
          else u'undef'
        author = articleJsonData[u'creator']\
          if (u'creator' in articleJsonData)\
          else u'undef'
        source = articleJsonData[u'source']\
          if (u'source' in articleJsonData)\
          else u'undef'
        title = articleJsonData[u'title']\
          if (u'title' in articleJsonData)\
          else u'undef'
        vid = articleJsonData[u'id']\
          if (u'id' in articleJsonData)\
          else u'undef'
        pages = articleJsonData[u'pages']\
          if (u'pages' in articleJsonData)\
          else u'undef'


        self.g.add_node(articleSubject,
              date = date,
              author = author,
              source = source,
              title = title,
              vid = vid,
              pages = pages,
              vtype = u'article' )

    def _createCitationNode(self, citedAuthorName, citationCount):
        # If the cited author already exists, we only update the count of
        # its citations.
        # N.B: We naively suppose the names are uniques.
        if (citedAuthorName in self.g.nodes()):
            self.g.node[citedAuthorName]['occurences'] =\
                    self.g.node[citedAuthorName]['occurences'] + citationCount
        else:
            self.g.add_node(citedAuthorName,
                    occurences=citationCount,
                    vtype = u'citedAuthor')

        return citedAuthorName

    #--------------------
    # Graph creation : graph general
    #--------------------
    def build_graph(self, file):
        self.data =  json.load(io.open(file, 'r', encoding='utf-8-sig'))
        self.g = nx.DiGraph()
        self._citedAuthorIndex = {}

        articles = [a for a in self.data]
        for article in articles:
            articleNode = self._createArticleNode(article, self.data[article])
            citedAuthors = [
               a.strip()
               for a in self.data[article][u'authors'].split(";")
               if len(a)>0
               ]
            for citedAuthor in citedAuthors:
                # Creating or updating the cited author Node, with attributes:
                #    - a name
                #    - a number of citations (occurences)
                (strCitationCount, citedAuthorName) = citedAuthor.split(' => ')
                citationCount = int(strCitationCount)

                citedAuthorName = self._createCitationNode(citedAuthorName, citationCount)
                # Relating the citation to the article with year
                citationYear = self.data[article][u'created'][0:4]\
                  if (
                    (u'created' in self.data[article]) and\
                      not self.data[article][u'created'] == u'none')\
                  else 0

                self.g.add_edge(article,
                    citedAuthorName,
                    year = int(citationYear),
                    occurenceInAtricle = citationCount)

#-------------------
# Graph creation : graph de cocitations
#-------------------
    def build_graphCoCitations(self, file):
        self.data =  json.load(io.open(file, 'r', encoding='utf-8-sig'))
        self.g = nx.MultiGraph()
        self._citedAuthorIndex = {}

        articles = [a for a in self.data]
        for article in articles:
            #articleNode = self._createArticleNode(article, self.data[article])
            vid = self.data[article][u'id']\
                if (u'id' in self.data[article])\
                    else u'undef'
            citedAuthors = [
                            a.strip()
                            for a in self.data[article][u'authors'].split(";")
                            if len(a)>0
                            ]
            # Relating the citation to the article with year
            citationYear = self.data[article][u'created'][0:4]\
                if (
                    (u'created' in self.data[article]) and\
                        not self.data[article][u'created'] == u'none')\
                else 0
            citedAuth2 = [  a.strip() for a in citedAuthors]
            citedAuth3 = [  a.strip() for a in citedAuthors]
            
            for citedAuthor in citedAuthors:
                # Creating or updating the cited author Node, with attributes:
                #    - a name
                #    - a number of citations (occurences)
                (strCitationCount, citedAuthorName) = citedAuthor.split(' => ')
                citationCount = int(strCitationCount)
                citedAuthorName = self._createCitationNode(citedAuthorName, citationCount)
            for citedAuthor in citedAuth2:
                (strCitationCount, citedAuthorName) = citedAuthor.split(' => ')
                #citedAuthorName = self._createCitationNode(citedAuthorName, citationCount)
                for cA2 in citedAuth2:
                    (strcA2, cAN2) = cA2.split(' => ')
                    if (citedAuthorName<cAN2):
                        #print (citedAuthorName,cAN2)
                        #if vid=="nouvelles-litteraires_1936-12-19_p.006":
                        #    print (citedAuthorName, cAN2,vid,int(citationYear))
                        self.g.add_edge(citedAuthorName,
                                        cAN2,
                                        article = vid,
                                        year = int(citationYear)
                                        )

    #-------------------
    # Graph creation : graph de cocitations
    #-------------------
    def build_graphCoCitations2(self, file):
        self.data =  json.load(io.open(file, 'r', encoding='utf-8-sig'))
        self.g = nx.DiGraph()
        self._citedAuthorIndex = {}
        
        articles = [a for a in self.data]
        for article in articles:
            #articleNode = self._createArticleNode(article, self.data[article])
            vid = self.data[article][u'id'] if (u'id' in self.data[article]) else u'undef'
            citedAuthors = [ a.strip() for a in self.data[article][u'authors'].split(";") if len(a)>0]
            
            # Relating the citation to the article with year
            citationYear = self.data[article][u'created'][0:4] if ( (u'created' in self.data[article]) and not self.data[article][u'created'] == u'none') else u'0'
            citedAuth2 = [  a for a in citedAuthors]
            
            for citedAuthor in citedAuthors:
                # Creating or updating the cited author Node, with attributes:
                #    - a name
                #    - a number of citations (occurences)
                (strCitationCount, citedAuthorName) = citedAuthor.split(' => ')
                citationCount = int(strCitationCount)
                citedAuthorName = self._createCitationNode(citedAuthorName, citationCount)
            for citedAuthor in citedAuth2:
                (strCitationCount, cAN1) = citedAuthor.split(' => ')
                #citedAuthorName = self._createCitationNode(citedAuthorName, citationCount)
                for cA2 in citedAuth2:
                    (strcA2, cAN2) = cA2.split(' => ')
                    if (cAN1<cAN2):
                        #print (citedAuthorName,cAN2)
                        #if vid=="nouvelles-litteraires_1936-12-19_p.006":
                        #    print (citedAuthorName, cAN2,vid,int(citationYear))
                        arti=u''
                        annee=u''
                        #print (self.g.edges())
                        if (cAN1,cAN2) in self.g.edges():
                            allArti=nx.get_edge_attributes(self.g,'article')
                            arti=allArti[(cAN1,cAN2)]
                            allYear=nx.get_edge_attributes(self.g,'year')
                            annee=allYear[(cAN1,cAN2)]
                            self.g.add_edge(cAN1,cAN2,article = arti+u':'+vid,year = annee+u':'+citationYear)
                        else:
                            self.g.add_edge(cAN1,cAN2,article = vid,year = citationYear)



    def saveToGraphml(self, name="YourcenarGraph"):
        nx.write_graphml(self.g, name+".graphml")
        print u"Fichier graphml ecrit: "+name+".graphml"

    def saveToTSV(self, name="YourcenarComplete"):

        outputFile = codecs.open(name+".tsv", "w", "utf-8")

        outputFile.write(u'vid\ttitle\tauthor\tsource\tdate\tpages\tcitedAuthor\tcitationsInArticle\ttotalCitations\n')
        for (article, citedAuthor) in self.g.edges_iter():
            elements = {
                "vid" : self.g.node[article]['vid'],
                "title" : self.g.node[article]['title'],
                "author" : self.g.node[article]['author'],
                "source" : self.g.node[article]['source'],
                "date" : self.g.edge[article][citedAuthor]['year'],
                "pages" : self.g.node[article]['pages'],
                "citedAuthor" : citedAuthor,
                "citationsInArticle" : self.g.edge[article][citedAuthor]['occurenceInAtricle'],
                "totalCitations" : self.g.node[citedAuthor]['occurences'],
            }
            outputFile.write(u'{vid}\t{title}\t{author}\t{source}\t{date}\t{pages}\t{citedAuthor}\t{citationsInArticle}\t{totalCitations}\n'.format(**elements))
        print "Fichier TSV ecrit: "+name+".tsv"


def main():
    usage = "usage: ./%prog [--graphml ou --tsv] [-c] -f parsedCorpus.json"
    parser = OptionParser(usage)
    parser.add_option("-f", "--file",
                      dest="filename",
                      help="Fichier JSON contenant les informations sur le corpus")
    parser.add_option("-o", "--output",
                        dest="outputName",
                        help="Fichier JSON contenant les informations sur le corpus")
    parser.add_option("-t", "--tsv",
                      action="store_true",
                      dest="toTSV",
                      help="Produit un fichier TSV")
    parser.add_option("-g", "--graphml",
                      action="store_false",
                      dest="toTSV",
                      help="Produit un fichier graphml pour visualiser dans Gephi")
    parser.add_option("-c", "--cocitations",
                  action="store_true",
                  dest="coCitations",
                  help="Produit le graph de cocitations")
    parser.add_option("-m", "--cocitations",
                    action="store_true",
                    dest="coCitations2",
                    help="Produit le multigraph de cocitations")
                  
    (options, args) = parser.parse_args()

    gb = GraphBuilder()
    resultJsonFile = options.filename
    outputName=options.outputName
    if outputName=="" or outputName==None:
       outputName="Yourcenar"
    if options.coCitations:
        gb.build_graphCoCitations2(resultJsonFile)
        outputName=outputName+"Cocit"
    elif options.coCitations2:
        gb.build_graphCoCitations(resultJsonFile)
        outputName=outputName+"MultiCocit"
    else:
        gb.build_graph(resultJsonFile)

    if options.toTSV:
        outputName=outputName+"Complete"
        gb.saveToTSV(outputName)
    else:
        outputName=outputName+"Graph"
        gb.saveToGraphml(outputName)
    sys.exit()

if __name__ == '__main__':
    main()
