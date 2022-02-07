from AOEInterpreter import Interpreter
from data import TokenType
from AOEscanner import Scanner
from AOEparser import Parcer
from AOEasserter import Asserter
from AOEprinter import Printer
from termcolor import colored
import sys
from pprint import pprint

#refactor have it look for the first aop file and throw warning
if len(sys.argv) < 2:
  raise Exception("needs argument of ai file name")
if len(sys.argv) > 2:
  raise Exception("aditional arguments are not currently supported!")
fileName = sys.argv[1]
if not '.' in fileName:
  fileName += ".aop"



f = open(fileName,"r")
lines = f.readlines()

myScanner = Scanner(lines)
myScanner.scan()

myScanner.stripTokens(TokenType.WHITE_SPACE)
myScanner.stripTokens(TokenType.COMMENT)

strippedTokens = myScanner.tokens

print("\n===Scanner Results===")
for token in strippedTokens:
    print(str(token.tokenType) + str(token))
    #token.print()

myParcer = Parcer(strippedTokens)
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
f = open("../"+fileName[0]+".per","w")
f.write(myPrinter.finalString)