from data import *

class Interpreter:
    def __init__(self, main):
        self.main = main
        self.newMain = []
    def putCommandsInRules(self, inList):
        for idx, item in enumerate(inList):
            if isinstance(item, CommandObject):
                inList[idx] = defruleObject(LineListObject( [CommandObject("true",[])] ), LineListObject( [item] ))    

    def collapseIftoDefrule(self, inIf):
        if not isinstance(inIf, IfObject):
            raise Exception("Did not pass IF to collapseIftoDefrule")
        tempMain = []
        deepistIf = True
        for item in inIf.lineList.lineList:
            if isinstance( item, (IfObject,defruleObject) ):
                deepistIf = False
        if deepistIf:
            tempMain.append(defruleObject(inIf.conditionList, inIf.lineList))
        else:
            raise Exception("nested if not yet implamented!")
            #collapse others to defrule
            #ad the funky negetion version
            #tempMain += collapseIftoDefrule(something)
        return tempMain

    def interpret(self):
        self.putCommandsInRules(self.main)
        
        for item in self.main:
            print(str(item.__class__))
            if isinstance(item, IfObject):
                print("true")
                self.newMain += self.collapseIftoDefrule(item)
            else:
                self.newMain.append(item)
        self.main = self.newMain
        for item in self.main:
            print(str(item.__class__))
