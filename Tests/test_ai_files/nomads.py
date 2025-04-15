#THINGS TO DO in compiler
#todo: make arrays
#todo: make objects asign to each other nicely, including touple asignments
#todo: implement default values for functions


#THINGS TO CODE in this AI
#todo: make a system of units having jobs and prios exec.
    #job name aka enum
    #job prioirity
    #way to lookup if a unit is busy
    #job return values for if the job is full or things like that

from scraper import *
from scraper import (
  #OBJECT TYPES
  Point, Constant, State, Integer, _,
  #ENUMS
  ObjectId, ObjectData, ObjectStatus, ObjectList,
  ClassId, UnitId, BuildingId, Resource, Terrain,
  SearchSource, PositionType, PlacementType, Age,
  TechId,
  #FUNCTIONS
  up_get_object_data, up_get_object_target_data, up_get_point,
  up_get_search_state, up_set_target_object, up_set_target_point,
  up_find_local, up_find_resource, up_filter_status, up_full_reset_search,
  up_get_point_terrain, timer_triggered, enable_timer, disable_timer,
  up_chat_data_to_all, up_point_distance, resource_found, disable_self,
  up_build, current_age, up_can_train, up_train, up_can_research, up_research,
  build, housing_headroom, population_headroom, building_type_count
)
'''
#______-Dark Age_________-#

__find TC Location__
1. walk twords middle of map for 5 seconds
2. if find gold localy, walk around gold
3. After 5 seconds place TC next to wood line when found
   (Gold+Hunt -> Gold -> Berry -> hunt -> stone)
4. build barracks with one of the villagers build house with other villager
5. send all villegers to TC to build and then collect food

__Exploring__
1. send all heardables to TC
2. explore with heardables
3. Explore with 5 malitia around ocean, try to kill vil or doc 
4. pick up heardables and 

__Eco__
1. push deer with malitia
2. lure far away bores with malitia
3. build mule cart if i did not find gold to get gold, and to age up

#______Feudal Age______--#

__kill buildings__
1. train malitia on the way up
2. get men at arms + longsword + arsen as fast as possible
3. attack plan to kill dock, one guy to keep curcling
4. attack plan to kill other buildings. specificaly target archery ranges

__Eco__
1. mule cart to get farther away hunt (mule cart to block bores)(build houses with these viligers)(now that military is attacking)
2. mill far away berries if no hunt availible, or get gold/stone if i dont need more food
3. mule cart for more efective wood gathering
4. mule cart upgrades as fast as possible/both if i have 2 out at the same time
5. if no docks, build fishingships, if not build mill and farms last case canario

__defence__
1. build second baracks, pikemen if i see lots of scouts
2. pikeman guard logic
3. wall in base logic
4. tower against archer logic

__Finish it__
1. if no bilding around and 20+ longswords dive
2. blacksmith and upgrades if i have extra resources
3. go to castle age if extra resources and 15+ longswords

#______--Castle Age______-#

__upgrades people, Upgrades!__
1. eco
2. military

__monestary__
1. get worrior priest and relics (healing silliness)
2. research faith if get converted
3. monestary drop silliness

__castle__
1. composit bowmen?
2. find good place to defence with it

__Eco__
1. docks and fish traps
2. balancing larger ecomony
3.
'''
VILLAGER_LOS = Constant(4)
DA_MILITIA_LOS = Constant(6)
STARTING_VILL_COUNT = Constant(3)
CLOCKWIZE = Constant(0)
COUNTER_CLOCKWIZE = Constant(1)

def JOB_explore_terrain(explorer_id, terrain:Terrain, tiles_away, explore_duration = 50, explore_direction = CLOCKWIZE) -> (Integer, Integer):
  INTERNAL_PRIORITY = Constant(1)
  EXPLORE_JOB_PRIORITY = Constant(1)
  terrain_type_at_point = Integer()
  terrain_id_at_point = Integer()
  up_get_point_terrain(starting_point, terrain_type_at_point, terrain_id_at_point)

def JOB_explore_object(explorer_id, thing:ObjectId, tiles_away, explore_duration = 50, explore_direction = CLOCKWIZE) -> (Integer, Integer):
  #pass in exploorer_id as -1 to make it just run the exploration.
  #pass in actual id to set a new explorer of an object.
  #eplorer will cirle around a group of touching objects staying tiles_away in its circle.
  explorer1_id = Integer()
  explorer1_timer = Constant(1)
  explorer1_thing = Integer()
  explorer1_tiles_away = Integer()
  explorer2_id = Integer()
  explorer2_timer = Constant(2)
  explorer2_thing = Integer()
  explorer2_tiles_away = Integer()
  explorer3_id = Integer()
  explorer3_timer = Constant(3)
  explorer3_thing = Integer()
  explorer3_tiles_away = Integer()

  #the math
  #get the perpendicular line to the closest resource and tiles_away from the resoruce in the direction of the villager. 
  #move 1 tiles away farther down that tangent line (or farther if you check that is full)
  #recalculate each time its called

  #find the gold point and villager point, 
  if explorer_id == -1: #run explore code
    if explorer1_id != -1:
      pass#do the math to explore
      if timer_triggered(explorer1_timer):
        explorer1_id = -1
        explorer1_thing = -1
        explorer1_tiles_away = -1
        disable_timer(explorer1_timer)
    if explorer2_id != -1:
      pass#do the math to explore
      if timer_triggered(explorer2_timer):
        explorer2_id = -1
        explorer2_thing = -1
        explorer2_tiles_away = -1
        disable_timer(explorer2_timer)
    if explorer3_id != -1:
      pass#do the math to explore
      if timer_triggered(explorer3_timer):
        explorer3_id = -1
        explorer3_thing = -1
        explorer3_tiles_away = -1
        disable_timer(explorer3_timer)

  else: 
    if explorer_id != explorer1_id and explorer_id != explorer2_id and explorer_id != explorer3_id:
      up_chat_data_to_all("%d is already an explorer", explorer_id)
      return
    
    if explorer1_id == -1:
      explorer1_id = explorer_id
      explorer1_thing = thing
      explorer1_tiles_away = tiles_away
      enable_timer(explorer1_timer, explore_duration)
    elif explorer2_id == -1:
      explorer2_id = explorer_id
      explorer2_thing = thing
      explorer2_tiles_away = tiles_away
      enable_timer(explorer2_timer, explore_duration)
    elif explorer3_id == -1:
      explorer3_id = explorer_id
      explorer3_thing = thing
      explorer3_tiles_away = tiles_away
      enable_timer(explorer3_timer, explore_duration)
    else:
      up_chat_data_to_all("%d cannot be set, already max exploring items", explorer_id)
      return

def JOB_push_deer(hunter_id, deer_id) -> Integer:
    return #return 0 if job full

def JOB_lure_bore(hunter_id, bore_id) -> Integer:
    return #return 0 if job full

def JOB_collect_headables(hearder_id, distance = 10) -> Integer:
    #find heardables within distance of hearder_id
    #move to the closest one
    #if there is none:
        return UNEMPLOYED
    #if there is one:
        return EMPLOYED_AS_HEARDABLE_COLLECTOR

def get_closest_unit_id(unit_type:UnitId, point:Point, count = 0) -> Integer:
  #will return unit id of closest unit, but will still set the active list with count you want
  temp_int = Integer()
  temp_state = State()
  up_full_reset_search()
  up_filter_status(ObjectStatus.status_ready, ObjectList.list_active)
  up_find_local(unit_type,1)
  up_get_search_state(temp_state)
  up_set_target_object(SearchSource.search_local, count)
  up_get_object_data(ObjectData.object_data_id, temp_int)
  return temp_int

def get_closest_resource_point(resource:Resource, point:Point) -> Point:
  temp_point = Point()
  temp_state = State()
  up_full_reset_search()
  up_set_target_point(point)
  up_filter_status(ObjectStatus.status_resource, ObjectList.list_active)
  up_find_resource(resource, 1)
  up_get_search_state(temp_state)
  up_set_target_object(SearchSource.search_remote, 0)
  up_get_point(PositionType.position_object, temp_point)
  return temp_point

def get_best_nomad_tc_location() -> Point:
  return

def up_get_object_point(point:Point) -> Point:
  up_get_object_data(ObjectData.object_data_point_x, point.x)
  up_get_object_data(ObjectData.object_data_point_y, point.y)
  return point

def try_train(unit:UnitId):
    if up_can_train(unit):
        up_train(unit)

def try_research(tech_id:TechId):
    if up_can_research(tech_id):
        up_research(tech_id)


#===========================#
#|        Dark Age         |#
#===========================#
if current_age() == Age.dark_age:
    #=========find TC Location=========#
    if building_type_count_total(BuildingId.town_center) == 0:
        #region ___walk twords middle of map for 5 seconds___
        if True:
            up_full_reset_search()
            up_find_local(ClassId.villager_class, 3)
            #walk twords middle of map
            disable_self()
        #endregion
        #region ___if find gold localy, walk around gold___
        if resource_found(Resource.gold):
            up_full_reset_search()
            up_find_local(ClassId.villager_class, 3)
            for i in range(STARTING_VILL_COUNT):
                up_set_target_object(SearchSource.search_local, i)
                villager_point = Point()
                villager_point = up_get_object_point(villager_point)
                closest_gold_point = get_closest_resource_point(Resource.gold, villager_point)
                if up_point_distance(villager_point, closest_gold_point) <= VILLAGER_LOS:
                    villager_id = -1
                    up_get_object_target_data(ObjectData.object_data_id, villager_id)
                    JOB_explore_object(villager_id, Resource.gold, VILLAGER_LOS, closest_gold_point)
        #endregion
        #region ___after 5 seconds place a TC___
        tc_location = Point()
        tc_location = get_best_nomad_tc_location()
        up_set_target_point(tc_location)

        #todo:how do I make all 3 of these build by differnt closest villiagers? 
        up_build(PlacementType.place_point,_,BuildingId.town_center) 
        up_build(BuildingId.house) 
        up_build(BuildingId.barracks)
        #endregion

    #==========Exploring==========#
    #region ___control livestock to explore and go to TC___
    up_full_reset_search()
    up_find_local(ClassId.livestock_class, 20)
    up_clean_search()#remove non-idle units
    up_target_point(tc_location, DUCAction.action_move, _, _)
    #scout around TC with them at some point
    #endregion
    #region ___control Malitia to explore and bring in herdable and hunt___
    if can_train(UnitId.militiaman):
        train(UnitId.militiaman)
        train(UnitId.militiaman)
        disable_self()
   
    magellan_malitia_id = Integer()
    hunter_malitia_id = Integer()
    #set the 2 malitia to specific ID varialbes
    
    JOB_collect_headables(magellan_malitia_id, 8)
       
    JOB_explore_terrain(magellan_malitia_id, Terrain.terrain_water, DA_MILITIA_LOS)
    if deer_within_20:#deer within 40 tiles of TC
        deer_id = get_closest_unit_id(ClassId.prey_animal_class, tc_location)
        JOB_push_deer(hunter_malitia_id, deer_id)
    elif Bore_within_40:
       boar_id = get_closest_unit_id(ClassId.predator_animal_class, tc_location)
       JOB_lure_bore(hunter_malitia_id, boar_id)
    elif deer_within_40:
        deer_id = get_closest_unit_id(ClassId.prey_animal_class, tc_location)
        JOB_push_deer(hunter_malitia_id, deer_id)
    #endregion

    #==========Economy==========#
    #region ___control Mule Card and build___
    #build a mule card and place it next to gold
    #endregion
    #region ___balance villagers on resources___
    #if <50 food, force drop off
    #if <65 wood, move people there?
    #switch between food and wood based on something?
    #endregion
    #region ___decide when to feudal___
    try_research(TechId.feudal_age)
    #endregion

    #==========Defensive==========#
    #region ___decide where to build house for walling___
    #endregion
    #region ___bring malitia back if there is shinanigans___
    #endregion
    pass

#=============================#
#|        Feudal Age         |#
#=============================#
if current_age() == Age.feudal_age:

    #__kill buildings__
    #1. train malitia on the way up
    try_research(TechId.ri_man_at_arms)
    try_research(TechId.ri_long_swordsman)
    try_research(TechId.ri_arson)
    #3. attack plan to kill dock, one guy to keep curcling
    #4. attack plan to kill other buildings. specificaly target archery ranges
    #
    #__Eco__
    try_research(TechId.ri_double_bit_axe)
    try_research(TechId.ri_gold_mining)
    #1. mule cart to get farther away hunt (mule cart to block bores)(build houses with these viligers)(now that military is attacking)
    #2. mill far away berries if no hunt availible, or get gold/stone if i dont need more food
    #3. mule cart for more efective wood gathering
    #4. mule cart upgrades as fast as possible/both if i have 2 out at the same time
    #5. if no docks, build fishingships, if not build mill and farms last case canario
    #
    #__defence__
    try_research(TechId.ri_pikeman)
    #1. build second baracks, pikemen if i see lots of scouts
    #2. pikeman guard logic
    #3. wall in base logic
    #4. tower against archer logic
    #
    #__Finish it__
    try_research(TechId.ri_forging)
    try_research(TechId.ri_scale_mail)  
    #1. if no bilding around and 20+ longswords dive
    #2. blacksmith and upgrades if i have extra resources
    #3. go to castle age if extra resources and 15+ longswords

#=============================#
#|        Castle Age         |#
#=============================#
if current_age() == Age.castle_age:
    #region __upgrades people, Upgrades!__
    try_research(TechId.ri_bow_saw)
    #endregion
    #1. eco
    #2. military
    #
    #__monestary__
    #1. get worrior priest and relics (healing silliness)
    #2. research faith if get converted
    #3. monestary drop silliness
    #
    #__castle__
    #1. composit bowmen?
    #2. find good place to defence with it
    #
    #__Eco__
    #1. docks and fish traps
    #2. balancing larger ecomony
    #3.

#=============================#
#|       Basic stuff         |#
#=============================#
if housing_headroom() < 3 and population_headroom() > 0 and building_type_count(BuildingId.town_center) > 0: #to not build house while searching for TC on nomad
    build(BuildingId.house)

try_train(UnitId.villager)

