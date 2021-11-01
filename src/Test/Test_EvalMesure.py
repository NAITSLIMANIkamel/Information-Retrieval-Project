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

if __name__=='__main__':
    parsed = Parser('../data/cacm/cacm.txt')
    indexer = IndexerSimple(parsed.getCollections())
    filequery = '../data/cacm/cacm.qry'
    filerelevant = '../data/cacm/cacm.rel'
    parser = QueryParser(filequery, filerelevant).getQueries()
    liste = list(Okapi_BM25(indexer).getRanking(parser.get(10).getTexte()).keys())
    rang=20
    print(f'Rappel au rang {rang}',Rappel(rang).evalQuery(liste, parser.get(10)))
    print(f'Precision au rang {rang}', Precision(rang).evalQuery(liste, parser.get(10)))
    print(f'AvgP ', AvgP().evalQuery(liste, parser.get(10)))
    print(f'RR ', RR().evalQuery(liste, parser.get(10)))
    print(f'NDCG au Rang {rang}',NDCG(rang).evalQuery(liste, parser.get(10)))
    print(f'F_measure au Rang {rang}',F_measure(rang).evalQuery(liste, parser.get(10)))