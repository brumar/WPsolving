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

#=================PROBLEME 1 : Tc4t=============================================
#===============================================================================
# Au supermarché, le kilo de poisson a augmenté de 5 euros cette année.
# Un kilo de poisson coûte maintenant 12 euros.
# Au début de l'année, le kilo de viande coûtait le même prix que le kilo de poisson.
# Le kilo de viande a augmenté de 3 euros de moins que le kilo de poisson.
# Combien coûte le kilo de viande maintenant ?
#===============================================================================


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
problem1=Problem(struct,text)
problem1.name="Tc4t"



#===============PROBLEME 2 : Tc1t ====================================================
#==============================================================================
# Pendant la récréation, Lucas gagne 7 billes.
# Après la récréation, Lucas a 16 billes.
# Avant la récréation, Simon avait autant de billes que Lucas.
# Pendant la récréation, Simon gagne 3 billes de moins que Lucas.
# Combien Simon a-t-il de billes après la récréation ?
#===============================================================================
problem2=copy.deepcopy(problem1)
problem2.name="Tc1t"
keydic={"Viande":"Lucas","Poisson":"Simon"}
problem2.renameKeywordObjects(keydic)
newrep=Representation(Quantity("LucasGAIN","T1"),'Après la récréation, Lucas gagne 16 billes')
problem2.text.getTextInformation(1).addAlternativeRepresentation(newrep)


#===============PROBLEME 3 : Tc2t ============================================
# Cette année, Théo a été pesé par le pédiatre.
# Théo a pris 5 kilos depuis le début de l’année.
# Théo pèse maintenant 14 kilos.
# Au début de l’année, Nicolas pesait le même poids que Théo.
# Nicolas a pris 2 kilos de moins que Théo cette année.
# Combien Nicolas pèse-t-il maintenant ?
#===============================================================================

problem3=copy.deepcopy(problem1)
problem3.name="Tc2t"
keydic={"Viande":"Théo","Poisson":"Nicolas"}
problem3.renameKeywordObjects(keydic) # no difference with pbm1 concerning possible alternative representations
problem3.text.getTextInformation(2).removeAlternativeRepresentations()
newrep=Representation(Quantity("NicolasEFminusThéoEF","dEI"),'A la fin de l\'année Nicolas pesait le même poids que Théo')
problem3.text.getTextInformation(2).addAlternativeRepresentation(newrep)

#===============PROBLEME 4 : Tc3t ============================================
#===============================================================================
# En janvier, 7 enfants se sont inscrits à la chorale.
# Après janvier, il y a 16 enfants à la chorale.
# Avant janvier, il y avait autant d'enfants inscrits au football qu'à la chorale.
# En janvier, il y a eu 2 inscriptions de moins au football qu'à la chorale.
# Combien y a-t-il d'enfants au football après janvier ?
#===============================================================================

problem4=copy.deepcopy(problem1)
problem4.name="Tc3t"
keydic={"Viande":"football","Poisson":"chorale"}
problem4.renameKeywordObjects(keydic)
newrep=Representation(Quantity("choraleGAIN","T1"),'')
problem4.text.getTextInformation(1).addAlternativeRepresentation(newrep)


#===============PROBLEME 1p : Tc4p  =============================================
#===============================================================================
# Au supermarché, le kilo de poisson a augmenté de 5 euros cette année.
# Un kilo de poisson coûte maintenant 12 euros.
# Au début de l'année, le kilo de viande coûtait le même prix que le kilo de poisson.
# Le kilo de viande coûte maintenant 3 euros de moins que le kilos de poisson.
# De combien d'euros le kilo de viande a-t-il augmenté ?
#===============================================================================


problem1p=copy.deepcopy(problem1)
problem1p.name="Tc4p"
info3_prime=TextInformation(Representation(Quantity("PoissonEFminusViandeEF","d"),'Le kilo de viande vaut 3 euros de moins que le kilo de poisson'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","d"),'Le kilo de viande a augmenté de 3 euros'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","-d"),'Le kilo de viande a diminué de 3 euros'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","-d"),'Le kilo de viande a augmenté de 3 euros de plus que le kilo de poisson'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","d"),'Le kilo de viande a augmenté de 3 euros de moins que le kilo de poisson'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","-d"),'Le kilo de viande vaut 3 euros de plus que le kilo de poisson'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("ViandeEF","d"),'Le kilo coute 3 euros à la fin'))
problem1p.text.textInformations[3]=info3_prime
problem1p.text.setGoal(TextGoal(Goal('ViandeGAIN','De combien le kilo de viande a t-il augmenté ?')))

#===============PROBLEME 2p : Tc3p  =============================================
#===============================================================================
# En janvier, 7 enfants se sont inscrits à la chorale.
# Après janvier, il y a 16 enfants à la chorale.
# Avant janvier, il y avait autant d'enfants inscrits au football qu'à la chorale.
# En janvier, il y a eu de nouvelles inscriptions au football.
# Après janvier, il y a 2 enfants de moins au football qu'à la chorale.
# Combien d'enfants se sont inscrits au football en janvier ?
#===============================================================================
#===============================================================================
problem2p=copy.deepcopy(problem1p)
problem2p.name="Tc3p"
keydic={"Viande":"football","Poisson":"chorale"}
problem2p.renameKeywordObjects(keydic)
newrep=Representation(Quantity("choraleGAIN","T1"),'')
problem2p.text.getTextInformation(1).addAlternativeRepresentation(newrep)


#===============PROBLEME 3p : Tc2p  =============================================
#===============================================================================
# Cette année, Théo a été pesé par le pédiatre.
# Théo a pris 5 kilos depuis le début de l’année.
# Théo pèse maintenant 14 kilos.
# Au début de l’année, Nicolas pesait le même poids que Théo.
# Maintenant, Nicolas pèse 2 kilos de moins que Théo.
# Combien de kilos Nicolas a-t-il pris cette année ?
#===============================================================================
#===============================================================================
problem3p=copy.deepcopy(problem1p)
problem3p.name="Tc2p"
keydic={"Viande":"Théo","Poisson":"Nicolas"}
problem3p.renameKeywordObjects(keydic) # no difference with pbm1 concerning possible alternative representations
problem3p.text.getTextInformation(2).removeAlternativeRepresentations()
newrep=Representation(Quantity("NicolasEFminusThéoEF","dEI"),'A la fin de l\'année Nicolas pesait le même poids que Théo')
problem3p.text.getTextInformation(2).addAlternativeRepresentation(newrep)

#===============PROBLEME 4p : Tc1p  =============================================
#===============================================================================
# Pendant la récréation, Lucas gagne 7 billes.
# Après la récréation, Lucas a 16 billes.
# Avant la récréation, Simon avait autant de billes que Lucas.
# Pendant la récréation, Simon gagne des billes,
# et après la récréation, il a 3 billes de moins que Lucas.
# Combien Simon a-t-il gagné de billes pendant la récréation ?
#===============================================================================
#===============================================================================
problem4p=copy.deepcopy(problem1p)
problem4p.name="Tc1p"
keydic={"Viande":"Lucas","Poisson":"Simon"}
problem4p.renameKeywordObjects(keydic)
newrep=Representation(Quantity("LucasGAIN","T1"),'Après la récréation, Lucas gagne 16 billes')
problem4p.text.getTextInformation(1).addAlternativeRepresentation(newrep)

simulatedDatas=SimulatedDatas()
problem1.setInitialValues({"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3})#important : always set the initial values at the start
problem1p.setInitialValues({"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3})
problem2.setInitialValues({"P1":7,"T1":16,"dEI":0,"d":3,"-d":-3})
problem2p.setInitialValues({"P1":7,"T1":16,"dEI":0,"d":3,"-d":-3})
problem3.setInitialValues({"P1":5,"T1":14,"dEI":0,"d":2,"-d":-2})
problem3p.setInitialValues({"P1":5,"T1":14,"dEI":0,"d":2,"-d":-2})
problem4.setInitialValues({"P1":7,"T1":16,"dEI":0,"d":2,"-d":-2})
problem4p.setInitialValues({"P1":7,"T1":16,"dEI":0,"d":2,"-d":-2})

generateAllPossibilities(problem2)
generateAllPossibilities(problem1)
generateAllPossibilities(problem3)
generateAllPossibilities(problem4)
generateAllPossibilities(problem2p)
generateAllPossibilities(problem1p)
generateAllPossibilities(problem3p)
generateAllPossibilities(problem4p)

print(simulatedDatas.printCSV(csvFile="datas1.csv",hideUnsolved=True))
simulatedDatas.printMiniCSV(csvFile="mini1.csv")




