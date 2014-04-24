import operations

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

    def addValue(self,key,value,erase=False,priority=False):
        if erase:
            self.erase(key)
        insertPosition=0
        if not priority:
            insertPosition=len(self.dic[key])
        self.dic[key].insert(insertPosition,value)

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
        if (move.type=="representationMove"):
            return self.applyRepresentationMove(move.move)

    def applySchema(self,schema):
        if(self.isSchemaAppliable(schema)):
            qdic=self.problemState.quantitiesDic
            n,unknow=findTheUnknown(schema,qdic)
            positionTofind=schema.positions[unknow]
            positionList=['qf','q1','q2']
            positionList.remove(positionTofind)
            operation=schema.operation
            if(positionTofind!='qf'):
                operation=-1*schema.operation # if the quantity to find is qf then no need to revert the operation of the schema to find the unknown
            valueList=[]
            for position in positionList:
                valueList.append(qdic.find(schema.objects[position]))
            valueToFind=max(valueList)+min(valueList)*(operation)
            qdic.addValue(unknow,valueToFind)
        self.updateAppliableSchemas()

        stringOperation='-'
        if(operation==1):
            stringOperation='+'
        infos=str(max(valueList))+stringOperation+str(min(valueList))+'='+str(valueToFind)+' ('+unknow+')'
        return infos

    def applyRepresentationMove(self,representationMove):
        indexInfo=representationMove.indexTextInformation
        indexSelection=representationMove.indexSelectedRepresentation
        self.representations.remove(indexInfo)
        self.representations.insert(indexInfo, indexSelection)
        rep=self.problem.text.textInformations[indexInfo].representations[indexSelection]
        quanti=rep.quantity
        self.problemState.quantitiesDic.addValue(quanti.object, quanti.value)
        infos=quanti.object+" is now equal to "+quanti.value
        return infos

    def updatePossibleRepresentationChange(self):
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

    def isSchemaAppliable(self,schema):
        dic=self.problemState.quantitiesDic
        n,unknow=findTheUnknown(schema,dic)
        if(n==1):
            return True
        else:
            return False

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
