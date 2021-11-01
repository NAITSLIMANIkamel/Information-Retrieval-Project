from TextRepresentre import *
from Porter import *
from Parser import *
from Document import *
from EvalIRModel import *
from IndexerSimple import *
from Weighter import *
from IRModel import *
from QueryParser import *
from EvalMesure import *
from Query import *
from collections import Counter
import pickle
from GridSearch import *
from PageRank import *


def saveindexes(dataset, filename):
    with open('../data/' + dataset + '.pkl', 'wb') as output:  # Overwrites any existing file.
        parser = Parser(filename+'.txt')
        queries = QueryParser(filename + '.qry', filename + '.rel').getQueries()
        index = IndexerSimple(parser.getCollections())
        pickle.dump({"Documents": parser.getCollections(), "Queries": queries, "Index": index}, output, pickle.HIGHEST_PROTOCOL)

def save():
        saveindexes('cacm', '../data/cacm/cacm')
        saveindexes('cisi', '../data/cisi/cisi')

def load(instruction):
    dicoCACM=pickle.load(open("../data/cacm.pkl", "rb"))
    dicoCISI=pickle.load(open("../data/cisi.pkl", "rb"))
    if(instruction=='cacm'):
        return dicoCACM
    if (instruction == 'cisi'):
        return dicoCISI


if __name__=='__main__':
    dico=load('cacm')
    document,queries,index=dico.get('Documents'),dico.get('Queries'),dico.get('Indexes')
    dicoModel={'Vectoriel':Vectoriel(index,Weighter4(index)),'ModeleLangue':ModeleLangue(index),\
               'Okapi_BM25':Okapi_BM25(index),'PageRank':PageRank(index)}
    rang=20
    dicoMeasure={'Precision':Precision(rang),'Rappel':Rappel(rang),'F_Mesure':F_measure(rang),'AvgP':AvgP(),'RR':RR(),'NDCG':NDCG(rang)}
    evaluator=EvalIRModel(dicoModel,dicoMeasure)
    print(evaluator.evalQueries(queries))
    train,test=train_test_split(queries,test_size=0.8)
    gd=GridSearch(train)
    print(gd.fit(Okapi_BM25(index),'AvgP',AvgP()))


