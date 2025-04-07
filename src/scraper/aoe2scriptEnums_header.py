# --- Removed parameters --- #
# all of the parameter types from the website with their IDs.
# mathops and comparison ops are handdled by the intepreter.
#
from aenum import Enum
class Strenum(Enum):

    @property
    def value(self):
        return self.values[0]

    @property
    def string(self):
        if type(self.value) is tuple and len(self.value) > 1 and type(self.value[1]) is str:
            return self.value[1]
        return self.name


class AOE2VarType():
    params_to_offet = {
        'LocalIndex':0,
        'LocalList':1,
        'RemoteIndex':2,
        'RemoteList':3,
    }
    @classmethod
    def get_offset(cls, abstracted_offset):
        return cls.params_to_offet.get(abstracted_offset, None)

class State(AOE2VarType):
    params_to_offet = {
        'LocalIndex':0,
        'LocalList':1,
        'RemoteIndex':2,
        'RemoteList':3,
    }
    length = 4
    def __init__(self):
        self.LocalIndex = None
        self.LocalList = None
        self.RemoteIndex = None
        self.RemoteList = None
    
class Point(AOE2VarType):
    params_to_offet = {
        'x':0,
        'y':1,
    }
    length = 2
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

class Constant(AOE2VarType):
    length = 1
    def __init__(self, value):
        self.value = value
    @classmethod
    def get_offset(cls, abstracted_offset):
        raise Exception(f"Constant do not have offsets or memory locations {abstracted_offset=}")

class Integer(AOE2VarType):
    length = 1
    def __init__(self, value = None):
        self.value = value

class FuncCall():
    pass #added manually