#all_code
from scraper.aoe2scriptFunctions import *
from scraper.aoe2scriptFunctions import (
    can_build,
    build,
)

from scraper.aoe2scriptEnums import *
from scraper.aoe2scriptEnums import (
    BuildingId,
)

if can_build(BuildingId.farm):
    build(BuildingId.farm)
else:
    chat_to_all("Cannot build farm")
