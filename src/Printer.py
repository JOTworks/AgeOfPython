import ast
from Compiler import Command, Variable, aoeOp
from scraper import *
from scraper import mathOp, compareOp, Strenum, typeOp
from utils_display import read_file_as_string
from colorama import Fore, Back, Style
import re
from MyLogging import logger
from utils import get_enum_classes
from time import time
from pprint import pprint

class DefRulePrintVisitor(ast.NodeVisitor):
    def __init__(self, final_list, const_tree = [], NO_FILE=False, TEST=True):
        super().__init__()
        self.final_list = final_list
        self.NO_FILE = NO_FILE
        self.enum_classes = get_enum_classes()
        self.TEST = TEST
        self.def_const_list = set()
        self.time_tracker = {"visit_DefRule": 0, "visit_defconst": 0, "visit_FunctionDef": 0, "visit_aoeOp": 0, "visit_Command": 0, "add_def_consts": 0, "evaluate_enum": 0}
        self.call_tracker = {"visit_DefRule": 0, "visit_defconst": 0, "visit_FunctionDef": 0, "visit_aoeOp": 0, "visit_Command": 0, "add_def_consts": 0, "evaluate_enum": 0,
                             "visit_if": 0, "visit_Return": 0, "visit_Assign": 0}
        try:
            for node in const_tree.body:
                name = node.targets[0].id
                value = node.value.args[0].value
                self.def_const_list.add(name + " " + str(value))
        except IndexErrors:
            raise Exception(f"defined Constant has no parameter, line {node.lineno}")
        

    def visit_if(self, node):
        self.call_tracker["visit_if"] += 1
        """
        so we dont print the test and other metadata in visit
        """
        for item in node.body:
            self.visit(item)

    def visit_Return(self, node):
        self.call_tracker["visit_Return"] += 1
        for item in node.body:
            self.visit(item)
        self.generic_visit(node) #!sus should we be going through twice?
    
    def visit_BinOp(self, node):
        self.visit(node.left)
        for item in node.body_post_left:
            self.visit(item) 
        self.visit(node.right)
        for item in node.body_post_right:
            self.visit(item)

    def visit_Assign(self, node): #todo: when refactored i will need to print temp math first, function calls, then asigns
        self.call_tracker["visit_Assign"] += 1
        self.generic_visit(node) #!sus should we be going through twice?
        for item in node.body: #currently this should be return value And assigns
            self.visit(item)


    def visit_FunctionDef(self, node):
        start = time()
        self.final_list.append( yellow(f";--- DEF {node.name} ---;\n"))
        self.time_tracker["visit_FunctionDef"] += (time() - start)*2
        self.call_tracker["visit_FunctionDef"] += 1
        self.generic_visit(node)
        self.final_list.append( yellow(f";--- END {node.name} ---;\n"))

    def visit_DefRule(self, node):  # adds (defrule _______  => ______)
        if node.body is None or len(node.body) == 0:
            logger.critical(f"defrule has no body, line {node.lineno}")
        start = time()
        self.final_list.append( (
            green("(defrule")
            + green(";")
            + green(str(node.defrule_num))
            + " "
            + yellow(node.comment)
            + comment(node, self.NO_FILE)
            + "\n"
        ) )
        self.time_tracker["visit_DefRule"] += time() - start
        self.call_tracker["visit_DefRule"] += 1
        if isinstance(node.test, Command):
            self.visit_Command(node.test)
        elif isinstance(node.test, aoeOp):
            self.visit_aoeOp(node.test)
        else:
            if type(node.test) is ast.Name and node.test.id == "true":
                raise Exception(f"on line {node.test.lineno}, you need to use True or true() not true")
            raise Exception(f"{type(node.test)} not implemented in defRulePrintVisiter")
        self.final_list.append( green("=>\n") )
        for body_node in node.body:
            if isinstance(body_node, Command):
                self.visit_Command(body_node)
            elif isinstance(body_node, ast.expr):
                self.visit_Expr(body_node)
        self.final_list.append( green(")\n") )

    def visit_aoeOp(self, node):
        start = time()
        # ADD (op THEN commands THEN )
        self.final_list.append( (
            red("(") + red(node.op.__doc__.lower()) + red("\n")
        ) ) # todo: check if __doc__ can cause errors.
        self.time_tracker["visit_aoeOp"] += time() - start
        self.call_tracker["visit_aoeOp"] += 1
        self.generic_visit(node)
        self.final_list.append( red(")") )

    def evaluate_enum(self, expr, next_expr, human_readable = True):
        start = time()
        value_str = ''
        if type(expr) in [mathOp, compareOp, typeOp]: #todo:figure out if this should even be in Printer as it is doing logic, not just printing. Also if that is true for all mathOp usages
            if next_expr is None:
                raise Exception(f"next_expr is None, but it should be a Variable or Constant or SnI, line {expr.lineno}")
            if type(next_expr) is Variable:
                if next_expr.as_const:
                    prefix = typeOp.constant
                else:
                    prefix = typeOp.goal
                value_str = str(int(expr.val) + 12)
            elif type(next_expr) is ast.Constant:
                prefix = typeOp.constant
                value_str = str(int(expr.val) + 24)
            elif type(next_expr) is SnId:
                prefix = typeOp.strategic_number
                value_str = str(expr.value)
            elif isinstance(next_expr, Strenum):# in self.enum_classes.values():
                prefix = typeOp.constant
            else:
                raise Exception(f"expr.value is not a Variable or Constant or SnI, it is {type(next_expr)}")
            if type(expr) is typeOp:
                if prefix.string != expr.string:
                    logger.warning(f"prefix.string {prefix.string} != expr.string {expr.string}, line {next_expr.end_lineno}")
                return prefix.string
            return prefix.string + expr.string
        
        if type(expr) in [ObjectData, SearchSource, SearchOrder, ObjectStatus, ObjectList]: #parameters that dont seem to have defconts internaly in AOE2
            return str(expr.value)

        if type(expr) is SN:
            return 'sn-' + expr.string.replace("_", "-")
        self.time_tracker["evaluate_enum"] += time() - start
        self.call_tracker["evaluate_enum"] += 1
        return expr.string.replace("_", "-")
    
    def add_def_consts(self):
        start = time()
        def_const_string = ''
        def_const_string = '\n'.join([f"(defconst {def_const})" for def_const in self.def_const_list])
        self.final_list.insert(0, blue(def_const_string) + "\n")
        self.time_tracker["add_def_consts"] += time() - start
        self.call_tracker["add_def_consts"] += 1

    def visit_Command(self, node):  # adds (command arg1 arg2)
        start = time()
        self.final_list.append( blue("  (") + blue(node.func.id.name.replace("_", "-")) )
        
        for itr, expr in enumerate(node.args):
            if type(expr) in list(self.enum_classes.values()):
                next_expr = node.args[itr+1] if itr+1 < len(node.args) else None
                expr_str = self.evaluate_enum(expr, next_expr)
            
            elif isinstance(expr, Variable):
                #expr_str = str(expr.memory_location) #todo: add option back in to make it not human readable
                expr_str = expr.memory_name
                self.def_const_list.add(expr.memory_name + " " + str(expr.memory_location))

            elif isinstance(expr, ast.Constant):
                if type(expr.value) is int:
                    expr_str = str(expr.value)
                elif type(expr.value) is str:
                    expr_str = '"'+expr.value+'"'
                else: 
                    raise Exception(f"Constants need to be an int or str, not {type(expr.value)}")
            else:
                raise Exception(f"visit_command has not implemeted {type(expr)}")
            
            
            self.final_list.append( " " + blue(expr_str) )
        self.final_list.append( blue(")") + comment(node, self.NO_FILE) + "\n" )
        self.time_tracker["visit_Command"] += time() - start
        self.call_tracker["visit_Command"] += 1
        self.generic_visit(node)


class Printer:
    def __init__(self, const_tree, combined_tree):
        self.const_tree = const_tree
        self.tree = combined_tree
        self.final_string = ['']
        self.def_const_list = set()

    @property
    def no_color_final_string(self):
        # Define a regex pattern to match ANSI escape sequences
        ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
        return ansi_escape.sub("", self.final_string)

    @property
    def non_readable_final_string(self):
        no_color = self.no_color_final_string
        no_comments = re.sub(r";.*\n", "", no_color)
        no_whitespace = no_comments.replace("\n", "")
        no_whitespace = re.sub(r" +", " ", no_whitespace)
        no_whitespace = re.sub(r" *=> *", "=>", no_whitespace)
        no_whitespace = re.sub(r" *\( *", "(", no_whitespace)
        no_whitespace = re.sub(r" *\) *", ")", no_whitespace)
        return no_whitespace

    def print_for_string_testing(self):
        visitor = DefRulePrintVisitor(self.final_string, self.const_tree, NO_FILE=True)
        visitor.visit(self.tree)

    def print_all(self, TEST=False):
        
        visitor = DefRulePrintVisitor(self.final_string, self.const_tree, TEST=TEST)
        visitor.visit(self.tree)
        visitor.add_def_consts()
        
        self.final_string = ('').join(visitor.final_list)
        print(self.non_readable_final_string)
        pprint(visitor.time_tracker)
        pprint(visitor.call_tracker)
        return self.final_string


def comment(node, NO_FILE):
    #if NO_FILE:
    #    return ""
    source_segment = lineno = file_path = ""
    if hasattr(node, "file_path") and node.file_path not in ["TEST","NOFILE"]:
        source_segment = ast.get_source_segment(
            read_file_as_string(node.file_path), node
        )
        lineno = str(node.lineno)
        file_path = str(node.file_path).split("/")[-1]
    
    return (
        Fore.GREEN
        + Style.DIM
        + " ;"
        + source_segment.replace("\n", "/n")
        + Style.NORMAL
        + " "
        + lineno
        + Style.DIM
        + "-"
        + file_path
        + Fore.WHITE
        + Style.NORMAL
    )


def check_str(string):
    if type(string) is not str:
        logger.warning(f"{string} is not a string in Printer")
    return str(string)


def green(string):
    return Fore.GREEN + check_str(string) + Fore.WHITE


def red(string):
    return Fore.RED + check_str(string) + Fore.WHITE


def blue(string):
    return Fore.BLUE + check_str(string) + Fore.WHITE


def yellow(string):
    return Fore.YELLOW + check_str(string) + Fore.WHITE
