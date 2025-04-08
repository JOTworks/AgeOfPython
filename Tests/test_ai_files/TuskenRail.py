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

def set_gatherer_percentages(wood, food, gold, stone):
    SN.wood_gatherer_percentage = wood
    SN.food_gatherer_percentage = food
    SN.gold_gatherer_percentage = gold
    SN.stone_gatherer_percentage = stone

def try_research(tech_id: TechId):
    if up_can_research(0, tech_id):
        research(tech_id)

if True:
    SN.cap_civilian_builders = 200
    SN.percent_civilian_builders = 100
    SN.disable_builder_assistance = 0
    SN.consecutive_idle_unit_limit = 1
    SN.do_not_scale_for_difficulty_level = 1
    SN.enable_boar_hunting = 1
    SN.enable_offensive_priority = 1
    SN.enable_patrol_attack = 1
    SN.initial_exploration_required = 0
    SN.maximum_fish_boat_drop_distance = 30
    SN.maximum_food_drop_distance = 20
    SN.maximum_gold_drop_distance = 20
    SN.maximum_hunt_drop_distance = 30
    SN.maximum_stone_drop_distance = 20
    SN.scale_minimum_attack_group_size = 0
    SN.task_ungrouped_soldiers = 0
    SN.allow_civilian_defense = 1
    SN.allow_civilian_offense = 1
    SN.percent_attack_soldiers = 95
    SN.number_attack_groups = 2
    SN.maximum_town_size = 255
    SN.number_civilian_militia = 6
    SN.enable_new_building_system = 1 #I added this for stone mining
    SN.camp_max_distance = 300
    SN.zero_priority_distance = 255
    SN.cap_civilian_explorers = 0
    SN.number_explore_groups = 1
    chat_to_all("glhf")
    disable_self()


try_research(TechId.feudal_age)
try_research(TechId.ri_loom)

if unit_type_count(UnitId.villager) == 8:
   set_gatherer_percentages(25,75,0,0)
   disable_self()

if current_age() == Age.feudal_age:
    set_gatherer_percentages(40, 35, 15, 10)
    disable_self()

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


if can_build(BuildingId.house) and housing_headroom() < 3:
  build(BuildingId.house)

if (can_research(TechId.ri_loom) 
    and building_type_count_total(BuildingId.house) > 1
    and (food_amount() < 50 or (housing_headroom() < 1 and not can_build(BuildingId.house)))
   ):
  research(TechId.ri_loom)
  disable_self()

if can_research(TechId.ri_loom):
   research(TechId.ri_loom)

if can_train(UnitId.villager):
  train(UnitId.villager)

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
  
#=================SHEEP CLAIM AND DEER LURE==============================================================#
#
# Basically, this code just searches around the scout for gaia sheep and, if it finds any, tasks the 
# scout to the nearest one, resetting the scout a few seconds after none are found anymore.
# 
# Essentially, once you have left time for the scout to explore your base, finds the closest deer to 
# the tc and directs the scout to the tile just behind it from the tc, thus pushing the deer forward. 
# Once the deer is close enough to the tc, task villagers to shoot the deer and reset the system for the 
# next deer. Continue like this until there are no more deer or it is time to scout for the enemy.
#
#=================By FireBall37==========================================================================#
#todo: make variable delcarations work, variable types like state, point, etc
#make it so all memeory types in my allocator are classes that inherit from same classs.
#then we could also allow them to have specific attributes and even each have their own call num
#todo: make initialization with numbers work
#todo: make Constant initialization work so we dont need to use goals for all of those! (just make a defrule I think)

#Paramters
SheepSearchDistance = 30
TimeBeforeDeerLuring = 5
TimeToStopDeerLuring = 50000
DistanceToShootDeer = 5
DistanceToLureDeer = 50
VillsToShootDeer = 4

#timers #todo: make timers alocate memory and pass into functions
t_sheep_claim = 1
t_deer_lure = 2
#Variables
deer_hp = -1
deer_id = -1
deer_lure_stage = -1
p_home = Point()
p_home_100 = Point()
sheep_point = Point()
deer_point = Point()
point_next_to_deer = Point()
search_state = State()

##------------SHEEP CLAIM-------------#
#if current_age() == Age.dark_age and unit_type_count(LineId.scout_cavalry_line) == 1:
#    up_full_reset_search()
#    up_find_local(LineId.scout_cavalry_line, 1) #add scout to local list
#    up_set_target_object(SearchSource.search_local, 0) #do this to get his position
#    up_get_point(PositionType.position_object, sheep_point) #save position in point
#    up_set_target_point(sheep_point)
#    up_filter_distance(-1, SheepSearchDistance) #don't look too far from the scout
#    SN.focus_player_number = 0 #to find gaia, need to focus player 0
#    up_find_remote(958, 1) #try to add one sheep to the remote list #todo: livestock_class is 958
#    up_get_search_state(search_state) #to set up the check
#
#    searchSource = SearchSource.search_remote
#    if search_state.RemoteIndex > 0: #found a sheep last rule
#        up_full_reset_search()
#        up_filter_distance(-1, SheepSearchDistance) #still uses last target point 
#        up_find_remote(958, 5) #livestock_class
#        up_clean_search(SearchSource.search_remote, ObjectData.object_data_distance, SearchOrder.search_order_asc) #use closest sheep
#        up_set_target_object(SearchSource.search_remote, 0) #get the position as above
#        up_get_point(PositionType.position_object, sheep_point)
#        up_bound_point(sheep_point, sheep_point) #be sure the point is on the map
#        up_find_local(LineId.scout_cavalry_line, 1) #add the scout to the local list
#        up_target_point(sheep_point, DUCAction.action_move, -1, AttackStance.stance_no_attack) #target the position of the sheep
#        chat_to_player(PlayerNumber.my_player_number, "Move") #todo: add my_plyaer_number
#        up_set_timer(t_sheep_claim, 4)
#        g_sheep_claim = 1
#
#    if g_sheep_claim == 1 and up_timer_status(t_sheep_claim) == TimerState.timer_triggered: #reset the scout once the timer runs out (means the above rule hasn't fired, which means there are no more sheep nearby)
#        chat_to_player(PlayerNumber.my_player_number, "Reset scout")
#        up_set_timer(t_sheep_claim, -1)
#        g_sheep_claim = 2
#        up_reset_scouts() #reset everything

#------------DEER LURE-------------#
if building_type_count(BuildingId.town_center) > 0:
    up_full_reset_search()
    up_find_local(BuildingId.town_center, 1)
    up_set_target_object(SearchSource.search_local, 0)
    up_get_point(PositionType.position_object, p_home)
    up_copy_point(p_home_100, p_home) #need to multiply by 100 for precise
    p_home_100.x = p_home_100.x * 100
    p_home_100.y = p_home_100.y * 100
    chat_to_all("set TC location")
    disable_self()

if True:
    SN.home_exploration_time = TimeToStopDeerLuring
    chat_to_all("set home_exploration_time")
    disable_self()

if deer_lure_stage == -1 and game_time() > SN.home_exploration_time:
    SN.total_number_explorers = 1
    SN.number_explore_groups = 1
    chat_to_all("Stop Deer Luring")
    up_reset_unit(LineId.scout_cavalry_line)
    deer_lure_stage = 100
    up_reset_scouts()
    disable_self()

if game_time() > TimeBeforeDeerLuring and game_time() < TimeToStopDeerLuring:
    #finding deer
    up_chat_data_to_all("deer_lure_stage:%d", deer_lure_stage)
    if deer_lure_stage != 100: #allow for exploration first
        #search for deer around the town center and pick the closest one
        up_full_reset_search()
        up_set_target_point(p_home)
        up_filter_distance(-1, DistanceToLureDeer)
        SN.focus_player_number = 0
        up_find_remote(909, 40) #find 40 deer Max
        up_clean_search(SearchSource.search_remote, ObjectData.object_data_distance, SearchOrder.search_order_asc)
        up_remove_objects(SearchSource.search_remote, ObjectData.object_data_index, compareOp.greater_than, 0) #only closest
        up_get_search_state(search_state) #check how many deer were found
        up_chat_data_to_all("deer found:%d", search_state.RemoteIndex)
        
        if deer_lure_stage == -1 and search_state.RemoteIndex >= 1 and up_set_target_object(SearchSource.search_remote, 0):
            up_get_object_data(ObjectData.object_data_id, deer_id) #get the id of the deer
            chat_to_all("start pushing the deer")
            deer_lure_stage = 0 #start pushing the deer

        if up_set_target_by_id(deer_id): #update chosen deer's position and hp every pass
            up_full_reset_search()
            up_get_object_data(ObjectData.object_data_hitpoints, deer_hp)
            up_get_object_data(ObjectData.object_data_precise_x, deer_point.x) #get the precise coordinates
            up_get_object_data(ObjectData.object_data_precise_y, deer_point.y)

        if deer_hp > 0 and up_set_target_by_id(deer_id): #if the deer is still alive
            chat_to_all("Push The Deer")
            up_copy_point(point_next_to_deer, deer_point) #copy deer position into a second point
            up_lerp_tiles(point_next_to_deer, p_home_100, -75) #move point one-quarter tile away from tc so the scout will be behind the deer
            up_full_reset_search()
            up_find_local(LineId.scout_cavalry_line, 1)
            SN.target_point_adjustment = 6 #set to enable precise targetting
            #up_bound_precise_point(point_next_to_deer, 1, 50) #Option unimplmented
            up_target_point(point_next_to_deer, DUCAction.action_move, Formation._1, AttackStance.stance_no_attack)
            SN.target_point_adjustment = 0 #reset

    #shooting Deer
    up_full_reset_search()
    up_set_target_point(p_home)
    up_filter_distance(-1, DistanceToShootDeer)
    SN.focus_player_number = 0
    up_find_remote(909, 5) #find up to 5 deer
    up_remove_objects(SearchSource.search_remote, ObjectData.object_data_carry, compareOp.less_than, 120) #only live deer
    up_get_search_state(search_state) #see how many were found

    #shoot the deer if not hunting boar and one is near the tc
    if ( search_state.RemoteIndex >= 1 #deer found near tc
        and up_timer_status(t_deer_lure) != TimerState.timer_running #this is so the command doesnt loop continuously
        and (dropsite_min_distance(Resource.live_boar) == -1 or dropsite_min_distance(Resource.live_boar) >= 10) #no boar nearby
    ):
        chat_to_all("Kill Deer")
        up_full_reset_search()
        up_set_target_point(p_home)
        up_find_local(ClassId.villager_class, 20)
        up_clean_search(SearchSource.search_local, ObjectData.object_data_distance, SearchOrder.search_order_asc)
        up_remove_objects(SearchSource.search_local, ObjectData.object_data_action, compareOp.equal, ActionId.actionid_build)
        up_remove_objects(SearchSource.search_local, ObjectData.object_data_dropsite, compareOp.equal, BuildingId.lumber_camp)
        up_remove_objects(SearchSource.search_local, ObjectData.object_data_index, compareOp.greater_than, VillsToShootDeer)
        up_find_remote(909, 10) #deer
        up_clean_search(SearchSource.search_remote, ObjectData.object_data_distance, SearchOrder.search_order_asc)  
        up_remove_objects(SearchSource.search_remote, ObjectData.object_data_index, compareOp.greater_than, 0) #only closest
        up_target_objects(0, DUCAction.action_default, Formation._1, AttackStance._1)
        up_set_timer(t_deer_lure, 15) #wait awhile before allowing this rule to fire again

        #reset the system once deer is shot
        if deer_hp < 2 and deer_lure_stage >= 0 and deer_lure_stage != 100:
            up_reset_unit(LineId.scout_cavalry_line)
            chat_to_all("Deer Shot--Reset")
            deer_lure_stage = -1
            deer_id = -1
            up_reset_scouts()

#==END======SHEEP CLAIM AND DEER LURE=======#