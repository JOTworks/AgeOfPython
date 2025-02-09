import ast
import inspect
from enum import Enum
from scraper import *
from scraper import aoe2scriptFunctions as aoe2scriptFunctions
from collections import defaultdict
from Memory import Memory
from copy import copy
from utils import ast_to_aoe, evaluate_expression, get_enum_classes, reverse_compare_op
from utils_display import print_bordered


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
                        node,
                        (
                            ast.BoolOp,
                            ast.And,
                            ast.Or,
                            ast.Not,
                            ast.Load,
                            ast.Eq,
                            ast.Gt,
                            ast.Constant,
                            ast.Add,
                        ),
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

class Variable(ast.Name):
    """
    something I can replace ast.Name objects with when I konw it will
    need memory alocation so Memory has an esier time finding them in the walk.
    """
    def __init__(self, args):
        self.offset_index = args.pop('offset_index')
        super().__init__(**args)

    pass

class aoeOp(ast.BoolOp):
    """
    this is a wrapper for a BoolOp BUT ALSO includes the UniOp Not()
    """
    def __init__(self, in_op):
        for attr in self._attributes:
            self.__setattr__(attr,in_op.__getattribute__(attr))
        self.values = in_op.values
        self.op = in_op.op
        if not self.__getattribute__("values"):
            raise Exception("BoolOp Created without a Values attribute")

#! make the commands take Variable Object instead of strings! then pass it to printer to print number
class Command(ast.Call):
    def __init__(self, name: AOE2FUNC, args: list, node):
        super().__init__()
        if node:
            self.lineno = node.lineno
            self.end_lineno = node.end_lineno
            self.col_offset = node.col_offset
            self.end_col_offset = node.end_col_offset
            self.file_path = node.file_path
        aoe2_enums = get_enum_classes()
        # TODO: this is where i can do hard type checking for command params
        if not isinstance(name, AOE2FUNC):
            raise TypeError(f"needs to be a AOE2FUNC, got {type(name)}")
        self.func = ast.Name(id=name, ctx=ast.Load())  # todo: check if this is redundant
        if not isinstance(args, list):
            raise TypeError("args must be a list")
        for itr, arg in enumerate(args):
            if type(arg) is ast.Attribute and arg.value.id in aoe2_enums.keys():
                arg_enum = aoe2_enums[arg.value.id]
                arg = arg_enum[arg.attr]
                assert arg is not str
                args[itr] = arg
            
            if type(arg) is ast.Constant:
                pass
            if type(arg) is Variable:
                pass
            if type(arg) not in [JumpType, Variable, ast.Constant] + list(aoe2_enums.values()):
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


class AstToCustomNodeTransformer(ast.NodeTransformer):
    def __init__(self, command_names, object_names):
        super().__init__()
        self.command_names = command_names
        self.object_names = object_names

    def make_variable(self, node):
        if type(node) is ast.Name:
            offset_index = 0
            id_n = node.id
        elif type(node) is ast.Attribute:
            offset_index = node.attr
            id_n = node.value.id
        else:
            raise Exception(f"{type(node)=} not Name or Attribute")

        is_variable = False
        if (id_n not in get_enum_classes()
        and id_n not in self.object_names
        and id_n not in self.command_names
            ):
            is_variable = True
        if is_variable:
            args = {
                'id':id_n,
                'ctx':node.ctx,
                'offset_index':offset_index,
                'lineno':node.lineno,
                'end_lineno':node.end_lineno,
                'col_offset':node.col_offset,
                'end_col_offset':node.end_col_offset,
            }
            node = Variable(args)
        return node
    
    def visit_Attribute(self, node):
        self.generic_visit(node)
        return self.make_variable(node)
    
    def visit_Name(self, node):
        self.generic_visit(node)
        return self.make_variable(node)
        

    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Name) and node.func.id in self.command_names:
            return Command(AOE2FUNC[node.func.id], node.args, node)

        if isinstance(node.func, ast.Name) and node.func.id in self.object_names:
            return Constructor(getattr(AOE2OBJ, node.func.id), node.args, node)
        return node


class ReduceCompareBoolUnaryTransformer(ast.NodeTransformer):
    """
    Becasue Compare and BoolOp both short circit in python, they are build as lists (left and [right_list]) instead of recurcive (lef and right) like binOps.
    Because aoe2script only short circits on implied and, and not on any defined BoolOps, we are removing all lists in favor of recursion to simplify the compiler.
    this mean the short circuting will vary based on compiler optimization step implementation
    #!users should not count on commands in conditionals executing!
    #todo: put back in BoolOp And Lists if they are alone in a conditional, so the user can decide when to short-curcit
    https://discord.com/channels/485565215161843714/485566694912163861/1306940924944715817
    """

    def __init__(self):
        super().__init__()

    # x < y < z -> x<y and y<z
    def visit_Compare(self, node):
        self.generic_visit(node)
        if len(node.comparators) > 1:
            # create a list of compare nodes
            compare_node_list = []
            compare_node_one = copy(node)
            compare_node_one.ops = [compare_node_one.ops[0]]
            compare_node_one.comparators = [compare_node_one.comparators[0]]
            compare_node_list.append(compare_node_one)
            for itr, comparator in enumerate([node.left] + node.comparators):
                if itr == 0:
                    continue
                compare_node_next = copy(compare_node_one)
                compare_node_next.left = compare_node_next.comparators[0]
                compare_node_next.ops = [node.ops[itr - 1]]
                compare_node_next.comparators = [comparator]
                compare_node_list.append(compare_node_next)

            # nest the list of compares into boolOps
            final_node = None
            for compare_node in compare_node_list:
                if final_node is None:
                    final_node = compare_node
                else:
                    final_node = ast.BoolOp(
                        op=ast.And(),
                        values=[compare_node, final_node],
                        lineno=compare_node.lineno,
                        col_offset=compare_node.col_offset,
                        end_lineno=compare_node.end_lineno,
                        end_col_offset=compare_node.end_col_offset,
                    )
            return final_node
        return node

    def visit_BoolOp(self, node):
        self.generic_visit(node)
        if (
            len(node.values) > 2
        ):  # todo: fix the lineno and col_offset for created boolOps
            # nest boolOps
            final_node = node.values[0]
            for itr, value in enumerate(node.values):
                if itr == 0:
                    continue
                boolop_node_next = aoeOp(copy(node))
                boolop_node_next.values = [value, final_node]
                final_node = boolop_node_next
            return final_node
        return aoeOp(node)
    
    def visit_UnaryOp(self, node):
        self.generic_visit(node)
        in_op = ast.BoolOp(
            op = node.op, 
            values = [node.operand], 
            lineno=node.lineno,
            col_offset=node.col_offset,
            end_lineno=node.end_lineno,
            end_col_offset=node.end_col_offset
        )
        final_node = aoeOp(in_op)
        return final_node

class GarenteeAllCommandsInDefRule(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.defrule_stack = []

    def visit_DefRule(self, node):
        self.defrule_stack.append(node)
        self.generic_visit(node)
        self.defrule_stack.pop()
        return node

    def visit_Command(self, node):
        if len(self.defrule_stack) == 0:
            return DefRule(Command(AOE2FUNC.true, [], None), [node], None)
        self.generic_visit(node)
        return node

class AlocateAllMemory(ast.NodeTransformer): 
    #! WIP 
    #! need to sort out asignments and mem alocation and Constructions. 
    #! referencing before asignment should be ok, becuase its a loop for the most part.
    #! get functions working STAT
    """
    if there is an asignment then I know what type it is.
    - either asign to constructor
    - asign to another object that has a type
    - in a for loop

    allow for DEL later
    DEL things that are out of scope (only functions)
    everything is pass by reference
    no globals!
    """
    def __init__(self, memory):
        super().__init__()
        self.memory = memory

    def visit_Assign(self, node):
        assert isinstance(self.memory, Memory)

        print('_____ASSIGN______')
        print(ast.dump(node, indent=4))
        if type(node.value) is Constructor:
            if len(node.targets) != 1:
                raise Exception(f"multiple targets is not suported on line {node.lineno}")
            if location := self.memory.get(node.targets[0].id):
                    raise Exception (f"{node.targets[0].id} is already in memory! dont try to re Construct it")
            else:
                var_type = node.value.func.id
                self.memory.malloc(node.targets[0].id,var_type)

    def visit_Variable(self, node):
        if location := self.memory.get(node.id):
            node.memory_location = location
            print(f"{location=}")
        else:
            self.memory.malloc(node.id, int)
            location = self.memory.get(node.id)
            node.memory_location = location
        return node

class CompileTransformer(ast.NodeTransformer):
    def __init__(self, command_names):
        super().__init__()
        self.command_names = command_names
        self.parent_map = {}
        self.temp_var_counter = 0

    def get_next_temp_var(self):
        self.temp_var_counter += 1
        return f"0t{self.temp_var_counter}"

    # todo: make this visit follow the one actual NodeTransformer one, and not the visitor one. if i want in_field and in_node to work
    # def generic_visit(self, node, parent=None, in_field=[], in_node=[]): #check this is fine or not? AI GEN
    #    if parent:
    #        self.parent_map[node] = parent
    #    for field, value in ast.iter_fields(node):
    #        if isinstance(value, list):
    #            for item in value:
    #                if isinstance(item, ast.AST):
    #                    self.visit(item, node, in_field + [field], in_node + [type(node)])
    #        elif isinstance(value, ast.AST):
    #            self.visit(value, node, in_field + [field], in_node + [type(node)])
    #    return node

    def visit(self, node, parent=None, in_field=[], in_node=[]):
        parent = self.parent_map.get(node)
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        temp_counter = 1
        # Call the visitor method with appropriate arguments
        sig = inspect.signature(visitor)
        params = sig.parameters
        args = {}
        if "parent" in params:
            args["parent"] = parent
        if "in_field" in params:
            args["in_field"] = in_field
        if "in_node" in params:
            args["in_node"] = in_node

        return visitor(node, **args)

    def visit_Attribute(self, node):
        self.generic_visit(node)
        return node
    
    def visit_Call(self, node, parent, in_field, in_node):
        self.generic_visit(node)
        return node

    def visit_If(self, node, parent, in_field, in_node):
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
        node.test = (
            None  # keeps the printer from printing twice. may need to reinstate later?
        )
        return node

    def in_node(
        self, node, ast_type
    ):  # returns true if node has a parent (recersivly) of type ast.AST
        looking_node = node
        while self.parent_map.get(looking_node, None):
            if isinstance(looking_node, ast_type):
                return True
            looking_node = self.parent_map[looking_node]

    def visit_Compare(self, node, parent, in_field, in_node):
        # x>12==y<12 turns into x>12 AND 12==y AND y<12
        print("in visit_compare")
        self.generic_visit(node)

        #if type(node.comparators[0]) not in [ast.Constant, ast.Name]:
        #    raise Exception(
        #        f"{node.left} type of {type(node.left)} is not suported in compare"
        #    )
        left_type = type(node.left)
        right_type = type(node.comparators[0])
        if (left_type is ast.Constant and right_type is ast.Constant):
            raise Exception(
                f"dont compare 2 constants {node.left.value} and {node.comparators[0].value}. just reduce"
            )
        elif left_type is Variable and right_type in (ast.Constant, Variable):
            compare_comand = Command(
                AOE2FUNC.up_compare_goal,
                [node.left, ast_to_aoe(type(node.ops[0])), node.comparators[0]],
                node,
            )
        elif left_type is ast.Constant and right_type is Variable:
            compare_comand = Command(
                AOE2FUNC.up_compare_goal,
                [node.comparators[0], reverse_compare_op(ast_to_aoe(type(node.ops[0]))), node.left],
                node,
            )
        else:
            raise Exception(f"visit_compare Error! {type(node.left)=} and {type(node.comparators[0])=}")
        return compare_comand
    
    def visit_BinOp(self, node, parent, in_field, in_node):
        # will be 2CT and needs to be up-goal-modify # ALWAYS use temperary vars for this
        self.generic_visit(node)
        if type(node.left) is ast.Constant and type(node.right) is ast.Constant:
            new_constant = copy(node.left)
            new_constant.end_lineno, new_constant.end_col_offset = (
                node.right.end_lineno,
                node.right.end_col_offset,
            )
            new_constant.value = evaluate_expression(
                node.left.value, node.op, node.right.value
            )
            node = new_constant
        return node

    def visit_BoolOp(self, node, parent, in_field, in_node):  # and, or
        raise Exception("all boolOp should be aoeOp")
    def visit_UnaryOp(self, node):
        raise Exception("all unaryOp should be aoeOp")
    
    def visit_aoeOp(self, node):
        # white listing what can exisit in boolOp
        if len(node.values) != 2:
            raise Exception(f"BoolOp must have 2 values nof {len(node.values)}")
        for itr, value in enumerate(node.values):
            if type(value) is ast.Constant:
                if value.value is True:
                    node.values[itr] = value = Command(AOE2FUNC.true, [], value)
                elif value.value is False:
                    node.values[itr] = value = Command(AOE2FUNC.false, [], value)
            if type(value) is ast.Name:
                raise Exception(
                    f"{type(value)} not a valid node inside a BoolOp, use [x != 0] instead of [x]"
                )
            if type(value) not in (aoeOp, ast.Compare, Command):
                raise Exception(
                    f"{type(value)}:{value.value} not a valid node inside a BoolOp after compile"
                )
        return node

    def visit_test(self, test):
        # returns a command or a tree of commands
        if isinstance(test, ast.Constant) and test.value == True:
            return Command(AOE2FUNC.true, [], test)
        self.generic_visit(test)
        return test

    def visit_Assign(self, node, parent, in_field, in_node):
        # returns a command or a tree of commands
        # target is a goal, and values can be goal, constant, or tree
        self.generic_visit(node)
        return node


class NumberDefrulesTransformer(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.defrule_counter = 0

    def visit_If(self, node):
        node.first_defrule = self.defrule_counter
        self.generic_visit(node)
        node.last_defrule = self.defrule_counter - 1
        # raise Exception(f"{node.first_defrule=},{node.last_defrule=}")
        return node

    def visit_DefRule(self, node):
        self.generic_visit(node)
        node.defrule_num = self.defrule_counter
        self.defrule_counter += 1
        return node


class ReplaceAllJumpStatementsTransformer(ast.NodeTransformer):
    def visit_If(self, node):
        for subnode in ast.walk(node):
            if isinstance(subnode, Command):
                for i, arg in enumerate(subnode.args):
                    if arg is JumpType.last_rule_in_node:
                        subnode.args[i] = str(node.last_defrule)
                    elif arg is JumpType.test_jump_to_beginning:
                        subnode.args[i] = str(node.first_defrule + 1)
        self.generic_visit(node)
        return node

    def visit_Name(self, node):
        if type(node.id) is JumpType:
            raise Exception(f"{type(node.id)} JumpType not implemented yet")
        self.generic_visit(node)
        return node


class ScopeAllVariables(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.scope_level = 0
        self.scoped_variables = {}

    # todo: make a visit_Variable function.

    def visit_FunctionDef(self, node):
        self.scope_level += 1
        self.generic_visit(node)
        self.scope_level -= 1
        return node

    def visit_Assign(self, node):
        self.generic_visit(node)
        for target in node.targets:
            if isinstance(target, ast.Name):
                scoped_name = f"{target.id}_scope{self.scope_level}"
                self.scoped_variables[target.id] = scoped_name
                target.id = scoped_name
        return node

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id in self.scoped_variables:
            node.id = self.scoped_variables[node.id]
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
        transformed_tree = AstToCustomNodeTransformer(
            command_names=self.command_names, object_names=self.object_names
        ).visit(trees.main_tree)
        transformed_tree = ReduceCompareBoolUnaryTransformer().visit(trees.main_tree)
        # optimize concepts like deleting things that do nothing

        transformed_tree = CompileTransformer(command_names=self.command_names).visit(
            transformed_tree
        )
        # optimize commands together

        transformed_tree = ScopeAllVariables().visit(transformed_tree)
        # todo: optimization for later
        # append last place used
        # transformed_tree = GetVeriableLastUseNodes().visit(transformed_tree)
        # walk through and keep a list of node and variable pairing, then add tag
        memory = Memory()
        transformed_tree = AlocateAllMemory(memory).visit(transformed_tree)

        transformed_tree = GarenteeAllCommandsInDefRule().visit(transformed_tree)
        transformed_tree = NumberDefrulesTransformer().visit(transformed_tree)
        transformed_tree = ReplaceAllJumpStatementsTransformer().visit(transformed_tree)

        print_bordered("Memory")
        memory.print_memory()

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
