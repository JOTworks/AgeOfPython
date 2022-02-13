from data import *


class Asserter: #assert that functions objects only have returns as a last line. #assert that variable asingms with function canot have another token in expression
    def __init__(self, main):
        self.main = main


    def checkUnsuported(self, inList):
        useDefConst = False
        useVarAsign = False
        for item in inList:
            if isinstance(item, ContainesLineList):
                self.checkUnsuported(item.lineList)
            
            #if isinstance(item,VarAsignObject): raise Exception("Variable asignment is currently UNSUPORTED!")
            if isinstance(item,VarAsignObject): 
                useVarAsign = True
                if len(item.expression) > 3:
                    raise Exception("variable asignments can only do one operation at a time. example x = y + 2") 
            if isinstance(item,defconstObject): useDefConst = True
            #if isinstance(item,FuncCallObject): raise Exception("Functions are currently UNSUPORTED!")
            #if isinstance(item,DefFuncObject): raise Exception("Functions are currently UNSUPORTED!")
            if isinstance(item,ForLoopObject): raise Exception("For Loops are currently UNSUPORTED!")
            if isinstance(item,WhileLoopObject): raise Exception("While Loops currently UNSUPORTED!")
        
        if useDefConst and useVarAsign: raise Exception("Defconst and variables canot both be used!")


    def check(self):
      self.checkUnsuported(self.main)


#check all of the const being assigned