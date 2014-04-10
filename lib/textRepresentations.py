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

class Text:
    def __init__(self):
        self.textInformations=[]
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
        self.alternativeGoals.append(Goal(obj,phrase,comment,weight))    
