import sys
sys.path.append('./src')
sys.path.append('../src')
sys.path.append('./Tests/test_ai_files')
from Interpreter import Interpreter
from data import *
from data import VarAsignObject
from AOP.AgeOfPython.Main import main
from Scanner import Scanner
from Parser import Parcer
from data import *
from data import IfObject, WhileLoopObject
from enums import TokenType
import pytest

class TestScanner(Scanner):
  def __init__(self, input_string):
    self.aiFolder = None
    self.fileName = 'fileName'
    self.input_string = input_string
    self.line = ""
    self.lineIndent = [] #position is line number, value is number of spaces
    self.tokens = []
    self.in_block:str = ''

  def scan(self):
    lines = self.input_string.splitlines(keepends=True)
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
  

@pytest.mark.parametrize("test_input,expected", [
("""
if (True):
  print("true")
 """, "exspected"),
("""
if (1 == 1):
  print("true")
 """, "exspected"),
#("""
#if 1 == 1:
#  print("true")
# """, "exspected"),
])
def test_if(test_input, expected):
  myScanner = TestScanner(test_input)
  myScanner.scan()
  myParcer = Parcer(myScanner.tokens, 'ai_folder')
  myParcer.parce()
  assert isinstance(myParcer.main[0],IfObject)

@pytest.mark.parametrize("test_input,expected", [
("""
while (True):
  print("true")
 """, "exspected"),
("""
while (x == 1):
  print("true")
 """, "exspected"),
("""
while x == 1:
  print("true")
 """, "exspected"),
])
def test_while(test_input, expected):
  myScanner = TestScanner(test_input)
  myScanner.scan()
  myParcer = Parcer(myScanner.tokens, 'ai_folder')
  myParcer.parce()
  assert isinstance(myParcer.main[0],WhileLoopObject)