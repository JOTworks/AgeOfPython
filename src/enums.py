import enum

class Structure(enum.Enum):
    POINT = 2
    STATE = 4

class TokenType(enum.Enum):
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
    FOR = 18
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
    SECOND_RULE = 36
    TYPEOP = 27
