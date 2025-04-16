from scraper import AOE2OBJ, Point, State, Integer, Boolean, AOE2VarType, aoe2scriptEnums, Array
from sortedcontainers import SortedDict
from utils_display import print_bright, print_dim
from pprint import pprint
import ast
import inspect

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
        out_string = f"{self.var_type.__name__ if hasattr(self.var_type,'__name__') else self.var_type.name}" + reg_str

        return out_string

class StoredFuncCall(StoredMemory):
    def __init__(self, name, length, start, arguments):
        super().__init__(name, AOE2OBJ.FuncCall, length, start)
        self.func = name
        self.arguments = arguments
class Memory:
    def __init__(self):
        self.verbose_memory = False #todo: make this an option
        self._FIRST_REGISTER = 41
        self._LAST_REGISTER = 15799 #15900 - 15999 is for the function stack, 15800 - 15899 is for function returns
        # self.openMemory = [] #list of open goals, they get deleted when in use and added when freed
        self._func_stack = ["main"]
        self._used_memory = {"main":SortedDict({})}  # {scope: SortedDict({varname: StoreddMemory})}
        self._func_blocks = SortedDict({})  # {start: StoredFuncCall}
        self._open_memory = SortedDict({self._FIRST_REGISTER: self._LAST_REGISTER})  # {start: end}

        classes = [cls for name, cls in inspect.getmembers(aoe2scriptEnums, inspect.isclass) if issubclass(cls, AOE2VarType) and cls is not AOE2VarType]
        self.class_constructer_default_size = {cls:cls.length for cls in classes if cls.length}

    def print_memory(self):
        print(f"{self.free_memory_count=}")
        pprint(self._open_memory)
        print(f"{self.used_memory_count=}")
        pprint(self._used_memory)
        print(f"_func_blocks")
        pprint(self._func_blocks)

    @property
    def free_memory_count(self):
        return sum([end + 1 - start for start, end in self._open_memory.items()])

    @property
    def used_memory_count(self):
        return sum(sum([var.length for var in used_memory_scope.values()]) for used_memory_scope in self._used_memory.values())

    def used_memory_in_scope(self, scope = -1):
        if scope == -1:
            scope = self._func_stack[-1]
        return self._used_memory[scope]
    
    def malloc_func_call(self, func, arguments):
        #todo: coppied code from malloc, find out if i should consolidate
        length = 3 + len(arguments)
        free_space_start = self.find_open_space(length)
        free_space_end = self._open_memory.pop(free_space_start)
        self._open_memory[free_space_start + length] = free_space_end

        self._func_blocks[func] = StoredFuncCall(
            func, length, free_space_start, arguments
        )
        if self.verbose_memory:
            print_bright(f"MALF: {func} {arguments} {free_space_start}")
            self.print_memory()

    def malloc(self, var_name, var_type, length=None, front=True):
        if var_type is AOE2OBJ.Point:
            var_type = Point
        if var_type is AOE2OBJ.State:
            var_type = State
        if var_type is AOE2OBJ.Integer:
            var_type = Integer
        if var_type is AOE2OBJ.Boolean:
            var_type = Boolean
        if var_type is AOE2OBJ.Array:
            var_type = Array
        if length and var_type is not Array:
            raise Exception("Length can only be specified for list types")
        if not length:
            length = self.class_constructer_default_size[var_type]
        free_space_start = self.find_open_space(length, front)

        free_space_end = self._open_memory.pop(free_space_start)
        self._open_memory[free_space_start + length] = free_space_end

        self.used_memory_in_scope()[var_name] = StoredMemory(
            var_name, var_type, length, free_space_start
        )
        if self.verbose_memory:
            print_bright(f"MALO: {var_name} {var_type} {length} {free_space_start}")
            self.print_memory()

    def free(self, var_name, scope = -1, front=True):
        var = self.used_memory_in_scope.pop(var_name, scope)

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
        
        if self.verbose_memory:
            print_dim(f"FREE: {var_name} {var.var_type} {var.length} {var.start}")
            self.print_memory()

    def get_name_at_location(self, reg_number):
        for scope, memory_dict in self._used_memory.items():
            for start, stored_memory in memory_dict.items():
                if stored_memory.start <= reg_number <= stored_memory.start + stored_memory.length - 1:
                    name = str(stored_memory.name) + "-" + str(reg_number - stored_memory.start)
                    return name
        raise Exception(f"could not find {reg_number} in {self._used_memory}")

    def get(self, var_name, abstracted_offset=None):
        try:
            stored_memory = self.used_memory_in_scope()[var_name]
        except KeyError:
            return None
        
            
        offset = stored_memory.var_type.get_offset(abstracted_offset, stored_memory.length)
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
        self.print_memory()
        raise Exception(f"Out of memory trying to allocate {length} registers")
