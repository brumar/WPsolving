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
import csv
import datetime
import time
import os
import logging


simulationName=raw_input("simulation Name ? : ")
#simulationName=""
start = time.time()
timeformat='%Y_%m_%d__%H_%M_%S'
timestamp = datetime.datetime.fromtimestamp(start).strftime(timeformat)
simulationDirectory="simulations/"+timestamp+"_"+simulationName+"/"
os.makedirs(simulationDirectory)

## GLOBAL OPTIONS
alreadySimulated=False
pickleFile="simulation24072014.pkl"
newsimulation=simulationDirectory+"simulation"+timestamp+".pkl"

## LOGGING
logging.basicConfig(filename=simulationDirectory+'simulation.log',level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt=timeformat)
logging.getLogger().addHandler(logging.StreamHandler())

class SimulationAprioribinderDic():
    """
    bind datas from simulations and from apriori generators
    tell if a formula is found or not in the simulations
    """
    def __init__(self,globalAprioriDic,simulation):
        self.dicPbmSetFormulaPlanned={}
        for pbm in simulation.iterkeys():
            aprioriDic=globalAprioriDic.problemDic[pbm]
            self.dicPbmSetFormulaPlanned[pbm]={}
            for formula in aprioriDic.formulaTosetDic.iterkeys():
                setName=aprioriDic.formulaTosetDic[formula]
                if setName not in self.dicPbmSetFormulaPlanned[pbm].keys():
                    self.dicPbmSetFormulaPlanned[pbm][setName]={}
                planned=(formula in simulation[pbm])
                self.dicPbmSetFormulaPlanned[pbm][setName][formula]=planned



def generateAllPossibilities(problem,dropToTest=False,
                             unorderedSteps=[Solver.INTERP,Solver.SCHEMA,Solver.SCHEMA,Solver.SCHEMA],
                             breakPreviousInterpretations="undefined"):
    """
    The main function of this program, generate all the paths possible for a problem
    Some options have to be apparent in new development.
    The option "breakPreviousInterpretations" is set at True AND False
    by the optionsFactory script. New developpments should
    to find as much as paths as possible.
    """
    logging.info(problem.name)
    global simulatedDatas #BAD LINE TODO:Fix this


    c1=IntervalConstraint(['GAIN','Minus'],operations.allowsNegativeValues)
    upD=Updater(problem)
    upD.startAsUnderstood()

    # we add the model of goodAnswers, we want to be able to
    # keep them for later
    model="goodAnswers"
    constraints=[c1]
    solver=Solver(upD,constraints)
    solver.generalSequentialSolver(listOfActions=[Solver.SOLVER]) # = just solve
    solver.TreePaths.scanTree()
    #logging.info(solver.TreePaths.treeOutput)
    simulatedDatas.addDataSet(solver.TreePaths.pathList,problem.name,model)
    logging.info("DONE : model "+model)

    optionsList=optionsFactory(unorderedSteps) # will generate all the options possible with 2 interpretations step randomly occuring
    for i,options in enumerate(optionsList) :
        if (not dropToTest) or (i%3==0): # [condition for debugging purpose]
                                        # if dropToTest is True, then only 1 third of the possibilities generated by optionsFactory will be investigated
            model=str(options[0])
            if(breakPreviousInterpretations!="undefined"):
                options[1]=breakPreviousInterpretations
            c2=BehavioralConstraint(breakPreviousInterpretations=options[1])
            constraints=[c1,c2]
            solver=Solver(upD,constraints)
            solver.generalSequentialSolver(listOfActions=options[0])
            solver.TreePaths.scanTree()
            #logging.info(solver.TreePaths.treeOutput)
            simulatedDatas.addDataSet(solver.TreePaths.pathList,problem.name,model)
            logging.info("DONE : model "+model+"( "+str(i)+" )")


#===============================================================================
# STEP 1 : Create problems
#===============================================================================

#=================PROBLEME 1 : Tc4t=============================================
#===============================================================================
# Au supermarch�, le kilo de poisson a augment� de 5 euros cette ann�e.
# Un kilo de poisson co�te maintenant 12 euros.
# Au d�but de l'ann�e, le kilo de viande co�tait le m�me prix que le kilo de poisson.
# Le kilo de viande a augment� de 3 euros de moins que le kilo de poisson.
# Combien co�te le kilo de viande maintenant ?
#===============================================================================


schema1=Schema("PoissonEF","PoissonEI",operations.addition,"PoissonGAIN","change")
schema2=Schema("ViandeEF","ViandeEI",operations.addition,"ViandeGAIN","change")
struct=ProblemStructure()
struct.addSchema(schema1)
struct.addSchema(schema2)
struct.addBridgingSchemas(schema1,schema2)
struct.updateObjectSet()

text=Text()
text.addTextInformation(TextInformation(Representation(Quantity("PoissonGAIN","P1"),'Au supermarch�, le kilo de poisson a augment� de 5 euros cette ann�e')))
text.addTextInformation(TextInformation(Representation(Quantity("PoissonEF","T1"),'Un kilo de poisson coute maintenant 12 euros.')))
text.addTextInformation(TextInformation(Representation(Quantity("PoissonEIminusViandeEI","dEI"),'Au d�but de l\'ann�e, le kilo de viande coutait le m�me prix que le kilo de poisson.')))
text.addTextInformation(TextInformation(Representation(Quantity("PoissonGAINminusViandeGAIN","d"),'Le kilo de viande a augment� de 3 euros de moins que le kilo de poisson')))
text.setGoal(TextGoal(Goal('ViandeEF','Combien coute le kilo de viande maintenant?')))

text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEI","P1"),'Au supermarch�, le kilo de poisson �tait de 5 euros'))
text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEF","P1"),'Au supermarch�, le kilo de poisson coute 5 euros'))
text.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("PoissonEI","T1"),'Un kilo de poisson �tait de 12 euros.'))
text.getTextInformation(2).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","dEI"),'Au la fin de l\'ann�e, le kilo de viande coute le m�me prix que le kilo de poisson.'))
text.getTextInformation(2).addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","dEI"),'Le kilo de viande a augment� du m�me prix que le kilo de poisson.'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","d"),'Le kilo de viande a augment� de 3 euros'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","-d"),'Le kilo de viande a diminu� de 3 euros'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","-d"),'Le kilo de viande a augment� de 3 euros de plus que le kilo de poisson'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","d"),'Le kilo de viande vaut 3 euros de moins que le kilo de poisson'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","-d"),'Le kilo de viande vaut 3 euros de plus que le kilo de poisson'))
text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeEF","d"),'Le kilo coute 3 euros � la fin'))
problemTc4t=Problem(struct,text)
problemTc4t.name="Tc4t"



#===============PROBLEME 2 : Tc1t ====================================================
#==============================================================================
# Pendant la r�cr�ation, Lucas gagne 7 billes.
# Apr�s la r�cr�ation, Lucas a 16 billes.
# Avant la r�cr�ation, Simon avait autant de billes que Lucas.
# Pendant la r�cr�ation, Simon gagne 3 billes de moins que Lucas.
# Combien Simon a-t-il de billes apr�s la r�cr�ation ?
#===============================================================================
problemTc1t=copy.deepcopy(problemTc4t)
problemTc1t.name="Tc1t"
keydic={"Poisson":"Lucas","Viande":"Simon"}
problemTc1t.renameKeywordObjects(keydic)
newrep=Representation(Quantity("LucasGAIN","T1"),'Apr�s la r�cr�ation, Lucas gagne 16 billes')
problemTc1t.text.getTextInformation(1).addAlternativeRepresentation(newrep)


#===============PROBLEME 3 : Tc2t ============================================
# Cette ann�e, Th�o a �t� pes� par le p�diatre.
# Th�o a pris 5 kilos depuis le d�but de l�ann�e.
# Th�o p�se maintenant 14 kilos.
# Au d�but de l�ann�e, Nicolas pesait le m�me poids que Th�o.
# Nicolas a pris 2 kilos de moins que Th�o cette ann�e.
# Combien Nicolas p�se-t-il maintenant�?
#===============================================================================

problemTc2t=copy.deepcopy(problemTc4t)
problemTc2t.name="Tc2t"
keydic={"Viande":"Th�o","Poisson":"Nicolas"}
problemTc2t.renameKeywordObjects(keydic) # no difference with pbm1 concerning possible alternative representations
problemTc2t.text.getTextInformation(2).removeAlternativeRepresentations()
newrep=Representation(Quantity("NicolasEFminusTh�oEF","dEI"),'A la fin de l\'ann�e Nicolas pesait le m�me poids que Th�o')
problemTc2t.text.getTextInformation(2).addAlternativeRepresentation(newrep)

#===============PROBLEME 4 : Tc3t ============================================
#===============================================================================
# En janvier, 7 enfants se sont inscrits � la chorale.
# Apr�s janvier, il y a 16 enfants � la chorale.
# Avant janvier, il y avait autant d'enfants inscrits au football qu'� la chorale.
# En janvier, il y a eu 2 inscriptions de moins au football qu'� la chorale.
# Combien y a-t-il d'enfants au football apr�s janvier ?
#===============================================================================

problemTc3t=copy.deepcopy(problemTc4t)
problemTc3t.name="Tc3t"
keydic={"Viande":"football","Poisson":"chorale"}
problemTc3t.renameKeywordObjects(keydic)
newrep=Representation(Quantity("choraleGAIN","T1"),'')
problemTc3t.text.getTextInformation(1).addAlternativeRepresentation(newrep)


#===============PROBLEME 1p : Tc4p  =============================================
#===============================================================================
# Au supermarch�, le kilo de poisson a augment� de 5 euros cette ann�e.
# Un kilo de poisson co�te maintenant 12 euros.
# Au d�but de l'ann�e, le kilo de viande co�tait le m�me prix que le kilo de poisson.
# Le kilo de viande co�te maintenant 3 euros de moins que le kilos de poisson.
# De combien d'euros le kilo de viande a-t-il augment� ?
#===============================================================================


problemTc4p=copy.deepcopy(problemTc4t)
problemTc4p.name="Tc4p"
info3_prime=TextInformation(Representation(Quantity("PoissonEFminusViandeEF","d"),'Le kilo de viande vaut 3 euros de moins que le kilo de poisson'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","d"),'Le kilo de viande a augment� de 3 euros'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","-d"),'Le kilo de viande a diminu� de 3 euros'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","-d"),'Le kilo de viande a augment� de 3 euros de plus que le kilo de poisson'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","d"),'Le kilo de viande a augment� de 3 euros de moins que le kilo de poisson'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","-d"),'Le kilo de viande vaut 3 euros de plus que le kilo de poisson'))
info3_prime.addAlternativeRepresentation(Representation(Quantity("ViandeEF","d"),'Le kilo coute 3 euros � la fin'))
problemTc4p.text.textInformations[3]=info3_prime
problemTc4p.text.setGoal(TextGoal(Goal('ViandeGAIN','De combien le kilo de viande a t-il augment� ?')))

#===============PROBLEME 2p : Tc3p  =============================================
#===============================================================================
# En janvier, 7 enfants se sont inscrits � la chorale.
# Apr�s janvier, il y a 16 enfants � la chorale.
# Avant janvier, il y avait autant d'enfants inscrits au football qu'� la chorale.
# En janvier, il y a eu de nouvelles inscriptions au football.
# Apr�s janvier, il y a 2 enfants de moins au football qu'� la chorale.
# Combien d'enfants se sont inscrits au football en janvier ?
#===============================================================================
#===============================================================================
problemTc3p=copy.deepcopy(problemTc4p)
problemTc3p.name="Tc3p"
keydic={"Viande":"football","Poisson":"chorale"}
problemTc3p.renameKeywordObjects(keydic)
newrep=Representation(Quantity("choraleGAIN","T1"),'')
problemTc3p.text.getTextInformation(1).addAlternativeRepresentation(newrep)


#===============PROBLEME 3p : Tc2p  ============================================
#===============================================================================
# Cette ann�e, Th�o a �t� pes� par le p�diatre.
# Th�o a pris 5 kilos depuis le d�but de l�ann�e.
# Th�o p�se maintenant 14 kilos.
# Au d�but de l�ann�e, Nicolas pesait le m�me poids que Th�o.
# Maintenant, Nicolas p�se 2 kilos de moins que Th�o.
# Combien de kilos Nicolas a-t-il pris cette ann�e�?
#===============================================================================
#===============================================================================
problemTc2p=copy.deepcopy(problemTc4p)
problemTc2p.name="Tc2p"
keydic={"Viande":"Th�o","Poisson":"Nicolas"}
problemTc2p.renameKeywordObjects(keydic) # no difference with pbm1 concerning possible alternative representations
problemTc2p.text.getTextInformation(2).removeAlternativeRepresentations()
newrep=Representation(Quantity("NicolasEFminusTh�oEF","dEI"),'A la fin de l\'ann�e Nicolas pesait le m�me poids que Th�o')
problemTc2p.text.getTextInformation(2).addAlternativeRepresentation(newrep)

#===============PROBLEME 4p : Tc1p  =============================================
#===============================================================================
# Pendant la r�cr�ation, Lucas gagne 7 billes.
# Apr�s la r�cr�ation, Lucas a 16 billes.
# Avant la r�cr�ation, Simon avait autant de billes que Lucas.
# Pendant la r�cr�ation, Simon gagne des billes,
# et apr�s la r�cr�ation, il a 3 billes de moins que Lucas.
# Combien Simon a-t-il gagn� de billes pendant la r�cr�ation ?
#===============================================================================
#===============================================================================

problemTc1p=copy.deepcopy(problemTc4p)
problemTc1p.name="Tc1p"
keydic={"Poisson":"Lucas","Viande":"Simon"}
problemTc1p.renameKeywordObjects(keydic)
newrep=Representation(Quantity("LucasGAIN","T1"),'Apr�s la r�cr�ation, Lucas gagne 16 billes')
problemTc1p.text.getTextInformation(1).addAlternativeRepresentation(newrep)

#===============================================================================
# Cc1t
# Antoine a 5 billes. Quand Antoine r�unit ses billes avec celles de Paul, ils ont 12 billes ensemble.
# Paul r�unit ses billes avec celles de Jacques.
# Jacques a 3 billes de moins qu�Antoine.
# Combien Paul et Jacques ont-ils de billes ensemble ?
#===============================================================================

schema1Cc1t=Schema(qf="AntoineETPaul",q1="Paul",operation=operations.addition,q2="Antoine",name="combinaison")
schema2Cc1t=Schema(qf="JacquesETPaul",q1="Paul",operation=operations.addition,q2="Jacques",name="combinaison")
structCc1t=ProblemStructure()
structCc1t.addSchema(schema1Cc1t)
structCc1t.addSchema(schema2Cc1t)
structCc1t.addBridgingSchemas(schema1Cc1t,schema2Cc1t)
structCc1t.updateObjectSet()

textCc1t=Text()
textCc1t.addTextInformation(TextInformation(Representation(Quantity("Antoine","P1"),'Antoine a 5 billes')))
textCc1t.addTextInformation(TextInformation(Representation(Quantity("AntoineETPaul","T1"),'Quand Antoine r�unit ses billes avec celles de Paul, ils ont 12 billes ensemble')))
textCc1t.addTextInformation(TextInformation(Representation(Quantity("PaulminusPaul","zero"),'Ce sont les m�mes "Paul"')))
textCc1t.addTextInformation(TextInformation(Representation(Quantity("AntoineminusJacques","d"),'Le kilo de viande a augment� de 3 euros de moins que le kilo de poisson')))
textCc1t.setGoal(TextGoal(Goal('JacquesETPaul','Combien Paul et Jacques ont-ils de billes ensemble ?')))


textCc1t.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("Paul","T1"),'Quand Antoine r�unit ses billes avec celles de Paul qui a 12 billes'))
textCc1t.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("Antoine","T1"),'Antoine recoit des billes de Paul, maintenant il en a 12'))
#=============== MISE A L ECART : VOLONTE DE SIMPLIFIER ======================
# textCc1t.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("Antoine","(T1+P1)"),'Antoine recoit 12 billes de Paul'))
# textCc1t.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("Antoine","zero"),'Antoine donne ses billes de Paul, maintenant il en a 12'))
# textCc1t.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("Paul","zero"),'Paul donne ses billes a Antoine, maintenant il en a 12'))
#===============================================================================

textCc1t.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("Jacques","d"),'Jacques a trois billes'))
textCc1t.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("AntoineminusJacques","-d"),'Antoine a trois billes de plus'))
#textCc1t.getTextInformation(2).addAlternativeRepresentation(Representation(Quantity("Antoine","T1"),'Antoine recoit des billes de Paul, maintenant il en a 3'))
textCc1t.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("Paul","zero"),'Antoine recoit des billes de Paul....'))

problemCc1t=Problem(structCc1t,textCc1t)
problemCc1t.name="Cc1t"

#===============================================================================
# c1=IntervalConstraint(['GAIN','Minus'],operations.allowsNegativeValues)
# c2=BehavioralConstraint(breakPreviousInterpretations=False) # when True, the old representation of the text information is still available
# upD=Updater(problemCc1t)
# upD.startAsUnderstood()
# constraints=[c1,c2]
# solver=Solver(upD,constraints)
# solver.generalSequentialSolver(listOfActions=[1,1,3])
# solver.TreePaths.scanTree()
# logging.info(solver.TreePaths.treeOutput)
#===============================================================================

#===============================================================================
# Cc1p
# Antoine a 5 billes. Quand Antoine r�unit ses billes avec celles de Paul, ils ont 12 billes ensemble.
# Quand Paul et Jacques r�unissent leurs billes, cela fait 3 billes de moins.
# Combien Jacques a-t-il de billes ?
#===============================================================================
problemCc1p=copy.deepcopy(problemCc1t)
problemCc1p.name="Cc1p"
infoCC1p_3=TextInformation(Representation(Quantity("AntoineETPaulminusJacquesETPaul","d"),'Quand Paul et Jacques r�unissent leurs billes, cela fait 3 billes de moins'))
infoCC1p_3.addAlternativeRepresentation(Representation(Quantity("AntoineETPaulminusJacquesETPaul","-d"),'Quand Paul et Jacques r�unissent leurs billes, cela fait 3 billes de plus'))
infoCC1p_3.addAlternativeRepresentation(Representation(Quantity("JacquesETPaul","d"),'Quand Paul et Jacques r�unissent leurs billes, cela fait 3 billes'))
infoCC1p_3.addAlternativeRepresentation(Representation(Quantity("Paul","zero"),'Paul donne ses billes � Jacques....'))
infoCC1p_3.addAlternativeRepresentation(Representation(Quantity("Jacques","zero"),'Paul donne ses billes � Jacques....'))
infoCC1p_3.addAlternativeRepresentation(Representation(Quantity("Paul","d"),'d'))
infoCC1p_3.addAlternativeRepresentation(Representation(Quantity("Jacques","d"),'d'))
problemCc1p.text.textInformations[3]=infoCC1p_3
problemCc1p.text.setGoal(TextGoal(Goal('Jacques','Combien Jacques a-t-il de billes ?')))

#===============================================================================
# Cc2t
# Quand Medor monte sur la balance chez le v�t�rinaire, la balance indique 6 kilos.
# Quand Medor et Rex montent ensemble sur la balance chez le v�t�rinaire, la balance indique 15 kilos.
# Fido et Rex montent ensemble sur la balance chez le v�t�rinaire. Fido p�se 2 kilos de moins que Medor.
# Combien Fido et Rex p�sent-ils ensemble ?
#===============================================================================
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
# text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEI","P1"),'Au supermarch�, le kilo de poisson �tait de 5 euros'))
# text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("PoissonEF","P1"),'Au supermarch�, le kilo de poisson coute 5 euros'))
# text.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("PoissonEI","T1"),'Un kilo de poisson �tait de 12 euros.'))
# text.getTextInformation(2).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","dEI"),'Au la fin de l\'ann�e, le kilo de viande coute le m�me prix que le kilo de poisson.'))
# text.getTextInformation(2).addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","dEI"),'Le kilo de viande a augment� du m�me prix que le kilo de poisson.'))
# text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","d"),'Le kilo de viande a augment� de 3 euros'))
# text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeGAIN","-d"),'Le kilo de viande a diminu� de 3 euros'))
# text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonGAINminusViandeGAIN","-d"),'Le kilo de viande a augment� de 3 euros de plus que le kilo de poisson'))
# text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","d"),'Le kilo de viande vaut 3 euros de moins que le kilo de poisson'))
# text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("PoissonEFminusViandeEF","-d"),'Le kilo de viande vaut 3 euros de plus que le kilo de poisson'))
# text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("ViandeEF","d"),'Le kilo coute 3 euros � la fin'))
# problemTc4t=Problem(struct,text)
# problemTc4t.name="Tc4t"
#===============================================================================


#===============================================================================
# Cc2p
# Quand Medor monte sur la balance chez le v�t�rinaire, la balance indique 6 kilos.
# Quand Medor et Rex montent ensemble sur la balance chez le v�t�rinaire, la balance indique 15 kilos.
# Lorsque Fido et Rex montent sur la balance ensemble, la balance indique 2 kilos de moins.
# Combien p�se Fido�?
#===============================================================================
problemCc2p=copy.deepcopy(problemCc1p)
problemCc2p.name="Cc2p"
keydic={"Antoine":"Medor","Paul":"Rex","Jacques":"Fido"}
problemCc2p.renameKeywordObjects(keydic)

problemCc2p.text.getTextInformation(1).removeAlternativeRepresentations()
problemCc2p.text.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("Medor","T1"),''))
problemCc2p.text.getTextInformation(1).addAlternativeRepresentation(Representation(Quantity("Rex","T1"),''))

problemCc2p.text.getTextInformation(3).removeAlternativeRepresentations()
problemCc2p.text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("MedorETRexminusFidoETRex","-d"),'Quand Rex et Fido r�unissent leurs billes, cela fait 3 billes de plus'))
problemCc2p.text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("FidoETRex","d"),'Quand Rex et Fido r�unissent leurs billes, cela fait 3 billes'))
problemCc2p.text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("Rex","d"),'d'))
problemCc2p.text.getTextInformation(3).addAlternativeRepresentation(Representation(Quantity("Fido","d"),'d'))

#===============================================================================
# Cc3t
# Dans la classe de CM2, il y a 6 �l�ves. Si on r�unit les CM2 et les CM1, cela fait un groupe de 15 �l�ves.
# On fait un groupe r�unissant les CE2 et les CM1. Dans la classe de CE2, il y a 2 �l�ves de moins qu'en CM2.
# Combien y a-t-il d'�l�ves dans le groupe r�unissant les CE2 et les CM1 ?
#===============================================================================
problemCc3t=copy.deepcopy(problemCc2t)
problemCc3t.name="Cc3t"
keydic={"Medor":"CM2","Rex":"CM1","Fido":"CE2"}
problemCc3t.renameKeywordObjects(keydic)

#===============================================================================
# Cc3p
# Dans la classe de CM2, il y a 6 �l�ves. Si on r�unit les CM2 et les CM1, cela fait un groupe de 15 �l�ves.
# Si on r�unit les CE2 et les CM1, le groupe a 2 �l�ves de moins.
# Combien y a-t-il d'�l�ves en CE2 ?
#===============================================================================
problemCc3p=copy.deepcopy(problemCc2p)
problemCc3p.name="Cc3p"
keydic={"Medor":"CM2","Rex":"CM1","Fido":"CE2"}
problemCc3p.renameKeywordObjects(keydic)

#===============================================================================
# Cc4t
# Un livre co�te 9 euros. Si on ach�te un livre et une r�gle, on paie 14 euros.
# On ach�te une r�gle et un cahier. Le cahier co�te 2 euros de moins que le livre.
# Combien co�tent la r�gle et le cahier ensemble ?
#===============================================================================
problemCc4t=copy.deepcopy(problemCc2t)
problemCc4t.name="Cc4t"
keydic={"Medor":"livre","Rex":"regle","Fido":"cahier"}
problemCc4t.renameKeywordObjects(keydic)
problemCc4t.text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("cahier","P1"),''))

#===============================================================================

# Cc4p
# Un livre co�te 9 euros. Si on ach�te un livre et une r�gle, on paie 14 euros.
# On ach�te une r�gle et un cahier. Cela co�te 2 euros de moins que lorsque l'on ach�te un livre et une r�gle.
# Combien co�te le cahier ?
#===============================================================================
problemCc4p=copy.deepcopy(problemCc2p)
problemCc4p.name="Cc4p"
keydic={"Medor":"livre","Rex":"regle","Fido":"cahier"}
#problemCc3t.renameKeywordObjects(keydic)
#problemCc4t.text.getTextInformation(0).addAlternativeRepresentation(Representation(Quantity("cahier","P1"),''))


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
problemTc3p.setInitialValues({"P1":7,"T1":16,"dEI":0,"d":3,"-d":-3})
problemTc2t.setInitialValues({"P1":5,"T1":14,"dEI":0,"d":2,"-d":-2})
problemTc2p.setInitialValues({"P1":5,"T1":14,"dEI":0,"d":2,"-d":-2})
problemTc3t.setInitialValues({"P1":7,"T1":16,"dEI":0,"d":2,"-d":-2})
problemTc1p.setInitialValues({"P1":7,"T1":16,"dEI":0,"d":2,"-d":-2})

bank=problemBank()
bank.addPbms([ problemTc1t, problemTc1p, problemTc2t, problemTc2p, problemTc3t, problemTc3p, problemTc4t, problemTc4p, problemCc1t, problemCc1p, problemCc2t, problemCc2p, problemCc3t, problemCc3p, problemCc4t, problemCc4p])

# #=============================================================================
# # STEP 2 : SIMULATIONS
# #=============================================================================



simulatedDatas=SimulatedDatas() # Most important instance of the programm
                                # Contains all the informations related to simulations
if(alreadySimulated): # to avoid long time of computations, we can load and save a pickle file that can replace the simulation
    simulatedDatas.pickleLoad(pickleFile)
else:
    generateAllPossibilities(problemTc1p,dropToTest=False)
    generateAllPossibilities(problemTc1t,dropToTest=False)
    generateAllPossibilities(problemTc2t,dropToTest=False)
    generateAllPossibilities(problemTc2p,dropToTest=False)
    generateAllPossibilities(problemTc3t,dropToTest=False)
    generateAllPossibilities(problemTc3p,dropToTest=False)
    generateAllPossibilities(problemTc4t,dropToTest=False)
    generateAllPossibilities(problemTc4p,dropToTest=False)
    generateAllPossibilities(problemCc1t,dropToTest=False)
    generateAllPossibilities(problemCc1p,dropToTest=False)
    generateAllPossibilities(problemCc2t,dropToTest=False)
    generateAllPossibilities(problemCc2p,dropToTest=False)
    generateAllPossibilities(problemCc3t,dropToTest=False)
    generateAllPossibilities(problemCc3p,dropToTest=False)
    generateAllPossibilities(problemCc4t,dropToTest=False)
    generateAllPossibilities(problemCc4p,dropToTest=False)


    logging.info('The simulation took '+str(time.time()-start)+' seconds.')

simulatedDatas.pickleSave(newsimulation)
simulatedDatas.buildBigDic()
simulatedDatas.printCSV(csvFile=simulationDirectory+"simulation"+timestamp+".csv",hideUnsolved=True)
simulatedDatas.printCSV(csvFile=simulationDirectory+"simulationWithModel"+timestamp+".csv",hideModel=False,hideUnsolved=True)
simulatedDatas.printMiniCSV(csvFile=simulationDirectory+"Mini_simulation"+timestamp+".csv")


#===============================================================================
# STEP 3 : A priori generator : find all the possible operations with numbers
# being given
#===============================================================================

aprioDIC=GlobalAprioriDic()
aprioDIC.addProblem("Tc1p",["T1","P1","d"],{"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3})
aprioDIC.addProblem("Cc1t",["T1","P1","d"],{"P1":5,"T1":12,"(T1+P1)":17,"zero":0,"d":3,"-d":-3})
aprioDIC.addProblem("Cc1p",["T1","P1","d"],{"P1":5,"T1":12,"(T1+P1)":17,"zero":0,"d":3,"-d":-3})
aprioDIC.addProblem("Cc2t",["T1","P1","d"],{"P1":6,"T1":15,"(T1+P1)":21,"zero":0,"d":2,"-d":-2})
aprioDIC.addProblem("Cc2p",["T1","P1","d"],{"P1":6,"T1":15,"(T1+P1)":21,"zero":0,"d":2,"-d":-2})
aprioDIC.addProblem("Cc3t",["T1","P1","d"],{"P1":6,"T1":15,"zero":0,"d":2,"-d":-2})
aprioDIC.addProblem("Cc3p",["T1","P1","d"],{"P1":6,"T1":15,"zero":0,"d":2,"-d":-2})
aprioDIC.addProblem("Cc4t",["T1","P1","d"],{"P1":9,"T1":14,"zero":0,"d":2,"-d":-2})
aprioDIC.addProblem("Cc4p",["T1","P1","d"],{"P1":9,"T1":14,"zero":0,"d":2,"-d":-2})
aprioDIC.addProblem("Tc4t",["T1","P1","d"],{"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3})
aprioDIC.addProblem("Tc4p",["T1","P1","d"],{"P1":5,"T1":12,"dEI":0,"d":3,"-d":-3})
aprioDIC.addProblem("Tc1t",["T1","P1","d"],{"P1":7,"T1":16,"dEI":0,"d":3,"-d":-3})
aprioDIC.addProblem("Tc3p",["T1","P1","d"],{"P1":7,"T1":16,"dEI":0,"d":3,"-d":-3})
aprioDIC.addProblem("Tc2t",["T1","P1","d"],{"P1":5,"T1":14,"dEI":0,"d":2,"-d":-2})
aprioDIC.addProblem("Tc2p",["T1","P1","d"],{"P1":5,"T1":14,"dEI":0,"d":2,"-d":-2})
aprioDIC.addProblem("Tc3t",["T1","P1","d"],{"P1":7,"T1":16,"dEI":0,"d":2,"-d":-2})
aprioDIC.addProblem("Tc1p",["T1","P1","d"],{"P1":7,"T1":16,"dEI":0,"d":2,"-d":-2})

#===============================================================================
# STEP 4 : Read empiricical datas
#===============================================================================

## We read the dataset of formulas (children answers)
obsdic=globalEmpiricalDic()
obsdic.readCsv("mergedDatas_final.csv")


# #=============================================================================
# # STEP 5 : Compare empirical datas with simulated datas using the a priori
# # formula dataset
# #=============================================================================

simulationDic=simulatedDatas.buildMiniDic(excludeUnsolvingProcesses=True)
sim=SimulationAprioribinderDic(aprioDIC,simulationDic)
d2=SimulationAprioriEmpiricbinderDic(sim,obsdic)
formulasToExclude=simulatedDatas.findFormulas(models=['goodAnswers','[1, 2, 2, 2, 3]'])
formulasToExclude2=simulatedDatas.findFormulas(models=['goodAnswers'])
logging.info(formulasToExclude2)
#d2.listAndCompare(sim,obsdic)
d2.printCSV(simulationDirectory+"simulations_versus_observations_exclusionOfLateReinterpretations"+timestamp+".csv",formulasToExclude) # print the csv which will be used for R analysis
d2.printCSV(simulationDirectory+"simulations_versus_observations_noExclusion"+timestamp+".csv",formulasToExclude2) # print the csv which will be used for R analysis


#===============================================================================
# POST_EVALUATION -- (experimental)
#===============================================================================
weight_eval=weightEvaluator()
weight_eval.prepareStructure(bank)
weight_eval.bindConfrontationToPathsDatas(d2,simulatedDatas.datasDic)#simDatasDic
weight_eval.normaliseWeightByPbm()
weight_eval.printCSV(simulationDirectory+"weightAnalysis"+timestamp+".csv")

