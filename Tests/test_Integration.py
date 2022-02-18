import sys
sys.path.append('./src')
sys.path.append('../src')
from Interpreter import Interpreter
from data import *
import unittest
from data import VarAsignObject


class TestInterpreter(unittest.TestCase):
  def setUp(self):
    self.myInterperter = Interpreter(None)
    self.tokenCenter = Token(TokenType.IDENTIFIER, "center", 0, "main")
    self.tokenEquals = Token(TokenType.OPERATOR, "=", 0, "main")
    self.tokenPlus = Token(TokenType.OPERATOR, "+", 0, "main")


  def test_test(self):
    self.assertTrue(True)


  def test_varAsignToCommands(self):
    varAsign = VarAsignObject(self.tokenCenter,[self.tokenCenter],0,"main")
    commands = self.myInterperter.varAsignToCommands(varAsign)
    self.assertTrue(len(commands) == 1)

    varAsign = VarAsignObject(self.tokenCenter,[self.tokenCenter,self.tokenPlus,self.tokenCenter],0,"main")
    commands = self.myInterperter.varAsignToCommands(varAsign)
    self.assertTrue(len(commands) == 2)

if __name__ == '__main__':
  unittest.main()

