import sys
sys.path.append('./src')
sys.path.append('../src')
sys.path.append('./Tests/test_ai_files')
import pytest
import ast
from test_ai_files.code_snipits_test import conditionals_success, conditionals_fail
from Parser import Aoe2Tree
from Compiler import Compiler
from Printer import Printer

class FilePathAdder(ast.NodeTransformer):
    def __init__(self, file_path=''):
        self.file_path = file_path

    def generic_visit(self, node):
        if isinstance(node, ast.AST):
            node.file_path = self.file_path
        return super().generic_visit(node)

def run_string_through_aop(string):
    tree = ast.parse(string)
    file_path_adder = FilePathAdder(file_path="TEST")
    modified_tree = file_path_adder.visit(tree) 
    trees = Aoe2Tree(modified_tree,None,None)
    compiler = Compiler()
    trees = compiler.compile(trees)
    myPrinter = Printer(trees)
    myPrinter.print_for_string_testing()

@pytest.mark.parametrize("test_input", conditionals_success)
def test_snipits_conditionals_success(test_input):
    run_string_through_aop(test_input)

@pytest.mark.parametrize("test_input", conditionals_fail)
def test_snipits_conditionals_fail(test_input):
    try:
        run_string_through_aop(test_input)
        assert False
    except:
        assert True


