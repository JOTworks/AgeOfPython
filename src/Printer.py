import ast
from Compiler import Command, DefRule, JumpType, Variable, aoeOp
from scraper import *
from scraper import mathOp
from utils_display import read_file_as_string
from colorama import Fore, Back, Style
import re
from MyLogging import logger
from enum import Enum
from utils import get_enum_classes


class DefRulePrintVisitor(ast.NodeVisitor):
    def __init__(self, final_string, NO_FILE=False, TEST=False):
        super().__init__()
        self.final_string = final_string
        self.NO_FILE = NO_FILE
        self.enum_classes = get_enum_classes()
        self.TEST = TEST

    def visit_if(self, node):
        """
        so we dont print the test and other metadata in visit
        """
        for item in node.body:
            self.visit(item)

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
            red("(") + red(node.op.__doc__) + red("\n")
        )  # todo: check if __doc__ can cause errors.
        self.generic_visit(node)
        self.final_string += red(")")

    def visit_Command(self, node):  # adds (command arg1 arg2)
        self.final_string += blue("  (") + blue(node.func.id.name.replace("_", "-"))
        for itr, expr in enumerate(node.args):
            if type(expr) in list(self.enum_classes.values()):
                if not self.TEST:
                    if type(expr) is mathOp:
                        if type(node.args[itr+1]) is Variable:
                            expr_str = str(int(expr.value) + 12) # goal math are all 12 over constant math
                            #todo: fix this to work with SN, needs to be able to tell if it SN then ad 24 instead of 12
                        else:
                            expr_str = str(expr.value)
                    else:
                        expr_str = str(expr.value)

                else:
                    expr_str = str(expr)

            elif isinstance(expr, Variable):
                expr_str = str(expr.memory_location)
            elif isinstance(expr, ast.Constant):
                if type(expr.value) is int:
                    expr_str = str(expr.value)
                elif type(expr.value) is str:
                    expr_str = "'"+expr.value+"'"
                else: 
                    raise Exception("Constatns need to be an int or str")
            elif isinstance(expr, str):
                expr_str = expr
            else:
                raise Exception(f"visit_command has not implemeted {type(expr)}")
            
            
            self.final_string += " " + blue(expr_str)
        self.final_string += blue(")") + comment(node, self.NO_FILE) + "\n"
        self.generic_visit(node)


class Printer:
    def __init__(self, trees):
        self.main = trees.main_tree
        self.funcList = trees.func_tree
        self.constList = trees.const_tree
        self.final_string = ""

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
        visitor.visit(self.main)

    def print_all(self, TEST=False):
        visitor = DefRulePrintVisitor(self.final_string, TEST=TEST)
        visitor.visit(self.main)
        visitor.visit(self.funcList)
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
