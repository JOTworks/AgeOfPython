import sys
sys.path.append('./src')
sys.path.append('../src')
from Interpreter import Interpreter
from data import *
from data import VarAsignObject
import pytest
from Scanner import Scanner
from Parser import Parcer




def validate_parse(lines, type):
  myParser = Parcer([],"")
  myScanner = Scanner("","")
  myScanner.scanLines(lines.split("\n"))
  myParser.tokens = myScanner.tokens
  myParser.main = []
  myParser.parce()
  assert len(myParser.main) == 1
  if len(myParser.main) == 1:
    firstItem = myParser.main[0]
    assert isinstance(firstItem, type)

def invalidate_parse(lines):
  myParser = Parcer([],"")
  myScanner = Scanner("","")
  myScanner.scanLines(lines.split("\n"))
  myParser.tokens = myScanner.tokens
  myParser.main = []
  with pytest.raises(Exception):
    myParser.parce()

@pytest.mark.parametrize("valid_if", [
'''
if(true):
  (do-nothing)
''',
'''
if (true):
  (do-nothing)
  (do-nothing)
''',
'''
if(true)
(true):
  (do-nothing)
''',
])
def test_valid_if(valid_if):
  validate_parse(valid_if, IfObject)

@pytest.mark.parametrize("invalid_if", [
'''
if(true): (do-nothing)
''',
'''
if(true)(true): (do-nothing)
''',
'''
if(true):
(do-nothing)
''',
])
def test_invalid_if(invalid_if):
  invalidate_parse(invalid_if)

@pytest.mark.parametrize("valid_func_def", [
'''
def myFunction():
  (do-nothing)
''',
])
def test_valid_func_def(valid_func_def):
  validate_parse(valid_func_def, DefFuncObject)

@pytest.mark.parametrize("invalid_func_def", [
'''
def myFunction()::

''',
])
def test_invalid_func_def(invalid_func_def):
  invalidate_parse(invalid_func_def)