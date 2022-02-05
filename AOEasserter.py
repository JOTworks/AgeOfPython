from data import *


class Asserter:
    def __init__(self, main):
        self.main = main


    def checkUnsuported(self, inList):
        for item in inList:
            if isinstance(item, ContainesLineList):
                self.checkUnsuported(item.lineList.lineList)
            
            if isinstance(item,VarAsignObject): raise Exception("variable asignment is currently UNSUPORTED!")
            if isinstance(item,FuncCallObject): raise Exception("Functions are currently UNSUPORTED!")
            if isinstance(item,DefFuncObject): raise Exception("Functions are currently UNSUPORTED!")
            if isinstance(item,ForLoopObject): raise Exception("For Loops are currently UNSUPORTED!")
            if isinstance(item,WhileLoopObject): raise Exception("While Loops currently UNSUPORTED!")
            
            print(str(item.__class__))


    def check(self):
      self.checkUnsuported(self.main)


#check all of the const being assigned