import ast
import inspect
from itertools import chain
from scraper import *
from scraper import AOE2FUNC, Integer, Constant
from scraper import aoe2scriptFunctions as aoe2scriptFunctions
from custom_ast_nodes import Command, DefRule, Variable, aoeOp, EnumNode, Constructor, JumpType, FuncModule
from Memory import Memory
from copy import copy
from utils import ast_to_aoe, evaluate_expression, get_enum_classes, reverse_compare_op, get_aoe2_var_types, get_list_from_return
from utils_display import print_bordered
from MyLogging import logger

FUNC_DEPTH_COUNT = "func_depth_count"
FUNC_RET_REG = 15800 #janky but up_set_indirect_goal needs an integer to store into, so either i need to sepreatly parce it out later, or start it as an integer here
reserved_function_names = [
    'range',
] + list(get_enum_classes().keys()) + list(get_aoe2_var_types().keys())

def new_jump(jump_type):
        return Command(AOE2FUNC.up_jump_direct, [jump_type], None)

def new_do_nothing():
        return Command(AOE2FUNC.do_nothing, [], None)


class compilerTransformer(ast.NodeTransformer):
    def p_visit(self, node, tree_name="tree", vv=False):
        if vv:
            print_bordered(f"{tree_name} after {type(self)}")
            print(ast.dump((node), indent=4))
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)
    
    def visit_Return(self, node):
        self.generic_visit(node)
        if hasattr(node, 'body'):
            for item in node.body:
                item = self.visit(item)
        return node
    
    def visit_Assign(self, node):
        self.generic_visit(node)
        if hasattr(node, 'body'):
            for item in node.body:
                item = self.visit(item)
        return node


class AstToCustomTR(compilerTransformer):
    def __init__(self, command_names, object_names):
        super().__init__()
        self.command_names = command_names
        self.object_names = object_names
        self.aoe2_enums = get_enum_classes()
    
    def make_variable(self, node, offset_index, id_n):
        is_variable = False
        if not(offset_index is None or type(offset_index) is str):
            raise Exception(f"offset_index needs to be a str, not {type(offset_index)}, line {node.lineno}")
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
        raise Exception("subscript not supported, need to figure out how to pass int to make_variable() as offset_index")
        return self.make_variable(node, node.slice.value, node.value.id)

    def visit_Attribute(self, node):
        self.generic_visit(node)
        if node.value.id in self.aoe2_enums:
            return EnumNode(node)
        return self.make_variable(node, node.attr, node.value.id)

    def visit_Name(self, node):
        self.generic_visit(node)
        return self.make_variable(node, None, node.id)

    def visit_UnaryOp(self, node): #todo: move this to ReduceTR class somehow. needs to happen before command generation in this class however
        self.generic_visit(node)
        if isinstance(node.op, ast.USub) and type(node.operand) is ast.Constant:
            node.operand.value = -node.operand.value
            return node.operand
        return node

    def add_missing_defaults(self, func_name, args, lineno=None):
        #todo: make _ symbol reserved as a variable name
        #todo: make _ get replaced as a default value as a shorthand.
        parameter_type_defaults = {
            EscrowGoalId.__name__: ast.Constant(0),
            PlacementType.__name__: PlacementType.place_normal,
            DUCAction.__name__: DUCAction.action_default,
            Formation.__name__: Formation._1,
            AttackStance.__name__: AttackStance._1,

        }
        parameters = inspect.signature(globals()[func_name]).parameters
        default_params_in_function = len([param for param in parameters if param in parameter_type_defaults])
        
        #if all args are set
        if len(args) == len(parameters):
            if "_" not in [arg.id for arg in args if type(arg) is Variable]:
                return args
            
            for i, param in enumerate(parameters):
                if param in parameter_type_defaults and type(args[i]) is Variable:
                    if args[i].id == "_":
                        args[i] = parameter_type_defaults[param]
            return args

        else: #incorrect number of args
            if compareOp.__name__ in parameters:
                logger.error(f"{func_name} is proably using drop compareOp syntax, line {lineno}")
                return args
            else:
                if len(parameters) - len(args) != default_params_in_function:
                    raise Exception(f"you must either ommit or define ALL default varaibles, use _ for default, line {lineno}")

                for i, param in enumerate(parameters):
                    if param in parameter_type_defaults:
                        args = args[:i] + [parameter_type_defaults[param]] + args[i:]
                return args
                
        raise Exception(f"should be imporsible to ge to here, line {lineno}")
        

    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Name) and node.func.id in self.command_names:
            command_args = self.add_missing_defaults(node.func.id, node.args, node.lineno)
            return Command(AOE2FUNC[node.func.id], command_args, node)

        if isinstance(node.func, ast.Name) and node.func.id in self.object_names:
            return Constructor(getattr(AOE2OBJ, node.func.id), node.args, node)
        return node


class ReduceTR(compilerTransformer):
    """
    Becasue Compare and BoolOp both short circit in python, they are build as lists (left and [right_list]) instead of recurcive (lef and right) like binOps.
    Because aoe2script only short circits on implied and, and not on any defined BoolOps, we are removing all lists in favor of recursion to simplify the compiler.
    this mean the short circuting will vary based on compiler optimization step implementation
    #!users should not count on commands in conditionals executing!
    #todo: put back in BoolOp And Lists if they are alone in a conditional, so the user can decide when to short-curcit
    https://discord.com/channels/485565215161843714/485566694912163861/1306940924944715817
    """
    #todo: make EscrowGoalId optional. if they have one less arg, place 0 in as the escro position arg
    def recursively_nested_comare_nodes(self, node):
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

    # x < y < z -> x<y and y<z
    def visit_Compare(self, node):
        self.generic_visit(node)

        #this simplifies all compareOps to nested format, instead of list format if its all the same operator
        if len(node.comparators) > 1:
            return self.recursively_nested_comare_nodes(node)

        #this allows for the compare to be pulled out of the Command 
        #example: unit_type_count(UnitId.Archer) > 12 instead of unit_type_count(UnitId.Archer, compareOp.greater_than, 12)
        if type(node.left) is Command:
            func_name = node.left.func.id.name
            function_obj = globals()[func_name]
            parameters = inspect.signature(function_obj).parameters
            if "compareOp" in parameters:
                node.left.append_args(ast_to_aoe(node.ops[0]))
                node.left.append_args(node.comparators[0])
                return node.left 
                 
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


class WrapInDefRules(compilerTransformer):
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
        assert isinstance(self.memory, Memory)
        if type(node.value) is Constructor:
            if len(node.targets) != 1:
                raise Exception(
                    f"multiple targets is not suported on line {node.lineno}"
                )
            if location := self.memory.get(node.targets[0].id):
                logger.warning(f"{node.targets[0].id} is already in memory! {location} dont try to re Construct it, line {node.lineno}")
            else:
                var_type = node.value.func.id
                self.memory.malloc(node.targets[0].id, var_type)
        node = super().visit_Return(node) #this one needs to happen after so it can us the Constructor before visit_Variable uses the default of Integer
        return node

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        assert isinstance(self.memory, Memory)
        self.memory.malloc_func_call(
            node.name, node.args.args
        )  # todo: i really dont like the args.args, figure out how that happend
        return node

    def visit_Variable(self, node):
        if not (location := self.memory.get(node.id,node.offset_index)):
            logger.error(f"we are doing strict typing. you need to initialize {node.id}")
            self.memory.malloc(node.id, Integer)
            location = self.memory.get(node.id, node.offset_index)
            
        node.memory_location = location
        node.memory_name = self.memory.get_name_at_location(location)
        return node


class CompileTR(compilerTransformer):
    # todo: make it so set_strategic_number(SN.initial_exploration_required, 0) could be replace with SN.initial_exploration_required = 0, and could have any expr in the asignment
    def __init__(self, command_names, func_def_dict):
        super().__init__()
        self.command_names = command_names
        self.parent_map = {}
        self.temp_var_counter = 0
        self.func_def_dict = func_def_dict
        self.current_func_def = None
        self.aoe2_var_types = get_aoe2_var_types()

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
        func_name = node.func.id
        if func_name in reserved_function_names:
            return node
        func_def_node = self.func_def_dict[func_name]
        if func_name in reserved_function_names:
            return node
        func_call_module = FuncModule(func_name, node.args, node)
        
        
        func_depth_incromenter = DefRule(
            Command(AOE2FUNC.true, [], node),
            [Command(AOE2FUNC.up_modify_goal, [Variable({'id':FUNC_DEPTH_COUNT,'offset_index':None}), mathOp.add, self.const_constructor(1)], node)], #todo: make a variable constructer 
            node,
            comment="FUNC_dept_inc " + str(node.lineno),
        )

        set_return_rule_pointer = DefRule(
            Command(AOE2FUNC.true, [], node),
            [Command(AOE2FUNC.up_set_indirect_goal, 
                     [Variable({'id':FUNC_DEPTH_COUNT,'offset_index':None}), JumpType.set_return_pointer], node)], #! make sure this dosnt dercomnavigate the momory alocattor.
            node,
            comment="FUNC_ret_set " + str(node.lineno),
        )

        func_depth_decromenter = DefRule(
            Command(AOE2FUNC.true, [], None),
            [Command(AOE2FUNC.up_modify_goal, [Variable({'id':FUNC_DEPTH_COUNT,'offset_index':None}), mathOp.sub, self.const_constructor(1)], None)], #todo: make a variable constructer 
            None, #todo: find a way to make this node and not have 3 lines of green comments in printer
            comment="FUNC_depth_dec " + str(node.lineno),
        )

        asign_func_arg_commands = []
        for i, arg in enumerate(node.args):
            if type(arg) is Variable:
                right_side = Variable({'id':arg.id})
            elif type(arg) in [ast.Constant, EnumNode]:
                right_side = arg
                
            else:
                raise Exception(f"func args need to be either a Variable or Constant, not {type(arg)}, line {node.lineno}")
            asign_func_arg_commands.append(
                Command(AOE2FUNC.up_modify_goal, [
                    Variable({'id':func_name + "." + func_def_node.args.args[i].arg,'offset_index':None}), #!this is bad, somehow i need to pull it the same way the memory does it, or the same way the scope walker does it
                    mathOp.eql, 
                    right_side,
                ], node)
                )
        asign_func_args = DefRule(
                Command(AOE2FUNC.true, [], node),
                asign_func_arg_commands,
                node,
        )
        jump_to_func = DefRule(
            Command(AOE2FUNC.true, [], node),
            [Command(AOE2FUNC.up_jump_direct, [JumpType.jump_to_func], node)],
            node,
        )

        func_call_module.body = (
            [
                func_depth_incromenter,
                set_return_rule_pointer,
                asign_func_args,
                jump_to_func,
                func_depth_decromenter,
            ]
        )
        return func_call_module

    def visit_While(self, node, parent, in_field, in_node):
        """
        jump to end automaticaly, then jump to beggining if conditions are true
        same as if, only remove the one jump that skips the conditional
        """
        self.generic_visit(node)

        to_test = DefRule(
            Command(AOE2FUNC.true, [], None),
            [new_jump(JumpType.last_rule_in_node)],
            node_copy_with_short_offset(node, 2),
            comment="WHILE to_test " + str(node.lineno),
        )

        test = DefRule(
            self.visit_test(node.test),
            [new_jump(JumpType.test_jump_to_beginning)],
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
            raise Exception(f"for loops only support range, not {node.iter}, line {node.lineno}")
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
            [new_jump(JumpType.test_jump_to_beginning_after_init)],
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
            [new_jump(JumpType.last_rule_in_node)],
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
        return ast.Constant(value=value)

    def visit_If(self, node, parent, in_field, in_node):
        self.generic_visit(node)

        test_commands = [new_jump(JumpType.jump_over_skip)]
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
            [new_jump(JumpType.jump_to_else if node.orelse != [] else JumpType.last_rule_after_node)],
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
                f"visit_compare Error! {type(node.left)=} and {type(node.comparators[0])=}, line {node.lineno}"
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
        self.generic_visit(node)
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
        raise Exception("AugAssign should all be parced out by ReduceTR")

    def visit_Assign(self, node, parent, in_field, in_node):
        #todo: Make nested asignments work with binOp ect
        node.body = []
        assign_command = []
        self.generic_visit(node)
        target = node.targets[0]
        if type(target) is Variable:
            modify_function = AOE2FUNC.up_modify_goal
        elif type(target) is EnumNode and type(target.enum) is SN:
            modify_function = AOE2FUNC.up_modify_sn
        else:
            #todo: refactor this when i do binops and everything
            raise Exception(
                f"target needs to be Variable or SN not {type(target)}, line {node.lineno}"
            )  # todo: add this to the asserter not the compiler
        if type(node.value) is ast.BinOp:
            if type(node.value.left) is Variable and type(node.value.right) in [
                ast.Constant,
                Variable,
            ]:
                if node.value.left.id != target.id:
                    raise Exception(
                        f"we only have 2c not 3c {ast.dump(node.value)}, and {node.value.left}!={target} line {node.lineno}"
                    )
                assign_command.append( Command(
                    modify_function,
                    [target, ast_to_aoe(type(node.value.op)), node.value.right],
                    node,
                ))
            else:
                raise Exception(
                    f"only simple BinOp asignments are suported {ast.dump(node.value)}"
                )

        elif type(node.value) is Variable:
            # todo: this will only work on ints, needs to be delt with in Memory management to exstend this command to each index of the variable
            assign_command.append( Command(
                modify_function,
                [target, mathOp.eql, node.value],
                node,
            ))

        elif type(node.value) is ast.Constant:
            assign_command.append( Command(
                modify_function,
                [target, mathOp.eql, node.value],
                node,
            ))
        elif type(node.value) is EnumNode:
            assign_command.append( Command(
                modify_function,
                [target, mathOp.eql, node.value.enum],
                node,
            ))
        elif type(node.value) is Constructor:
            if len(node.value.args) > 0:
                raise Exception(
                    f"we dont curently support constructors with args {[arg.value if hasattr(arg, 'value') else arg for arg in node.value.args]}, line {node.lineno}"
                )
            return node
        
        elif type(node.value) is FuncModule:
            assign_command = self.make_set_returned_values_commands(node)

        else:
            # todo: allow var[0] instead of just var.x (uses ast.Subscript)
            raise Exception(f"{type(node.value)} not suported in asignments")
        
        node.body = [DefRule(
            Command(AOE2FUNC.true, [], node),
            assign_command,
            node,
            "FUNC_returned " + str(node.lineno),
        )]
        return node

    def make_jump_back_rules(self, lineno):
        set_jump_back = DefRule(
            Command(AOE2FUNC.true, [], None),
            [Command(AOE2FUNC.up_get_indirect_goal, [Variable({'id':FUNC_DEPTH_COUNT,'offset_index':None}), ast.Constant(15900)], None)],
                None, #todo: find a way to make this node and not have 3 lines of green comments in printer
                comment="FUNC_set_jump " + str(lineno),
        ) 
        jump_back_to_after_call = DefRule(
            Command(AOE2FUNC.true, [], None),
            [new_jump(JumpType.jump_back_to_after_call)],
            None, #todo: find a way to make this node and not have 3 lines of green comments in printer
            comment="FUNC_return " + str(lineno),
        )
        return [set_jump_back, jump_back_to_after_call]

    def make_set_returned_values_commands(self, node): #todo: merge with make_set_return_pointers_commands at some point
        #!#!make sure the fucntion happens first before the asigning
        #instead of (set-goal 15800 1)
        #it will be (up-set-goal-indirect return_Val_name G! 15800)]
        return_values = get_list_from_return(node.targets)
        funct_returns_values = get_list_from_return(self.func_def_dict[node.value.name].returns)
        if len(return_values) != len(funct_returns_values):
            if len(return_values) == 0:
                return []
            raise Exception(f"function {self.current_func_def.name} has {len(funct_returns_values)} returns, not {len(return_values)}, line {node.lineno}")

        set_returned_values_commands = []
        return_register_count = 0
        for i, funct_ret_val in enumerate(funct_returns_values):
            length = self.aoe2_var_types[funct_ret_val.id].length
            for j in range(length):
                
                set_returned_values_commands.append(Command(
                    AOE2FUNC.up_set_indirect_goal,
                    [
                        Variable({'id':return_values[i].id,'offset_index':j}),
                        ast.Constant(FUNC_RET_REG+return_register_count),
                    ],
                    node,))
                return_register_count += 1

        return set_returned_values_commands
    
    def make_set_return_pointers_commands(self, node):
        return_values = get_list_from_return(node.value)
        funct_returns_values = get_list_from_return(self.current_func_def.returns)
        if len(return_values) != len(funct_returns_values):
            if len(return_values) == 0:
                return []
            raise Exception(f"function {self.current_func_def.name} has {len(funct_returns_values)} returns, not {len(return_values)}, line {node.lineno}")
        set_return_pointers_commands = []
        return_register_count = 0
        for i, funct_ret_val in enumerate(funct_returns_values):
            length = self.aoe2_var_types[funct_ret_val.id].length
            for j in range(length):
                if type(return_values[i]) is ast.Tuple:
                    return_value = return_values[i].elts[j]
                else:
                    return_value = return_values[i]
                    if length > 1:
                        raise Exception(f"return value {return_values[i]} is a constant but has length {length}, line {node.lineno}")
                    
                if type(return_value) is ast.Constant:
                    set_return_pointers_commands.append(Command(
                        AOE2FUNC.set_goal,
                        [ast.Constant(FUNC_RET_REG+return_register_count),
                         ast.Constant(return_values[i].value),
                        ],node,))
                    
                if type(return_value) is Variable: #! this will probably fail trying to return points. only returning the first part
                    set_return_pointers_commands.append(Command(
                        AOE2FUNC.up_set_indirect_goal,
                        [
                            Variable({'id':return_values[i].id,'offset_index':j}),
                            ast.Constant(FUNC_RET_REG+return_register_count),
                        ],
                        node,
                    ))   
                return_register_count += 1

        return set_return_pointers_commands

    def visit_Return(self, node):
        self.generic_visit(node)
        jump_back_rules = self.make_jump_back_rules(node.lineno)
            
        set_return_pointers_commands = self.make_set_return_pointers_commands(node)
        set_return_pointers_rule = [DefRule(
            Command(AOE2FUNC.true, [], node),
            set_return_pointers_commands,
            node,
            comment="FUNC_ret_val " + str(node.lineno),
        )] if set_return_pointers_commands else []
        
        node.body = set_return_pointers_rule + jump_back_rules
        return node

    def visit_FunctionDef(self, node):
        self.current_func_def = self.func_def_dict[node.name]
        self.generic_visit(node)
        jump_back_rules = self.make_jump_back_rules(node.lineno)
        node.body = node.body + jump_back_rules
        return node    
class NumberDefrulesTR(compilerTransformer):
    def __init__(self, func_def_dict):
        super().__init__()
        self.defrule_counter = 0
        self.func_def_dict = func_def_dict
    
    def p_visit(self, node, tree_name="tree", vv=False):
        result = super().p_visit(node, tree_name, vv)
        return result, self.defrule_counter-1

    #def visit_body

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
    
    def visit_Return(self, node):
        node.first_defrule = self.defrule_counter
        node = super().visit_Return(node)
        node.last_defrule = self.defrule_counter - 1
        # raise Exception(f"{node.first_defrule=},{node.last_defrule=}")
        return node
    
    def visit_Assign(self, node):
        node.first_defrule = self.defrule_counter
        node = super().visit_Assign(node)
        node.last_defrule = self.defrule_counter - 1
        # raise Exception(f"{node.first_defrule=},{node.last_defrule=}")
        return node

    def visit_DefRule(self, node):
        self.generic_visit(node)
        node.defrule_num = self.defrule_counter
        self.defrule_counter += 1
        return node
    
    def visit_FunctionDef(self, node):
        node.first_defrule = self.defrule_counter
        self.func_def_dict[node.name].first_defrule = self.defrule_counter
        self.generic_visit(node)
        node.last_defrule = self.defrule_counter - 1
        # raise Exception(f"{node.first_defrule=},{node.last_defrule=}")
        return node

    def visit_FuncModule(self, node):
        node.first_defrule = self.defrule_counter
        self.generic_visit(node)
        node.last_defrule = self.defrule_counter - 1
        # raise Exception(f"{node.first_defrule=},{node.last_defrule=}")
        return node


class ReplaceAllJumpStatementsTransformer(compilerTransformer):
    def __init__(self, func_def_dict, rule_count):
        self.rule_count = rule_count
        self.func_def_dict = func_def_dict

    def replace_calculate_global_jump(self, node):
        for subnode in node.body:
            for i, jump in enumerate(subnode.args):
                if type(jump) is not JumpType:
                    continue
                if jump is JumpType.last_rule_in_file:
                    subnode.set_arg(i, ast.Constant(self.rule_count))
        return node

    def get_first_defrule_num(self, body_list):
        for node in ast.walk(ast.Module(body=body_list)):
            if hasattr(node, "defrule_num"):
                return node.defrule_num
        raise Exception(f"no defrule_num found in body_list line {body_list[0].lineno}")

    def calculate_jump(self, command, node):
        for i, jump in enumerate(command.args):
            if type(jump) is not JumpType:
                continue
            
            if jump is JumpType.jump_over_skip:
                command.set_arg(i, ast.Constant(node.first_defrule + 2))

            elif jump is JumpType.last_rule_after_node:
                command.set_arg(i, ast.Constant(node.last_defrule + 1))

            elif jump is JumpType.last_rule_in_node:
                command.set_arg(i, ast.Constant(node.last_defrule))

            elif jump is JumpType.test_jump_to_beginning:
                command.set_arg(i, ast.Constant(node.first_defrule + 1))

            elif jump is JumpType.test_jump_to_beginning_after_init:
                command.set_arg(i, ast.Constant(node.first_defrule + 2))
            
            elif jump is JumpType.jump_to_func:
                command.set_arg(i, ast.Constant(self.func_def_dict[node.name].first_defrule))

            elif jump is JumpType.set_return_pointer:
                command.set_arg(i, ast.Constant(node.last_defrule)) #because currently the last rule is the one that decrements and wee need to not make that part of another defrule

            elif jump is JumpType.jump_back_to_after_call:
                command.set_arg(i, ast.Constant(15900))

            elif jump is JumpType.jump_to_else:
                if type(node) is not ast.If:
                    raise Exception(f"jump_to_else must only be in if statments, not {type(node)}")
                command.set_arg(i, ast.Constant(self.get_first_defrule_num(node.orelse)))
            else:
                command.set_arg(i, ast.Constant(-1))
                raise Exception(f"{jump} not implemented yet")
    
    def replace_jump(self, node):
        subnode_lists = [node.body]
        if hasattr(node, "orelse"):
            subnode_lists.append(node.orelse)

        for subnode in chain(*subnode_lists):
            if isinstance(subnode, ast.Expr):
                subnode = subnode.value #todo:check this doesnt break anything by having defrules stacked in expr
            if isinstance(subnode, DefRule):
                for defrule_subnode in subnode.body:
                    self.calculate_jump(defrule_subnode, node)
            if isinstance(subnode, Command):
                self.calculate_jump(subnode, node)
        return node

    def visit_FunctionDef(self, node): #! check to see if it needs to dig into Expr inside the funcDef body
        self.generic_visit(node)
        return self.replace_jump(node)
    
    def visit_FuncModule(self, node):
        self.generic_visit(node)
        return self.replace_jump(node)
    
    def visit_For(self, node):
        self.generic_visit(node)
        return self.replace_jump(node)

    def visit_While(self, node):
        self.generic_visit(node)
        return self.replace_jump(node)

    def visit_If(self, node):
        self.generic_visit(node)
        return self.replace_jump(node)

    def visit_Name(self, node):
        if type(node.id) is JumpType:
            raise Exception(f"{type(node.id)} JumpType not implemented yet")
        self.generic_visit(node)
        return node

    def visit_Return(self, node): #overwriding defualt becuase we need to call replace_calculate_global_jump
        self.generic_visit(node)
        return self.replace_jump(node)

    def visit_Assign(self, node): #overwriding defualt becuase we need to call replace_calculate_global_jump
        self.generic_visit(node)
        return self.replace_jump(node)
    
    def visit_DefRule(self, node): #should run before any other ones to catch global jumps first, also caches naket defrules in bodys
        self.generic_visit(node)
        return self.replace_calculate_global_jump(node)
    

class ScopeAllVariables(compilerTransformer):
    def __init__(self):
        super().__init__()
        self.scope_level = 0
        self.current_function = None

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
        if node.id not in reserved_function_names:
            node.id = self.current_function + "." + node.id #make this a function that determins how variable names are made to be used elsewere
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
        if found and node.orelse != []:
            raise Exception(f"'disable_self' is not allowed in if statments with else clauses {node.lineno}")
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

    def get_func_def_dict(self, func_tree):
        func_def_dict = {}
        for func_def in func_tree.body:
            if not isinstance(func_def, ast.FunctionDef):
                raise Exception(f"func_def {func_def} is not a function def, its a {type(func_def)}")
            func_def_dict[func_def.name] = func_def
        return func_def_dict
    
    def compile(self, trees, vv=False):
        trees.main_tree = AstToCustomTR(
            self.command_names, self.object_names
        ).p_visit(trees.main_tree, "main_tree", vv)
        trees.func_tree = AstToCustomTR(
            self.command_names, self.object_names
        ).p_visit(trees.func_tree, "func_tree", vv)
        trees.main_tree = DisableSelfChecker().p_visit(trees.main_tree, "main_tree", vv)
        trees.func_tree = DisableSelfChecker().p_visit(trees.func_tree, "func_tree", vv)
        trees.main_tree = ReduceTR().p_visit(trees.main_tree, "main_tree", vv)
        trees.func_tree = ReduceTR().p_visit(trees.func_tree, "func_tree", vv)
        trees.func_tree = ScopeAllVariables().p_visit(trees.func_tree, "func_tree", vv)
        func_def_dict = self.get_func_def_dict(trees.func_tree)
        trees.main_tree = CompileTR(self.command_names, func_def_dict).p_visit(trees.main_tree, "main_tree", vv)
        trees.func_tree = CompileTR(self.command_names, func_def_dict).p_visit(trees.func_tree, "func_tree", vv)
        trees.main_tree = WrapInDefRules().p_visit(trees.main_tree, "main_tree", vv)  # optimize commands together into defrules
        trees.func_tree = WrapInDefRules().p_visit(trees.func_tree, "func_tree", vv)
        
        combined_tree = trees.main_tree
        combined_tree.body = (
            [
                DefRule(
                    Command(AOE2FUNC.true, [], None),
                    [
                        Command(AOE2FUNC.set_goal, [Variable({'id':FUNC_DEPTH_COUNT,'offset_index':None}), ast.Constant(15900)], None), #todo: get rid of magic number 15900, and use actualy memory allocation
                        Command(AOE2FUNC.disable_self, [], None),
                    ], None)]
            +
            combined_tree.body
            + [
                DefRule(
                Command(AOE2FUNC.true, [], None),
                [new_jump(JumpType.last_rule_in_file)],
                None,
            )]
            + trees.func_tree.body
            + [
                DefRule(
                Command(AOE2FUNC.false, [], None),
                [new_do_nothing()],
                None,
            )]
        )

        combined_tree, rule_count = NumberDefrulesTR(func_def_dict).p_visit(combined_tree, "combined_tree", vv)
        combined_tree = ReplaceAllJumpStatementsTransformer(func_def_dict, rule_count).p_visit(combined_tree, "combined_tree", vv)

        memory = Memory()

        trees.main_tree = AlocateAllMemory(memory).p_visit(
            trees.main_tree, "main_tree", vv
        )  # find out last place vars are used, and automaticaly call free on them; walk through and keep a list of node and variable pairing, then add tag
        trees.func_tree = AlocateAllMemory(memory).p_visit(
            trees.func_tree, "func_tree", vv
        )
        if vv:
            print_bordered("Memory after all alocations")
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
