# -*- coding: cp1252 -*-
import operations

class Quantity:
    def __init__(self,obj,value):
        self.object=obj
        self.value=value

class Representation:
    def __init__(self,quantity,weight,phrase="",comment=""):
        self.quantity=quantity
        self.weight=weight
        self.phrase=phrase
        self.comment=comment       
        
class Problem:
   def __init__(self,structure,text):
       self.structure=structure
       self.text=text

class Text:
    textInformations=[]
    def __init__(self):
        pass
    def addTextInformation(self,textInformation):
        self.textInformations.append(textInformation)
    def setGoal(self,goal):
        self.goal=goal

class TextInformation:
    alternativeRepresentations=[]
    def __init__(self,quantity,phrase="",weight=0):
        self.quantity=quantity
        self.phrase=phrase
        self.weight=weight
    def addAlternativeRepresentation(self,quantity,phrase="",comment="", weight=0):
        self.alternativeRepresentations.append(Representation(quantity,weight,phrase,comment))

class Goal:
    alternativeGoals=[]
    def __init__(self,obj,phrase="",weight=0):
        self.obj=obj
        self.phrase=phrase
        self.weight=weight
    def addAlternativeGoal(self,obj,phrase="",comment="", weight=0):
        self.alternativeGoals.append(obj,phrase,comment,weight)                                              

class ProblemStructure:
    schemas=[]
    def __init__(self):
        pass
    def addSchema(self,schema):
        self.schemas.append(schema)
    def addBridgingSchemas(self,schema1,schema2,names=[]):#Create all the schemas and objects related to eventual relations between two schemas
                                                         #convention : schema1.objects['qf'] > schema2.objects['qf']
        commonObject=self.detectCommonObject(schema1,schema2)
        if(not commonObject):
            for i,position in enumerate(['q1','q2','qf']):
                self.bridge(schema1,schema2,position,operations.soustractionBridge)
        else :
            theCommonObject=commonObject.pop()# to get the only value of the set
            if(schema1.positions[theCommonObject]==schema2.positions[theCommonObject]):#to bridge two schemas, the commonObject must be at the same position
                posOfTheCommonObject=schema1.positions[theCommonObject]
                l=['q1','q2','qf']
                for i,position in enumerate(l):
                    if position!=posOfTheCommonObject:
                        self.bridge(schema1,schema2,position,operations.soustractionBridge)                 
            else:
                return
    def bridge(self,schema1,schema2,position,operationBridge):
        bridgef=schema1.objects[position]+operationBridge+schema2.objects[position] # create string like T2minusT1
        self.addSchema(Schema(bridgef,schema1.objects[position],operations.soustraction,schema2.objects[position])) # create T1-T2=T1minusT2 schema and to the structure

    def detectCommonObject(self,schema1,schema2):#todo
        return schema1.getSetObjects().intersection(schema2.getSetObjects())
    def updateObjectList(self):
        objectList=[]
        for s,schema in enumerate(self.schemas):
            for o,obj in enumerate(schema.getSetObjects()):
                objectList.append(obj)
        self.objectSet=set(objectList)
        

class Schema: #a simple schema is a schema binding 3 values (e.g. a+b=c)
    def  __init__(self,qf,q1,operation,q2,name=""):#convention : q1 must be bigger than q2
        self.name=name
        self.operation=operation
        self.objects = {'qf': qf, 'q1': q1,  'q2': q2}
        self.positions = {qf: 'qf', q1: 'q1',  q2: 'q2'}#usefull to get the position (e.g T1 is the qf of this schema)
    def getSetObjects(self):
        return set([self.objects['q1'],self.objects['q2'],self.objects['qf']])
#    def solve()
    
schema1=Schema("PoissonEF","PoissonEI",operations.addition,"PoissonGAIN","change")
schema2=Schema("ViandeEF","ViandeEI",operations.addition,"ViandeGAIN","change")
struct=ProblemStructure()
struct.addSchema(schema1)
struct.addSchema(schema2)
struct.addBridgingSchemas(schema1,schema2)
struct.updateObjectList()
print(struc.objectSet)
##Au supermarché, le kilo de poisson a augmenté de 5 euros cette année.
##Un kilo de poisson coûte maintenant 12 euros.
##Au début de l'année, le kilo de viande coûtait le même prix que le kilo de poisson.
##Le kilo de viande a augmenté de 3 euros de moins que le kilo de poisson.
##Combien coûte le kilo de viande maintenant  ?
text=Text()
text.addTextInformation(TextInformation(Quantity("PoissonGAIN",5),'Au supermarché, le kilo de poisson a augmenté de 5 euros cette année'))
text.addTextInformation(TextInformation(Quantity("PoissonEF",12),'Un kilo de poisson coûte maintenant 12 euros.'))
text.addTextInformation(TextInformation(Quantity("PoissonEIminusViandeEI",0),'Au début de l\'année, le kilo de viande coûtait le même prix que le kilo de poisson.'))
text.addTextInformation(TextInformation(Quantity("PoissonGAINminusViandeGAIN",3),'Le kilo de viande a augmenté de 3 euros de moins que le kilo de poisson'))
text.setGoal(Goal('ViandeEF','Combien coûte le kilo de viande maintenant?'))
probleme1=Problem(struct,text)
