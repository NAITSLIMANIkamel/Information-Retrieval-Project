from .IRModel import *
from random import sample
from .IndexerSimple import *


class PageRank(IRModel):

    def __init__(self,index ,n=50,k=10,d=0.85,epsilon=1e-5,maxIter=500,model=None):
        super(PageRank,self).__init__(index)
        self.n=n #pour le nombre de document a cosiderer
        self.k=k #nombre de lien a cosiderer
        self.model= model if model else Okapi_BM25(index)  #model de recherche par defaut Okapi_BM25
            
        self.d=d
        self.epsilon=epsilon
        self.maxIter=maxIter

    def getD(self):
        return self.d

    def setD(self,d):
        self.d=d

    def evaluateQuery(self,query):
        """Pour renvoyer seeds 'n' Document"""
        docs = list(self.model.getRanking(query).keys())
        return docs[:self.n]#V_Q initiale le nombre de noeuds

    def addLinkToSeed(self,seeds):
        """
        :param seeds:la liste des documents seeds
        :return: une liste des documents a considere
        """
        out_in_coming=[]
        for idDoc in seeds:
            out_in_coming.extend(self.index.getHyperlinksFrom(idDoc).keys())
            doc_in=self.index.getHyperlinksTo(idDoc).keys()
            k=min(self.k,len(doc_in))
            out_in_coming.extend(sample(doc_in,k))
        return list(set(out_in_coming))

    def initAndUpdateVertex(self,query):
        V_Q=self.evaluateQuery(query)
        V_Q+=self.addLinkToSeed(V_Q)
        return V_Q

    def create_adjacency_matrix(self,selected_docs):
        """
        :param selected_docs: les documents appris
        :return: matrice de transition P et s
        """
        N=len(selected_docs) #le nombre de document pour le sous-graphe
        s=np.ones(N)/N  #a_ij uniforme pour tout les documents
        P=np.zeros((N,N)) #matrice de transition faudra prendre en compte les occurences
        self.DocToIndex=dict(enumerate(selected_docs)) #pour les indexes (index,idDoc)
        self.IndexToDoc={idDoc:index for index,idDoc in self.DocToIndex.items()} #pour les indexes (idDoc,index)

        for idDoc in selected_docs:
            indexDoc=self.IndexToDoc.get(idDoc)
            out_docs=np.array(list(self.index.getHyperlinksFrom(idDoc).items())) #qui cite idDoc ->dict (les documents , les occurences)
            if(len(out_docs)>0):
                out_docs=out_docs[np.in1d(out_docs[:,0],selected_docs)]
                normalization=np.sum(out_docs[:,1])
                for DocCite,freq in out_docs:
                    P[indexDoc,self.IndexToDoc[DocCite]]=freq/normalization
        return s,P

    def getScores(self, query):
        """s=dsP+(1−d)a"""
        selected_docs=self.initAndUpdateVertex(query)
        s_pred,P=self.create_adjacency_matrix(selected_docs)

        for _ in range(self.maxIter):
            s_succ=self.d*(np.dot(s_pred,P))+(1-self.d)*len(s_pred)
            if(np.abs(s_pred-s_succ).max()<self.epsilon):
                break
            s_pred=s_succ
        return {self.DocToIndex[idx]: score for idx, score in enumerate(s_succ)}







