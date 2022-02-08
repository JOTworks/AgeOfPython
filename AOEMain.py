from AOEInterpreter import Interpreter
from data import TokenType
from AOEscanner import Scanner
from AOEparser import Parcer
from AOEasserter import Asserter
from AOEprinter import Printer
from termcolor import colored
import sys
from pprint import pprint
import os.path
from pathlib import Path




#refactor have it look for the first aop file and throw warning
if len(sys.argv) < 2:
  raise Exception("needs argument of ai file name")
if len(sys.argv) > 2:
  raise Exception("aditional arguments are not currently supported!")
fileName = sys.argv[1].split('.')[0] #gets rid of anything after the first '.'

#############################################################
aiFolder = Path(__file__)
limit = 0
while (aiFolder.name != "ai"):
  aiFolder = aiFolder.parent
  print(aiFolder.name)
  limit += 1
  if limit > 100:
    raise Exception("AgeOfPython needs to be in the ai folder AoE2DE/reasources/_common/ai/")

myScanner = Scanner(str(fileName), aiFolder)
myScanner.scan()


strippedTokens = myScanner.tokens

print("\n===Scanner Results===")
for token in strippedTokens:
    print(str(token.tokenType) + str(token))
    #token.print()

myParcer = Parcer(strippedTokens, aiFolder)
myParcer.parce()

print(len(myParcer.main))
print("\n")

print("\n===Parcer Results===")
for myObject in myParcer.main:
  pprint(myObject, indent=2, width=20)

myAsserter = Asserter(myParcer.main)
myAsserter.check()

myInterpreter = Interpreter(myParcer.main)
myInterpreter.interpret()

print("\n===Interpreter Results===")
for myObject in myInterpreter.main:
  pprint(myObject, indent=2, width=20)

myPrinter = Printer(myInterpreter.main)
myPrinter.print()

print("\n===Printer Results===")
print(myPrinter.finalString)

#if ai file dosnt exist make it
#write over per file
fileName = fileName.split(".")
#raise Exception (aiFolder)
f = open(str(aiFolder)+'\\'+fileName[0]+".per","w")
print(fileName[0]+".per")
f.write(myPrinter.finalString)