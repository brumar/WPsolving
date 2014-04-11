# -*- coding: cp1252 -*-
import lib.operations as operations
from lib.schemas import *
from lib.textRepresentations import *
import copy

class Problem: #fields : structure, text
   def __init__(self,structure,text):
       self.structure=structure
       self.text=text

class Solver:
   def __init__(self,problem):
      self.problem=problem
      self.treeVIZ=""

   def recurcive_solve(self,movelist=[],newmove="",step=0,history=[],schemeToApply=0):
      if(step!=0):
         movelist.append(newmove)
      ml=len(movelist)
      updater=Updater(self.problem)
      updater.applyMoveList(movelist)
      if (not updater.problemState.isProblemEnded()):
         for s,schem in enumerate(updater.appliableSchemaList):
            newmove=Move(schem) 
            print(step,s,ml,schem.positions.keys())
            self.updateTree(step,schem.positions.keys())
            self.recurcive_solve(copy.deepcopy(movelist),newmove,step+1,copy.deepcopy(history))
      else:
         #print(history)
         step=0##problem here
   def updateTree(self,step,keys):
      line=step*"\t"+str(keys)+"\r\n"
      self.treeVIZ+=line
         

class Move:
   def __init__(self,move):
      classname=move.__class__.__name__
      if(classname=="Schema"):
         self.type="schema"
         self.move=move
      elif (classname=="Representation"):
         self.type="representation"
         self.move=move
      
   
   
class Updater: #fields : problem, problemState
   
   def __init__(self,problem):
      self.problem=problem
      self.appliableSchemaList=[]
      
   def startAsUnderstood(self):#initialise all the quantities, goals and representations, as experts do
      goal=self.problem.text.goal
      quantitiesDic = dict.fromkeys(self.problem.structure.objectSet,operations.unknown)#get all the objects, init with unknon
                                                                                          #note : maybe one day => necessary to consider multiple values for a single object
      representations=[]
      for i,info in enumerate(self.problem.text.textInformations):
         quantitiesDic[info.quantity.object]=info.quantity.value# bind object to their values
         representations.append(0)#0 indicate that the first (the good one) interpretation is selected
      self.problemState=ProblemState(quantitiesDic,goal,representations)
      self.updateAppliableSchemas()

   def applyMoveList(self,movelist,startAsUnderstood=True):
      if(startAsUnderstood):
         self.startAsUnderstood()
      for m,move in enumerate(movelist):
         if (move.type=="schema"):
            self.applySchema(move.move)
         if (move.type=="representation"):
            self.applyRepresentationMove(move.move)
             
      
   def applySchema(self,schema):
      if(self.isSchemaAppliable(schema)):
         dic=self.problemState.quantitiesDic
         n,unknow=findTheUnknown(schema,dic)
         if(schema.positions[unknow]=='qf'):
            if(schema.operation==operations.addition):
               self.problemState.quantitiesDic[schema.objects['qf']]=dic[schema.objects['q2']]+dic[schema.objects['q1']]
            else:
               self.problemState.quantitiesDic[schema.objects['qf']]=dic[schema.objects['q2']]-dic[schema.objects['q1']]
         if(schema.positions[unknow]=='q1'):
            if(schema.operation==operations.addition):
               self.problemState.quantitiesDic[schema.objects['q1']]=dic[schema.objects['qf']]-dic[schema.objects['q2']]
            else:
               self.problemState.quantitiesDic[schema.objects['q1']]=dic[schema.objects['qf']]+dic[schema.objects['q2']]
         if(schema.positions[unknow]=='q2'):
            if(schema.operation==operations.addition):
               self.problemState.quantitiesDic[schema.objects['q2']]=dic[schema.objects['qf']]-dic[schema.objects['q1']]
            else:
               self.problemState.quantitiesDic[schema.objects['q2']]=dic[schema.objects['q1']]-dic[schema.objects['qf']]
      self.updateAppliableSchemas()
               
   def applyRepresentationMove(self,representation):
      pass#TODO

   def updateAppliableSchemas(self):
      self.appliableSchemaList=[]
      schemasList=self.problem.structure.schemas
      for i,schema in enumerate(schemasList):
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
      self.representations=representations
   def isProblemEnded(self):
      return(not self.quantitiesDic[self.goal.obj]==operations.unknown)
       
def findTheUnknown (schema,dic):
   numberOfUnknow=0
   theLastUnknown=""
   for o,obj in enumerate(schema.positions.keys()):
      if(dic[obj]==operations.unknown):
         theLastUnknown=obj
         numberOfUnknow+=1
   return numberOfUnknow,theLastUnknown
         
    
schema1=Schema("PoissonEF","PoissonEI",operations.addition,"PoissonGAIN","change")
schema2=Schema("ViandeEF","ViandeEI",operations.addition,"ViandeGAIN","change")
struct=ProblemStructure()
struct.addSchema(schema1)
struct.addSchema(schema2)
struct.addBridgingSchemas(schema1,schema2)
struct.updateObjectList()
text=Text()
text.addTextInformation(TextInformation(Quantity("PoissonGAIN",5),'Au supermarché, le kilo de poisson a augmenté de 5 euros cette année'))
text.addTextInformation(TextInformation(Quantity("PoissonEF",12),'Un kilo de poisson coûte maintenant 12 euros.'))
text.addTextInformation(TextInformation(Quantity("PoissonEIminusViandeEI",0),'Au début de l\'année, le kilo de viande coûtait le même prix que le kilo de poisson.'))
text.addTextInformation(TextInformation(Quantity("PoissonGAINminusViandeGAIN",3),'Le kilo de viande a augmenté de 3 euros de moins que le kilo de poisson'))
text.setGoal(Goal('ViandeEF','Combien coûte le kilo de viande maintenant?'))
text.textInformations[3].addAlternativeRepresentation(Quantity("PoissonGAIN",3),'Le kilo de viande a augmenté de 3 euros')

probleme1=Problem(struct,text)
upD=Updater(probleme1)
upD.startAsUnderstood()
solver=Solver(probleme1)
move=Move(schema1)
solver.recurcive_solve()
print(upD.appliableSchemaList)
#print(solver.treeVIZ)
##upD.applySchema(upD.appliableSchemaList[2])
##upD
##print(upD.appliableSchemaList)
