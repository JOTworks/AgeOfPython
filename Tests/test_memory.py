import sys

sys.path.append("./src")
sys.path.append("../src")
from Memory import Memory
from scraper import class_constructers
import pytest
from scraper import Const
from sortedcontainers import SortedDict

types_len_dict = class_constructers
STARTING_OPEN_MEMORY = 15959


def test_memory_count():
    memory = Memory()
    assert memory.free_memory_count == STARTING_OPEN_MEMORY
    assert memory.used_memory_count == 0


def test_malloc():
    memory = Memory()
    for type, len in types_len_dict.items():
        memory.malloc("var", type)
        assert memory.used_memory_count == len
        memory.__init__()


def test_free():
    memory = Memory()
    for type, len in types_len_dict.items():
        memory.malloc("var", type)
        memory.free("var")
        assert memory.used_memory_count == 0
        memory.__init__()


def test_free_combine_both_sides():
    memory = Memory()
    for type, len in types_len_dict.items():
        memory.malloc("var_1", type)
        memory.malloc("var_2", type)
        memory.malloc("var_3", type)
        memory.malloc("var_4", type)
        memory.malloc("var_5", type)
        assert memory.used_memory_count == len * 5, memory._used_memory
        assert memory.free_memory_count == STARTING_OPEN_MEMORY - len * 5, (
            memory._open_memory
        )
        assert memory._open_memory.__len__() == 1, str(memory._open_memory)
        memory.free("var_2")
        memory.free("var_4")
        assert memory.used_memory_count == len * 3, memory._used_memory
        assert memory.free_memory_count == STARTING_OPEN_MEMORY - len * 3, (
            memory._open_memory
        )
        assert memory._open_memory.__len__() == 3, len(memory._open_memory)
        memory.free("var_3")
        assert memory.used_memory_count == len * 2, memory._used_memory
        assert memory.free_memory_count == STARTING_OPEN_MEMORY - len * 2, (
            memory._open_memory
        )
        assert memory._open_memory.__len__() == 2, memory._open_memory
        memory.__init__()


def test_get():
    memory = Memory()
    for type, len in types_len_dict.items():
        memory.malloc("var", type)
        for i in range(len):
            assert memory.get("var", str(i)) == 41 + i
            if i < 4:
                assert memory.get("var", ["x", "y", "z", "t"][i]) == 41 + i
        memory.__init__()


# def test_isUsed():
#  memory = Memory()
#  memory.isUsed()

# def test_Free(test_input, expected):
#  memory = Memory()
#  memory.Free
