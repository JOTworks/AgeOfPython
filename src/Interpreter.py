from pprint import pprint
import copy
from Memory import Memory
from data import *
from enums import Structure

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
                    tempList.append(self.functionCallToLines(line.expression[0], callStack, line.variable))
                    #tempList.append(line) #not needed as the assign will always happen in the return.
                    #raise Exception("function returns are not Supported")
                else:
                    tempList.append(line)
            elif isinstance(line, ConditionalObject):
                line.lineList = self.flattenFuncCalls(line.lineList, callStack)
                tempList.append(line)
            elif isinstance(line, CommandObject):
                tempList.append(line)
            elif isinstance(line, ReturnObject):
                line.set_assignVars([callStack[-1].assignVars])
                tempList.append(line)
            else:
                raise Exception("Need to implament "+str(line.__class__)+" in flattenFuncCalls function")
        return tempList

    def functionCallToLines(self, funcCall, callStack, assignVars = None): 
        for callStackItem in callStack:
            if funcCall.name == callStackItem.funcCall.name:
                raise Exception("Recursion will not be suported. function "+funcCall.name+" canot call itself")
        functionCallWrapper = Wrapper(FuncCallObject, [], funcCall.name)
        argAssignWrapper = Wrapper(ArgAssignObject, [])
        calledFunc = self.getFunctionCopyByName(funcCall.name)
        nextCallStack = CallStackItem(funcCall, calledFunc.argList, assignVars)
        argAssignWrapper.lineList = []
        for i in range(len(calledFunc.argList)):
            calledFunc.argList[i].scope(callStack + [nextCallStack])
            #passed_var_type = 
            #make it so functions pass a specific type (default is int)
            #argAssignList.append(VarAsignObject(calledFunc.argList[i], passed_var_type, -1, ''))
            argAssignWrapper.lineList.append(VarAsignObject(copy.deepcopy(calledFunc.argList[i]), [copy.deepcopy(funcCall.args[i])], -1, ''))
        #for line in argAssignList:
            #line.scope(callStack + [nextCallStack])
        flat_function = self.flattenFuncCalls(calledFunc.lineList, callStack + [nextCallStack])
        functionCallWrapper.lineList = [argAssignWrapper] + flat_function
        #inner_flat = self.flattenFuncCalls(calledFunc.lineList, callStack + [nextCallStack])
        #if inner_flat != None:
        #    functionCallWrapper.lineList += inner_flat

        return functionCallWrapper
    
    def optimizeRules(self, inList):
        newList = []
        i = 0
        while i < len(inList):
            if isinstance(inList[i], Wrapper):
               inList[i].lineList = self.optimizeRules(inList[i].lineList)
               newList.append(inList[i]) 
            elif isinstance(inList[i], defruleObject):
                if inList[i].true_condition():
                    new_defrule = defruleObject(TRUE_CONDITION,[])
                    while((i < len(inList)) and isinstance(inList[i], defruleObject) and inList[i].true_condition()):
                        new_defrule.executeList += inList[i].executeList
                        i += 1
                    i -= 1
                    newList.append(new_defrule)
                else:
                    newList.append(inList[i])
            else:
                raise Exception("there is a class besides wrapper or defrule when trying to optimizeRules()\n"+str(line))
            i += 1
        return newList
    
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
                            command.argList[-1].value = str(inLine[1].position)
                            isUpJump = True
                        elif command.argList[-1].tokenType == TokenType.FIRST_RULE:
                            command.argList[-1].value = str(inLine[0].position)
                        elif command.argList[-1].tokenType == TokenType.RETURN_POINT:
                            command.argList[-1].value = get_return_Point()
                        else:
                            raise Exception("cammand.name == up-jump-direct but TokenType is not [placement]_RULE")

                tempList.append(line)
        return tempList

    def isVariable(self, variable):
        if isinstance(variable, Structure):
            return False
        return (len(variable) >= 5) and (variable[:5] == "main/")

    def get_type_of_thing(self, thing):
        if isReservedInitFunc(thing.value):
            return thing.value
        elif self.isVariable(thing.value):
            if thing.value.split('/')[-1] in self.constList:
                return Structure.INT
            else:
                return self.memory.get_type(thing.value)
        elif thing.tokenType == TokenType.NUMBER:
            return Structure.INT
        else:
            raise Exception(f'cant figure out what type {thing} is')
    def inc_memLoc_for_assign_command(self, command, inc):
        if not isinstance(command, CommandObject): raise Exception("inc_memLoc_for_assign_command needed a command")
        if command.name != 'up-modify-goal': raise Exception(f"inc_memLoc_for_assign_command needed up-modify-goal command not {command.name}")
        if isinstance(command.argList[0], Token):
            command.argList[0].value = str(int(command.argList[0].value) + inc)
        else: command.argList[0] = str(int(command.argList[0]) + inc)
        if isinstance(command.argList[2], Token):
            command.argList[2].value = str(int(command.argList[2].value) + inc)
        else: command.argList[2] = str(int(command.argList[2]) + inc)
        return command

    def allocateArg(self, inCommand, isArgAssign = False):
        if isinstance(inCommand, logicCommandObject):
            for command in inCommand.commands:
                self.allocateArg(command)
            return
        if not isinstance(inCommand, CommandObject):
            raise Exception(str(inCommand.__class__)+" is not a CommandObject")
        for arg in inCommand.argList:
            if isinstance(arg, str):
                arg = Token(TokenType.UNIDENTIFIED, arg, "-1", "")
                print(Fore.YELLOW+f"warning: arg {arg} is a str and not a Token"+Fore.WHITE)
            if not isinstance(arg, Token):
                raise Exception(str(arg.__class__)+" is not a Token")

        if inCommand.name == "defconst":
            self.constList[inCommand.argList[0].value.split('/')[-1]] = inCommand.argList[1].value

        elif inCommand.name == "up-modify-goal":
            
            goal_name = inCommand.argList[0].value
            oporator = inCommand.argList[1]
            assign_value = inCommand.argList[2]

            #alocating goal_name
            if inCommand.argList[0].value.split('/')[-1] in self.constList:
                raise Exception("dont asign const to variable!")

            if not self.memory.isUsed(inCommand.argList[0].value):
                s_type = self.get_type_of_thing(inCommand.argList[2])
                if isArgAssign and inCommand.argList[2].value.split('/')[-1] in self.constList:
                    self.constList[inCommand.argList[0].value] = self.constList[inCommand.argList[2].value.split('/')[-1]]
                    return []
                else:
                    self.memory.malloc(inCommand.argList[0].value, s_type)
            inCommand.argList[0].value = str(self.memory.getMemLoc(inCommand.argList[0].value))

            #alocate assign_value 
            if self.isVariable(inCommand.argList[2].value):
                if inCommand.argList[2].value.split('/')[-1] in self.constList:
                    inCommand.argList[1].value = "c:="
                    inCommand.argList[2].value = self.constList[inCommand.argList[2].value.split('/')[-1]]
                elif inCommand.argList[2].value in self.constList:
                    inCommand.argList[1].value = "c:="
                    inCommand.argList[2].value = self.constList[inCommand.argList[2].value]
                else:
                    typeLength = get_type_length(self.get_type_of_thing(inCommand.argList[2]))
                    if self.memory.isUsed(inCommand.argList[2].value):
                        inCommand.argList[2] = str(self.memory.getMemLoc(inCommand.argList[2].value))
                    else:
                        raise Exception(f'variable {inCommand.argList[2].value} has not been initialized, File:{inCommand.file} {inCommand.line}')
                    
                    outCommands = []
                    for i in range(0,typeLength):
                        newCommand = CommandObject(inCommand.name,inCommand.argList,inCommand.line,inCommand.file)
                        newCommand = self.inc_memLoc_for_assign_command(newCommand,i)
                        outCommands.append(newCommand)
                    return outCommands
            elif isReservedInitFunc(inCommand.argList[2].value):
                inCommand.argList[2] = ZERO_NUMBER_TOKEN #turned to 0 to be deleted later
            else:
                pass #it is a number or string and we dont need to translate to MemLoc
            #adding structure asignments
        else: #alocate all non "up-modify-goal" commands
            for arg in inCommand.argList:
                if self.isVariable(arg.value):
                    if arg.value.split('/')[-1] in self.constList:
                        arg.value = self.constList[arg.value.split('/')[-1]]
                    if arg.value in self.constList:
                        arg.value = self.constList[arg.value]
                    elif self.memory.isUsed(arg.value):
                        arg.value = str(self.memory.getMemLoc(arg.value))
                    else:
                        arg.value = arg.value.split('/')[-1]
                        #print(self.memory.printUsedMemory())
                        #print(self.constList)
                        #raise Exception(f'arg {arg.value} is not in memory, and canot be referenced')              
        return [inCommand]   

    def allocateMemory(self, inList):
        for item in inList:
            if isinstance(item, Wrapper):
                if item.Type == ArgAssignObject:
                    temp_ArgAssignCommands = []
                    for line in item.lineList:
                        if len(line.executeList) != 1:
                            raise Exception("ArgAssignObjects wrapper defrules' should only have 1 execute command")
                        line.executeList = self.allocateArg(line.executeList[0], isArgAssign=True)
                else:
                    self.allocateMemory(item.lineList)
                if item.Type == FuncCallObject:
                    #print(f"++++++++before Free {item.func_name}")
                    #print(self.memory.printUsedMemory())
                    self.memory.free_func_variables(self.constList, item.func_name)
                    
            elif isinstance(item, defconstObject):
                self.constList[item.name.value.split('/')[-1]] = item.value.value

            elif isinstance(item, defruleObject):
                for condition in item.conditionList:
                    if isinstance(condition, logicCommandObject):
                        for command in condition.commands:
                            self.allocateArg(command)
                    else:
                        self.allocateArg(condition)
                temp_executeList = []
                for execute in item.executeList:
                    temp_executeList += self.allocateArg(execute)
                item.executeList = temp_executeList
            else: raise Exception("allocateMemory() can only parce defrulesObjects, not "+str(item.__class__)+"\n"+str(item)+"\n"+str(inList))
        inListWithoutDefConst = [item for item in inList if not isinstance(item, defconstObject)]
        return inListWithoutDefConst

    def interpret(self):
        self.constList = self.moveDefconst(self.main)
        self.funcList = self.moveFuncDef(self.main)
        self.main = self.main #+ self.funcList #something to jumpPastFunctions 
        #self.convertdefrulesToIfs(self.main) #May be nessesary later
        firstCallStack = CallStackItem(FuncCallObject("main",[]),[])
        self.main = self.flattenFuncCalls(self.main, [firstCallStack])
        self.main = self.interpretLine(self.main) #turns all objects in to wrappers full of commands
        ##self.main = self.wrapCommandsInDefrules(self.main) #turns all commands into defrules
        self.main = self.allocateMemory(self.main) #allocate memory switch out identifiers for memoryLocations.
        #self.main = self.optimizeRules(self.main)
        self.addPositiontoDefrules(self.main, 0)
        self.main = self.replaceJumpValues(self.main)
        
        #for line in self.main:
        #    if isinstance(line, Wrapper):
        #        line = self.replaceJumpValues(line, None) #adds the jump commands now that it knows what rules there are