from distutils import command
import sys
sys.path.append('./src')
sys.path.append('../src')
from Interpreter import Interpreter
from data import *
from data import VarAsignObject
import pytest
from Scanner import Scanner
from Parser import Parcer

def validate_parse(lines, type):
  myParser = Parcer([],"")
  myScanner = Scanner("","")
  myScanner.scanLines(lines.split("\n"))
  myParser.tokens = myScanner.tokens
  myParser.main = []
  myParser.parce()
  assert len(myParser.main) == 1
  if len(myParser.main) == 1:
    firstItem = myParser.main[0]
    assert isinstance(firstItem, type)

def invalidate_parse(lines):
  myParser = Parcer([],"")
  myScanner = Scanner("","")
  myScanner.scanLines(lines.split("\n"))
  myParser.tokens = myScanner.tokens
  myParser.main = []
  with pytest.raises(Exception):
    myParser.parce()