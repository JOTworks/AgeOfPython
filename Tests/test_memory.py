import sys
sys.path.append('./src')
sys.path.append('../src')
from Memory import Memory
from scraper import class_constructers
import pytest


def test_memory_count():
    memory = Memory()
    assert memory.free_memory_count == 15958
    assert memory.used_memory_count == 0

def test_malloc():
  memory = Memory()
  memory.malloc("variable", int)
  assert memory.used_memory_count == 1

def test_free():
  memory = Memory()
  memory.malloc("variable", int)
  memory.free("variable")
  assert memory.used_memory_count == 0


 
#def test_isUsed():
#  memory = Memory()
#  memory.isUsed() 

#def test_Free(test_input, expected):
#  memory = Memory()
#  memory.Free