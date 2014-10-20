import csv

class SimulationAprioriEmpiricbinderDic():
    def __init__(self,dicPbmSetFormula,globalobservationDic):
        self.dicPbmSetFormulaPlannedObserved=dicPbmSetFormula.dicPbmSetFormulaPlanned
        for pbm in  self.dicPbmSetFormulaPlannedObserved.iterkeys():
            observationDic=globalobservationDic.problemDic[pbm]
            for setName in  self.dicPbmSetFormulaPlannedObserved[pbm].iterkeys():
                for formula in  self.dicPbmSetFormulaPlannedObserved[pbm][setName].iterkeys():
                    observationsCount=0
                    if(formula in observationDic.keys() ):
                        observationsCount=observationDic[formula]
                    planned=self.dicPbmSetFormulaPlannedObserved[pbm][setName][formula]
                    self.dicPbmSetFormulaPlannedObserved[pbm][setName][formula]=[planned,observationsCount]

    def listAndCompare(self,dicPbmSetFormula,observationDic):
        """
        Not mandatory for analysis, does not involve changes in
        SimulationAprioriEmpiricbinderDic instance.

        Check the formulas which are not in the a priori set but in the
        simulation set. This designed for debugging purpose but also to count the number
        of errors that are not in our scope.
        """
        for pbm in  self.dicPbmSetFormulaPlannedObserved.iterkeys():
            print(pbm)
            for formula in observationDic.problemDic[pbm].keys():
                booli=False
                for setName in  self.dicPbmSetFormulaPlannedObserved[pbm].iterkeys():
                    if( formula in  self.dicPbmSetFormulaPlannedObserved[pbm][setName].iterkeys()):
                        booli=True
                if not booli:
                    formulaToBePrinted=formula
                    if (formula=="")or(formula==" ")or(formula=="Neant"):
                        formulaToBePrinted="No Answer"
                    print(formulaToBePrinted+" : "+str(observationDic.problemDic[pbm][formula])+" occurences")

    def printCSV(self,filename):
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for pbm in  self.dicPbmSetFormulaPlannedObserved.iterkeys():
                for setName in  self.dicPbmSetFormulaPlannedObserved[pbm].iterkeys():
                    for formula in  self.dicPbmSetFormulaPlannedObserved[pbm][setName].iterkeys():
                        planned = self.dicPbmSetFormulaPlannedObserved[pbm][setName][formula][0]
                        observationsCount = self.dicPbmSetFormulaPlannedObserved[pbm][setName][formula][1]
                        writer.writerow([pbm]+[setName]+[formula]+[planned]+[observationsCount])



class globalEmpiricalDic():
    def __init__(self):
        self.problemDic={}

    def readCsv(self,filename):
        with open(filename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in spamreader:
                problem=row[0]
                formula=row[1]
                self.addElement(problem,formula)

    def addElement(self,problem,formula):
        if problem not in self.problemDic.keys():
            self.problemDic[problem]={}
        if formula not in self.problemDic[problem].keys():
            self.problemDic[problem][formula]=1
        else:
            self.problemDic[problem][formula]+=1


class problemEmpiricalDic():
    def __init__(self,dic):
        self.ObservationsDic=dic

