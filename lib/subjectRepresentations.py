import operations
import logging

BREAKPREVIOUSREPRESENTATION=False
ERASE=True

class InfoStep:
    def __init__(self,shortInfo=""):
        self.shortInfo=shortInfo
        self.objectsFormula=""
        self.objectsFormulaFirstPart=""
        self.formulaFirstPart=""
        self.unknow=""
        self.valueToFind=""
        self.type=""
        self.operands="no"
        self.move=""
        self.solved=False

    def log(self,prefix=""):
        if(prefix!=""):
            logging.info("step prefixed "+prefix)
        logging.info(self.shortInfo);
        logging.info(self.objectsFormula);
        logging.info(self.objectsFormulaFirstPart);
        logging.info(self.formulaFirstPart);
        logging.info(self.unknow);
        logging.info(self.valueToFind);
        logging.info(self.type);
        logging.info(self.operands);
        logging.info(self.move);
        logging.info(self.solved);

    def buildSchemaInfos(self,operation, objectA, valueA, objectB, valueB, unknow):
        valueToFind=valueA+valueB*(operation)
        stringOperation='-'
        if(operation==1):
            stringOperation='+'
        self.formulaFirstPart=" "+str(valueA)+" "+stringOperation+" "+str(valueB)+" " #12-3=9 (ViandeEF)
        self.shortInfo=self.formulaFirstPart+'='+" "+str(valueToFind)+" "+' ('+unknow+')'#PoissonEF-PoissonEFminusViandeEF=ViandeEF
        self.objectsFormulaFirstPart=" "+objectA+" "+stringOperation+" "+objectB+" "
        self.objectsFormula=self.objectsFormulaFirstPart+'='+" "+unknow+" "
        self.unknow=unknow
        self.valueToFind=valueToFind
        self.type="schema"
        self.operands=[objectA,objectB]


class Problem: #fields : structure, text

    def __init__(self,structure,text,name="untitled"):
        self.name=name
        self.structure=structure
        self.text=text
        self.problemInitialStaticValues={} #link T1,P1,etc.. to its values

    def setInitialValues(self,dic,onlyDic=False):
        self.problemInitialStaticValues=dic
        if(not onlyDic):
            for tInfo in self.text.textInformations:
                for rep in tInfo.representations:
                    oldValue=rep.quantity.value
                    rep.quantity.value=dic[oldValue] # TODO: not a good line as it alters the generic aspect of the problem

    def renameObjects(self,renameDic):
        self.text.renameObjects_t(renameDic)
        self.structure.renameObjects_s(renameDic)

    def renameKeywordObjects(self,renameDic):
        self.text.renameKeywordObjects_t(renameDic)
        self.structure.renameKeywordObjects_s(renameDic)

class Move:
    def __init__(self,move):
        classname=move.__class__.__name__
        if(classname=="Schema"):
            self.type="schema"
            self.move=move
        elif (classname=="RepresentationMove"):
            self.type="RepresentationMove"
            self.move=move

class RepresentationMove:
    def __init__(self,indexTextInformation, indexSelectedRepresentation):
        self.indexTextInformation=indexTextInformation
        self.indexSelectedRepresentation=indexSelectedRepresentation

class QuantityDic:

    def __init__(self, realDic,startAsVoid=False):
        self.dic={}
        for key in realDic.keys():
            self.dic[key]=[]
            self.dic[key].append(realDic[key])
            if startAsVoid:
                self.erase(key);


    def isMultiple(self, key):
        return (len(self.dic[key])>0)

    def find(self,key,multiple=False):
        if multiple:
            return self.dic[key]
        else:
            e=self.dic[key].pop(0)
            self.dic[key].insert(0,e)
            return e # if an element has a priority, it's at the first position

    def addValue(self,key,value,erase=ERASE,priority=True):
        if erase:
            self.erase(key)
        insertPosition=0
        if not priority:
            insertPosition=len(self.dic[key])
        self.dic[key].insert(insertPosition,value)

    def removeValue(self,key,value):
        if(value in self.dic[key]):
            self.dic[key].remove(value)

    def isUnknown(self, key):
        return not self.dic[key] #simplest way to check if the list is empty

    def erase (self,key):
        self.dic[key]=[]

class Updater: #fields : problem, problemState, representations, quantitiesDic

    def __init__(self,problem):
        self.problem=problem
        self.appliableSchemaList=[]
        self.possibleRepresentationChangeList=[]
        self.constraintController=None #constraint controller will check the consistency with constraints

    def startAsUnderstood(self):
        '''
        initialise all the quantities, goals and representations as experts ones
        '''
        goal=self.problem.text.goal.expertGoal
        quantitiesDic = QuantityDic(dict.fromkeys(self.problem.structure.objectSet,operations.unknown),startAsVoid=True)    #get all the objects, init with unknow                                                                                                                  #note : maybe one day => necessary to consider multiple values for a single object
        representations=[]
        for info in self.problem.text.textInformations:
            quantitiesDic.addValue(info.getExpertRepresentation().quantity.object, info.getExpertRepresentation().quantity.value) # update the dic bind object to their values according the representations
            representations.append(0)    #0 indicate that the first (the good one) interpretation is selected

        self.problemState=ProblemState(quantitiesDic,goal,representations) # the most important line
        self.updatePossibleRepresentationChange()
        self.updateAppliableSchemas()

    def applyMove(self,move):
        if (move.type=="schema"):
            return self.tryApplySchema(move.move)
        if (move.type=="RepresentationMove"):
            return self.applyRepresentationMove(move.move)

    def tryApplySchema(self,schema,trial=False):
        """
        the function that try to compute an unknown quantity
        when trial is True, the unknown is computed without any change in the problemState
        it is usefull to check the compatibility with the constraints
        """

        qdic=self.problemState.quantitiesDic
        n,unknow=findTheUnknown(schema,qdic)
        positionTofind=schema.positions[unknow]
        positionList=['qf','q1','q2']
        positionList.remove(positionTofind)
        operation=schema.operation
        objectA=schema.objects[positionList[0]]
        valueA=qdic.find(objectA)
        objectB=schema.objects[positionList[1]]
        valueB=qdic.find(objectB)
        # we need to find the operation needed to get the unknown quantity
        if(positionTofind!='qf'):
            operation=-1*schema.operation # if the quantity to find is qf then no need to revert the operation of the schema to find the unknown
        if(positionTofind=='q2'):   #if q2 is the quantity to find then the operation needed is always a substraction
            operation=operations.soustraction
            if(schema.operation==operations.soustraction):
                valueA, valueB = valueB, valueA #invert the values
                objectA, objectB = objectB, objectA #invert the object
        infos=InfoStep()

        infos.buildSchemaInfos(operation, objectA, valueA, objectB, valueB, unknow)

        if self.constraintController.checkStep(infos): # the step is compatible with constraints
            if not trial : # when trial is True, the unknown is computed without any change in the problemState
                infos=self.constraintController.alterStep(infos) # some constraints can alter the step, for example reverse the operands when negative numbers found
                qdic.addValue(unknow,infos.valueToFind)
                self.updateAppliableSchemas()
                return infos
            else : # if we enter this function with the trial mode, then we just want to know if it's compatible with the constraints or not
                return True
        else:
            return False

    def applyRepresentationMove(self,representationMove):
        indexInfo=representationMove.indexTextInformation
        indexSelection=representationMove.indexSelectedRepresentation
        oldSelection=self.problemState.representations.pop(indexInfo)
        breakPreviousInterpretations=self.constraintController.breakPreviousInterpretation
        if(breakPreviousInterpretations):
            oldRep=self.problem.text.textInformations[indexInfo].representations[oldSelection] # TODO
            oldQuanti=oldRep.quantity
            self.problemState.quantitiesDic.removeValue(oldQuanti.object, oldQuanti.value)
        self.problemState.representations.insert(indexInfo, indexSelection)#pop and insert in order to avoid loosing the value
        rep=self.problem.text.textInformations[indexInfo].representations[indexSelection]
        quanti=rep.quantity
        self.problemState.quantitiesDic.addValue(quanti.object, quanti.value)
        infos=InfoStep()
        infos.move=representationMove
        infos.type="RepresentationMove"
        infos.newlyAssignedObject=quanti.object
        infos.valueToFind=quanti.value
        infos.shortInfo=str(quanti.value)+" interpreted as "+quanti.object
        return infos

    def isSchemaAppliable(self,schema):
        dic=self.problemState.quantitiesDic
        n,unknow=findTheUnknown(schema,dic)
        if(n==1)and(self.tryApplySchema(schema,trial=True)):
            return True
        return False

    def updatePossibleRepresentationChange(self):
        self.possibleRepresentationChangeList=[]
        currentReps=self.problemState.representations
        for t,textInfo in enumerate(self.problem.text.textInformations):
            for r,representation in enumerate(textInfo.representations):
                if(currentReps[t]!=r):
                    self.possibleRepresentationChangeList.append(RepresentationMove(t,r))


    def updateAppliableSchemas(self):
        self.appliableSchemaList=[]
        schemasList=self.problem.structure.schemas
        for schema in schemasList:
            if(self.isSchemaAppliable(schema)):
                self.appliableSchemaList.append(schema)

    def attachConstraintController(self,constraintController):
        self.constraintController=constraintController


class ProblemState:
    def __init__(self,quantitiesDic,goal,representations):
        self.quantitiesDic=quantitiesDic
        self.goal=goal
        self.representations=representations #une liste d'index !

    def isProblemEnded(self):
        return(not self.quantitiesDic.isUnknown(self.goal.obj))

def findTheUnknown (schema,quantitiesDic):
    '''
    count the number of unknowns in the schema,
    and give the object of the last unknown found
    '''
    numberOfUnknow=0
    theLastUnknown=""
    for obj in schema.positions.keys():
        if(quantitiesDic.isUnknown(obj)):
            theLastUnknown=obj
            numberOfUnknow+=1
    return numberOfUnknow,theLastUnknown
