from AOEInterpreter import Interpreter
from data import TokenType
from AOEscanner import Scanner
from AOEparser import Parcer
from AOEasserter import Asserter
from termcolor import colored



from pprint import pprint
f = open("./testInput2.txt","r")
lines = f.readlines()

myScanner = Scanner(input)

lineNum = 0
for line in lines: #REFACTOR accept multiline strings and comments
  lineNum = lineNum + 1
  myScanner.scan(line, lineNum)

myScanner.stripTokens(TokenType.WHITE_SPACE)
myScanner.stripTokens(TokenType.COMMENT)

strippedTokens = myScanner.tokens

#for token in strippedTokens:
#    print(token)
    #token.print()

myParcer = Parcer(strippedTokens)
myParcer.parce()

print(len(myParcer.main))
print("\n")

#for myObject in myParcer.main:
#  print(myObject)
#  pprint(myObject, indent=2, width=20)

myAsserter = Asserter(myParcer.main)
myAsserter.check()

myInterpreter = Interpreter(myParcer.main)
myInterpreter.interpret()

for myObject in myInterpreter.main:
  print(myObject)
  pprint(myObject, indent=2, width=20)