from scraper.aoe2scriptFunctions import *
from scraper.aoe2scriptEnums import *

iddle_villager_count = 6
iddle_villager_count = up_get_fact(FactId.idle_farm_count)
if True:
    up_assign_builders(BuildingId.barracks, iddle_villager_count)
if up_assign_builders(BuildingId.barracks, iddle_villager_count):
    pass


