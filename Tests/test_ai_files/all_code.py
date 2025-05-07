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

i = Integer(2)
J_explore_object_things = Array(Integer, 10) #J_EXPLORE_OBJECT_ARRAY_SIZE
out_thing = J_explore_object_things[i]
def J_explore_object():
    global J_explore_object_things

    for i in range(10): #J_EXPLORE_OBJECT_ARRAY_SIZE
        thing = J_explore_object_things[i]