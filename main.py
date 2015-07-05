# -*- coding: cp1252 -*-
import lib.operations as operations
from blindgenerator.generate import *
from lib.schemas import *
from lib.subjectRepresentations import *
from lib.textRepresentations import *
from lib.paths import *
from lib.dataManager import *
from lib.optionsFactory import *
from lib.observations import *
from lib.problemBank import *
from lib.postEvaluation import *
from lib.constraints  import *
from lib.keywordSolver import KeywordSolver
import csv
import datetime
import time
import os
import logging
import re
import pickle

## SIMULATION DIRECTORY
simulationName=raw_input("simulation Name ? : ")
#simulationName=""
start = time.time()
timeformat='%Y_%m_%d__%H_%M_%S'
timestamp = datetime.datetime.fromtimestamp(start).strftime(timeformat)
simulationDirectory="simulations/"+timestamp+"_"+simulationName+"/"
os.makedirs(simulationDirectory)

## GLOBAL OPTIONS
alreadySimulated=False
#change the pickle filename if alreadySimulate==True
pickleFile="simulations/2014_11_03__16_08_03_seriousStuff/simulation2014_11_03__16_08_03.pkl"
newsimulation=simulationDirectory+"simulation"+timestamp+".pkl"

## LOGGING
logging.basicConfig(filename=simulationDirectory+'simulation.log',level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt=timeformat)
logging.getLogger().addHandler(logging.StreamHandler())


class Model():
    def __init__(self):
        pass
    def extractPredictions(self,*args):
        raise NotImplementedError("must be implemented")









#===============================================================================
# STEP 1 : Create problems
#===============================================================================

#=================PROBLEME 1 : Tc4t=============================================
Tc4t="""Au supermarché, le kilo de poisson a augmenté de 5 euros cette année.
Un kilo de poisson coûte maintenant 12 euros.
Au début de l\'année, le kilo de viande coûtait le même prix que le kilo de poisson.
Le kilo de viande a augmenté de 3 euros de moins que le kilo de poisson.
Combien coûte le kilo de viande maintenant ?"""



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
problemTc4t=Problem(struct,text)
problemTc4t.name="Tc4t"

#===============PROBLEME 2 : Tc1t ====================================================
Tc1t="""Pendant la récréation, Lucas gagne 7 billes.
Après la récréation, Lucas a 16 billes.
Avant la récréation, Simon avait autant de billes que Lucas.
Pendant la récréation, Simon gagne 3 billes de moins que Lucas.
Combien Simon a-t-il de billes après la récréation ?"""

problemTc1t=copy.deepcopy(problemTc4t)
problemTc1t.name="Tc1t"
keydic={"Poisson":"Lucas","Viande":"Simon"}
problemTc1t.renameKeywordObjects(keydic)
newrep=Representation(Quantity("LucasGAIN","T1"),'Après la récréation, Lucas gagne 16 billes')
problemTc1t.text.getTextInformation(1).addAlternativeRepresentation(newrep)


#===============PROBLEME 3 : Tc2t ============================================
Tc2t="""Cette année, Théo a été pesé par le pédiatre.
Théo a pris 5 kilos depuis le début de l’année.
Théo pèse maintenant 14 kilos.
Au début de l’année, Nicolas pesait le même poids que Théo.
Nicolas a pris 2 kilos de moins que Théo cette année.
Combien Nicolas pèse-t-il maintenant ?"""

problemTc2t=copy.deepcopy(problemTc4t)
problemTc2t.name="Tc2t"
keydic={"Viande":"Théo","Poisson":"Nicolas"}
problemTc2t.renameKeywordObjects(keydic) # no difference with pbm1 concerning possible alternative representations
problemTc2t.text.getTextInformation(2).removeAlternativeRepresentations()
newrep=Representation(Quantity("NicolasEFminusThéoEF","dEI"),'A la fin de l\'année Nicolas pesait le même poids que Théo')
problemTc2t.text.getTextInformation(2).addAlternativeRepresentation(newrep)

#===============PROBLEME 4 : Tc3t ============================================

Tc3t="""En janvier, 7 enfants se sont inscrits à la chorale.
Après janvier, il y a 16 enfants à la chorale.
Avant janvier, il y avait autant d\'enfants inscrits au football qu\'à la chorale.
En janvier, il y a eu 2 inscriptions de moins au football qu\'à la chorale.
Combien y a-t-il d\'enfants au football après janvier ?"""

problemTc3t=copy.deepcopy(problemTc4t)
problemTc3t.name="Tc3t"
keydic={"Viande":"football","Poisson":"chorale"}
problemTc3t.renameKeywordObjects(keydic)
newrep=Representation(Quantity("choraleGAIN","T1"),'')
problemTc3t.text.getTextInformation(1).addAlternativeRepresentation(newrep)


#===============PROBLEME 1p : Tc4p  =============================================
Tc4p="""Au supermarché, le kilo de poisson a augmenté de 5 euros cette année.
Un kilo de poisson coûte maintenant 12 euros.
Au début de l\'année, le kilo de viande coûtait le même prix que le kilo de poisson.
Le kilo de viande coûte maintenant 3 euros de moins que le kilos de poisson.
De combien d\'euros le kilo de viande a-t-il augmenté ?"""

problemTc4p=copy.deepcopy(problemTc4t)
problemTc4p.name="Tc4p"
info3_prime=TextInformation(Representation(Quantity("PoissonEFminusViandeEF","d"),'Le kilo de viande vaut 3 euros de moins que le kilo de poisson'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","d"),'Le kilo de viande a augmenté de 3 euros'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","-d"),'Le kilo de viande a diminué de 3 euros'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","-d"),'Le kilo de viande a augmenté de 3 euros de plus que le kilo de poisson'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","d"),'Le kilo de viande a augmenté de 3 euros de moins que le kilo de poisson'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","-d"),'Le kilo de viande vaut 3 euros de plus que le kilo de poisson'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("ViandeEF","d"),'Le kilo coute 3 euros à la fin'))
problemTc4p.text.textInformations[3]=info3_prime
problemTc4p.text.setGoal(TextGoal(Goal('ViandeGAIN','De combien le kilo de viande a t-il augmenté ?')))

#===============PROBLEME 3p : Tc3p  =============================================
Tc3p="""En janvier, 7 enfants se sont inscrits à la chorale.
Après janvier, il y a 16 enfants à la chorale.
Avant janvier, il y avait autant d\'enfants inscrits au football qu\'à la chorale.
En janvier, il y a eu de nouvelles inscriptions au football.
Après janvier, il y a 2 enfants de moins au football qu\'à la chorale.
Combien d\'enfants se sont inscrits au football en janvier ?"""


problemTc3p=copy.deepcopy(problemTc4p)
problemTc3p.name="Tc3p"
keydic={"Viande":"football","Poisson":"chorale"}
problemTc3p.renameKeywordObjects(keydic)
newrep=Representation(Quantity("choraleGAIN","T1"),'')
problemTc3p.text.getTextInformation(1).addAlternativeRepresentation(newrep)


#===============PROBLEME 3p : Tc2p  ============================================

Tc2p="""Cette année, Théo a été pesé par le pédiatre.
Théo a pris 5 kilos depuis le début de l’année.
Théo pèse maintenant 14 kilos.
Au début de l’année, Nicolas pesait le même poids que Théo.
Maintenant, Nicolas pèse 2 kilos de moins que Théo.
Combien de kilos Nicolas a-t-il pris cette année ?"""



problemTc2p=copy.deepcopy(problemTc4p)
problemTc2p.name="Tc2p"
keydic={"Viande":"Théo","Poisson":"Nicolas"}
problemTc2p.renameKeywordObjects(keydic) # no difference with pbm1 concerning possible alternative representations
problemTc2p.text.getTextInformation(2).removeAlternativeRepresentations()
newrep=Representation(Quantity("NicolasEFminusThéoEF","dEI"),'A la fin de l\'année Nicolas pesait le même poids que Théo')
problemTc2p.text.getTextInformation(2).addAlternativeRepresentation(newrep)

#===============PROBLEME 4p : Tc1p  =============================================

Tc1p="""Pendant la récréation, Lucas gagne 7 billes.
Après la récréation, Lucas a 16 billes.
Avant la récréation, Simon avait autant de billes que Lucas.
Pendant la récréation, Simon gagne des billes,
et après la récréation, il a 3 billes de moins que Lucas.
Combien Simon a-t-il gagné de billes pendant la récréation ?"""

problemTc1p=copy.deepcopy(problemTc4p)
problemTc1p.name="Tc1p"
keydic={"Poisson":"Lucas","Viande":"Simon"}
problemTc1p.renameKeywordObjects(keydic)
newrep=Representation(Quantity("LucasGAIN","T1"),'Après la récréation, Lucas gagne 16 billes')
problemTc1p.text.getTextInformation(1).addAlternativeRepresentation(newrep)

# Cc1t
Cc1t="""Antoine a 5 billes.
Quand Antoine réunit ses billes avec celles de Paul, ils ont 12 billes ensemble
Paul réunit ses billes avec celles de Jacques.
Jacques a 3 billes de moins qu’Antoine.
Combien Paul et Jacques ont-ils de billes ensemble ?"""


schema1Cc1t=Schema(qf="AntoineETPaul",q1="Paul",operation=operations.addition,q2="Antoine",name="combinaison")
schema2Cc1t=Schema(qf="JacquesETPaul",q1="Paul",operation=operations.addition,q2="Jacques",name="combinaison")
structCc1t=ProblemStructure()
structCc1t.addSchema(schema1Cc1t)
structCc1t.addSchema(schema2Cc1t)
structCc1t.addBridgingSchemas(schema1Cc1t,schema2Cc1t)
structCc1t.updateObjectSet()

textCc1t=Text()
textCc1t.addTextInformation(TextInformation(Representation(Quantity("Antoine","P1"),'Antoine a 5 billes')))
textCc1t.addTextInformation(TextInformation(Representation(Quantity("AntoineETPaul","T1"),'Quand Antoine réunit ses billes avec celles de Paul, ils ont 12 billes ensemble')))
textCc1t.addTextInformation(TextInformation(Representation(Quantity("PaulminusPaul","zero"),'Ce sont les mêmes "Paul"')))
textCc1t.addTextInformation(TextInformation(Representation(Quantity("AntoineminusJacques","d"),'Le kilo de viande a augmenté de 3 euros de moins que le kilo de poisson')))
textCc1t.setGoal(TextGoal(Goal('JacquesETPaul','Combien Paul et Jacques ont-ils de billes ensemble ?')))


textCc1t.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("Paul","T1"),'Quand Antoine réunit ses billes avec celles de Paul qui a 12 billes'))
textCc1t.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("Antoine","T1"),'Antoine recoit des billes de Paul, maintenant il en a 12'))
#=============== MISE A L ECART : VOLONTE DE SIMPLIFIER ======================
# textCc1t.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("Antoine","(T1+P1)"),'Antoine recoit 12 billes de Paul'))
# textCc1t.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("Antoine","zero"),'Antoine donne ses billes de Paul, maintenant il en a 12'))
# textCc1t.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("Paul","zero"),'Paul donne ses billes a Antoine, maintenant il en a 12'))
#===============================================================================

textCc1t.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("Jacques","d"),'Jacques a trois billes'))
textCc1t.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("AntoineminusJacques","-d"),'Antoine a trois billes de plus'))
#textCc1t.getTextInformation(2).addAlternativeRepresentation(Representation(Quantity("Antoine","T1"),'Antoine recoit des billes de Paul, maintenant il en a 3'))
#textCc1t.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("Paul","zero"),'Antoine recoit des billes de Paul....'))

problemCc1t=Problem(structCc1t,textCc1t)
problemCc1t.name="Cc1t"

#===============================================================================
# c1=IntervalConstraint(['GAIN','Minus'],operations.avoidNegativeValuesWithException)
# c2=BehavioralConstraint(breakPreviousInterpretations=False) # when True, the old representation of the text information is still available
# upD=Updater(problemCc1t)
# upD.startAsUnderstood()
# constraints=[c1,c2]
# solver=Solver(upD,constraints)
# solver.generalSequentialSolver(listOfActions=[1,1,3])
# solver.TreePaths.scanTree()
# logging.info(solver.TreePaths.treeOutput)
#===============================================================================

# Cc1p
Cc1p="""Antoine a 5 billes.
Quand Antoine réunit ses billes avec celles de Paul, ils ont 12 billes ensemble.
Quand Paul et Jacques réunissent leurs billes, cela fait 3 billes de moins.
Combien Jacques a-t-il de billes ?"""

problemCc1p=copy.deepcopy(problemCc1t)
problemCc1p.name="Cc1p"
infoCC1p_3=TextInformation(Representation(Quantity("AntoineETPaulminusJacquesETPaul","d"),'Quand Paul et Jacques réunissent leurs billes, cela fait 3 billes de moins'))
infoCC1p_3.addAlternativeRepresentation(Representation(Quantity("AntoineETPaulminusJacquesETPaul","-d"),'Quand Paul et Jacques réunissent leurs billes, cela fait 3 billes de plus'))
infoCC1p_3.addAlternativeRepresentation(Representation(Quantity("JacquesETPaul","d"),'Quand Paul et Jacques réunissent leurs billes, cela fait 3 billes'))
#infoCC1p_3.addAlternativeRepresentation(Representation(Quantity("Paul","zero"),'Paul donne ses billes à Jacques....'))
#infoCC1p_3.addAlternativeRepresentation(Representation(Quantity("Jacques","zero"),'Paul donne ses billes à Jacques....'))
infoCC1p_3.addAlternativeRepresentation(Representation(Quantity("Paul","d"),'d'))
infoCC1p_3.addAlternativeRepresentation(Representation(Quantity("Jacques","d"),'d'))
problemCc1p.text.textInformations[3]=infoCC1p_3
problemCc1p.text.setGoal(TextGoal(Goal('Jacques','Combien Jacques a-t-il de billes ?')))

#===============================================================================
# Cc2t

Cc2t="""Quand Medor monte sur la balance chez le vétérinaire, la balance indique 6 kilos.
Quand Medor et Rex montent ensemble sur la balance chez le vétérinaire, la balance indique 15 kilos.
Fido et Rex montent ensemble sur la balance chez le vétérinaire.
Fido pèse 2 kilos de moins que Medor.
Combien Fido et Rex pèsent-ils ensemble ?"""


problemCc2t=copy.deepcopy(problemCc1t)
problemCc2t.name="Cc2t"
keydic={"Antoine":"Medor","Paul":"Rex","Jacques":"Fido"}
problemCc2t.renameKeywordObjects(keydic)
problemCc2t.text.getTextInformation(1).removeAlternativeRepresentations()
problemCc2t.text.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("Medor","T1"),''))
problemCc2t.text.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("Rex","T1"),''))
problemCc2t.text.getTextInformation(3).removeAlternativeRepresentations()
problemCc2t.text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("Fido","d"),''))
problemCc2t.text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("MedorminusFido","-d"),''))

#===============================================================================
# text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEI","P1"),'Au supermarché, le kilo de poisson était de 5 euros'))
# text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEF","P1"),'Au supermarché, le kilo de poisson coute 5 euros'))
# text.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("PoissonEI","T1"),'Un kilo de poisson était de 12 euros.'))
# text.getTextInformation(2).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","dEI"),'Au la fin de l\'année, le kilo de viande coute le même prix que le kilo de poisson.'))
# text.getTextInformation(2).addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","dEI"),'Le kilo de viande a augmenté du même prix que le kilo de poisson.'))
# text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","d"),'Le kilo de viande a augmenté de 3 euros'))
# text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","-d"),'Le kilo de viande a diminué de 3 euros'))
# text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","-d"),'Le kilo de viande a augmenté de 3 euros de plus que le kilo de poisson'))
# text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","d"),'Le kilo de viande vaut 3 euros de moins que le kilo de poisson'))
# text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","-d"),'Le kilo de viande vaut 3 euros de plus que le kilo de poisson'))
# text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeEF","d"),'Le kilo coute 3 euros à la fin'))
# problemTc4t=Problem(struct,text)
# problemTc4t.name="Tc4t"
#===============================================================================


#===============================================================================
# Cc2p

Cc2p="""Quand Medor monte sur la balance chez le vétérinaire, la balance indique 6 kilos.
Quand Medor et Rex montent ensemble sur la balance chez le vétérinaire, la balance indique 15 kilos.
Lorsque Fido et Rex montent sur la balance ensemble, la balance indique 2 kilos de moins.
Combien pèse Fido ?"""

problemCc2p=copy.deepcopy(problemCc1p)
problemCc2p.name="Cc2p"
keydic={"Antoine":"Medor","Paul":"Rex","Jacques":"Fido"}
problemCc2p.renameKeywordObjects(keydic)

problemCc2p.text.getTextInformation(1).removeAlternativeRepresentations()
problemCc2p.text.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("Medor","T1"),''))
problemCc2p.text.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("Rex","T1"),''))

problemCc2p.text.getTextInformation(3).removeAlternativeRepresentations()
problemCc2p.text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("MedorETRexminusFidoETRex","-d"),'Quand Rex et Fido réunissent leurs billes, cela fait 3 billes de plus'))
problemCc2p.text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("FidoETRex","d"),'Quand Rex et Fido réunissent leurs billes, cela fait 3 billes'))
problemCc2p.text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("Rex","d"),'d'))
problemCc2p.text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("Fido","d"),'d'))

#===============================================================================
# Cc3t
# Dans la classe de CM2, il y a 6 élèves.
# Si on réunit les CM2 et les CM1, cela fait un groupe de 15 élèves.
# On fait un groupe réunissant les CE2 et les CM1.
# Dans la classe de CE2, il y a 2 élèves de moins qu'en CM2.
# Combien y a-t-il d'élèves dans le groupe réunissant les CE2 et les CM1 ?
#===============================================================================
Cc3t="""Dans la classe de CM2, il y a 6 élèves.
Si on réunit les CM2 et les CM1, cela fait un groupe de 15 élèves.
On fait un groupe réunissant les CE2 et les CM1.
Dans la classe de CE2, il y a 2 élèves de moins qu\'en CM2.
Combien y a-t-il d\'élèves dans le groupe réunissant les CE2 et les CM1 ?"""

problemCc3t=copy.deepcopy(problemCc2t)
problemCc3t.name="Cc3t"
keydic={"Medor":"CM2","Rex":"CM1","Fido":"CE2"}
problemCc3t.renameKeywordObjects(keydic)


# Cc3p

Cc3p="""Dans la classe de CM2, il y a 6 élèves.
Si on réunit les CM2 et les CM1, cela fait un groupe de 15 élèves.
Si on réunit les CE2 et les CM1, le groupe a 2 élèves de moins.
Combien y a-t-il d\'élèves en CE2 ?"""

problemCc3p=copy.deepcopy(problemCc2p)
problemCc3p.name="Cc3p"
keydic={"Medor":"CM2","Rex":"CM1","Fido":"CE2"}
problemCc3p.renameKeywordObjects(keydic)


# Cc4t

Cc4t="""Un livre coûte 9 euros. Si on achète un livre et une règle, on paie 14 euros.
On achète une règle et un cahier.
Le cahier coûte 2 euros de moins que le livre.
Combien coûtent la règle et le cahier ensemble ?"""

problemCc4t=copy.deepcopy(problemCc2t)
problemCc4t.name="Cc4t"
keydic={"Medor":"livre","Rex":"regle","Fido":"cahier"}
problemCc4t.renameKeywordObjects(keydic)
problemCc4t.text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("cahier","P1"),''))

#===============================================================================
# Cc4p
Cc4p="""Un livre coûte 9 euros.
Si on achète un livre et une règle, on paie 14 euros.
On achète une règle et un cahier.
Cela coûte 2 euros de moins que lorsque l\'on achète un livre et une règle.
Combien coûte le cahier ?"""

problemCc4p=copy.deepcopy(problemCc2p)
problemCc4p.name="Cc4p"
keydic={"Medor":"livre","Rex":"regle","Fido":"cahier"}
#problemCc3t.renameKeywordObjects(keydic)
#problemCc4t.text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("cahier","P1"),''))

problemCc1t.text.fullText=Cc1t
problemCc1p.text.fullText=Cc1p
problemCc2t.text.fullText=Cc2t
problemCc2p.text.fullText=Cc2p
problemCc3t.text.fullText=Cc3t
problemCc3p.text.fullText=Cc3p
problemCc4t.text.fullText=Cc4t
problemCc4p.text.fullText=Cc4p
problemTc4t.text.fullText=Tc4t
problemTc4p.text.fullText=Tc4p
problemTc1t.text.fullText=Tc1t
problemTc3p.text.fullText=Tc3p
problemTc2t.text.fullText=Tc2t
problemTc2p.text.fullText=Tc2p
problemTc3t.text.fullText=Tc3t
problemTc1p.text.fullText=Tc1p

##############SECOND VERSION OF THE PROBLEMS####################
problemTc1t_v2=copy.deepcopy(problemTc1t)
problemTc2p_v2=copy.deepcopy(problemTc2p)
problemTc3t_v2=copy.deepcopy(problemTc3t)
problemTc4p_v2=copy.deepcopy(problemTc1p)## IMPORTANT : ds la v2 les formulations contexte 4 sont équivalents au contexte 1
problemCc1t_v2=copy.deepcopy(problemCc1t)
problemCc2p_v2=copy.deepcopy(problemCc2p)
problemCc3t_v2=copy.deepcopy(problemCc3t)
problemCc4p_v2=copy.deepcopy(problemCc1p)## IMPORTANT : ds la v2 les formulations contexte 4 sont équivalents au contexte 1
problemTc1p_v2=copy.deepcopy(problemTc1p)
problemTc2t_v2=copy.deepcopy(problemTc2t)
problemTc3p_v2=copy.deepcopy(problemTc3p)
problemTc4t_v2=copy.deepcopy(problemTc1t)## IMPORTANT : ds la v2 les formulations contexte 4 sont équivalents au contexte 1
problemCc1p_v2=copy.deepcopy(problemCc1p)
problemCc2t_v2=copy.deepcopy(problemCc2t)
problemCc3p_v2=copy.deepcopy(problemCc3p)
problemCc4t_v2=copy.deepcopy(problemCc1t)## IMPORTANT : ds la v2 les formulations contexte 4 sont équivalents au contexte 1


Cc4p_v2="""Jules achète un livre à 7 euros et une règle. Jules paie 15 euros.
Aurélien achète une règle et un cahier.
En tout, Aurélien paie 3 euros de moins que Jules.
Combien coûte le cahier ?"""

keydic={"Antoine":"Livre","Paul":"Règle","Jacques":"Cahier"}
problemCc4p_v2.renameKeywordObjects(keydic)

Cc4t_v2="""Jules achète un livre à 7 euros et une règle. Jules paie 15 euros.
Aurélien achète une règle et un cahier.
Le cahier coûte 3 euros de moins que le livre.
Combien Aurélien doit-il payer ? """

keydic={"Antoine":"Livre","Paul":"Règle","Jacques":"Cahier"}
problemCc4t_v2.renameKeywordObjects(keydic)

Tc4p_v2="""Pour Noël, Camille reçoit 7 euros.
Après Noël, Camille a 12 euros dans sa tirelire.
Avant Noël, Léa avait autant d'argent que Camille dans sa tirelire.
Pour Noël, Léa reçoit de l'argent.
Après Noël, Léa a 3 euros de moins que Camille dans sa tirelire.
Combien d'euros Léa a-t-elle reçu pour Noël ?"""

keydic={"Lucas":"Camille","Simon":"Léa"}
problemTc4p_v2.renameKeywordObjects(keydic)

Tc4t_v2="""Après Noël, Camille a 12 euros dans sa tirelire.
Avant Noël, Léa avait autant d'argent que Camille dans sa tirelire.
Pour Noël, Léa reçoit 3 euros de moins que Camille.
Combien Léa a-t-elle d'argent dans sa tirelire après Noël ?"""

keydic={"Lucas":"Camille","Simon":"Léa"}
problemTc4t_v2.renameKeywordObjects(keydic)


Cc1t_v2="""Antoine a 7 billes.
Quand Antoine réunit ses billes avec celles de Paul, ils ont 16 billes ensemble.
Jacques a 4 billes de moins qu’Antoine.
Paul réunit ses billes avec celles de Jacques.
Combien Paul et Jacques ont-ils de billes ensemble ?"""

Cc2t_v2="""Quand Médor monte sur la balance chez le vétérinaire, la balance indique 9 kilos.
Quand Médor et Rex montent ensemble sur la balance chez le vétérinaire, la balance indique 15 kilos.
Fido pèse 4 kilos de moins que Médor.
Fido et Rex montent ensemble sur la balance chez le vétérinaire.
Combien Fido et Rex pèsent-ils ensemble ?"""

Cc3t_v2="""Dans la classe de CM2, il y a 9 élèves.
Si on réunit les CM2 et les CM1, cela fait un groupe de 17 élèves.
Dans la classe de CE2, il y a 3 élèves de moins qu'en CM2.
On fait un groupe réunissant les CE2 et les CM1.
Combien y a-t-il d'élèves dans ce groupe ?"""

Cc1p_v2="""Antoine a 7 billes.
Quand Antoine réunit ses billes avec celles de Paul, ils ont 16 billes ensemble.
Quand Paul et Jacques réunissent leurs billes, cela fait 4 billes de moins.
Combien Jacques a-t-il de billes ?"""

Cc2p_v2="""Quand Médor monte sur la balance chez le vétérinaire, la balance indique 9 kilos.
Quand Médor et Rex montent ensemble sur la balance chez le vétérinaire, la balance indique 15 kilos.
Lorsque Fido et Rex montent sur la balance ensemble, la balance indique 4 kilos de moins.
Combien pèse Fido ?"""

Cc3p_v2="""Dans la classe de CM2, il y a 9 élèves.
Si on réunit les CM2 et les CM1, cela fait un groupe de 17 élèves.
Si on réunit les CE2 et les CM1, le groupe a 3 élèves de moins.
Combien y a-t-il d'élèves en CE2 ?"""

Tc1p_v2="""Pendant la récréation, Lucas gagne 6 billes.
Après la récréation, Lucas a 15 billes.
Avant la récréation, Simon avait autant de billes que Lucas.
Pendant la récréation, Simon gagne 4 billes de moins que Lucas.
Combien Simon a-t-il de billes après la récréation ?"""

Tc2p_v2="""Cette année, Théo a été pesé par le pédiatre.
Théo a pris 5 kilos depuis le début de l’année.
Théo pèse maintenant 14 kilos.
Au début de l’année, Nicolas pesait le même poids que Théo.
Nicolas a pris 2 kilos de moins que Théo cette année.
Combien Nicolas pèse-t-il maintenant ?"""

Tc3p_v2="""En janvier, 6 enfants se sont inscrits à la chorale.
Après janvier, il y a 13 enfants à la chorale.
Avant janvier, il y avait autant d'enfants inscrits au football qu'à la chorale.
En janvier, il y a eu 2 inscriptions de moins au football qu'à la chorale.
Combien y a-t-il d'enfants au football après janvier ?"""

Tc1t_v2="""Pendant la récréation, Lucas gagne 6 billes.
Après la récréation, Lucas a 15 billes.
Avant la récréation, Simon avait autant de billes que Lucas.
Pendant la récréation, Simon gagne des billes, et après la récréation, il a 4 billes de moins que Lucas.
Combien Simon a-t-il gagné de billes pendant la récréation ?"""

Tc2t_v2="""Cette année, Théo a été pesé par le pédiatre.
Théo a pris 5 kilos depuis le début de l’année.
Théo pèse maintenant 14 kilos.
Au début de l’année, Nicolas pesait le même poids que Théo.
Maintenant, Nicolas pèse 2 kilos de moins que Théo.
Combien de kilos Nicolas a-t-il pris cette année ?"""

Tc3t_v2="""En janvier, 6 enfants se sont inscrits à la chorale.
Après janvier, il y a 13 enfants à la chorale.
Avant janvier, il y avait autant d'enfants inscrits au football qu'à la chorale.
En janvier, il y a eu de nouvelles inscriptions au football.
Après janvier, il y a 2 enfants de moins au football qu'à la chorale.
Combien d'enfants se sont inscrits au football en janvier ?"""



problemCc1t_v2.text.fullText=Cc1t_v2
problemCc1p_v2.text.fullText=Cc1p_v2
problemCc2t_v2.text.fullText=Cc2t_v2
problemCc2p_v2.text.fullText=Cc2p_v2
problemCc3t_v2.text.fullText=Cc3t_v2
problemCc3p_v2.text.fullText=Cc3p_v2
problemCc4t_v2.text.fullText=Cc4t_v2
problemCc4p_v2.text.fullText=Cc4p_v2
problemTc4t_v2.text.fullText=Tc4t_v2
problemTc4p_v2.text.fullText=Tc4p_v2
problemTc1t_v2.text.fullText=Tc1t_v2
problemTc3p_v2.text.fullText=Tc3p_v2
problemTc2t_v2.text.fullText=Tc2t_v2
problemTc2p_v2.text.fullText=Tc2p_v2
problemTc3t_v2.text.fullText=Tc3t_v2
problemTc1p_v2.text.fullText=Tc1p_v2

problemCc1t_v2.name="Cc1t_v2"
problemCc1p_v2.name="Cc1p_v2"
problemCc2t_v2.name="Cc2t_v2"
problemCc2p_v2.name="Cc2p_v2"
problemCc3t_v2.name="Cc3t_v2"
problemCc3p_v2.name="Cc3p_v2"
problemCc4t_v2.name="Cc4t_v2"
problemCc4p_v2.name="Cc4p_v2"
problemTc4t_v2.name="Tc4t_v2"
problemTc4p_v2.name="Tc4p_v2"
problemTc1t_v2.name="Tc1t_v2"
problemTc3p_v2.name="Tc3p_v2"
problemTc2t_v2.name="Tc2t_v2"
problemTc2p_v2.name="Tc2p_v2"
problemTc3t_v2.name="Tc3t_v2"
problemTc1p_v2.name="Tc1p_v2"

problemCc1t_v2.setInitialValues({"P1":7,"T1":16,"(T1+P1)":23,"zero":0,"d":4,"-d":-4})
problemCc1p_v2.setInitialValues({"P1":7,"T1":16,"(T1+P1)":23,"zero":0,"d":4,"-d":-4})
problemCc2t_v2.setInitialValues({"P1":9,"T1":15,"(T1+P1)":24,"zero":0,"d":4,"-d":-4})
problemCc2p_v2.setInitialValues({"P1":9,"T1":15,"(T1+P1)":24,"zero":0,"d":4,"-d":-4})
problemCc3t_v2.setInitialValues({"P1":9,"T1":17,"zero":0,"d":3,"-d":-3})
problemCc3p_v2.setInitialValues({"P1":9,"T1":17,"zero":0,"d":3,"-d":-3})
problemCc4t_v2.setInitialValues({"P1":7,"T1":15,"zero":0,"d":3,"-d":-3})
problemCc4p_v2.setInitialValues({"P1":7,"T1":15,"zero":0,"d":3,"-d":-3})

problemTc4t_v2.setInitialValues({"P1":7,"T1":12,"dEI":0,"d":3,"-d":-3})
problemTc4p_v2.setInitialValues({"P1":7,"T1":12,"dEI":0,"d":3,"-d":-3})
problemTc1t_v2.setInitialValues({"P1":6,"T1":15,"dEI":0,"d":4,"-d":-4})
problemTc3p_v2.setInitialValues({"P1":6,"T1":13,"dEI":0,"d":2,"-d":-2})
problemTc2t_v2.setInitialValues({"P1":5,"T1":14,"dEI":0,"d":2,"-d":-2})
problemTc2p_v2.setInitialValues({"P1":5,"T1":14,"dEI":0,"d":2,"-d":-2})
problemTc3t_v2.setInitialValues({"P1":6,"T1":13,"dEI":0,"d":2,"-d":-2})
problemTc1p_v2.setInitialValues({"P1":6,"T1":15,"dEI":0,"d":4,"-d":-4})

problemCc1t.setInitialValues({"P1":5,"T1":12,"(T1+P1)":17,"zero":0,"d":3,"-d":-3})
problemCc1p.setInitialValues({"P1":5,"T1":12,"(T1+P1)":17,"zero":0,"d":3,"-d":-3})
problemCc2t.setInitialValues({"P1":6,"T1":15,"(T1+P1)":21,"zero":0,"d":2,"-d":-2})
problemCc2p.setInitialValues({"P1":6,"T1":15,"(T1+P1)":21,"zero":0,"d":2,"-d":-2})
problemCc3t.setInitialValues({"P1":6,"T1":15,"zero":0,"d":2,"-d":-2})
problemCc3p.setInitialValues({"P1":6,"T1":15,"zero":0,"d":2,"-d":-2})
problemCc4t.setInitialValues({"P1":9,"T1":14,"zero":0,"d":2,"-d":-2})
problemCc4p.setInitialValues({"P1":9,"T1":14,"zero":0,"d":2,"-d":-2})

problemTc4t.setInitialValues({"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3})
problemTc4p.setInitialValues({"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3})
problemTc1t.setInitialValues({"P1":7,"T1":16,"dEI":0,"d":3,"-d":-3})
problemTc3p.setInitialValues({"P1":7,"T1":16,"dEI":0,"d":2,"-d":-2}) #TODO: vérifier avec les pbms de val
problemTc2t.setInitialValues({"P1":5,"T1":14,"dEI":0,"d":2,"-d":-2})
problemTc2p.setInitialValues({"P1":5,"T1":14,"dEI":0,"d":2,"-d":-2})
problemTc3t.setInitialValues({"P1":7,"T1":16,"dEI":0,"d":2,"-d":-2})
problemTc1p.setInitialValues({"P1":7,"T1":16,"dEI":0,"d":3,"-d":-3}) #TODO: vérifier avec les pbms de val

bank=problemBank() # TODO: oh never used right ?
bank.addPbms([ problemTc1t, problemTc1p, problemTc2t, problemTc2p, problemTc3t, problemTc3p, problemTc4t, problemTc4p, problemCc1t, problemCc1p, problemCc2t, problemCc2p, problemCc3t, problemCc3p, problemCc4t, problemCc4p,problemTc1t_v2, problemTc1p_v2, problemTc2t_v2, problemTc2p_v2, problemTc3t_v2, problemTc3p_v2, problemTc4t_v2, problemTc4p_v2, problemCc1t_v2, problemCc1p_v2, problemCc2t_v2, problemCc2p_v2, problemCc3t_v2, problemCc3p_v2, problemCc4t_v2, problemCc4p_v2])

# #=============================================================================
# # STEP 2 : SIMULATIONS
# #=============================================================================


reinterpretationModel_extended=ReinterpretationModel(numberOfReinterpretation=2,dropToTest=False)
reinterpretationModel=ReinterpretationModel(numberOfReinterpretation=1,dropToTest=False)
reinterpretationModel_direct=ReinterpretationModel(numberOfReinterpretation=1,dropToTest=False,excludeLateReinterpretations=True)
                                # Contains all the informations related to simulations

keywordSolver=KeywordSolver(extendedKeyWord=False)
keywordSolver_extended=KeywordSolver(extendedKeyWord=True)

if(alreadySimulated): # to avoid long time of computations, we can load and save a pickle file that can replace the simulation
    reinterpretationModel.pickleLoad(pickleFile) #TODO: no up to date at all
else:
    for problem in bank.dicPbm.values():
        keywordSolver.generateKeyWordBehaviour(problem)
        keywordSolver_extended.generateKeyWordBehaviour(problem)
        #reinterpretationModel.generateAllPossibilities(problem)
        #reinterpretationModel_extended.generateAllPossibilities(problem)
        reinterpretationModel_direct.generateAllPossibilities(problem)

    logging.info('The simulation took '+str(time.time()-start)+' seconds.')
#===============================================================================
#
# logging.info('keyword model : '+str(keywordSolver_extended))
# reinterpretationModel.pickleSave(newsimulation)
# reinterpretationModel.buildBigDic()
# reinterpretationModel.printCSV(csvFile=simulationDirectory+"simulation"+timestamp+".csv",hideUnsolved=True)
# reinterpretationModel.printCSV(csvFile=simulationDirectory+"simulationWithModel"+timestamp+".csv",hideModel=False,hideUnsolved=True)
# reinterpretationModel.printMiniCSV(csvFile=simulationDirectory+"Mini_simulation"+timestamp+".csv")
#===============================================================================
reinterpretationModel_direct.buildBigDic()
#===============================================================================
# STEP 3 : A priori generator : find all the possible operations with numbers
# being given
#===============================================================================

predictionSpace=PredictionSpace()
#TODO: These lines are ugly, it would have been better if process problem Banks
predictionSpace.processProblem("Tc1p",["T1","P1","d"],{"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3})
predictionSpace.processProblem("Cc1t",["T1","P1","d"],{"P1":5,"T1":12,"(T1+P1)":17,"zero":0,"d":3,"-d":-3})
predictionSpace.processProblem("Cc1p",["T1","P1","d"],{"P1":5,"T1":12,"(T1+P1)":17,"zero":0,"d":3,"-d":-3})
predictionSpace.processProblem("Cc2t",["T1","P1","d"],{"P1":6,"T1":15,"(T1+P1)":21,"zero":0,"d":2,"-d":-2})
predictionSpace.processProblem("Cc2p",["T1","P1","d"],{"P1":6,"T1":15,"(T1+P1)":21,"zero":0,"d":2,"-d":-2})
predictionSpace.processProblem("Cc3t",["T1","P1","d"],{"P1":6,"T1":15,"zero":0,"d":2,"-d":-2})
predictionSpace.processProblem("Cc3p",["T1","P1","d"],{"P1":6,"T1":15,"zero":0,"d":2,"-d":-2})
predictionSpace.processProblem("Cc4t",["T1","P1","d"],{"P1":9,"T1":14,"zero":0,"d":2,"-d":-2})
predictionSpace.processProblem("Cc4p",["T1","P1","d"],{"P1":9,"T1":14,"zero":0,"d":2,"-d":-2})
predictionSpace.processProblem("Tc4t",["T1","P1","d"],{"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3})
predictionSpace.processProblem("Tc4p",["T1","P1","d"],{"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3})
predictionSpace.processProblem("Tc1t",["T1","P1","d"],{"P1":7,"T1":16,"dEI":0,"d":3,"-d":-3})
predictionSpace.processProblem("Tc3p",["T1","P1","d"],{"P1":7,"T1":16,"dEI":0,"d":3,"-d":-3})
predictionSpace.processProblem("Tc2t",["T1","P1","d"],{"P1":5,"T1":14,"dEI":0,"d":2,"-d":-2})
predictionSpace.processProblem("Tc2p",["T1","P1","d"],{"P1":5,"T1":14,"dEI":0,"d":2,"-d":-2})
predictionSpace.processProblem("Tc3t",["T1","P1","d"],{"P1":7,"T1":16,"dEI":0,"d":2,"-d":-2})
predictionSpace.processProblem("Tc1p",["T1","P1","d"],{"P1":7,"T1":16,"dEI":0,"d":2,"-d":-2})


predictionSpace.processProblem("Cc1t_v2",["T1","P1","d"],{"P1":7,"T1":16,"(T1+P1)":23,"zero":0,"d":4,"-d":-4})
predictionSpace.processProblem("Cc1p_v2",["T1","P1","d"],{"P1":7,"T1":16,"(T1+P1)":23,"zero":0,"d":4,"-d":-4})
predictionSpace.processProblem("Cc2t_v2",["T1","P1","d"],{"P1":9,"T1":15,"(T1+P1)":24,"zero":0,"d":4,"-d":-4})
predictionSpace.processProblem("Cc2p_v2",["T1","P1","d"],{"P1":9,"T1":15,"(T1+P1)":24,"zero":0,"d":4,"-d":-4})
predictionSpace.processProblem("Cc3t_v2",["T1","P1","d"],{"P1":9,"T1":17,"zero":0,"d":3,"-d":-3})
predictionSpace.processProblem("Cc3p_v2",["T1","P1","d"],{"P1":9,"T1":17,"zero":0,"d":3,"-d":-3})
predictionSpace.processProblem("Cc4t_v2",["T1","P1","d"],{"P1":7,"T1":15,"zero":0,"d":3,"-d":-3})
predictionSpace.processProblem("Cc4p_v2",["T1","P1","d"],{"P1":7,"T1":15,"zero":0,"d":3,"-d":-3})

predictionSpace.processProblem("Tc4t_v2",["T1","P1","d"],{"P1":7,"T1":12,"dEI":0,"d":3,"-d":-3})
predictionSpace.processProblem("Tc4p_v2",["T1","P1","d"],{"P1":7,"T1":12,"dEI":0,"d":3,"-d":-3})
predictionSpace.processProblem("Tc1t_v2",["T1","P1","d"],{"P1":6,"T1":15,"dEI":0,"d":4,"-d":-4})
predictionSpace.processProblem("Tc3p_v2",["T1","P1","d"],{"P1":6,"T1":13,"dEI":0,"d":2,"-d":-2})
predictionSpace.processProblem("Tc2t_v2",["T1","P1","d"],{"P1":5,"T1":14,"dEI":0,"d":2,"-d":-2})
predictionSpace.processProblem("Tc2p_v2",["T1","P1","d"],{"P1":5,"T1":14,"dEI":0,"d":2,"-d":-2})
predictionSpace.processProblem("Tc3t_v2",["T1","P1","d"],{"P1":6,"T1":13,"dEI":0,"d":2,"-d":-2})
predictionSpace.processProblem("Tc1p_v2",["T1","P1","d"],{"P1":6,"T1":15,"dEI":0,"d":4,"-d":-4})

#===============================================================================
# STEP 4 : Read empiricical datas
#===============================================================================

## We read the dataset of formulas (children answers)
obsdic=globalEmpiricalDic()
obsdic.readCsv("mergedDatas_final_separated_recoded.csv",recodeOneliner=True)


# #=============================================================================
# # STEP 5 : Compare empirical datas with simulated datas (keyword and reinterpretations)
# # using the a priori formula dataset
# #=============================================================================

#===============================================================================
# rModelPredictions=reinterpretationModel.extractPredictions(excludeUnsolvingProcesses=True)
# rModelPredictions_extended=reinterpretationModel_extended.extractPredictions(excludeUnsolvingProcesses=True)
rModelPredictions_direct=reinterpretationModel_direct.extractPredictions(predictionSpace)
#===============================================================================
kModelPredictions_extended=keywordSolver_extended.extractPredictions(predictionSpace)
kModelPredictions=keywordSolver.extractPredictions(predictionSpace)

pm=predictionsManager()#pm.
pm.addPredictionsSpace(predictionSpace)
#pm.addModelPredictions(rModelPredictions,"ReinterpretationModel")
pm.addModelPredictions(kModelPredictions,"KeywordModel")
#pm.addModelPredictions(rModelPredictions_extended,"ReinterpretationModel_extended")
pm.addModelPredictions(kModelPredictions_extended,"KeywordModel_extended")
pm.addModelPredictions(rModelPredictions_direct,"ReinterpretationModel_direct")
pm.addEmpiricalDatas(obsdic)

formulasToExclude=reinterpretationModel_direct.findFormulas(models=['goodAnswers'])
logging.info(formulasToExclude)
pm.printCSVModelComparison(simulationDirectory+"simulations_versus_observations_noExclusion"+timestamp+".csv",formulasToExclude) # print the csv which will be used for R analysis
pm.listAndCompare(obsdic)
with open(simulationDirectory+"pickle_DUMP",'wb') as f:
    pickle.dump([pm,kModelPredictions,kModelPredictions_extended],f)


#===============================================================================
# POST_EVALUATION -- (experimental)
#===============================================================================
#===============================================================================
# weight_eval=weightEvaluator()
# weight_eval.prepareStructure(bank)
# weight_eval.bindConfrontationToPathsDatas(d2,reinterpretationModel.datasDic)#simDatasDic
# weight_eval.normaliseWeightByPbm()
# weight_eval.printCSV(simulationDirectory+"weightAnalysis"+timestamp+".csv")
#===============================================================================

