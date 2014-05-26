import csv

class SimulatedDatas: # gathering and printing informations accross the different solving models
    def __init__(self):
        self.datas={}

    def addDataSet(self,pathList,problemName,solvingModel):
        formulaDic=self.createFormulaDic(pathList)
        self.createDataSet(formulaDic,problemName,solvingModel)

    def createFormulaDic(self,pathList):
        formulaDic={}
        for path in pathList:
            if path.formula not in formulaDic.keys():
                formulaDic[path.formula]=[path]
            else :
                formulaDic[path.formula].append(path)
        return formulaDic

    def createDataSet(self,formulaDic,problem,model):
        self.datas[problem,model]=[]
        for key in formulaDic:
            for path in formulaDic[key]:
                line=[key,path.problemSolved,path.objectFormula,set(path.interpretationsList)]
                if line not in self.datas[problem,model]:
                    self.datas[problem,model].append(line)
                    #print(line)
    def printLines(self):
        for problem,solvingModel in self.datas:
            for line in self.datas[problem,solvingModel]:
                print(problem,solvingModel,line)

    def printCSV(self,csvFile="datas.csv",fieldToHide=[]):
        with open(csvFile, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for problem,solvingModel in self.datas:
                for line in self.datas[problem,solvingModel]:
                    writer.writerow([problem]+[solvingModel]+line)