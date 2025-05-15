from scraper import *
from scraper import (
  #OBJECT TYPES
  Point, Constant, State, Integer, Array, _,
  #ENUMS
  ObjectId, ObjectData, ObjectStatus, ObjectList,
  ClassId, UnitId, BuildingId, Resource, Terrain,
  SearchSource, PositionType, PlacementType, Age,
  TechId, DUCAction, AttackStance, SN,
  #FUNCTIONS
  up_get_object_data, up_get_object_target_data, up_get_point,
  up_get_search_state, up_set_target_object, up_set_target_point,
  up_find_local, up_find_resource, up_filter_status, up_full_reset_search,
  up_get_point_terrain, timer_triggered, enable_timer, disable_timer,
  up_chat_data_to_all, up_point_distance, resource_found, disable_self,
  up_build, current_age, up_can_train, up_train, up_can_research, up_research,
  build, housing_headroom, population_headroom, building_type_count,
  up_lerp_tiles, up_set_target_by_id, up_target_point, building_type_count_total,
  chat_to_all, up_send_flare, up_filter_range,
)
'''
building killing idea:
    militia vs dark age doc, 1800/4 = 450 hits 
    - 2 take out in 4.75 min

    Longsword vs fudeal dock, 1800/14 = 129 hits
    14 = 4base, 5upgrades, 3bonusdamage, 1forging, 2arson, -1doc armor
    - 2 take out in 1 min

    Longsword vs fudeal military building, 1500hp 1armor
    - 7 take out in 15 seconds

    longsword vs fudeal tower, 850hp 1 armor
    - 7 take out in 8.5 seconds

    longsword vs palisade wall, 250hp 2 armor
    - 3 take out in 3.5 seconds

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
FALSE = Constant(0)
TRUE = Constant(1)
EMPLOYED = Constant(1)
UNEMPLOYED = Constant(0)

i = Integer(0)
j = Integer(0)
#===========================#
#|   JOB MANAGER CLASS     |#
#===========================#
#job arrays for each type of job used
#all functions dealing with jobs will be in this class
#only functions in this class should access these veriables
#have an asign job function, a remove job function, and a do job function
#__________explore_object__________#

J_explore_object_ids = Array(Integer, 10) #J_EXPLORE_OBJECT_ARRAY_SIZE
J_explore_object_things = Array(Integer, 10) #J_EXPLORE_OBJECT_ARRAY_SIZE
J_explore_object_tiles_away = Array(Integer, 10) #J_EXPLORE_OBJECT_ARRAY_SIZE
J_explore_object_direction = Array(Integer, 10) #J_EXPLORE_OBJECT_ARRAY_SIZE #ClOCKWIZE or COUNTER_CLOCKWIZE
J_explore_object_timers = Array(Integer, 10) #J_EXPLORE_OBJECT_ARRAY_SIZE
J_explore_object_timers[0] = 1
J_explore_object_timers[1] = 2
J_explore_object_timers[2] = 3
villager_id = Integer()
is_employed = Integer(8)
villager_point = Point(0,0)
closest_gold_point = Point(0,0)
'''
def J_get_employment_status(id:Integer) -> Integer:
    #chat_to_all("in J_get_employment_status")
    global J_explore_object_ids, J_explore_object_things, J_explore_object_tiles_away, J_explore_object_direction, J_explore_object_timers, EMPLOYED, UNEMPLOYED
    array_explorer_id = Integer()
    for i in range(10): #J_EXPLORE_OBJECT_ARRAY_SIZE
        array_explorer_id = J_explore_object_ids[i]
        if array_explorer_id == id:
            return EMPLOYED
    return UNEMPLOYED

def J_explore_object():
    chat_to_all("in J_explore_object")
    global J_explore_object_ids, J_explore_object_things, J_explore_object_tiles_away, J_explore_object_direction, J_explore_object_timers, EMPLOYED, UNEMPLOYED
    explorer_point = Point(0,0)
    resource_point = Point(0,0)
    dest_point = Point(0,0)
    normalized_point = Point(0,0)

    for i in range(10): #J_EXPLORE_OBJECT_ARRAY_SIZE
        explorer_id = i
        explorer_id = J_explore_object_ids[i]
        thing = J_explore_object_things[i]
        tiles_away = J_explore_object_tiles_away[i]
        explore_direction = J_explore_object_direction[i]
        explorer_timer = J_explore_object_timers[i]
        
        #the math #todo: fix this to use specific points, i think how it is, it wont work only using tile integeres
        up_full_reset_search()
        up_set_target_by_id(explorer_id)
        explorer_point.x, explorer_point.y = up_get_object_Point()
        #resource_point.x, resource_point.y = get_closest_resource_point(thing, dest_point)
        
        dest_point.x = resource_point.x
        dest_point.y = resource_point.y
        up_lerp_tiles(dest_point, explorer_point, tiles_away)

        #Rotate point 90 degrees to get perpendicular line 1 tile away
        #normalized_point.x = -(dest_point.y - resource_point.y)/tiles_away
        normalized_point.x = dest_point.y 
        normalized_point.x -= resource_point.y 
        normalized_point.x *= -1
        normalized_point.x /= tiles_away
        #normalized_point.y = (dest_point.x - resource_point.x)/tiles_away
        normalized_point.y = dest_point.x
        normalized_point.y -= resource_point.x
        normalized_point.y /= tiles_away
        
        up_full_reset_search()
        up_set_target_by_id(explorer_id)
        up_target_point(normalized_point, DUCAction.action_move, _, _)

        if timer_triggered(explorer_timer):
            J_FIRE_explore_object(explorer_id)

def J_HIRE_explore_object(explorer_id:Integer, thing:ObjectId, tiles_away:Integer, explore_duration:Integer = 50, explore_direction:Integer = CLOCKWIZE) -> Integer:
    chat_to_all("in J_HIRE_explore_object")
    global J_explore_object_ids, J_explore_object_things, J_explore_object_tiles_away, J_explore_object_direction, J_explore_object_timers, EMPLOYED, UNEMPLOYED
    for i in range(10): #J_EXPLORE_OBJECT_ARRAY_SIZE
        array_explorer_id = J_explore_object_ids[i]
        if array_explorer_id == -1:
            up_chat_data_to_all("%d is HIRED to explore object", explorer_id)
            J_explore_object_ids[i] = explorer_id
            J_explore_object_things[i] = thing
            J_explore_object_tiles_away[i] = tiles_away
            J_explore_object_direction[i] = explore_direction
            enable_timer(J_explore_object_timers[i], explore_duration)
            return EMPLOYED
        up_chat_data_to_all("%d did not have explorer job open", explorer_id)
        return UNEMPLOYED

def J_FIRE_explore_object(explorer_id:Integer) -> Integer:
    chat_to_all("in J_FIRE_explore_object")
    global J_explore_object_ids, J_explore_object_things, J_explore_object_tiles_away, J_explore_object_direction, J_explore_object_timers, EMPLOYED, UNEMPLOYED
    for i in range(10): #J_EXPLORE_OBJECT_ARRAY_SIZE
        array_explorer_id = J_explore_object_ids[i]
        if array_explorer_id == explorer_id:
            up_chat_data_to_all("%d is FIRED from explore object", explorer_id)
            J_explore_object_ids[i] = -1
            J_explore_object_things[i] = -1
            J_explore_object_tiles_away[i] = -1
            J_explore_object_direction[i] = -1
            disable_timer(J_explore_object_timers[i])
            return UNEMPLOYED
        up_chat_data_to_all("%d did not have the explorer job", explorer_id)
        return UNEMPLOYED

def get_closest_unit_id(unit_type:UnitId, point:Point, count:Integer = 0) -> Integer:
  chat_to_all("in get_closest_unit_id")
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

def get_closest_resource_point(resource:Resource, point:Point) -> (Integer, Integer):
  #chat_to_all("in get_closest_resource_point")


  temp_point = Point(8,8)
  temp_state = State(8,8,8,8)
  up_full_reset_search()
  up_filter_range(-1,-1,0,100)
  up_set_target_point(point)
  up_filter_status(ObjectStatus.status_resource, ObjectList.list_active)
  up_find_resource(resource, 5)
  up_chat_data_to_all("resource num: %d", resource)
  up_get_search_state(temp_state)
  up_chat_data_to_all("gold Count: %d", temp_state.RemoteIndex)

  up_clean_search(SearchSource.search_remote, ObjectData.object_data_distance, SearchOrder.search_order_asc)

  
  up_set_target_object(SearchSource.search_remote, 0)
  up_get_point(PositionType.position_object, temp_point)
  up_chat_data_to_all("gold.x: %d", temp_point.x)
  up_chat_data_to_all("gold.y: %d", temp_point.y)
  return temp_point.x, temp_point.y

def get_best_nomad_tc_location() -> Point:
   chat_to_all("in get_best_nomad_tc_location")
   point = Point(0,0)
   return point #return (0,0) #todo: make this work

def up_get_object_Point() -> (Integer, Integer):
    chat_to_all("in up_get_object_Point")
    temp_point = Point()
    up_get_object_data(ObjectData.object_data_point_x, temp_point.x)
    up_get_object_data(ObjectData.object_data_point_y, temp_point.y)
    return temp_point.x, temp_point.y

def try_train(unit:UnitId):
    if up_can_train(unit):
        up_train(unit)

def try_research(tech_id:TechId):
    if up_can_research(tech_id):
        up_research(tech_id)
'''
#SETTERS
if True:
    map_center_point = Point(0,0)
    up_get_point(PositionType.position_center, map_center_point)

    SN.percent_civilian_gatherers = 0
    SN.wood_gatherer_percentage = 0
    SN.food_gatherer_percentage = 0
    SN.stone_gatherer_percentage = 0
    SN.gold_gatherer_percentage = 0
    SN.cap_civilian_gatherers = 0
    SN.maximum_food_drop_distance=10
    SN.maximum_gold_drop_distance=10
    SN.maximum_hunt_drop_distance=20
    SN.maximum_stone_drop_distance=10
    SN.maximum_wood_drop_distance=10
    SN.percent_civilian_explorers=0
    SN.minimum_civilian_explorers=0
    SN.cap_civilian_explorers=0
    SN.total_number_explorers=0
    SN.number_explore_groups=0
    SN.percent_civilian_builders=0 #100 maybe
    SN.initial_exploration_required=0

    SN.cap_civilian_builders = 200
    SN.disable_builder_assistance = 0
    SN.consecutive_idle_unit_limit = 1
    SN.do_not_scale_for_difficulty_level = 1
    SN.enable_boar_hunting = 0
    SN.enable_offensive_priority = 1
    SN.enable_patrol_attack = 1
    SN.maximum_fish_boat_drop_distance = 30
    SN.scale_minimum_attack_group_size = 0
    SN.task_ungrouped_soldiers = 0
    SN.allow_civilian_defense = 0
    SN.allow_civilian_offense = 0
    SN.percent_attack_soldiers = 95
    SN.number_attack_groups = 0
    SN.maximum_town_size = 255
    SN.number_civilian_militia = 0
    SN.enable_new_building_system = 0 #I added this for stone mining
    SN.mill_max_distance = 50
    SN.camp_max_distance = 300
    SN.zero_priority_distance = 255
    chat_to_all("Setters Ran!")
    disable_self()


#===========================#
#|        Dark Age         |#
#===========================#

if current_age() == Age.dark_age:
    #=========find TC Location=========#
    if building_type_count_total(BuildingId.town_center) == 0:
        #region ___walk twords middle of map for 5 seconds___
        if True:
            up_full_reset_search()
            up_find_local(ClassId.villager_class, STARTING_VILL_COUNT)
            chat_to_all("walking to center")
            up_target_point(map_center_point, DUCAction.action_move, _, AttackStance.stance_no_attack)
            up_send_flare(map_center_point)
            disable_self()
        #endregion
        #region ___if find gold localy, walk around gold___
        if resource_found(Resource.gold):
            for i in range(STARTING_VILL_COUNT):
                up_full_reset_search()
                up_filter_range(-1,-1,-1,-1)
                up_find_local(ClassId.villager_class, STARTING_VILL_COUNT)

                up_set_target_object(SearchSource.search_local, i)
                up_get_object_data(ObjectData.object_data_id, villager_id)

                #---J_get_employment_status---#
                array_explorer_id = Integer()
                is_employed = UNEMPLOYED
                for j in range(10): #J_EXPLORE_OBJECT_ARRAY_SIZE
                    array_explorer_id = J_explore_object_ids[j]
                    if array_explorer_id == villager_id:
                        is_employed = EMPLOYED
                #----------------------------#

                #up_chat_data_to_all("interaer: %d",i)
                #up_chat_data_to_all("Villager: %d",villager_id)
                #up_chat_data_to_all("employed: %d",is_employed)
                if True: #is_employed == UNEMPLOYED:
                    
                    #villager_point.x, villager_point.y  = up_get_object_Point()
                    up_get_object_data(ObjectData.object_data_point_x, villager_point.x)
                    up_get_object_data(ObjectData.object_data_point_y, villager_point.y)
                    up_chat_data_to_all("V.x: %d", villager_point.x)
                    up_chat_data_to_all("V.y: %d", villager_point.y)


                    #---GET CLOSEST RESOURCE POINT---#
                    temp_state = State()
                    up_full_reset_search()
                    up_filter_range(-1,-1,0,100)
                    up_set_target_point(villager_point)
                    up_filter_status(ObjectStatus.status_resource, ObjectList.list_active)
                    up_find_resource(Resource.gold, 100)
                    #up_chat_data_to_all("resource num: %d", Resource.gold)
                    up_get_search_state(temp_state)
                    #up_chat_data_to_all("gold Count: %d", temp_state.RemoteIndex)

                    up_clean_search(SearchSource.search_remote, ObjectData.object_data_distance, SearchOrder.search_order_asc)
                    
                    up_set_target_object(SearchSource.search_remote, 0)
                    up_get_point(PositionType.position_object, closest_gold_point)
                    up_chat_data_to_all("gold.x: %d", closest_gold_point.x)
                    up_chat_data_to_all("gold.y: %d", closest_gold_point.y)
                     
                    #--------------------------------#

                    if up_point_distance(villager_point, closest_gold_point) <= VILLAGER_LOS:
                        up_chat_data_to_all("is close to gold!!!!: %d",villager_id)
                    #    up_chat_data_to_all("HIRE!: %d",villager_id)
        #                J_HIRE_explore_object(villager_id, Resource.gold, VILLAGER_LOS, 50, CLOCKWIZE)
        #endregion
        ##region ___after 5 seconds place a TC___
        #tc_location = Point(0,0)
        #tc_location = get_best_nomad_tc_location()
        #up_set_target_point(tc_location)
        #
        ##todo:how do I make all 3 of these build by differnt closest villiagers? 
        #up_build(PlacementType.place_point,_,BuildingId.town_center) 
        #up_build(BuildingId.house) 
        #up_build(BuildingId.barracks)
        ##endregion

    ##==========Exploring==========#
    ##region ___control livestock to explore and go to TC___
    #up_full_reset_search()
    #up_find_local(ClassId.livestock_class, 20)
    #up_clean_search()#remove non-idle units
    #up_target_point(tc_location, DUCAction.action_move, _, _)
    ##scout around TC with them at some point
    ##endregion
    ##region ___control Malitia to explore and bring in herdable and hunt___
    #if can_train(UnitId.militiaman):
    #    train(UnitId.militiaman)
    #    train(UnitId.militiaman)
    #    disable_self()
    #
    #magellan_malitia_id = Integer()
    #hunter_malitia_id = Integer()
    ##set the 2 malitia to specific ID varialbes
    #
    #J_collect_headables(magellan_malitia_id, 8)
    #   
    #J_explore_terrain(magellan_malitia_id, Terrain.terrain_water, DA_MILITIA_LOS)
    #if deer_within_20:#deer within 40 tiles of TC
    #    deer_id = get_closest_unit_id(ClassId.prey_animal_class, tc_location)
    #    J_push_deer(hunter_malitia_id, deer_id)
    #elif Bore_within_40:
    #   boar_id = get_closest_unit_id(ClassId.predator_animal_class, tc_location)
    #   J_lure_bore(hunter_malitia_id, boar_id)
    #elif deer_within_40:
    #    deer_id = get_closest_unit_id(ClassId.prey_animal_class, tc_location)
    #    J_push_deer(hunter_malitia_id, deer_id)
    ##endregion

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
    #try_research(TechId.feudal_age)
    #endregion

    ##==========Defensive==========#
    ##region ___decide where to build house for walling___
    ##endregion
    ##region ___bring malitia back if there is shinanigans___
    ##endregion
    #pass
