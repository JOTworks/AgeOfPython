import sys
sys.path.append('./src')
sys.path.append('../src')
sys.path.append('./Tests/test_ai_files')
from main import main
import pytest


#@pytest.mark.parametrize("test_input,expected", [
#("if_code.py", test_strings.string_variable_asign),
##("test_while_loop.aop", test_strings.string_while_loop),
##("test_if.aop", test_strings.string_if),
##("test_nested_if.aop", test_strings.string_nested_if),
##("test_incroment.aop", test_strings.string_incroment),
#])
#def test_full_file(test_input, expected):
#  final_string = main([".\src\Main.py",test_input,"-t"])
#  print_file = expected
#  assert final_string == print_file


def test_replaced_JumpType():
  final_string = main([".\src\Main.py","if_code.py","-t"])
  assert "JumpType" not in final_string, "JumpType is not replaced"
