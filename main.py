# -*- coding: cp1252 -*-
import lib.operations as operations
from lib.schemas import *
from lib.subjectRepresentations import *
from lib.textRepresentations import *
from lib.paths import *
from lib.dataManager import *
from lib.optionsFactory import *
# analysis script 1


def generateAllPossibilities(problem):
    global simulatedDatas
    c1=IntervalConstraint(['EF','EI'],operations.superiorOrEqualTo0)
    upD=Updater(problem)
    upD.startAsUnderstood()
    print([Solver.INTERP,Solver.INTERP,Solver.SCHEMA,Solver.SCHEMA,Solver.SCHEMA])
    optionsList=optionsFactory([Solver.INTERP,Solver.INTERP,Solver.SCHEMA,Solver.SCHEMA,Solver.SCHEMA]) # will generate all the options possible with 2 interpretations step randomly occuring
    for i,options in enumerate(optionsList) :
        model=str(options[0])
        c2=BehavioralConstraint(breakTheOldOne=options[1])
        constraints=[c1,c2]
        solver=Solver(upD,constraints)
        solver.generalSequentialSolver(listOfActions=options[0])
        solver.TreePaths.scanTree()
        #print(solver.TreePaths.treeOutput)
        simulatedDatas.addDataSet(solver.TreePaths.pathList,problem.name,model)
        print("DONE : model "+model+"( "+str(i)+" )")


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


problem2=copy.deepcopy(probleme1)
info3_prime=TextInformation(Representation(Quantity("PoissonEFminusViandeEF","d"),'Le kilo de viande vaut 3 euros de moins que le kilo de poisson'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","d"),'Le kilo de viande a augmenté de 3 euros'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","-d"),'Le kilo de viande a diminué de 3 euros'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","-d"),'Le kilo de viande a augmenté de 3 euros de plus que le kilo de poisson'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","d"),'Le kilo de viande a augmenté de 3 euros de moins que le kilo de poisson'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","-d"),'Le kilo de viande vaut 3 euros de plus que le kilo de poisson'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("ViandeEF","d"),'Le kilo coute 3 euros à la fin'))
problem2.text.textInformations[3]=info3_prime
problem2.text.setGoal(TextGoal(Goal('ViandeGAIN','De combien le kilo de viande a t-il augmenté ?')))
problem2.name="Tc4p"
probleme1.name="Tc4t"

problem3=copy.deepcopy(problem2)
problem3.renameObjects({'PoissonEF': 'PoissonEFsecond',
           'PoissonEI': 'PoissonEIsecond',
           'PoissonGAIN': 'PoissonGAINsecond',
           'ViandeEF': 'ViandeEFsecond',
           'ViandeEI': 'ViandeEIsecond',
           'ViandeGAIN': 'ViandeGAINsecond',
           'PoissonGAINminusViandeGAIN' : 'PoissonGAINminusViandeGAIN_second',
           'PoissonEIminusViandeEI' : 'PoissonEIminusViandeEI_second',
           'PoissonEFminusViandeEF' : 'PoissonEFminusViandeEF_second'
           })
problem3.setInitialValues({"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3})
problem3.name="Tc4t_replace"

simulatedDatas=SimulatedDatas()
probleme1.setInitialValues({"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3})#important : always set the initial values at the start
problem2.setInitialValues({"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3})
generateAllPossibilities(problem2) # change simulated datas
generateAllPossibilities(probleme1)

print(simulatedDatas.printCSV(hideUnsolved=True))





