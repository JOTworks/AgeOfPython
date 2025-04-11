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
    up_build,
    BuildingId,
    UnitId,
    TechId,
    PlacementType,
    up_target_objects,
    Formation
)



up_target_objects(0)

up_target_objects(0, _, Formation.formation_box, _)

up_target_objects(0, DUCAction.action_delete, Formation._1, AttackStance._1)


up_build(PlacementType.place_normal, 0, BuildingId.house)