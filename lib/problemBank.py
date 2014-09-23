'''
Created on 25 juil. 2014

@author: Nevrose
'''
class problemBank():
    def __init__(self):
        self.dicPbm={}

    def addPbm(self,problem):
        self.dicPbm[problem.name]=problem

    def addPbms(self,problems):
        for problem in problems:
            self.addPbm(problem)