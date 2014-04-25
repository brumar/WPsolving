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

	def addStep(self, step):
		self.steps.append(step)
		self.dicStep[step.sId]=len(self.steps)-1
		self.addChild(step.parentId,step.sId)

	def addChild(self,parentId,childId):
		if(parentId==0): # if parentId = 0 then it is a 1rst level node
			parentId=self.nullMoveId  # then the parent Id is set to the id of the nullMove which is by convention the initial state
		indexOfStep=self.dicStep[parentId]
		parentStep=self.steps[indexOfStep]
		parentStep.childrenIds.append(childId)

	def getStep(self,sId):
		return (self.steps[self.dicStep[sId]])

	def printAsTree(self,sId=0,level=0): # to be use
		if sId==0:
			sId=self.nullMoveId
		firstStep=self.getStep(sId)
		childrenIds=firstStep.childrenIds
		for childrenId in childrenIds:
			infos=self.getStep(childrenId).infos
			line=level*"\t"+infos+"\r\n"
			self.treeOutput+=line
			self.printAsTree(childrenId,level+1)



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
	def __init__(self,problem):
		self.problem=problem
		self.TreePaths=TreePaths(Updater(self.problem))

	def recurciveBlindForwardSolve(self,currentStep="",updater="",level=0):
		currentStepId=0
		infos=""
		if(level!=0):
			currentStepId=currentStep.sId
			infos=updater.applyMove(currentStep.move)
			currentStep.addInfos(infos)
			self.TreePaths.addStep(currentStep)
		else:
			updater=Updater(self.problem)
			updater.startAsUnderstood()
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
text.addTextInformation(TextInformation(Representation(Quantity("PoissonGAIN",5),'Au supermarché, le kilo de poisson a augmenté de 5 euros cette année')))
text.addTextInformation(TextInformation(Representation(Quantity("PoissonEF",12),'Un kilo de poisson coute maintenant 12 euros.')))
text.addTextInformation(TextInformation(Representation(Quantity("PoissonEIminusViandeEI",0),'Au début de l\'année, le kilo de viande coutait le même prix que le kilo de poisson.')))
text.addTextInformation(TextInformation(Representation(Quantity("PoissonGAINminusViandeGAIN",3),'Le kilo de viande a augmenté de 3 euros de moins que le kilo de poisson')))
text.setGoal(TextGoal(Goal('ViandeEF','Combien coute le kilo de viande maintenant?')))

text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEI",5),'Au supermarché, le kilo de poisson était de 5 euros'))
text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEF",5),'Au supermarché, le kilo de poisson coute 5 euros'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonGAIN",3),'Le kilo de viande a augmenté de 3 euros'))


probleme1=Problem(struct,text)
upD=Updater(probleme1)
upD.startAsUnderstood()
upD.updatePossibleRepresentationChange()
solver=Solver(probleme1)
moveList=[Move(upD.possibleRepresentationChangeList[0])]
#solver.recurciveBlindForwardSolve(moveList)
solver.recurciveBlindForwardSolve()
print(solver.treeVIZ)
solver.TreePaths.printAsTree()
print(solver.TreePaths.treeOutput)