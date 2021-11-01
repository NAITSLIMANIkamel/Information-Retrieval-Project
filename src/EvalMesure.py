from abc import ABC,abstractmethod
import numpy as np
class EvalMesure(ABC):

   @abstractmethod
   def evalQuery(self,liste, query):
       pass

class Precision(EvalMesure):
    """Precision au rang K d'une requete"""
    def __init__(self,rang):
        self.rang=rang

    def getRang(self):
        return self.rang

    def setRang(self, rang):
        self.rang = rang

    def evalQuery(self,liste, query):
        relDoc=query.isRelevant(liste[:self.rang])
        return relDoc.sum()/self.rang


class Rappel(EvalMesure):
    """Rappel au rang k"""
    def __init__(self,rang):
        self.rang=rang

    def getRang(self):
        return self.rang

    def setRang(self, rang):
        self.rang = rang

    def evalQuery(self,liste, query):
        relDoc=query.isRelevant(liste[:self.rang])
        length=query.reLength()
        if(length ==0 ):
            return 1.
        return relDoc.sum()/length


class F_measure(EvalMesure):
    """F-Mesure avec beta=1"""
    def __init__(self,rang,beta=1):
        self.beta=beta
        self.rang=rang

    def getBeta(self):
        return self.beta

    def setBeta(self,beta):
        self.beta=beta

    def getRang(self):
        return self.rang

    def setRang(self, rang):
        self.rang = rang

    def evalQuery(self,liste, query):
        r=Rappel(self.rang).evalQuery(liste,query)
        p=Precision(self.rang).evalQuery(liste,query)
        if(r==0. or p==0.):
            return 0.
        return ((1+self.beta*self.beta)*(p*r))/((self.beta*self.beta*p)+r)

class AvgP(EvalMesure):
    """Moyenne des precisions au dernier document pertinent"""
    def evalQuery(self,liste, query):
        relDoc = query.isRelevant(liste)
        avgp=0.
        for k in np.where(relDoc)[0]:
            avgp+=Precision(k+1).evalQuery(liste,query)
        return avgp/(query.reLength() or 1)

class RR(EvalMesure):
    """Le premier rang du premier document pertinent"""
    def evalQuery(self,liste, query):
        relDoc = np.where(query.isRelevant(liste))[0]
        if(len(relDoc)==0):
            return 0.
        return 1/(relDoc[0]+1)


class NDCG(EvalMesure):

    def __init__(self,rang):
        self.rang=rang


    def DCG(self,relDoc):

        dcg=relDoc[0]
        dcg += (relDoc[1:self.rang]/np.log2(np.arange(2,(self.rang+1)))).sum()
        return dcg

    def evalQuery(self,liste, query):
        #relIdeal = np.sort(query.isRelevant(liste))[::-1]
        relIdeal=np.ones(len(query.getPertiDoc()))
        if (len(relIdeal) < self.rang):
            relIdeal = np.hstack((relIdeal, np.ones(self.rang - len(relIdeal))))
        relIdeal = relIdeal[:self.rang]
        relDoc = query.isRelevant(liste[:self.rang])
        return self.DCG(relDoc) / self.DCG(relIdeal)




