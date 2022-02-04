from data import TokenType
from AOEscanner import Scanner
from AOEparser import Parcer
from termcolor import colored



from pprint import pprint
f = open("./testInput.txt","r")
lines = f.readlines()

myScanner = Scanner(input)

lineNum = 0
for line in lines:
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

for myObject in myParcer.main:
#  print(myObject)
  pprint(myObject, indent=2, width=20)
