from lib.paths import *
from lib.optionsFactory import *
from lib.observations import *
from lib.constraints  import *
import logging
import pickle


class ReinterpretationModel(): # gathering and printing informations accross the different solving models
    def __init__(self,numberOfReinterpretation=1,dropToTest=False,breakPreviousInterpretations="undefined",excludeLateReinterpretations=False):
        self.datas=[] #list of dictionnaries (selected datas)
        self.datasBrut=[] #list of dictionnaries (all the datas)
        self.datasDic={} # composite dictionnary to get better access to datas
        self.seenLinesDatas=[]
        self.seenLinesDatasBrut=[]
        self.maxNumberOfReinterpretation=numberOfReinterpretation
        self.dropToTest=dropToTest
        self.breakPreviousInterpretations=breakPreviousInterpretations
        self.excludeLateReinterpretations=excludeLateReinterpretations

    def pickleSave(self,src):
        output = open(src, 'wb')
        pickle.dump([self.datas,self.datasBrut], output)

    def pickleLoad(self,src):
        pkl_file = open(src, 'rb')
        loadedPickle=pickle.load(pkl_file)
        if(len(loadedPickle)==2):
            self.datas=loadedPickle[0]
            self.datasBrut=loadedPickle[1]
        else:
            self.datas=loadedPickle #to be retrocompatible

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
                    #logging.info(line)

    def printLines(self):
        for problem,solvingModel in self.datas:
            for line in self.datas[problem,solvingModel]:
                logging.info(problem,solvingModel,line)

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
        dicPbmSetFormula=self.extractPredictions()
        self.printMyDic(dicPbmSetFormula, csvFile)

    def printMyDic(self, dic, filename):
        with open(filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for problem in dic.iterkeys():
                l=list(dic[problem])
                l.sort()
                l.sort(lambda x,y: cmp(len(x), len(y) ) )
                writer.writerow([problem]+l)


    def extractPredictions(self,excludeUnsolvingProcesses=False):
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

    def findFormulas(self,models):
        dicPbmForms={}
        for pbm in self.datasDic.keys():
            forms=[]
            for data in self.datasBrut:
                if(data["problem"]==pbm):
                    f=data["path"].formula
                    if(data["model"]in models) and (f not in forms ):
                        forms.append(f)
            dicPbmForms[pbm]=forms
        return dicPbmForms


    def printDatas(self):
        for data in self.datas:
            path=data["path"]
            logging.info(path.formula)

    def createSteps(self): # TODO: This is lazy as hell
        if(self.maxNumberOfReinterpretation==1):
            return [Solver.INTERP,Solver.SCHEMA,Solver.SCHEMA,Solver.SCHEMA]
        elif(self.maxNumberOfReinterpretation==2):
            return [Solver.INTERP,Solver.INTERP,Solver.SCHEMA,Solver.SCHEMA,Solver.SCHEMA]
        else:
            raise Exception("maxNumberOfReinterpretation too high")

    def generateAllPossibilities(self,problem):
        """ The main function of this program, generate all the paths possible for a problem
        Some options have to be apparent in new development.
        The option "breakPreviousInterpretations" is set at True AND False
        by the optionsFactory script. New developpments should
        to find as much as paths as possible.
        """
        unorderedSteps=self.createSteps()
        logging.info(problem.name)
        c1=StepConstraint(lambda info: (info.valueToFind>0)or("MINUS" in info.unknow) , "avoid negative values, except for comparisons")
        c2=StepConstraint(lambda info: (info.valueToFind!=0), "avoid null value")
        alter_c1=AlterStepConstraint()
        c_controller=ConstraintsController([c1,c2],[alter_c1])
        upD=Updater(problem)
        upD.attachConstraintController(c_controller)
        upD.startAsUnderstood()
        # we add the model of goodAnswers, we want to be able to
        # keep them for later
        model="goodAnswers"
        solver=Solver(upD)
        solver.generalSequentialSolver(listOfActions=[Solver.SOLVER]) # = just solve
        solver.TreePaths.scanTree()
        #logging.info(solver.TreePaths.treeOutput)
        self.addDataSet(solver.TreePaths.pathList,problem.name,model)
        nbDiscoveries=str(len(solver.TreePaths.pathList))
        logging.info("DONE : model "+model)
        logging.info("Number of paths found : "+nbDiscoveries)

        optionsList=optionsFactory(unorderedSteps) # will generate all the options possible with 2 interpretations step randomly occuring
        for i,options in enumerate(optionsList) :
            if (not self.dropToTest) or (i%3==0): # [condition for debugging purpose]
                                            # if dropToTest is True, then only 1 third of the possibilities generated by optionsFactory will be investigated
                model=str(options[0])
                upD.constraintController.breakPreviousInterpretation=options[1]
                solver=Solver(upD)
                solver.generalSequentialSolver(listOfActions=options[0])
                solver.TreePaths.scanTree()
                #logging.info(solver.TreePaths.treeOutput)
                self.addDataSet(solver.TreePaths.pathList,problem.name,model)
                logging.info("DONE : model "+model+"( "+str(i)+" )")
                nbDiscoveries=str(len(solver.TreePaths.pathList))
                logging.info("Number of paths found : "+nbDiscoveries)
                if(self.excludeLateReinterpretations):
                    # a bit dirty, the idea is that optionsFactory first element is specifically
                    # the sole element to be tested when excludeLateReinterpretations
                    break



