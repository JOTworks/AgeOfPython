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

ARRAY_LENGTH = Constant(10)

myArray = Array(Point, ARRAY_LENGTH)


myArray2 = Array(Integer, 2)