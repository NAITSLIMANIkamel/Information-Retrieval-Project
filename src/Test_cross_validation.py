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
from PageRank import *
from Hits import *
from Cross_Validation import *

if __name__=='__main__':
    parsed = Parser('../data/cacm/cacm.txt')
    indexer = IndexerSimple(parsed.getCollections())
    filequery = '../data/cacm/cacm.qry'
    filerelevant = '../data/cacm/cacm.rel'
    parser = QueryParser(filequery, filerelevant).getQueries()
    dicoModel = {'Vectoriel': Vectoriel(indexer, Weighter4(indexer)), 'ModeleLangue': ModeleLangue(indexer), \
                 'Okapi_BM25': Okapi_BM25(indexer), 'PageRank': PageRank(indexer)}
    rang = 20
    dicoMeasure = {'Precision': Precision(rang), 'Rappel': Rappel(rang), 'F_Mesure': F_measure(rang), 'AvgP': AvgP(),
                   'RR': RR(), 'NDCG': NDCG(rang)}
    evaluator = EvalIRModel(dicoModel, dicoMeasure)
    cv=Cross_Validation(parser,10,Okapi_BM25(indexer),evaluator)

    print(cv.crossValidate())