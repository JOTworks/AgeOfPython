from scraper import AOE2OBJ, Point, State
from sortedcontainers import SortedDict
from pprint import pprint
import ast

class StoredMemory:
    def __init__(self, name, var_type, length, start):
        self.name = name
        self.var_type = var_type
        self.length = int(length)
        self.start = int(start)

    def __repr__(self):
        reg_str = str(self.start)
        if self.length > 1:
            reg_str += f"-{self.start + self.length - 1}"
        out_string = f"{self.var_type.__name__} " + reg_str

        return out_string


class Memory:
    def __init__(self):
        self._FIRST_REGISTER = 41
        self._LAST_REGISTER = 15999
        # self.openMemory = [] #list of open goals, they get deleted when in use and added when freed
        self._used_memory = SortedDict({})  # {start: StoreddMemory}
        self._open_memory = SortedDict({41: 15999})  # {start: end}

    def print_memory(self):
        print(f"{self.free_memory_count=}")
        pprint(self._open_memory)
        print(f"{self.used_memory_count=}")
        pprint(self._used_memory)

    @property
    def free_memory_count(self):
        return sum([end + 1 - start for start, end in self._open_memory.items()])

    @property
    def used_memory_count(self):
        return sum([var.length for var in self._used_memory.values()])

    def malloc(self, var_name, var_type, length=None, front=True):
        class_constructer_default_size = {Point:2, State:4, int:1, list:8}

        if var_type is AOE2OBJ.Point:
            var_type = Point
        if var_type is AOE2OBJ.State:
            var_type = State
        if length and not isinstance(var_type, list):
            raise Exception("Length can only be specified for list types")
        if not length:
            length = class_constructer_default_size[var_type]
        free_space_start = self.find_open_space(length, front)

        free_space_end = self._open_memory.pop(free_space_start)
        self._open_memory[free_space_start + length] = free_space_end

        self._used_memory[var_name] = StoredMemory(
            var_name, var_type, length, free_space_start
        )

    def free(self, var_name, front=True):
        var = self._used_memory.pop(var_name)

        # create free space
        self._open_memory[var.start] = var.start + var.length - 1

        # check if free memory after, and combine them
        if var.start + var.length in self._open_memory.keys():
            memory_after_end = self._open_memory.pop(var.start + var.length)
            self._open_memory[var.start] = memory_after_end

        # check if free memory before, and combine them
        if var.start - 1 in self._open_memory.values():
            for start, end in self._open_memory.items():
                if end == var.start - 1:
                    var_memory_end = self._open_memory.pop(var.start)
                    self._open_memory[start] = var_memory_end

    def get(self, var_name, abstracted_offset="0"):
        try:
            stored_memory = self._used_memory[var_name]
        except KeyError:
            return None
        if abstracted_offset.isdigit():
            offset = int(abstracted_offset)
        elif abstracted_offset in ["x", "LocalIndex"]:
            offset = 0
        elif abstracted_offset in ["y", "LocalList"]:
            offset = 1
        elif abstracted_offset in ["z", "RemoteIndex"]:
            offset = 2
        elif abstracted_offset in ["t", "RemoteList"]:
            offset = 3
        else:
            raise Exception(f"Invalid offset {abstracted_offset}")
        if offset >= stored_memory.length:
            raise Exception(f"Out of index error {offset}>{var_name} len")
        return stored_memory.start + offset

    def find_open_space(self, length, front=True):
        if front:
            temp_open_memory = self._open_memory
        else:
            temp_open_memory = reversed(self._open_memory)
        for start, end in temp_open_memory.items():
            if end - start >= length:
                return start
        raise Exception("Out of memory")
