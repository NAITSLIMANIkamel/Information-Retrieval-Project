import numpy as np

from .IRModel import *
from .EvalIRModel import *
from .PageRank import *
from itertools import product

def train_test_split(queries,test_size=None,shuffle=True):
    queries=list(queries.copy().items())
    if(shuffle):
        np.random.shuffle(queries)
    if(test_size is None ):
        test_size=0.25
    length=int((1-test_size)*len(queries))
    Train=queries[:length]
    Test=queries[length:]
    return dict(enumerate(Train)),dict(enumerate(Test))

class GridSearch(object):
    def __init__(self,queries):
        self.queries=queries
        self.best=None

    def fit(self,model,NameMesure,mesure):
        if(isinstance(model,ModeleLangue)):
            sigmas=np.arange(0,1.1,0.1)
            res=[]
            for sigma in sigmas:
                model.setSigma(sigma)
                evaluator = EvalIRModel({'ModeleLangue':model}, {NameMesure:mesure})
                res.append(evaluator.evalQueriesWithModelAndMeasure('ModeleLangue',NameMesure,self.queries)[0])
            bestSigma,bestScore=np.argmax(res),np.max(res)
            self.best=sigmas[bestSigma]
            return sigmas[bestSigma], bestScore

        if(isinstance(model,Okapi_BM25)):
            k1=np.arange(1.2,2.1,0.1)
            b=np.arange(0.,1.1,0.1)
            iterList=[tup for tup in product(k1,b)]
            #Manque un itertools pour toute les combinaisons possible
            res=[]
            for k in k1:
                for bpa in b:
                    model.setK1(k)
                    model.setB(bpa)
                    evaluator=EvalIRModel({'Okapi_BM25':model},{NameMesure:mesure})
                    res.append(evaluator.evalQueriesWithModelAndMeasure('Okapi_BM25',NameMesure,self.queries)[0])
            bestparams,bestScore=np.argmax(res),np.max(res)
            self.best = iterList[bestparams]
            return iterList[bestparams],bestScore

        if(isinstance(model,PageRank)):
            d=np.arange(0.2,1,0.1)
            res=[]
            for dpa in d:
                model.setD(dpa)
                evaluator = EvalIRModel({'PageRank': model}, {NameMesure: mesure})
                res.append(evaluator.evalQueriesWithModelAndMeasure('PageRank', NameMesure, self.queries)[0])
            bestSigma, bestScore = np.argmax(res), np.max(res)
            self.best=d[bestSigma]
            return d[bestSigma], bestScore





