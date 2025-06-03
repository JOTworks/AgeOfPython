#BAD BUGS
#todo: allow Array to be assigned touples, currenlty just uses first slice no matter what get_offset() may be culprit
#! a = Array(Point, 10)
#! w = 5
#! a[w] = (1,2)
#! a[5] = (1,2)
#todo: BUG if you do x = func() and x is not constructed it will just not give it a value... no error thrown
#todo: BUG if you have a file name nomads.py and nomads_nf.py
#todo: BUG else statments dont work in functions!

#OPTIMIXSTION
# Un-Optimized custom functions: get_name_at_location, visit_Constant, get_function_list_typeOp, get_enum_classes
# Checking type: isclass, builtins.issubclass, builtins.isinstance
# Getting Attributes: _getmembers, builtins.getattr
# Sorting: 'sort' of 'list' objects

#SCRAPER
#todo: fix scrping to pull all *s, make sure nothing is missing
#todo: make it a 1 button run

#MAIN
#todo: fix all the parameters for user and printing / error logging
#todo: SOMEHOW THROW ERROR IF FILE IS OPEN AND NOT EDITED!

#MEMORY
#todo: make it actual allocation for the function return values and pointers, to get rid of magic numbers

#COMPILER
#todo: fixe compare op enums in function (not useing shortcut)
#todo: fix variable compare to enum. expecialy with == even if other is disable
#todo: get nested binOp expressions working
#todo: get expressions working in conditionals
#todo: x < y < z is not implemented, currently have to use x < y and y < z
#todo: abs_dx = -dx if dx < 0 else dx is not implemented, needs own lines
#todo: abs_dx = -dx  not implemtned, needed to abs_dx = dx * -1
#todo: return (center_x, center_y) not implemented, needed to return_point = (center_x, center_y); return return_point
#todo: does not throw error when wood_amount() uses the compare drop but dont asctuly compare... instead it just had an AOE2 error in engine
    

#FUNCTION ISSUES
#todo: if elses dont seem to work in functinos
#todo: for loops in functions (maybe all) asigning a variable to an array does not initialize it
    #todo: for i in range(10):
    #todo:      explorer_id = J_explore_object_ids[i]
