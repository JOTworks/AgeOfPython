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
if(true):
''',
'''
if(true):
(do-nothing)
''',
])
def test_invalid_if(invalid_if):
  invalidate_parse(invalid_if)