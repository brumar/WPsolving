#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import logging
import re

class predictionsManager():
    """
    bind datas from simulations and from apriori generators
    tell if a formula is found or not in the simulations
    """
    def __init__(self):
        self.dicPbmSetFormulaPredicted={}
        self.dataTable=[]

    def addPredictionsSpace(self,globalAprioriDic):
        for pbm in globalAprioriDic.problemDic.iterkeys():
            aprioriDic=globalAprioriDic.problemDic[pbm]
            self.dicPbmSetFormulaPredicted[pbm]={}
            for formula in aprioriDic.formulaTosetDic.iterkeys():
                setName=aprioriDic.formulaTosetDic[formula]
                if setName not in self.dicPbmSetFormulaPredicted[pbm].keys():
                    self.dicPbmSetFormulaPredicted[pbm][setName]={}
                self.dicPbmSetFormulaPredicted[pbm][setName][formula]=[]

    def addModelPredictions(self,predictions,modelName="untitledModel"):
        for pbm,setName,formula in self.walk():
            predicted=False
            if(formula in predictions[pbm]):
                predicted=True
            self.dicPbmSetFormulaPredicted[pbm][setName][formula].append((modelName,predicted))

    def walk(self):
        for pbm in self.dicPbmSetFormulaPredicted.iterkeys():
            for setName in self.dicPbmSetFormulaPredicted[pbm].iterkeys():
                for formula in self.dicPbmSetFormulaPredicted[pbm][setName].iterkeys():
                    yield pbm,setName,formula

    def addEmpiricalDatas(self,empirDatas):
        for pbm,setName,formula in self.walk():
            occurences=0
            if formula in empirDatas.problemDic[pbm].keys():
                occurences=empirDatas.problemDic[pbm][formula]
            self.dicPbmSetFormulaPredicted[pbm][setName][formula].append(("occurrences",occurences))

    #===========================================================================
    # def printCSV(self,filename,formulasToExclude={}):
    #     noExclusion=(len(formulasToExclude.keys())==0)
    #     with open(filename, 'wb') as csvfile:
    #         writer = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #         writer.writerow(["problem"]+["set"]+["formula"]+["selected"]+["occurrences"])
    #         for pbm,setName,formula in self.walk():
    #                 #writer.writerow([pbm]+[setName]+[formula]+[planned]+[observationsCount])
    #===========================================================================

    def printCSVModelComparison(self,filename,formulasToExclude={}):
        self.createPrintableTable(formulasToExclude)
        self.printCSV(filename)

    def printCSV(self,filename):
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in self.dataTable:
                writer.writerow(row)

    def createPrintableTable(self,formulasToExclude):
        noExclusion=(len(formulasToExclude.keys())==0)
        firstIteration=True
        firstrow=["pbm","set","formula"]
        for pbm,setName,formula in self.walk():
            if noExclusion or (formula not in formulasToExclude[pbm]):
                line=[pbm,setName,formula]
                for model in self.dicPbmSetFormulaPredicted[pbm][setName][formula]:
                    name=model[0]
                    value=model[1]
                    line.append(value)
                    if(firstIteration):
                        firstrow.append(name)
                firstIteration=False
                self.dataTable.append(line)
        self.dataTable.insert(0, firstrow)

    def listAndCompare(self,obsdic):
        """
        Not mandatory for analysis, does not involve changes in
        predictionsManager instance.

        Check the formulas which are not in the a priori set but in the
        simulation set. This designed for debugging purpose but also to count the number
        of errors that are not in our scope.
        """
        noAnsSum=0
        ininterpSum=0
        resteSum=0
        for pbm in  self.dicPbmSetFormulaPredicted.iterkeys():
            logging.info(pbm)
            for formula in obsdic.problemDic[pbm].keys():
                booli=False
                for setName in  self.dicPbmSetFormulaPredicted[pbm].iterkeys():
                    if( formula in  self.dicPbmSetFormulaPredicted[pbm][setName].iterkeys()):
                        booli=True
                if not booli:
                    formulaToBePrinted=formula
                    if (formula=="")or(formula=="aucun calcul")or(formula==" ")or((formula.find("ant")!=-1)):
                        formulaToBePrinted="Pas_de_rep"
                        noAnsSum+=obsdic.problemDic[pbm][formula]
                    elif(formula.find("interp")!=-1):
                        ininterpSum+=obsdic.problemDic[pbm][formula]
                        formulaToBePrinted="Ininterp"
                    else:
                        resteSum+=obsdic.problemDic[pbm][formula]
                    logging.info(formulaToBePrinted+" : "+str(obsdic.problemDic[pbm][formula])+" occurences")
        logging.info("somme des absences de réponses : "+str(noAnsSum))
        logging.info("somme des ininterpretables : "+str(ininterpSum))
        logging.info("somme des autres : "+str(resteSum))



class globalEmpiricalDic():
    def __init__(self):
        self.problemDic={}

    def readCsv(self,filename,recodeOneliner=False):
        """
        read datas
        recodeOneliner allows the integration of formulas like T1+P1-d which
        signals that the student solved like that 5+8=13-2=12 or like that 5+8-2=12
        """
        with open(filename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in spamreader:
                problem=row[0]
                if(recodeOneliner):
                    formula=self.recode(row[1])
                else:
                    formula=row[1]
                self.addElement(problem,formula)

    def addElement(self,problem,formula):
        if problem not in self.problemDic.keys():
            self.problemDic[problem]={}
        if formula not in self.problemDic[problem].keys():
            self.problemDic[problem][formula]=1
        else:
            self.problemDic[problem][formula]+=1

    def recode(self,stri):
        NbOp=len(re.findall("[-+]",stri))
        NbPar=len(re.findall("[\(\)]",stri))
        if(NbOp==2 and NbPar==0):
            for i,m in enumerate(re.finditer(r"[-+]", "T1+P1-d")):
                if(i==0):
                    continue
                pos=m.start()
                stri="("+stri[:pos]+")"+stri[pos:]
        return(stri)

class problemEmpiricalDic():
    def __init__(self,dic):
        self.ObservationsDic=dic

if __name__ == "__main__":
    obsdic=globalEmpiricalDic()
    obsdic.readCsv("../mergedDatas_final_separated_recoded.csv",recodeOneliner=True)
    print(obsdic)

