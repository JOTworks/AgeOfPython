from scraper import *
import ast
import operator

def ast_to_aoe(item):
    ast_to_aoe_dict = {
        ast.Gt: compareOp.greater_than,
        ast.GtE: compareOp.greater_or_equal,
        ast.Lt: compareOp.less_than, #todo: make the scraper pull in compareOp.less_then 
        ast.LtE: compareOp.less_or_equal,
        ast.Eq: compareOp.equal,
        ast.NotEq: compareOp.not_equal,
    }
    out_item = ast_to_aoe_dict.get(item, None)
    if out_item is None:
        raise NotImplementedError(f"ast_to_aoe not implemented for {item}")
    return out_item
    
class BinOperator:

    @staticmethod
    def get(op, result_type):
        type_tuple = ['ast', 'operator', 'mathOp', 'str']
        op_tuples = [
            (ast.Add, operator.add, mathOp.add, '+'),
            (ast.Sub, operator.sub, mathOp.sub, '-'),
            (ast.Mult, operator.mul, mathOp.mul, '*'),
            (ast.Div, operator.truediv, mathOp.div_fl, '/'), # IDK if these are the right devides
            (ast.FloorDiv, operator.floordiv, mathOp.div_rd, '//'),
            (ast.Mod, operator.mod, mathOp.mod, '%'),
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
            if isinstance(op, row[search_index]): #todo: only works with ast probably
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