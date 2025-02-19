#IF
1: if test -> jump 3
2: jump 5
3: random
4: random

#While Loop
1: jump 3
2: do_body
3: if test -> jump 2

#for Loop
1: i = 0
2: jump 5
3: do_body
4: i += 1
5: if test -> jump 3

#break
jump to 1 after the loop

#continue
jump to the last one (aka the conditional)

# return positon reg 
# return value reg

1 RETURN    = 9
2 circle    = 30
3 squars    = None
4 RET_POS   = final = circle + squars
5 RET_VAL   = 3
6 NEXT_RET  = None
7 .x        = 100
8 .y        = 400 
9 RET_POS   = z = x+y
10 RET_VAL  = 8
11 NEXT_RET = 4
12 ..x      = 20


"""
def function(Args):
    lines
    return statment

Variable = function(arg)

aloc  variable  return to if not alocated
aloc  RET_block (RET_pos, RET_next_pt, RET_var_pt)

set   RET_pos
set   RET_next_pt to    RETURN_pt
set   RET_var_pt  to    Variable 
set   RETURN_pt   to    RET_Block(register)

ADD   function    to    CALLSTACK

aloc  Args
set   Args        to    args

DO    FUNCTION LINES

Set   RET_var     to    return statment

POP   function    from  CALLSTACK   (un-al all vars in funtion)

un-al args
un-al RET_block
"""

def square(x):
  return x*x

def add_squares(x,y):
  x = square(x)
  y = square(y)
  z = x+y
  return y

circle = 30
squars = add_squares(10,20)
final = circle + squars