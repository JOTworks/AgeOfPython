from distutils import command
from pprint import pprint
import copy
from Memory import Memory
from data import *

class Interpreter:
    def __init__(self, main):
        self.main = main
        self.newMain = []
        self.constList = []
        self.funcList = []
        self.memory = Memory()

    def interpretLine(self, lineList):
        newLineList = []
        for line in lineList:
            newLineList.append(line.interpret())
        return newLineList

    def moveDefconst(self, InList):
        tempConstList = {}
        itr=0
        while (itr<len(InList)):
            if isinstance(InList[itr], defconstObject):
                
                tempConstList[InList[itr].name] = (InList[itr].value)
                InList.pop(itr)
                itr -= 1
            itr += 1
        return tempConstList

    def moveFuncDef(self, InList):
        tempFuncList = []
        itr=0
        while (itr<len(InList)):
            if isinstance(InList[itr], DefFuncObject):
                tempFuncList.append(InList.pop(itr))
                itr -= 1
            itr += 1
        return tempFuncList

    def getFunctionCopyByName(self, name):
        for func in self.funcList:
            if name == func.name:
                return copy.deepcopy(func)
        raise Exception("Canot call fuction "+name+"() that is not Defined")

    def flattenFuncCalls(self, inList, callStack):
        tempList = []
        for line in inList:
            line.scope(callStack)
            if isinstance(line, FuncCallObject):
                tempList.append(self.functionCallToLines(line, callStack))
            elif isinstance(line, VarAsignObject):
                if line.isSetToFunction():
                    raise Exception("function returns are not Supported")
                else:
                    tempList.append(line)
            elif isinstance(line, ConditionalObject):
                line.lineList = self.flattenFuncCalls(line.lineList, callStack)
                tempList.append(line)
            elif isinstance(line, CommandObject):
                tempList.append(line)
            else:
                raise Exception("Need to implament "+str(line.__class__)+" in flattenFuncCalls function")
        return tempList

    def functionCallToLines(self, funcCall, callStack): 
        for callStackItem in callStack:
            if funcCall.name == callStackItem.funcCall.name:
                raise Exception("Recursion will not be suported. function "+funcCall.name+" canot call itself")
        functionCallWrapper = Wrapper(FuncCallObject, [])
        calledFunc = self.getFunctionCopyByName(funcCall.name)
        nextCallStack = CallStackItem(funcCall, calledFunc.argList)
        functionCallWrapper.lineList = self.flattenFuncCalls(calledFunc.lineList, callStack + [nextCallStack])
        return functionCallWrapper
    
    def optimizeRules(self, inList):
        return inList
    
    def addPositiontoDefrules(self, lineList, count):
        #newLineList = []
        for line in lineList:
            #newLineList.append(line.interpret())
            if isinstance(line, Wrapper):
                count = self.addPositiontoDefrules(line.lineList, count)
            elif isinstance(line, defruleObject):
                line.position = count
                count += 1
            else:
                raise Exception("there is a class besides wrapper or defrule when trying to replace jump values\n"+str(line))
        return count

    def replaceJumpValues(self, inLine):
        tempList = []
        for line in inLine:
            if isinstance(line, Wrapper):
                tempList.append(Wrapper(line.Type, self.replaceJumpValues(line.lineList)))
            if isinstance(line, defruleObject):
                isUpJump = False
                for command in line.executeList:
                    if command.name == "up-jump-direct":
                        if command.argList[-1].tokenType == TokenType.LAST_RULE:
                            command.argList[-1].value = str(inLine[-1].position)
                            isUpJump = True
                        elif command.argList[-1].tokenType == TokenType.SECOND_RULE:
                            raise Exception("broken code, should not have run this")
                            command.argList[-1].value = str(line.rulePosition(1))
                if(isUpJump):
                    print("++++++++++++++++++++")
                    print(line)
                    print("++++++++++++++++++++")
                tempList.append(line)
        return tempList
                    

    def allocateArg(self, inCommand):
        if not isinstance(inCommand, CommandObject):
            raise Exception(str(inCommand.__class__)+" is not a CommandObject")
        if len(inCommand.argList) == 0:
            return
        for arg in inCommand.argList:
            if isinstance(arg, str):
                arg = Token(TokenType.UNIDENTIFIED, arg, "-1", "")
            elif not isinstance(arg, Token):
                raise Exception(str(arg.__class__)+" is not a Token")
            tempSplitArgValue = arg.value.split('()')
            arg.value = tempSplitArgValue[0]
            structure = None
            if len(tempSplitArgValue) > 1:
                structure = tempSplitArgValue[1]
            if (len(arg.value) >= 5) and (arg.value[:5] == "main/"):

                if (not self.memory.isUsed(arg.value)) and (inCommand.name == "up-modify-goal"):
                    if structure == None:
                        if arg.value.split('/')[-1] in self.constList:
                            arg.value = self.constList[arg.value.split('/')[-1]].value
                            return
                        self.memory.mallocInt(arg.value)
                    elif structure == "Int":
                        self.memory.mallocInt(arg.value)
                    elif structure == "Point":
                        self.memory.mallocPoint(arg.value)
                    elif structure == "State":
                        self.memory.mallocState(arg.value)
                    elif structure == "Const":
                        return
                    else:
                        raise Exception("Structure "+structure+" not recognized")

                print(arg.value)
                if self.memory.isUsed(arg.value):
                    print("IS USED")
                    arg.value = str(self.memory.getMemLoc(arg.value))
                else:
                    arg.value = arg.value.split('/')[-1]
                
    def allocateMemory(self, inList):
        for item in inList:
            if isinstance(item, Wrapper):
                self.allocateMemory(item.lineList)
            elif isinstance(item, defconstObject):
                self.constList[item.name] = item.value
            elif isinstance(item, defruleObject):
                for condition in item.conditionList:
                    if isinstance(condition, logicCommandObject):
                        for command in condition.commands:
                            self.allocateArg(command)
                    else:
                        self.allocateArg(condition)
                for execute in item.executeList:
                    self.allocateArg(execute)
            else: raise Exception("allocateMemory() can only parce defrulesObjects, not "+str(item.__class__)+"\n"+str(item))
        inListWithoutDefConst = [item for item in inList if not isinstance(item, defconstObject)]
        return inListWithoutDefConst

    def interpret(self):
        self.constList = self.moveDefconst(self.main)
        self.funcList = self.moveFuncDef(self.main)
        #self.convertdefrulesToIfs(self.main) #May be nessesary later
        firstCallStack = CallStackItem(FuncCallObject("main",[]),[])
        self.main = self.flattenFuncCalls(self.main, [firstCallStack])
        self.main = self.interpretLine(self.main) #turns all objects in to wrappers full of commands
        #self.main = self.wrapCommandsInDefrules(self.main) #turns all commands into defrules
        self.main = self.allocateMemory(self.main) #allocate memory switch out identifiers for memoryLocations.
        #self.main = self.optimizeRules(self.main)
        self.addPositiontoDefrules(self.main, 0)
        self.main = self.replaceJumpValues(self.main)
        
        #for line in self.main:
        #    if isinstance(line, Wrapper):
        #        line = self.replaceJumpValues(line, None) #adds the jump commands now that it knows what rules there are