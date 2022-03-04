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

@pytest.mark.parametrize("valid_asignment", [
'''
x = y\n
''',
'''
my_Point_12 = Point()\n
\n
''',
'''
My_state = State()
''',
'''
counter = Int()
''',
'''
my_point.y = 12 + x
''',
])
def test_valid_func_def(valid_asignment):
  validate_parse(valid_asignment, VarAsignObject)

@pytest.mark.parametrize("invalid_asignment", [
'''
12 = 12
''',
'''
my_point = Point() + 12
''',
'''
variable = 13 + 12 + 1
''',
'''
variable = variable + 1 + 1
''',
])
def test_invalid_asignment(invalid_asignment):
  invalidate_parse(invalid_asignment)


@pytest.mark.parametrize("invalid_asignment_initializing_with_params", [
'''
my_point = Point(12,14)
''',
'''
my_point = Point(12)
''',
])
@pytest.mark.xfail
def test_invalid_asignment_initializing_with_params(invalid_asignment_initializing_with_params):
  invalidate_parse(invalid_asignment_initializing_with_params)