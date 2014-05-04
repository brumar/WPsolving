# -*- coding: cp1252 -*-
import lib.operations as operations
from lib.schemas import *
from lib.subjectRepresentations import *
from lib.textRepresentations import *
from lib.paths import *
import uuid
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
				line=[key,path.problemSolved,path.objectFormula,path.interpretationsSummary]
				if line not in self.datas[problem,model]:
					self.datas[problem,model].append(line)
					print(line)

	def printCSV(self):
		with open('datas.csv', 'wb') as csvfile:
			writer = csv.writer(csvfile, delimiter=';',quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for problem,solvingModel in self.datas:
				for line in self.datas[problem,solvingModel]:
					writer.writerow([problem]+[solvingModel]+line)




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
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4t","Solve")

solver=Solver(upD)
solver.addConstraint(IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0))
solver.addConstraint(BehavioralConstraint(breakTheOldOne=True))
solver.generalSequentialSolver(listOfActions=[solver.INTERP, solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4t","Int+Solve_BREAK")

solver=Solver(upD)
solver.addConstraint(IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0))
solver.addConstraint(BehavioralConstraint(breakTheOldOne=True))
solver.generalSequentialSolver(listOfActions=[solver.INTERP,solver.SCHEMA,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4t","Int+Schem+Int+Solve_BREAK")

solver=Solver(upD)
solver.addConstraint(IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0)) #TODO: changer le equal
solver.addConstraint(BehavioralConstraint(breakTheOldOne=True))
solver.generalSequentialSolver(listOfActions=[solver.INTERP,solver.INTERP,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4t","Int+Int+Solve_BREAK")

solver=Solver(upD)
solver.addConstraint(IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0))
solver.addConstraint(BehavioralConstraint(breakTheOldOne=False))
solver.generalSequentialSolver(listOfActions=[solver.INTERP, solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4t","Int+Solve_NOBREAK")

solver=Solver(upD)
solver.addConstraint(IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0))
solver.addConstraint(BehavioralConstraint(breakTheOldOne=False))
solver.generalSequentialSolver(listOfActions=[solver.INTERP,solver.SCHEMA,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4t","Int+Schem+Int+Solve_NOBREAK")

solver=Solver(upD)
solver.addConstraint(IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0)) #TODO: changer le equal
solver.addConstraint(BehavioralConstraint(breakTheOldOne=False))
solver.generalSequentialSolver(listOfActions=[solver.INTERP,solver.INTERP,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4t","Int+Int+Solve_NOBREAK")


#===============================================================================
# PROBLEM 2
#===============================================================================


text2=copy.deepcopy(text)
text2.setGoal(TextGoal(Goal('ViandeGAIN','Combien coute le kilo de viande maintenant?')))
probleme2=Problem(struct,text2)
probleme2.setInitialValues({"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3},onlyDic=True)
upD=Updater(probleme2)
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

print(simulatedDatas.printCSV())
print(solver.TreePaths.treeOutput)
print(solver.TreePaths.pathsCount)




