import enum

class Structure(enum.Enum):
    CONST = 0
    INT = 1
    POINT = 2
    STATE = 4

class TokenType(enum.Enum):
    END_LINE = 0
    LEFT_PAREN = 1      #length: 1
    RIGHT_PAREN = 2     #length: 1
    LOGIC_OP = 3
    COMMA = 4
    COLON = 5           #length: 1
    ARROW = 6           #length: 2
    OPERATOR = 7
    POINTER = 8
    NUMBER = 9
    # Variable length tokens:
    STRING = 10
    COMMENT = 11
    IDENTIFIER = 12
    WHITE_SPACE = 13
    # Keywords:
    DEFCONST = 14
    DEFRULE = 15
    IF = 16
    ELSE = 17
    ELIF = 18
    FOR = 19
    WHILE = 20
    DEF = 21
    # Comment keywords:
    LOAD_IF = 22
    UNIDENTIFIED = 24
    UNCAUGHT = 25
    TABS = 26
    IN = 27
    RANGE = 28
    EQUALS = 29
    MATHOP = 30
    RETURN = 31
    LOAD = 32
    LOAD_RANDOM = 33
    STRATEGIC_NUMBER = 34
    LAST_RULE = 35
    FIRST_RULE = 36
    SECOND_RULE = 37
    TYPEOP = 38
    COMPAREOP = 39
    INCREMENTER = 40
    DECREMENTER = 41
    RETURN_VAR_TOKEN = 42
    RETURN_POINT = 43
    ARROW_SMALL = 44
    VAR_INIT = 45
    BLOCK = 46
    BLOCK_END = 47
    BLOCK_START = 48
    COMMAND = 49
