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
        self.TRUE_CONDITION = [CommandObject("true",[],"","")]
        
    def collapseIftoDefrule(self, inIf):
        if not isinstance(inIf, IfObject):
            raise Exception("Did not pass IF to collapseIftoDefrule")
        tempMain = []
        deepistIf = True
        itr = 0
        while (itr < len(inIf.lineList)):
            if isinstance( inIf.lineList[itr], (IfObject,defruleObject,FuncCallObject) ):
                deepistIf = False
            if isinstance( inIf.lineList[itr], VarAsignObject):
                commands = self.varAsignToCommands(inIf.lineList[itr])
                if commands != None:
                    inIf.lineList = inIf.lineList[:itr] + self.varAsignToCommands(inIf.lineList[itr]) + inIf.lineList[itr:+1]
                else:
                    inIf.lineList = inIf.lineList[:itr] + inIf.lineList[itr+1:]
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

    def scope(self, variables, callStack):
        if isinstance(variables, list):
            for var in variables:
                self.scope(var, callStack)
        elif isinstance(variables, CommandObject):
            self.scope(variables.argList, callStack)
        elif isinstance(variables, Token):
            if variables.tokenType == TokenType.IDENTIFIER:
                if len(callStack) == 1:
                    defArgList = []
                else:
                    defArgList = self.getFunctionCopyByName(callStack[-1].name).argList
                inArgList = False
                for itr in range(len(defArgList)):
                    if variables.value == defArgList[itr].value:
                        variables.value = callStack[-1].args[itr].value
                        inArgList = True
                if not inArgList:
                    variables.value = "/".join([o.name for o in callStack])+"/"+ variables.value
        else:
            raise Exception("Need to implament "+str(variables.__class__)+" in scope function")

    def scopeVariables(self, line, callStack):
        if isinstance(line, FuncCallObject):
            self.scope(line.args, callStack)
        elif isinstance(line, VarAsignObject):
            self.scope(line.variable, callStack)
            self.scope(line.expression, callStack)
        elif isinstance(line, CommandObject):
            self.scope(line.argList, callStack)
        elif isinstance(line, IfObject):
            self.scope(line.conditionList, callStack)
        else:
            raise Exception("Need to implament "+str(line.__class__)+" in scopeVariables function")
    
    def flattenFuncCalls(self, inList, callStack):
        tempList = []
        for line in inList:
            self.scopeVariables(line, callStack)
            if isinstance(line, FuncCallObject):
                tempList.append(self.functionCallToLines(line, callStack))
            elif isinstance(line, VarAsignObject):
                if line.isSetToFunction():
                    tempList.append(self.functionCallToLines(line, callStack))
                else:
                    tempList.append(line)
            elif isinstance(line, IfObject):
                line.lineList = self.flattenFuncCalls(line.lineList, callStack)
                tempList.append(line)
            elif isinstance(line, CommandObject):
                tempList.append(line)
            else:
                raise Exception("Need to implament "+str(line.__class__)+" in flattenFuncCalls function")
        return tempList

    def functionCallToLines(self, funcCall, callStack): 
        for call in callStack:
            if funcCall.name == call.name:
                raise Exception("Recursion will not be suported. function "+funcCall.name+" canot call itself")
        functionCallWrapper = Wrapper(FuncCallObject, [])
        calledFunc = self.getFunctionCopyByName(funcCall.name)
        functionCallWrapper.lineList = self.flattenFuncCalls(calledFunc.lineList, callStack + [funcCall])
        return functionCallWrapper
    
    def optimizeRules(self):
        pass
   
    def interpret(self):
        self.constList = self.moveDefconst(self.main)
        self.funcList = self.moveFuncDef(self.main)
        #self.convertdefrulesToIfs(self.main) #May be nessesary later
        self.main = self.flattenFuncCalls(self.main, [FuncCallObject("main",[])] )
        
        #!self.main = self.allocateMemory(self.main) #allocate memory switch out identifiers for memoryLocations.
        #!self.main = self.interpretLine(self.main) #turns all objects in to wrappers full of commands
        #!self.main = self.wrapCommandsInDefrules(self.main) #turns all commands into defrules
        self.main = self.optimizeRules(self.main)
        #!self.main = self.replaceJumpvalues(self.main) #adds the jump commands now that it knows what rules there are