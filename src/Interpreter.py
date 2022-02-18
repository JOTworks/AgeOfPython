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


############################################################################### 
    def varAsignToCommands(self, varAsign):
        AsignCommands = []
        if not self.memory.isUsed(varAsign.variable.value):
            if isinstance(varAsign.expression[0], FuncCallObject):
                if varAsign.expression[0].name == "Point":
                    print(varAsign.variable.value)
                    self.memory.mallocPoint(varAsign.variable.value)
                    return 
                if varAsign.expression[0].name == "State":
                    self.memory.mallocState(varAsign.variable.value)
                    return               
            self.memory.mallocInt(varAsign.variable.value)
        if not isinstance(varAsign.expression[0], FuncCallObject):
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
###########################################################################################

    def interpretLine(self, lineList):
        newLineList = []
        for line in lineList:
            newLineList.append(line.interpret())
        return newLineList

    def moveDefconst(self, InList):
        tempConstList = []
        itr=0
        while (itr<len(InList)):
            if isinstance(InList[itr], defconstObject):
                tempConstList.append(InList.pop(itr))
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
                    tempList.append(self.functionCallToLines(line, callStack))
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
                raise Exception("there is a class besides wrapper or defrule when trying to replace jump values")
        return count

    def replaceJumpValues(self, lineList):
        for line in lineList:
            if isinstance(line, Wrapper):
                if line.Type == IfObject:
                    for rule in line.lineList:
                        if isinstance(rule, defruleObject):
                            for command in rule.executeList:
                                if command.name == "up-jump-direct":
                                    print("COMMAND TOKEN TYPE: "+str(command.argList[-1].tokenType))
                                    if command.argList[-1].tokenType == TokenType.LAST_RULE:
                                        command.argList[-1].value = str(line.rulePosition(-1))
                                    elif command.argList[-1].tokenType == TokenType.SECOND_RULE:
                                        command.argList[-1].value = str(line.rulePosition(1))

                                    #ifel string based on command.arg[-1] token type
                                    #command.arg[-1] == something
                                

                self.replaceJumpValues(line.lineList)

    def allocateArg(self, inCommand):
        if not isinstance(inCommand, CommandObject):
            raise Exception(str(inCommand.__class__)+" is not a CommandObject")
        print(inCommand)
        if len(inCommand.argList) == 0:
            return
        for arg in inCommand.argList:
            if isinstance(arg, str):
                arg = Token(TokenType.UNIDENTIFIED, arg, "-1", "")
            elif not isinstance(arg, Token):
                raise Exception(str(arg.__class__)+" is not a Token")
            if (len(arg.value) >= 5) and (arg.value[:5] == "main/"):
                if not self.memory.isUsed(arg.value):
                    self.memory.mallocInt(arg.value)
                print(arg.value)
                print("ASIGNED "+str(self.memory.getMemLoc(arg.value)))
                arg.value = str(self.memory.getMemLoc(arg.value))
                

    def allocateMemory(self, inList):
        #very bad allocation thing
        for item in inList:
            if isinstance(item, Wrapper):
                self.allocateMemory(item.lineList)
            elif isinstance(item, defruleObject):
                for condition in item.conditionList:
                    if isinstance(condition, logicCommandObject):
                        for command in condition.commands:
                            self.allocateArg(command)
                    else:
                        self.allocateArg(condition)
                for execute in item.executeList:
                    self.allocateArg(execute)


            else: raise Exception("allocateMemory() can only parce defrulesObjects, not "+str(item.__class__))
    
    def interpret(self):
        self.constList = self.moveDefconst(self.main)
        self.funcList = self.moveFuncDef(self.main)
        #self.convertdefrulesToIfs(self.main) #May be nessesary later
        firstCallStack = CallStackItem(FuncCallObject("main",[]),[])
        self.main = self.flattenFuncCalls(self.main, [firstCallStack])
        
        self.main = self.interpretLine(self.main) #turns all objects in to wrappers full of commands
        #self.main = self.wrapCommandsInDefrules(self.main) #turns all commands into defrules
        self.allocateMemory(self.main) #allocate memory switch out identifiers for memoryLocations.
        #self.main = self.optimizeRules(self.main)
        #self.addPositiontoDefrules(self.main, 0)
        #self.replaceJumpValues(self.main) #adds the jump commands now that it knows what rules there are