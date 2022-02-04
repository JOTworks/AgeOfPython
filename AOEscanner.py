from data import TokenType, Token

class Scanner:
  def __init__(self, input):
    self.input = input
    self.lineIndent = [] #position is line number, value is number of spaces
    self.tokens = []
  
  def stripTokens(self, tokenType):
    strippedTokens = []
    for token in self.tokens:
      if token.tokenType != tokenType:
        strippedTokens.append(token)
    self.tokens = strippedTokens
    return strippedTokens

  def popToken(self,line,length,type):
    newToken = Token(type,self.input[:length],line)
    self.tokens.append(newToken)
    self.input = self.input[length:]

  def basicState(self):
    if self.input[:2] == '=>':
      self.popToken(self.lineNum,2,TokenType.ARROW)
      return True
    elif self.input[:2] in {'<=', '>=', '!=', '=='}:
      self.popToken(self.lineNum,2,TokenType.OPERATOR)
      return True
    elif self.input[:1] == ')':
      self.popToken(self.lineNum,1,TokenType.RIGHT_PAREN)
      return True
    elif self.input[:1] == '(':
      self.popToken(self.lineNum,1,TokenType.LEFT_PAREN)
      return True
    elif self.input[:1] == ':':
      self.popToken(self.lineNum,1,TokenType.COLON)
      return True
    elif self.input[:1] == ',':
      self.popToken(self.lineNum,1,TokenType.COMMA)
      return True
    elif self.input[:1] == '=':
      self.popToken(self.lineNum,1,TokenType.EQUALS)
      return True
    elif self.input[:1] in {'<', '>', '='}:
      self.popToken(self.lineNum,1,TokenType.OPERATOR)
      return True
    elif self.input[:1] in {'/', '*', '-', '+'}:
      self.popToken(self.lineNum,1,TokenType.MATHOP)
      return True
    return False

  def commentState(self):
    if self.input[:1] in {';' , '#'}:
      self.popToken(self.lineNum,len(self.input),TokenType.COMMENT)
      return True
    return False

  def loadState(self):
    if self.input[:1] == '#':
      number =  1
      if self.input[:7] == '#end-if':
        number =  7
      elif self.input[:16] == '#load-if-defined':
        number =  16
      elif self.input[:20] == '#load-if-not-defined':
        number =  20
      elif self.input[:5] == '#else':
        number =  5
      else:
        return False
      self.popToken(self.lineNum,number,TokenType.LOAD_IF)
      return True
    return False

  def whiteSpaceState(self):
    length = 0
    while(self.input[:length+1].isspace()):
        length = length + 1
        if(length == len(self.input)):
          self.popToken(self.lineNum,length,TokenType.WHITE_SPACE)
          return True
    if length == 0:
      return False
    if length > len(self.input):
      print("error")
    self.popToken(self.lineNum,length,TokenType.WHITE_SPACE)
    return True

  def tabState(self):
    length = 0
    while(self.input[:length+1].isspace()):
        length = length + 1
        if(length == len(self.input)):
          self.popToken(self.lineNum,length,TokenType.TABS)
          return True
    if length == 0:
      return False
    if length > len(self.input):
      print("error")
    self.popToken(self.lineNum,length,TokenType.TABS)
    return True

  def identifierSymbol(self, symbol):
    if symbol == '\n':
      return False
    if symbol.isalnum():
      return True
    if symbol in {'-', '_', ':', '+', '*', '/'}: #Refactor for expressions to work without spaces. needed now for c:+ case
      return True
    return False

  def stringState(self):
    if self.input[:1] == '"':
      length = 1
      while(self.input[length] != '"'):
        length = length + 1
        if length == len(self.input):
          self.popToken(self.lineNum,length-1,TokenType.UNIDENTIFIED)
          return True
      length = length + 1
      self.popToken(self.lineNum,length,TokenType.STRING)
      return True
    return False

  def identifierState(self):
    length = 0
    if self.input[length].isalpha():
      length += 1 
    while(self.identifierSymbol(self.input[length])):
      length += 1 
        #print("input: "+self.input)
        #print("inputlen: "+str(len(self.input)))
        #print("length: "+ str(length))
    if length == 0:
      return False
    if length > len(self.input):
      print("error")
    identifierType = TokenType.IDENTIFIER
    if self.input[:length] == "if":
      identifierType = TokenType.IF
    elif self.input[:length] == "while":
      identifierType = TokenType.WHILE
    elif self.input[:length] == "for":
      identifierType = TokenType.FOR
    elif self.input[:length] == "in":
      identifierType = TokenType.IN
    elif self.input[:length] == "range":
      identifierType = TokenType.RANGE
    elif self.input[:length] == "else":
      identifierType = TokenType.ELSE
    elif self.input[:length] == "elif":
      identifierType = TokenType.ELIF
    elif self.input[:length] == "for":
      identifierType = TokenType.FOR
    elif self.input[:length] == "while":
      identifierType = TokenType.WHILE
    elif self.input[:length] == "def":
      identifierType = TokenType.DEF
    elif self.input[:length] == "defconst":
      identifierType = TokenType.DEFCONST
    elif self.input[:length] == "defrule":
      identifierType = TokenType.DEFRULE
    elif self.input[:length] == "return":
      identifierType = TokenType.RETURN
    elif self.input[:length] in {'or','and','not','nor','xor','nand', 'xnor'}:
      identifierType = TokenType.LOGIC_OP


    self.popToken(self.lineNum,length,identifierType)
    return True

  def numberState(self):
    length = 0
    while(self.input[:length+1].isnumeric()):
        length = length + 1
    if length == 0:
      return False
    if length > len(self.input):
      print("error")
    if self.input[length].isalpha():
      self.popToken(self.lineNum,length,TokenType.UNIDENTIFIED)
      return True
    self.popToken(self.lineNum,length,TokenType.NUMBER)
    return True

  def mainState(self):
    if self.whiteSpaceState(): return
    elif self.basicState(): return
    elif self.loadState(): return
    elif self.commentState(): return
    elif self.numberState(): return   
    elif self.identifierState(): return
    elif self.stringState(): return
    self.popToken(self.lineNum,1,TokenType.UNCAUGHT)

  def scan(self, line, lineNum):
    self.input = line
    self.lineNum = lineNum
    if line.isspace(): #strips empty lines
      return
    if self.tabState():
      if self.loadState() or self.commentState():
        if self.tokens[len(self.tokens)-2].tokenType == TokenType.TABS:
          del self.tokens[len(self.tokens)-2]
        else: print("ERROR in SCAN, tried to delete tabs but was different tokenType")
    while(len(self.input)>0):
      self.mainState()
      #print(self.input)
    #print(self.input)
