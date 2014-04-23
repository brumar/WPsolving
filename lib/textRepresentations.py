import operations

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

    def get(self,key,multiple=False):
        if multiple:
            return self.dic[key]
        else:
            return self.dic[key].pop(0) # if an element has a priority, it's at the first position

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

class Text:
    def __init__(self):
        self.textInformations=[]
    def getTextInformation(self,index):
        return(self.textInformations[index])
    def addTextInformation(self,textInformation):
        self.textInformations.append(textInformation)
    def setGoal(self,goal):
        self.goal=goal

class TextInformation:
    def __init__(self,representation):
        self.representations=[]
        self.expertRepresentation=representation
        self.representations.append(representation) #by convention the expert representation is also the first element in representations

    def addAlternativeRepresentation(self,representation):
        self.representations.append(representation)

    def getExpertRepresentation(self):
        return self.expertRepresentation

    def getRepresentations(self):
        return self.representations

class Goal:
    def __init__(self,obj,phrase="",weight=0):
        self.obj=obj
        self.phrase=phrase
        self.weight=weight

class TextGoal:
    def __init__(self,goal):
        self.alternativeGoals=[]
        self.expertGoal=goal

    def addAlternativeGoal(self,goal):
        self.alternativeGoals.append(goal)

    def getExpertGoal(self):
        return self.expertGoal

    def getAlternativeGoals(self):
        return self.alternativeGoals

#===============================================================================
# dict = {'Alice': "balbalbal" , 'Beth': '9102', 'Cecil': '3258'}
# qd=QuantityDic(dict)
# print(qd.isUnknown('Beth'))
# print(qd.isUnknown('Alice'))
# qd.add_value('Cecil', 'dadada',priority=True)
# print(qd.isMultiple('Cecil'))
# print(qd.get('Cecil', False))
#===============================================================================