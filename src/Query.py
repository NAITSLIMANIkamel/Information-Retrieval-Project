import numpy as np

class Query(object):

    def __init__(self,idReq,texte=""):
        self.idReq=idReq
        self.texte=texte
        self.pertiDoc=[]

    def getIdReq(self):
        return self.idReq

    def getTexte(self):
        return self.texte

    def getPertiDoc(self):
        return self.pertiDoc

    def setTexte(self,texte):
        self.texte=texte

    def setPertiDoc(self,pertiDoc):
        self.pertiDoc=pertiDoc

    def appendPertiDoc(self,idDoc):
        self.pertiDoc.append(idDoc)

    def isRelevant(self,docs):
        return np.in1d(docs,self.pertiDoc)

    def reLength(self):
        return len(self.pertiDoc)

    def __str__(self):
        return 'Query id :'+ str(self.idReq) +' Texte :' +self.texte +'Document Pertinent ' +str(self.pertiDoc)
