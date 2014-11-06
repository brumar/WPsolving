'''
Created on 3 nov. 2014

@author: Nevrose
'''
class ConstraintsController:
    def __init__(self,stepConstraints=[],alterStepConstraints=[],strictAvoidance=True,breakPreviousInterpretation=False):
        self.strictAvoidance=strictAvoidance
        self.logMessages=[]
        self.stepConstraints=stepConstraints
        self.alterStepConstraints=alterStepConstraints
        self.breakPreviousInterpretation=breakPreviousInterpretation

    def alterStep(self,stepInfos):
        for stepConstraint in self.alterStepConstraints:
            if (stepConstraint.condition(stepInfos)):
                stepInfos=stepConstraint.alterStep(stepInfos)
        return stepInfos

    def checkStep(self,stepInfos):
        for stepConstraint in self.stepConstraints:
            if (stepConstraint.checkStep(stepInfos)==False):
                if(not self.strictAvoidance):
                    self.logMessages.append(stepConstraint.name)
                    return True
                return False
        return True

    def addStepConstraint(self,stepConstraint):
        self.stepConstraints.append(stepConstraint)

    def constraintController(self,stepInfos):
        return stepInfos

class StepConstraint:
    def __init__(self,condition,name="unamed"):
        self.condition=condition #condition is a function which must take a step info as argument and return a boolean
        self.name=name

    def checkStep(self,stepInfos):
        if(stepInfos.__class__.__name__=='InfoStep'):
            validity=self.condition(stepInfos)
            return validity
        else:
            raise ValueError("argument must be an InfoStep instance")

class AlterStepConstraint:
    def __init__(self,condition=lambda info: True , alterAction=lambda info: info):
        self.condition=condition
        self.alterAction=alterAction

    def alterStep(self,stepInfos):
        if(self.condition(stepInfos)):
            return self.alterAction(stepInfos)
