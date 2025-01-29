from scraper import class_constructers
from sortedcontainers import SortedDict

class StoredMemory:
    def __init__(self, name, var_type, length, start):
        self.name = name
        self.var_type = var_type
        self.length = length
        self.start = start

class Memory:
    def __init__(self):
        self._FIRST_REGISTER = 41
        self._LAST_REGISTER = 15999
        # self.openMemory = [] #list of open goals, they get deleted when in use and added when freed
        self._used_memory = SortedDict({}) # {start: StoreddMemory}
        self._open_memory = SortedDict({41:15999}) # {start: end}
    
    @property
    def free_memory_count(self):
        return sum([end - start for start, end in self._open_memory.items()])   
    
    @property
    def used_memory_count(self):
        return sum([var.length for var in self._used_memory.values()])

    def malloc(self, var_name, var_type, front=True):
        length = class_constructers[var_type]
        free_space_start = self.find_open_space(length, front)
        
        free_space_end = self._open_memory.pop(free_space_start)
        self._open_memory[free_space_start + length] = free_space_end

        self._used_memory[var_name] = StoredMemory(var_name, var_type, length, free_space_start)

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


    def find_open_space(self, length, front=True):
        if front:
            temp_open_memory = self._open_memory
        else:
            temp_open_memory = reversed(self._open_memory)
        for start, end in temp_open_memory.items():
            if end - start >= length:
                return start
        raise Exception("Out of memory")
