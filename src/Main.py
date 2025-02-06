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
from utils_display import print_bright, print_bordered


def main(argv):
    file_name, arguments = setup_args(argv)
    ai_folder = get_ai_folder()

    if "h" in arguments or "?" in arguments:
        print_bright("\n===HELP===")
        print(
            "-s Scanner\n"
            + "-p Parcer\n"
            + "-i Interpreter\n"
            + "-f Function List\n"
            + "-m Memory\n"
            + "-r Printer\n"
            + "-v everything\n"
            + "-t test\n"
        )

    # *----PARSING----*#
    myParser = Parser(file_name, ai_folder)
    trees = myParser.parse()
    if "p" in arguments or "v" in arguments:
        print_bordered("Parsed tree")
        print(ast.dump(trees.main_tree, indent=4))
        print("_________")

    # TODO: add ast tree viewer back in
    # ast_json = parse_and_convert_to_json(trees['main_tree'])
    # with open('ast.json', 'w') as f:
    #    f.write(ast_json)

    # *----ASSERTING----*#
    # myAsserter = Asserter()
    # myAsserter.check(trees)

    # *----COMPILING----*#
    compiler = Compiler()
    trees = compiler.compile(trees)

    if "p" in arguments or "v" in arguments:
        print_bordered("Compiled tree")
        print(ast.dump((trees.main_tree), indent=4))

    # *----PRINTING----*#
    myPrinter = Printer(trees)
    if "t" in arguments:
        myPrinter.print_all(TEST=True)  # currently makes it not go to numbers
    else:
        myPrinter.print_all(TEST=False)
        file_name = file_name.split(".")[0]
        per_file_path = str(ai_folder) + "/" + file_name + ".per"
        ai_file_path = str(ai_folder) + "/" + file_name + ".ai"

        with open(per_file_path, "w") as f:
            f.write(myPrinter.no_color_final_string)
        open(ai_file_path, "w").close()

    if "r" in arguments or "v" in arguments:
        print(myPrinter.final_string)
        nonTestPrinter = Printer(trees)
        nonTestPrinter.print_all(TEST=False)
        print(nonTestPrinter.non_readable_final_string)
    
    return(myPrinter.non_readable_final_string)


def setup_args(argv):
    arguments = []
    if len(argv) < 2:
        raise Exception("needs argument of ai file name")
    file_name = argv[1].split(".")[0]
    for arg in argv[2:]:
        if arg[0] == "-":
            for letter in arg[1:]:
                arguments.append(letter)
        else:
            raise Exception("Invalid argument, needs to start with -: " + arg)
        print(arguments)
    return file_name, arguments


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
    main(sys.argv)
