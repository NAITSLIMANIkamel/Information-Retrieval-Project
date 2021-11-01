import re
from .Document import *


class Parser(object):

    def __init__(self, filename):
        # self.docs = Parser.buildDocCollectionSimple(filename)
        self.docs = Parser.buildDocCollection(filename)

    def getCollections(self):
        return self.docs

    def getOneDoc(self,key):
        return self.docs[key]

    @classmethod
    def buildDocumentCollectionRegexCACM(cls, filename):
        documents = dict()
        with open(filename, 'r') as f:
            line = f.read()
            reDoc = re.findall(r"\.I (.*)\n(?:\.T\n((?:[^.]*\n)*))?(?:\.W\n((?:[^.]*(?:[.][^ABCKNX])*\n*)*))?(?:\.B\n((?:[^.]*\n)*))?(?:\.A\n((?:[^.]*(?:[.][^CKNX])*\n*)*))?(?:\.K\n((?:[^.]*\n)*))?(?:\.C\n((?:[^.]*(?:[.][^NX])*\n*)*))?(?:\.N\n((?:[^.]*\n)*))?(?:\.X\n((?:[^.]*\n)*))?",line,re.MULTILINE)
            for I, T, W, B, A, K, C, N, X in reDoc:
                documents[int(I)] = Document(I, T, W,B, A, K, X)
        return documents

    @classmethod
    def buildDocCollection(cls,filename):
        docs = dict()
        with open(filename) as fp:
            textf = ' ' + fp.read()
        doc = re.split(r'\s+\.I\s+', textf)[1:]
        for d in doc:
            id, d = re.split(r'\s+',d,1)
            id = int(id)
            # l'ordre des balise est inconu
            # on remplace par .I car il n'est pas utiliser dans les metadatas
            d = re.sub(r'\s*(\.[TBAKWX])\s+',r'\n\.I 1\n\1 ', d).split("\n\.I 1\n")[1:]
            # print(d)
            doc = Document(id)
            for meta in d:
                h, val = re.split(r'\s+',meta,1)
                doc.setValue(h.replace('.',''),val)
            doc.textXtoList()
            # print(doc.getDocument())
            docs.update({id: doc})
        # print(docs)
        return docs

    @classmethod
    def buildDocCollectionSimple(cls, filename):
        docs = dict()
        with open(filename, "r") as f:
            l = f.readline()
            while (l):
                if l[:2] == ".I":
                    I = int(l[3:].strip())
                    docs[I] = Document(I)
                    l = f.readline()
                key = l[1]
                value = ""
                l = f.readline()
                while l and l[0] != '.':
                    value += l
                    l = f.readline()
                docs[I].setValue(key, value)
                if(key=='X'):
                    docs[I].textXtoList()
                print(docs[I].getDocument())
                break
        return docs



