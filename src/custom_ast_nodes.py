import ast
from utils import get_enum_classes, get_function_list_typeOp
from scraper import aoe2scriptFunctions as aoe2scriptFunctions
from scraper import typeOp
from enum import Enum
from scraper import AOE2FUNC
from MyLogging import logger

class JumpType(Enum):
    last_rule_in_node = 0
    test_jump_to_beginning = 1
    jump_over_test = 2
    test_jump_to_beginning_after_init = 3
    jump_over_skip = 4
    last_rule_after_node = 5
    set_return_pointer = 6
    jump_to_func = 7
    jump_back_to_after_call = 8
    last_rule_in_file = 9
    jump_to_else = 10

class FuncModule(ast.Module): 
    def __init__(self, name: str, args: list = [], node=None):
        super().__init__()
        self.lineno = node.lineno if node else None
        self.name = name
        self.args = args
        self.body = []
        self.type_ignores = []
        self.file_path = None

class Constructor(ast.Call):
    def __init__(self, object_name: str, args: list = [], lineno="."):
        super().__init__()
        self.lineno = lineno
        self.func = ast.Name(
            id=object_name, ctx=ast.Store()
        )  # TODO: make sure store was the right call here

        self.args = args


class EnumNode(ast.Attribute):
    def __init__(self, attr):
        self.attr = attr.attr
        self.value = attr.value
        aoe2_enums = get_enum_classes()
        
        try:
            arg_enum = aoe2_enums[attr.value.id]
        except KeyError:
            raise Exception(f"{attr.value.id} is not a valid parameterType")
        try:
            arg = arg_enum[attr.attr]
        except KeyError:
            raise Exception(f"{attr.attr} is not a valid option for parameterType: {attr.value.id}, line {attr.lineno}")
        assert arg is not str
        self.enum = arg


class Variable(ast.Name): #! give Variable a good constructor for comiler classes to use.
    """
    something I can replace ast.Name objects with when I konw it will
    need memory alocation so Memory has an esier time finding them in the walk.
    """

    def __init__(self, args):
        if "offset_index" in args:
            self.offset_index = args.pop("offset_index")
        
        super().__init__(**args)

    pass


class aoeOp(ast.BoolOp):
    """
    this is a wrapper for a BoolOp BUT ALSO includes the UniOp Not()
    """

    def __init__(self, in_op):
        for attr in self._attributes:
            self.__setattr__(attr, in_op.__getattribute__(attr))
        self.values = in_op.values
        self.op = in_op.op
        if not self.__getattribute__("values"):
            raise Exception("BoolOp Created without a Values attribute")


class Command(ast.Call):
    def __init__(self, function_name: AOE2FUNC, args: list, node):
        super().__init__()
        
        self.function_list_typeOp = get_function_list_typeOp()

        if node:
            self.lineno = node.lineno
            self.end_lineno = node.end_lineno
            self.col_offset = node.col_offset
            self.end_col_offset = node.end_col_offset
            self.file_path = node.file_path
        
        del node

        self.aoe2_enums = get_enum_classes()
        # TODO: this is where i can do hard type checking for command params
        if not isinstance(function_name, AOE2FUNC):
            raise TypeError(f"needs to be a AOE2FUNC, got {type(function_name)}")
        self.func = ast.Name(
            id=function_name, ctx=ast.Load()
        )  # todo: check if this is redundant
        if not isinstance(args, list):
            raise TypeError("args must be a list")
        self._args = self.add_typeOp_args(args, function_name.name)
        if self._args:
            for itr, arg in enumerate(self._args):
                self._args[itr] = self.validate_arg(arg)

    def add_typeOp_args(self, args, name):
        try:
            command_args = args
            if name in list(self.function_list_typeOp.keys()):
                function_arg_types = self.function_list_typeOp[name]
                typeOp_indexs = [index for index, element in enumerate(function_arg_types) if element == "typeOp"]
                for index in typeOp_indexs:
                    if type(command_args[index]) is Variable:
                        type_op = typeOp.goal
                    elif type(command_args[index]) is ast.Constant:
                        type_op = typeOp.constant
                    elif type(command_args[index]) is EnumNode:
                        type_op = typeOp.constant
                    elif type(command_args[index]) is JumpType:
                        if command_args[index] in [
                            JumpType.jump_back_to_after_call,
                        ]:
                            type_op = typeOp.goal
                        elif command_args[index] in [
                            JumpType.last_rule_in_file,
                            JumpType.last_rule_in_node,
                            JumpType.test_jump_to_beginning,
                            JumpType.jump_over_test,
                            JumpType.test_jump_to_beginning_after_init,
                            JumpType.jump_over_skip,
                            JumpType.last_rule_after_node,
                            JumpType.jump_to_func,
                            JumpType.set_return_pointer,
                            JumpType.jump_to_else,
                        ]:
                            type_op = typeOp.constant
                        else:
                            logger.error(f"assuming const, not goal: {command_args[index]}")
                            type_op = typeOp.constant
                    else:
                        #todo: make SNs get tracked here for s:
                        raise Exception(f"typeOp expects a variable or constant at index {index} not {type(command_args[index])} for {self.func.id} at {self.lineno}")
                    command_args = command_args[:index] + [type_op] + command_args[index:]
            return command_args
        except IndexError as e:
            print(name, args, function_arg_types,"lineno", self.lineno)
            raise e

    @property
    def args(self):
        return self._args

    def append_args(self, arg):
        self._args.append(None)
        self.set_arg(len(self._args)-1, arg)
        

    def set_arg(self, index, arg):
        if index >= len(self._args):
            raise IndexError(f"index {index} out of range for args {self._args}")
        if index < 0:
            raise IndexError(f"index {index} out of range for args {self._args}")
        self._args[index] = self.validate_arg(arg)

    def validate_arg(self, arg):
        if type(arg) is EnumNode:
            arg = arg.enum

        elif type(arg) is ast.Constant:
            pass
        elif type(arg) is Variable:
            pass
        elif type(arg) is str:
            raise Exception("str is not a valid type for args")
        elif type(arg) not in [JumpType, Variable, ast.Constant] + list(
            self.aoe2_enums.values()
        ):
            raise TypeError(f"arg {arg} is {type(arg)}, not ast.Constant, Variable, or str. line{self.lineno}")
        return arg

    def __repr__(self):
        args_str = ", ".join(map(str, self._args))
        return f"{self.func.id}({args_str})"


# defrules are just test and body. basicly if statements. so i just need to make everything into if statements
class DefRule(ast.If):
    def __init__(self, test: list, body: list, node, comment=""):
        super().__init__()
        self.check_terminal_nodes(test, Command)
        self.comment = comment
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

    def check_terminal_nodes(self, tree, node_type):
        for node in ast.walk(tree):
            if isinstance(node, ast.AST):
                children = [
                    getattr(node, field) for field in node._fields if hasattr(node, field)
                ]
                if all(not isinstance(child, ast.AST) for child in children):
                    if not (
                        isinstance(node, node_type)
                        or isinstance(
                            node,
                            (
                                ast.BoolOp,
                                ast.And,
                                ast.Or,
                                ast.Not,
                                ast.Load,
                                ast.Store,
                                ast.Eq,
                                ast.Gt,
                                ast.GtE,
                                ast.Constant,
                                ast.Add,
                            ),
                        )
                    ):
                        raise TypeError(
                            f"Terminal node {ast.dump(node)} is not {node_type}"
                        )