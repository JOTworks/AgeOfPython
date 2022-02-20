import sys
sys.path.append('./src')
sys.path.append('../src')
from Interpreter import Interpreter
from data import *
from data import VarAsignObject
import pytest
from Scanner import Scanner

@pytest.mark.parametrize("test_input,expected", [
('variableName', TokenType.IDENTIFIER)
])
def test_scanner(test_input, expected):
  assert expected == expected

myInterperter = Interpreter(None)
tokenCenter = Token(TokenType.IDENTIFIER, "center", 0, "main")
tokenEquals = Token(TokenType.OPERATOR, "=", 0, "main")
tokenPlus = Token(TokenType.OPERATOR, "+", 0, "main")
  
def test_varAsignToCommands():
  varAsign = VarAsignObject(tokenCenter,[tokenCenter],0,"main")
  defrule = varAsign.interpret()
  assert len(defrule.executeList) == 1
  varAsign = VarAsignObject(tokenCenter,[tokenCenter,tokenPlus,tokenCenter],0,"main")
  defrule = varAsign.interpret()
  assert len(defrule.executeList) == 2


