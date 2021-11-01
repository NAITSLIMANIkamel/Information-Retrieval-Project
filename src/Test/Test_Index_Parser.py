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
    indexer=IndexerSimple(parsed.getCollections())
    print('Le taille de la collection est :' , indexer.getTotalStem())
    print('getTfsForDoc :' , indexer.getTfsForDoc(12))
    print('getTfIDFsForDoc :', indexer.getTfIDFsForDoc(12))
    print('getTfsForStem :', indexer.getTfsForStem('estim'))
    print('getTfIDFsForStem :', indexer.getTfIDFsForStem('estim'))