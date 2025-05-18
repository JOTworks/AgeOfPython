#THINGS TO DO in compiler
#todo: make arrays work with items of lenght > 1
#todo: implement struct object types
#todo: make objects asign to each other nicely, including touple asignments

#not really needed
#todo: implement default values for functions
#todo: get boolians working (currrently using the coments)

#THINGS TO CODE in this AI
#todo: make a system of units having jobs and prios exec.
    #job name aka enum
    #job prioirity
    #way to lookup if a unit is busy
    #job return values for if the job is full or things like that

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
  chat_to_all, up_send_flare, up_filter_range, up_add_object_by_id
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
BUILD_TC_TIME = Constant(30)

i = Integer(0)
##region Round Counters
#if True:
#    round_counter = 0
#    disable_self()
#every_2 = FALSE
#every_4 = FALSE
#every_8 = FALSE
#every_16 = FALSE
#every_32 = FALSE
#every_64 = FALSE
#every_128 = FALSE
#every_256 = FALSE
#reset_every = FALSE
#round_counter += 1 #round_counter goes from 1 - 256
#if round_counter % 2 == 0:
#    every_2 = TRUE
#if round_counter % 4 == 0:
#    every_4 = TRUE
#if round_counter % 8 == 0:
#    every_8 = TRUE
#if round_counter % 16 == 0:
#    every_16 = TRUE
#if round_counter % 32 == 0:
#    every_32 = TRUE
#if round_counter % 64 == 0:
#    every_64 = TRUE
#if round_counter % 128 == 0:
#    every_128 = TRUE
#if round_counter % 256 == 0:
#    every_256 = TRUE
#if round_counter >= 256:
#    round_counter = 0
##endregion
#======================================================  CLASSES  ===========================================================#
#===========================#
#| RESROUCE MANAGER CLASS  |#
#===========================#
MINE_LIMIT = Constant(10)
R_gold_mine_count = Integer(0)
R_gold_total_count = Integer()
R_gold_location = Array(Point, 10)
R_gold_ammount = Array(Integer, 10)
R_stone_mine_count = Integer(0)
R_stone_total_count = Integer()
R_stone_location = Array(Point, 10)
R_stone_ammount = Array(Integer, 10)

def R_add_new_mine(resource:Resource, location:Point) -> Integer:
    global TRUE, FALSE, MINE_LIMIT
    global R_gold_mine_count, R_gold_total_count, R_gold_location, R_gold_ammount
    global R_stone_mine_count, R_stone_total_count, R_stone_location, R_stone_ammount
    if resource == Resource.gold:
        if R_gold_mine_count >= MINE_LIMIT:
            #up_chat_data_to_all("ER:R_add_new_mine:mineLimit%d",MINE_LIMIT)
            return FALSE
        #!See if either one works
        R_gold_location[R_gold_mine_count] = location
        R_gold_mine_count += 1
        up_chat_data_to_all("added Gold mine #%d",R_gold_mine_count)
        return TRUE

    if resource == Resource.stone:
        if R_stone_mine_count >= MINE_LIMIT:
            #up_chat_data_to_all("ER:R_add_new_mine:mineLimit%d",MINE_LIMIT)
            return FALSE
        #!See if either one works
        R_stone_location[R_stone_mine_count] = location
        R_stone_mine_count += 1
        up_chat_data_to_all("added Stone mine #%d",R_stone_mine_count)
        return TRUE
        
    return FALSE

def R_update_mines(resource:Resource):
    global TRUE, FALSE, MINE_LIMIT
    global R_gold_mine_count, R_gold_total_count, R_gold_location, R_gold_ammount
    global R_stone_mine_count, R_stone_total_count, R_stone_location, R_stone_ammount

    if resource == Resource.wood or resource == Resource.food:
        up_chat_data_to_all("ER:R_update_mines:%d",resource)
    temp_state = State()
    up_full_reset_search()
    up_filter_range(-1,-1,-1,-1)
    up_filter_status(ObjectStatus.status_resource, ObjectList.list_active)
    up_find_resource(resource, 240)
    up_get_search_state(temp_state)
    
    #filter out groups that are close to each target point
    for i in range(temp_state.RemoteList):
        tile_id = Integer()
        tile_loc = Point()
        up_set_target_object(SearchSource.search_remote, i)
        up_get_object_data(ObjectData.object_data_id, tile_id)
        tile_loc = up_get_object_Point()

        temp_mine_loc = Point()
        part_of_existing_mine = FALSE
        for j in range(MINE_LIMIT):
            if resource == Resource.gold:
                temp_mine_loc = R_gold_location[j]
            if resource == Resource.stone:
                temp_mine_loc = R_stone_location[j]
           
            if up_point_distance(tile_loc, temp_mine_loc) < 4:
                part_of_existing_mine = TRUE

        if part_of_existing_mine == FALSE:
            R_add_new_mine(resource, tile_loc)

#===========================#
#|   JOB MANAGER CLASS     |#
#===========================#
#job arrays for each type of job used
#all functions dealing with jobs will be in this class
#only functions in this class should access these veriables
#have an asign job function, a remove job function, and a do job function
J_DEER_PUSH_ARRAY_LENGTH = Constant(3)
#__________explore_object__________#

J_EXPLORE_OBJECT_ARRAY_SIZE = Constant(10)
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

def J_get_employment_status(id:Integer) -> Integer:
    #chat_to_all("in J_get_employment_status")
    global J_explore_object_ids, J_deer_push_hunter, EMPLOYED, UNEMPLOYED
    array_explorer_id = Integer()
    array_hunter_id = Integer()
    for i in range(10):
        array_explorer_id = J_explore_object_ids[i]
        if array_explorer_id == id:
            return EMPLOYED
    for i in range(3):
        array_hunter_id = J_deer_push_hunter[i]
        if array_hunter_id == id:
            return EMPLOYED
    return UNEMPLOYED

def J_explore_object():
    global J_explore_object_ids, J_explore_object_things, J_explore_object_tiles_away, J_explore_object_direction, J_explore_object_timers, EMPLOYED, UNEMPLOYED
    explorer_point = Point()
    resource_point = Point()
    dest_point = Point()
    prime_point = Point()
    normalized_point = Point()
    for i in range(3): #J_EXPLORE_OBJECT_ARRAY_SIZE

        explorer_id = J_explore_object_ids[i]
        if explorer_id != -1:
            thing = J_explore_object_things[i]
            tiles_away = J_explore_object_tiles_away[i]
            explore_direction = J_explore_object_direction[i]
            explorer_timer = J_explore_object_timers[i]
            #the math #todo: fix this to use specific points, i think how it is, it wont work only using tile integeres
            up_full_reset_search()
            up_set_target_by_id(explorer_id)
            explorer_point.x, explorer_point.y = up_get_object_Point()
            resource_point.x, resource_point.y = get_closest_resource_point(thing, explorer_point)
            
            dest_point.x = resource_point.x
            dest_point.y = resource_point.y
            
            up_lerp_tiles(dest_point, explorer_point, tiles_away)
           

            #translate reletive
            #prime_point = resource_point - dest_point #todo:we want to be able to do this
            prime_point.x = resource_point.x
            prime_point.y = resource_point.y
            prime_point.x -= dest_point.x
            prime_point.y -= dest_point.y
            #rotate 90
            temp = Integer()
            temp = prime_point.x
            prime_point.x = prime_point.y
            prime_point.y = temp * -1
            #translate back
            dest_point.x += prime_point.x
            dest_point.y += prime_point.y

            up_full_reset_search()
            up_add_object_by_id(SearchSource.search_local, explorer_id)
            
            up_target_point(dest_point, DUCAction.action_move, _, _)

            if timer_triggered(explorer_timer):
                J_FIRE_explore_object(explorer_id)

def J_HIRE_explore_object(explorer_id:Integer, thing:ObjectId, tiles_away:Integer, explore_duration:Integer = 50, explore_direction:Integer = CLOCKWIZE) -> Integer:
    global J_explore_object_ids, J_explore_object_things, J_explore_object_tiles_away, J_explore_object_direction, J_explore_object_timers
    global EMPLOYED, UNEMPLOYED, J_EXPLORE_OBJECT_ARRAY_SIZE
    for i in range(J_EXPLORE_OBJECT_ARRAY_SIZE):
        array_explorer_id = J_explore_object_ids[i]
        if array_explorer_id == -1:
            up_chat_data_to_all("%d is HIRED to explore object", explorer_id)
            J_explore_object_ids[i] = explorer_id
            J_explore_object_things[i] = thing
            J_explore_object_tiles_away[i] = tiles_away
            J_explore_object_direction[i] = explore_direction
            enable_timer(J_explore_object_timers[i], explore_duration)
            t = J_explore_object_ids[0]
            up_chat_data_to_all("A0: %d",t)
            t = J_explore_object_ids[1]
            up_chat_data_to_all("A1: %d",t)
            t = J_explore_object_ids[2]
            up_chat_data_to_all("A2: %d",t)
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

def J_FIRE_ALL_explore_object():
    chat_to_all("in J_FIRE_explore_object")
    global J_explore_object_ids, J_explore_object_things, J_explore_object_tiles_away, J_explore_object_direction, J_explore_object_timers, EMPLOYED, UNEMPLOYED
    for i in range(10): #J_EXPLORE_OBJECT_ARRAY_SIZE
        array_explorer_id = J_explore_object_ids[i]
        up_chat_data_to_all("%d is FIRED from explore object", array_explorer_id)
        J_explore_object_ids[i] = -1
        J_explore_object_things[i] = -1
        J_explore_object_tiles_away[i] = -1
        J_explore_object_direction[i] = -1
        disable_timer(J_explore_object_timers[i])

##__________explore_terrain__________#
#def J_explore_terrain(explorer_id, terrain:Terrain, tiles_away, explore_duration = 50, explore_direction = CLOCKWIZE) -> (Integer, Integer):
#    terrain_type_at_point = Integer()
#    terrain_id_at_point = Integer()
#    up_get_point_terrain(terrain_type_at_point, terrain_id_at_point)
##__________push_deer__________#

J_deer_push_hunter = Array(Integer, 3)
J_deer_push_pray = Array(Integer, 3)

deer_id = Integer()
hunter_id = Integer()
deer_search_state = State()

SHOOT_DEER_DIST = 2
LURE_DEER_DIST = 50
VIL_SHOOT_DEER_COUNT = 4
p_home = Point()
p_home_100 = Point()

def J_push_deer():
    global p_home, p_home_100, J_DEER_PUSH_ARRAY_LENGTH, SHOOT_DEER_DIST, LURE_DEER_DIST, VIL_SHOOT_DEER_COUNT
    global J_deer_push_hunter, J_deer_push_pray, deer_search_state
    deer_hp = Integer()
    deer_id = Integer()
    deer_point = Point()
    point_next_to_deer = Point()

    #pushing Deer
    for i in range(J_DEER_PUSH_ARRAY_LENGTH):
        deer_id = J_deer_push_pray[i]
        hunter_id = J_deer_push_hunter[i]
        deer_id = J_deer_push_pray[i]
        if hunter_id != -1:
            if up_set_target_by_id(deer_id):
                up_full_reset_search()
                up_get_object_data(ObjectData.object_data_hitpoints, deer_hp)
                up_get_object_data(ObjectData.object_data_precise_x, deer_point.x)
                up_get_object_data(ObjectData.object_data_precise_y, deer_point.y)
            else:
                J_FIRE_push_deer(hunter_id)

            if deer_hp > 0: #if the deer is still alive
                point_next_to_deer = deer_point
                up_lerp_tiles(point_next_to_deer, p_home_100, -75) #move point one-quarter tile away from tc so the scout will be behind the deer

                flare_point = Point()
                flare_point.x = point_next_to_deer.x / 100
                flare_point.y = point_next_to_deer.y / 100
                up_send_flare(flare_point)
                up_full_reset_search()
                up_add_object_by_id(SearchSource.search_local, hunter_id)
                SN.target_point_adjustment = 6 #set to enable precise targetting
                up_target_point(point_next_to_deer, DUCAction.action_move, _, AttackStance.stance_no_attack)
                SN.target_point_adjustment = 0 #reset
            else:
                J_FIRE_push_deer(hunter_id)

    #shooting Deer
    up_full_reset_search()
    up_set_target_point(p_home)
    up_filter_distance(-1, SHOOT_DEER_DIST)
    SN.focus_player_number = 0
    up_find_remote(ClassId.prey_animal_class, 5)
    up_remove_objects(SearchSource.search_remote, ObjectData.object_data_carry, compareOp.less_than, 120) #remove dead live deer
    up_clean_search(SearchSource.search_remote, ObjectData.object_data_distance, SearchOrder.search_order_asc)
    up_remove_objects(SearchSource.search_remote, ObjectData.object_data_index, compareOp.greater_than, 0) #only closest
    up_get_search_state(deer_search_state)
    if deer_search_state.RemoteIndex >= 1: #deer found
        chat_to_all("Kill Deer")
        up_set_target_point(p_home)
        up_find_local(ClassId.villager_class, 20)
        up_clean_search(SearchSource.search_local, ObjectData.object_data_distance, SearchOrder.search_order_asc)
        up_remove_objects(SearchSource.search_local, ObjectData.object_data_action) == ActionId.actionid_build
        up_remove_objects(SearchSource.search_local, ObjectData.object_data_dropsite) == BuildingId.lumber_camp
        up_remove_objects(SearchSource.search_local, ObjectData.object_data_index) > VIL_SHOOT_DEER_COUNT
        up_target_objects(0,_,_,_)

def J_HIRE_push_deer(hunter_id:Integer, deer_id:Integer) -> Integer:
    global p_home, p_home_100, J_DEER_PUSH_ARRAY_LENGTH, SHOOT_DEER_DIST, LURE_DEER_DIST, VIL_SHOOT_DEER_COUNT
    global J_deer_push_hunter, J_deer_push_pray, deer_search_state, UNEMPLOYED, EMPLOYED
    for i in range(J_DEER_PUSH_ARRAY_LENGTH):
        array_hunter_id = J_deer_push_hunter[i]
        if array_hunter_id == -1:
            up_chat_data_to_all("%d is HIRED to Push Deer", hunter_id)
            up_chat_data_to_all("deer id:%d", deer_id)
            J_deer_push_hunter[i] = hunter_id
            J_deer_push_pray[i] = deer_id
            return EMPLOYED
    up_chat_data_to_all("%d did not have Push Deer open", hunter_id)
    return UNEMPLOYED

def J_FIRE_push_deer(hunter_id:Integer) -> Integer:
    chat_to_all("in J_FIRE_push_deer")
    global p_home, p_home_100, J_DEER_PUSH_ARRAY_LENGTH, SHOOT_DEER_DIST, LURE_DEER_DIST, VIL_SHOOT_DEER_COUNT
    global J_deer_push_hunter, J_deer_push_pray, deer_search_state, UNEMPLOYED, EMPLOYED
    for i in range(J_DEER_PUSH_ARRAY_LENGTH): #J_EXPLORE_OBJECT_ARRAY_SIZE
        array_hunter_id = J_deer_push_hunter[i]
        if array_hunter_id == hunter_id:
            up_chat_data_to_all("%d is FIRED from explore object", hunter_id)
            J_deer_push_hunter[i] = -1
            J_deer_push_pray[i] = -1
            return UNEMPLOYED
    up_chat_data_to_all("%d did not have the explorer job", hunter_id)
    return UNEMPLOYED

##__________lure_boar__________#
#def J_lure_boar(hunter_id, bore_id) -> Integer:
#    return #return 0 if J full
##__________collect_heardables__________#
##def J_collect_headables(hearder_id, distance = 10) -> Integer:
#    #find heardables within distance of hearder_id
#    #move to the closest one
#    #if there is none:
#        return UNEMPLOYED
#    #if there is one:
#        return EMPLOYED_AS_HEARDABLE_COLLECTOR



#======================================================  Functions  ===========================================================#
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

  temp_point = Point()
  temp_int = Integer()
  temp_state = State()
  up_full_reset_search()
  up_set_target_point(point)

  if resource == Resource.wood:
    up_filter_range(-1,-1,0,10)
    up_filter_status(ObjectStatus.status_ready, ObjectList.list_active)
    up_find_resource(resource, 240)
  else:
    up_filter_range(-1,-1,0,100)
    up_filter_status(ObjectStatus.status_resource, ObjectList.list_active)
    up_find_resource(resource, 240)
  
  up_get_search_state(temp_state)
  up_clean_search(SearchSource.search_remote, ObjectData.object_data_distance, SearchOrder.search_order_asc)
  
  if temp_state.RemoteList > 0:
    up_set_target_object(SearchSource.search_remote, 0)
    up_get_point(PositionType.position_object, temp_point)
    return temp_point.x, temp_point.y
    
  temp_int = -1
  return temp_int, temp_int

def get_best_nomad_tc_location() -> Point:
    # After X seconds place TC next to wood line when found
    # (Gold+Hunt -> Gold -> Berry -> hunt -> stone)
    chat_to_all("in get_best_nomad_tc_location")
    global J_explore_object_ids
    global R_stone_location, R_gold_location, R_gold_mine_count
    global map_center_point

    if R_gold_mine_count > 0:
        for i in range(R_gold_mine_count):
            gold_loc = Point()
            wood_loc = Point()
            gold_loc = R_gold_location[i]
            wood_loc = get_closest_resource_point(Resource.wood, gold_loc)
            if wood_loc.x != -1:
                chat_to_all("found wood&gold TC location")
                return gold_loc #wood_loc

    return map_center_point

def up_get_object_Point() -> (Integer, Integer):
    #chat_to_all("in up_get_object_Point")
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

def try_build(building:BuildingId):
    if up_can_build(_, building) and up_pending_objects(building) < 1:
        up_build(_,_,building)
#===================================SETTERS======================================
if True:
    map_center_point = Point(0,0)
    up_get_point(PositionType.position_center, map_center_point)
    SN.placement_zone_size=20
    SN.percent_civilian_gatherers=0
    SN.wood_gatherer_percentage=0
    SN.food_gatherer_percentage=0
    SN.stone_gatherer_percentage=0
    SN.gold_gatherer_percentage=0
    SN.cap_civilian_gatherers=0
    SN.maximum_food_drop_distance=10
    SN.maximum_gold_drop_distance=10
    SN.maximum_hunt_drop_distance=20
    SN.maximum_stone_drop_distance=10
    SN.maximum_wood_drop_distance=10
    # SN.isable_villager_garrison=3
    SN.percent_civilian_explorers=0
    SN.minimum_civilian_explorers=0
    SN.cap_civilian_explorers=0
    SN.total_number_explorers=0
    SN.number_explore_groups=0
    SN.percent_civilian_builders=0
    SN.initial_exploration_required=0
    SN.disable_defend_groups=1
    SN.disable_attack_groups=1 
    SN.enable_new_building_system = 1

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
    SN.number_attack_groups = 0
    SN.maximum_town_size = 255
    SN.number_civilian_militia = 0
    SN.enable_new_building_system = 1 #I added this for stone mining
    SN.mill_max_distance = 50
    SN.camp_max_distance = 300
    SN.zero_priority_distance = 255
    SN.cap_civilian_explorers = 0
    SN.number_explore_groups = 0
    chat_to_all("Setters Ran!")
    disable_self()

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

#=====================================  Actual Code  ===================================================
#------deer stuff-------#
#search for deer around the town center and pick the closest one
up_full_reset_search()
up_set_target_point(p_home)
up_filter_distance(-1, LURE_DEER_DIST)
SN.focus_player_number = 0
up_find_remote(ClassId.prey_animal_class,40) #find 40 deer Max
up_remove_objects(SearchSource.search_remote, ObjectData.object_data_carry) < 70 #remove chickens
up_clean_search(SearchSource.search_remote, ObjectData.object_data_distance, SearchOrder.search_order_asc)
up_get_search_state(deer_search_state) #check how many deer were found

if deer_search_state.RemoteIndex > 0:
    deer_to_hunt = Integer()
    deer_already_hunted = Integer()
    already_hired_once = Integer()
    deer_to_hunt = -1
    for i in range(deer_search_state.RemoteIndex): # get unhunted deer
        up_set_target_object(SearchSource.search_remote, i)
        up_get_object_data(ObjectData.object_data_id, deer_id)
        deer_already_hunted = FALSE
        for j in range(J_DEER_PUSH_ARRAY_LENGTH):
            array_deer_id = J_deer_push_pray[j]
            if deer_id == array_deer_id:
                deer_already_hunted = TRUE
        if deer_already_hunted == FALSE:
            deer_to_hunt = deer_id
    
    if deer_to_hunt != -1:
        up_find_local(UnitId.militiaman, 10)
        up_get_search_state(deer_search_state)
        
        already_hired_once = 0
        if deer_search_state.LocalList > 0:
            for i in range(deer_search_state.LocalList):
                up_set_target_object(SearchSource.search_local, i)
                up_get_object_data(ObjectData.object_data_id, hunter_id)
                is_employed = J_get_employment_status(hunter_id)
                if is_employed == UNEMPLOYED and already_hired_once == 0:
                    J_HIRE_push_deer(hunter_id, deer_to_hunt)
                    already_hired_once = 1
                    


#===========================#
#|        Dark Age         |#
#===========================#

#class running functions
J_explore_object()
J_push_deer()
R_update_mines(Resource.gold)
R_update_mines(Resource.stone)


if current_age() == Age.dark_age:

    #=========find TC Location=========#
    if building_type_count_total(BuildingId.town_center) == 0:
        #region ___walk twords middle of map for 5 seconds___
        if True:
            up_full_reset_search()
            up_find_local(ClassId.villager_class, STARTING_VILL_COUNT)
            chat_to_all("walking to center")
            up_target_point(map_center_point, DUCAction.action_move,_, AttackStance.stance_no_attack)
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

                is_employed = J_get_employment_status(villager_id)
                #up_chat_data_to_all("employed: %d",is_employed)
                
                if is_employed == UNEMPLOYED:
                    villager_point.x, villager_point.y  = up_get_object_Point()
                    closest_gold_point.x, closest_gold_point.y = get_closest_resource_point(Resource.gold, villager_point)
                    if up_point_distance(villager_point, closest_gold_point) <= VILLAGER_LOS:
                        up_chat_data_to_all("HIRE!: %d",villager_id)
                        J_HIRE_explore_object(villager_id, Resource.gold, VILLAGER_LOS, 50, CLOCKWIZE)
        #endregion
        ##region ___after 5 seconds place a TC___
        if game_time() > BUILD_TC_TIME:
            if True:
                J_FIRE_ALL_explore_object()
                tc_location = Point()
                tc_location = get_best_nomad_tc_location()
                up_set_target_point(tc_location)
                up_build(PlacementType.place_point,_,BuildingId.town_center)
                disable_self()

            #if True:
            #    vil_point = Point()
            #    chat_to_all("Try Build House")
            #    up_full_reset_search()
            #    up_find_local(ClassId.villager_class, 2)
            #    up_set_target_object(SearchSource.search_local, 0)
            #    vil_point = up_get_object_Point()
            #    up_send_flare(vil_point)
            #    up_build_line(vil_point,vil_point,BuildingId.house)
            #    
            #    chat_to_all("Try Build Baracks")
            #    up_set_target_object(SearchSource.search_local, 1)
            #    vil_point = up_get_object_Point()
            #    up_send_flare(vil_point)
            #    up_build_line(vil_point,vil_point,BuildingId.barracks)
            #    disable_self()


            
        
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
'''
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
'''
#=============================#
#|       Basic stuff         |#
#=============================#
if (housing_headroom() < 3 
    and population_headroom() > 0 
    and building_type_count(BuildingId.town_center) > 0
): #to not build house while searching for TC on nomad
    chat_to_all("trying to build a house")
    try_build(BuildingId.house)

if building_type_count(BuildingId.barracks) < 1:
    try_build(BuildingId.barracks)

try_train(UnitId.villager)
try_train(UnitId.militiaman)

