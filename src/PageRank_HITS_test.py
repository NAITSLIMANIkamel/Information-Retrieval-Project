from TextRepresenter import *
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


if __name__=='__main__':
    parsed = Parser('../data/cacm/cacm.txt')
    indexer = IndexerSimple(parsed.getCollections())
    filequery = '../data/cacm/cacm.qry'
    filerelevant = '../data/cacm/cacm.rel'
    parser = QueryParser(filequery, filerelevant).getQueries()
    liste = list(Hits(indexer, n=30, k=5).getRanking(parser.get(10).getTexte()).keys())
    print('Hits liste',liste)
    liste = list(PageRank(indexer, n=30, k=5).getRanking(parser.get(10).getTexte()).keys())
    print('PageRank List ', liste)

