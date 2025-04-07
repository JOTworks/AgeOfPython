import ast
from Compiler import Command, Variable, aoeOp
from scraper import *
from scraper import mathOp, compareOp, Strenum
from utils_display import read_file_as_string
from colorama import Fore, Back, Style
import re
from MyLogging import logger
from utils import get_enum_classes


class DefRulePrintVisitor(ast.NodeVisitor):
    def __init__(self, final_string, NO_FILE=False, TEST=True):
        super().__init__()
        self.final_string = final_string
        self.NO_FILE = NO_FILE
        self.enum_classes = get_enum_classes()
        self.TEST = TEST
        self.def_const_list = set()

    def visit_if(self, node):
        """
        so we dont print the test and other metadata in visit
        """
        for item in node.body:
            self.visit(item)

    def visit_FunctionDef(self, node):
        self.final_string += yellow(f";--- DEF {node.name} ---;\n")
        self.generic_visit(node)
        self.final_string += yellow(f";--- END {node.name} ---;\n")

    def visit_DefRule(self, node):  # adds (defrule _______  => ______)
        self.final_string += (
            green("(defrule")
            + green(";")
            + green(str(node.defrule_num))
            + " "
            + yellow(node.comment)
            + comment(node, self.NO_FILE)
            + "\n"
        )
        if isinstance(node.test, Command):
            self.visit_Command(node.test)
        elif isinstance(node.test, aoeOp):
            self.visit_aoeOp(node.test)
        else:
            if type(node.test) is ast.Name and node.test.id == "true":
                raise Exception(f"on line {node.test.lineno}, you need to use True or true() not true")
            raise Exception(f"{type(node.test)} not implemented in defRulePrintVisiter")
        self.final_string += green("=>\n")
        for body_node in node.body:
            if isinstance(body_node, Command):
                self.visit_Command(body_node)
            elif isinstance(body_node, ast.expr):
                self.visit_Expr(body_node)
        self.final_string += green(")\n")

    def visit_aoeOp(self, node):
        # ADD (op THEN commands THEN )
        self.final_string += (
            red("(") + red(node.op.__doc__.lower()) + red("\n")
        )  # todo: check if __doc__ can cause errors.
        self.generic_visit(node)
        self.final_string += red(")")

    def evaluate_enum(self, expr, next_expr, human_readable = True):
        value_str = ''
        if type(expr) in [mathOp, compareOp]: #todo:figure out if this should even be in Printer as it is doing logic, not just printing. Also if that is true for all mathOp usages
            if next_expr is None:
                raise Exception(f"next_expr is None, but it should be a Variable or Constant or SnI, line {expr.lineno}")
            if type(next_expr) is Variable:
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
            return prefix.string + expr.string
        
        if type(expr) in [ObjectData]: #parameters that dont seem to have defconts internaly in AOE2
            return str(expr.value)

        if type(expr) is SN:
            return 'sn-' + expr.string.replace("_", "-")

        return expr.string.replace("_", "-")
    
    def add_def_consts(self):
        def_const_string = """
            (defconst search-local 1)
            (defconst search-remote 2)
                           """
        def_const_string += '\n'.join([f"(defconst {def_const})" for def_const in self.def_const_list])
        self.final_string = '\n' + def_const_string + '\n' + self.final_string + '\n'

    def visit_Command(self, node):  # adds (command arg1 arg2)
        self.final_string += blue("  (") + blue(node.func.id.name.replace("_", "-"))
        
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
            
            
            self.final_string += " " + blue(expr_str)
        self.final_string += blue(")") + comment(node, self.NO_FILE) + "\n"
        self.generic_visit(node)


class Printer:
    def __init__(self, tree):
        self.tree = tree
        self.final_string = ""
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
        no_whitespace = re.sub(r"\) +\)", "))", no_whitespace)
        return no_whitespace

    def print_for_string_testing(self):
        visitor = DefRulePrintVisitor(self.final_string, NO_FILE=True)
        visitor.visit(self.tree)

    def print_all(self, TEST=False):
        visitor = DefRulePrintVisitor(self.final_string, TEST=TEST)
        visitor.visit(self.tree)
        visitor.add_def_consts()
        
        self.final_string = visitor.final_string
        return visitor.final_string


def comment(node, NO_FILE):
    #if NO_FILE:
    #    return ""
    if hasattr(node, "file_path"):
        source_segment = ast.get_source_segment(
            read_file_as_string(node.file_path), node
        )
        lineno = str(node.lineno)
        file_path = str(node.file_path).split("/")[-1]
    else:
        source_segment = lineno = file_path = ""
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
