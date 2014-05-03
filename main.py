# -*- coding: cp1252 -*-
import lib.operations as operations
from lib.schemas import *
from lib.subjectRepresentations import *
from lib.textRepresentations import *
import copy
import uuid
import csv

KEEPZEROS=False #when writing the formula with true values, the operation containing 0 are dropped
REPLACEBYGENERICVALUES=True

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
				line=[key,path.objectFormula,path.interpretationsSummary]
				if line not in self.datas[problem,model]:
					self.datas[problem,model].append(line)
					print(line)

	def printCSV(self):
		with open('datas.csv', 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for problem,solvingModel in self.datas:
				for line in self.datas[problem,solvingModel]:
					writer.writerow([problem]+[solvingModel]+line)



class TreePaths: # contains all valuable informations on the different paths followed by the solver
	def __init__(self,updater):

		stepZero=Step(Move(RepresentationMove(0,0)))# by convention the initial state is the NULL move
		self.dicStep={stepZero.sId:0}	# id to index
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
		summaryRepresentation=""
		if not((" 0 " in infos.formulaFirstPart)and(not keepzeros)): #TODO: DRY not respected here (and below)
			computedFormula=infos.formulaFirstPart
		else:
			computedFormula=" "+str(infos.valueToFind)+" "
		unknow=""
		IdCursor=leafId
		notroot=True
		while (notroot):
			if(unknow=="")or(unknow not in operands): # if the schema did not allow to find the needed operand
				IdCursor=self.getStep(IdCursor).parentId #then continue the search with the parent node
				if(IdCursor!=self.nullMoveId):
					unknow=self.getStep(IdCursor).infos.unknow #and take its output (unknow)
					if(self.getStep(IdCursor).move.type=="RepresentationMove"):
						summaryRepresentation=summaryRepresentation+"## At step "+str(self.getStep(IdCursor).level)+" : "+self.getStep(IdCursor).infos.shortInfo
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
			computedFormula=self.replaceByGenerVal(computedFormula)
		computedFormula=self.sanitizeFormula(computedFormula)
		formula=self.sanitizeFormula(formula)
		self.pathList.append(Path(computedFormula,formula,summaryRepresentation,finalValue))#TODO: interpSteps, also avoid extern parenthesis like (T1-d) instead T1-d
		return computedFormula+" : interpretation -> "+formula

	def sanitizeFormula(self,computedFormula):
		computedFormula=computedFormula.replace(" ","")
		computedFormula=computedFormula.replace("--","+") #TODO: Mention this somewhere
		if(computedFormula.count("(")==1)and(computedFormula[0]=="(")and(computedFormula[-1]==")"):# we want to drop parenthesis for single expression like (T1-P1)
			computedFormula=computedFormula[1:-1]
		return computedFormula

	def replaceByGenerVal(self,computedFormula):
		for generVal in self.initialValuesDic.keys() :
			if not("-" in generVal):	# we wish to avoid -d
				val=str(self.initialValuesDic[generVal])
				if ( val in computedFormula):
					computedFormula=computedFormula.replace(val,generVal)
		return computedFormula


class Path:
	def __init__(self,formula,objectFormula,interpretationsSummary,valueFound):
		self.formula=formula
		self.objectFormula=objectFormula
		self.interpretationsSummary=interpretationsSummary
		self.valueFound=valueFound

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
			updater.updateAppliableSchemas(self.constraints)
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
		self.updater.updatePossibleRepresentationChange(self.constraints)
		moveList=self.updater.possibleRepresentationChangeList
		for repMove in moveList:
			newstep=Step(Move(repMove),currentStepId,level=level)
			self.generalSequentialSolver(newstep,copy.deepcopy(updater),level+1,copy.deepcopy(listOfActions))

	def addConstraint(self,constraint):
		self.constraints.append(constraint)


schema1=Schema("PoissonEF","PoissonEI",operations.addition,"PoissonGAIN","change")
schema2=Schema("ViandeEF","ViandeEI",operations.addition,"ViandeGAIN","change")
struct=ProblemStructure()
struct.addSchema(schema1)
struct.addSchema(schema2)
struct.addBridgingSchemas(schema1,schema2)
struct.updateObjectList()

text=Text()
text.addTextInformation(TextInformation(Representation(Quantity("PoissonGAIN","P1"),'Au supermarché, le kilo de poisson a augmenté de 5 euros cette année')))
text.addTextInformation(TextInformation(Representation(Quantity("PoissonEF","T1"),'Un kilo de poisson coute maintenant 12 euros.')))
text.addTextInformation(TextInformation(Representation(Quantity("PoissonEIminusViandeEI","dEI"),'Au début de l\'année, le kilo de viande coutait le même prix que le kilo de poisson.')))
text.addTextInformation(TextInformation(Representation(Quantity("PoissonGAINminusViandeGAIN","d"),'Le kilo de viande a augmenté de 3 euros de moins que le kilo de poisson')))
text.setGoal(TextGoal(Goal('ViandeEF','Combien coute le kilo de viande maintenant?')))

text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEI","P1"),'Au supermarché, le kilo de poisson était de 5 euros'))
text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEF","P1"),'Au supermarché, le kilo de poisson coute 5 euros'))
text.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("PoissonEI","T1"),'Un kilo de poisson était de 12 euros.'))
text.getTextInformation(2).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","dEI"),'Au la fin de l\'année, le kilo de viande coute le même prix que le kilo de poisson.'))
text.getTextInformation(2).addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","dEI"),'Le kilo de viande a augmenté du même prix que le kilo de poisson.'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonGAIN","d"),'Le kilo de viande a augmenté de 3 euros'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonGAIN","-d"),'Le kilo de viande a diminué de 3 euros'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","d"),'Le kilo de viande a augmenté de 3 euros'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeEF","d"),'Le kilo coute 3 euros à la fin'))
probleme1=Problem(struct,text)
probleme1.setInitialValues({"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3})


simulatedDatas=SimulatedDatas()

upD=Updater(probleme1)
upD.startAsUnderstood()

solver=Solver(upD)
solver.addConstraint(IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0))
solver.addConstraint(BehavioralConstraint(breakTheOldOne=True))
solver.generalSequentialSolver(listOfActions=[solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4p","Solve")

solver=Solver(upD)
solver.addConstraint(IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0))
solver.addConstraint(BehavioralConstraint(breakTheOldOne=True))
solver.generalSequentialSolver(listOfActions=[solver.INTERP, solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4p","Int+Solve_BREAK")

solver=Solver(upD)
solver.addConstraint(IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0))
solver.addConstraint(BehavioralConstraint(breakTheOldOne=True))
solver.generalSequentialSolver(listOfActions=[solver.INTERP,solver.SCHEMA,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4p","Int+Schem+Int+Solve_BREAK")

solver=Solver(upD)
solver.addConstraint(IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0)) #TODO: changer le equal
solver.addConstraint(BehavioralConstraint(breakTheOldOne=True))
solver.generalSequentialSolver(listOfActions=[solver.INTERP,solver.INTERP,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4p","Int+Int+Solve_BREAK")

solver=Solver(upD)
solver.addConstraint(IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0))
solver.addConstraint(BehavioralConstraint(breakTheOldOne=False))
solver.generalSequentialSolver(listOfActions=[solver.INTERP, solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4p","Int+Solve_NOBREAK")

solver=Solver(upD)
solver.addConstraint(IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0))
solver.addConstraint(BehavioralConstraint(breakTheOldOne=False))
solver.generalSequentialSolver(listOfActions=[solver.INTERP,solver.SCHEMA,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4p","Int+Schem+Int+Solve_NOBREAK")

solver=Solver(upD)
solver.addConstraint(IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0)) #TODO: changer le equal
solver.addConstraint(BehavioralConstraint(breakTheOldOne=False))
solver.generalSequentialSolver(listOfActions=[solver.INTERP,solver.INTERP,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4p","Int+Int+Solve_NOBREAK")

simulatedDatas.printCSV()

print(solver.TreePaths.treeOutput)
print(solver.TreePaths.pathsCount)


