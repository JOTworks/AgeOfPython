import ast
from Compiler import Command, DefRule, JumpType
from scraper import *
from utils_display import read_file_as_string
from colorama import Fore, Back, Style

class DefRuleVisitor(ast.NodeVisitor):
    def __init__(self, finalString):
        super().__init__()
        self.finalString = finalString

    #! something is printing out the jump commands twice inside of defrule body
    def visit_DefRule(self, node): # adds (defrule _______  => ______)
        self.finalString += green("(defrule") + comment(node) + "\n"
        if isinstance(node.test, Command):
            self.visit_Command(node.test)
        elif isinstance(node.test, ast.expr):
            self.visit_expr(node.test)
        self.finalString += green("=>\n")
        for body_node in node.body:
            if isinstance(body_node, Command):
                self.visit_Command(body_node)
            if isinstance(body_node, ast.expr):
                self.visit_Expr(body_node)
        self.finalString += green(")\n")

    def visit_Command(self, node): # adds (command arg1 arg2)
        self.finalString += blue("  (") + blue(node.func.id.name)
        for expr in node.args:
            if isinstance(expr, JumpType):
                expr = str(expr)
                print(f"WARNING! JumpType in final print")
            self.finalString += " " + blue(expr)
        self.finalString += blue(")") + comment(node) + "\n"
        self.generic_visit(node)
        
    def visit_Expr(self, node): # adds (op  )
        if isinstance(node, Command):
            self.visit_Command(node)

        elif isinstance(node, ast.BinOp) or isinstance(node, ast.unaryop):
            self.finalString += red("(")
            self.generic_visit(node)
            self.finalString += red(")")
        else:
            print(f"WARNING! {node.__class__}:{node} not accounted in visit_Expr")
            self.generic_visit(node)
        

class Printer:
    def __init__(self, trees):
        self.main = trees.main_tree
        self.funcList = trees.func_tree
        self.constList = trees.const_tree
        self.finalString = ""   
        print(self.main)

    def print_all(self, test = False):
        visitor = DefRuleVisitor(self.finalString)
        visitor.visit(self.main)
        visitor.visit(self.funcList)
        self.finalString = visitor.finalString
        return visitor.finalString

def comment(node):
    if hasattr(node, "file_path"):
        source_segment = ast.get_source_segment(read_file_as_string(node.file_path), node)
        lineno = str(node.lineno)
        file_path = str(node.file_path).split('/')[-1]
    else:
        source_segment=lineno=file_path= ""
    return (Fore.GREEN+Style.DIM+" ; "
            +source_segment.replace("\n","/n")
            +" "+lineno
            +"-"+file_path
            +Fore.WHITE+Style.NORMAL)
def green(string):
    return Fore.GREEN+string+Fore.WHITE
def red(string):
    return Fore.RED+string+Fore.WHITE
def blue(string):
    return Fore.BLUE+string+Fore.WHITE

