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

def print_column(rows):
  widths = [max(map(len, col)) for col in zip(*rows)]
  for row in rows:
    print("  ".join((val.ljust(width) for val, width in zip(row, widths))))

def main(argv):
  #TODO: have it look for the first aop file and throw warning
  print(argv)
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

  myScanner = Scanner(str(fileName), aiFolder)
  myScanner.scan()



  if "-s" in arguments or "-v" in arguments:
    print("\n===Scanner Results===")
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
    print_column(token_list)


  myParcer = Parcer(myScanner.tokens, aiFolder)
  myParcer.parce()

  if "-p" in arguments or "-v" in arguments:
    print(len(myParcer.main))
    print("\n")

  if "-p" in arguments or "-v" in arguments:
    print("\n===Parcer Results===")
    for myObject in myParcer.main:
      pprint(myObject, indent=2, width=20)

  myAsserter = Asserter(myParcer.main)
  myAsserter.check()

  myInterpreter = Interpreter(myParcer.main)
  myInterpreter.interpret()

  if "-i" in arguments or "-v" in arguments:
    print("\n===Interpreter Results===")
    for myObject in myInterpreter.main:
      pprint(myObject, indent=2, width=20)
  if "-f" in arguments or "-v" in arguments:
    print("\n===Function List===")
    for func in myInterpreter.funcList:
      pprint(func, indent=2, width=20)
  if "-m" in arguments or "-v" in arguments:
    print("\n===Used Memory===")
    print(myInterpreter.memory.printUsedMemory())
    print("\n===Constant List===")
    print(myInterpreter.constList)

  myPrinter = Printer(myInterpreter.main, myInterpreter.funcList, myInterpreter.constList)
  myPrinter.print()

  if "-r" in arguments or "-v" in arguments:
    print("\n===Printer Results===")
    print(myPrinter.finalString)

  fileName = fileName.split(".")
  f = open(str(aiFolder)+'\\'+fileName[0]+".per","w")
  open(str(aiFolder)+'\\'+fileName[0]+".ai","w") #adds the ai file if it doesnt exist already
  print(fileName[0]+".per")
  f.write(myPrinter.finalString)

if __name__ == '__main__':
  main(sys.argv)