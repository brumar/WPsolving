import operations


class IntervalConstraint:
    def __init__(self,listOfObjects,condition):
        self.listOfObjects=listOfObjects
        self.condition=condition

class BehavioralConstraint:
    def __init__(self,breakPreviousInterpretations):
        self.breakPreviousRepresentation=breakPreviousInterpretations

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

    def renameObjects_t(self,remaningDic):
        for infos in self.textInformations:
            for representation in infos.representations:
                oldobj=representation.quantity.object
                newoobj=remaningDic[oldobj]
                representation.quantity.object=newoobj
        oldgoal=self.goal.expertGoal.obj
        self.goal.expertGoal.obj=remaningDic[oldgoal]

    def renameKeywordObjects_t(self,remaningDic):
        for infos in self.textInformations:
            for representation in infos.representations:
                oldobj=representation.quantity.object
                currentObj=oldobj
                for keyword,newKeyword in remaningDic.iteritems():
                    if (keyword in oldobj):
                        currentObj=currentObj.replace(keyword,newKeyword)
                representation.quantity.object=currentObj
        currentG=self.goal.expertGoal.obj
        for keyword,newKeyword in remaningDic.iteritems():
            if (keyword in currentG):
                currentG=currentG.replace(keyword,newKeyword)
        self.goal.expertGoal.obj=currentG

    def setGoal(self,goal):
        self.goal=goal

class TextInformation:
    def __init__(self,representation):
        self.representations=[]
        self.representations.append(representation) #by convention the expert representation is also the first element in representations

    def addAlternativeRepresentation(self,representation):
        self.representations.append(representation)

    def getExpertRepresentation(self):
        return self.representations[0]

    def getRepresentations(self):
        return self.representations

    def removeAlternativeRepresentations(self):
        self.representations=[self.getExpertRepresentation()]


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