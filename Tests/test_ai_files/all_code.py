#all_code
from scraper import *
from scraper import Integer as int, Boolean as bool
from scraper import (
    can_build,
    build,
    chat_to_all,
    up_can_research,
    research,
    can_train,
    train,
    BuildingId,
    UnitId,
    TechId,
)

if can_build(BuildingId.farm):
    build(BuildingId.farm)
else:
    chat_to_all("Cannot build farm")


def try_research(tech_id: TechId) -> int:
    if up_can_research(0, tech_id):
        up_research(0, tech_id)
        return 1
    else:
        chat_to_all("Cannot research")
        return 3
    
    return

table = try_research(TechId.ri_loom)