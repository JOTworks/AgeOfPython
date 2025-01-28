import ast
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)

class NodeCounter(ast.NodeVisitor):
    def __init__(self):
        self.counts = {}

    def visit(self, node):
        node_type = type(node)
        self.counts[node_type] = self.counts.get(node_type, 0) + 1
        self.generic_visit(node)

class FunctionCallValidator(ast.NodeVisitor):
    def __init__(self, defined_functions):
        self.defined_functions = defined_functions
        self.errors = []

    def visit_Call(self, node):
        func_name = self.get_func_name(node)
        if func_name not in self.defined_functions:
            self.errors.append(f"Function '{func_name}' is not defined")
        else:
            func_def = self.defined_functions[func_name]
            self.check_arguments(node, func_def)
        self.generic_visit(node)

    def get_func_name(self, node):
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            return node.func.attr
        return None

    def check_arguments(self, node, func_def):
        expected_args = func_def.args.args
        if len(node.args) != len(expected_args):
            print(vars(node))
            self.errors.append(f"line: {node.lineno}, Function '{self.get_func_name(node)}' called with incorrect number of arguments")   

class Asserter:
    def is_valid_python(self, code):
        try:
            myMod = compile(code, '', 'exec')
            return True
        except SyntaxError as e:
            print(f"SyntaxError: {e}")
            return False

    def get_node_counts(self, tree):
        counter = NodeCounter()
        counter.visit(tree)
        return counter.counts
    
    def check_unsuported(self, node_counts):
        supported_nodes = [
            ast.If,
            ast.Add,
            ast.FunctionDef,
            ast.Name,
            ast.arg,
            ast.Assign,
            ast.BinOp,
            ast.Call,
            ast.ImportFrom,
            ast.Module,
            ast.alias,
            ast.Constant,
            ast.Store,
            ast.Assign,
            ast.Constant,
            ast.Module,
            ast.Store,
        ]

        not_supported_nodes = {
            ast.Import: "Use from ... import ... instead. keeps all imports non contextual.",
        }


        implemented_nodes = [
            ast.If,
            ast.Module,
            ast.ImportFrom,
            ast.alias,
            ast.Assign,
            ast.Constant,
            ast.Name,
            ast.Store,
        ]
        errors = []
        for node in node_counts:
            if node not in supported_nodes:
                if node in not_supported_nodes.keys():
                    errors.append(f'Not supported: {node.__name__} - {not_supported_nodes[node]}')
                else:
                    errors.append(f'Not supported: {node.__name__}')
            elif node not in implemented_nodes:
                errors.append(f'Not implemented: {node.__name__}')
        if errors:
            #raise Exception('\n'+'\n'.join(sorted(errors)))
            print(Fore.RED +'\n'+'\n'.join(sorted(errors)))
    
    def get_defined_functions(self, tree):
        defined_functions = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                defined_functions[node.name] = node
        return defined_functions

    def validate_function_calls(self, tree):
        defined_functions = self.get_defined_functions(tree)
        validator = FunctionCallValidator(defined_functions)
        validator.visit(tree)
        if validator.errors:
            raise Exception('\n'+'\n'.join(validator.errors))

    def check_function_calls(self, tree):
        pass
    def check(self, trees):
        for tree in trees:
            node_counts = self.get_node_counts(trees[tree]) 
            self.check_unsuported(node_counts)
        self.check_function_calls(trees['main_tree'])
        self.check_function_calls(trees['function_tree'])
