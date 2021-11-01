import numpy as np

from .EvalMesure import AvgP
from .IRModel import Okapi_BM25, ModeleLangue
from .PageRank import *

class Cross_Validation(object):

    def __init__(self,queries,n_splits,model,evaluator):
        self.queries=queries
        self.n_splits=n_splits
        self.model=model
        self.evaluator=evaluator

    def train_test_split(self):
        """

        :param queries: Dict
        :return: les splits de taille k sous forme d'un générateur
        """
        indices = np.arange(len(self.queries))
        for test_index in self.test_masks():
            train_index = indices[np.logical_not(test_index)]
            test_index = indices[test_index]
            yield train_index, test_index

    def test_masks(self):
        for test_index in self.test_indices():
            test_mask = np.zeros(len(self.queries), dtype=bool)
            test_mask[test_index] = True
            yield test_mask

    def test_indices(self):
        n_samples = len(self.queries)
        indices = np.arange(n_samples)
        n_splits = self.n_splits
        fold_sizes = np.full(n_splits, n_samples // n_splits, dtype=int)
        fold_sizes[:n_samples % n_splits] += 1
        current = 0
        for fold_size in fold_sizes:
            print('Current Batch query:',current)
            start, stop = current, current + fold_size
            yield indices[start:stop]
            current = stop

    def crossValidate(self):
        queries=np.array(list(self.queries.values()))
        resTrain,resTest=[],[]
        for train_index, test_index in self.train_test_split():
            train=queries[train_index]
            test=queries[test_index]
            moy1=self.evalQueries(train,True)
            moy2=self.evalQueries(test,False)
            resTrain.append(moy1)
            resTest.append(moy2)
        return np.mean(resTrain),np.mean(resTest)

    def evalQueries(self,splited,split_train):
        if isinstance(self.model,Okapi_BM25):
            if(split_train):
                self.model.setB(self.model.getB()+0.1)
                self.model.setK1(self.model.getK1()+0.1)
            res=[]
            for query in splited:
                res.append(AvgP().evalQuery(self.model.getRanking(query.getTexte()),query))
            return np.mean(res)

        if (isinstance(self.model,ModeleLangue)):
            if (split_train):
                self.model.setSigma(self.model.getSigma()+0.1)
            res=[]
            for query in splited:
                res.append(AvgP().evalQuery(self.model.getRanking(query.getTexte()),query))
            return np.mean(res)

        if (isinstance(self.model, PageRank)):
            if (split_train):
                self.model.setD(self.model.getD()+0.1)
            res = []
            for query in splited:
                res.append(AvgP().evalQuery(self.model.getRanking(query.getTexte()),query))
            return np.mean(res)