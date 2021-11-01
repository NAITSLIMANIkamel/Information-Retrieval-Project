from abc import ABC,abstractmethod
from .TextRepresentre import *
import numpy as np

class Weighter(ABC):

    def __init__(self,index):
        self.index=index
        self.porter=PorterStemmer()

    @abstractmethod
    def getWeightsForDoc(self,idDoc):
        pass

    @abstractmethod
    def getWeightsForStem(self,stem):
        pass

    @abstractmethod
    def getWeightsForQuery(self,query):
        pass

class Weighter1(Weighter):
    """wt,d=tft,d et wt,q= 1 si t∈q, O sinon"""
    def __init__(self,index):
        super().__init__(index)


    def getWeightsForDoc(self,idDoc):
        return self.index.getTfsForDoc(idDoc)


    def getWeightsForStem(self,stem):
        return self.index.getTfsForStem(stem)


    def getWeightsForQuery(self,query):
        words=self.porter.getTextRepresentation(query)
        return {term:1 for term in words}

class Weighter2(Weighter):
    """wt,d=tft,d et wt,q=tft,q"""
    def __init__(self,index):
        super().__init__(index)

    def getWeightsForDoc(self,idDoc):
        return self.index.getTfsForDoc(idDoc)

    def getWeightsForStem(self,stem):
        return self.index.getTfsForStem(stem)

    def getWeightsForQuery(self,query):
        return self.porter.getTextRepresentation(query)

class Weighter3(Weighter):
    """wt,d=tft,d et wt,q=idft si t∈q, 0 sinon ;"""
    def __init__(self,index):
        super().__init__(index)

    def getWeightsForDoc(self,idDoc):
        return self.index.getTfsForDoc(idDoc)

    def getWeightsForStem(self,stem):
        return self.index.getTfsForStem(stem)

    def getWeightsForQuery(self,query):
        words = self.porter.getTextRepresentation(query)
        N = len(self.index.getIndex())
        return {term:(np.log((1+N)/(1+self.index.getNbDocsForStem(term)))) for term in words}


class Weighter4(Weighter):
    """wt,d= 1 +log(tft,d) si t∈d, 0 sinon ; et wt,q=idft si t∈q, 0"""

    def __init__(self, index):
        super().__init__(index)

    def getWeightsForDoc(self, idDoc):
        res = self.index.getTfsForDoc(idDoc)
        return {term:(1+np.log(tf)) for term,tf in res.items()}


    def getWeightsForStem(self, stem):
        res= self.index.getTfsForStem(stem)
        return {idDoc:(1+np.log(freq)) for idDoc,freq in res.items()}


    def getWeightsForQuery(self, query):
        words = self.porter.getTextRepresentation(query)
        N = len(self.index.getIndex())
        return {term: (np.log((1 + N) / (1 + self.index.getNbDocsForStem(term)))) for term in words}



class Weighter5(Weighter):
    """wt,d= (1 +log(tft,d))*idft si t∈d, 0 sinon ; et wt,q= (1 +log(tft,q))x idft si t∈q, 0."""

    def __init__(self, index):
        super().__init__(index)

    def getWeightsForDoc(self, idDoc):
        res = self.index.getTfsForDoc(idDoc)
        N=len(self.index.getIndex())
        return {term:((1+np.log(freq))*(np.log((1+N)/(1+self.index.getNbDocsForStem(term))))) for term,freq in res.items()}

    def getWeightsForStem(self, stem):
        res= self.index.getTfsForStem(stem)
        N=len(self.index.getIndex())
        idf=(np.log((1 + N) / (1 + self.index.getNbDocsForStem(stem))))
        return {idDoc: (1 + np.log(freq)) * idf for idDoc,freq in res.items()}

    def getWeightsForQuery(self, query):
        words = self.porter.getTextRepresentation(query)
        N = len(self.index.getIndex())
        return {term:(1+np.log(freq))* (np.log((1+N)/(1+self.index.getNbDocsForStem(term)))) for term,freq in words.items()}









