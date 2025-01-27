import ast
from Compiler import Command, DefRule
from scraper import *
class DefRuleVisitor(ast.NodeVisitor):
    def __init__(self):
        self.finalString = ""

    def visit_DefRule(self, node): # adds (defrule _______  => ______)
        self.finalString += "(defrule"
        print(f"type: {type(node.test)}")
        cmd = Command(AOE2FUNC.unit_count, [])
        print(f"type: {type(cmd)}")
        if isinstance(node.test, Command):
            print("in Command")
            self.visit_command(node.test)
        elif isinstance(node.test, ast.expr):
            print("in Expr")
            self.visit_expr(node.test)
        self.finalString += "=>"
        for body_node in node.body:
            if isinstance(body_node, Command):
                print("in body Command")
                self.visit_command(body_node)
            if isinstance(body_node, ast.expr):
                print("in body Expr")
                self.visit_expr(body_node)

        self.finalString += ")"
        return node

    def visit_command(self, node): # adds (command arg1 arg2)
        self.finalString += "(" + node.value.func.id
        for expr in node.args:
            self.finalString += " " + expr
        self.finalString += ")"
        return node
        
    def visit_expr(self, node): # adds (op  )
        if isinstance(node, ast.BinOp) or isinstance(node, ast.unaryop):
            self.finalString += "(" + str(node.op)
        else:
            raise Exception("printing "+str(node.__class__)+" is not yet Iplamented!"+str(node))
        self.generic_visit(node)
        self.finalString += ")"

class Printer:
    def __init__(self, main, funcList, constList):
        self.main = main
        self.funcList = funcList
        self.constList = constList
        self.finalString = ""   

    def print_all(self, test = False):
        visitor = DefRuleVisitor()
        visitor.visit(self.main)
        self.finalString = visitor.finalString
        return visitor.finalString