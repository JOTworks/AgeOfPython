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


JOB_TIMER_1 = Timer()
TIMER_2 = Timer()
up_timer_status(JOB_TIMER_1) == 0
TIMER_2 = Timer()
TIMER_2 = 1