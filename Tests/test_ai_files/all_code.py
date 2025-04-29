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
#J_EXPLORE_OBJECT_ARRAY_SIZE = Constant(3)
#J_explore_object_ids = Array(Integer, J_EXPLORE_OBJECT_ARRAY_SIZE)
#EMPLOYED = Constant(1)
#UNEMPLOYED = Constant(0)
#
#def J_get_employment_status(id:Integer) -> Integer:
#    global J_explore_object_ids
#    global J_EXPLORE_OBJECT_ARRAY_SIZE
#    i = Integer(0)
#    for i in range(J_EXPLORE_OBJECT_ARRAY_SIZE):
#        array_explorer_id = J_explore_object_ids[i]
#        if array_explorer_id == id:
#            return EMPLOYED
#    return UNEMPLOYED

outside = 12

def explore(test:Integer) -> Integer:
    global outside
    outside += 1
    return outside

myTest = 44
explore(myTest)