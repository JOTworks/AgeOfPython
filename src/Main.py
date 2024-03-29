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

def print_column(rows, num_columns):
  columned_rows = []
  length_column = int(len(rows)/num_columns)
  col_line = ["  \u2502"]
  for i in range(length_column):
    single_row = []
    for j in range(num_columns):
      single_row += col_line
      single_row += rows[i+(j*length_column)]
    columned_rows.append(single_row)
  widths = [max(map(len, col)) for col in zip(*columned_rows)]
  for row in columned_rows:
    print("  ".join((val.ljust(width) for val, width in zip(row, widths))))

def main(argv):
  #TODO: have it look for the first aop file and throw warning
  print("ARGS: "+str(argv))
  #file_path = os.path.Path(__file__)
  #print("FILEPATH: "+str(file_path)+" ::")
  #print (file_path.name)
  if len(argv) < 2:
    raise Exception("needs argument of ai file name")
  fileName = argv[1].split('.')[0] #gets rid of anything after the first '.'
  arguments = argv[2:]
  #############################################################
  aiFolder = Path(__file__).parent.resolve()
  limit = 0
  while (aiFolder.name != "ai"):
    aiFolder = aiFolder.parent
    #print(aiFolder)
    limit += 1
    if limit > 100:
      raise Exception("AgeOfPython needs to be in the ai folder AoE2DE/reasources/_common/ai/")
    
  if "-h" in arguments or "-help" in arguments or "help" in arguments or "?" in arguments:
    print_bright("\n===HELP===")
    print("-s Scanner\n"+
          "-p Parcer\n"+
          "-i Interpreter\n"+
          "-f Function List\n"+
          "-m Memory\n"+
          "-r Printer\n"+
          "-v everything\n"       
          )
  myScanner = Scanner(str(fileName), aiFolder)
  myScanner.scan()


  if "-s" in arguments or "-v" in arguments:
    print_bright("\n+===================+\n"+
                   "|  Scanner Results  |\n"+
                   "+===================+")
    token_list = []
    last_file_line = ''
    for tok in myScanner.tokens:
      row = [str(tok.tokenType).split('.')[1], str(tok.value)]
      if str(tok.file)+str(tok.line) != last_file_line:
        last_file_line = str(tok.file)+str(tok.line)
        row.append(Fore.WHITE + str(tok.file))
        row.append(str(tok.line) +Fore.WHITE)
      else:
        row.append(Fore.LIGHTBLACK_EX + str(tok.file))
        row.append(str(tok.line) +Fore.WHITE)
      token_list.append(row)   
    #token_list = [[str(tok.tokenType).split('.')[1], str(tok.value), str(tok.file), str(tok.line)] for tok in myScanner.tokens]
    print_column(token_list, 3)


  myParcer = Parcer(myScanner.tokens, aiFolder)
  myParcer.parce()

  if "-p" in arguments or "-v" in arguments:
    print_bright("\n+===================+\n"+
                   "|  Parcer Results   |\n"+
                   "+===================+")
    for myObject in myParcer.main:
      pprint(myObject, indent=2, width=20)

  myAsserter = Asserter(myParcer.main)
  myAsserter.check()

  myInterpreter = Interpreter(myParcer.main)
  myInterpreter.interpret()

  if "-i" in arguments or "-v" in arguments:
    print_bright("\n+===================+\n"+
                  "|Interpreter Results|\n"+
                  "+===================+")
    for myObject in myInterpreter.main:
      pprint(myObject, indent=2, width=20)
  if "-f" in arguments or "-v" in arguments:
    print_bright("\n===Function List===")
    for func in myInterpreter.funcList:
      pprint(func, indent=2, width=20)
  if "-m" in arguments or "-v" in arguments:
    print_bright("\n===Used Memory===")

    print(myInterpreter.memory.printUsedMemory())
    print_bright("\n===Constant List===")
    print(myInterpreter.constList)
    #sorts const list by number and strips token to number
    constList = [[str(const), myInterpreter.constList[const]] for const in myInterpreter.constList]
    constList.sort(key = lambda x: x[1])
    print_column([[const[0], str(const[1])] for const in constList],4)

  myPrinter = Printer(myInterpreter.main, myInterpreter.funcList, myInterpreter.constList)
  
  if "test" in arguments:
    myPrinter.print(test = True)
  else:
    myPrinter.print()

  if "-r" in arguments or "-v" in arguments:
    print_bright("\n+===================+\n"+
                   "|  Printer Result   |\n"+ 
                   "+===================+")

    pattern = r'(\;.*)'
    replacement = Fore.GREEN+Style.DIM+r'\1'+Fore.WHITE+Style.NORMAL
    regexed_finalString = re.sub(pattern, replacement, myPrinter.finalString)
    print(regexed_finalString)

  if "-test" not in arguments:
    fileName = fileName.split(".")
    f = open(str(aiFolder)+'\\'+fileName[0]+".per","w")
    open(str(aiFolder)+'\\'+fileName[0]+".ai","w") #adds the ai file if it doesnt exist already
    print(tokenErrorCounter)
    print("FILE: "+str(fileName[0])+".per")
    f.write(myPrinter.finalString)

  pattern = r'(\ *;.*)'
  replacement = '' 
  regexed_finalString = re.sub(pattern, replacement, myPrinter.finalString)

  if "-test" in arguments:
   print(regexed_finalString)
   return regexed_finalString

def print_bright(string):
  print(Style.BRIGHT+string+Style.NORMAL)

if __name__ == '__main__':
  main(sys.argv)