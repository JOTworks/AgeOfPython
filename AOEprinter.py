from data import *


class Printer:
    def __init__(self, main, funcList, constList):
        self.main = main
        self.funcList = funcList
        self.constList = constList
        self.finalString = ""


    def printDefrule(self, rule):
        defruleStr = '(defrule '
        for item in rule.conditionList.lineList:
            defruleStr += "  "
            if isinstance(item, CommandObject):
                defruleStr += self.printCommand(item)
            elif isinstance(item, logicCommandObject):
                defruleStr += self.printLogicCommand(item)
        defruleStr += '=>'
        for item in rule.executeList.lineList:
            defruleStr += "  "
            defruleStr += self.printCommand(item)
        defruleStr = defruleStr[:-1]
        defruleStr += '\n)\n'
        return defruleStr
    
    def printLogicCommand(self, logicCommand):
        logicStr = "("
        logicStr += logicCommand.logicOp.value
        logicStr += " "
        for item in logicCommand.commands:
            if isinstance(item, logicCommandObject):
                logicStr += self.printLogicCommand(item)
            elif isinstance(item, CommandObject):
                logicStr += self.printCommand(item)
        logicStr += ")"
        return logicStr

    def printCommand(self, command):
        #logicCommandObject
        commandStr = "("
        commandStr += command.name
        for item in command.argList:
            if isinstance(item, Token):
                commandStr += " "
                if item.tokenType == TokenType.STRING: commandStr += '"'
                commandStr += item.value
                if item.tokenType == TokenType.STRING: commandStr += '"'
            else:
                commandStr += " "
                commandStr += str(item)
        commandStr += ") ;"
        commandStr += (str(command.line) +" "+ command.file)
        commandStr += "\n"
        return commandStr

    def printDefconst(self, const):
        return "(defconst "+const.name+" "+const.value+") ;"+str(const.line)+" "+const.file+"\n"



    def print(self):
        for item in self.main:
            if isinstance(item, defruleObject):
                self.finalString += self.printDefrule(item)
            elif isinstance(item, defconstObject):
                self.finalString += self.printDefconst(item)
            #function calls should be broken down by the interpreter!
            #elif isinstance(item, FuncCallObject):
            #    self.finalString += self.printFuncCall(item)
            else:
                raise Exception("printing "+str(item.__class__)+" is not yet Iplamented!")
