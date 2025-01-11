
from pdb import line_prefix
from os import name
from enums import TokenType, Structure
import typing
import copy
import dataclasses
import commands as c
from colorama import Fore, Back, Style
from utils import *

class PrettyPrinter(object):
    def __repr__(self):
      lines = [Fore.GREEN + self.__class__.__name__ + Fore.WHITE + ':']
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

def newToken(oldToken):
  if isinstance(oldToken, Token):
    return Token(oldToken.tokenType, oldToken.value, oldToken.line, oldToken.file)
  else:
    tokenErrorCounter.add_error("canot create newToken out of"+str(oldToken)+" "+str(oldToken.__class__))
    #print(f"canot create newToken out of {oldToken} {oldToken.__class__}")
    return oldToken

class TokenErrorCounter():
  def __init__(self):
    self.errors = []
  def add_error(self, error):
    self.errors.append(error)
  def __repr__(self):
    return Fore.YELLOW + f'NewToken Errors: {len(self.errors)}' + Fore.WHITE
tokenErrorCounter = TokenErrorCounter()

class Token(PrettyPrinter):
  
  def __init__(self, tokenType:TokenType, value:str, line:int, file:str):
    self.tokenType:TokenType = tokenType
    self.value:str = value
    self.line:int = line
    self.file:str = file
    self.lineNum:int = 0
  def __repr__(self):
    
    return("["+str(self.print_value()) +" "+str(self.tokenType).split('.')[1]+' '+self.file+str(self.line)+"]")
  def scope(self, callStack):
    if self.tokenType == TokenType.IDENTIFIER:
      self.value = "/".join([o.funcCall.name for o in callStack])+"/"+ self.value
  def print_value(self):
    tempValues = {
      '\n':'/n',
      '"""':'3dQ',
      "'''":'3sQ',
    }
    if self.value in tempValues.keys():
      return tempValues[self.value]
    return self.value

class Wrapper(PrettyPrinter):
  def __init__(self, Type, lineList, func_name = None):
    self.Type = Type
    self.lineList = lineList
    self.func_name = func_name
  def interpret(self):
    newList = []
    for line in self.lineList:
      newList.append(line.interpret())
      #raise Exception("LINE"+str(line))
    return Wrapper(self.Type, newList, self.func_name)
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
  def true_condition(self):
    return (self.conditionList == TRUE_CONDITION)

class CommandObject(PrettyPrinter):
  def __init__(self, name, argList, line, file):
    self.line = line
    self.file = file
    self.name = newToken(name)
    self.argList = [newToken(arg) for arg in argList]
  def __repr__(self):
    return ("COMMAND name:"+str(self.name)+" args:"+str(self.argList))
  def scope(self, callStack):
    for line in self.argList:
      line.scope(callStack)
  def interpret(self):
    return defruleObject(TRUE_CONDITION, [self])

class ReturnObject(PrettyPrinter):
  def __init__(self, args, line, file):
    self.args = args
    self.assignVars = None
    self.line = line
    self.file = file
  def set_assignVars(self, assignVars):
    self.assignVars = assignVars
  def scope(self, callStack):
    for line in self.args:
      line.scope(callStack)
  def interpret(self):
    commands = []
    if self.assignVars:
      for i in range(len(self.args)):
        x = self.assignVars[i]
        y = [self.args[i]]
        if x and y:
          commands.append(VarAsignObject(self.assignVars[i], [self.args[i]], -1, '').interpret())
    return Wrapper(ReturnObject, commands)
        
  ##used for stack based functions
  #def interpret(self):
  #  commands = []
  #  for arg in self.args:
  #    argList = [RETURN_VAR_TOKEN()]
  #    if arg.tokenType == TokenType.NUMBER:
  #      argList.append(CONSTANT_TOKEN)
  #    else:
  #      argList.append(GOAL_TOKEN)
  #    argList.append(arg)
  #    commands.append(CommandObject("up-modify-goal", argList, -1,""))
  #  commands.append(JUMP_TO_RETURN_COMMAND())
  #  return Wrapper(ReturnObject, [defruleObject(TRUE_CONDITION, commands)])

class VarInit(PrettyPrinter):
  def __init__(self, name, args):
    if name == "Int":
      self.name = Structure.INT
    elif name == "Point":
      self.name = Structure.POINT
    elif name == "State":
      self.name = Structure.STATE
    elif name == "Const":
      self.name = Structure.CONST
    else:
      raise Exception(f'{name} is not a var init type')
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
      if self.expression[0].name == Structure.CONST:
        return defconstObject(self.variable, self.expression[0].args[0], self.line, self.file)
        return CommandObject("defconst", [self.variable,self.expression[0].args[0]], self.line, self.file)
        raise Exception("why are we here again??? no Const()")
      asignCommands.append(self.createAsignCommand(self.variable, "+", Token(TokenType.VAR_INIT, self.expression[0].name, -1,''))) #creates asign command so it is allocated, but +0 so it doesnt reset every loop
    elif isinstance(self.expression[0], FuncCallObject):
      raise Exception("actual function returns not implemented yet")
      #TODO: add return value stuff: but its the returns, not the asign that needs to return
      #asignCommands.append(self.createAsignCommand(self.variable, "=", ZERO_NUMBER_TOKEN)) # shouldnt be ZNT, self.expression[0].name this donest work, needs to get the deffunc return variable not the name
    else:
      asignCommands.append(self.createAsignCommand(self.variable, "=", self.expression[0]))
      if len(self.expression) == 3:
        asignCommands.append(self.createAsignCommand(self.variable, self.expression[1], self.expression[2]))
    return defruleObject(TRUE_CONDITION, asignCommands)
  
  def createAsignCommand(self, variable, op, tempVariable):
    args = []
    args.append(Token(variable.tokenType, variable.value, variable.line, variable.file))
    if tempVariable.tokenType == TokenType.NUMBER or tempVariable.tokenType == TokenType.VAR_INIT:
        if isinstance(op, Token): properOp = "c:"+ op.value
        else: properOp = "c:"+ op
    else:
        if isinstance(op, Token): properOp = "g:"+ op.value
        else: properOp = "g:"+ op
    args.append(Token(TokenType.MATHOP ,properOp, -1, ''))
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
    newList.append(defruleObject(TRUE_CONDITION, [JUMP_FIRST_COMMAND()]))
    newList.append(defruleObject( TRUE_CONDITION, [DO_NOTHING_COMMAND]))
    if isDisableSelf:
      newList[0].executeList.append(DISABLE_SELF_COMMAND)
    return Wrapper(WhileLoopObject, newList)

class ForLoopObject(ConditionalObject):
  def __init__(self, lineList, iterator, itrStart, itrEnd, itrJump):
    if isinstance(itrEnd, Token):
      #if itrEnd.tokenType != TokenType.NUMBER:
        #raise Exception("only Integers are supported in the range function currently. itrEnd")
      numberToken = itrEnd
    else:
      numberToken = Token(TokenType.NUMBER, itrEnd, -1, "")
    if itrEnd.tokenType == TokenType.NUMBER:
      conditionals = [CommandObject("up-compare-goal",[iterator, GREATER_THEN_OR_EQUAL_TOKEN, numberToken], -1,"")]
    else:
      conditionals = [CommandObject("up-compare-goal",[iterator, GREATER_THEN_OR_EQUAL_GOAL_TOKEN, numberToken], -1,"")]
    super().__init__(conditionals, lineList)
    self.iterator = iterator
    if isinstance(itrStart, Token):
      self.itrStart = itrStart
    else: 
      self.itrStart = Token(TokenType.NUMBER, itrStart, -1, "")
    if isinstance(itrJump, Token):
      self.itrJump = itrJump
    else:
      self.itrJump = Token(TokenType.NUMBER, itrJump, -1, "")
  def interpret(self):
    isDisableSelf = False
    newList = []
    if self.itrStart.tokenType == TokenType.NUMBER:
      newList.append(defruleObject(TRUE_CONDITION, [CommandObject("up-modify-goal",[self.iterator, CONSTANT_EQUAL_TOKEN, self.itrStart],-1,"")]))
    else:
      raise Exception("only Integers are supported in the range function currently. itrStart")
    newList.append(defruleObject(self.conditionList, [JUMP_LAST_COMMAND()]))
    for line in self.lineList:
      if isinstance(line, CommandObject) and (line.name == "disable-self"):
        raise Exception("disable-self command in a for loop is undefined behavior")#isDisableSelf = True
      else:
        newList.append(line.interpret())
    incroment_comamnd = CommandObject("up-modify-goal",[self.iterator, CONSTANT_ADD_TOKEN, self.itrJump],"","")
    newList.append(defruleObject(TRUE_CONDITION, [incroment_comamnd, JUMP_SECOND_COMMAND()]))        
    newList.append(defruleObject( TRUE_CONDITION, [DO_NOTHING_COMMAND]))
    return Wrapper(WhileLoopObject, newList)
  def scope(self, callStack):
    super().scope(callStack)
    self.iterator.scope(callStack)
  

class DefFuncObject(PrettyPrinter):
  def __init__(self, name, argList, lineList, returnType):
    self.name = name
    self.argList = argList
    self.lineList = lineList
    if not isReservedInitFunc(returnType):
      raise Exception(f'{returnType} is not a reserved init function')
    self.returnType = returnType
  def get_Return_type_varInit(self):
    return VarInit(self.returnType,[])
  def interpret(self):
    newList = []
    for line in self.lineList:
      if isinstance(line, CommandObject) and (line.name == "disable-self"):
        raise Exception("disable-self command in a deffuncobject is undefined behavior")#isDisableSelf = True
      else:
        newList.append(line.interpret())
    if not isinstance(self.lineList[-1], ReturnObject):
      newList.append(Wrapper(ReturnObject, [defruleObject( TRUE_CONDITION, [JUMP_TO_RETURN_COMMAND()])]))
    return Wrapper(DefFuncObject, newList)
  
#only exists to make wrapper to keep track of function arg assign commands
class ArgAssignObject(PrettyPrinter):
  pass

class FuncCallObject(PrettyPrinter):
  def __init__(self, name, args):
    self.name = name
    self.args = args
  def scope(self, callStack):
    for line in self.args:
      line.scope(callStack)

class CallStackItem(PrettyPrinter):
  def __init__(self, funcCall, defFuncArgs, assignVars = None):
    self.funcCall = funcCall
    self.defFuncArgs = defFuncArgs 
    self.assignVars = assignVars    

  def isSetToFunction(self):
    if isinstance(self.expression[0], FuncCallObject):
      return True
    else:
      return False



TRUE_CONDITION = [CommandObject("true",[],"","")]
NOT_TOKEN = Token(TokenType.LOGIC_OP,"not",-1,"")
ZERO_NUMBER_TOKEN = Token(TokenType.NUMBER, "0",-1,"")
ONE_NUMBER_TOKEN = Token(TokenType.NUMBER, "1",-1,"")
GREATER_THEN_OR_EQUAL_TOKEN = Token(TokenType.COMPAREOP, ">=",-1,"")
GREATER_THEN_OR_EQUAL_GOAL_TOKEN = Token(TokenType.COMPAREOP, "g:>=",-1,"")
GOAL_TOKEN = Token(TokenType.IDENTIFIER,"g:",-1,"")
CONSTANT_TOKEN = Token(TokenType.IDENTIFIER,"c:",-1,"")
CONSTANT_ADD_TOKEN = Token(TokenType.MATHOP, "c:+",-1,"")
CONSTANT_EQUAL_TOKEN = Token(TokenType.MATHOP, "c:=",-1,"")
DISABLE_SELF_COMMAND = CommandObject("disable-self",[],"","")
DO_NOTHING_COMMAND = CommandObject("do-nothing",[],"","")
def RETURN_VAR_TOKEN():
  return Token(TokenType.RETURN_VAR_TOKEN,"",-1,"")
def LAST_RULE_TOKEN():
  return Token(TokenType.LAST_RULE,"",-1,"")
def FIRST_RULE_TOKEN():
  return Token(TokenType.FIRST_RULE,"",-1,"")
def SECOND_RULE_TOKEN():
  return Token(TokenType.SECOND_RULE,"",-1,"")
def RETURN_POINT():
  return Token(TokenType.RETURN_POINT,"",-1,"")
def JUMP_TO_RETURN_COMMAND():
  return CommandObject("up-jump-direct",[GOAL_TOKEN,RETURN_POINT() ],"","")
def JUMP_FIRST_COMMAND():
  return CommandObject("up-jump-direct",[CONSTANT_TOKEN,FIRST_RULE_TOKEN() ],"","")
def JUMP_LAST_COMMAND():
  return CommandObject("up-jump-direct",[CONSTANT_TOKEN,LAST_RULE_TOKEN() ],"","")
def JUMP_SECOND_COMMAND():
  return CommandObject("up-jump-direct",[CONSTANT_TOKEN,SECOND_RULE_TOKEN() ],"","")
def JUMP_1_COMMANDS():
  return CommandObject("up-jump-rule",[Token(TokenType.NUMBER,"1",-1,"")],"","")