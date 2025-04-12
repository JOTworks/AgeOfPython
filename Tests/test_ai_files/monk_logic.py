#testing pushs
from scraper import *
from scraper import (
    up_find_local, 
    up_set_target_object, 
    disable_self,
    build,
    train,
    can_train,
    research,
    up_get_search_state,
    can_research,
    chat_to_all,
    building_type_count,
    unit_type_count_total,
    up_reset_search,
    up_find_remote,
    up_target_objects,
    )
from scraper import (
    SN,
    UnitId,
    BuildingId,
    SearchSource,
    TechId,
    compareOp,
    DUCAction,
    )
from scraper import (
  State,
)

gl_state = State()

if True:
    monk_target = -1
    disable_self()

if building_type_count(BuildingId.monastery, compareOp.less_than, 1): #should be building_type_count(BuildingId.monastery) < 1
  build(BuildingId.monastery)

if can_research(TechId.ri_redemption):
  research(TechId.ri_redemption)

if unit_type_count_total(UnitId.monk, compareOp.less_than, 1) and can_train(UnitId.monk):
  train(UnitId.monk)

if monk_target == -1:
    chat_to_all("looking")
    up_reset_search(1, 1, 1, 1)
    up_find_local(UnitId.monk, 1) 
    SN.focus_player_number = 2
    up_find_remote(BuildingId.stable, 1) 
    up_get_search_state(gl_state.remoteList) #! todo: fix state attr to be auto as well! and not in memory

if gl_state.remoteList > 0:
  chat_to_all("found stable")

if gl_state.localList > 0:
  chat_to_all("found monk")

if (
   gl_state.remoteList > 0 and 
   gl_state.localList > 0 and
   monk_target == -1
    ):
  chat_to_all("converting")
  up_set_target_object(SearchSource.search_remote, 0)
  up_target_objects(0,DUCAction.action_default, -1, -1)