# -*- coding: cp1252 -*-
import lib.operations as operations
from lib.schemas import *
from lib.subjectRepresentations import *
from lib.textRepresentations import *
import copy


class Solver:
	def __init__(self,problem):
		self.history=[]
		self.problem=problem
		self.treeVIZ=""

	def recurciveBlindForwardSolve(self,movelist=[],newmove="",step=0,history=[],schemeToApply=0):
		if(step!=0):
			movelist.append(newmove)
		updater=Updater(self.problem)
		updater.applyMoveList(movelist)
		if (not updater.problemState.isProblemEnded()):
			for schem in updater.appliableSchemaList:
				newmove=Move(schem)
				#print(step,s,ml,schem.positions.keys())
				self.updateTree(step,schem.positions.keys())
				self.recurcive_solve(copy.deepcopy(movelist),newmove,step+1,copy.deepcopy(history))
		else:
			#print(history)
			step=0
	def updateTree(self,step,keys):
		line=step*"\t"+str(keys)+"\r\n"
		self.treeVIZ+=line



schema1=Schema("PoissonEF","PoissonEI",operations.addition,"PoissonGAIN","change")
schema2=Schema("ViandeEF","ViandeEI",operations.addition,"ViandeGAIN","change")
struct=ProblemStructure()
struct.addSchema(schema1)
struct.addSchema(schema2)
struct.addBridgingSchemas(schema1,schema2)
struct.updateObjectList()

text=Text()
text.addTextInformation(TextInformation(Representation(Quantity("PoissonGAIN",5),'Au supermarché, le kilo de poisson a augmenté de 5 euros cette année')))
text.addTextInformation(TextInformation(Representation(Quantity("PoissonEF",12),'Un kilo de poisson coûte maintenant 12 euros.')))
text.addTextInformation(TextInformation(Representation(Quantity("PoissonEIminusViandeEI",0),'Au début de l\'année, le kilo de viande coûtait le même prix que le kilo de poisson.')))
text.addTextInformation(TextInformation(Representation(Quantity("PoissonGAINminusViandeGAIN",3),'Le kilo de viande a augmenté de 3 euros de moins que le kilo de poisson')))
text.setGoal(TextGoal(Goal('ViandeEF','Combien coûte le kilo de viande maintenant?')))

text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEI",5),'Au supermarché, le kilo de poisson était de 5 euros'))
text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEF",5),'Au supermarché, le kilo de poisson coute 5 euros'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonGAIN",3),'Le kilo de viande a augmenté de 3 euros'))


probleme1=Problem(struct,text)
upD=Updater(probleme1)
upD.startAsUnderstood()
upD.updatePossibleRepresentationChange()
solver=Solver(probleme1)
moveList=[Move(upD.possibleRepresentationChangeList[0])]
solver.recurciveBlindForwardSolve(moveList)
print(solver.treeVIZ)