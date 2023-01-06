from data import *


class Printer:
    def __init__(self, main, funcList, constList):
        self.main = main
        self.funcList = funcList
        self.constList = constList
        self.finalString = ""


    def printDefrule(self, rule):
        defruleStr = '(defrule '
        for item in rule.conditionList:
            defruleStr += "  "
            if isinstance(item, CommandObject):
                defruleStr += self.printCommand(item)
            elif isinstance(item, logicCommandObject):
                defruleStr += self.printLogicCommand(item)
        defruleStr += '=>'
        for item in rule.executeList:
            defruleStr += "  "
            defruleStr += self.printCommand(item)
        defruleStr = defruleStr[:-1]
        defruleStr += '\n);'+str(rule.position)+'\n'
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
                commandStr += item
        commandStr += ") ;"
        commandStr += (str(command.line) +" "+ command.file)
        commandStr += "\n"
        return commandStr

    def printDefconst(self, const):
        return "(defconst "+const.name+" "+const.value+") ;"+str(const.line)+" "+const.file+"\n"

    def printWrapper(self, wrapper):
        for item in wrapper.lineList:
            self.printObject(item)

    def printConstants(self):
        for constant in self.constList:
            if type(self.constList[constant]) == type("string"):
                self.finalString += "(defconst "+constant+" "+self.constList[constant]+")"
                self.finalString += " ;"+"unknown line or file"+"\n"
            else:
                self.finalString += "(defconst "+constant+" "+self.constList[constant].value+")"
                self.finalString += " ;"+str(self.constList[constant].line)+" "+self.constList[constant].file+"\n"


    def printObject(self, item):
        if isinstance(item, defruleObject):
            self.finalString += self.printDefrule(item)
        elif isinstance(item, defconstObject):
            self.finalString += self.printDefconst(item)
        elif isinstance(item, Wrapper):
            self.printWrapper(item)
        else:
            raise Exception("printing "+str(item.__class__)+" is not yet Iplamented!")

    def print(self):
        self.printConstants()
        for item in self.main:
            self.printObject(item)
            
                    
            #function calls should be broken down by the interpreter!
            #elif isinstance(item, FuncCallObject):
            #    self.finalString += self.printFuncCall(item)
            
