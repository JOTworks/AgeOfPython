import ast
import inspect
from itertools import chain
from aenum import EnumType, Enum
from scraper import *
from scraper import AOE2FUNC, Integer, Constant, Array, Register
from scraper import aoe2scriptFunctions as aoe2scriptFunctions
from custom_ast_nodes import Command, DefRule, Variable, aoeOp, EnumNode, Constructor, JumpType, FuncModule
from Memory import Memory, FUNC_RET_REG, ARRAY_RETURN_REG, FUNC_DEPTH_COUNT, FUNC_RETURN_LENGTH, ARRAY_RETURN_PTR, FUNC_RETURN_ARRAY, ARRAY_OFFSET
from copy import copy, deepcopy
from utils import ast_to_aoe, evaluate_expression, get_enum_classes, reverse_compare_op, get_aoe2_var_types, get_list_from_return, TEMP_SUPBSTRING
from utils_display import print_bordered
from MyLogging import logger

reserved_function_names = [
    'range',
] + list(get_enum_classes().keys()) + list(get_aoe2_var_types().keys())

def new_jump(jump_type):
        return Command(AOE2FUNC.up_jump_direct, [jump_type], None)

def new_do_nothing():
        return Command(AOE2FUNC.do_nothing, [], None)


class compilerTransformer(ast.NodeTransformer):
    def generic_visit(self, node):
        try:
            return super().generic_visit(node)
        except Exception as e:
            if hasattr(node, "lineno"):
                line = node.lineno
            elif hasattr(node, "end_lineno"):
                line = node.end_lineno
            else:
                line = "No Line"
            print(f"Exception: {type(self).__name__} | Node:{type(node).__name__} | Line:{line}" )
            
            raise Exception(e)

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
    
    def visit_BinOp(self, node):
        self.generic_visit(node)
        if hasattr(node, 'body_post_left'):
            for item in node.body_post_left:
                item = self.visit(item)
        if hasattr(node, 'body_post_right'):
            for item in node.body_post_right:
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
        if not(offset_index is None or type(offset_index) is str or type(offset_index) is Variable):
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
                "ctx": node.ctx if hasattr(node, "ctx") else None,
                "offset_index": offset_index,
                "lineno": node.lineno,
                "end_lineno": node.end_lineno,
                "col_offset": node.col_offset,
                "end_col_offset": node.end_col_offset,
            }
            if hasattr(node, "slice"):
                args['slice'] = node.slice

            node = Variable(args)
        return node

    def visit_Subscript(self, node):
        self.generic_visit(node)
        if type(node.slice) is Variable:
            return self.make_variable(node, None, node.value.id)
        return self.make_variable(node, None, node.value.id)

    def visit_Attribute(self, node):
        if type(node.value) is ast.Subscript:
            raise Exception(f" [] and . not suported together, line {node.lineno}")
        self.generic_visit(node)
        if node.value.id in self.aoe2_enums:
            return EnumNode(node)
        return self.make_variable(node, node.attr, node.value.id)

    def visit_Name(self, node):
        self.generic_visit(node)
        return self.make_variable(node, None, node.id)

    def add_missing_defaults(self, func_name, args, lineno=None):

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
                logger.warning(f"{func_name} is proably using drop compareOp syntax, line {lineno}")
                return args
            else:
                if len(parameters) - len(args) != default_params_in_function:
                    raise Exception(f"you must either ommit or define ALL default varaibles, use _ for default, line {lineno}")

                for i, param in enumerate(parameters):
                    if param in parameter_type_defaults:
                        args = args[:i] + [parameter_type_defaults[param]] + args[i:]
                return args
                
        raise Exception(f"should be imporsible to ge to here, line {lineno}")
        
    def visit_UnaryOp(self, node):
        self.generic_visit(node)
        if isinstance(node.op, ast.USub) and type(node.operand) is ast.Constant:
            node.operand.value = -node.operand.value
            return node.operand
        return node

    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Name) and node.func.id in self.command_names:
            command_args = self.add_missing_defaults(node.func.id, node.args, node.lineno)
            return Command(AOE2FUNC[node.func.id], command_args, node)

        if isinstance(node.func, ast.Name) and node.func.id in self.object_names:
            return Constructor(getattr(AOE2OBJ, node.func.id), node.args, node)
        return node

    #def visit_FunctionDef(self, node):
        

class ReduceTR(compilerTransformer):
    """
    Becasue Compare and BoolOp both short circit in python, they are build as lists (left and [right_list]) instead of recurcive (lef and right) like binOps.
    Because aoe2script only short circits on implied and, and not on any defined BoolOps, we are removing all lists in favor of recursion to simplify the compiler.
    this mean the short circuting will vary based on compiler optimization step implementation
    users should not count on commands in conditionals executing!
    #todo: put back in BoolOp And Lists if they are alone in a conditional, so the user can decide when to short-curcit
    https://discord.com/channels/485565215161843714/485566694912163861/1306940924944715817
    """
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
            if compareOp.__name__ in parameters:
                node.left.append_args(ast_to_aoe(node.ops[0], compareOp))
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
        if type(node.target) is not Variable:
            raise Exception(f"AugAssign only supports Variables, not {type(node.target)}, line {node.lineno}")
        node_target_copy = Variable({ #todo: copy() would be better but cannot get it to work
            "id": node.target.id,
            "ctx": node.target.ctx,
            "offset_index": node.target.offset_index,
            "lineno": node.target.lineno,
            "end_lineno": node.target.end_lineno,
            "col_offset": node.target.col_offset,
            "end_col_offset": node.target.end_col_offset,
        })
        in_op = ast.Assign(
            targets=[node_target_copy],
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
    
    def visit_BinOp(self, node):
        node = super().visit_BinOp(node)
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

    def __init__(self, memory, const_dict, temp_variable_type_dict):
        super().__init__()
        assert isinstance(memory, Memory)
        self.memory = memory
        self.const_dict = const_dict
        for var_name, var_type in temp_variable_type_dict.items():
            if not self.memory.get(var_name):
                if var_type is not Array and type(var_type) is not EnumType: #todo: fix this later so arrays dont have to be an excpetion
                    self.memory.malloc(var_name, var_type)

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
                if var_type is AOE2OBJ.Array:
                    if len(node.value.args) != 2:
                        raise Exception(f"Array constructor needs 2 args, var type and length, not {len(node.value.args)}, line {node.lineno}")
                    if type(node.value.args[1]) is Variable: #test if this works Arrya(Integer, SIZE)
                        length = self.const_dict[node.value.args[1].id]
                    else:
                        length = node.value.args[1].value
                    self.memory.malloc(node.targets[0].id, node.value.args[0], array_length=length, is_array=True)
                else:
                    self.memory.malloc(node.targets[0].id, var_type)

        node = super().visit_Assign(node) #this one needs to happen after so it can us the Constructor before visit_Variable uses the default of Integer
        return node

    def visit_DefRule(self, node):
        if type(node.test) is list:
            for item in node.test:
                item = self.visit(item)
        else:
            node.test = self.visit(node.test)
        if type(node.body) is list:
            for item in node.body:
                item = self.visit(item)
        else:
            node.body = self.visit(node.body)
        return node
    
    def visit_Command(self, node):
        for arg in node.args:
            if type(arg) is Variable:
                arg = self.visit_Variable(arg)
        return node

    def visit_Variable(self, node):
        if node.id in self.const_dict:
            node.as_const = True
            node.memory_location = self.const_dict[node.id]
            node.memory_name = node.id
            return node #todo: maybe make these constant objects instead of variables with as_const, beucause as_const is ment for pointer
                
        if node.id is FUNC_RET_REG:
            node.memory_location = self.memory.get(node.id,0) + node.offset_index
            node.memory_name = self.memory.get_name_at_location(node.memory_location)
            return node
        
        if TEMP_SUPBSTRING in node.id:
            logger.error("temp Vars should know there type")
        
        single_slice = node.slice if hasattr(node, "slice") else None
        if type(single_slice) is Variable:
            single_slice = None #this is becuase the get function for memory should return the array start location

        if not (location := self.memory.get(node.id,node.offset_index, slice=single_slice)):
            logger.error(f"we are doing strict typing. you need to initialize {node.id}")
            self.memory.malloc(node.id, Integer)
            location = self.memory.get(node.id, node.offset_index, slice=single_slice)

        node.memory_location = location
        node.memory_name = self.memory.get_name_at_location(location)
        return node

class CompileTR(compilerTransformer):
    def __init__(self, command_names, func_def_dict, temp_var_prefix, variable_type_dict = {}, variable_array_types = {}, variable_array_lengths = {}):
        super().__init__()
        self.temp_var_prefix = str(temp_var_prefix) + TEMP_SUPBSTRING
        self.command_names = command_names
        self.parent_map = {}
        self.variable_types = variable_type_dict
        self.variable_array_lengths = variable_array_lengths
        self.variable_array_types = variable_array_types
        self.temp_var_counter = 0
        self.func_def_dict = func_def_dict
        self.current_func_def = None
        self.aoe2_var_types = get_aoe2_var_types()
        self.array_return_offset = 0
        self.loop_stack = []

    
    def get_temp_variable_type_dict(self):
        return self.variable_types #todo: only add function def args, as they are not using constructors. but have type still
        #return {k:v for k, v in self.variable_types.items() if k.startswith(self.temp_var_prefix)}
    
    def get_next_temp_var(self):
        self.temp_var_counter += 1
        return f"{self.temp_var_prefix}_{self.temp_var_counter}"

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
        func_name = node.func.id.split(".")[-1] #todo: check if we want to keep nested function names with the full set, or only the last one
        if func_name in reserved_function_names:
            return node
        func_def_node = self.func_def_dict[func_name]
        if func_name in reserved_function_names:
            return node
        func_call_module = FuncModule(func_name, node.args, node)
        
        
        func_depth_incromenter = DefRule(
            Command(AOE2FUNC.true, [], None),
            [Command(AOE2FUNC.up_modify_goal, [Variable({'id':FUNC_DEPTH_COUNT,'offset_index':None}), mathOp.add, self.const_constructor(1)], node)],
            node,
            comment="FUNC_dept_inc " + str(node.lineno),
        )

        set_return_rule_pointer = DefRule(
            Command(AOE2FUNC.true, [], None),
            [Command(AOE2FUNC.up_set_indirect_goal, 
                     [Variable({'id':FUNC_DEPTH_COUNT,'offset_index':None}), JumpType.set_return_pointer], node)], 
            node,
            comment="FUNC_ret_set " + str(node.lineno),
        )

        func_depth_decromenter = DefRule(
            Command(AOE2FUNC.true, [], None),
            [Command(AOE2FUNC.up_modify_goal, [Variable({'id':FUNC_DEPTH_COUNT,'offset_index':None}), mathOp.sub, self.const_constructor(1)], None)],
            node,
            comment="FUNC_depth_dec " + str(node.lineno),
        )

        asign_func_arg_commands = []
        for i, arg in enumerate(node.args):
            asign_func_arg_commands += self.create_modify_commands(
                func_def_node.args.args[i],
                ast.Eq,
                arg,
                )
        if len(asign_func_arg_commands) > 0:
            asign_func_args = DefRule(
                    Command(AOE2FUNC.true, [], None),
                    asign_func_arg_commands,
                    node,
            )
        else:
            asign_func_args = None

        jump_to_func = DefRule(
            Command(AOE2FUNC.true, [], None),
            [Command(AOE2FUNC.up_jump_direct, [JumpType.jump_to_func], node)],
            node,
            comment="FUNC_jump " + str(node.lineno),
        )


        func_call_module.body = []
        func_call_module.body.append(func_depth_incromenter)
        func_call_module.body.append(set_return_rule_pointer)
        if asign_func_args:
            func_call_module.body.append(asign_func_args)
        func_call_module.body.append(jump_to_func)
        func_call_module.body.append(func_depth_decromenter)

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
    
    def visit_Continue(self, node):
        #continue would simply jump to incrementer
        #break would jump to one minus test
        if len(self.loop_stack) == 0:
            raise Exception(f"break outside of loop, line {node.lineno}")
        node = DefRule(
            Command(AOE2FUNC.true, [], None),
            [new_jump(JumpType.jump_continue)],
            node,
            comment="Continue " + str(node.lineno),
        )
        return node
    
    def visit_Break(self, node):
        #continue would simply jump to incrementer
        #break would jump to one minus test
        if len(self.loop_stack) == 0:
            raise Exception(f"break outside of loop, line {node.lineno}")
        node = DefRule(
            Command(AOE2FUNC.true, [], None),
            [new_jump(JumpType.jump_break)],
            node,
            comment="Break " + str(node.lineno),
        )
        return node

    def visit_For(self, node, parent, in_field, in_node):
        self.loop_stack.append(node)
        """
        jump to end automaticaly, then jump to beggining if conditions are true
        same as if, only remove the one jump that skips the conditional
        """
        if type(node.iter) is not ast.Call or node.iter.func.id != "range":
            raise Exception(f"for loops only support range, not {node.iter}, line {node.lineno}")
        if not self.get_var_type(node.target): #becasue we need to asign itr in for loop before we get to the visit_assign where it would happen natural
            self.set_var_type(node.target.id, Integer) #I is dumb
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
            Command(AOE2FUNC.up_compare_goal, [node.target, op, stop], None),
            [new_jump(JumpType.test_jump_to_beginning_after_init)],
            None,
            comment="FOR test " + str(node.lineno),
        )
        init = DefRule(
            Command(AOE2FUNC.true, [], None),
            self.create_modify_commands(node.target, ast.Eq, start),
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
            [Command(AOE2FUNC.up_modify_goal, [node.target, mathOp.add, step], None)],
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
        self.loop_stack.pop()
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
        skip_orelses_if_true = DefRule(
            Command(AOE2FUNC.true, [], None),
            [new_jump(JumpType.last_rule_after_node)],
            node_copy_with_short_offset(node, 2),
            comment="IF skip_orelses_if_true " + str(node.lineno),
        )

        node.body = [
            test,
            skip,
        ] + node.body

        if node.orelse != []: 
            node.body.append(skip_orelses_if_true)

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
        elif left_type is Variable and right_type in (ast.Constant, Variable, EnumNode):
            compare_comand = Command(
                AOE2FUNC.up_compare_goal,
                [node.left, ast_to_aoe(type(node.ops[0]), compareOp), node.comparators[0]],
                node,
            )
        elif left_type in (ast.Constant, EnumNode) and right_type is Variable:
            compare_comand = Command(
                AOE2FUNC.up_compare_goal,
                [
                    node.comparators[0],
                    reverse_compare_op(ast_to_aoe(type(node.ops[0], compareOp))),
                    node.left,
                ],
                node,
            )
        else:
            raise Exception(
                f"visit_compare Error! {type(node.left)=} and {type(node.comparators[0])=}, line {node.lineno}"
            )
        return compare_comand

    def check_type_compatible(list_vars_1, list_vars_2, lineno = "unknown"): #todo: scurrently not used anywhere
        if len(list_vars_1) != len(list_vars_2):
            raise Exception(
                f"var lists are not the same length {len(list_vars_1)} and {len(list_vars_2)}, line {lineno}"
            )
        for var_1, var_2 in zip(list_vars_1, list_vars_2):
            var_1_name, var_1_size = var_1
            var_2_name, var_2_size = var_2
            if var_1_size is not var_2_size:
                raise Exception(
                    f"var types are not compatible {var_1_size} and {var_2_size}, line {lineno}"
                )

    def tupleify(self, node):
        if type(node) is ast.Tuple:
            return node
        elif type(node) in [Variable, ast.BinOp]:
            if node.var_name() == FUNC_RET_REG:
                length = FUNC_RETURN_LENGTH
            else:
                length = self.get_length(node)
            elts = [Variable({'id':node.var_name(),'offset_index':i}) for i in  range(length)]
        elif type(node) is FuncModule:
            return_types = self.get_function_return_types(node.name)
            elts = [
                Variable({'id':FUNC_RET_REG,'offset_index':None, 'lineno':node.lineno}, )
                for _ in return_types
            ]
        else:
            raise Exception(f"cannot tupleify {type(node)}, line {node.lineno}")
        
        return ast.Tuple(elts=elts)
    
    def get_aoe2_modify_function(self, node):
        if type(node) in [Variable, ast.arg, ast.Return]:
            return AOE2FUNC.up_modify_goal
        if type(node) is EnumNode and type(node.enum) is SN: #used to say type(node) in [SN, SnId] but i think that never worked?
            return AOE2FUNC.up_modify_sn
        if type(node) is ast.Constant:
            raise Exception(
                f"you cannot modify a constant {node.value}, line {node.lineno}"
            )
        else:
            raise Exception(
                f"you cannot modify a {type(node)}, line {node.lineno}"
            )

    def create_modify_commands(self, node_1, op, node_2, reset_array_offset=True):
        #! NEED TO FINIISH ASIGNMENTS
        #todo: implemet constructors taking args, in visit_Assign (make it a one time asign with disable_rule()
        if reset_array_offset:
            self.array_return_offset = 0

        modify_commands = [] 
        
        #Right side set length
        if type(node_2) is Variable and node_2.offset_index is not None:
            node_2_length = 1 #all basic type offset attr aka .x or .locallsit are size 1 elements
        elif type(node_2) is Variable and node_2.var_name() == FUNC_RET_REG:
            node_2_length = None
        elif type(node_2) is ast.Tuple:
            node_2_length = len(node_2.elts)
        elif type(node_2) is FuncModule:
            return_types = self.get_function_return_types(node_2.name)
            if len(return_types) == 1:
                node_2_length = self.get_length(return_types[0])
            else:
                node_2_length = len(return_types)
        else:
            node_2_length = self.get_length(node_2)

        #Left side set length
        if type(node_1) is not ast.Tuple and self.get_var_type(node_1) is None:
            self.set_var_type(node_1.var_name(), self.get_var_type(node_2))

        if type(node_1) is Variable and node_1.offset_index is not None:
            node_1_length = 1 #all basic type offset attr aka .x or .locallsit are size 1 elements
        elif type(node_1) is ast.Tuple:
            node_1_length = len(node_1.elts)
        elif type(node_1) is ast.Return: 
            node_1_length = node_2_length #assuming bad returns are caught in Asserter
        else:
            node_1_length = self.get_length(node_1)
        
        #check lengths
        if (node_1_length and node_2_length 
            and node_1_length != node_2_length
            and node_2.var_name() != FUNC_RET_REG):
            raise Exception(
                f"var types are not compatible {node_1_length} and {node_2_length}, line UNKONWN"
            )
        else:
            length = node_1_length if node_1_length else node_2_length

        
        #recursion shortcut
        if type(node_2) is FuncModule and len(return_types) == 1:
            modify_commands += self.create_modify_commands(node_1, op, Variable({'id':FUNC_RET_REG,'offset_index':None, 'lineno':node_1.lineno}), reset_array_offset=False)
        #recursion   
        elif (type(node_1) is ast.Tuple 
        or type(node_2) is ast.Tuple
        or type(node_2) is FuncModule and len(return_types) > 1
        ):
            tupled_node_1 = self.tupleify(node_1)
            tupled_node_2 = self.tupleify(node_2)
            for i in range(length):
                if i > len(tupled_node_1.elts) - 1 or i > len(tupled_node_2.elts) - 1:
                    raise Exception(f"tupled_node 1 or 2 has no {i}th element, line {node_1.lineno}")
                modify_commands += self.create_modify_commands(tupled_node_1.elts[i], op, tupled_node_2.elts[i], reset_array_offset=False)
        #base case
        else:
            modify_commands += self.create_single_modify_commands(node_1, op, node_2, length)
        return modify_commands
    
    def create_single_modify_commands(self, node_1, op, node_2, length):
        modify_commands = []
        modify_func = self.get_aoe2_modify_function(node_1)
        for i in range(length):
            #if its the full basic type getting coppied
            left_offset_index = i
            right_offset_index = i
            left_slice = node_1.slice if hasattr(node_1, 'slice') else None
            right_slice = node_2.slice if hasattr(node_2, 'slice') else None
            
            #should only happen if length is 1, pulls the one piece of the basic type
            if type(node_1) is Variable and node_1.offset_index is not None:
                if length != 1:
                    raise Exception(f"basic type attr should only by length 1, not {length}, line {node_1.lineno}")
                left_offset_index = node_1.offset_index
                left_slice = node_1.slice
            if type(node_2) is Variable and node_2.offset_index is not None:
                if length != 1:
                    raise Exception(f"basic type attr should only by length 1, not {length}, line {node_1.lineno}")
                right_offset_index = node_2.offset_index
                right_slice = node_2.slice

            #for when we are using the amourphous func_ret_reg array devoid of types
            if node_1.var_name() == FUNC_RET_REG:
                left_offset_index = self.array_return_offset
                left_slice = None
                self.array_return_offset += 1
            if node_2.var_name() == FUNC_RET_REG:
                right_offset_index = self.array_return_offset
                right_slice = None
                self.array_return_offset += 1

            if modify_func is AOE2FUNC.up_modify_sn: #todo: make sure that right side SN works (ie x = SN.food_gathereres)
                left = node_1
            else:
                left = Variable({'id':node_1.var_name(),'offset_index':left_offset_index, 'slice':left_slice}) #! EnumNode should not become a variable in this function
            if modify_func is AOE2FUNC.up_modify_sn or type(node_2) is EnumNode:
                right = node_2
            else:
                right = Variable({'id':node_2.var_name(),'offset_index':right_offset_index, 'slice':right_slice})
            if type(node_2) is ast.Constant:
                right = node_2
            
            #ARRAYS #todo: optimization, add for i in array: and make it just add element_size each time when accessing
            if hasattr(node_2, 'slice') and node_2.slice is not None:
                if type(node_2.slice) in [Variable, str]: #getting array element
                    modify_commands += self.create_set_array_ptr_commands(node_2, right_offset_index)
                    modify_commands.append( Command( #todo: double check you can use the same variable for both sides of up_get_indirect_goal, you can but may not want to for optimizations later
                        AOE2FUNC.up_get_indirect_goal,
                        [Variable({'id':ARRAY_RETURN_PTR,'offset_index':None}), Variable({'id':ARRAY_RETURN_REG,'offset_index':None})],
                        node_2,
                    ))
                    right = Variable({'id':ARRAY_RETURN_REG,'offset_index':None})

            if hasattr(node_1, 'slice') and node_1.slice is not None:
                if type(node_1.slice) in [Variable, str]: #setting array element
                    if type(op) is not ast.Eq:
                        raise Exception(f"cannot use {op} on Array asignments, line {node_1.lineno}")
                    modify_commands += self.create_set_array_ptr_commands(node_1, left_offset_index)
                    modify_func = AOE2FUNC.up_set_indirect_goal
                    left = Variable({'id':ARRAY_RETURN_PTR,'offset_index':None})

            if modify_func in [AOE2FUNC.up_set_indirect_goal, AOE2FUNC.up_get_indirect_goal]:
                args = [left, right]
            else: 
                args = [left, ast_to_aoe(op, mathOp), right]
            modify_commands.append(Command(modify_func, args, None))

        return modify_commands

    def create_set_array_ptr_commands(self, node, offset_index):
        if node.offset_index is not None:
            raise Exception(f"need to add code here, but currenlty array nodes dont have offset_indexes?, line {node.lineno}")
        if hasattr(node.slice, 'slice') and node.slice.slice is not None:
            raise Exception(f"slicing not supprted in slices, line {node.lineno}")
        if node.offset_index and self.get_var_type(node.offset_index) not in [Integer, Register]:
            raise Exception(f"array [] must be [Integer, Register] not {self.get_var_type(node.offset_index)}, line {node.lineno}")
        modify_commands = []
        #set to begining of array
        node_copy = Variable({ #todo: copy() would be better but cannot get it to work
            "id": node.id,
            "ctx": node.ctx,
            "offset_index": None,
            "lineno": node.lineno,
            "end_lineno": node.end_lineno,
            "col_offset": node.col_offset,
            "end_col_offset": node.end_col_offset,
            "as_const": True, #set this up so it looks at the memory location and not the values
        })
        modify_commands.append( Command(
            AOE2FUNC.up_modify_goal,
            [Variable({'id':ARRAY_RETURN_PTR,'offset_index':None}), mathOp.eql, node_copy],
            None,
        ))
        #add offset
        modify_commands.append( Command(
                AOE2FUNC.up_modify_goal,
                [Variable({'id':ARRAY_RETURN_PTR,'offset_index':None}), mathOp.add, ast.Constant(offset_index)],
                node,
            ))
        #calculate slice
        modify_commands.append( Command(
            AOE2FUNC.up_modify_goal,
            [Variable({'id':ARRAY_OFFSET,'offset_index':None}), mathOp.eql, ast.Constant(value=self.get_array_element_size(node))],
            node,
            ))
        modify_commands.append( Command(
            AOE2FUNC.up_modify_goal,
            [Variable({'id':ARRAY_OFFSET,'offset_index':None}), mathOp.mul, node.slice],
            node,
            ))
        #add slice
        modify_commands.append( Command(
            AOE2FUNC.up_modify_goal,
            [Variable({'id':ARRAY_RETURN_PTR,'offset_index':None}), mathOp.add, Variable({'id':ARRAY_OFFSET,'offset_index':None})],
            node,
        ))
        return modify_commands

    def get_array_element_size(self, node):
        if not self.is_array(node):
            raise Exception(f"get_array_element_size only works on arrays, not {self.get_var_type(node)}, line {node.lineno}")
        name = node.var_name()
        if name in self.variable_array_types:
            return self.variable_array_types[name].length
        else:
            raise Exception(f"array {name} not in variable_array_types, line {node.lineno}")


    def set_array_var_type(self, var_name, var_type):
        cleaned_var_type = None
        if var_name in self.variable_array_types:
            raise Exception(f"var {var_name} already has a type {self.variable_array_types[var_name]}, line unknown")
        elif aoe2_vartype := self.aoe2_var_types.get(var_type, None):
             cleaned_var_type = aoe2_vartype
        elif aoe2_vartype := self.aoe2_var_types.get(var_type.__name__, None):
             cleaned_var_type = aoe2_vartype
        
        if cleaned_var_type:
            self.variable_array_types[var_name] = cleaned_var_type

        else:
            raise Exception("booooooo!")

    def set_var_type(self, var_name, var_type):
        if type(var_name) is not str:
            raise Exception(f"var_name must be a string, not {type(var_name)}, line {var_name.lineno}")

        cleaned_var_type = None
        if var_name in self.variable_types:
            raise Exception(f"var {var_name} already has a type {self.variable_types[var_name]}, line unknown")
        elif aoe2_vartype := self.aoe2_var_types.get(var_type, None):
             cleaned_var_type = aoe2_vartype
        elif aoe2_vartype := self.aoe2_var_types.get(var_type.__name__, None):
             cleaned_var_type = aoe2_vartype
        elif type(var_type) is EnumType:
             cleaned_var_type = var_type
        if cleaned_var_type:
            self.variable_types[var_name] = cleaned_var_type

        else:
            raise Exception("booooooo!")

    def is_array(self, node):
        var_name = node.var_name()
        if type(node) in [ast.Constant,Constant]:
            return False
        if var_name in self.variable_types:
            var_type = self.variable_types[var_name]
        else:
            raise Exception(f"var {var_name} not in defined, line {node.lineno}")
        if var_type is Array:
            return True
        return False    

    def get_var_type(self, node):
        if type(node) is EnumNode:
            return type(node.enum)
        if type(node) is ast.Constant:
            if type(node.value) is int:
                return Integer
            #elif type(node.value) is bool:
            #    return Boolean
            #elif type(node.value) is str:
            #    return String
            else:
                raise Exception(f"Constant of type {type(node.value)} not supported, line {node.lineno}")
        elif type(node) is FuncModule:
            function_return_types = self.get_function_return_types(node.name)
            if len(function_return_types) == 1:
                return function_return_types[0]
            return self.tupleify
        var_name = node.var_name()
        
        if hasattr(node, 'offset_index') and node.offset_index is not None: #all subsection are currently single regesters
            return Register

        if hasattr(node, 'slice') and node.slice is not None:
            return self.variable_array_types.get(var_name, None)

        if var_name in self.variable_types:
            return self.variable_types[var_name]
        
        return # not in dictionary

    def get_length(self, node):
        if type(node) is ast.Tuple:
            length = len(node.elts)
        elif type(node) is EnumNode:
            length = 1
        elif hasattr(node, 'length'):
            length = node.length
        else:
            var_type = self.get_var_type(node)
            if not var_type:
                raise Exception(f"var {node.var_name()} not defined, line {node.lineno}")
            if self.is_array(node) is Array:
                if slice is None:
                    length = self.variable_array_lengths[node.var_name()] * self.get_length(self.variable_array_types[node.var_name()])
                else:
                    if not (array_type := self.variable_array_types.get(node.var_name())):
                        raise Exception(f"array {node.var_name()} not defined, line {node.lineno}")
                    length = self.get_length(array_type)
            elif type(var_type) is EnumType:
                length = 1
            else:
                length = var_type.length
        if type(length) is property:
            raise Exception(f"length is a property, not a value, line {node.lineno}")
        return length

    def visit_BinOp(self, node, parent, in_field, in_node):
        # will be 2CT and needs to be up-goal-modify # ALWAYS use temperary vars for this
        #BINOP: #tempVar-1 size(1)
        node = super().visit_BinOp(node)
        node.temp_var_name = self.get_next_temp_var()
        
        if not self.get_length(node.left) == self.get_length(node.right):
            raise Exception(f"binop left [{self.get_var_type(node.left)}] and right [{self.get_var_type(node.right)}] size are not the same, line {node.lineno}")
        
        node.body_post_left = [DefRule(
            Command(AOE2FUNC.true, [], None),
            self.create_modify_commands(
                Variable({'id':node.var_name(),'offset_index':None}), #var_name()
                ast.Eq(),
                node.left
            ),
            node
        )]
        
        node.body_post_right = [DefRule(
                Command(AOE2FUNC.true, [], None),
                self.create_modify_commands(
                Variable({'id':node.var_name(),'offset_index':None}), #var_name()
                node.op,
                node.right
            ),
            node,
        )]
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
            or (len(node.values) == 1 and node.op.__doc__ == ast.Not.__doc__)
        ):
            raise Exception(f"BoolOp must have 2 values not {len(node.values)}")

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
        if isinstance(test, ast.Constant):
            if test.value == True:
                return Command(AOE2FUNC.true, [], test)
            elif test.value == False:
                return Command(AOE2FUNC.false, [], test)
            else:
                raise Exception(f"test cant be a constant unless its 1 or 0 {test.value}, line {test.lineno}")
        self.generic_visit(test)
        return test

    def visitAugAssign(self, node):
        raise Exception("AugAssign should all be parced out by ReduceTR")

    def visit_Assign(self, node, parent, in_field, in_node):
        #! clean up this function from all the leftover code

        self.generic_visit(node)

        msg = None
        node.body = []
        assign_commands = []
        target = node.targets[0]

        #constructor
        if type(node.value) is Constructor:
            self.set_var_type(target.var_name(), node.value.func.id.name)
            if node.value.func.id.name is Array.__name__:
                if len(node.value.args) != 2:
                    raise Exception(f"array constructor must have 2 args, not {len(node.value.args)}, line {node.lineno}")
                if type(node.value.args[1]) is Variable:
                    if const_value := self.variable_types.get(node.value.args[1].id, None) is Constant:
                        self.variable_array_lengths[target.var_name()] = const_value
                elif type(node.value.args[1]) is ast.Constant:  
                    self.variable_array_lengths[target.var_name()] = node.value.args[1].value #!add 2 checks to make sure you initilize an array correctly
                else:
                    raise Exception(f"array constructor second arg must be a Variable of a Constant or a Constant, not {type(node.value.args[1])}, line {node.lineno}")
                self.set_array_var_type(target.var_name(), node.value.args[0].id)
                #todo:fix array initilization
            else: #asignments for non array constructors that take arms
                if len(node.value.args) != 0:
                    if len(node.value.args) == 1:
                        right = node.value.args[0]
                    else:
                        right = ast.Tuple(elts=node.value.args)
                    assign_commands += self.create_modify_commands(target, ast.Eq(), right)
                    assign_commands.append(Command(AOE2FUNC.disable_self, [], node))
        else:
            assign_commands += self.create_modify_commands(target, ast.Eq(), node.value)

        # multiple targets (ei x = y = 12)
        if len(node.targets) > 1:
            for i in range(1, len(node.targets)):
                assign_commands += self.create_modify_commands(node.targets[i], ast.Eq(), target)
        
        #Return it all
        if len(assign_commands) == 0:
            logger.warning("no assign commands, line " + str(node.lineno))
            node.body = []
        else:
            node.body = [DefRule(
                    Command(AOE2FUNC.true, [], None),
                    assign_commands,
                    node,
                    '' if msg is None else msg + " " + str(node.lineno),
                )]
        return node

    def make_jump_back_rules(self, lineno):
        set_jump_back = DefRule(
            Command(AOE2FUNC.true, [], None),
            [Command(AOE2FUNC.up_get_indirect_goal, [Variable({'id':FUNC_DEPTH_COUNT,'offset_index':None}), FUNC_RETURN_ARRAY], None)],
                None,
                comment="FUNC_set_jump " + str(lineno),
        ) 
        jump_back_to_after_call = DefRule(
            Command(AOE2FUNC.true, [], None),
            [new_jump(JumpType.jump_back_to_after_call)],
            None,
            comment="FUNC_return " + str(lineno),
        )
        return [set_jump_back, jump_back_to_after_call]

    def get_function_return_types(self, function_name):
        args = get_list_from_return(self.func_def_dict[function_name].returns)
        arg_types = []
        for arg in args:
            if arg.id in self.aoe2_var_types:
                arg_types.append(self.aoe2_var_types[arg.id])
            else:
                raise Exception(f"function {function_name} has a return type of {arg.id} that is not in the aoe2_var_types, line {self.lineno}")
        return arg_types
    
    def make_set_return_reg_commands(self, node):
        return_values = get_list_from_return(node.value)
        funct_returns_values = get_list_from_return(self.current_func_def.returns)
        if len(return_values) != len(funct_returns_values):
            raise Exception(f"function {self.current_func_def.name} has {len(funct_returns_values)} returns, not {len(return_values)}, line {node.lineno}")
        
        set_ret_commands = []
        self.array_return_offset = 0
        for ret_val in return_values:
            set_ret_commands += self.create_modify_commands(node, ast.Eq, ret_val, reset_array_offset=False)


        return set_ret_commands

    def visit_Return(self, node):
        self.generic_visit(node)
        jump_back_rules = self.make_jump_back_rules(node.lineno)
            
        set_return_pointers_commands = self.make_set_return_reg_commands(node)
        set_return_pointers_rule = [DefRule(
            Command(AOE2FUNC.true, [], None),
            set_return_pointers_commands,
            node,
            comment="FUNC_ret_val " + str(node.lineno),
        )] if set_return_pointers_commands else []
        
        node.body = set_return_pointers_rule + jump_back_rules
        return node

    def visit_FunctionDef(self, node):
        self.current_func_def = self.func_def_dict[node.name]
        self.get_function_return_types
        for arg in node.args.args:
            if not hasattr(arg, 'annotation') or arg.annotation is None:
                raise Exception(f"function {node.name} arg {arg.arg} has no annotation, line {node.lineno}")
            #self.set_var_type(arg.arg,arg.annotation.id) currently already done in the get_function_param_types()
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
        self.loop_stack = []

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
                command.set_arg(i, FUNC_RETURN_ARRAY)

            elif jump is JumpType.jump_to_else:
                if type(node) is not ast.If:
                    raise Exception(f"jump_to_else must only be in if statments, not {type(node)}")
                command.set_arg(i, ast.Constant(self.get_first_defrule_num(node.orelse)))

            elif jump is JumpType.jump_break: #break would jump to one minus test
                if len(self.loop_stack) == 0:
                    raise Exception(f"jump_break must be in a For loop, not {type(node)}")
                command.set_arg(i, ast.Constant(self.loop_stack[-1].last_defrule + 1))

            elif jump is JumpType.jump_continue: #continue would simply jump to incrementer
                if len(self.loop_stack) == 0:
                    raise Exception(f"jump_break must be in a For loop, not {type(node)}")
                command.set_arg(i, ast.Constant(self.loop_stack[-1].last_defrule - 1))
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

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        return self.replace_jump(node)
    
    def visit_FuncModule(self, node):
        self.generic_visit(node)
        return self.replace_jump(node)
    
    def visit_For(self, node):
        self.loop_stack.append(node)
        self.generic_visit(node)
        result = self.replace_jump(node)
        self.loop_stack.pop()
        return result
        

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
        self.globalized_variables = {} #function name -> list of variables

    def visit_Global(self, node):
        for name in node.names:
            if not self.current_function:
                raise Exception(f"global can only be used inside a function, line {node.lineno}")
            if not self.globalized_variables.get(self.current_function, None):
                self.globalized_variables[self.current_function] = [name]
            else:
                self.globalized_variables[self.current_function].append(name)
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        if self.current_function is not None:
            raise Exception(
                f"current_function is {self.current_function}, you cannot define {node.name if node else 'a function'} in a function"
            )
        self.current_function = node.name
        for arg in node.args.args:
            if arg.arg not in self.globalized_variables.get(self.current_function, []):
                if "." in arg.arg:
                    raise Exception(f"arg {arg.arg.id} already has a '.', line {node.lineno}")
                arg.arg = self.current_function + "." + arg.arg
        self.generic_visit(node)
        self.current_function = None
        return node

    def visit_Variable(self, node):
        if hasattr(node, 'offset_index') and type(node.offset_index) is Variable: #visiting variables inside array []
            raise Exception(f"Depricated, should not hit this, useing array [] instead of offset {node.offset_index}, line {node.lineno}")
            node.offset_index = self.visit_Variable(node.offset_index)
        self.generic_visit(node)
        if hasattr(node, 'slice') and type(node.slice) is Variable:
            node.slice = self.visit_Variable(node.slice)
        if node.id not in reserved_function_names and node.id not in self.globalized_variables.get(self.current_function, []):
            if "." in node.id:
                raise Exception(f"already has a '.', {node.id}, line {node.lineno}")
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
        self.aoe2_var_types = get_aoe2_var_types()
        return

    def get_func_def_dict(self, func_tree):
        func_def_dict = {}
        for func_def in func_tree.body:
            if not isinstance(func_def, ast.FunctionDef):
                raise Exception(f"func_def {func_def} is not a function def, its a {type(func_def)}")
            func_def_dict[func_def.name] = func_def
        return func_def_dict
    
    def get_dict_from_const_tree(self, const_tree):
        const_dict = {}
        for const in const_tree.body:
            if not isinstance(const, ast.Assign):
                raise Exception(f"func_def {const} is not a ast.Assign, its a {type(const)}")
            const_dict[const.targets[0].id] = const.value.args[0].value
        return const_dict

    def get_function_param_types(self, func_tree):
        enum_classes = get_enum_classes()
        #enum_class_var_type_dict = {
        #    ObjectId
        #}
        set_var_type = {}
        for node in func_tree.body:
            for arg in node.args.args:
                var_name, var_type = arg.arg, arg.annotation.id #todo: allow annotations of aoe2params, aka ObjectId instead of just Integer
                if not hasattr(arg, 'annotation') or arg.annotation is None:
                    raise Exception(f"function {node.name} arg {arg.arg} has no annotation, line {node.lineno}")
                if var_type in enum_classes:
                    cleaned_var_type = enum_classes[var_type]
                    #raise Exception(f"Not yet supporting AOE2Script Parameter like {var_type} types as annotations, Use basic types, {node.lineno}")
                elif aoe2_vartype := self.aoe2_var_types.get(var_type, None):
                    cleaned_var_type = aoe2_vartype
                elif aoe2_vartype := self.aoe2_var_types.get(var_type.__name__, None):
                    cleaned_var_type = aoe2_vartype
                set_var_type[var_name] = cleaned_var_type
        return set_var_type
        
    def get_constant_param_types(self, const_tree):
        set_var_type = {}
        for node in const_tree.body:
            for target in node.targets:
                set_var_type[target.var_name()] = Constant
        return set_var_type
    
    def compile(self, trees, vv=False):

        trees.const_tree = AstToCustomTR(
            self.command_names, self.object_names
        ).p_visit(trees.const_tree, "const_tree", vv)

        trees.main_tree = AstToCustomTR(
            self.command_names, self.object_names
        ).p_visit(trees.main_tree, "main_tree", vv)
        trees.func_tree = AstToCustomTR(
            self.command_names, self.object_names
        ).p_visit(trees.func_tree, "func_tree", vv)
        trees.main_tree = DisableSelfChecker().p_visit(trees.main_tree, "main_tree", vv)
        trees.func_tree = DisableSelfChecker().p_visit(trees.func_tree, "func_tree", vv)
        #is after astToCustom so it has Command objects to compare with in visit_compare()
        trees.main_tree = ReduceTR().p_visit(trees.main_tree, "main_tree", vv)
        trees.func_tree = ReduceTR().p_visit(trees.func_tree, "func_tree", vv)

        trees.func_tree = ScopeAllVariables().p_visit(trees.func_tree, "func_tree", vv)
        func_def_dict = self.get_func_def_dict(trees.func_tree)


        function_param_and_constant_types = self.get_function_param_types(trees.func_tree) | self.get_constant_param_types(trees.const_tree)
        main_compiler = CompileTR(self.command_names, func_def_dict, temp_var_prefix="T", variable_type_dict = function_param_and_constant_types)
        trees.main_tree = main_compiler.p_visit(trees.main_tree, "main_tree", vv)
        func_compiler = CompileTR(self.command_names, func_def_dict, temp_var_prefix="F", variable_type_dict = main_compiler.get_temp_variable_type_dict() | function_param_and_constant_types, variable_array_lengths = main_compiler.variable_array_lengths, variable_array_types = main_compiler.variable_array_types)
        trees.func_tree = func_compiler.p_visit(trees.func_tree, "func_tree", vv)
        
        temp_variable_type_dict = main_compiler.get_temp_variable_type_dict() | func_compiler.get_temp_variable_type_dict()
        
        trees.main_tree = WrapInDefRules().p_visit(trees.main_tree, "main_tree", vv)  # optimize commands together into defrules
        trees.func_tree = WrapInDefRules().p_visit(trees.func_tree, "func_tree", vv)
        


        combined_tree = trees.main_tree
        combined_tree.body = (
            [
                DefRule(
                    Command(AOE2FUNC.true, [], None),
                    [
                        Command(AOE2FUNC.set_goal, [Variable({'id':FUNC_DEPTH_COUNT,'offset_index':None}), FUNC_RETURN_ARRAY], None), #todo: get rid of magic number 15900, and use actualy memory allocation
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
        const_dict = self.get_dict_from_const_tree(trees.const_tree)
        combined_tree = AlocateAllMemory(memory, const_dict, temp_variable_type_dict).p_visit(
            combined_tree, "combined_tree", vv
        )

        #trees.main_tree = AlocateAllMemory(memory, const_dict, ).p_visit(
        #    trees.main_tree, "main_tree", vv
        #)  # find out last place vars are used, and automaticaly call free on them; walk through and keep a list of node and variable pairing, then add tag
        #trees.func_tree = AlocateAllMemory(memory, const_dict, ).p_visit(
        #    trees.func_tree, "func_tree", vv
        #)
        if vv:
            print_bordered("Memory after all alocations")
            memory.print_memory()
        
        return combined_tree, memory


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
