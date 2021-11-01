import re
from .Query import *
class QueryParser(object):

    def __init__(self,filequery,fileRel):
        self.queries=self.buildCollectionSimple(filequery,fileRel)

    def buildCollectionSimple(self,filequery,fileRel):
        queries=dict()
        with open(filequery,'r') as file:
            line=file.readline()
            while line:
                if (line[:2] == '.I'):
                    idReq = int(line[3:].strip())
                line = file.readline()
                Texte = ''
                if (line[:2] == '.W'):
                    line = file.readline()
                    while line and line[0] != '.':
                        Texte += line
                        line = file.readline()
                    queries[idReq]=Query(idReq,texte=Texte)
        self.getRelevantDocs(queries,fileRel)
        return queries


    def getRelevantDocs(self,queries,fileRel):
        with open(fileRel,'r') as file:
            line = file.readline()
            while line:
                res=line.split()
                if(len(res)>0):
                    queries[int(res[0])].appendPertiDoc(int(res[1]))
                line = file.readline()

    def getQueries(self):
        return self.queries


