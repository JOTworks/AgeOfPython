# --- Removed parameters --- #
# all of the parameter types from the website with their IDs.
# mathops and comparison ops are handdled by the intepreter.
#
from aenum import Enum
class Strenum(Enum):

    @property
    def val(self):
        return self.value[0]

    @property
    def string(self):
        if type(self.value) is tuple and len(self.value) > 1 and type(self.value[1]) is str:
            return self.value[1]
        return self.name

_ = "DEFAULT VALUE" # default value for all optional enums
class AOE2VarType():
    pass

class Array(AOE2VarType):

    @property
    def length(self):
        return self.length
    
    def __init__(self, length):
        if type(length) is not int and length < 0:
            raise Exception(f"Array length {length} is not valid")
        self.length = length

class Timer(AOE2VarType):
    params_to_offet = {
        0:0,
    }
    length = 1
    
class State(AOE2VarType):
    params_to_offet = {
        'LocalIndex':0,
        0:0,
        'LocalList':1,
        1:1,
        'RemoteIndex':2,
        2:2,
        'RemoteList':3,
        3:3,
    }
    length = 4
    def __init__(self):
        self.LocalIndex = None
        self.LocalList = None
        self.RemoteIndex = None
        self.RemoteList = None
    
class Point(AOE2VarType): #todo: this colides with Point parmater, fix that someitme
    params_to_offet = {
        'x':0,
        0:0,
        'y':1,
        1:1,
    }
    length = 2
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

class Constant(AOE2VarType):
    params_to_offet = {
        0:0,
    }
    length = 1
    def __init__(self, value):
        self.value = value

class Integer(AOE2VarType):
    params_to_offet = {
        0:0,
    }
    length = 1
    def __init__(self, value = None):
        self.value = value
class Boolean(AOE2VarType):
    params_to_offet = {
        0:0,
    }
    length = 1
    def __init__(self, value = None):
        self.value = value
class FuncCall():
    pass #added manually