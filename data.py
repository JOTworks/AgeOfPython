import enum
class TokenType(enum.Enum):
    LEFT_PAREN = 1      #length: 1
    RIGHT_PAREN = 2     #length: 1
    LOGIC_OP = 3
    COMMA = 4
    COLON = 5           #length: 1
    ARROW = 6           #length: 2
    OPERATOR = 7
    POINTER = 8
    NUMBER = 9
    # Variable length tokens:
    STRING = 10
    COMMENT = 11
    IDENTIFIER = 12
    WHITE_SPACE = 13
    # Keywords:
    DEFCONST = 14
    DEFRULE = 15
    IF = 16
    ELSE = 17
    ELIF = 18
    FOR = 18
    WHILE = 20
    DEF = 21
    # Comment keywords:
    LOAD_IF = 22
    UNIDENTIFIED = 24
    UNCAUGHT = 25
    TABS = 26
    IN = 27
    RANGE = 28
    EQUALS = 29
    MATHOP = 30
    RETURN = 31
    LOAD = 32
    LOAD_RANDOM = 33

from os import name
# Data Classes


class PrettyPrinter(object):
    def __repr__(self):
        if self.__class__.__name__ == "LineListObject":
          lines  = []
          for val in self.lineList:
            lines += '{}'.format(val).split('\n')
          return ('\n    '+ '\n    '.join(lines) )

        else:    
          lines = [self.__class__.__name__ + ':']
          for key, val in vars(self).items():
              lines += '{}: {}'.format(key, val).split('\n')
          return ( '\n|    '.join(lines) )

class Token(PrettyPrinter):
  def __init__(self, tokenType, value, line):
    self.tokenType = tokenType
    self.value = value
    self.line = line
    self.lineNum = 0
  def __repr__(self):
    tempValue = self.value
    if self.value == '\n':
      tempValue = '/n'
    #return("("+str(self.tokenType)+" "+ tempValue +" "+ str(self.line)+")")
    return("( "+ tempValue +" "+ str(self.line)+" )")

  def print(self,setting = ""):
    tempValue = self.value
    #if self.value == '\n':
    #  tempValue = '/n'
    if self.tokenType == TokenType.UNCAUGHT:
      if setting == "full errors":
        print(str(self.tokenType)+"\t ["+ tempValue +"] "+ str(self.line)) 
      print(colored("["+ tempValue +"]","blue"), end =" ")
    elif self.tokenType == TokenType.UNIDENTIFIED:
      if setting == "full errors":
        print(str(self.tokenType)+"\t ["+ tempValue +"] "+ str(self.line))
      print(colored("["+ tempValue +"]","red"), end =" ")
    elif setting != "errors" and setting != "full errors":
      print("["+ tempValue +"]", end =" ")


class LoadIfObject():
  def __init__(self, name, arg = ""):
    self.name = name
    self.arg = arg
  def __repr__(self):
    return ("LOADIF name:"+str(self.name)+" args:"+str(self.arg))

class ContainesLineList(PrettyPrinter):
  pass

class LineListObject(PrettyPrinter):
  def __init__(self, lineList):
    self.lineList = lineList

class logicCommandObject(PrettyPrinter):
  def __init__(self, logicOp, commands):
    self.logicOp = logicOp
    self.commands = commands

class defconstObject(PrettyPrinter):
  def __init__(self, name, value):
    self.name = name
    self.value = value

class defruleObject(PrettyPrinter):
  def __init__(self, conditionList, executeList):
    self.conditionList = conditionList
    self.executeList = executeList

class CommandObject(PrettyPrinter):
  def __init__(self, name, argList):
    self.name = name
    self.argList = argList
  def __repr__(self):
    return ("COMMAND name:"+str(self.name)+" args:"+str(self.argList))

class IfObject(ContainesLineList):
  def __init__(self, conditionList, lineList):
    self.conditionList = LineListObject(conditionList)
    self.lineList = LineListObject(lineList)

class WhileLoopObject(ContainesLineList):
  def __init__(self, conditionals, lineList):
    self.conditionals = conditionals
    self.lineList = LineListObject(lineList)

class ForLoopObject(ContainesLineList):
  def __init__(self, lineList, interator, itrStartValue, itrEndValue, itrJumpValue):
    self.interator = interator
    self.itrStartValue = itrStartValue
    self.itrEndValue = itrEndValue
    self.itrJumpValue = itrJumpValue
    self.lineList = LineListObject(lineList)

class DefFuncObject(ContainesLineList):
  def __init__(self, functionName, argList, lineList):
    self.functionName = functionName
    self.argList = argList
    self.lineList = LineListObject(lineList)
  #def __repr__(self):
  #  return("FUNCDEF name: "+self.functionName+" arg:"+str(self.argList)+" lines:"+ str(self.lineList))

class VarAsignObject(PrettyPrinter):
  def __init__(self, variable, expression):
    self.variable = variable
    self.expression = expression

class FuncCallObject(PrettyPrinter):
  def __init__(self, name, args):
    self.name = name
    self.args = args