from distutils import command
import sys
sys.path.append('./src')
sys.path.append('../src')
from Interpreter import Interpreter
from data import *
from data import VarAsignObject
import pytest
from Scanner import Scanner
from Parser import Parcer
from test_structure_utils import *

@pytest.mark.parametrize("valid_func_def", [
'''
def myFunction():
  (do-nothing)
''',
'''
def myFunction ():
  (do-nothing)
''',
'''
def myFunction():
  (do-nothing)
  (do-nothing)
  (do-nothing)
  (do-nothing)
  (do-nothing)
''',
'''
def myFunction(x):
  (do-nothing)
''',
'''
def myFunction(x,y):
  (do-nothing)
''',
'''
def myFunction(x , y):
  (do-nothing)
''',
])
def test_valid_func_def(valid_func_def):
  validate_parse(valid_func_def, DefFuncObject)

@pytest.mark.parametrize("invalid_func_def", [
'''
def myFunction ():

''',
'''
def myFunction(x x):
  (do-nothing)
''',
'''
def myFunction(x,y,):
  (do-nothing)
''',
'''
def myFunction(,):
  (do-nothing)
''',
])
def test_invalid_func_def(invalid_func_def):
  invalidate_parse(invalid_func_def)

@pytest.mark.xfail
def test_accedental_multiline_parse(): #TODO:this works differently then if its in a file :(
  acidental_funtion_call = '''
x = y
(do-nothing)
\n\n
'''
  myParser = Parcer([],"")
  myScanner = Scanner("","")
  myScanner.scanLines(acidental_funtion_call.split("\n"))
  myParser.tokens = myScanner.tokens
  myParser.main = []
  myParser.parce()
  assert len(myParser.main) == 2
  if len(myParser.main) == 2:
    assert isinstance(myParser.main[0], VarAsignObject)
    assert isinstance(myParser.main[1], CommandObject)
