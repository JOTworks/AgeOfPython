from termcolor import colored
from Scanner import Scanner
import random
from data import *
from enums import TokenType, Structure
from commands import JUMP_COMMANDS
from utils import *

class Parcer: #TODO spell it parser
  def __init__(self, tokens, aiFolder):
    self.tokens = tokens
    self.main = []
    self.tokPtr = 0
    self.tabSize = 2
    self.loadLimit = 1000
    self.loadCount = 0
    self.aiFolder = aiFolder

  def consumeTokens(self):
    self.tokens = self.tokens[self.tokPtr:]
    self.tokPtr = 0
  
  def compareTokenTypes(self, tokens, throwable = False):
    #print("comparing: "+str(tokens)+" Ptr: "+str(self.tokPtr))
    tokPtrOffset = self.tokPtr
    for i in range(len(tokens)):
      if tokPtrOffset + i > len(self.tokens)-1: 
        return False
      #print("comparingS: "+str(self.tokens[tokPtrOffset + i].tokenType)+" Ptr: "+str(tokens[i]))
      if self.tokens[tokPtrOffset + i].tokenType != tokens[i]:
        if self.tokens[tokPtrOffset + i].tokenType == TokenType.TABS:
          #return False
          #print("token=TABS")
          if tokPtrOffset + i > len(self.tokens)-1: 
            return False
          #print("comparingA: "+str(self.tokens[tokPtrOffset + i +1].tokenType)+" Ptr: "+str(tokens[i]))
          if self.tokens[tokPtrOffset + i +1].tokenType != tokens[i]:
            #print("CompareAfterTabFalse")
            if(throwable):
              raise Exception("compareTokenTypes Failed")
            return False #self.tokens[i] #this is where i would have info to throw error?
          tokPtrOffset += 1 #if token was tabs but next one is corect, need to incorment to consume tabs
        else:
          #print("CompareFalse")
          return False
    #print("CompareTRUE")
    self.tokPtr = tokPtrOffset
    self.tokPtr += len(tokens)
    return True
      
  def defconstState(self, openObject):
    if self.compareTokenTypes([TokenType.LEFT_PAREN, 
                               TokenType.DEFCONST, 
                               TokenType.IDENTIFIER, 
                               TokenType.NUMBER, 
                               TokenType.RIGHT_PAREN]):
      openObject.append( defconstObject(self.tokens[2].value,self.tokens[3].value,self.tokens[2].line,self.tokens[2].file) )
      self.consumeTokens() 
      return True
    return False

  def argumentState(self, openObject):
    if (self.compareTokenTypes([TokenType.EQUALS]) or
        self.compareTokenTypes([TokenType.COMPAREOP]) or
        self.compareTokenTypes([TokenType.IDENTIFIER]) or 
        self.compareTokenTypes([TokenType.NUMBER]) or 
        self.compareTokenTypes([TokenType.STRATEGIC_NUMBER]) or
        self.compareTokenTypes([TokenType.TYPEOP]) or
        self.compareTokenTypes([TokenType.MATHOP]) or
        self.compareTokenTypes([TokenType.STRING])):
      openObject.append(self.tokens[self.tokPtr-1])
      return True
    return False

  def mathopState(self, openObject):
    if self.compareTokenTypes([TokenType.MATHOP]):
      openObject.append(self.tokens[self.tokPtr-1])
      return True
    return False

  def argumentphraseState(self, openObject):
    while(self.argumentState(openObject)): pass
    return True

  def pyargumentphraseState(self, openObject):
    if self.argumentState(openObject):
      while(self.compareTokenTypes([TokenType.COMMA])):
        if not self.argumentState(openObject):
          return False
    return True

  def expargumentphraseState(self, openObject):
    if self.argumentState(openObject):
      while self.mathopState(openObject):
        if not self.argumentState(openObject):
          return False
    return True

  def returnState(self, openObject):
    if self.compareTokenTypes([TokenType.RETURN]):
      print("found return")
      returns = []
      if self.compareTokenTypes([TokenType.NUMBER]) or self.compareTokenTypes([TokenType.IDENTIFIER]):
        print("found first N/I")
        returns.append(self.tokens[self.tokPtr - 1])
      while self.compareTokenTypes([TokenType.COMMA, TokenType.NUMBER]) or self.compareTokenTypes([TokenType.COMMA, TokenType.IDENTIFIER]):
        print("found another N/I")
        returns.append(self.tokens[self.tokPtr - 1])
      last_token = self.tokens[self.tokPtr - 1]  
      openObject.append(ReturnObject(returns, last_token.line, last_token.file))
      return True

  def commandState(self, openObject):
    if self.compareTokenTypes([TokenType.LEFT_PAREN, TokenType.IDENTIFIER]):
      commandName = self.tokens[self.tokPtr - 1].value
      commandLine = self.tokens[self.tokPtr - 1].line
      commandFile = self.tokens[self.tokPtr - 1].file
      argList = []
      if self.argumentphraseState(argList):
        if self.compareTokenTypes([TokenType.RIGHT_PAREN]):
          openObject.append(CommandObject(commandName, argList, commandLine, commandFile))
          if commandName in JUMP_COMMANDS:
            raise Exception("Jump Cammands will break code please remove all Jump commands")
          return True
    return False

  def logiccommandState(self, openObject):
    if self.tokPtr >= len(self.tokens)-1: #issue for end of file with next if statment
      return False
    if self.compareTokenTypes([TokenType.LEFT_PAREN, TokenType.LOGIC_OP]):
        logicOp = self.tokens[self.tokPtr-1]
        commands = []
        if self.tokens[self.tokPtr-1].value != "not":
          if not (self.logiccommandState(commands) or self.commandState(commands)):
            return False
        if self.logiccommandState(commands) or self.commandState(commands):
          if self.compareTokenTypes([TokenType.RIGHT_PAREN]):
              openObject.append(logicCommandObject(logicOp, commands))
              return True
    return False

  def commandphraseState(self, openObject):
    if self.logiccommandState(openObject) or self.commandState(openObject):
      self.compareTokenTypes([TokenType.END_LINE])
      while(self.logiccommandState(openObject) or self.commandState(openObject)):
        self.compareTokenTypes([TokenType.END_LINE])
      return True
    
    return False

  def defruleState(self, openObject):
    if self.compareTokenTypes([TokenType.LEFT_PAREN, TokenType.DEFRULE]):
      conditionalCammandList = []
      if self.commandphraseState(conditionalCammandList):
        if self.compareTokenTypes([TokenType.ARROW]):
          executeCammandList = []
          if self.commandphraseState(executeCammandList):
            if self.compareTokenTypes([TokenType.RIGHT_PAREN]):
              openObject.append(defruleObject(conditionalCammandList, executeCammandList))
              self.consumeTokens()
              return True
    return False

  def loadIfState(self, openObject): #TODO: need to refactor LOAD_IF into ones w/wo identifier
    if self.compareTokenTypes([TokenType.LOAD_IF, TokenType.IDENTIFIER]):
      openObject.append( LoadIfObject(self.tokens[0].value ,self.tokens[1].value) )
      self.consumeTokens()
      return True
    if self.compareTokenTypes([TokenType.LOAD_IF]):
      openObject.append(self.tokens[0])
      self.consumeTokens()
      return True
    return False

  def ifState(self, openObject, tabValue):
    exist = False #todo: test code without this line
    if self.compareTokenTypes([TokenType.IF]):
      conditionals = []
      lines = []
      if self.commandphraseState(conditionals):
        if self.compareTokenTypes([TokenType.COLON]):
          self.compareTokenTypes([TokenType.END_LINE])
          if self.lineState(lines, tabValue + self.tabSize):
            openObject.append(IfObject(conditionals,lines))
            self.consumeTokens()
            return True
          else: raise Exception("expected lineState got TOK:"+str(self.tokens[self.tokPtr])) 
        else: raise Exception("expected : got TOK:"+str(self.tokens[self.tokPtr]))  
      else: raise Exception("expected commandPhrase got TOK:"+str(self.tokens[self.tokPtr]))      
    return False

  def elseState(self, openObject, tabValue):
      if self.compareTokenTypes([TokenType.ELSE]):
        conditionals = []
        lines = []
        self.commandphraseState(conditionals)
        if self.compareTokenTypes([TokenType.COLON]):
          self.compareTokenTypes([TokenType.END_LINE])
          if self.lineState(lines, tabValue + self.tabSize):
            openObject.append(ElseObject(conditionals,lines))
            self.consumeTokens()   
            return True
          else: raise Exception("expected lineState got TOK:"+str(self.tokens[self.tokPtr])) 
        else: raise Exception("expected : got TOK:"+str(self.tokens[self.tokPtr]))    
      return False

  def whileState(self, openObject,tabValue):
    if self.compareTokenTypes([TokenType.WHILE]):
      conditionals = []
      lines = []
      if self.commandphraseState(conditionals):
        if self.compareTokenTypes([TokenType.COLON]):
          self.compareTokenTypes([TokenType.END_LINE])
          if self.lineState(lines, tabValue + self.tabSize):
            openObject.append(WhileLoopObject(conditionals,lines))
            self.consumeTokens()
            return True
          else: Exception("expected lineState got TOK:"+str(self.tokens[self.tokPtr])) 
        else: Exception("expected : got TOK:"+str(self.tokens[self.tokPtr]))    
      else: Exception("expected commandPhrase got TOK:"+str(self.tokens[self.tokPtr]))    
    return False

  def forState(self, openObject,tabValue):
    if self.compareTokenTypes([TokenType.FOR, TokenType.IDENTIFIER, TokenType.IN, TokenType.RANGE, TokenType.LEFT_PAREN]):
      iterator = self.tokens[self.tokPtr-4]
      args = []
      if self.pyargumentphraseState(args):
        if self.compareTokenTypes([TokenType.RIGHT_PAREN, TokenType.COLON]):
          self.compareTokenTypes([TokenType.END_LINE])
          lines = []
          if self.lineState(lines, tabValue + self.tabSize):
            if len(args) == 1:
              openObject.append(ForLoopObject(lines, iterator, "0", args[0], "1"))
            elif len(args) == 2:
              openObject.append(ForLoopObject(lines, iterator, args[0], args[1], "1"))
            elif len(args) == 3:
              openObject.append(ForLoopObject(lines, iterator, args[0], args[1], args[2]))
            else:
              Exception("wrong number of imputs in for loop range function") 
            self.consumeTokens()
            return True
          else: Exception("expected lineState got TOK:"+str(self.tokens[self.tokPtr])) 
        else: Exception("expected ): got TOK:"+str(self.tokens[self.tokPtr])) 
      else: Exception("expected pyargumentphrase got TOK:"+str(self.tokens[self.tokPtr])) 
    return False

  def varasignState(self, openObject, tabValue):
      if self.compareTokenTypes([TokenType.IDENTIFIER, TokenType.EQUALS]):
        variable = self.tokens[self.tokPtr-2]
        line = self.tokens[self.tokPtr-2].line
        file = self.tokens[self.tokPtr-2].file
        expression = []
        if self.funccallState( expression, tabValue):
          openObject.append(VarAsignObject(variable, expression, line, file ))
          self.consumeTokens()
          return True
        elif self.expargumentphraseState(expression):
          openObject.append(VarAsignObject(variable, expression, line, file))
          self.consumeTokens()
          return True
      return False

  def deffuncState(self, openObject):
    if self.compareTokenTypes([TokenType.DEF, TokenType.IDENTIFIER, TokenType.LEFT_PAREN]):
      name = self.tokens[self.tokPtr-2].value #potential error, might need a tokPtr
      arguments = []
      lines = []
      if self.pyargumentphraseState(arguments):
        if self.compareTokenTypes([TokenType.RIGHT_PAREN]):
          if self.compareTokenTypes([TokenType.ARROW_SMALL, TokenType.IDENTIFIER]):
            return_type = self.tokens[self.tokPtr-1].value
            raise Exception("need to use Structure enum instead of settint return_type to a string")
          else:
            return_type = Structure.INT
          if self.compareTokenTypes([TokenType.COLON]):
            self.compareTokenTypes([TokenType.END_LINE])
            if self.lineState(lines, self.tabSize):
              openObject.append(DefFuncObject(name, arguments, lines, return_type)) #ERROR needs the line items in the def
              self.consumeTokens()
    
            return True
    return False
  


  def funccallState(self, openObject, tabValue):
    if self.compareTokenTypes([TokenType.IDENTIFIER, TokenType.LEFT_PAREN]):
      name = self.tokens[self.tokPtr-2].value
      args = []
      if self.pyargumentphraseState(args):
        if self.compareTokenTypes([TokenType.RIGHT_PAREN]):
          if isReservedInitFunc_str(name):
            openObject.append(VarInit(name, args))
          else:
            openObject.append(FuncCallObject(name, args))
          self.consumeTokens()
          return True
    return False

  def lineState(self, openObject, tabValue):
    #print(self.tokens[self.tokPtr])
    #print("tabValue: "+str(tabValue))
    anotherLine = True
    while(anotherLine):
      anotherLine = False
      if self.tokPtr > len(self.tokens)-1:
        return True
      if tabValue > 0: 
        if self.tokens[self.tokPtr].tokenType != TokenType.TABS:
          return True
        elif len(self.tokens[self.tokPtr].value) > tabValue:
          return False
        elif len(self.tokens[self.tokPtr].value) < tabValue:
          print("TAB:"+ str(len(self.tokens[self.tokPtr].value))+" TABValue:"+ str(tabValue)+" line:"+str(self.tokens[self.tokPtr].line)+str(self.tokens[self.tokPtr].file))
          return True
      else: #should only run if line by itself
        if self.compareTokenTypes([TokenType.TABS]):
          raise Exception("TAB FOUND WHEN TABS=0 FAIL STATE "+str(self.tokens[self.tokPtr]))
          return False
      if self.ifState( openObject, tabValue): 
        self.elseState( openObject, tabValue)
        anotherLine = True
      elif self.whileState( openObject, tabValue):  anotherLine = True
      elif self.forState( openObject, tabValue):  anotherLine = True
      elif self.funccallState( openObject, tabValue):  anotherLine = True
      elif self.varasignState( openObject, tabValue):  anotherLine = True
      elif self.commandState(openObject):  anotherLine = True
      elif self.returnState(openObject): anotherLine = True
      self.compareTokenTypes([TokenType.END_LINE])
      self.consumeTokens()  
    return True

  def loadRandomPhrase(self, openObject):
    fileNameList = []
    while self.compareTokenTypes([TokenType.NUMBER, TokenType.STRING]):
      for i in range(int(self.tokens[self.tokPtr-2].value)):
        fileNameList.append(self.tokens[self.tokPtr-1].value)
    if self.compareTokenTypes([TokenType.STRING]):
      for i in range(100):
        fileNameList.append(self.tokens[self.tokPtr-1].value)
    else: 
      for i in range(100):
        fileNameList.append("")
    self.consumeTokens()
    return fileNameList[random.randint(0, 99)]
    

  def loadState(self, openObject): #TODO: this is just a weird fucntion.
    fileName = ""
    if self.compareTokenTypes([TokenType.LEFT_PAREN, TokenType.LOAD, TokenType.STRING, TokenType.RIGHT_PAREN]):
      self.loadCount += 1
      if self.loadCount > self.loadLimit:
        raise Exception("Loaded over "+str(self.loadLimit)+" times. You probably have a load circle.")
      fileName = self.tokens[self.tokPtr-2].value
      newScanner = Scanner(fileName, self.aiFolder) 
      newScanner.scan()
      self.consumeTokens() 
      self.tokens = newScanner.tokens + self.tokens
      return True

    elif self.compareTokenTypes([TokenType.LEFT_PAREN, TokenType.LOAD_RANDOM]):  
      self.loadCount += 1
      if self.loadCount > self.loadLimit:
        raise Exception("Loaded over "+str(self.loadLimit)+" times. You probably have a load circle.")
      fileName = self.loadRandomPhrase(openObject)
      if not self.compareTokenTypes([TokenType.RIGHT_PAREN]):
        raise Exception("expected RIGHT_PERAN at the end of Load-random Statment")
      if fileName != "":
        newScanner = Scanner(fileName) 
        newScanner.scan()
        self.consumeTokens() 
        self.tokens = newScanner.tokens + self.tokens
      else:
        self.consumeTokens() 
      return True
    return False

  def mainState(self, openObject):
    if self.loadState(openObject): return
    if self.loadIfState(openObject): return
    if self.defconstState(openObject): return
    if self.defruleState(openObject): return
    if self.deffuncState(openObject): return
    
    curLen = len(self.main)
    if self.lineState(openObject, 0): 
      if curLen != len(self.main):
        return

    raise Exception(str( "Parce failed at "+str(self.tokens[self.tokPtr])))
    self.tokens = self.tokens[1:]
    self.tokPtr = 0

  def parce(self):
      while(len(self.tokens)>0):
        self.mainState(self.main)