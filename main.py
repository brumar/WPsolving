# -*- coding: cp1252 -*-
import lib.operations as operations
from lib.schemas import *
from lib.subjectRepresentations import *
from lib.textRepresentations import *
from lib.paths import *
from lib.dataManager import *

schema1=Schema("PoissonEF","PoissonEI",operations.addition,"PoissonGAIN","change")
schema2=Schema("ViandeEF","ViandeEI",operations.addition,"ViandeGAIN","change")
struct=ProblemStructure()
struct.addSchema(schema1)
struct.addSchema(schema2)
struct.addBridgingSchemas(schema1,schema2)
struct.updateObjectSet()

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
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","d"),'Le kilo de viande a augmenté de 3 euros'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","-d"),'Le kilo de viande a diminué de 3 euros'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","-d"),'Le kilo de viande a augmenté de 3 euros de plus que le kilo de poisson'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","d"),'Le kilo de viande vaut 3 euros de moins que le kilo de poisson'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","-d"),'Le kilo de viande vaut 3 euros de plus que le kilo de poisson'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeEF","d"),'Le kilo coute 3 euros à la fin'))
probleme1=Problem(struct,text)
probleme1.setInitialValues({"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3})


simulatedDatas=SimulatedDatas()

upD=Updater(probleme1)
upD.startAsUnderstood()

c1=IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0)
c2=BehavioralConstraint(breakTheOldOne=True)
constraints=[c1,c2]

solver=Solver(upD,constraints)
solver.generalSequentialSolver(listOfActions=[solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4t","Solve")

solver=Solver(upD,constraints)

solver.generalSequentialSolver(listOfActions=[solver.INTERP,solver.SCHEMA,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4t","Int+Schem+Int+Solve_BREAK")

solver=Solver(upD,constraints)

solver.generalSequentialSolver(listOfActions=[solver.INTERP,solver.INTERP,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4t","Int+Int+Solve_BREAK")

solver=Solver(upD,constraints)
solver.generalSequentialSolver(listOfActions=[solver.SCHEMA,solver.INTERP,solver.SCHEMA,solver.INTERP,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4t","Schem+Int+Schem+Int+Solve_BREAK")

c2=BehavioralConstraint(breakTheOldOne=False)
constraints=[c1,c2]

solver=Solver(upD,constraints)
solver.generalSequentialSolver(listOfActions=[solver.INTERP,solver.SCHEMA,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4t","Int+Schem+Int+Solve_NOBREAK")

solver=Solver(upD,constraints)
solver.generalSequentialSolver(listOfActions=[solver.SCHEMA,solver.INTERP,solver.SCHEMA,solver.INTERP,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4t","Schem+Int+Schem+Int+Solve_NOBREAK")

solver=Solver(upD,constraints)
solver.generalSequentialSolver(listOfActions=[solver.INTERP,solver.INTERP,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4t","Int+Int+Solve_NOBREAK")



#===============================================================================
# PROBLEM 2
#===============================================================================
text2=Text()
text2.addTextInformation(TextInformation(Representation(Quantity("PoissonGAIN","P1"),'Au supermarché, le kilo de poisson a augmenté de 5 euros cette année')))
text2.addTextInformation(TextInformation(Representation(Quantity("PoissonEF","T1"),'Un kilo de poisson coute maintenant 12 euros.')))
text2.addTextInformation(TextInformation(Representation(Quantity("PoissonEIminusViandeEI","dEI"),'Au début de l\'année, le kilo de viande coutait le même prix que le kilo de poisson.')))
text2.addTextInformation(TextInformation(Representation(Quantity("PoissonEFminusViandeEF","d"),'Le kilo de viande coûte maintenant 3 euros de moins que le kilos de poisson.')))
text2.setGoal(TextGoal(Goal('ViandeGAIN','De combien le kilo de viande a t-il augmenté ?')))

text2.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEI","P1"),'Au supermarché, le kilo de poisson était de 5 euros'))
text2.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEF","P1"),'Au supermarché, le kilo de poisson coute 5 euros'))
text2.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("PoissonEI","T1"),'Un kilo de poisson était de 12 euros.'))
text2.getTextInformation(2).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","dEI"),'Au la fin de l\'année, le kilo de viande coute le même prix que le kilo de poisson.'))
text2.getTextInformation(2).addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","dEI"),'Le kilo de viande a augmenté du même prix que le kilo de poisson.'))
text2.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","d"),'Le kilo de viande a augmenté de 3 euros'))
text2.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","-d"),'Le kilo de viande a diminué de 3 euros'))
text2.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","-d"),'Le kilo de viande a augmenté de 3 euros de plus que le kilo de poisson'))
text2.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","d"),'Le kilo de viande vaut 3 euros de moins que le kilo de poisson'))
text2.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","-d"),'Le kilo de viande vaut 3 euros de plus que le kilo de poisson'))
text2.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeEF","d"),'Le kilo coute 3 euros à la fin'))

probleme2=Problem(struct,text2)
probleme2.setInitialValues({"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3})

upD=Updater(probleme2)
upD.startAsUnderstood()
c1=IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0)
c2=BehavioralConstraint(breakTheOldOne=True)
constraints=[c1,c2]

solver=Solver(upD,constraints)
solver.generalSequentialSolver(listOfActions=[solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4p","Solve")

solver=Solver(upD,constraints)
solver.generalSequentialSolver(listOfActions=[solver.INTERP,solver.SCHEMA,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4p","Int+Schem+Int+Solve_BREAK")
print(solver.TreePaths.treeOutput)
print(solver.TreePaths.pathsCount)

solver=Solver(upD,constraints)
solver.generalSequentialSolver(listOfActions=[solver.INTERP,solver.INTERP,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4p","Int+Int+Solve_BREAK")

c2=BehavioralConstraint(breakTheOldOne=False)
constraints=[c1,c2]

solver=Solver(upD,constraints)
solver.generalSequentialSolver(listOfActions=[solver.INTERP,solver.SCHEMA,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4p","Int+Schem+Int+Solve_NOBREAK")

solver=Solver(upD,constraints)
solver.generalSequentialSolver(listOfActions=[solver.INTERP,solver.INTERP,solver.SOLVER])
solver.TreePaths.scanTree()
simulatedDatas.addDataSet(solver.TreePaths.pathList,"Tc4p","Int+Int+Solve_NOBREAK")

print(simulatedDatas.printCSV())






