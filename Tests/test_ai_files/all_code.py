#all_code
from scraper.aoe2scriptFunctions import *
from scraper.aoe2scriptFunctions import (
    can_build,
    build,
    chat_to_all,
    up_can_research,
    research,
    can_train,
    train,
)
from scraper.aoe2scriptEnums import *
from scraper.aoe2scriptEnums import (
    BuildingId,
    UnitId,
    TechId,
)

if can_build(BuildingId.farm):
    build(BuildingId.farm)
else:
    chat_to_all("Cannot build farm")


def try_research(tech_id: TechId):
    if up_can_research(0, tech_id):
        up_research(0, tech_id)

if can_train(UnitId.villager):
    train(UnitId.villager)

try_research(TechId.feudal_age)
try_research(TechId.ri_loom)