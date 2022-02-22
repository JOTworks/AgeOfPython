
from pdb import line_prefix
from os import name
from enums import TokenType
import typing
import dataclasses

class PrettyPrinter(object):
    def __repr__(self):
      lines = [self.__class__.__name__ + ':']
      for key, val in vars(self).items():
          if val.__class__.__name__ == "list":
            #print("###"+key.__class__.__name__+"###"+val.__class__.__name__+"###")
            lines += '{}:'.format(key).split('\n')
            for item in val:
              if item is None:
                lines += '***NONTYPTE***'
              else:  
                lines += '| {}'.format(item).split('\n')
          else:
            lines += '{}: {}'.format(key, val).split('\n')

      return ( '\n|    '.join(lines) )

class Token(PrettyPrinter):
  def __init__(self, tokenType, value, line, file):
    self.tokenType = tokenType
    self.value = value
    self.line = line
    self.file = file
    self.lineNum = 0
  def __repr__(self):
    tempValue = self.value
    if self.value == '\n':
      tempValue = '/n'
    return("["+tempValue +" "+str(self.line)+self.file+"]")
  def scope(self, callStack):
    if self.tokenType == TokenType.IDENTIFIER:
      if len(callStack) == 1:
          defArgList = []
      else:
          defArgList = callStack[-1].defFuncArgs
      inArgList = False
      for itr in range(len(defArgList)):
          if self.value == defArgList[itr].value:
              self.value = callStack[-1].funcCall.args[itr].value
              inArgList = True
      if not inArgList:
          self.value = "/".join([o.funcCall.name for o in callStack])+"/"+ self.value

class Wrapper(PrettyPrinter):
  def __init__(self, Type, lineList):
    self.Type = Type
    self.lineList = lineList
  def interpret(self):
    newList = []
    for line in self.lineList:
      newList.append(line.interpret())
      #raise Exception("LINE"+str(line))
    return Wrapper(self.Type, newList)
  def rulePosition(self,index): #TODO: this will be a problem later
    if index == 1:
      return self.lineList[0].position + 1
    elif index == -1:
      return self.lineList[-1].position
    else:
      raise Exception("only 1 and -1 is supported for rulePosition()")

class LoadIfObject():
  def __init__(self, name, arg = ""):
    self.name = name
    self.arg = arg
  def __repr__(self):

    return ("LOADIF name:"+str(self.name)+" args:"+str(self.arg))
class logicCommandObject(PrettyPrinter):
  def __init__(self, logicOp, commands):
    self.logicOp = logicOp
    self.commands = commands
  def scope(self, callStack):
    for command in self.commands:
      command.scope(callStack)

class defconstObject(PrettyPrinter):
  def __init__(self, name, value, line, file):
    self.name = name
    self.value = value
    self.line = line
    self.file = file

class defruleObject(PrettyPrinter):
  def __init__(self, conditionList, executeList):
    self.conditionList = conditionList
    self.executeList = executeList
    self.position = -1

class CommandObject(PrettyPrinter):
  def __init__(self, name, argList, line, file):
    self.line = line
    self.file = file
    self.name = name
    self.argList = argList
  def __repr__(self):
    return ("COMMAND name:"+str(self.name)+" args:"+str(self.argList))
  def scope(self, callStack):
    for line in self.argList:
      line.scope(callStack)
  def interpret(self):
      return defruleObject(TRUE_CONDITION, [self])

class ReturnObject(PrettyPrinter):
  def __init__(self, arg):
    self.arg = arg

class VarInit(PrettyPrinter):
  def __init__(self, name, args):
    self.name = name
    self.args = args
  def scope(self, callStack):
    for line in self.args:
      line.scope(callStack)

class VarAsignObject(PrettyPrinter):
  def __init__(self, variable, expression, line, file):
    self.variable = variable
    self.expression = expression
    self.line = line
    self.file = file
  def scope(self, callStack):
      self.variable.scope(callStack)
      for item in self.expression:
        item.scope(callStack)
  def isSetToFunction(self):
    if len(self.expression)==1:
      if isinstance(self.expression[0], FuncCallObject):
        return True
    return False
  def interpret(self):
    asignCommands = []
    if isinstance(self.expression[0], VarInit): #TODO: this is BROKEN!
      if self.expression[0].name == "Const":
        return defconstObject(self.variable.value.split('/')[-1], self.expression[0].args[0],"","")
      self.variable.value = self.variable.value + "()" + self.expression[0].name

      asignCommands.append(self.createAsignCommand(self.variable, "=", ZERO_NUMBER_TOKEN))
    else:
      asignCommands.append(self.createAsignCommand(self.variable, "=", self.expression[0]))
      if len(self.expression) == 3:
        asignCommands.append(self.createAsignCommand(self.variable, self.expression[1], self.expression[2]))
    return defruleObject(TRUE_CONDITION, asignCommands)
  def createAsignCommand(self, variable, op, tempVariable):
    args = []
    args.append(variable)
    if tempVariable.tokenType == TokenType.NUMBER:
        if isinstance(op, Token): properOp = "c:"+ op.value
        else: properOp = "c:"+ op
    else:
        if isinstance(op, Token): properOp = "g:"+ op.value
        else: properOp = "g:"+ op
    args.append(properOp)
    args.append(tempVariable)
    return CommandObject("up-modify-goal", args, variable.line, variable.file)

class ConditionalObject(PrettyPrinter):
  def __init__(self, conditionList, lineList):
    self.conditionList = conditionList
    self.lineList = lineList
  def scope(self, callStack):
    for line in self.conditionList:
      line.scope(callStack)

class IfObject(ConditionalObject):
  def __init__(self, conditionList, lineList):
    super().__init__(conditionList, lineList)
  def interpret(self):
    isDisableSelf = False
    newList = []
    newList.append(defruleObject(self.conditionList, [JUMP_1_COMMANDS()]))
    newList.append(defruleObject(TRUE_CONDITION, [JUMP_LAST_COMMAND()]))
    for line in self.lineList:
      if isinstance(line, CommandObject) and (line.name == "disable-self"):
        isDisableSelf = True
      else:
        newList.append(line.interpret())
    newList.append(defruleObject( TRUE_CONDITION, [DO_NOTHING_COMMAND]))
    if isDisableSelf:
      newList[0].executeList.append(DISABLE_SELF_COMMAND)
    return Wrapper(IfObject, newList)

class ElseObject(ConditionalObject):
  def __init__(self, conditionList, lineList):
    super().__init__(conditionList, lineList)

class WhileLoopObject(ConditionalObject):
  def __init__(self, conditionList, lineList):
    super().__init__(conditionList, lineList)

class ForLoopObject(ConditionalObject):
  def __init__(self, lineList, iterator, itrStartValue, itrEndValue, itrJumpValue):
    lessthenToken = Token(TokenType.MATHOP, "<", -1, "")
    numberToken = Token(TokenType.NUMBER, itrEndValue, -1, "")
    conditionals = [CommandObject("up-compare-goal",[iterator, lessthenToken, numberToken])]
    super().__init__(conditionals, lineList)
    self.iterator = iterator
    self.itrStartValue = itrStartValue
    self.itrJumpValue = itrJumpValue

class DefFuncObject(PrettyPrinter):
  def __init__(self, name, argList, lineList, returnValue):
    self.name = name
    self.argList = argList
    self.lineList = lineList
    self.returnValue = returnValue

class FuncCallObject(PrettyPrinter):
  def __init__(self, name, args):
    self.name = name
    self.args = args
  def scope(self, callStack):
    for line in self.args:
      line.scope(callStack)

class CallStackItem(PrettyPrinter):
  def __init__(self, funcCall, defFuncArgs):
    self.funcCall = funcCall
    self.defFuncArgs = defFuncArgs

  def isSetToFunction(self):
    if isinstance(self.expression[0], FuncCallObject):
      return True
    else:
      return False

#TODO change all of these to returns
TRUE_CONDITION = [CommandObject("true",[],"","")]
NOT_TOKEN = Token(TokenType.LOGIC_OP,"not",-1,"")
ZERO_NUMBER_TOKEN = Token(TokenType.NUMBER, "0",-1,"")
CONSTANT_TOKEN = Token(TokenType.IDENTIFIER,"c:",-1,"")
LAST_RULE_TOKEN = Token(TokenType.LAST_RULE,"",-1,"")
SECOND_RULE_TOKEN = Token(TokenType.SECOND_RULE,"",-1,"")
DISABLE_SELF_COMMAND = CommandObject("disable-self",[],"","")
DO_NOTHING_COMMAND = CommandObject("do-nothing",[],"","")
def JUMP_LAST_COMMAND():
  return CommandObject("up-jump-direct",[CONSTANT_TOKEN,LAST_RULE_TOKEN ],"","")
def JUMP_SECOND_COMMAND():
  return CommandObject("up-jump-direct",[CONSTANT_TOKEN,SECOND_RULE_TOKEN ],"","")
def JUMP_1_COMMANDS():
  return CommandObject("up-jump-rule",[Token(TokenType.NUMBER,"1",-1,"")],"","")