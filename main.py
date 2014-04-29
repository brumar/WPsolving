# -*- coding: cp1252 -*-
import lib.operations as operations
from lib.schemas import *
from lib.subjectRepresentations import *
from lib.textRepresentations import *
import copy
import uuid


class TreePaths:
	def __init__(self,updater):

		stepZero=Step(Move(RepresentationMove(0,0)))# by convention the initial state is the NULL move
		self.dicStep={stepZero.sId:0}	# id to index
		self.steps=[stepZero]
		self.initialState=updater
		self.treeOutput=""
		self.nullMoveId=self.steps[0].sId
		self.pathsCount=0

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

	def printAsTree(self,sId=0,level=0,addFormula=True): # to be use
		if sId==0:
			sId=self.nullMoveId
		firstStep=self.getStep(sId)
		childrenIds=firstStep.childrenIds
		if not childrenIds:
			self.pathsCount+=1
			if(addFormula):
				formulaLine=level*"\t"+self.createFormula(sId)+"\r\n"
				self.treeOutput+=formulaLine
		for childrenId in childrenIds:
			infos=self.getStep(childrenId).infos.shortInfo
			line=level*"\t"+infos+"\r\n"
			self.treeOutput+=line
			self.printAsTree(childrenId,level+1)

	def createFormula(self,leafId):
		infos=self.getStep(leafId).infos
		operands=infos.operands
		formula=infos.objectsFormula
		unknow=""
		IdCursor=leafId
		notroot=True
		while (notroot):
			if(unknow=="")or(unknow not in operands): # if the schema did not allow to find the needed operand
				IdCursor=self.getStep(IdCursor).parentId #then continue the search with the parent node
				if(IdCursor!=self.nullMoveId):
					unknow=self.getStep(IdCursor).infos.unknow #and take its output (unknow)
				else:
					notroot=False
			else :
				infos=self.getStep(IdCursor).infos  # if the schema allowed to find a recquired operand
				operands=infos.operands # then we continue the search on its own operands
				formula=formula.replace(" "+unknow+" ","( "+infos.objectsFormulaFirstPart+" )")
		return formula



class Step:
	def __init__(self,move,parentId=0,infos=""):
		self.childrenIds=[]
		self.move=move
		self.parentId=parentId
		self.sId=uuid.uuid4()
		self.infos=infos

	def addInfos(self,infos):
		self.infos=infos



class Solver:
	def __init__(self,updater,constraints=[]):
		self.updater=updater
		self.TreePaths=TreePaths(updater) # store all the paths taken by solver
		self.constraints=constraints

	def addConstraint(self,constraint):
		self.constraints.append(constraint)

	def reInterpretationStep(self,interpSteps=1,level=0,currentStep=None):
		self.updater.updatePossibleRepresentationChange(self.constraints)
		moveList=self.updater.possibleRepresentationChangeList
		print(len(moveList))
		updater=copy.deepcopy(self.updater)
		for repMove in moveList:
			currentStep=Step(Move(repMove))
			if(interpSteps==1):
				self.recurciveBlindForwardSolve(currentStep, copy.deepcopy(updater), level+1)
			else:
				self.reInterpretationStep(interpSteps-1, level+1,currentStep)


	def recurciveBlindForwardSolve(self,currentStep="",updater="",level=0):
		currentStepId=0
		infos=""
		if(level!=0):
			currentStepId=currentStep.sId
			infos=updater.applyMove(currentStep.move)
			updater.updateAppliableSchemas(self.constraints)
			currentStep.addInfos(infos)
			self.TreePaths.addStep(currentStep)
		else:
			updater=copy.deepcopy(self.updater) # we init the updater
		if (not updater.problemState.isProblemEnded()):
			for schem in updater.appliableSchemaList:
				newstep=Step(Move(schem),currentStepId)
				#print(step,s,ml,schem.positions.keys())
				self.recurciveBlindForwardSolve(newstep,copy.deepcopy(updater),level+1)

schema1=Schema("PoissonEF","PoissonEI",operations.addition,"PoissonGAIN","change")
schema2=Schema("ViandeEF","ViandeEI",operations.addition,"ViandeGAIN","change")
struct=ProblemStructure()
struct.addSchema(schema1)
struct.addSchema(schema2)
struct.addBridgingSchemas(schema1,schema2)
struct.updateObjectList()

text=Text()
text.addTextInformation(TextInformation(Representation(Quantity("PoissonGAIN","P1"),'Au supermarch�, le kilo de poisson a augment� de 5 euros cette ann�e')))
text.addTextInformation(TextInformation(Representation(Quantity("PoissonEF","T1"),'Un kilo de poisson coute maintenant 12 euros.')))
text.addTextInformation(TextInformation(Representation(Quantity("PoissonEIminusViandeEI","dEI"),'Au d�but de l\'ann�e, le kilo de viande coutait le m�me prix que le kilo de poisson.')))
text.addTextInformation(TextInformation(Representation(Quantity("PoissonGAINminusViandeGAIN","dGAIN"),'Le kilo de viande a augment� de 3 euros de moins que le kilo de poisson')))
text.setGoal(TextGoal(Goal('ViandeEF','Combien coute le kilo de viande maintenant?')))

text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEI","P1"),'Au supermarch�, le kilo de poisson �tait de 5 euros'))
text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEF","P1"),'Au supermarch�, le kilo de poisson coute 5 euros'))
text.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("PoissonEI","T1"),'Un kilo de poisson �tait de 12 euros.'))
text.getTextInformation(2).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","dEI"),'Au la fin de l\'ann�e, le kilo de viande coute le m�me prix que le kilo de poisson.'))
text.getTextInformation(2).addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","dEI"),'Le kilo de viande a augment� du m�me prix que le kilo de poisson.'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonGAIN","dGAIN"),'Le kilo de viande a augment� de 3 euros'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonGAIN","-dGAIN"),'Le kilo de viande a diminu� de 3 euros'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","dGAIN"),'Le kilo de viande a augment� de 3 euros'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeEF","dGAIN"),'Le kilo coute 3 euros � la fin'))
text.setValues({"P1":5,"T1":12,"dEI":0,"dGAIN":3,"-dGAIN":-3})

probleme1=Problem(struct,text)
upD=Updater(probleme1)
upD.startAsUnderstood()
solver=Solver(upD)
solver.addConstraint(IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0))
#moveList=[Move(upD.possibleRepresentationChangeList[0])]
#solver.recurciveBlindForwardSolve(moveList)
solver.reInterpretationStep(interpSteps=1)
solver.TreePaths.printAsTree()
print(solver.TreePaths.treeOutput)
print(solver.TreePaths.pathsCount)