import ast
from Compiler import Command, DefRule, JumpType
from scraper import *
from utils_display import read_file_as_string
from colorama import Fore, Back, Style
import re
from MyLogging import logger 

class DefRuleVisitor(ast.NodeVisitor):
    def __init__(self, final_string):
        super().__init__()
        self.final_string = final_string

    def visit_DefRule(self, node): # adds (defrule _______  => ______)
        self.final_string += green("(defrule") + comment(node) + "\n"
        if isinstance(node.test, Command):
            self.visit_Command(node.test)
        elif isinstance(node.test, ast.expr):
            self.visit_expr(node.test)
        self.final_string += green("=>\n")
        for body_node in node.body:
            if isinstance(body_node, Command):
                self.visit_Command(body_node)
            elif isinstance(body_node, ast.expr):
                self.visit_Expr(body_node)
        self.final_string += green(")\n")

    def visit_Command(self, node): # adds (command arg1 arg2)
        self.final_string += blue("  (") + blue(node.func.id.name)
        for expr in node.args:
            if isinstance(expr, JumpType):
                expr = str(expr)
                logger.warning(f"JumpType in final print")
            self.final_string += " " + blue(expr)
        self.final_string += blue(")") + comment(node) + "\n"
        self.generic_visit(node)
        
    def visit_Expr(self, node): # adds (op  )
        if isinstance(node, Command):
            self.visit_Command(node)

        elif isinstance(node, ast.BinOp) or isinstance(node, ast.unaryop):
            self.final_string += red("(")
            self.generic_visit(node)
            self.final_string += red(")")
        else:
            logger.warning(f"{node.__class__}:{node} not accounted in visit_Expr")
            self.generic_visit(node)

class Printer:
    def __init__(self, trees):
        self.main = trees.main_tree
        self.funcList = trees.func_tree
        self.constList = trees.const_tree
        self.final_string = ""   
        print(self.main)
    
    @property
    def no_color_final_string(self):
        # Define a regex pattern to match ANSI escape sequences
        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
        return ansi_escape.sub('', self.final_string)

    
    @property
    def non_readable_final_string(self):
        no_color = self.no_color_final_string
        no_comments = re.sub(r';.*\n', '', no_color)
        no_whitespace = no_comments.replace('\n', '')
        no_whitespace = re.sub(r' +', ' ', no_whitespace)
        no_whitespace = re.sub(r' *=> *', '=>', no_whitespace)
        no_whitespace = re.sub(r'\) +\)', '))', no_whitespace)
        print(no_whitespace)

    def print_all(self, test = False):
        visitor = DefRuleVisitor(self.final_string)
        visitor.visit(self.main)
        visitor.visit(self.funcList)
        self.final_string = visitor.final_string
        return visitor.final_string

def comment(node):
    if hasattr(node, "file_path"):
        source_segment = ast.get_source_segment(read_file_as_string(node.file_path), node)
        lineno = str(node.lineno)
        file_path = str(node.file_path).split('/')[-1]
    else:
        source_segment=lineno=file_path= ""
    return (Fore.GREEN+Style.DIM+" ;"
            +source_segment.replace("\n","/n")
            +Style.NORMAL+" "+lineno+Style.DIM
            +"-"+file_path
            +Fore.WHITE+Style.NORMAL)

def green(string):
    return Fore.GREEN+string+Fore.WHITE
def red(string):
    return Fore.RED+string+Fore.WHITE
def blue(string):
    return Fore.BLUE+string+Fore.WHITE

