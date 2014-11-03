'''
Created on 3 nov. 2014

@author: Nevrose
'''
class ConstraintsController:
    def __init__(self,stepConstraints=[],strictAvoidance=True,breakPreviousInterpretation=False):
        self.strictAvoidance=strictAvoidance
        self.logMessages=[]
        self.stepConstraints=stepConstraints
        self.breakPreviousInterpretation=breakPreviousInterpretation

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


