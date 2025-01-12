from data import Token
from enums import TokenType
from pprint import pprint
import pickle
class Scanner: #TODO: add extra line at end of file for mid token parces to fail instead of OOI crash
  def __init__(self, fileName, aiFolder):
    self.aiFolder = aiFolder
    self.fileName = fileName
    self.line = ""
    self.lineIndent = [] #position is line number, value is number of spaces
    self.tokens = []
    self.in_block:str = ''
  
  def stripTokens(self, tokenType: TokenType) -> list:
    """
    Removes all tokens of 1 type from the tokens list.
    tokenType: token to be removed from tokens list
    """
    strippedTokens = []
    for token in self.tokens:
      if token.tokenType != tokenType:
        strippedTokens.append(token)
    self.tokens = strippedTokens
    return strippedTokens

  def popToken(self,line:str,length:int,type:TokenType):
    """
    removes characters and cretes it into token
    line: line of code (is edited)
    Length: number of characters to remove from line and make into token
    type: type of token to be created
    """
    newToken = Token(type,self.line[:length],line,self.fileName)
    self.tokens.append(newToken)
    self.line = self.line[length:]

  def basicState(self):
    if self.line[:2] == '=>':
      self.popToken(self.lineNum,2,TokenType.ARROW)
      return True
    elif self.line[:2] == '->':
      self.popToken(self.lineNum,2,TokenType.ARROW_SMALL)
      return True
    elif self.line[:2] in {'<=', '>=', '!=', '=='}:
      self.popToken(self.lineNum,2,TokenType.COMPAREOP)
      return True
    elif self.line[:1] == ')':
      self.popToken(self.lineNum,1,TokenType.RIGHT_PAREN)
      return True
    elif self.line[:1] == '(':
      self.popToken(self.lineNum,1,TokenType.LEFT_PAREN)
      return True
    elif self.line[:1] == ':':
      self.popToken(self.lineNum,1,TokenType.COLON)
      return True
    elif self.line[:1] == ',':
      self.popToken(self.lineNum,1,TokenType.COMMA)
      return True
    elif self.line[:1] == '=':
      self.popToken(self.lineNum,1,TokenType.EQUALS)
      return True
    elif self.line[:1] in {'<', '>'}:
      self.popToken(self.lineNum,1,TokenType.COMPAREOP)
      return True
    elif self.line[:2] == '+=':
      self.popToken(self.lineNum,2,TokenType.INCREMENTER)
      return True
    elif self.line[:2] == '-=':
      self.popToken(self.lineNum,2,TokenType.DECREMENTER)
      return True      
    elif self.line[:1] in {'/', '*', '-', '+'}:
      self.popToken(self.lineNum,1,TokenType.MATHOP)
      return True
    #elif self.line[:2] in {'c:', 'g:', 's:'}:
    #  self.popToken(self.lineNum,2,TokenType.TYPEOP)
    #  return True
    return False

  def commentState(self):
    if self.line[:1] in {';' , '#'}:
      self.popToken(self.lineNum,len(self.line),TokenType.COMMENT)
      return True
    return False
  
  def BlockState(self):
    if self.line[:3] in {'"""' , "'''"}:
      self.popToken(self.lineNum,3,TokenType.BLOCK_START)
      return True
    return False

  def loadState(self):
    if self.line[:1] == '#':
      number =  1
      if self.line[:7] == '#end-if':
        number =  7
      elif self.line[:16] == '#load-if-defined':
        number =  16
      elif self.line[:20] == '#load-if-not-defined':
        number =  20
      elif self.line[:5] == '#else':
        number =  5
      else:
        return False
      self.popToken(self.lineNum,number,TokenType.LOAD_IF)
      return True
    return False
  
  def endLineState(self):
    if self.line[:1] == '\n':
      self.popToken(self.lineNum,1,TokenType.END_LINE)
      self.tokens[-1].value = '/n'
      return True
    return False

  def whiteSpaceState(self):
    length = 0
    while(self.line[:length+1].isspace() and self.line[:length+1] != '\n'):
        length = length + 1
        if(length == len(self.line)):
          self.popToken(self.lineNum,length,TokenType.WHITE_SPACE)
          return True
    if length == 0:
      return False
    if length > len(self.line):
      print("error")
    self.popToken(self.lineNum,length,TokenType.WHITE_SPACE)
    return True

  def tabState(self):
    length = 0
    while(self.line[:length+1].isspace()):
        length = length + 1
        if(length == len(self.line)):
          self.popToken(self.lineNum,length,TokenType.TABS)
          return True
    if length == 0:
      self.popToken(self.lineNum,length,TokenType.TABS)
      return True
    if length > len(self.line):
      raise Exception("tabState: lenght is greater then line length")
    self.popToken(self.lineNum,length,TokenType.TABS)
    return True

  def identifierSymbol(self, symbol):
    if symbol == '\n':
      return False
    if symbol.isalnum():
      return True
    if symbol in {'-', '_', '!', '<', '>', ':', '+', '*', '/', '=', '.'}: #TODO: for expressions to work without spaces. needed now for c:+ case
      return True
    return False

  def stringState(self):
    if self.line[:1] == '"':
      length = 1
      while(self.line[length] != '"'):
        length = length + 1
        if length == len(self.line):
          self.popToken(self.lineNum,length-1,TokenType.UNIDENTIFIED)
          return True
      length = length + 1
      self.line = self.line[1:] #gets rid of the leading "
      self.popToken(self.lineNum,length-2,TokenType.STRING)
      self.line = self.line[1:] #gets rid of the lagging ""
      return True
    return False

  def identifierState(self):
    length = 0
    if self.line[length].isalpha():
      length += 1 
    while(self.identifierSymbol(self.line[length])):
      length += 1 
        #print("input: "+self.line)
        #print("inputlen: "+str(len(self.line)))
        #print("length: "+ str(length))
    if length == 0:
      return False
    if length > len(self.line):
      print("error")
    identifierType = TokenType.IDENTIFIER

    # Load from a file
    with open('command_names.pkl', 'rb') as file:
        command_names = pickle.load(file)
    #TODO: add all the COMPARE ops with have C G and S
    if self.line[:length] in {"c:=","c:+","c:-","c:*","c:z/","c:/","c:mod","c:min","c:max","c:neg","c:%/","c:%*",
                              "g:=","g:+","g:-","g:*","g:z/","g:/","g:mod","g:min","g:max","g:neg","g:%/","g:%*",
                              "s:=","s:+","s:-","s:*","s:z/","s:/","s:mod","s:min","s:max","s:neg","s:%/","s:%*"}:
      identifierType = TokenType.MATHOP
    elif self.line[:2] in {'g:','c:','s:'}:
      identifierType = TokenType.TYPEOP
    elif self.line[:3] == "sn-":
      identifierType = TokenType.STRATEGIC_NUMBER
    elif self.line[:length] == "if":
      identifierType = TokenType.IF
    elif self.line[:length] == "while":
      identifierType = TokenType.WHILE
    elif self.line[:length] == "for":
      identifierType = TokenType.FOR
    elif self.line[:length] == "in":
      identifierType = TokenType.IN
    elif self.line[:length] == "range":
      identifierType = TokenType.RANGE
    elif self.line[:length] == "else":
      identifierType = TokenType.ELSE
    elif self.line[:length] == "elif":
      identifierType = TokenType.ELIF
    elif self.line[:length] == "def":
      identifierType = TokenType.DEF
    elif self.line[:length] == "defconst":
      identifierType = TokenType.DEFCONST
    elif self.line[:length] == "defrule":
      identifierType = TokenType.DEFRULE
    elif self.line[:length] == "return":
      identifierType = TokenType.RETURN
    elif self.line[:length] == "load-random":
      identifierType = TokenType.LOAD_RANDOM
    elif self.line[:length] == "load":
      identifierType = TokenType.LOAD
    elif self.line[:length] in {'Point','State','Int','Const'}:
      identifierType = TokenType.VAR_INIT
    elif self.line[:length] in {'or','and','not','nor','xor','nand', 'xnor'}:
      identifierType = TokenType.LOGIC_OP
    elif self.line[:length] == "else:":
      raise Exception("Sorry you need a space beteen else and : at line"+str(self.lineNum)+str(self.fileName))  
    elif self.line[:length] in command_names:
      identifierType = TokenType.COMMAND



    self.popToken(self.lineNum,length,identifierType)
    return True

  def numberState(self):
    length = 0
    if(self.line[0] == '-'):
      length += 1
      if not self.line[length].isnumeric():
        return False
    while(self.line[length].isnumeric()):
      length += 1
    if length == 0:
      return False
    if length > len(self.line):
      print("error")
    if self.line[length].isalpha():
      self.popToken(self.lineNum,length,TokenType.UNIDENTIFIED)
      return True
    self.popToken(self.lineNum,length,TokenType.NUMBER)
    return True

  def mainState(self):
    if self.endLineState(): return
    if self.whiteSpaceState(): return
    if self.BlockState():
      self.in_block = self.tokens[-1].value
      return
    elif self.numberState(): return   
    elif self.basicState(): return
    elif self.loadState(): return
    elif self.commentState(): return
    elif self.identifierState(): return
    elif self.stringState(): return
    self.popToken(self.lineNum,1,TokenType.UNCAUGHT)

  def scanLine(self, line:str, lineNum:int):
    self.line = line
    self.lineNum = lineNum
    if self.line.isspace(): #strips empty lines
      return
    if self.tabState():
      if self.loadState() or self.commentState():
        if self.tokens[len(self.tokens)-2].tokenType == TokenType.TABS:
          del self.tokens[len(self.tokens)-2]
        else: print("ERROR in SCAN, tried to delete tabs but was different tokenType")
    
    while(len(self.line)>0):
      #deals with block comments and block strings
      if self.in_block:
        if self.in_block in self.line:
          index = self.line.index(self.in_block)
          if index != 0: 
            self.popToken(self.lineNum,index,TokenType.BLOCK)
          self.popToken(self.lineNum,len(self.in_block),TokenType.BLOCK_END)
          self.in_block = ''
        else: #rest of line is in block
          if self.line[-1] == '\n':
            self.popToken(self.lineNum,len(self.line)-1,TokenType.BLOCK)
            self.popToken(self.lineNum,1,TokenType.BLOCK)
          else:
            self.popToken(self.lineNum,len(self.line),TokenType.BLOCK)
        if self.line.isspace(): #strips empty ends of lines after blocks
          return
      else:
        self.mainState()
      #print(self.line)
    #print(self.line)
  
  def scan(self):
    fullPath = "FILE NOT FOUND"
    self.fileName = self.fileName.replace("/","\\")
    for file in list(self.aiFolder.glob('**/*.per')):
      if self.fileName+".per" in str(file) or self.fileName in str(file):
        fullPath = file
    for file in list(self.aiFolder.glob('**/*.aop')): #prioritizes aop files because it is last
      if self.fileName+".aop" in str(file) or self.fileName in str(file):
        fullPath = file
    if fullPath == "FILE NOT FOUND":
      raise Exception(self.fileName+" is not found")
   # infile = open(os.path.join(os.path.dirname(sys.argv[0]), "folder2/test.txt"), "r+")
    try:
      f = open(fullPath,"r")
    except IOError:
      raise Exception ("Unable to open file:"+fullPath+", make sure you are not using paths")
    lines = f.readlines()

    lineNum = 0
    for line in lines:
      lineNum = lineNum + 1
      self.scanLine(line, lineNum)

    Tokens_to_remove = [
      TokenType.WHITE_SPACE,
      TokenType.COMMENT,
      #TokenType.BLOCK,
      #TokenType.BLOCK_START,
      #TokenType.BLOCK_END,
    ]
    for token in Tokens_to_remove:
      self.stripTokens(token)
