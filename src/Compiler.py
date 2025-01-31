import ast
import inspect
from enum import Enum
from scraper import *
from scraper import aoe2scriptFunctions as aoe2scriptFunctions
from collections import defaultdict

def check_terminal_nodes(tree, node_type):
    for node in ast.walk(tree):
        if isinstance(node, ast.AST):
            children = [
                getattr(node, field) for field in node._fields if hasattr(node, field)
            ]
            if all(not isinstance(child, ast.AST) for child in children):
                if not (
                    isinstance(node, node_type)
                    or isinstance(
                        node, (ast.BoolOp, ast.And, ast.Or, ast.Not, ast.Load)
                    )
                ):
                    raise TypeError(
                        f"Terminal node {ast.dump(node)} is not {node_type}"
                    )


def find_extra_node_types(tree, allowed_types):
    allowed_types = [t for t in allowed_types]
    allowed_types += (ast.Module, ast.Load, ast.Name, ast.Store)
    allowed_types = tuple(allowed_types)
    extra_node_counts = defaultdict(int)
    for node in ast.walk(tree):
        if not isinstance(node, allowed_types):
            extra_node_counts[type(node).__name__] += 1
    return dict(extra_node_counts)


class JumpType(Enum):
    last_rule_in_node = 0
    test_jump_to_beginning = 1


class Constructor(ast.Call):
    def __init__(self, object_name: str, args: list = [], lineno="."):
        super().__init__()
        self.lineno = lineno
        self.func = ast.Name(
            id=object_name, ctx=ast.Store()
        )  # TODO: make sure store was the right call here

        self.args = args


class Command(ast.Call):
    def __init__(self, name: AOE2FUNC, args: list, node):
        super().__init__()
        if node:
            self.lineno = node.lineno
            self.end_lineno = node.end_lineno
            self.col_offset = node.col_offset
            self.end_col_offset = node.end_col_offset
            self.file_path = node.file_path

        # TODO: this is where i can do hard type checking for command params
        if not isinstance(name, AOE2FUNC):
            raise TypeError(f"needs to be a AOE2FUNC, got {type(name)}")
        self.func = ast.Name(id=name, ctx=ast.Load())
        if not isinstance(args, list):
            raise TypeError("args must be a list")
        for arg in args:
            if not (isinstance(arg, JumpType) or isinstance(arg, str)):
                raise TypeError(f"arg {arg} is {type(arg)}")
        self.args = args

    def __repr__(self):
        args_str = ", ".join(map(str, self.args))
        return f"{self.func.id}({args_str})"


# defrules are just test and body. basicly if statements. so i just need to make everything into if statements
class DefRule(ast.If):
    def __init__(self, test: list, body: list, node):
        super().__init__()
        check_terminal_nodes(test, Command)
        if node:
            self.lineno = node.lineno
            self.end_lineno = node.end_lineno
            self.col_offset = node.col_offset
            self.end_col_offset = node.end_col_offset
            self.file_path = node.file_path

        self.test = test
        for cmd in body:
            pass  # TODO: check if all of the tree end objects are commands
        if not isinstance(body, list):
            raise TypeError(f"body {type(body)} must be a list")
        for stmt in body:
            if not isinstance(stmt, Command):
                raise TypeError(f"body {type(stmt)} must be a list of commands")
        self.body = body


class CallToCommandAndConstructorTransformer(ast.NodeTransformer):
    def __init__(self, command_names, object_names):
        super().__init__()
        self.command_names = command_names
        self.object_names = object_names

    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Name) and node.func.id in self.command_names:
            return Command(
                AOE2FUNC[node.func.id], [ast.unparse(arg) for arg in node.args], node
            )

        if isinstance(node.func, ast.Name) and node.func.id in self.object_names:
            return Constructor(
                AOE2OBJ[node.func.id], [ast.unparse(arg) for arg in node.args]
            )
        return node


class GarenteeAllCommandsInDefRule(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.defrule_stack = []

    def visit_DefRule(self, node):
        print(len(self.defrule_stack))
        self.defrule_stack.append(node)
        self.generic_visit(node)
        self.defrule_stack.pop()
        return node

    def visit_Command(self, node):
        if not self.defrule_stack:
            return DefRule(Command(AOE2FUNC.true, [], None), [node], None)
        self.generic_visit(node)
        return node


class CompileTransformer(ast.NodeTransformer):
    def __init__(self, command_names):
        super().__init__()
        self.command_names = command_names

    def visit_Call(self, node):
        self.generic_visit(node)

    def visit_If(self, node):
        """
        jump to end automaticaly, then jump to beggining if conditions are true
        """
        self.generic_visit(node)
        last_rule_in_node = Command(
            AOE2FUNC.up_jump_direct, [JumpType.last_rule_in_node], None
        )
        test_jump_to_beginning = Command(
            AOE2FUNC.up_jump_direct, [JumpType.test_jump_to_beginning], None
        )
        node.body = (
            [
                DefRule(
                    Command(AOE2FUNC.true, [], None),
                    [last_rule_in_node],
                    node_copy_with_short_offset(node, 2),
                )
            ]
            + node.body
            + [DefRule(self.visit_test(node.test), [test_jump_to_beginning], None)]
        )
        return node

    def visit_test(self, test):
        # returns a command or a tree of commands
        if isinstance(test, ast.Constant) and test.value == True:
            return Command(AOE2FUNC.true, [], test)
        self.generic_visit(test)
        return test

    def visit_Assign(self, node):
        # returns a command or a tree of commands
        # target is a goal, and values can be goal, constant, or tree
        self.generic_visit(node)
        return node


class Compiler:
    def __init__(self):
        self.command_names = [
            name
            for name, obj in inspect.getmembers(aoe2scriptFunctions, inspect.isfunction)
        ]
        self.object_names = [
            name
            for name, obj in inspect.getmembers(aoe2scriptFunctions, inspect.isclass)
        ]
        return

    def compile(self, trees):
        transformed_tree = CallToCommandAndConstructorTransformer(
            command_names=self.command_names, object_names=self.object_names
        ).visit(trees.main_tree)

        # optimize concepts like deleting things that do nothing

        transformed_tree = CompileTransformer(command_names=self.command_names).visit(
            transformed_tree
        )

        # optimize commands together

        # alocate Memory

        transformed_tree = GarenteeAllCommandsInDefRule().visit(transformed_tree)

        # replace all the jumps

        extra_nodes = find_extra_node_types(transformed_tree, (ast.If, Command))
        if extra_nodes:
            print(f"Extra nodes found: {extra_nodes}")

        trees.main_tree = transformed_tree
        return trees


def node_copy_with_short_offset(node, offset):
    node_copy = DummyNode(node)
    node_copy.end_lineno = node.lineno
    node_copy.end_col_offset = node.col_offset + offset
    return node_copy


class DummyNode:
    def __init__(self, node):
        self.lineno = node.lineno
        self.end_lineno = node.end_lineno
        self.col_offset = node.col_offset
        self.end_col_offset = node.end_col_offset
        self.file_path = node.file_path
