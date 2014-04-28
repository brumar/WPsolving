import operations

BREAKTHEOLDONE=True
ERASE=True

class InfoStep:
    def __init__(self,shortInfo=""):
        self.shortInfo=shortInfo
        self.objectsFormula=""
        self.unknow=""
        self.valueToFind=""
        self.type=""

class Problem: #fields : structure, text
    def __init__(self,structure,text):
        self.structure=structure
        self.text=text


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
        self.representations=[]

    def startAsUnderstood(self):    #initialise all the quantities, goals and representations, as experts do
        goal=self.problem.text.goal.expertGoal
        quantitiesDic = QuantityDic(dict.fromkeys(self.problem.structure.objectSet,operations.unknown),startAsVoid=True)    #get all the objects, init with unknow                                                                                                                  #note : maybe one day => necessary to consider multiple values for a single object
        for info in self.problem.text.textInformations:
            quantitiesDic.addValue(info.expertRepresentation.quantity.object, info.expertRepresentation.quantity.value) # update the dic bind object to their values according the representations
            self.representations.append(0)    #0 indicate that the first (the good one) interpretation is selected

        self.problemState=ProblemState(quantitiesDic,goal,self.representations) # the most important line

        self.updateAppliableSchemas()

    def applyMoveList(self,movelist,startAsUnderstood=True):
        if(startAsUnderstood):
            self.startAsUnderstood()
        for move in movelist:
            self.applyMove(move)

    def applyMove(self,move):
        if (move.type=="schema"):
            return self.applySchema(move.move)
        if (move.type=="RepresentationMove"):
            return self.applyRepresentationMove(move.move)

    def applySchema(self,schema,trial=False): # when trial is True, the unknown is computed without any change in the problemState
        infos=InfoStep() #if non appliable
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

            infos.shortInfo=str(valueA)+stringOperation+str(valueB)+'='+str(valueToFind)+' ('+unknow+')' #12-3=9 (ViandeEF)
            infos.objectsFormula=objectA+stringOperation+objectB+'='+unknow #PoissonEF-PoissonEFminusViandeEF=ViandeEF
            infos.unknow=unknow
            infos.valueToFind=valueToFind
            infos.type="SchemaApplied"

            if not trial: # when trial is True, the unknown is computed without any change in the problemState
                qdic.addValue(unknow,valueToFind)
                self.updateAppliableSchemas()
        return infos

    def applyRepresentationMove(self,representationMove,breakTheOldOne=BREAKTHEOLDONE):
        indexInfo=representationMove.indexTextInformation
        indexSelection=representationMove.indexSelectedRepresentation
        oldSelection=self.representations.pop(indexInfo)
        if(breakTheOldOne):
            oldRep=self.problem.text.textInformations[indexInfo].representations[oldSelection] # TODO
            oldQuanti=oldRep.quantity
            self.problemState.quantitiesDic.removeValue(oldQuanti.object, oldQuanti.value)
        self.representations.insert(indexInfo, indexSelection)#pop and insert in order to avoid loosing the value
        rep=self.problem.text.textInformations[indexInfo].representations[indexSelection]
        quanti=rep.quantity
        self.problemState.quantitiesDic.addValue(quanti.object, quanti.value)
        infos=InfoStep()
        infos.type="RepresentationMove"
        infos.shortInfo=quanti.object+" is now equal to "+str(quanti.value)
        return infos

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

    def checkIntervall(self,schema,constraint): #listOfObjects, condition
        infos=self.applySchema(schema,trial=True)
        objectComputed=infos.unknow
        valueComputed=infos.valueToFind
        for objectToCheck in constraint.listOfObjects:
            if(objectToCheck in objectComputed) and (constraint.condition==operations.superiorOrEqualTo0) and (valueComputed<=0): # e.g if 'EI' is in poissonEI and poissonEI<0
                #TODO: new function(condition,value)
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
