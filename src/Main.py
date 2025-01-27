from Asserter import Asserter
from Printer import Printer
from Compiler import Compiler
import sys
from pprint import pprint
import os.path
from pathlib import Path
from colorama import Fore, Back, Style
import re
from math import ceil, floor
import ast
import os
from collections import namedtuple
import json
from scraper import *

def get_file_path(file_name, ai_folder): #TODO: issue if 2 files have same name
  #OPEN FILE
  fullPath = "FILE NOT FOUND"
  file_name = file_name.replace("/","\\")
  for file in list(ai_folder.glob('**/*.per')):
    if file_name+".per" in str(file) or file_name in str(file):
      fullPath = file
  for file in list(ai_folder.glob('**/*.aop')): #prioritizes aop files because it is last
    if file_name+".aop" in str(file) or file_name in str(file):
      fullPath = file
  for file in list(ai_folder.glob('**/*.py')): #prioritizes aop files because it is last
    if file_name+".aop" in str(file) or file_name in str(file):
      fullPath = file
  if fullPath == "FILE NOT FOUND":
    raise Exception(file_name+" is not found")
  # infile = open(os.path.join(os.path.dirname(sys.argv[0]), "folder2/test.txt"), "r+")
  return fullPath

def parse_multiple_files(base_file, ai_folder):
    """Parses the given file and all its imports.
    the imports will only have functdef, assign in their tree. 
    they will have edited names if imported with the as keyword
    """

    parsed_files = set()  # Keep track of parsed files to avoid cycles
    asts = {}

    def parse_file(file_name, ai_folder, names, base_file = False):
        import_all = False
        alias_names = [alias.name for alias in names]
        alias_asnames = dict([(alias.name,alias.asname) if hasattr(alias,"asname") else (alias.name,alias.name) for alias in names])
        if alias_names == ['*']:
            alias_names = []
            import_all = True
            
        file_path = get_file_path(file_name, ai_folder)
        if file_path in parsed_files:
            return
        parsed_files.add(file_path)

        with open(file_path, "r") as f:
            tree = ast.parse(f.read(), filename=file_path)
            module = ast.Module(body=[])
            for node in tree.body:
                if isinstance(node, ast.FunctionDef) and (node.name in alias_names  or import_all):
                    if not import_all:
                      alias_names.remove(node.name)
                      node.name = alias_asnames[node.name]
                    module.body.append(node)
                elif isinstance(node, ast.Assign):
                  if len(node.targets) != 1:
                   raise Exception("Only one target allowed in assignment")
                  if isinstance(node.targets[0], ast.Name) and (node.targets[0].id in alias_names or import_all):
                    if not import_all:
                      alias_names.remove(node.targets[0].id)
                      node.targets[0].id = alias_asnames[node.targets[0].id]
                    module.body.append(node)
                elif isinstance(node, ast.ImportFrom):
                    if not ('aoe2scriptEnums' in node.module or 'aoe2scriptFunctions' in node.module):
                      parse_file(node.module, ai_folder, node.names)
            if len(alias_names) > 0 and '*' not in alias_names:
              raise Exception(f"{alias_names} not found in {file_name}")
            
            if base_file:
              asts[file_name] = tree
            else:
              asts[file_name] = module

    parse_file(base_file, ai_folder, [ast.alias("*")], base_file = True)
    return asts


def main(argv):
  file_name, arguments = setup_args(argv) 
  ai_folder = get_ai_folder()
    
  if "h" in arguments or "?" in arguments:
    print_bright("\n===HELP===")
    print("-s Scanner\n"+
          "-p Parcer\n"+
          "-i Interpreter\n"+
          "-f Function List\n"+
          "-m Memory\n"+
          "-r Printer\n"+
          "-v everything\n"+
          "-t test\n"       
          )
  
  #Jack TODO: figure out if ast can make tree from multiple files based on imports!
  #
  # import basicly just loads the code there
  # check for import loops
  # dont define functions in functions
  # 
  asts = parse_multiple_files(file_name, ai_folder)

  
  file_path = get_file_path('aoe2scriptFunctions.py', ai_folder)
  with open(file_path, "r") as f:
    aoe_func_tree = ast.parse(f.read(), filename=file_path)
    #aoe_constant_tree = get ast from the enums file
  trees = {
    "main_tree":asts.pop(file_name),
    "function_tree":ast.Module(body=[]), 
    "constant_tree":ast.Module(body=[]),
  }
  #combine all functDefs and constants
  for node in list(trees['main_tree'].body):
    if isinstance(node, ast.FunctionDef):
      trees['function_tree'].body.append(node)
      trees['main_tree'].body.remove(node)
    elif isinstance(node, ast.ImportFrom):
      trees['main_tree'].body.remove(node)
    elif isinstance(node, ast.Assign):
      if isinstance(node.value, ast.Call) and node.value.func.id == "Const":
        trees['constant_tree'].body.append(node)
        trees['main_tree'].body.remove(node)
  for tree_filename, tree in asts.items():
    for node in tree.body:
      if isinstance(node, ast.FunctionDef):
        trees['function_tree'].body.append(node)
      elif isinstance(node, ast.Assign):
        trees['constant_tree'].body.append(node)
      else:
        raise Exception("Only FunctionDefs and Assigns allowed in imports")
  
  if "p" in arguments or "v" in arguments:
    for key, value in trees.items():
      print_bordered(str(key))
      print(ast.dump(value, indent=4))
      print("_________")

  #TODO: add ast tree viewer back in
  #ast_json = parse_and_convert_to_json(trees['main_tree']) 
  #with open('ast.json', 'w') as f:
  #    f.write(ast_json)

  #myAsserter = Asserter()
  #myAsserter.check(trees)
  
  compiler = Compiler()
  trees['main_tree'] = compiler.compile(trees['main_tree'])

  if "p" in arguments or "v" in arguments:
    print_bordered('altered tree')
    print(ast.dump(trees['main_tree'], indent=4))

  myPrinter = Printer(trees['main_tree'], trees['function_tree'], trees['constant_tree'])
  myPrinter.print_all()
  
  if "r" in arguments or "v" in arguments:
    print_bordered("Printer Result")
    pattern = r'(\;.*)'
    replacement = Fore.GREEN+Style.DIM+r'\1'+Fore.WHITE+Style.NORMAL
    regexed_finalString = re.sub(pattern, replacement, myPrinter.finalString)
    print(regexed_finalString)
  
  if "t" in arguments:
    myPrinter.print_all(test = True) #currently test dosn't do anything
  else:
    myPrinter.print_all()
    file_name = file_name.split(".")
    f = open(str(ai_folder)+'\\'+file_name[0]+".per","w")
    open(str(ai_folder)+'\\'+file_name[0]+".ai","w") #adds the ai file if it doesnt exist already
    print("FILE: "+str(file_name[0])+".per")
    f.write(myPrinter.finalString)

  pattern = r'(\ *;.*)'
  replacement = '' 
  regexed_finalString = re.sub(pattern, replacement, myPrinter.finalString)

  if "t" in arguments:
   print(regexed_finalString)
   return regexed_finalString

def setup_args(argv):
  arguments = []
  if len(argv) < 2:
    raise Exception("needs argument of ai file name")
  file_name = argv[1].split('.')[0]
  for arg in argv[2:]:
    if arg[0] == '-':
      for letter in arg[1:]:
        arguments.append(letter)
    else:
      raise Exception("Invalid argument, needs to start with -: "+arg)
    print(arguments)
  return file_name, arguments

def get_ai_folder():
  ai_folder = Path(__file__).parent.resolve()
  limit = 0
  while (ai_folder.name != "ai"):
    ai_folder = ai_folder.parent
    limit += 1
    if limit > 100:
      raise Exception("AgeOfPython needs to be in the ai folder AoE2DE/reasources/_common/ai/")
  return ai_folder

def print_bright(string):
  print(Style.BRIGHT+string+Style.NORMAL)

def print_bordered(string):
  bordered_string = ['','','']
  min_width = 20
  border_length = max(min_width, len(string)+2)
  right_side_padding = max(0,floor((border_length-len(string))/2))
  left_side_padding = right_side_padding + (border_length-len(string))%2
  #left side
  bordered_string[0]+="\u2554"
  bordered_string[1]+="\u2551"
  bordered_string[2]+="\u255A"
  #middle
  bordered_string[1]+= " "*(left_side_padding)
  for i in range(border_length):
    bordered_string[0]+="\u2550"
    bordered_string[1]+= string[i] if i < len(string) else ""
    bordered_string[2]+="\u2550"
  bordered_string[1]+= " "*(right_side_padding)
  #right side
  bordered_string[0]+="\u2557\n"
  bordered_string[1]+="\u2551\n"
  bordered_string[2]+="\u255D"
  return print_bright("".join(bordered_string))

def print_column(rows, num_columns):
  columned_rows = []
  length_column = ceil(len(rows) / num_columns)
  extra_rows_needed = len(rows) % num_columns
  if extra_rows_needed > 0:
    for i in range(num_columns - extra_rows_needed):
      rows.append(['-', '-', '\x1b[37m-', '-\x1b[37m'])
  col_line = ["  \u2502"]
  for i in range(length_column):
    single_row = []
    for j in range(num_columns):
      single_row += col_line
      try:
        single_row += rows[i+(j*length_column)]
      except Exception as e:
        print(f'EXECPTION:{e}')
    columned_rows.append(single_row)
  widths = [max(map(len, col)) for col in zip(*columned_rows)]
  for row in columned_rows:
    print("  ".join((val.ljust(width) for val, width in zip(row, widths))))

def display_scanner(myScanner):
  print_bordered("Scanner Results")
  max_value_len = 18
  token_list = []
  last_file_line = ''
  for tok in myScanner.tokens:
    print(tok)
  for tok in myScanner.tokens:
    val = str(tok.print_value())
    if len(val) > max_value_len:
      val = val[:max_value_len-2]+'~'+str(len(val))
    row = [str(tok.tokenType).split('.')[1], val]
    if str(tok.file)+str(tok.line) != last_file_line:
      last_file_line = str(tok.file)+str(tok.line)
      row.append(Fore.WHITE + str(tok.file))
      row.append(str(tok.line) +Fore.WHITE)
    else:
      row.append(Fore.LIGHTBLACK_EX + str(tok.file))
      row.append(str(tok.line) +Fore.WHITE)
    token_list.append(row)   
  print_column(token_list, 3)

if __name__ == '__main__':
  main(sys.argv)