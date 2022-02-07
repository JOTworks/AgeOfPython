from termcolor import colored
from data import *

class Parcer: #REFACTOR spell it parser
  def __init__(self, tokens):
    self.tokens = tokens
    self.main = []
    self.tokPtr = 0
    self.tabSize = 4

  def consumeTokens(self):
    #print("consumed:"+str(self.tokens[:self.tokPtr]))
    self.tokens = self.tokens[self.tokPtr:]
    self.tokPtr = 0

    #print(self.tokens)
  
  def compareTokenTypes(self, tokens, throwable = False):
    #print("comparing: "+str(tokens)+" Ptr: "+str(self.tokPtr))
    tokPtrOffset = self.tokPtr
    for i in range(len(tokens)):
      if tokPtrOffset + i > len(self.tokens)-1: 
        return False
      #print("comparingS: "+str(self.tokens[tokPtrOffset + i].tokenType)+" Ptr: "+str(tokens[i]))
      if self.tokens[tokPtrOffset + i].tokenType != tokens[i]:
        if self.tokens[tokPtrOffset + i].tokenType == TokenType.TABS:
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
      openObject.append(defconstObject(self.tokens[2].value,self.tokens[3].value))
      self.consumeTokens() 
      return True
    return False

  def argumentState(self, openObject):
    if (self.compareTokenTypes([TokenType.OPERATOR]) or
        self.compareTokenTypes([TokenType.IDENTIFIER]) or 
        self.compareTokenTypes([TokenType.NUMBER]) or 
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

  def commandState(self, openObject):
    if self.compareTokenTypes([TokenType.LEFT_PAREN, TokenType.IDENTIFIER]):
      commandName = self.tokens[self.tokPtr - 1].value
      argList = []
      if self.argumentphraseState(argList):
        if self.compareTokenTypes([TokenType.RIGHT_PAREN]):
          openObject.append(CommandObject(commandName, argList))
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
      while(self.logiccommandState(openObject) or self.commandState(openObject)): pass
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
              openObject.append(defruleObject(LineListObject(conditionalCammandList), LineListObject(executeCammandList)))
              self.consumeTokens()
              return True
    return False

  def loadState(self, openObject): #need to refactor LOAD_IF into ones w/wo identifier
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
    if self.compareTokenTypes([TokenType.IF]):
      conditionals = []
      lines = []
      if self.commandphraseState(conditionals):
        if self.compareTokenTypes([TokenType.COLON]):
          if self.lineState(lines, tabValue + self.tabSize):
            openObject.append(IfObject(conditionals,lines))
            self.consumeTokens()
            return True
    return False

  def whileState(self, openObject,tabValue):
    if self.compareTokenTypes([TokenType.WHILE]):
      conditionals = []
      lines = []
      if self.commandphraseState(conditionals):
        if self.compareTokenTypes([TokenType.COLON]):
          if self.lineState(lines, tabValue + self.tabSize):
            openObject.append(WhileLoopObject(conditionals,lines))
            self.consumeTokens()
            return True
    return False

  def forState(self, openObject,tabValue):
    if self.compareTokenTypes([TokenType.FOR, TokenType.IDENTIFIER, TokenType.IN, TokenType.RANGE, TokenType.LEFT_PAREN]):
      iterator = self.tokens[self.tokPtr-4].value
      args = []
      if self.pyargumentphraseState(args):
        if self.compareTokenTypes([TokenType.RIGHT_PAREN, TokenType.COLON]):
          lines = []
          if self.lineState(lines, tabValue + self.tabSize):
            if len(args) == 1:
              openObject.append(ForLoopObject(lines, iterator, 0, args[0], 1))
            elif len(args) == 2:
              openObject.append(ForLoopObject(lines, iterator, args[0], args[1], 1))
            elif len(args) == 3:
              openObject.append(ForLoopObject(lines, iterator, args[0], args[1], args[2]))
            else:
              return False #throw error, for loop not right number of inputs
            self.consumeTokens()
            return True
    return False

  def varasignState(self, openObject, tabValue):
      if self.compareTokenTypes([TokenType.IDENTIFIER, TokenType.EQUALS]):
        variable = self.tokens[self.tokPtr-2].value
        expression = []
        if self.funccallState( expression, tabValue):
          print("FUNC CALL FOUND IN VAR ASIGN")
          openObject.append(VarAsignObject(variable, expression))
          self.consumeTokens()
          return True
        elif self.expargumentphraseState(expression):
          openObject.append(VarAsignObject(variable, expression))
          self.consumeTokens()
          return True
      return False

  def deffuncState(self, openObject):
    if self.compareTokenTypes([TokenType.DEF, TokenType.IDENTIFIER, TokenType.LEFT_PAREN]):
      name = self.tokens[self.tokPtr-2].value #potential error, might need a tokPtr
      arguments = []
      lines = []
      if self.pyargumentphraseState(arguments):
        if self.compareTokenTypes([TokenType.RIGHT_PAREN, TokenType.COLON]):
          if self.lineState(lines, self.tabSize):
            openObject.append(DefFuncObject(name, arguments, lines)) #ERROR needs the line items in the def
            self.consumeTokens()
            return True
    return False

  def funccallState(self, openObject, tabValue):
    if self.compareTokenTypes([TokenType.IDENTIFIER, TokenType.LEFT_PAREN]):
      name = self.tokens[self.tokPtr-2].value
      args = []
      if self.pyargumentphraseState(args):
        if self.compareTokenTypes([TokenType.RIGHT_PAREN]):
          #print("IS FUNC CALL")
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
        if len(self.tokens[self.tokPtr].value) > tabValue:
          print("TAB GRATER FAIL STATE")
          return False
        if len(self.tokens[self.tokPtr].value) < tabValue:
          print("TAB LESS:"+ str(len(self.tokens[self.tokPtr].value))+" < "+ str(tabValue))
          return True
      else: #should only run if line by itself
        if self.compareTokenTypes([TokenType.TABS]):
          print("TAB FOUND WHEN TABS=0 FAIL STATE")
          return False
      if self.ifState( openObject, tabValue):  anotherLine = True
      elif self.whileState( openObject, tabValue):  anotherLine = True
      elif self.forState( openObject, tabValue):  anotherLine = True
      elif self.funccallState( openObject, tabValue):  anotherLine = True
      elif self.varasignState( openObject, tabValue):  anotherLine = True
      elif self.commandState(openObject):  anotherLine = True
      self.consumeTokens()  
        
    return True

  def mainState(self, openObject):
    if self.loadState(openObject): return
    if self.defconstState(openObject): return
    if self.defruleState(openObject): return
    if self.deffuncState(openObject): return
    
    curLen = len(self.main)
    if self.lineState(openObject, 0): 
      if curLen != len(self.main):
        return

    raise Exception(str("Parce failed at "+str(self.tokens[self.tokPtr])))
    self.tokens = self.tokens[1:]
    self.tokPtr = 0

  def parce(self):
      while(len(self.tokens)>0):
        self.mainState(self.main)