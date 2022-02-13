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

    def flattenFuncCalls(self, inList):
        callStack = ["main"]
        tempList = []
        for line in inList:
            if isinstance(line, FuncCallObject):
                tempList.append(self.functionCallToLines(line, callStack))
            elif isinstance(line, VarAsignObject) and line.isSetToFunction():
                tempList.append(self.functionCallToLines(line, callStack))
                line.expression = line.expression[0].returnVar
                tempList.append(self.varAsignToCommands(line)) #this will probably be a bug later on with function scoped variables
            else:
                tempList.append(line)
        return tempList

    #needs to switch out function parameters and add function Scope
    def functionCallToLines(self, funcCall, callStack): 
        if funcCall.name in callStack: raise Exception("Recursion will not be suported. function canot call itself")
        else: callStack.append(funcCall.name)
        functionCallWrapper = Wrapper(FuncCallObject, [])
        calledFunc = self.getFunctionCopyByName(funcCall.name)
        for item in calledFunc.lineList:
            if isinstance(item, FuncCallObject):
                functionCallWrapper.lineList.append(self.functionCalltoLines(item, callStack))
            else:
                functionCallWrapper.lineList.append(item)
        return functionCallWrapper

    def interpret(self):
        self.constList = self.moveDefconst(self.main)
        self.funcList = self.moveFuncDef(self.main)
        #self.convertdefrulesToIfs(self.main) #May be nessesary later
        self.main = self.flattenFuncCalls(self.main)
        #replace function calls #add to stack trace, and deal with returns #RETURNS ONLY ALOWED AT THE END
        #allocate memory switch out identifiers for memoryLocations.
        #self.main = self.interpretLine(self.main)
        #self.wrapCommandsInDefrules(self.main)
        #interpreteLine is Scoping (how deep i am in interpreteLine) pass memory to each scope
        #funcCallStack, how many functions im in # add funcstack to var name in mem exp. /func/x
        #as i interpret lines, turn every object into a wrapper (list of rules or commands)
        #optimize wraped objects
        #add goto functions

#        def modulate(w,y,z)
#            (set food total w)
#            (set wood total y)
#            (set gold total z)
#            d = 14
#            return d
#        
#        
#        x = modulate(a,b,c)
#        
#        if(true):
#            (set food total w)
#            (set wood total y)
#            (set gold total z)
#            /modulate/d = 14
#            x = /modulate/d
#
#
#        x = 1
#        if(x):
#            d = x
#            (set food total a)
#            (set wood total b)
#            (set gold total c)
#            /modulate/d = 14              #setResorces(a,b,c)
#
#
#        1 x
#        2   d
#        3   /modulate/x
#        4
#        5
#
#        1 x
#        2  
#        3   
#        4
#        5