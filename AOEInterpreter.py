from pprint import pprint
import copy
from data import *
class Memory:
    def __init__(self):
        self.openMemory = [] #list of open goals, they get deleted when in use and added when freed
        self.usedMemory = [] #list of variable name for used goals, equals "" if open memory
        for itr in range (1,256):
            self.openMemory.append(itr)
            self.usedMemory.append("")
    def printUsedMemory(self):
        memoryString = ""
        for itr in range(len(self.usedMemory)):
            if self.usedMemory[itr] != "":
                memoryString += str(itr) +" "+self.usedMemory[itr]+"\n"
        return memoryString
                
    def checkSpace(self):
        if len(self.openMemory) == 0:
            raise Exception("Malloc ERROR RAN OUT OF GOALS!")
    
    def isUsed(self, varName):
        varName = varName.split(".")
        if varName[0] in self.usedMemory:
            return True
        
    def getMemLoc(self, varName):
        varNameList = varName.split(".")
        if not self.isUsed(varNameList[0]):
            raise Exception("Can't get memLoc that dosnt exist: "+varName+"\n"+self.printUsedMemory())
        memStartLoc = self.usedMemory.index(varNameList[0]) 
        if (len(varNameList)==1):
            return memStartLoc
        elif(len(varNameList)==2) and (self.usedMemory[memStartLoc+1]==Structure.POINT):
            if varNameList[1]=='x' or varNameList[1]=='0':
                return memStartLoc
            if varNameList[1]=='y' or varNameList[1]=='1':
                return memStartLoc+1
            


    def mallocInt(self, varName):
        self.checkSpace()
        self.usedMemory[self.openMemory[0]] = varName
        index = self.openMemory[0]
        del self.openMemory[0]
        return index

    def mallocPoint(self, varName):
        self.checkSpace()
        for itr in range(len(self.openMemory)-1):
            if self.openMemory[itr]+1 == self.openMemory[itr+1]:
                self.usedMemory[self.openMemory[itr]] = varName
                self.usedMemory[self.openMemory[itr+1]] = str("Structure.POINT")
                index = self.openMemory[itr]
                del self.openMemory[itr:itr+2]
                return index
        raise Exception("Malloc ERROR RAN OUT OF SPACE FOR A POINT!")
    #victory data is 3
    def mallocState(self, varName): #state and cost
        self.checkSpace()
        for itr in range(len(self.openMemory)-3):
            if (self.openMemory[itr] == self.openMemory[itr+1] + 1) and (self.openMemory[itr] == self.openMemory[itr+2] + 2) and (self.openMemory[itr] == self.openMemory[itr+3] + 3):
                self.usedMemory[self.openMemory[itr]] = varName
                self.usedMemory[self.openMemory[itr+1]] = Structure.State
                self.usedMemory[self.openMemory[itr+3]] = Structure.State
                self.usedMemory[self.openMemory[itr+4]] = Structure.State
                index = self.openMemory[itr]
                del self.openMemory[itr:itr+3]
                return index
        return False
        raise Exception("Malloc ERROR RAN OUT OF SPACE FOR A STATE!")

    def free(self, varName):
        if not varName in self.usedMemory:
            raise Exception ("tried to free"+varName+"but it was not in Memory!")
        index = self.usedMemory.index(varName)
        if self.usedMemory[index+1] == Structure.POINT:
            self.freeGoal(index)
            self.freeGoal(index+1)
        elif self.usedMemory[index+1] == Structure.STATE:
            self.freeGoal(index)
            self.freeGoal(index+1)
            self.freeGoal(index+2)
            self.freeGoal(index+3)
        else:
            self.freeGoal(index)

    def freeGoal(self, goal):
        self.openMemory.append(goal)
        self.usedMemory[goal] = ""

class Interpreter:
    def __init__(self, main):
        self.main = main
        self.newMain = []
        self.constList = []
        self.funcList = []
        self.callStack = []
        self.memory = Memory()
        self.TRUE_CONDITION = LineListObject( [CommandObject("true",[],"","")] )
        
    def collapseIftoDefrule(self, inIf):
        if not isinstance(inIf, IfObject):
            raise Exception("Did not pass IF to collapseIftoDefrule")
        tempMain = []
        deepistIf = True
        itr = 0
        while (itr < len(inIf.lineList.lineList)):
            print("itr: "+str(itr))
            if isinstance( inIf.lineList.lineList[itr], (IfObject,defruleObject,FuncCallObject) ):
                deepistIf = False
            if isinstance( inIf.lineList.lineList[itr], VarAsignObject):
                commands = self.varAsignToCommands(inIf.lineList.lineList[itr])
                if commands != None:
                    inIf.lineList.lineList = inIf.lineList.lineList[:itr] + self.varAsignToCommands(inIf.lineList.lineList[itr]) + inIf.lineList.lineList[itr:+1]
                else:
                    inIf.lineList.lineList = inIf.lineList.lineList[:itr] + inIf.lineList.lineList[itr+1:]
                    itr -= 1
            itr += 1
        if deepistIf:
            tempMain.append(defruleObject(inIf.conditionList, inIf.lineList))
        else:
            raise Exception("nested if not yet implamented!")
            #collapse others to defrule
            #ad the funky negetion version
            #tempMain += collapseIftoDefrule(something)
        return tempMain

    def moveDefconst(self):
        itr=0
        while (itr<len(self.main)):
            if isinstance(self.main[itr], defconstObject):
                self.constList.append(self.main.pop(itr))
                itr -= 1
            itr += 1

    def moveFuncDef(self):
        itr=0
        while (itr<len(self.main)):
            if isinstance(self.main[itr], DefFuncObject):
                self.funcList.append(self.main.pop(itr))
                itr -= 1
            itr += 1

    def varAsignToCommands(self, varAsign):
        AsignCommands = []
        if not self.memory.isUsed(varAsign.variable.value):
            if isinstance(varAsign.expression[0], FuncCallObject):
                if varAsign.expression[0].name == "Point":
                    self.memory.mallocPoint(varAsign.variable.value)
                    return 
                if varAsign.expression[0].name == "State":
                    self.memory.mallocState(varAsign.variable.value)
                    return               
            self.memory.mallocInt(varAsign.variable.value)
        AsignCommands.append(self.createAsignCommand(varAsign.variable, "=", varAsign.expression[0]))
        if len(varAsign.expression) == 3:
            AsignCommands.append(self.createAsignCommand(varAsign.variable, varAsign.expression[1], varAsign.expression[2]))
        return AsignCommands
    
    def createAsignCommand(self, variable, op, tempVariable): #REFACTOR need to allow S: as well
        args = []
        if variable.tokenType == TokenType.NUMBER:
            args.append(variable.value)
        else:
            args.append(self.memory.getMemLoc(variable.value))
        if tempVariable.tokenType == TokenType.NUMBER:
            if isinstance(op, Token): properOp = "c:"+ op.value
            else: properOp = "c:"+ op
            args.append(properOp)
            args.append(tempVariable.value)
        else:
            if isinstance(op, Token): properOp = "g:"+ op.value
            else: properOp = "g:"+ op
            args.append(properOp)
            args.append(self.memory.getMemLoc(tempVariable.value))
        return CommandObject("up-modify-goal", args, variable.line, variable.file)

    def replaceArg(self, arg, callList, funcList):
        for itr, funcItem in enumerate(funcList):
            if arg.value == funcList[itr].value:
                if callList[itr].tokenType == TokenType.IDENTIFIER:
                    arg.value = str(self.memory.getMemLoc(callList[itr].value))
                else:
                    arg.value = callList[itr].value

    def funcCallToLines(self, funcCall):
        if funcCall.name in self.callStack:
            raise Exception("Recursion will not be suported. function canot call itself")
        self.callStack.append(funcCall.name)
        calledFunction = None
        for func in self.funcList:
            if func.name == funcCall.name:
                calledFunction = copy.deepcopy(func)
        lineList = calledFunction.lineList.lineList
        for item in lineList:
            if isinstance(item, CommandObject):
                for arg in item.argList:
                    self.replaceArg(arg, funcCall.args, calledFunction.argList)
            elif isinstance(item, defruleObject):
                for command in item.conditionList:
                    for arg in command.argList:
                        self.replaceArg(arg, funcCall.args, calledFunction.argList)
                for command in item.executeList:
                    for arg in command.argList:
                        self.replaceArg(arg, funcCall.args, calledFunction.argList)
            elif isinstance(item, VarAsignObject):
                for arg in item.expression:
                    self.replaceArg(arg, funcCall.args, calledFunction.argList)
            else:
                raise Exception("printing "+str(item.__class__)+" in Functions is not yet Iplamented!")
        #replace all of the variables used
        self.callStack.pop(-1)
        return lineList

    def interpretLine(self, lineList):
        newLineList = []
        idx = 0
        while idx < len(lineList):
            if isinstance(lineList[idx], CommandObject): 
                newLineList.append(defruleObject( self.TRUE_CONDITION, LineListObject([lineList[idx]])) )
            elif isinstance(lineList[idx], VarAsignObject): 
                commands = self.varAsignToCommands(lineList[idx])
                if commands != None:
                    newLineList = newLineList + commands
            elif isinstance(lineList[idx], IfObject): 
                newLineList += self.collapseIftoDefrule(lineList[idx])


            elif isinstance(lineList[idx], FuncCallObject): 
                #print("LINELIST BEFORE")
                #print(lineList)
                lineList = lineList[:idx] + self.funcCallToLines(lineList[idx]) + lineList[idx+1:]
                #print("LINELIST AFTER")
                #print(lineList)
                idx -= 1
            else:
                print("appending "+str(lineList[idx].__class__))
                newLineList.append(lineList[idx])
            idx += 1
        return newLineList

    def wrapCommandsInDefrules(self, lineList):
        for itr in range(len(lineList)):
            if isinstance(lineList[itr], CommandObject):
                lineList[itr] = defruleObject(self.TRUE_CONDITION, LineListObject([lineList[itr]]))

    def interpret(self):
        self.moveDefconst()
        self.moveFuncDef()
        self.main = self.interpretLine(self.main)
        self.wrapCommandsInDefrules(self.main)
        #for item in self.funcList:
        #    item.lineList.lineList = self.interpretLine(item.lineList.lineList)

