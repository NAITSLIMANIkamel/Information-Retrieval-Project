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
    weighters = Weighter4(indexer)
    porter = PorterStemmer()
    query=" A Formal Semantics for Computer Languages and its Application In a Compiler-Compiler"
    print('Should return document 1496 , Le texte correspond .I 1496 dans le cacm.txt')
    print('Avec le Vectoriel:',list(Vectoriel(indexer, weighters).getRanking(query).keys())[0])
    print('Avec le Model de Langue',list(ModeleLangue(indexer).getRanking(query).keys())[0])
    print('Avec le Okapi_BM25',list(Okapi_BM25(indexer).getRanking(query).keys())[0])