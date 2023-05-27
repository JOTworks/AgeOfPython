import sys
sys.path.append('./src')
sys.path.append('../src')
sys.path.append('./Tests/test_ai_files')
from Interpreter import Interpreter
from data import *
from data import VarAsignObject
from Main import main
import test_strings
import pytest
from Scanner import Scanner

myInterperter = Interpreter(None)
tokenCenter = Token(TokenType.IDENTIFIER, "center", 0, "main")
tokenEquals = Token(TokenType.OPERATOR, "=", 0, "main")
tokenPlus = Token(TokenType.OPERATOR, "+", 0, "main")

@pytest.mark.parametrize("test_input,expected", [
("test_variable_asign.aop", test_strings.string_variable_asign)
])
def test_varAsignToCommands(test_input, expected):
  final_string = main([".\src\Main.py",test_input,"-test"])
  print_file = expected
  assert final_string == print_file


