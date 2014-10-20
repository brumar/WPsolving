'''
Created on 25 juil. 2014

@author: Nevrose
'''
import csv

class weightEvaluator():
    def __init__(self):
        self.datas={}

    def prepareStructure(self,problemBank):
        for problemName in problemBank.dicPbm.iterkeys():
            problem=problemBank.dicPbm[problemName]
            for indexInfo in range(len(problem.text.textInformations)):
                textInfo=problem.text.textInformations[indexInfo]
                for indexRepresentation in range(len(textInfo.representations)):
                    rep=textInfo.representations[indexRepresentation]
                    if(problemName not in self.datas.keys()):
                        self.datas[problemName]={}
                    if(indexInfo not in self.datas[problemName].keys()):
                        self.datas[problemName][indexInfo]={}
                    if(indexRepresentation not in self.datas[problemName][indexInfo].keys()):
                        self.datas[problemName][indexInfo][indexRepresentation]={}
                    self.datas[problemName][indexInfo][indexRepresentation]={"representation":rep,"occurences":0,"verbalDescription":"","weight":0}

    def bindConfrontationToPathsDatas(self,confrontationDic, dDic):
        #self.dicPbmSetFormulaPlannedObserved[pbm][setName][formula]=[planned,observationsCount]
        dic=confrontationDic.dicPbmSetFormulaPlannedObserved
        for problem in dic.iterkeys():
            for set in dic[problem].iterkeys():
                for formula in dic[problem][set]:
                    if dic[problem][set][formula][0]==True:
                        numberOfObservations=dic[problem][set][formula][1]
                        #print("found")
                        congruentLines=(len(dDic[problem][formula]))
                        for pathLine in dDic[problem][formula]:
                            path=pathLine["path"]
                            numberOfRepresentationUsed=len(path.interpretationsList)
                            for interpIndex in range(numberOfRepresentationUsed):
                                verbalDescription=path.interpretationsList[interpIndex]
                                textIndex=path.richInterpretationsList[interpIndex].indexTextInformation
                                repIndex=path.richInterpretationsList[interpIndex].indexSelectedRepresentation
                                #print(verbalDescription,textIndex,repIndex)
                                self.datas[problem][textIndex][repIndex]["occurences"]+=float(numberOfObservations)/congruentLines
                                #print(self.datas[problem][textIndex][repIndex]["occurences"])
                                if( self.datas[problem][textIndex][repIndex]["verbalDescription"]==""):
                                    self.datas[problem][textIndex][repIndex]["verbalDescription"]=verbalDescription

    def normaliseWeightByPbm(self):
        for pbm in self.datas:
            suma=0
            for info in self.datas[pbm]:
                for rep in self.datas[pbm][info]:
                    suma+=self.datas[pbm][info][rep]["occurences"]
            for info in self.datas[pbm]:
                for rep in self.datas[pbm][info]:
                    if(self.datas[pbm][info][rep]["verbalDescription"]!=""):
                        self.datas[pbm][info][rep]["weight"]=float(self.datas[pbm][info][rep]["occurences"])/suma
                        #=======================================================
                        # print(pbm)
                        # print(self.datas[pbm][info][rep]["verbalDescription"])
                        # print(self.datas[pbm][info][rep]["weight"])
                        #=======================================================

    def printCSV(self,csvFile="datasWeight.csv"):
            with open(csvFile, 'wb') as csvfile:
                for pbm in self.datas:
                    for info in self.datas[pbm]:
                        for rep in self.datas[pbm][info]:
                            writer = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            writer.writerow([pbm,self.datas[pbm][info][rep]["verbalDescription"],self.datas[pbm][info][rep]["weight"],self.datas[pbm][info][rep]["occurences"]])



