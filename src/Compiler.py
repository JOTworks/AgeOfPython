import ast
import inspect
from enum import Enum
from scraper import *
from scraper import aoe2scriptFunctions as aoe2scriptFunctions
from scraper import function_list
from collections import defaultdict
from Memory import Memory
from copy import copy
from utils import ast_to_aoe, evaluate_expression, get_enum_classes, reverse_compare_op
from utils_display import print_bordered
from MyLogging import logger


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
                            ast.Store,
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


class JumpType(Enum):
    last_rule_in_node = 0
    test_jump_to_beginning = 1
    jump_over_test = 2
    test_jump_to_beginning_after_init = 3
    jump_over_skip = 4
    last_rule_after_node = 5


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
        arg_enum = aoe2_enums[attr.value.id]
        arg = arg_enum[attr.attr]
        assert arg is not str
        self.enum = arg


class Variable(ast.Name):
    """
    something I can replace ast.Name objects with when I konw it will
    need memory alocation so Memory has an esier time finding them in the walk.
    """

    def __init__(self, args):
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
        self.func = ast.Name(
            id=name, ctx=ast.Load()
        )  # todo: check if this is redundant
        if not isinstance(args, list):
            raise TypeError("args must be a list")
        for itr, arg in enumerate(args):
            if type(arg) is EnumNode:
                arg = arg.enum
                args[itr] = arg

            if type(arg) is ast.Constant:
                pass
            if type(arg) is Variable:
                pass
            if type(arg) not in [JumpType, Variable, ast.Constant] + list(
                aoe2_enums.values()
            ):
                raise TypeError(f"arg {arg} is {type(arg)}")
        self.args = args

    def __repr__(self):
        args_str = ", ".join(map(str, self.args))
        return f"{self.func.id}({args_str})"


# defrules are just test and body. basicly if statements. so i just need to make everything into if statements
class DefRule(ast.If):
    def __init__(self, test: list, body: list, node, comment=""):
        super().__init__()
        check_terminal_nodes(test, Command)
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


class compilerTransformer(ast.NodeTransformer):
    def p_visit(self, node, tree_name="tree", vv=False):
        if vv:
            print_bordered(f"{tree_name} after {type(self)}")
            print(ast.dump((node), indent=4))
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


class AstToCustomNodeTransformer(compilerTransformer):
    def __init__(self, command_names, object_names):
        super().__init__()
        self.command_names = command_names
        self.object_names = object_names
        self.aoe2_enums = get_enum_classes()

    def make_variable(self, node, offset_index, id_n):
        is_variable = False
        if (
            id_n not in get_enum_classes()
            and id_n not in self.object_names
            and id_n not in self.command_names
        ):
            is_variable = True
        if is_variable:
            args = {
                "id": id_n,
                "ctx": node.ctx,
                "offset_index": offset_index,
                "lineno": node.lineno,
                "end_lineno": node.end_lineno,
                "col_offset": node.col_offset,
                "end_col_offset": node.end_col_offset,
            }
            node = Variable(args)
        return node

    def visit_Subscript(self, node):
        return self.make_variable(node, node.slice.value, node.value.id)

    def visit_Attribute(self, node):
        self.generic_visit(node)
        if node.value.id in self.aoe2_enums:
            return EnumNode(node)
        return self.make_variable(node, node.attr, node.value.id)

    def visit_Name(self, node):
        self.generic_visit(node)
        return self.make_variable(node, 0, node.id)

    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Name) and node.func.id in self.command_names:
            return Command(AOE2FUNC[node.func.id], node.args, node)

        if isinstance(node.func, ast.Name) and node.func.id in self.object_names:
            return Constructor(getattr(AOE2OBJ, node.func.id), node.args, node)
        return node


class ReduceTransformer(compilerTransformer):
    """
    Becasue Compare and BoolOp both short circit in python, they are build as lists (left and [right_list]) instead of recurcive (lef and right) like binOps.
    Because aoe2script only short circits on implied and, and not on any defined BoolOps, we are removing all lists in favor of recursion to simplify the compiler.
    this mean the short circuting will vary based on compiler optimization step implementation
    #!users should not count on commands in conditionals executing!
    #todo: put back in BoolOp And Lists if they are alone in a conditional, so the user can decide when to short-curcit
    https://discord.com/channels/485565215161843714/485566694912163861/1306940924944715817
    """

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
            op=node.op,
            values=[node.operand],
            lineno=node.lineno,
            col_offset=node.col_offset,
            end_lineno=node.end_lineno,
            end_col_offset=node.end_col_offset,
        )
        final_node = aoeOp(in_op)
        return final_node

    def visit_AugAssign(self, node):
        self.generic_visit(node)
        in_op = ast.Assign(
            targets=[node.target],
            value=ast.BinOp(
                left=node.target,
                op=node.op,
                right=node.value,
                lineno=node.lineno,
                col_offset=node.col_offset,
                end_lineno=node.end_lineno,
                end_col_offset=node.end_col_offset,
                file_path=node.file_path,
            ),
            lineno=node.lineno,
            col_offset=node.col_offset,
            end_lineno=node.end_lineno,
            end_col_offset=node.end_col_offset,
            file_path=node.file_path,
        )
        return in_op


class GarenteeAllCommandsInDefRule(compilerTransformer):
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


class AlocateAllMemory(compilerTransformer):
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
        self.generic_visit(node)
        assert isinstance(self.memory, Memory)
        if type(node.value) is Constructor:
            if len(node.targets) != 1:
                raise Exception(
                    f"multiple targets is not suported on line {node.lineno}"
                )
            if location := self.memory.get(node.targets[0].id):
                raise Exception(
                    f"{node.targets[0].id} is already in memory! dont try to re Construct it"
                )
            else:
                var_type = node.value.func.id
                self.memory.malloc(node.targets[0].id, var_type)
        return node

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        assert isinstance(self.memory, Memory)
        self.memory.malloc_func_call(
            node.name, node.args.args
        )  # todo: i really dont like the args.args, figure out how that happend
        return node

    def visit_Variable(self, node):
        if location := self.memory.get(node.id):
            node.memory_location = location
        else:
            self.memory.malloc(node.id, int)
            location = self.memory.get(node.id)
            node.memory_location = location
        return node


class CompileTransformer(compilerTransformer):
    # todo: make it so set_strategic_number(SN.initial_exploration_required, 0) could be replace with SN.initial_exploration_required = 0, and could have any expr in the asignment
    def __init__(self, command_names):
        super().__init__()
        self.command_names = command_names
        self.parent_map = {}
        self.temp_var_counter = 0

    def get_next_temp_var(self):
        self.temp_var_counter += 1
        return f"0t{self.temp_var_counter}"

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

    def visit_While(self, node, parent, in_field, in_node):
        """
        jump to end automaticaly, then jump to beggining if conditions are true
        same as if, only remove the one jump that skips the conditional
        """
        self.generic_visit(node)

        to_test = DefRule(
            Command(AOE2FUNC.true, [], None),
            [self.jump_constructor(JumpType.last_rule_in_node)],
            node_copy_with_short_offset(node, 2),
            comment="WHILE to_test " + str(node.lineno),
        )

        test = DefRule(
            self.visit_test(node.test),
            [self.jump_constructor(JumpType.test_jump_to_beginning)],
            None,
            comment="WHILE test " + str(node.lineno),
        )

        node.body = [to_test] + node.body + [test]

        node.test = (
            None  # remove to keep printer from printing it from test and from the body
        )
        return node

    def visit_For(self, node, parent, in_field, in_node):
        """
        jump to end automaticaly, then jump to beggining if conditions are true
        same as if, only remove the one jump that skips the conditional
        """
        if type(node.iter) is not ast.Call or node.iter.func.id != "range":
            raise Exception(f"for loops only support range, not {node.iter}")
        self.generic_visit(node)
        if len(node.iter.args) == 1:
            start, stop, step = (
                self.const_constructor(0),
                node.iter.args[0],
                self.const_constructor(1),
            )
        elif len(node.iter.args) == 2:
            start, stop, step = (
                node.iter.args[0],
                node.iter.args[1],
                self.const_constructor(1),
            )
        elif len(node.iter.args) == 3:
            start, stop, step = node.iter.args[0], node.iter.args[1], node.iter.args[2]
        else:
            raise Exception(f"for loop has {len(node.iter.args)} args, not 1, 2, or 3")

        op = compareOp.less_than
        if step.value and step.value < 0:
            op = compareOp.greater_than

        test = DefRule(
            Command(AOE2FUNC.up_compare_goal, [node.target, op, stop], node),
            [self.jump_constructor(JumpType.test_jump_to_beginning_after_init)],
            None,
            comment="FOR test " + str(node.lineno),
        )
        init = DefRule(
            Command(AOE2FUNC.true, [], None),
            [Command(AOE2FUNC.set_goal, [node.target, start], node)],
            None,
            comment="FOR init " + str(node.lineno),
        )
        jump_to_test = DefRule(
            Command(AOE2FUNC.true, [], None),
            [self.jump_constructor(JumpType.last_rule_in_node)],
            node_copy_with_short_offset(node, 2),
            comment="FOR to_test " + str(node.lineno),
        )
        incrementer = DefRule(
            Command(AOE2FUNC.true, [], None),
            [Command(AOE2FUNC.up_modify_goal, [node.target, mathOp.add, step], node)],
            None,
            comment="FOR inc " + str(node.lineno),
        )

        node.body = (
            [
                init,
                jump_to_test,
            ]
            + node.body
            + [
                incrementer,
                test,
            ]
        )
        return node

    def const_constructor(self, value):
        return ast.Constant(value=0)

    def jump_constructor(self, jump_type):
        return Command(AOE2FUNC.up_jump_direct, [jump_type], None)

    def visit_If(self, node, parent, in_field, in_node):
        self.generic_visit(node)

        test_commands = [self.jump_constructor(JumpType.jump_over_skip)]
        if node.disable_self:
            test_commands.append(Command(AOE2FUNC.disable_self, [], node))
        test = DefRule(
            self.visit_test(node.test),
            test_commands,
            None,
            comment="IF test " + str(node.lineno),
        )

        skip = DefRule(
            Command(AOE2FUNC.true, [], None),
            [self.jump_constructor(JumpType.last_rule_after_node)],
            node_copy_with_short_offset(node, 2),
            comment="IF skip " + str(node.lineno),
        )

        node.body = [
            test,
            skip,
        ] + node.body
        node.test = (
            None  # remove to keep printer from printing it from test and from the body
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
        self.generic_visit(node)

        # if type(node.comparators[0]) not in [ast.Constant, ast.Name]:
        #    raise Exception(
        #        f"{node.left} type of {type(node.left)} is not suported in compare"
        #    )
        left_type = type(node.left)
        right_type = type(node.comparators[0])
        if left_type is ast.Constant and right_type is ast.Constant:
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
                [
                    node.comparators[0],
                    reverse_compare_op(ast_to_aoe(type(node.ops[0]))),
                    node.left,
                ],
                node,
            )
        else:
            raise Exception(
                f"visit_compare Error! {type(node.left)=} and {type(node.comparators[0])=}"
            )
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

        if not (
            len(node.values) == 2
            or (len(node.values) == 1 and node.op.__doc__ == "Not")
        ):
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

    def visitAugAssign(self, node):
        raise Exception("AugAssign should all be parced out by ReduceTransformer")

    def visit_Assign(self, node, parent, in_field, in_node):
        #! todo: Make nested asignments work with binOp ect
        self.generic_visit(node)
        target = node.targets[0]
        if type(target) is not Variable:
            raise Exception(
                f"target needs to be Variable not {target}"
            )  # todo: add this to the asserter not the compiler
        if type(node.value) is ast.BinOp:
            if type(node.value.left) is Variable and type(node.value.right) in [
                ast.Constant,
                Variable,
            ]:
                if node.value.left.id != target.id:
                    raise Exception(
                        f"we only have 2c not 3c {ast.dump(node.value)}, and {node.value.left}!={target}"
                    )
                assign_command = Command(
                    AOE2FUNC.up_modify_goal,
                    [target, ast_to_aoe(type(node.value.op)), node.value.right],
                    node,
                )
            else:
                raise Exception(
                    f"only simple BinOp asignments are suported {ast.dump(node.value)}"
                )

        elif type(node.value) is Variable:
            # todo: this will only work on ints, needs to be delt with in Memory management to exstend this command to each index of the variable
            assign_command = Command(
                AOE2FUNC.up_modify_goal,
                [target, mathOp.eql, node.value],
                node,
            )

        elif type(node.value) is ast.Constant:
            assign_command = Command(
                AOE2FUNC.up_modify_goal,
                [target, mathOp.eql, node.value],
                node,
            )
        elif type(node.value) is EnumNode:
            assign_command = Command(
                AOE2FUNC.up_modify_goal,
                [target, mathOp.eql, node.value.enum],
                node,
            )
        elif type(node.value) is Constructor:
            return node
        else:
            # todo: allow var[0] instead of just var.x (uses ast.Subscript)
            raise Exception(f"{type(node.value)} not suported in asignments")
        if hasattr(target, "enum"):
            if type(target.enum) is SN:
                assign_command.func.id = AOE2FUNC.up_modify_sn
        return assign_command


class NumberDefrulesTransformer(compilerTransformer):
    def __init__(self):
        super().__init__()
        self.defrule_counter = 0

    def visit_If(self, node):
        node.first_defrule = self.defrule_counter
        self.generic_visit(node)
        node.last_defrule = self.defrule_counter - 1
        # raise Exception(f"{node.first_defrule=},{node.last_defrule=}")
        return node

    def visit_For(self, node):
        node.first_defrule = self.defrule_counter
        self.generic_visit(node)
        node.last_defrule = self.defrule_counter - 1
        # raise Exception(f"{node.first_defrule=},{node.last_defrule=}")
        return node

    def visit_While(self, node):
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


class ReplaceAllJumpStatementsTransformer(compilerTransformer):
    def replace_jump(self, node):
        for subnode in ast.walk(node):
            if isinstance(subnode, Command):
                for i, arg in enumerate(subnode.args):
                    arg_type = type(arg)
                    if arg_type == JumpType:
                        if arg is JumpType.jump_over_skip:
                            subnode.args[i] = str(node.first_defrule + 2)

                        elif arg is JumpType.last_rule_after_node:
                            subnode.args[i] = str(node.last_defrule + 1)

                        elif arg is JumpType.last_rule_in_node:
                            subnode.args[i] = str(node.last_defrule)

                        # both are the same right now because normal test_jump_to_beginning has an empty first rule like that.
                        elif (
                            arg is JumpType.test_jump_to_beginning
                            or arg is JumpType.test_jump_to_beginning_after_init
                        ):
                            subnode.args[i] = str(node.first_defrule + 1)

                        else:
                            subnode.args[i] = str(-1)
                            logger.error(f"{arg} not implemented yet")
        self.generic_visit(node)
        return node

    def visit_For(self, node):
        return self.replace_jump(node)

    def visit_While(self, node):
        return self.replace_jump(node)

    def visit_If(self, node):
        return self.replace_jump(node)

    def visit_Name(self, node):
        if type(node.id) is JumpType:
            raise Exception(f"{type(node.id)} JumpType not implemented yet")
        self.generic_visit(node)
        return node


class ScopeAllVariables(compilerTransformer):
    def __init__(self):
        super().__init__()
        self.scope_level = 0
        self.current_function = None

    ast.FunctionDef

    def visit_FunctionDef(self, node):
        if self.current_function is not None:
            raise Exception(
                f"current_function is {self.current_function}, you cannot define {node.name if node else 'a function'} in a function"
            )
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = None
        return node

    def visit_Variable(self, node):
        self.generic_visit(node)
        node.id = self.current_function + "." + node.id
        return node


class DisableSelfChecker(compilerTransformer):
    def __init__(self):
        self.valid_disable_selfs = []

    def unique_id(self, node):
        return f"{node.lineno}:{node.col_offset}"

    def visit_If(self, node):
        # Check each statement in the body of the If node
        new_body = []
        node.disable_self = False
        for stmt in node.body:
            found = False
            if isinstance(stmt, ast.Expr):  # Check if the statement is an Expr
                if isinstance(
                    stmt.value, ast.Call
                ):  # Check if the Expr contains a Call
                    func = stmt.value.func
                    if isinstance(func, ast.Name) and func.id == AOE2FUNC.disable_self:
                        found = True
                        node.disable_self = True
                        self.valid_disable_selfs.append(self.unique_id(stmt.value))
                        # logger.debug(f"Found 'disable_self' in If body at line {stmt.lineno}")
            if not found:
                new_body.append(stmt)
        node.body = new_body
        self.generic_visit(node)
        return node

    def visit_Command(self, node):
        # Check if the function being called is `disable_self`
        if isinstance(node.func, ast.Name) and node.func.id == AOE2FUNC.disable_self:
            if self.unique_id(node) not in self.valid_disable_selfs:
                raise Exception(
                    f"'disable_self' found outside of an If statement at line {node.lineno}"
                )
        self.generic_visit(node)
        return node

class AddTypeOp(compilerTransformer):
    #!#! need to add type of params back in for the printer to print! based on what is being passed into it
    def visit_Command(self, node):
            # Check if the function being called is `disable_self`
            function_list_typeOp = {}
            for function, args in function_list.items():
                if "typeOp" in args:
                    function_list_typeOp[function] = args

            if isinstance(node.func, ast.Name) and node.func.id in function_list_typeOp.keys():
                if self.unique_id(node) not in self.valid_disable_selfs:
                    raise Exception(
                        f"'disable_self' found outside of an If statement at line {node.lineno}"
                    )
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

    def compile(self, trees, vv=False):
        trees.main_tree = AstToCustomNodeTransformer(
            self.command_names, self.object_names
        ).p_visit(trees.main_tree, "main_tree", vv)
        trees.func_tree = AstToCustomNodeTransformer(
            self.command_names, self.object_names
        ).p_visit(trees.func_tree, "func_tree", vv)
        trees.main_tree = DisableSelfChecker().p_visit(trees.main_tree, "main_tree", vv)
        trees.func_tree = DisableSelfChecker().p_visit(trees.func_tree, "func_tree", vv)
        trees.main_tree = ReduceTransformer().p_visit(trees.main_tree, "main_tree", vv)
        trees.func_tree = ReduceTransformer().p_visit(trees.func_tree, "func_tree", vv)
        trees.func_tree = ScopeAllVariables().p_visit(trees.func_tree, "func_tree", vv)
        trees.main_tree = CompileTransformer(self.command_names).p_visit(
            trees.main_tree, "main_tree", vv
        )
        trees.func_tree = CompileTransformer(self.command_names).p_visit(
            trees.func_tree, "func_tree", vv
        )

        memory = Memory()

        trees.main_tree = AlocateAllMemory(
            memory
        ).p_visit(
            trees.main_tree, "main_tree", vv
        )  # find out last place vars are used, and automaticaly call free on them; walk through and keep a list of node and variable pairing, then add tag
        trees.func_tree = AlocateAllMemory(memory).p_visit(
            trees.func_tree, "func_tree", vv
        )
        trees.main_tree = GarenteeAllCommandsInDefRule().p_visit(
            trees.main_tree, "main_tree", vv
        )  # optimize commands together into defrules
        trees.func_tree = GarenteeAllCommandsInDefRule().p_visit(
            trees.func_tree, "func_tree", vv
        )

        combined_tree = trees.main_tree
        combined_tree.body = combined_tree.body + trees.func_tree.body

        combined_tree = NumberDefrulesTransformer().p_visit(
            combined_tree, "combined_tree", vv
        )
        combined_tree = ReplaceAllJumpStatementsTransformer().p_visit(
            combined_tree, "combined_tree", vv
        )

        print_bordered("Memory")
        memory.print_memory()

        return combined_tree


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
