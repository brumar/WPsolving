import operations as operations
from schemas import *
from subjectRepresentations import *
from textRepresentations import *
import copy
import uuid

KEEPZEROS=False #when writing the formula with true values, the operation containing 0 are dropped
REPLACEBYGENERICVALUES=True

class TreePaths: # contains all valuable informations on the different paths followed by the solver
    def __init__(self,updater):

        stepZero=Step(Move(RepresentationMove(0,0)))# by convention the initial state is the NULL move
        self.dicStep={stepZero.sId:0}    # id to index
        self.steps=[stepZero]
        self.initialState=updater
        self.treeOutput=""
        self.nullMoveId=self.steps[0].sId
        self.pathsCount=0
        self.initialValuesDic=updater.problem.problemInitialStaticValues
        self.pathList=[]

    def addStep(self, step):
        self.steps.append(step)
        self.dicStep[step.sId]=len(self.steps)-1
        if(step.parentId==0): # if parentId = 0 then it is a 1rst level node
            step.parentId=self.nullMoveId  # then the parent Id is set to the id of the nullMove which is by convention the initial state
        self.addChild(step.parentId,step.sId)


    def addChild(self,parentId,childId):
        indexOfStep=self.dicStep[parentId]
        parentStep=self.steps[indexOfStep]
        parentStep.childrenIds.append(childId)

    def getStep(self,sId):
        return (self.steps[self.dicStep[sId]])

    def scanTree(self,sId=0,level=0,addFormula=True): # to be use
        if sId==0:
            sId=self.nullMoveId
        firstStep=self.getStep(sId)
        childrenIds=firstStep.childrenIds
        if not childrenIds: # the tree is at its last step, we can now track back the path
            self.pathsCount+=1
            formula=self.trackBack(sId)
            if(addFormula):
                formulaLine=level*"\t"+formula+"\r\n"
                self.treeOutput+=formulaLine
        for childrenId in childrenIds:
            infos=self.getStep(childrenId).infos.shortInfo
            line=level*"\t"+infos+"\r\n"
            self.treeOutput+=line
            self.scanTree(childrenId,level+1)

    def trackBack(self,leafId,keepzeros=KEEPZEROS,replaceByGenericValues=REPLACEBYGENERICVALUES):
        infos=self.getStep(leafId).infos
        finalValue=infos.valueToFind
        operands=infos.operands
        formula=infos.objectsFormula
        problemSolved=infos.solved
        if(formula==""):
            formula=infos.newlyAssignedObject
            operands=[infos.newlyAssignedObject]
        summaryRepresentation=""
        if not((" 0 " in infos.formulaFirstPart)and(not keepzeros))and(infos.formulaFirstPart!=""): #TODO: DRY not respected here (and below)
            computedFormula=infos.formulaFirstPart
        else:
            computedFormula=" "+str(infos.valueToFind)+" "
        unknow=""
        IdCursor=leafId
        notroot=True
        while (notroot):
            if(unknow=="")or(unknow not in operands): # if the schema did not allow to find the needed operand
                if(self.getStep(IdCursor).move.type=="RepresentationMove"):
                    if(self.getStep(IdCursor).infos.newlyAssignedObject in operands):
                        summaryRepresentation=" # "+self.getStep(IdCursor).infos.shortInfo+summaryRepresentation
                IdCursor=self.getStep(IdCursor).parentId #then continue the search with the parent node
                if(IdCursor!=self.nullMoveId):
                    unknow=self.getStep(IdCursor).infos.unknow #and take its output (unknow)
                else:
                    notroot=False
            else :
                infos=self.getStep(IdCursor).infos  # if the schema allowed to find a recquired operand
                operands.remove(unknow)#we stop looking for the operand which have been found (but we keep the second one)
                operands=operands+infos.operands # and we continue the search on its own operands
                formula=formula.replace(" "+unknow+" ","( "+infos.objectsFormulaFirstPart+" )")
                if not((" 0 " in infos.formulaFirstPart)and(not keepzeros)):
                    computedFormula=computedFormula.replace(" "+str(infos.valueToFind)+" ","( "+infos.formulaFirstPart+" )")
        if(replaceByGenericValues):
            summaryRepresentation=self.replaceByGenerVal(summaryRepresentation)
            computedFormula=self.replaceByGenerVal(computedFormula)
        computedFormula=self.sanitizeFormula(computedFormula)
        formula=self.sanitizeFormula(formula)
        self.pathList.append(Path(computedFormula,formula,summaryRepresentation,finalValue,problemSolved))
        return computedFormula+" : interpretation -> "+formula

    def sanitizeFormula(self,computedFormula):
        computedFormula=computedFormula.replace(" ","")
        computedFormula=computedFormula.replace("--","+") #TODO: Mention this somewhere
        computedFormula=computedFormula.replace("+-","-")
        if(computedFormula.count("(")==1)and(computedFormula[0]=="(")and(computedFormula[-1]==")"):# we want to drop parenthesis for single expression like (T1-P1)
            computedFormula=computedFormula[1:-1]
        return computedFormula

    def replaceByGenerVal(self,computedFormula):
        for generVal in self.initialValuesDic.keys() :
            if not("-" in generVal):    # we wish to avoid -d
                val=str(self.initialValuesDic[generVal])
                if ( val in computedFormula):
                    computedFormula=computedFormula.replace(val,generVal)
        return computedFormula


class Path:
    def __init__(self,formula,objectFormula,interpretationsSummary,valueFound,problemSolved):
        self.formula=formula
        self.objectFormula=objectFormula
        self.interpretationsSummary=interpretationsSummary
        self.valueFound=valueFound
        self.problemSolved=problemSolved

class Step:
    def __init__(self,move,parentId=0,infos="",level=0):
        self.childrenIds=[]
        self.move=move
        self.parentId=parentId
        self.sId=uuid.uuid4()
        self.infos=infos
        self.level=level

    def addInfos(self,infos):
        self.infos=infos

class Solver:
    INTERP=1
    SCHEMA=2
    SOLVER=3
    def __init__(self,updater,constraints=[]):
        self.updater=updater
        self.TreePaths=TreePaths(updater) # store all the paths taken by solver
        self.constraints=constraints

    def generalSequentialSolver(self,currentStep="",updater="",level=0,listOfActions=[SOLVER]):
        currentStepId=0
        infos=""
        if(level!=0):
            currentStepId=currentStep.sId
            infos=updater.applyMove(currentStep.move,self.constraints)
            updater.updatePossibleRepresentationChange(self.constraints)
            updater.updateAppliableSchemas(self.constraints)
            infos.solved=updater.problemState.isProblemEnded()
            currentStep.addInfos(infos)
            self.TreePaths.addStep(currentStep)
        else:
            updater=copy.deepcopy(self.updater) # we init the updater
        if (not updater.problemState.isProblemEnded()):
            action=listOfActions.pop(0)
            if(action==self.SOLVER):
                listOfActions=[self.SOLVER]# when solver is found, we keep applying schemas until the end of the possibilities

            if (action==self.INTERP):
                self.interpretationSteps(updater,level,listOfActions,currentStepId)

            if(action==self.SCHEMA)or(action==self.SOLVER):
                self.schemaSteps(updater,level,listOfActions,currentStepId)

    def schemaSteps(self,updater,level,listOfActions,currentStepId):
        updater.updateAppliableSchemas(self.constraints)
        for schem in updater.appliableSchemaList:
            newstep=Step(Move(schem),currentStepId,level=level)
            self.generalSequentialSolver(newstep,copy.deepcopy(updater),level+1,copy.deepcopy(listOfActions))


    def interpretationSteps(self,updater,level,listOfActions,currentStepId):
        updater.updatePossibleRepresentationChange(self.constraints)
        moveList=updater.possibleRepresentationChangeList
        for repMove in moveList:
            newstep=Step(Move(repMove),currentStepId,level=level)
            self.generalSequentialSolver(newstep,copy.deepcopy(updater),level+1,copy.deepcopy(listOfActions))

    def addConstraint(self,constraint):
        self.constraints.append(constraint)

