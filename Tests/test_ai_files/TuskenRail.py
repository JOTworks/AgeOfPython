#testing pushs
from scraper import *
from scraper import (
    up_find_local, 
    up_set_target_object, 
    disable_self,
    up_get_point,
    up_chat_data_to_player,
    unit_type_count,
    chat_to_player,
    set_strategic_number,
    true,
    housing_headroom,
    build,
    can_build,
    train,
    can_train,
    research,
    food_amount,
    building_type_count_total,
    up_get_search_state,
    up_find_resource,
    up_filter_status,
    up_full_reset_search,
    resource_found,
    can_research,
    up_send_flare,
    )
from scraper import (
    SN,
    UnitId,
    PlayerNumber,
    Age,
    PositionType,
    BuildingId,
    SearchSource,
    ObjectList,
    ObjectStatus,
    Resource,
    ClassId,
    TechId,
    )
from scraper import (
  Point,
  State,
)
"""
#**************************************************************************
# --------------------------FUNCTIONS--------------------------------------
#**************************************************************************
def printD(string, player_number):
  (up-chat-data-to-player my-player-number string g: player_number)

def set_gather_percent(food, wood, gold, stone):
  set_strategic_number( sn-food-gatherer-percentage food)
  set_strategic_number( sn-wood-gatherer-percentage wood)
  set_strategic_number( sn-gold-gatherer-percentage gold)
  set_strategic_number( sn-stone-gatherer-percentage stone)

def get_type_at_point(in_point):
  (up-chat-data-to-player my-player-number "testing Point %d" g: in_point.x)
  (up-chat-data-to-player my-player-number "testing Point %d" g: in_point.y)
  id = 0
  (up-get-point-contains in_point id c: -1)
  (up-set-target-by-id g: id)
  output = 0
  (up-get-object-data object-data-class output)
  (up-chat-data-to-player my-player-number "class: %d" g: output)
  (up-get-object-data object-data-type output)
  (up-chat-data-to-player my-player-number "type: %d" g: output)

  #for i in range(0,1000):
  #  if (up-get-point-contains tracking_point trash c: i):
  #    (up-chat-data-to-player my-player-number "value: %d" g: i)

def get_resource_bounds(resource_type, point_UP_LF, point_DW_RT):
  test_point = Point()
  point_UP_RT = Point()
  point_DW_LF = Point()
  move_UP = False
  move_LF = False
  move_RT = False
  move_DW = False
  isEmpty_UP = False
  isEmpty_LF = False
  isEmpty_RT = False
  isEmpty_DW = False
  trash = 0
  isEmpty = False
  if(goal isEmpty_UP True)(goal isEmpty_LF True)(goal isEmpty_RT True)(goal isEmpty_DW True):
    isEmpty = True

  while (goal isEmpty False):
    move_UP = False
    move_LF = False
    move_RT = False
    move_DW = False
    
    point_UP_LF.x += 1 #up
    point_UP_LF.y += 1 #left
    point_DW_RT.x -= 1 #down
    point_DW_RT.y -= 1 #right
    #these 2 points are just needed to compare the corners with
    point_UP_RT.x = point_UP_LF.x
    point_UP_RT.y = point_DW_RT.y
    point_DW_LF.x = point_DW_RT.x
    point_DW_LF.y = point_UP_LF.y
    if (up-get-point-contains point_UP_LF trash c: resource_type):
      (chat-to-player my-player-number "UP_LF corner YES")
      move_UP = True
      move_LF = True
      isEmpty_UP = False
      isEmpty_LF = False
    if (up-get-point-contains point_UP_RT trash c: resource_type):
      (chat-to-player my-player-number "UP_RT corner YES")
      move_UP = True
      move_RT = True
      isEmpty_UP = False
      isEmpty_RT = False
    if (up-get-point-contains point_DW_RT trash c: resource_type):
      (chat-to-player my-player-number "DW_RT corner YES")
      move_DW = True
      move_RT = True
      isEmpty_DW = False
      isEmpty_RT = False
    if (up-get-point-contains point_DW_LF trash c: resource_type):
      (chat-to-player my-player-number "DW_LF corner YES")
      move_DW = True
      move_LF = True
      isEmpty_DW = False
      isEmpty_LF = False
 
    #left to right
    if (goal move_UP False)(goal isEmpty_UP False):
      test_point.x = point_UP_LF.x
      test_point.y = point_UP_LF.y - 1
      while(up-compare-goal test_point.y g:> point_DW_RT.y):
        if (up-get-point-contains test_point trash c: resource_type):
          move_UP = True
          #break
        test_point.y -= 1 
    if (goal move_DW False)(goal isEmpty_DW False):
      test_point.x = point_DW_RT.x
      test_point.y = point_UP_LF.y - 1
      while(up-compare-goal test_point.y g:> point_DW_RT.y):
        if (up-get-point-contains test_point trash c: resource_type):
          move_DW = True
          #break
        test_point.y -= 1
   
    #top to bottom
    if (goal move_LF False)(goal isEmpty_LF False):
      test_point.x = point_UP_LF.x - 1
      test_point.y = point_UP_LF.y
      while(up-compare-goal test_point.x g:> point_DW_RT.x):
        if (up-get-point-contains test_point trash c: resource_type):
          move_LF = True
          #break
        test_point.x -= 1
    if (goal move_RT False)(goal isEmpty_RT False):
      test_point.x = point_UP_LF.x - 1
      test_point.y = point_DW_RT.y
      while(up-compare-goal test_point.x g:> point_DW_RT.x):
        if (up-get-point-contains test_point trash c: resource_type):
          move_RT = True
          #break
        test_point.x -= 1
    
    if (goal move_UP False):
      point_UP_LF.x -= 1
    if (goal move_LF False):
      point_UP_LF.y -= 1
    if (goal move_DW False):
      point_DW_RT.x += 1
    if (goal move_RT False):
      point_DW_RT.y += 1
  
  (chat-to-player my-player-number "wwooooord")
  (up-chat-data-to-player my-player-number ": UP %d" g: point_UP_LF.x)
  (up-chat-data-to-player my-player-number "  LT %d" g: point_UP_LF.y)
  (up-chat-data-to-player my-player-number "  DW %d" g: point_DW_RT.x)
  (up-chat-data-to-player my-player-number "  RT %d" g: point_DW_RT.y)
  state_UP_LF_DW_RT = State()
  state_UP_LF_DW_RT.0 = point_UP_LF.x
  state_UP_LF_DW_RT.1 = point_UP_LF.y
  state_UP_LF_DW_RT.2 = point_DW_RT.x
  state_UP_LF_DW_RT.3 = point_DW_RT.y
  
  return state_UP_LF_DW_RT

#def find_next_house_point(house_position, resource_center):
#  #if central
#  return_point = house_position
#  house_position_y_min_1 = house_position.y-1
#  if(resource_center.y == house_position.y or resource_center.y == house_position_y_min_1):
#    if resource_center.x > house_position.x:
#      return_point.x += 3
#    else :
#      return_point.x -= 3
#    return return_point
#  house_position_x_plus_1 = house_position.x+1
#  if(resource_center.x == house_position.x or resource_center.x == house_position_x_plus_1):
#    if resource_center.y > house_position.y:
#      return_point.y += 3
#    else :
#      return_point.y -= 3
#    return return_point
#  
#  #if diagnal
#  if(resource_center.y < house_position.y):
#    if(resource_center.x < house_position.x):
#      if(resource_center.x-house_position.x <= resource_center.y-house_position.y):
#        return_point.x -= 3
#        return_point.y -= 1
#      else :
#        return_point.x -= 1
#        return_point.y -= 3
#    else :
#      if(house_position.x-resource_center.x <= resource_center.y-house_position.y):
#        return_point.x += 3
#        return_point.y -= 1
#      else :
#        return_point.x -= 3
#        return_point.y += 1
#  else :
#    if(resource_center.x < house_position.x):
#      if(house_position.x-resource_center.x <= resource_center.y-house_position.y):
#        return_point.x -= 1
#        return_point.y += 3
#      else :
#        return_point.x -= 3
#        return_point.y += 1
#    else :
#      if(resource_center.x-house_position.x <= resource_center.y-house_position.y):
#        return_point.x += 1
#        return_point.y += 3
#      else :
#        return_point.x += 3
#        return_point.y += 1
#  return return_point
"""
#**************************************************************************
# -----------------------------CODE----------------------------------------
#**************************************************************************


search_state = State()
#Our first age status is that we are in the dark age. Post Imp games will require a different definition
if True:
  age_status = Age.dark_age
  disable_self()

tc_location = Point()
if up_find_local(BuildingId.town_center, 1):
  up_set_target_object(SearchSource.search_local, 0)   
  up_get_point(PositionType.position_object, tc_location)
  up_chat_data_to_player(PlayerNumber.my_player_number, "tc_location x %d", tc_location.x)
  up_chat_data_to_player(PlayerNumber.my_player_number, "tc_location x %d", tc_location.y)
  disable_self()

if True: # set counts
  round_count_2 = 0
  round_count_10 = 0
  round_count_100 = 0
  round_count_1000 = 0
  disable_self()

#count counts
round_count_2 += 1
round_count_10 += 1
round_count_100 += 1
round_count_1000 += 1
if round_count_2 >= 2:
  round_count_2 = 0
if round_count_10 >= 10:
  round_count_10 = 0
if round_count_100 >= 100:
  round_count_100 = 0
if round_count_1000 >= 1000:
  round_count_1000 = 0

if (True): #set strategic_number starting
  chat_to_player(PlayerNumber.my_player_number, "Scouting with villagers and, scout")
  SN.cap_civilian_explorers=0
  SN.number_explore_groups=0
  SN.cap_civilian_builders=100
  SN.cap_civilian_gatherers=0
  # SN.cap_civilian_explorers=0
  SN.initial_exploration_required=0
  SN.maximum_food_drop_distance=10
  SN.maximum_gold_drop_distance=10
  SN.maximum_hunt_drop_distance=20
  SN.maximum_stone_drop_distance=10
  SN.maximum_wood_drop_distance=10
  # SN.isable_villager_garrison=3
  SN.percent_civilian_explorers=0
  SN.minimum_civilian_explorers=0
  SN.cap_civilian_explorers=0
  SN.total_number_explorers=1
  SN.number_explore_groups=1
  SN.cap_civilian_builders=100
  SN.percent_civilian_builders=100
  SN.initial_exploration_required=0
  disable_self()

#-------------------Dark Age Econ-------------------------
#if age_status == Age.dark_age:
#  set_gather_percent(100, 0, 0, 0)
#if age_status == Age.dark_age and unit_type_count(UnitId.villager, '==', 7):
#  set_gather_percent(85, 15, 0, 0)
#if age_status == Age.dark_age and unit_type_count(UnitId.villager, '==', 8):
#  set_gather_percent(75, 25, 0, 0)
#if age_status == Age.dark_age and unit_type_count(UnitId.villager, '==', 11):
#  set_gather_percent(69, 31, 0, 0)
#if age_status == Age.dark_age and unit_type_count(UnitId.villager, '==', 13):
#  set_gather_percent(70, 30, 0, 0)
#if age_status == Age.dark_age and unit_type_count(UnitId.villager, '==', 15):
#  set_gather_percent(71, 29, 0, 0)
#if age_status == Age.dark_age and unit_type_count(UnitId.villager, '==', 17):
#  set_gather_percent(63, 37, 0, 0)
#if age_status == Age.dark_age and unit_type_count(UnitId.villager, '==', 19):
#  set_gather_percent(70, 30, 0, 0)

#-----------------------------------------------------------
if can_train(UnitId.villager):
  train(UnitId.villager)

if can_build(BuildingId.house) and housing_headroom('<',3):
  build(BuildingId.house)

if (can_research(TechId.ri_loom) 
    and building_type_count_total(BuildingId.house,'>',1) 
    and (food_amount('<',50) or (housing_headroom('<',1) and not can_build(BuildingId.house)))
   ):
  research(TechId.ri_loom)
  disable_self()

#berry_uper = Point()
#berry_lower = Point()
#trash = 0

#if resource_found(Resource.food): #calculate berry bushes
#  up_full_reset_search()
#  up_filter_status(ObjectStatus.status_resource, ObjectList.list_active)
#  up_find_resource(Resource.food, 20)
#  up_get_search_state(search_state)
#  if True: #flares the first run
#    up_set_target_object(SearchSource.search_remote, 0) 
#    temp_point = Point()
#    up_get_point(PositionType.position_object, temp_point)
#    up_send_flare(temp_point)
#    berry_uper = temp_point
#    berry_lower = temp_point
#    #get_type_at_point(berry_uper)
#    berry_state = State()
#    #berry_state = get_resource_bounds(ClassId.forage_class, berry_uper, berry_lower)
#    berry_uper.x = berry_state[0]
#    berry_uper.y = berry_state[1]
#    berry_lower.x = berry_state[2]
#    berry_lower.y = berry_state[3]
#    #(up-chat-data-to-player my-player-number "upper %d x" g: berry_uper.x)
#    #(up-chat-data-to-player my-player-number "upper %d y" g: berry_uper.y)
#    #(up-chat-data-to-player my-player-number "lower %d x" g: berry_lower.x)
#    #(up-chat-data-to-player my-player-number "lower %d y" g: berry_lower.y)
#    #set_resource_boundry(forage-class, berry_uper, berry_lower)
#    disable_self()
#
##recalculate berry bushes
#if resource_found(Resource.food) and round_count_10 == 0: 
#  #berry_state = get_resource_bounds(ClassId.forage_class, berry_uper, berry_lower)
#  berry_uper.x = berry_state[0]
#  berry_uper.y = berry_state[1]
#  berry_lower.x = berry_state[2]
#  berry_lower.y = berry_state[3]
  
