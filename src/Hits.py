from .IRModel import *
from random import sample
from .IndexerSimple import *

class Hits(IRModel):
    def __init__(self,index,n=50,k=10,epsilon=1e-5,max_iter=100,model=Okapi_BM25):
        super(Hits,self).__init__(index)
        self.index=index
        self.n=n
        self.k=k
        self.max_iter=max_iter
        self.model=model(index)
        self.epsilon=epsilon

    def evaluateQuery(self, query):
        """Pour renvoyer seeds 'n' Document"""
        docs = list(self.model.getRanking(query).keys())
        return docs[:self.n]  # V_Q initiale le nombre de noeuds

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

    def initAndUpdateVertex(self, query):
        V_Q = self.evaluateQuery(query)
        V_Q += self.addLinkToSeed(V_Q)
        return V_Q

    def create_adjacency_matrix(self,selected_docs):
        """

        :param selected_docs: les documents appris
        :return: matrice de transition P et s
        """
        N=len(selected_docs) #le nombre de document pour le sous-graphe
        P=np.zeros((N,N)) #matrice de transition faudra prendre en compte les occurences
        self.DocToIndex=dict(enumerate(selected_docs)) #pour les indexes (index,idDoc)
        self.IndexToDoc={idDoc:index for index,idDoc in self.DocToIndex.items()} #pour les indexes (idDoc,index)

        for idDoc in selected_docs:
            indexDoc=self.IndexToDoc.get(idDoc)
            out_docs=np.array(list(self.index.getHyperlinksFrom(idDoc).items())) #qui cite idDoc ->dict (les documents , les occurences)
            if(len(out_docs)>0):
                out_docs=out_docs[np.in1d(out_docs[:,0],selected_docs)]
                for DocCite,freq in out_docs:
                    P[indexDoc,self.IndexToDoc[DocCite]]=freq
        return P

    def getScores(self, query):
        selected_docs = self.initAndUpdateVertex(query)
        P = self.create_adjacency_matrix(selected_docs)
        N=len(P)
        authority_pred = np.ones(N)
        hub_pred  = np.ones(N)
        for _ in range(self.max_iter):
            authority_suc=np.dot(P.T,hub_pred)
            hub_suc=np.dot(P,authority_pred)
            authority_suc/=np.linalg.norm(authority_suc,2)
            hub_suc /= np.linalg.norm(hub_suc, 2)
            if (np.abs(authority_pred - authority_suc).max() < self.epsilon):
                break
            authority_pred = authority_suc
            hub_pred=hub_suc
        return {self.DocToIndex[idx]: score for idx, score in enumerate(authority_pred)}






