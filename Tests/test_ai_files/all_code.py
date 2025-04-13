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
    Formation,
    Integer,
    Constant,
)

def resource_total(r: Resource) -> Integer:
  search_state = State()
  up_full_reset_search()
  up_filter_status(ObjectStatus.status_resource, ObjectList.list_active)
  up_find_resource(r, 20)
  up_get_search_state(search_state)
  total = 0
  temp = 0
  up_set_target_object(SearchSource.search_remote, i)
  up_get_object_data(ObjectData.object_data_carry, temp)
  temp += temp
  total += temp
  up_chat_data_to_all("Total:%d", total)
  return total