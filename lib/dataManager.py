import csv
import pickle

class SimulatedDatas: # gathering and printing informations accross the different solving models
    def __init__(self):
        self.datas=[] #list of dictionnaries (selected datas)
        self.datasBrut=[] #list of dictionnaries (all the datas)
        self.datasDic={} # composite dictionnary to get better access to datas
        self.seenLinesDatas=[]
        self.seenLinesDatasBrut=[]

    def pickleSave(self,src):
        output = open(src, 'wb')
        pickle.dump(self.datas, output)

    def pickleLoad(self,src):
        pkl_file = open(src, 'rb')
        self.datas=pickle.load(pkl_file)

    def addDataSet(self,pathList,problemName,solvingModel):
        for path in pathList:
            data={}
            data["problem"]=problemName
            data["model"]=solvingModel
            data["path"]=path

            curLineDatas=[problemName,path.problemSolved,path.formula,path.objectFormula,set(path.interpretationsList)]
            if (curLineDatas not in self.seenLinesDatas): # We add datas only when the path is new (formula + reintepretations used)
                self.seenLinesDatas.append(curLineDatas)
                self.datas.append(data)

            curLineDatasBrut=[solvingModel,problemName,path.problemSolved,path.formula,path.objectFormula,set(path.interpretationsList)]
            # same as curLineDatas but with solvingModel taken into account
            if (curLineDatasBrut not in self.seenLinesDatasBrut):
                self.seenLinesDatasBrut.append(curLineDatasBrut)
                self.datasBrut.append(data)

    def createFormulaDic(self,pathList): # unused !
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
        if(hideModel):
            dataToWorkWith=self.datas
        else:
            dataToWorkWith=self.datasBrut
        with open(csvFile, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for data in dataToWorkWith:
                path=data["path"]
                if not(hideUnsolved and not path.problemSolved):
                    line=[path.index,path.formula,path.problemSolved,path.objectFormula,path.interpretationsList]
                    if(hideModel):
                        writer.writerow([data["problem"]]+line)
                    else:
                        writer.writerow([data["problem"]]+[data["model"]]+line)

    def printMiniCSV(self, csvFile="minidatas.csv"):
        dicPbmSetFormula=self.buildMiniDic()
        self.printMyDic(dicPbmSetFormula, csvFile)

    def printMyDic(self, dic, filename):
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for problem in dic.iterkeys():
                l=list(dic[problem])
                l.sort()
                l.sort(lambda x,y: cmp(len(x), len(y) ) )
                writer.writerow([problem]+l)


    def buildMiniDic(self,excludeUnsolvingProcesses=False):
        dicPbmSetFormula={}
        for data in self.datas:
            path=data["path"]
            if not(excludeUnsolvingProcesses and not path.problemSolved):
                pbm=data["problem"]
                if(pbm not in dicPbmSetFormula.keys()):
                    dicPbmSetFormula[pbm]=set()
                dicPbmSetFormula[pbm].add(data["path"].formula)
        return dicPbmSetFormula

    def buildBigDic(self,excludeUnsolvingProcesses=False):
        self.datasDic={}
        for data in self.datas:
            path=data["path"]
            if not(excludeUnsolvingProcesses and not path.problemSolved):
                pbm=data["problem"]
                formula=data["path"].formula
                if(pbm not in self.datasDic.keys()):
                    self.datasDic[pbm]={}
                if (formula not in self.datasDic[pbm].keys() ):
                    self.datasDic[pbm][formula]=[]
                self.datasDic[pbm][formula].append({"path":data["path"],"model":data["model"]})
        return self.datasDic

    def printDatas(self):
        for data in self.datas:
            path=data["path"]
            print(path.formula)



