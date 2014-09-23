import operations

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

    def startAsUnderstood(self):    #initialise all the quantities, goals and representations, as experts do
        goal=self.problem.text.goal.expertGoal
        quantitiesDic = QuantityDic(dict.fromkeys(self.problem.structure.objectSet,operations.unknown),startAsVoid=True)    #get all the objects, init with unknow                                                                                                                  #note : maybe one day => necessary to consider multiple values for a single object
        representations=[]
        for info in self.problem.text.textInformations:
            quantitiesDic.addValue(info.getExpertRepresentation().quantity.object, info.getExpertRepresentation().quantity.value) # update the dic bind object to their values according the representations
            representations.append(0)    #0 indicate that the first (the good one) interpretation is selected

        self.problemState=ProblemState(quantitiesDic,goal,representations) # the most important line
        self.updatePossibleRepresentationChange()
        self.updateAppliableSchemas()

    def applyMove(self,move,constraints=[]):
        if (move.type=="schema"):
            return self.applySchema(move.move,constraints)
        if (move.type=="RepresentationMove"):
            return self.applyRepresentationMove(move.move,constraints)

    def applySchema(self,schema,constraints=[],trial=False): # when trial is True, the unknown is computed without any change in the problemState
        infos=InfoStep()
        if(self.isSchemaAppliable(schema)):
            qdic=self.problemState.quantitiesDic
            n,unknow=findTheUnknown(schema,qdic)
            positionTofind=schema.positions[unknow]
            positionList=['qf','q1','q2']
            positionList.remove(positionTofind)
            operation=schema.operation
            if(positionTofind!='qf'):
                operation=-1*schema.operation # if the quantity to find is qf then no need to revert the operation of the schema to find the unknown
            if(positionTofind=='q2'):   #if q2 is the quantity to find then the operation needed is always a substraction
                operation=operations.soustraction

            objectA=schema.objects[positionList[0]]
            valueA=qdic.find(objectA)
            objectB=schema.objects[positionList[1]]
            valueB=qdic.find(objectB)

            if (valueB>valueA):
                valueA, valueB = valueB, valueA #invert the values
                objectA, objectB = objectB, objectA #invert the object

            valueToFind=valueA+valueB*(operation)

            stringOperation='-'
            if(operation==1):
                stringOperation='+'
            infos.formulaFirstPart=" "+str(valueA)+" "+stringOperation+" "+str(valueB)+" "
            infos.shortInfo=infos.formulaFirstPart+'='+" "+str(valueToFind)+" "+' ('+unknow+')' #12-3=9 (ViandeEF)
            infos.objectsFormulaFirstPart=" "+objectA+" "+stringOperation+" "+objectB+" "
            infos.objectsFormula=infos.objectsFormulaFirstPart+'='+" "+unknow+" " #PoissonEF-PoissonEFminusViandeEF=ViandeEF
            infos.unknow=unknow
            infos.valueToFind=valueToFind
            infos.type="schema"
            infos.operands=[objectA,objectB]

            if not trial: # when trial is True, the unknown is computed without any change in the problemState
                qdic.addValue(unknow,valueToFind)
                self.updateAppliableSchemas()
        return infos

    def applyRepresentationMove(self,representationMove,constraints=[],):
        indexInfo=representationMove.indexTextInformation
        indexSelection=representationMove.indexSelectedRepresentation
        oldSelection=self.problemState.representations.pop(indexInfo)
        breakPreviousInterpretations=self.doIBreakTheOldOne(constraints)
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

    def doIBreakTheOldOne(self, constraints):
        for constraint in constraints:
            classname=constraint.__class__.__name__
            if(classname=="BehavioralConstraint"):
                return constraint.breakPreviousRepresentation
        return BREAKPREVIOUSREPRESENTATION #default value


    def updatePossibleRepresentationChange(self,constraints=[]):
        self.possibleRepresentationChangeList=[]
        currentReps=self.problemState.representations
        for t,textInfo in enumerate(self.problem.text.textInformations):
            for r,representation in enumerate(textInfo.representations):
                if(currentReps[t]!=r):
                    self.possibleRepresentationChangeList.append(RepresentationMove(t,r))


    def updateAppliableSchemas(self,constraints=[]):
        self.appliableSchemaList=[]
        schemasList=self.problem.structure.schemas
        for schema in schemasList:
            if(self.isSchemaAppliable(schema,constraints)):
                self.appliableSchemaList.append(schema)

    def isSchemaAppliable(self,schema,constraints=[]):
        dic=self.problemState.quantitiesDic
        n,unknow=findTheUnknown(schema,dic)
        if(n!=1):
            return False
        else:
            return self.isConstraintsRespectedBySchema(schema,constraints)

    def isConstraintsRespectedBySchema(self,schema,constraints=[]):
        isAllConstraintsRespectedBySchema=True
        for constraint in constraints:
            if not (self.isConstraintRespectedBySchema(schema,constraint)):
                isAllConstraintsRespectedBySchema=False
        return isAllConstraintsRespectedBySchema

    def isConstraintRespectedBySchema(self,schema,constraint):
        classname=constraint.__class__.__name__
        if(classname=="IntervalConstraint"):
            return self.checkIntervall(schema,constraint)
        else:
            return True

    def checkIntervall(self,schema,constraint): #listOfObjects, condition
        infos=self.applySchema(schema,trial=True)
        objectComputed=infos.unknow
        valueComputed=infos.valueToFind
        for objectToCheck in constraint.listOfObjects:
            if (valueComputed<0):
                if(objectToCheck in objectComputed) and (constraint.condition==operations.allowsNegativeValues) : # e.g if 'EI' is in poissonEI and poissonEI<0
                    return True
                else:
                    return False
        return True



    #def applySchema(self,schema):

class ProblemState:
    def __init__(self,quantitiesDic,goal,representations):
        self.quantitiesDic=quantitiesDic
        self.goal=goal
        self.representations=representations #une liste d'index !

    def isProblemEnded(self):
        return(not self.quantitiesDic.isUnknown(self.goal.obj))

def findTheUnknown (schema,quantitiesDic): #count the number of unknowns in the schema, and give the object of the last unknown found
    numberOfUnknow=0
    theLastUnknown=""
    for obj in schema.positions.keys():
        if(quantitiesDic.isUnknown(obj)):
            theLastUnknown=obj
            numberOfUnknow+=1
    return numberOfUnknow,theLastUnknown
