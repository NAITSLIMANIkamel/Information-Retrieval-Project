from .EvalMesure import *
import scipy.stats as s

class EvalIRModel(object):
    def __init__(self,models,measure):
        self.models=models #Dictionnaire de modeles
        self.measure=measure #Dictionnaire de mesure


    def evalQueries(self,queries):
        res=dict.fromkeys(self.models.keys(),dict.fromkeys(self.measure.keys()))
        for nameModel,model in self.models.items():
            for nameMeasure,mesure in self.measure.items():
                result=np.array([mesure.evalQuery(list(model.getRanking(query.getTexte()).keys()), query) for query in queries.values()])
                res[nameModel][nameMeasure]=(np.mean(result),np.std(result))
        return res

    def evalQueriesWithModelAndMeasure(self,model,measure,queries):
        modelEval=self.models.get(model)
        measureEval=self.measure.get(measure)
        result=np.array([measureEval.evalQuery(list(modelEval.getRanking(query.getTexte()).keys()), query) for query in queries.values()])
        return np.mean(result),np.std(result)

    def evalQueryWithAllModel(self,measure,query):
        measureEval=self.measure.get(measure)
        result=dict()
        for nameModel,model in self.models.items():
            result[nameModel]=measureEval.evalQuery(list(model.getRanking(query.getTexte()).keys()), query)
        return result

    def evalQueryWithAllmeasure(self,model,query):
        modelEval=self.models.get(model)
        result=dict()
        for nameMeasure,measureEval in self.measure.items():
            result[nameMeasure]=measureEval.evalQuery(list(modelEval.getRanking(query.getTexte()).keys()), query)
        return result


    def t_test(self,X,Y,alpha):

        n=len(X)
        moyX=np.mean(X)
        moyY=np.mean(Y)
        varX=np.std(X)
        varY=np.std(Y)
        moyT=moyX-moyY
        varT=varX+varY
        normale = (moyT) / (np.sqrt((varT) / n))
        degFree=n-1
        student = s.t.ppf(1. - alpha , degFree)
        return normale, student, np.abs(normale) <= student






