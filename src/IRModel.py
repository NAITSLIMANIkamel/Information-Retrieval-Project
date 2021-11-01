from abc import ABC,abstractmethod
import numpy as np
from .TextRepresentre import *
from random import sample


class IRModel(ABC):
    def __init__(self,index):
        self.index=index

    @abstractmethod
    def getScores(self,query):
        pass

    def getRanking(self,query):
        scores = self.getScores(query)
        return dict(sorted(scores.items(), reverse=True, key=lambda item: item[1]))

class Vectoriel(IRModel):
    def __init__(self, index, weighter=w, normalized=True):
        super().__init__(index)
        self.weighter = weighter
        self.normalized = normalized
        self.docWeight={idDoc:self.weighter.getWeightsForDoc(idDoc) for idDoc in self.index.getIndex()}
        if(normalized):
            self.docWeight={idDoc: self.normalize(self.docWeight[idDoc]) for idDoc in self.docWeight}


    def normalize(self,dicWord):
        norm=np.linalg.norm(list(dicWord.values()))
        return {k: v / norm for k, v in dicWord.items()}

    def getScores(self, query):
        stemWeight = self.weighter.getWeightsForQuery(query)
        if(self.normalized):
            stemWeight=self.normalize(stemWeight)
        scores=dict()
        for term,termWaight in stemWeight.items():
            docs=self.weighter.getWeightsForStem(term)
            for doc in docs:
                scores[doc]=scores.get(doc,0.)+(termWaight*self.docWeight[doc][term])
        return scores

class ModeleLangue(IRModel):
    """ sigma 0.1 for short queries
        sigma 0.7 for long queries
        P(t|d) = (1−sig)*P(t|Md) + sig*tP(t|MC) pour t dans q ]
        P(t|Md) = tf(t,d)/nb_mots_dans_le_document
        P(t|MC) = freq_de_t_dans_la _collection/nb_de_mots_dans_la_collection
    """

    def __init__(self,index,sigma=0.1):
        super().__init__(index)
        self.sigma=sigma

    def getSigma(self):
        return self.sigma

    def setSigma(self,sigma):
        self.sigma=sigma

    def getScores(self,query):
        tf_query = PorterStemmer().getTextRepresentation(query)
        scores=dict()
        total_tf_corpus = self.index.getTotalStem()
        for idDoc,stemDict in self.index.getIndex().items():
            lenDoc = self.index.getLengthOfDoc(idDoc)
            P=0.
            for term,t_weight in tf_query.items():
                docsForStem=self.index.getTfsForStem(term)
                P_t_MC = np.sum(list(docsForStem.values())) / total_tf_corpus
                P_t_Md = stemDict.get(term, 0.) / lenDoc if lenDoc != 0. else 0.
                P += t_weight*np.log(((1 - self.sigma) * P_t_Md + (self.sigma * P_t_MC))+1e-12)
            scores[idDoc]=P
        return scores

class Okapi_BM25(IRModel):

    def __init__(self, index, k1=1.2, b=0.75):
        super().__init__(index)
        self.k1 = k1
        self.b = b
        self.docCount = self.index.getNbsDocs()
        self.avgdl=self.index.getTotalStem()/self.docCount

    def getScores(self, query):
        tf_query = PorterStemmer().getTextRepresentation(query)
        res = dict()
        for idDoc,stemDic in self.index.getIndex().items():
            scorer = 0
            for term,t_weight in tf_query.items():
                idf = self.idf(self.index.getNbDocsForStem(term), self.docCount)
                tf = stemDic.get(term,0.)
                norme = self.k1 * (1 - self.b + self.b * (self.index.getLengthOfDoc(idDoc) / self.avgdl))
                scorer += idf * (tf / (tf + norme))
            res[idDoc] = scorer
        return res

    def idf(self, docFreq, docCount):
        if (docFreq == 0):
            return 0.0
        return np.log(docCount/docFreq + 1e-20)

    def getK1(self):
        return self.k1

    def getB(self):
        return self.b

    def setK1(self,k1):
        self.k1=k1

    def setB(self,b):
        self.b=b





