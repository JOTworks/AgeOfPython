#all_code
from scraper import *
from scraper import Integer, Boolean, Point, State, Constant, Array, Timer
from scraper import (
    can_build,
    build,
    chat_to_all,
    up_can_research,
    research,
    can_train,
    train,
    up_build,
    BuildingId,
    UnitId,
    TechId,
    PlacementType,
    up_target_objects,
    Formation,
    Integer,
    Constant,
)

#test = Integer()
#final = Integer()
#test = final*final + 12
def add_points(p1:Point) -> (Point, Point):
    p3 = Point()
    return p1, p3

loc = Point()
new_p = Point()
new_p, loc = add_points(loc)
new_p, loc = ((1,1),(2,2))


#def one_ret() -> Point:
#    myPoint = Point()
#    return myPoint
#
#loc = Point()
#loc = one_ret()
##lengths are the same
#new_p = loc
#new_p = (0,1)
#x = 0
#y = 1
#x,y = x+4,y
#
###right side 1
##    #left side 1
##new_p += (x,(x,y))
##
##    #left side length of right side
##x,y,z = loc
#
##dont allow this
#x = y = 0



#final = myArray[test] + 3 + 4 + final
#final = myArray[test] #first asigment should be forced to a c:=, and 3rd and 4th may be able to be combined
#myArray[test] = final #find out where this happens because it just does one goal and that not helpful. Try to combine them, so everytime and array is found it can use the fake array register!
