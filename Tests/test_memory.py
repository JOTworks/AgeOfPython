import sys
sys.path.append('./src')
sys.path.append('../src')
import pytest

from Memory import Memory


def test_mallocInt():
  memory = Memory()
  memory.mallocInt("variable")
  assert memory.getMemLoc("variable")

def test_mallocPoint():
  memory = Memory()
  memory.mallocPoint("variable")
  assert memory.getMemLoc("variable")

def test_mallocState():
  memory = Memory()
  memory.mallocState("variable")
  assert memory.getMemLoc("variable")

def test_getMemLoc():
  memory = Memory()
  memory.mallocInt("variable")
  location = memory.getMemLoc("variable")
  assert location == 1
 
#def test_isUsed():
#  memory = Memory()
#  memory.isUsed() 

#def test_Free(test_input, expected):
#  memory = Memory()
#  memory.Free