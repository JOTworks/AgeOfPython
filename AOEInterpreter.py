from data import *

class Interpreter:
    def __init__(self, main):
        self.main = main
    
    def putCommandsInRules(self, inList):
        for idx, item in enumerate(inList):
            if isinstance(item, CommandObject):
                inList[idx] = defruleObject([CommandObject("true",[])], [item])

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
            newItem = self.reduceNestedObjects(self.main, 0)  
            newMain.append(newItem)
        self.main = newMain
        #print(self.main)