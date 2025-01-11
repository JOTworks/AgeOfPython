from Interpreter import Interpreter
from Scanner import Scanner
from Parser import Parcer
from Asserter import Asserter
from Printer import Printer
from termcolor import colored
import sys
from pprint import pprint
import os.path
from pathlib import Path
from colorama import Fore, Back, Style
import re
from data import tokenErrorCounter
from math import ceil, floor

def main(argv):

  fileName, arguments = setup_args(argv) 
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
    
  myScanner = Scanner(str(fileName), ai_folder)
  myScanner.scan()
  if "s" in arguments or "v" in arguments:
    display_scanner(myScanner)

  myParcer = Parcer(myScanner.tokens, ai_folder)
  myParcer.parce()
  if "p" in arguments or "v" in arguments:
    print_bordered("Parcer Results")
    for myObject in myParcer.main:
      pprint(myObject, indent=2, width=20)

  myAsserter = Asserter(myParcer.main)
  myAsserter.check()

  myInterpreter = Interpreter(myParcer.main)
  myInterpreter.interpret()

  if "i" in arguments or "v" in arguments:
    print_bordered("Interpreter Results")
    for myObject in myInterpreter.main:
      pprint(myObject, indent=2, width=20)

  if "f" in arguments or "v" in arguments:
    print_bright("\n===Function List===")
    for func in myInterpreter.funcList:
      pprint(func, indent=2, width=20)

  if "m" in arguments or "v" in arguments:
    print_bright("\n===Used Memory===")
    print(myInterpreter.memory.printUsedMemory())
    print_bright("\n===Constant List===")
    print(myInterpreter.constList)
    #sorts const list by number and strips token to number
    constList = [[str(const), myInterpreter.constList[const]] for const in myInterpreter.constList]
    constList.sort(key = lambda x: x[1])
    print_column([[const[0], str(const[1])] for const in constList],4)

  myPrinter = Printer(myInterpreter.main, myInterpreter.funcList, myInterpreter.constList)
  
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
    fileName = fileName.split(".")
    f = open(str(ai_folder)+'\\'+fileName[0]+".per","w")
    open(str(ai_folder)+'\\'+fileName[0]+".ai","w") #adds the ai file if it doesnt exist already
    print(tokenErrorCounter)
    print("FILE: "+str(fileName[0])+".per")
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
  fileName = argv[1].split('.')[0]
  for arg in argv[2:]:
    if arg[0] == '-':
      for letter in arg[1:]:
        arguments.append(letter)
    else:
      raise Exception("Invalid argument, needs to start with -: "+arg)
    print(arguments)
  return fileName, arguments

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
  bordered_string[0]+="+"
  bordered_string[1]+="|"
  bordered_string[2]+="+"
  #middle
  bordered_string[1]+= " "*(left_side_padding)
  for i in range(border_length):
    bordered_string[0]+="="
    bordered_string[1]+= string[i] if i < len(string) else ""
    bordered_string[2]+="="
  bordered_string[1]+= " "*(right_side_padding)
  #right side
  bordered_string[0]+="+\n"
  bordered_string[1]+="|\n"
  bordered_string[2]+="+"
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