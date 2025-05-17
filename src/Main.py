from Asserter import Asserter
from Printer import Printer
from Compiler import Compiler
import sys
from pprint import pprint
from pathlib import Path
from Parser import Parser
from colorama import Fore, Back, Style
import re
from math import ceil, floor
import ast
from collections import namedtuple
from scraper import *
from utils_display import print_bright, print_bordered, print_stats
import argparse
from time import time


def main(file_name, arguments):
    first_time = time()
    last_time = time()
    ai_folder = get_ai_folder()

    # *----PARSING----*#
    myParser = Parser(file_name, ai_folder)
    trees = myParser.parse()
    if arguments.parcer or arguments.verbose:
        print_bordered("Parsed Main tree")
        print(ast.dump(trees.main_tree, indent=4))
        print_bordered("Parsed Func tree")
        print(ast.dump(trees.func_tree, indent=4))
        print_bordered("Parsed Const tree")
        print(ast.dump(trees.const_tree, indent=4))
        print("_________")
        print(f"Parsing completed in {time() - last_time:.2f} seconds")
        last_time = time()
    # ast_json = parse_and_convert_to_json(trees['main_tree'])
    # with open('ast.json', 'w') as f:
    #    f.write(ast_json)

    # *----ASSERTING----*#
    #myAsserter = Asserter()
    #myAsserter.check(trees.main_tree)
    #myAsserter.check(trees.func_tree)
    #myAsserter.check(trees.const_tree)

    # *----COMPILING----*#
    compiler = Compiler()
    verbose_compiler = True if arguments.everything_verbose or arguments.compile_verbose else False
    combined_tree, memory = compiler.compile(trees, verbose_compiler)

    if arguments.compile or arguments.verbose:
        print_bordered("Combined Tree")
        print(ast.dump((combined_tree), indent=4))
        print(f"Compiling completed in {time() - last_time:.2f} seconds")
        last_time = time()
    # *----PRINTING----*#
    myPrinter = Printer(trees.const_tree, combined_tree)
    if arguments.test:
        myPrinter.print_all(TEST=True)  # currently makes it not go to numbers
    else:
        myPrinter.print_all(TEST=False)
        file_name = file_name.split(".")[0]
        per_file_path = str(ai_folder) + "/" + file_name + ".per"
        ai_file_path = str(ai_folder) + "/" + file_name + ".ai"

        with open(per_file_path, "w") as f:
            f.write(myPrinter.no_color_final_string)
        open(ai_file_path, "w").close()

    if arguments.printer or arguments.verbose:
        print(myPrinter.final_string)
        nonTestPrinter = Printer(trees.const_tree, combined_tree)
        nonTestPrinter.print_all(TEST=False)
    print(f"Printing completed in {time() - last_time:.2f} seconds")
    last_time = time()


    # *----stats on code----*#
    print_stats(
        combined_tree.body[-1].defrule_num,
        memory.free_memory_count, 
        memory.used_memory_count, 
    )
    print(f"Program runtime {time() - first_time:.2f} seconds")

def get_ai_folder():
    ai_folder = Path(__file__).parent.resolve()
    limit = 0
    while ai_folder.name != "ai":
        ai_folder = ai_folder.parent
        limit += 1
        if limit > 100:
            raise Exception(
                "AgeOfPython needs to be in the ai folder AoE2DE/reasources/_common/ai/"
            )
    return ai_folder


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="compile python to aoe2script")
    parser.add_argument("-f", "--filename", help="input filename")
    parser.add_argument("-p", "--parcer", help="output parcer abstract syntax tree", action="store_true")
    parser.add_argument("-m", "--memory", help="output memory locations", action="store_true") #todo: make a history of memory locations for better printing
    parser.add_argument("-c", "--compile", help="output compiled abstract syntax tree", action="store_true")
    parser.add_argument("-cv", "--compile_verbose", help="output ASTs for each step of compiling", action="store_true")
    parser.add_argument("-r", "--printer", help="output final .per results", action="store_true")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-vv", "--everything_verbose", help="increase output verbosity", action="store_true")
    
    parser.add_argument("-t", "--test", help="test that makes things not actauly save", action="store_true")
    parser.add_argument("-o", "--obfuscate", help="safe .per file in non human readable way", action="store_true")
    
    args = parser.parse_args()
    
    if hasattr(args,"everything_verbose") and args.everything_verbose:
        args.v = True
        args.cv = True
    
    if hasattr(args,"verbose") and args.verbose:
        args.p = True
        args.m = True
        args.c = True
        args.r = True

    main(args.filename, args)
