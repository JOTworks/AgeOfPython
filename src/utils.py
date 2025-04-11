from scraper import *
import ast
import operator
import inspect
import enum
import scraper.aoe2scriptEnums
from scraper.aoe2scriptFunctions import function_list, AOE2VarType
from MyLogging import logger

def get_function_list_typeOp():
    function_list_typeOp = {}
    for function, args in function_list.items():
            if "typeOp" in args:
                function_list_typeOp[function.replace('-','_')] = args
    return function_list_typeOp

def reverse_compare_op(compare_op):
    reverse_dict = {
        compareOp.greater_than: compareOp.less_or_equal,
        compareOp.less_than: compareOp.greater_or_equal,
        compareOp.equal: compareOp.equal,
        compareOp.not_equal: compareOp.not_equal
    }
    combined_dict = {**reverse_dict, **{v: k for k, v in reverse_dict.items()}}
    return combined_dict[compare_op]

def ast_to_aoe(item):
    ast_to_aoe_dict = {
        ast.Gt: compareOp.greater_than,
        ast.GtE: compareOp.greater_or_equal,
        ast.Lt: compareOp.less_than,  # todo: make the scraper pull in compareOp.less_then
        ast.LtE: compareOp.less_or_equal,
        ast.Eq: compareOp.equal,
        ast.NotEq: compareOp.not_equal,
        ast.Add: mathOp.add,
        ast.Sub: mathOp.sub,
        ast.Mult: mathOp.mul,
        ast.Div: mathOp.div_rd,
        ast.FloorDiv: mathOp.div_fl,
        ast.Mod: mathOp.mod,
    }
    out_item = ast_to_aoe_dict.get(item, None)
    if out_item is None:
        out_item = ast_to_aoe_dict.get(item.__class__, None)
    if out_item is None:
        raise NotImplementedError(f"ast_to_aoe not implemented for {item}")
    return out_item


class BinOperator:
    @staticmethod
    def get(op, result_type):
        type_tuple = ["ast", "operator", "mathOp", "str"]
        op_tuples = [
            (ast.Add, operator.add, mathOp.add, "+"),
            (ast.Sub, operator.sub, mathOp.sub, "-"),
            (ast.Mult, operator.mul, mathOp.mul, "*"),
            (
                ast.Div,
                operator.truediv,
                mathOp.div_fl,
                "/",
            ),  # IDK if these are the right devides
            (ast.FloorDiv, operator.floordiv, mathOp.div_rd, "//"),
            (ast.Mod, operator.mod, mathOp.mod, "%"),
        ]
        try:
            search_index = type_tuple.index(op.__module__)
        except ValueError:
            raise ValueError(f"Unsupported search type: {op}")
        try:
            result_index = type_tuple.index(result_type.__name__)
        except ValueError:
            raise ValueError(f"Unsupported result type: {result_type.__name__}")

        for row in op_tuples:
            if isinstance(op, row[search_index]):  # todo: only works with ast probably
                return row[result_index]
        raise ValueError(f"Unsupported operator: {op}")

    @staticmethod
    def get_ast(op):
        return BinOperator.get(op, ast)

    @staticmethod
    def get_operator(op):
        return BinOperator.get(op, operator)

    @staticmethod
    def get_aoe(op):
        return BinOperator.get(op, mathOp)

    @staticmethod
    def get_string(op):
        return BinOperator.get(op, str)


def evaluate_expression(constant1, operator_str, constant2):
    for constant in [constant1, constant2]:
        try:
            constant = int(constant)
        except ValueError:
            raise Exception(f"constant1 is not an int: {constant}")

    op_func = BinOperator.get_operator(operator_str)
    if op_func is None:
        raise ValueError(f"Unsupported operator: {operator_str}")

    return int(op_func(constant1, constant2))

def get_aoe2_var_types():
    aoe2_var_types = {}
    for name, obj in inspect.getmembers(scraper.aoe2scriptEnums):
        if inspect.isclass(obj) and issubclass(obj, AOE2VarType):
            aoe2_var_types[name] = obj
            if name == "Boolean":
                aoe2_var_types["bool"] = obj
            if name == "Integer":
                aoe2_var_types["int"] = obj

    return aoe2_var_types

def get_list_from_return(value_returns):
    if value_returns is None:
        return_values = []
    elif type(value_returns) is ast.Tuple:
        return_values = value_returns.elts
    elif type(value_returns) in [ast.List, list]:
        return_values = value_returns
    else: #todo: maybe make throw error if not a type that is part of the scraper import
        return_values = [value_returns]
        logger.error(f"Unknown return type {type(value_returns)}")
    return return_values

def get_enum_classes():
    enum_classes = {}
    for name, obj in inspect.getmembers(aoe2scriptEnums):
        if inspect.isclass(obj) and issubclass(obj, enum.Enum):
            enum_classes[name] = obj
    return enum_classes
