# -*- coding: cp1252 -*-
import operations
import itertools
import re
import copy
'''
Created on 30 avr. 2015

@author: Nevrose
'''

dicSignKeyword={"augment":operations.addition,"moins": operations.soustraction,
                "plus": operations.addition,"dimin": operations.soustraction,
                "gagne":operations.addition,"reÃ§oit":operations.addition}


dicSignKeywordExtended={ "pris": operations.addition,"ensemble": operations.addition,
                        "après": operations.addition,"avant": operations.soustraction,
                        "réuni": operations.addition}

class KeywordSolver :

    def __init__(self,directionnality=True,limitUncuedNumbers=True,extendedKeyWord=True):
        self.dicPbmsToconstraints={}
        self.rules={"directionnality":directionnality,"limitUncuedNumbers":limitUncuedNumbers}
        self.dicSignKeyword=copy.deepcopy(dicSignKeyword) # make a copy to avoid changes to dicSignKeyword
        if(extendedKeyWord):
            self.dicSignKeyword.update(dicSignKeywordExtended)

    def __str__(self):
        output=""
        for pbm in self.dicPbmsToconstraints.keys():
            dic=str(self.dicPbmsToconstraints[pbm])
            output=output+"%s => %s\n"%(pbm,dic)
        return output

    def extractPredictions(self,d2): #TODO: Comment or refractor quick
        mainDic=d2.problemDic
        output={}
        for problem in self.dicPbmsToconstraints.keys():
            output[problem]=[]
            #print(problem,self.dicPbmsToconstraints[problem])
            aprioDic=mainDic[problem]
            for formula in aprioDic.formulaTosetDic.keys():
                stopCheking_CurrentFormula=False
                untilNow_FormulaFilteredIn=True
                for number in self.dicPbmsToconstraints[problem]["OnceOrNone"]:
                    if self.rules["limitUncuedNumbers"] and (len(re.findall(number,formula))>1):
                        stopCheking_CurrentFormula=True
                        untilNow_FormulaFilteredIn=False
                        break
                for inter in self.dicPbmsToconstraints[problem]["inter"]:
                    if(stopCheking_CurrentFormula):
                        break
                    if inter not in formula:
                        continue
                    untilNow_FormulaFilteredIn=False
                    for autor in self.dicPbmsToconstraints[problem]["autor"]:
                        if(autor in formula):
                            stopCheking_CurrentFormula=True
                            untilNow_FormulaFilteredIn=True
                            break
                if(untilNow_FormulaFilteredIn):
                    #print("come one "+formula)
                    output[problem].append(formula)
        print(output)
        return output

    def generateKeyWordBehaviour(self,problem): # TODO: Simulation stuff must be in a class
        psentenceWithNumber = re.compile('(' # TODO: Ugly must be done only once
                   +'[^.!?]*?' # not end of sentence
                   +'\s' # blank space
                   +'(\d+)' # number
                   +'\s' # blank space
                   +'[^.!?]*?' # not end of sentence
                   +'[.!?]' # end of sentence
                   +')')
        dicConstraintsOnBehavior=self.findInterdictions(problem.text.fullText,problem.problemInitialStaticValues, psentenceWithNumber)
        self.dicPbmsToconstraints[problem.name]=dicConstraintsOnBehavior


    def findKeywords(self, dicValues,psentenceWithNumber, fullText):
        matchs=psentenceWithNumber.findall(fullText)
    # turn tuples into list and convert the second member in object
        listOfItems=[]
        newMatchs=[]
        for match in matchs:
            for item in dicValues.keys():
                number = str(dicValues[item])
                if (str(number) == match[1]):
                    listOfItems.append(item)
                    newMatchs.append([match[0], item])

        return newMatchs, listOfItems


    def findAssociatedCues(self, newMatchs):
        # find and store the operation cue in sentences
        unCuedNumbers = []
        numberWithKeywordDic = {}
        for match in newMatchs:
            amatch = False
            for k in self.dicSignKeyword.keys():
                keyword = k.lower()
                sentence = match[0].lower()
                if keyword in sentence: # if keyword in sentence
                    numberWithKeywordDic.setdefault(match[1], []).append(self.dicSignKeyword[k])
                    amatch = True

            if not amatch:
                unCuedNumbers.append(match[1])

    #print(unCuedNumbers)
        return numberWithKeywordDic, unCuedNumbers


    def couplesBlindGenerator(self, listOfItems):
        # two uncued numbers can't be add
        allCouples = []
        unCuedNumberCouples = itertools.product(itertools.permutations(listOfItems, 2), "-+")
        for unc in unCuedNumberCouples:
            allCouples.append("%s%s%s" % (unc[0][0], unc[1], unc[0][1])) # T1+P1

        return allCouples


    def produceConstraintsPieces(self, listOfItems, numberWithKeywordDic):
        interdictions = []
        forcedautorisations = []
        for numberWithKeyword in numberWithKeywordDic.keys():
            if (self.rules["directionnality"]):
                # directionnality means that substraction or addition is applied to another number
                # John lost 4 marbles => X-4, not 4-X
                interdictions.append(numberWithKeyword + "-(")
            if (operations.addition not in numberWithKeywordDic[numberWithKeyword]):
                interdictions.append(numberWithKeyword + "+(")
                interdictions.append(")+" + numberWithKeyword)
            if (operations.soustraction not in numberWithKeywordDic[numberWithKeyword]):
                interdictions.append(")-" + numberWithKeyword)
            if (operations.addition in numberWithKeywordDic[numberWithKeyword]):
                for item in listOfItems:
                    if (item != numberWithKeyword):
                        forcedautorisations.append(numberWithKeyword + "+" + item)
                        forcedautorisations.append(item + "+" + numberWithKeyword)

            if (operations.soustraction in numberWithKeywordDic[numberWithKeyword]):
                for item in listOfItems:
                    if (item != numberWithKeyword):
                        forcedautorisations.append(item + "-" + numberWithKeyword)

        return interdictions, forcedautorisations

    def findInterdictions(self, fullText,dicValues,psentenceWithNumber):

        newMatchs, listOfItems = self.findKeywords(dicValues, psentenceWithNumber,fullText)
        numberWithKeywordDic, unCuedNumbers = self.findAssociatedCues(newMatchs)
        interdictions, forcedautorisations = self.produceConstraintsPieces(listOfItems, numberWithKeywordDic)
        allCouples = self.couplesBlindGenerator(listOfItems)
        interdictions.extend([c for c in allCouples if not c in forcedautorisations])
        dicConstraintsOnBehavior={}
        dicConstraintsOnBehavior["inter"]=list(set(interdictions))
        dicConstraintsOnBehavior["autor"]=[]# deprecated
        dicConstraintsOnBehavior["OnceOrNone"]=unCuedNumbers # uncued numbers can be used in formulas, but not more than once

        return dicConstraintsOnBehavior



