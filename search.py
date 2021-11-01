import numpy as np
import json
import re
import numpy as np
from src.IndexerSimple import *
from src.Document import *
import src.Parser as prs
import src.Weighter as wg
import src.IRModel as ri
import src.PageRank as pr
import src.Hits as ht
# Corpus
parser = prs.Parser('src/data/cisi/cisi.txt')
corpus = parser.getCollections()
# Index
index = IndexerSimple(corpus)

# Weighter
indexWgBool = wg.Weighter1(index)
indexWgTF = wg.Weighter2(index)
indexWgIDF = wg.Weighter3(index)
indexWgLogTf = wg.Weighter4(index)
indexWgLog = wg.Weighter5(index)
weighter_ = {
'WeighterBool':indexWgBool,
'WeighterTF':indexWgTF,
'WeighterIDF':indexWgIDF,
'WeighterLogTF':indexWgLogTf,
'WeighterLog':indexWgLog
}

# Model
model_ = {
    'Vectoriel':ri.Vectoriel,
    'OkapiBM25':ri.Okapi_BM25,
    'ModeleLangue':ri.ModeleLangue,
 }


def to_metadata(doc):
    balises = {"T":"titre","B":"date","A":"auteur","K":"mots-cle","W":"texte","X":"liens"}
    newdoc = dict({})
    for b,v in balises.items():
        newdoc[v] = doc.getValue(b)
    return newdoc

def getData(requestJson):
    opt = requestJson.get('opt')
    query = requestJson.get('query')
    return opt, query


def search(opt,query):
    model = model_.get(opt.get("model"),ri.Vectoriel)
    
    if(model.__name__=="Vectoriel"):
        print("Vectoriel")
        weig = weighter_.get(opt.get("wg"),indexWgBool)
        norm = opt.get("norm",True)
        model = model(index,weig,norm)
    elif(model.__name__=="Okapi_BM25"):
            print("Okapi_BM25")
            try:
                b = float(opt.get("b",0.75))
            except:
                b = 0.75
            try:
                k1 = float(opt.get("k1",1.2))
            except:
                k1 = 1.2
            model = model(index,k1=k1,b=b)
    elif(model.__name__=="ModeleLangue"):
                print("ModeleLangue")
                try:
                    sigma = float(opt.get("sigma",0.1))
                except:
                    sigma = 0.1
                model = model(index,sigma=sigma)
                
    _usePageRank=bool(opt.get('pageRank'))            
    if _usePageRank:
            print("page rank used")
            model=pr.PageRank(index,model=model)
            

    res = [{"id":iddoc,"scors":scors,"metadata":to_metadata(corpus.get(iddoc))}
            for iddoc,scors in model.getRanking(query).items()][:100]
    if(len(res)<1):
        res = [{"id":-1,"scors":0,"metadata":to_metadata(Document(-1))}]
        return json.loads(json.dumps({'ranking':res,'query':query,'state': 'ko'}))
    return json.loads(json.dumps({'ranking':res,'query':query,'state': 'ok'}))
    


def getPageDoc(iddoc):
    page = corpus.get(iddoc)
    if(page):
        return json.loads(json.dumps({'metadata':to_metadata(page),'query':iddoc,'state': 'ok'}))
    else:
        return json.loads(json.dumps({'metadata':to_metadata(Document(-1)),'query':iddoc,'state': 'ko'}))
