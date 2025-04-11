import ast
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

#todo: no variables names are function names
#todo: all functions have the correct parameters, unless the compareOp special grammer
#todo: do not allow use of reserved words like range (may already be taken care of in the ast.parcer)
#todo: check that all returns of a function match the return definition of python
#todo: what happens if someone tries to put in a c: or g: to a function where it would normaly belong?
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

    def visit_Return(self, node):
        # Find the function this return belongs to
        current_function = self.get_enclosing_function(node)
        if current_function is None:
            return  # Skip if not inside a function

        # Get the annotated return type of the function
        annotated_return_type = current_function.returns
        if annotated_return_type is None:
            return  # Skip if the function has no annotated return type

        # Check the type of the return value
        return_value = node.value
        if return_value is not None:
            if not self.is_type_compatible(return_value, annotated_return_type):
                self.errors.append(
                    f"line: {node.lineno}, Return value does not match the annotated return type '{annotated_return_type.id}' in function '{current_function.name}'"
                )
        else:
            # If the return is `None`, ensure the annotated type is `None` or compatible
            if not isinstance(annotated_return_type, ast.Name) or annotated_return_type.id != "None":
                self.errors.append(
                    f"line: {node.lineno}, Return value is None, but the annotated return type is '{annotated_return_type.id}' in function '{current_function.name}'"
                )

        self.generic_visit(node)
        
    def get_enclosing_function(self, node):
        # Traverse up the AST to find the enclosing function definition
        while node:
            if isinstance(node, ast.FunctionDef):
                return node
            node = getattr(node, "parent", None)
        return None

    def is_type_compatible(self, return_value, annotated_return_type):
        # Check compatibility between the return value and the annotated type
        if isinstance(annotated_return_type, ast.Name):
            # Handle basic types like int, str, etc.
            if annotated_return_type.id == "int" and isinstance(return_value, ast.Constant) and isinstance(return_value.value, int):
                return True
            if annotated_return_type.id == "str" and isinstance(return_value, ast.Constant) and isinstance(return_value.value, str):
                return True
            if annotated_return_type.id == "float" and isinstance(return_value, ast.Constant) and isinstance(return_value.value, float):
                return True
            if annotated_return_type.id == "bool" and isinstance(return_value, ast.Constant) and isinstance(return_value.value, bool):
                return True
            if annotated_return_type.id == "None" and return_value is None:
                return True
        # Add more type compatibility checks as needed
        return False


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
            self.errors.append(
                f"line: {node.lineno}, Function '{self.get_func_name(node)}' called with incorrect number of arguments"
            )


class Asserter:
    def is_valid_python(self, code):
        try:
            myMod = compile(code, "", "exec")
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
                    errors.append(
                        f"Not supported: {node.__name__} - {not_supported_nodes[node]}"
                    )
                else:
                    errors.append(f"Not supported: {node.__name__}")
            elif node not in implemented_nodes:
                errors.append(f"Not implemented: {node.__name__}")
        if errors:
            # raise Exception('\n'+'\n'.join(sorted(errors)))
            print(Fore.RED + "\n" + "\n".join(sorted(errors)))

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
            raise Exception("\n" + "\n".join(validator.errors))

    def check_function_calls(self, tree):
        pass

    def check(self, tree):
        self.check_unsuported(tree)
        self.check_function_calls(tree)
