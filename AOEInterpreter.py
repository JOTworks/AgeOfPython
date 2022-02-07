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
#words
"""
from data import *

class Interpreter:
    def __init__(self, main):
        self.main = main
    
    def putCommandsInRules(self, inList):
        for idx, item in enumerate(inList):
            if isinstance(item, CommandObject):
                inList[idx] = defruleObject(LineListObject( [CommandObject("true",[])] ), LineListObject( [item] ))

    def reduceNestedObjects(self, inList, depth):
        itemReducedList = []
        for item in inList:
            if isinstance(item, IfObject):
                nested = False
                for subItem in item.lineList.lineList:
                    if isinstance(subItem, (ContainesLineList, FuncCallObject)):
                        nested = True
                if nested:
                    itemReducedList = self.reduceNestedObjects(item.lineList.lineList, depth+1)
                    #ad the goofy NOT conditional, then the jump statement
                else:
                    itemReducedList = self.putIfsInRules(item)
            else: #just copy without changing
                itemReducedList.append(item)
        #print(itemReducedList)
        return itemReducedList

    def putIfsInRules(self, inIf):
        for item in inIf.lineList.lineList:
            if not isinstance(item,CommandObject): #this is where i would turn anything other then command into command
                raise Exception("Object in If.LineList was not CommandObject! only Commands and ifs in ifs are supported!")
        return defruleObject(inIf.conditionList, inIf.lineList)
    
    def interpret(self):
        self.putCommandsInRules(self.main)
        newMain = []
        for item in self.main:
            if isinstance(item, defruleObject):
                newMain.append(item)
            else:
                newItem = self.reduceNestedObjects(self.main, 0)  
                newMain.append(newItem)
        self.main = newMain
        #print(self.main)
"""