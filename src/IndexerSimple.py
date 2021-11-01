from .TextRepresentre import *
from collections import Counter
import numpy as np
import copy

class IndexerSimple(object):

    def __init__(self,collection):
        self.collection=collection
        self.totalStem=0
        self.index,self.index_inv,self.index_from,self.index_to=self.indexation(copy.deepcopy(collection))

    def indexation(self,collection):
        index,index_inv,index_from,index_to=dict(),dict(),dict(),dict()
        porter = PorterStemmer()
        for idDoc,doc in collection.items():
            index[idDoc]=porter.getTextRepresentation(doc.getTitle()+" " +doc.getText())
            index_from[idDoc]=Counter(doc.getLink())
            for word,freq in index[idDoc].items():
                self.totalStem+=freq
                if (index_inv.get(word)):
                    index_inv[word].update({idDoc: freq})
                else:
                    index_inv[word] = {idDoc: freq}
            for doc,freq in index_from[idDoc].items():
                if(index_to.get(doc)):
                    index_to[doc].update({idDoc: freq})
                else:
                    index_to[doc]={doc:freq}
        return index,index_inv,index_from,index_to

    def getTfsForDoc(self, idDoc):
        res = self.index.get(idDoc)
        if (res):
            return res
        return dict()

    def getTfIDFsForDoc(self, idDoc):
        tfidf = dict()
        N = len(self.index)
        tf=self.index.get(idDoc)
        for word,freq in tf.items():
            idf=np.log((1 + N) / (1 + len(self.index_inv.get(word))))
            tfidf[word] =freq*idf
        return tfidf

    def getTfsForStem(self, stem):
        res = self.index_inv.get(stem)
        if (res):
            return res
        return dict()

    def getTfIDFsForStem(self, stem):
        tfidf = dict()
        N = len(self.index)
        tdf=self.index_inv.get(stem)
        if (tdf):
            df = len(tdf)
            idf = np.log((1 + N) / (1 + df))
            for doc,freq in tdf.items():
                tfidf[doc] = freq*idf
        return tfidf

    def getHyperlinksTo (self,idDoc):
        return self.index_to.get(idDoc,dict())

    def getHyperlinksFrom(self,idDoc):
        return self.index_from.get(idDoc,dict())

    def getIndex(self):
        return self.index

    def getIndex_inv(self):
        return self.index_inv

    def getIndex_to(self):
        return self.index_to

    def getIndex_from(self):
        return self.index_from

    def getCollection(self):
        return self.collection

    def getNbDocsForStem(self,stem):
        rep=self.index_inv.get(stem)
        if(rep):
            return len(rep)
        return 0

    def getNbStemForDocs(self,idDoc):
        res=self.index.get(idDoc)
        if(res):
            return len(res)
        return 0

    def getNbsDocs(self):
        return len(self.index)

    def getNbsStems(self):
        return len(self.index_inv)

    def getTotalStem(self):
        return self.totalStem

    def getLengthOfDoc(self,idDoc):
        res=self.index.get(idDoc)
        if(res):
            return np.sum(list(res.values()))
        return 0

    def getStrDoc(self,idDoc):
        return str(self.collection[idDoc].getDocument())