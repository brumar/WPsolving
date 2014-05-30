import csv

class SimulatedDatas: # gathering and printing informations accross the different solving models
    def __init__(self):
        self.datas=[] #list of dictionnaries
        self.seenLines=[]

    def addDataSet(self,pathList,problemName,solvingModel,reducePaths=True):
        for path in pathList:
            data={}
            add=True
            if (reducePaths):
                curLine=[problemName,path.problemSolved,path.formula,path.objectFormula,set(path.interpretationsList)]
                if (curLine not in self.seenLines):
                    self.seenLines.append(curLine)
                else:
                    add=False
            if(add):
                print(path.formula)
                data["problem"]=problemName
                data["model"]=solvingModel
                data["path"]=path
                self.datas.append(data)

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

    def printCSV(self,csvFile="datas.csv",hideModel=True,hideUnsolved=True,printIndex=True):
        dataSeen=[]
        with open(csvFile, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for data in self.datas:
                path=data["path"]
                if not(hideUnsolved and not path.problemSolved):
                    if(hideModel):
                        line=[path.index,path.formula,path.problemSolved,path.objectFormula,path.interpretationsList]
                        writer.writerow([data["problem"]]+line)
                    else:
                        line=[path.index,path.problemSolved,path.objectFormula,path.interpretationsList]
                        writer.writerow([data["problem"]]+[data["model"]]+line)

    def printDatas(self):
        for data in self.datas:
            path=data["path"]
            print(path.formula)



