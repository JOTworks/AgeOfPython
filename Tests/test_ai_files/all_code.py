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
def add_points(p1:Point, p2:Point) -> Point:
    p1 = p1+p2
    return p1

loc = Point()
tc_l = Point()
new_p = Point()
new_p = add_points(loc, tc_l)


#final = myArray[test] + 3 + 4 + final
#final = myArray[test] #first asigment should be forced to a c:=, and 3rd and 4th may be able to be combined
#myArray[test] = final #find out where this happens because it just does one goal and that not helpful. Try to combine them, so everytime and array is found it can use the fake array register!
