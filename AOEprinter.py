from data import *


class Printer:
    def __init__(self, main):
        self.main = main
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
        defruleStr += ')\n\n'
        return defruleStr
    
    def printLogicCommand(self, logicCommand):
        logicStr = "("
        logicStr += logicCommand.logicOp.value
        logicStr += " "
        for item in logicCommand.commands:
            if isinstance(item, defruleObject):
                logicStr += self.printDefrule(item)
            elif isinstance(item, defconstObject):
                logicStr += self.printDefconst(item)
        logicStr += ")"
        return logicStr

    def printCommand(self, command):
        #logicCommandObject
        commandStr = "("
        commandStr += command.name
        for item in command.argList:
            commandStr += " "
            commandStr += item.value
        commandStr += ")\n"
        return commandStr

    def printDefconst(self, const):
        return "(defconst "+const.name+" "+const.value+")\n"

    def print(self):
        for item in self.main:
            if isinstance(item, defruleObject):
                self.finalString += self.printDefrule(item)
            elif isinstance(item, defconstObject):
                self.finalString += self.printDefconst(item)
            else:
                raise Exception("printing "+str(item.__class__)+" is not yet Iplamented!")
