from scraper import *
from scraper import (
  #OBJECT TYPES
  Point, Constant, State, Integer, Array, Timer, _,
  #ENUMS
  ObjectId, ObjectData, ObjectStatus, ObjectList, ClassId, UnitId, BuildingId, Resource, Terrain, SearchSource, PositionType, 
  PlacementType, Age, TechId, DUCAction, AttackStance, SN, SearchOrder, compareOp, ActionId, ResearchState, TimerState, ExploredState,
  #FUNCTIONS
  up_get_object_data, up_get_object_target_data, up_get_point, up_get_search_state, up_set_target_object, up_set_target_point,
  up_find_local, up_find_resource, up_filter_status, up_full_reset_search, up_get_point_terrain, timer_triggered, enable_timer, 
  disable_timer, up_chat_data_to_all, up_point_distance, resource_found, disable_self, up_build, current_age, up_can_train, 
  up_train, up_can_research, up_research, build, housing_headroom, population_headroom, building_type_count, up_lerp_tiles,
  up_set_target_by_id, up_target_point, building_type_count_total, chat_to_all, up_send_flare, up_filter_range, wood_amount,
  up_add_object_by_id, up_filter_distance, up_find_remote, up_remove_objects, up_clean_search,up_can_build, up_pending_objects, 
  up_copy_point, game_time,up_target_objects, unit_type_count, food_amount, up_find_status_local, up_research_status, 
  up_point_terrain, up_can_build_line, up_build_line, up_lerp_percent, idle_farm_count, up_timer_status, military_population, 
  attack_now, up_point_explored, research_completed,

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

#===================================PARAMETERS=====================================
BUILD_TC_TIME = Constant(30)
J_EXPLORE_OBJECT_ARRAY_SIZE = Constant(10)
J_DEER_PUSH_ARRAY_LENGTH = Constant(10)
J_SHEPERD_ARRAY_SIZE = Constant(1)
MINE_LIMIT = Constant(10)
SHOOT_DEER_DIST = 2
LURE_DEER_DIST = 50
VIL_SHOOT_DEER_COUNT = 4
HIT_DEER_COUNTER_TOTAL = Constant(15)
#===================================CONSTANTS======================================
VILLAGER_LOS = Constant(4)
DA_MILITIA_LOS = Constant(6)
STARTING_VILL_COUNT = Constant(3)
CLOCKWIZE = Constant(0)
COUNTER_CLOCKWIZE = Constant(1)
FALSE = Constant(0)
TRUE = Constant(1)
EMPLOYED = Constant(1)
UNEMPLOYED = Constant(0)
my_player_number = Integer(1)
enemy_player_number = Integer(2)


#================================== SETTERS ======================================#
if True:
    map_center_point = Point(0,0)
    map_west_corner = Point(0,0)
    map_east_corner = Point()
    i = Integer(0)
    up_get_point(PositionType.position_center, map_center_point)
    up_get_point(PositionType.position_map_size, map_east_corner)
    map_east_corner.x -= 1
    map_east_corner.y -= 1
    map_north_corner = Point(map_east_corner.x,0)
    map_south_corner = Point(0,map_east_corner.y)

    SN.placement_zone_size=7
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
    SN.minimum_attack_group_size = 10
    chat_to_all("Setters Ran!")
    disable_self()

    #setters

if building_type_count(BuildingId.town_center) > 0: #set TC location as p_home
    p_home = Point()
    p_home_100 = Point()
    up_full_reset_search()
    up_find_local(BuildingId.town_center, 1)
    up_set_target_object(SearchSource.search_local, 0)
    up_get_point(PositionType.position_object, p_home)
    p_home_100.x = p_home.x * 100
    p_home_100.y = p_home.y * 100
    chat_to_all("set TC location")
    disable_self()

#================================= FUNCTIONS =====================================#

def target_point(local_id:Integer, point:Point):
    global p_home
    up_full_reset_search()
    up_add_object_by_id(SearchSource.search_local, local_id)
    up_set_target_point(p_home)
    up_target_point(point,_,_,_)

def target_id(local_id:Integer, remote_id:Integer):
    up_full_reset_search()
    up_add_object_by_id(SearchSource.search_local, local_id)
    up_add_object_by_id(SearchSource.search_remote, remote_id)
    up_target_objects(0,_,_,_)     

def up_get_object_Point() -> (Integer, Integer): # type: ignore
    #chat_to_all("in up_get_object_Point")
    temp_point = Point()
    up_get_object_data(ObjectData.object_data_point_x, temp_point.x)
    up_get_object_data(ObjectData.object_data_point_y, temp_point.y)
    return temp_point.x, temp_point.y

def next_spiral_point(center_x:Integer, center_y:Integer, current_x:Integer, current_y:Integer, ring_width:Integer) -> Point:
    # Compute current radius from center (Manhattan-style)
    dx = Integer()
    dy = Integer()
    return_point = Point()
    dx = current_x - center_x
    dy = current_y - center_y
    
    #absolute value
    abs_dx = dx
    if dx < 0: 
        abs_dx = dx * -1 
        
    abs_dy = dy
    if dy < 0: 
        abs_dy = dy * -1

    current_radius = abs_dx + abs_dy

    # Find the next position in current ring
    step = ring_width  # The spacing between each spiral "ring"
    dx = current_x - center_x
    dy = current_y - center_y

    # Case: just starting at center
    if current_radius == 0:
        center_x = center_x + step
        return_point = (center_x, center_y)
        return return_point  # Start the first ring

    # Generate next point in the ring perimeter
    # Traverse ring perimeter clockwise: right -> up -> left -> down -> back to start
    neg_dx = dx * -1
    neg_dy = dy * -1
    if dx >= 0 and dy < dx and dy >= neg_dx:
        dy += step  # go up
    elif dy >= 0 and neg_dy < dx and dx <= dy:
        dx -= step  # go left
    elif dx <= 0 and dy > dx and dy <= neg_dx:
        dy -= step  # go down
    elif dy <= 0 and dx < dy and dy < neg_dx:
        dx += step  # go right
    elif True:
        # We've finished the current ring — go to next ring start (right of center)
        current_radius += step
        dx = current_radius
        dy = 0

    center_x += dx
    center_y += dy
    return_point = (center_x, center_y)
    return return_point


#=================================================================================#
#|                          RESROUCE MANAGER CLASS                               |#
#=================================================================================#

#gold
R_gold_mine_count = Integer(0)
R_gold_total_count = Integer()
R_gold_location = Array(Point, MINE_LIMIT)
R_gold_ammount = Array(Integer, MINE_LIMIT)
#stone
R_stone_mine_count = Integer(0)
R_stone_total_count = Integer()
R_stone_location = Array(Point, MINE_LIMIT)
R_stone_ammount = Array(Integer, MINE_LIMIT)

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
        part_of_existing_mine = Integer()
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

#=================================================================================#
#|                            JOB MANAGER CLASS                                  |#
#=================================================================================#
# job arrays for each type of job used
# each job should have a J_ J_HIRE and J_FIRE function at minimum

#____explore_object____#
# circle around a cluster of closest object, like gold
J_explore_object_ids = Array(Integer, J_EXPLORE_OBJECT_ARRAY_SIZE)
J_explore_object_things = Array(Integer, J_EXPLORE_OBJECT_ARRAY_SIZE) 
J_explore_object_tiles_away = Array(Integer, J_EXPLORE_OBJECT_ARRAY_SIZE) 
J_explore_object_direction = Array(Integer, J_EXPLORE_OBJECT_ARRAY_SIZE) #ClOCKWIZE or COUNTER_CLOCKWIZE
#____Deer Push____#
# push deer twards TCs, attack them if stuck in woodlines
J_deer_push_hunter = Array(Integer, J_DEER_PUSH_ARRAY_LENGTH)
J_deer_push_pray = Array(Integer, J_DEER_PUSH_ARRAY_LENGTH)
deer_id = Integer()
hunter_id = Integer()
deer_search_state = State()
#_____sheperd_____#
# pick up all the sheep and heardables
J_sheperd_ids = Array(Integer, J_SHEPERD_ARRAY_SIZE)
#___explore map___#
J_EXPLORE_MAP_ARRAY_SIZE = Constant(10)
J_explore_map_ids = Array(Integer, J_EXPLORE_MAP_ARRAY_SIZE)
J_explore_map_target_point = Array(Point, J_EXPLORE_MAP_ARRAY_SIZE)
J_explore_map_type = Array(Integer, J_EXPLORE_MAP_ARRAY_SIZE)
EXPLORE_TYPE_SIMPLE = Constant(1)
EXPLORE_TYPE_CORNERS = Constant(2)

#_________class functions_________#

def J_get_employment_status(id:Integer) -> Integer:
    #chat_to_all("in J_get_employment_status")
    global J_explore_object_ids, J_deer_push_hunter, J_explore_map_ids
    global EMPLOYED, UNEMPLOYED, J_EXPLORE_OBJECT_ARRAY_SIZE, J_DEER_PUSH_ARRAY_LENGTH, J_EXPLORE_MAP_ARRAY_SIZE
    i = Integer()
    array_id = Integer()
    for i in range(J_EXPLORE_OBJECT_ARRAY_SIZE):
        array_id = J_explore_object_ids[i]
        if array_id == id:
            return EMPLOYED
    for i in range(J_DEER_PUSH_ARRAY_LENGTH):
        array_id = J_deer_push_hunter[i]
        if array_id == id:
            return EMPLOYED
    for i in range(J_EXPLORE_MAP_ARRAY_SIZE):
        array_id = J_explore_map_ids[i]
        if array_id == id:
            return EMPLOYED
    return UNEMPLOYED

def J_get_unemployed_id(unit_type:UnitId) -> Integer:
    global J_explore_object_ids, J_deer_push_hunter, EMPLOYED, UNEMPLOYED
    unemployed_state = State()
    unit_id = Integer()
    up_full_reset_search()
    up_find_local(unit_type, 100)
    up_get_search_state(unemployed_state)
    for i in range(unemployed_state.LocalIndex):
        up_set_target_object(SearchSource.search_local, i)
        up_get_object_data(ObjectData.object_data_id, unit_id)
        is_employed = J_get_employment_status(unit_id)
        if is_employed == UNEMPLOYED:
            return unit_id
    return -1

#----------------------------------#
#      JOB explore_object          #
#----------------------------------#


def J_HIRE_explore_object(explorer_id:Integer, thing:ObjectId, tiles_away:Integer, explore_duration:Integer = 50, explore_direction:Integer = CLOCKWIZE) -> Integer:
    global J_explore_object_ids, J_explore_object_things, J_explore_object_tiles_away, J_explore_object_direction
    global EMPLOYED, UNEMPLOYED, J_EXPLORE_OBJECT_ARRAY_SIZE
    for i in range(J_EXPLORE_OBJECT_ARRAY_SIZE):
        array_explorer_id = J_explore_object_ids[i]
        if array_explorer_id == -1:
            up_chat_data_to_all("%d is HIRED to explore object", explorer_id)
            J_explore_object_ids[i] = explorer_id
            J_explore_object_things[i] = thing
            J_explore_object_tiles_away[i] = tiles_away
            J_explore_object_direction[i] = explore_direction

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
    global J_explore_object_ids, J_explore_object_things, J_explore_object_tiles_away, J_explore_object_direction, EMPLOYED, UNEMPLOYED
    for i in range(J_EXPLORE_OBJECT_ARRAY_SIZE):
        array_explorer_id = J_explore_object_ids[i]
        if array_explorer_id == explorer_id:
            up_chat_data_to_all("%d is FIRED from explore object", explorer_id)
            J_explore_object_ids[i] = -1
            J_explore_object_things[i] = -1
            J_explore_object_tiles_away[i] = -1
            J_explore_object_direction[i] = -1
            return UNEMPLOYED
    up_chat_data_to_all("%d did not have the explorer job", explorer_id)
    return UNEMPLOYED

def J_FIRE_ALL_explore_object():
    chat_to_all("in J_FIRE_explore_object")
    global J_explore_object_ids, J_explore_object_things, J_explore_object_tiles_away, J_explore_object_direction, EMPLOYED, UNEMPLOYED
    for i in range(J_EXPLORE_OBJECT_ARRAY_SIZE):
        array_explorer_id = J_explore_object_ids[i]
        up_chat_data_to_all("%d is FIRED from explore object", array_explorer_id)
        J_explore_object_ids[i] = -1
        J_explore_object_things[i] = -1
        J_explore_object_tiles_away[i] = -1
        J_explore_object_direction[i] = -1

def J_explore_object():
    global J_explore_object_ids, J_explore_object_things, J_explore_object_tiles_away, J_explore_object_direction, EMPLOYED, UNEMPLOYED
    explorer_point = Point()
    resource_point = Point()
    dest_point = Point()
    prime_point = Point()
    for i in range(J_EXPLORE_OBJECT_ARRAY_SIZE):

        explorer_id = J_explore_object_ids[i]
        if explorer_id != -1:
            thing = J_explore_object_things[i]
            tiles_away = J_explore_object_tiles_away[i]
            #the math #todo: fix this to use specific points, i think how it is, it wont work only using tile integeres
            up_full_reset_search()
            up_set_target_by_id(explorer_id)
            explorer_point = up_get_object_Point()
            resource_point = get_closest_resource_point(thing, explorer_point)
            dest_point = resource_point
            
            up_lerp_tiles(dest_point, explorer_point, tiles_away)
           
            #translate reletive
            #prime_point = resource_point - dest_point #todo:we want to be able to do this
            prime_point = resource_point
            prime_point -= dest_point
            #rotate 90
            temp = Integer()
            temp = prime_point.x
            prime_point.x = prime_point.y
            prime_point.y = temp * -1
            #translate back
            dest_point += prime_point

            up_full_reset_search()
            up_add_object_by_id(SearchSource.search_local, explorer_id)
            
            up_target_point(dest_point, DUCAction.action_move, _, _)

#----------------------------------#
#        JOB explore_map           #
#----------------------------------#

def J_HIRE_explore_map(explorer_id:Integer, explore_type:Integer) -> Integer:
    global J_explore_map_ids, J_explore_map_type, J_explore_map_target_point
    global UNEMPLOYED, EMPLOYED, J_EXPLORE_MAP_ARRAY_SIZE
    for i in range(J_EXPLORE_MAP_ARRAY_SIZE):
        array_explorer_id = J_explore_map_ids[i]
        if array_explorer_id == -1:
            up_chat_data_to_all("%d is HIRED to explore_map", explorer_id)
            up_chat_data_to_all("%d explore_type", explore_type)
            J_explore_map_ids[i] = explorer_id
            J_explore_map_type[i] = explore_type
            
            return EMPLOYED
    up_chat_data_to_all("%d did not have explore_map open", explorer_id)
    return UNEMPLOYED

def J_FIRE_explore_map(explorer_id:Integer) -> Integer:
    global J_explore_map_ids, J_explore_map_type, J_explore_map_target_point
    global UNEMPLOYED, EMPLOYED, J_EXPLORE_MAP_ARRAY_SIZE
    for i in range(J_EXPLORE_MAP_ARRAY_SIZE): #J_EXPLORE_OBJECT_ARRAY_SIZE
        array_explore_id = J_explore_map_ids[i]
        if array_explore_id == explorer_id:
            up_chat_data_to_all("%d is FIRED from explore_map", explorer_id)
            J_explore_map_ids[i] = -1
            J_explore_map_target_point[i] = (-1, -1)
            J_explore_map_type[i] = -1
            return UNEMPLOYED
    up_chat_data_to_all("%d did not have the explore_map job", explorer_id)
    return UNEMPLOYED

def J_explore_map_corners(j_explore_index:Integer) -> Integer:
    global J_explore_map_ids, J_explore_map_type, J_explore_map_target_point
    global map_west_corner, map_north_corner, map_east_corner, map_south_corner

    if True:
        TIME_FOR_ONE_SIDE = map_east_corner.x / 3
        WEST_C = 0
        NORTH_C = TIME_FOR_ONE_SIDE
        EAST_C = TIME_FOR_ONE_SIDE * 2
        SOUTH_C = TIME_FOR_ONE_SIDE * 3
        END_C = TIME_FOR_ONE_SIDE * 4
        disable_self()

    explorer_id = Integer()
    fake_corner_timer = Integer(-1)
    fake_corner_timer += 1
    if fake_corner_timer > END_C:
        fake_corner_timer = 0
    
    if fake_corner_timer >= WEST_C and fake_corner_timer < NORTH_C:
        explorer_id = J_explore_map_ids[j_explore_index]
        target_point(explorer_id, map_west_corner)
    
    if fake_corner_timer == NORTH_C and fake_corner_timer < EAST_C:
        explorer_id = J_explore_map_ids[j_explore_index]
        target_point(explorer_id, map_north_corner)

    if fake_corner_timer == EAST_C and fake_corner_timer < SOUTH_C:
        explorer_id = J_explore_map_ids[j_explore_index]
        target_point(explorer_id, map_east_corner)

    if fake_corner_timer == SOUTH_C and fake_corner_timer < END_C:
        explorer_id = J_explore_map_ids[j_explore_index]
        target_point(explorer_id, map_south_corner)

def J_explore_map_simple(J_explore_index:Integer) -> Integer:
    global J_explore_map_ids, J_explore_map_type, J_explore_map_target_point
    explorer_point = Point()
    explorer_target_point = Point()
    next_point = Point()
    explorer_id = Integer()
    explorer_id = J_explore_map_ids[J_explore_index]
    explorer_target_point = J_explore_map_target_point[J_explore_index]
    target_id(explorer_id)
    explorer_point = up_get_object_Point()
    if up_point_explored(explorer_target_point) == ExploredState.explored_no:
        target_point(explorer_id, explorer_target_point)
        return 1
    next_point = explorer_point
    for i in range(16):
        next_point = next_spiral_point(explorer_point.x,explorer_point.y,next_point.x,next_point.y,3)
        if up_point_explored(next_point) == ExploredState.explored_no:
            target_point(explorer_id, explorer_target_point)
            return 1
    J_FIRE_explore_map(explorer_id)

def J_explore_map():
    global J_explore_map_ids, J_explore_map_type, J_explore_map_target_point, J_EXPLORE_MAP_ARRAY_SIZE, EXPLORE_TYPE_SIMPLE, EXPLORE_TYPE_CORNERS
    explore_type = Integer()
    for i in range(J_EXPLORE_MAP_ARRAY_SIZE):
        explore_type = J_explore_map_type[i]
        if explore_type == EXPLORE_TYPE_SIMPLE:
            J_explore_map_simple(i)
        elif explore_type == EXPLORE_TYPE_CORNERS:
            J_explore_map_corners(i)

#----------------------------------#
#        JOB push_deer             #
#----------------------------------#

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
    global p_home, p_home_100, J_DEER_PUSH_ARRAY_LENGTH, SHOOT_DEER_DIST, LURE_DEER_DIST, VIL_SHOOT_DEER_COUNT
    global J_deer_push_hunter, J_deer_push_pray, deer_search_state, UNEMPLOYED, EMPLOYED
    for i in range(J_DEER_PUSH_ARRAY_LENGTH): #J_EXPLORE_OBJECT_ARRAY_SIZE
        array_hunter_id = J_deer_push_hunter[i]
        if array_hunter_id == hunter_id:
            up_chat_data_to_all("%d is FIRED from Push Deer", hunter_id)
            J_deer_push_hunter[i] = -1
            J_deer_push_pray[i] = -1
            return UNEMPLOYED
    up_chat_data_to_all("%d did not have the Push Deer job", hunter_id)
    return UNEMPLOYED

def J_push_deer():
    global p_home, p_home_100, J_DEER_PUSH_ARRAY_LENGTH, SHOOT_DEER_DIST, LURE_DEER_DIST, VIL_SHOOT_DEER_COUNT
    global J_deer_push_hunter, J_deer_push_pray
    deer_search_state = State()
    hit_deer_counter = Integer(0)
    hit_deer_counter += 1
    if hit_deer_counter >= 15:
        hit_deer_counter = 0
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
                if hit_deer_counter == 0: #once every HIT_DEER_COUNTER_TOTAL times, Attach deer instead of push. this keep from getting stuck on woodlines
                    #up_full_reset_search()
                    #up_filter_distance(-1,3)
                    #up_filter_status(ObjectStatus.status_ready, ObjectList.list_active)
                    #up_find_resource(Resource.wood,10)
                    #up_get_search_state(deer_search_state)
                    #up_chat_data_to_all("trees neer deer %d", deer_search_state.RemoteList)
                    #if deer_search_state.RemoteList >= 10:
                    up_add_object_by_id(SearchSource.search_local, hunter_id)
                    up_target_objects(1,_,_,AttackStance.stance_aggressive)

                if hit_deer_counter != 0:
                    point_next_to_deer = deer_point
                    up_lerp_tiles(point_next_to_deer, p_home_100, -75) #move point one-quarter tile away from tc so the scout will be behind the deer

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

#----------------------------------#
#        JOB lure_boar             #
#----------------------------------#

#----------------------------------#
#        JOB collect_heardables    #
#----------------------------------#

def J_HIRE_sheperd(hearder_id:Integer, sheep_id:Integer):
    pass
    #store the variables needed

def J_FIRE_sheperd():
    pass

def J_sheperd():
    global deer_search_state, p_home
    for i in range(J_SHEPERD_ARRAY_SIZE):
        up_full_reset_search()
        up_set_target_point(p_home)
        SN.focus_player_number = 0 #to find gaia, need to focus player 0
        up_find_remote(ClassId.livestock_class, 5) #try to add one sheep to the remote list #todo: livestock_class is 958
        up_get_search_state(deer_search_state) #to set up the check

        if deer_search_state.RemoteIndex > 0: #found a sheep last rule
            sheep_id = Integer()
            hearder_id = Integer()
            up_clean_search(SearchSource.search_remote, ObjectData.object_data_distance, SearchOrder.search_order_asc) #use closest sheep
            up_set_target_object(SearchSource.search_remote, 0) #get the position as above
            up_get_object_data(ObjectData.object_data_id, sheep_id)
            
            hearder_id = J_get_unemployed_id(UnitId.militiaman)
            if hearder_id != -1:
                J_HIRE_sheperd(hearder_id, sheep_id)
    # i need to task the shepard to move to the sheep and call it good.
    
    #also need to add the arrays

    # fire shepard on complete and rehire if there is another sheep close by
    # fire if sheep dies

#_________functions kickoff_________#
J_explore_object()
J_push_deer()
J_sheperd()
J_explore_map()
R_update_mines(Resource.gold)
R_update_mines(Resource.stone)

#====================END OF CLASSES========================#


#======================================================  Functions  ===========================================================#


def build_around_tc(building:BuildingId, radius:Integer) -> Integer:
    global p_home
    place_point = Point()
    if p_home.x == -1:
        chat_to_all("E: tc_location not set, cannot build_around_tc")
        return -1
    place_point = p_home + (radius, radius)
    if up_can_build_line(_, place_point, building):
        up_build_line(place_point,place_point, building)
        return 1
    place_point = p_home - (radius, radius)
    if up_can_build_line(_, place_point, building):
        up_build_line(place_point,place_point, building)
        return 1
    place_point = p_home + (radius, radius)
    if up_can_build_line(_, place_point, building):
        up_build_line(place_point,place_point, building)
        return 1
    place_point = p_home - (radius, radius)
    if up_can_build_line(_, place_point, building):
        up_build_line(place_point,place_point, building)
        return 1

def build_at_point(start_point:Point, Building:BuildingId) -> Integer:
    global TRUE, FALSE
    original_point = start_point
    radius = Integer(0)
    dx = Integer()
    dy = Integer()
    abs_dx = Integer()
    radius = 0
    point1 = Point()
    point2 = Point()
    z = Integer()
    for z in range(6): #number of rings to check
        dx = radius * -1
        while dx <= radius:
            abs_dx = dx
            if dx < 0:
                abs_dx = dx * -1
            dy = radius - abs_dx

            # Top point in ring
            point1.x = start_point.x + dx
            point1.y = start_point.y + dy
            if up_can_build_line(_,point1,Building):
                up_build_line(point1, point1, Building)
                return TRUE

            # Bottom point in ring, avoid duplicate when dy == 0
            if dy != 0:
                point2.x = start_point.x + dx
                point2.y = start_point.y - dy
                if up_can_build_line(_,point2,Building):
                    up_build_line(point2, point2, Building)
                    return TRUE
            dx += 1
        radius += 1
    up_set_target_point(original_point)
    up_build(PlacementType.place_point,_,Building)
    return FALSE

def set_gather_percent(wood:Integer, food:Integer, gold:Integer, stone:Integer):
    SN.wood_gatherer_percentage = wood
    SN.food_gatherer_percentage = food
    SN.gold_gatherer_percentage = gold
    SN.stone_gatherer_percentage = stone

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

def get_closest_resource_point(resource:Resource, point:Point) -> (Integer, Integer): # type: ignore
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
                up_lerp_percent(wood_loc, gold_loc, 50)
                return wood_loc #half way between gold and wood with the lerp

    return map_center_point

def try_train(unit:UnitId):
    if up_can_train(unit):
        up_train(unit)

def try_research(tech_id:TechId):
    if up_can_research(tech_id):
        up_research(tech_id)

def try_build(building:BuildingId) -> Integer:
    if up_can_build(_, building) and up_pending_objects(building) < 1:
        up_build(_,_,building)
        return 1
    return 0


#=================================================================================#
#|                            CODE EXECUTION START                               |#
#=================================================================================#



#===========================#
#|        Dark Age         |#
#===========================#
if current_age() == Age.dark_age:
    #setters
    if True:
        villager_cap = 20
        disable_self()

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
                villager_id = Integer()
                up_get_object_data(ObjectData.object_data_id, villager_id)
                is_employed = J_get_employment_status(villager_id)
                #up_chat_data_to_all("employed: %d",is_employed)
                
                if is_employed == UNEMPLOYED:
                    villager_point = Point()
                    villager_point = up_get_object_Point()
                    closest_gold_point = Point()
                    closest_gold_point = get_closest_resource_point(Resource.gold, villager_point)
                    if up_point_distance(villager_point, closest_gold_point) <= VILLAGER_LOS:
                        up_chat_data_to_all("HIRE!: %d",villager_id)
                        J_HIRE_explore_object(villager_id, Resource.gold, VILLAGER_LOS, 50, CLOCKWIZE)
        #endregion
        ##region ___after 5 seconds place a TC___
        if game_time() > BUILD_TC_TIME:
            if True: #place TC
                J_FIRE_ALL_explore_object()
                nomad_tc_location = Point()
                nomad_tc_location = get_best_nomad_tc_location()
                chat_to_all("try building a TC_location")
                build_at_point(nomad_tc_location, BuildingId.town_center_foundation)
                disable_self()

    if building_type_count_total(BuildingId.town_center) == 1: #task all villegers to build TC
        tc_search_state = State()
        chat_to_all("TASK VILLIGERS TO BUILD TC")
        #TC to target object
        up_full_reset_search()
        up_filter_status(ObjectStatus.status_pending, ObjectList.list_active)
        up_find_status_local(ObjectId.town_center_foundation,1)
        up_set_target_object(SearchSource.search_local,0)
        #Task viligers to TC
        up_full_reset_search()
        up_find_local(ClassId.villager_class, STARTING_VILL_COUNT)
        up_target_objects(1,_,_,_)
        #set farthest villager from TC to target object
        up_clean_search(SearchSource.search_local, ObjectData.object_data_distance, SearchOrder.search_order_desc)
        up_get_search_state(tc_search_state)
        #set IDs
        house_villager_id = Integer()
        up_set_target_object(SearchSource.search_local,1)
        up_get_object_data(ObjectData.object_data_id, house_villager_id)
        barrack_villager_id = Integer() #needs to happen second so villager point is this one
        up_set_target_object(SearchSource.search_local,0)
        up_get_object_data(ObjectData.object_data_id, barrack_villager_id)
        #use farthest vil point to build barrack
        villager_point = up_get_object_Point()
        build_at_point(villager_point, BuildingId.barracks)
        disable_self()

    if building_type_count_total(BuildingId.town_center) == 1 and building_type_count_total(BuildingId.barracks) == 1:
        #task to barracks
        barracks_point = Point()
        up_full_reset_search()
        up_filter_status(ObjectStatus.status_pending, ObjectList.list_active)
        up_find_status_local(ObjectId.barracks,1)
        up_set_target_object(SearchSource.search_local,0)
        barracks_point = up_get_object_Point()
        up_set_target_point(barracks_point)
        up_full_reset_search()
        up_add_object_by_id(SearchSource.search_local, barrack_villager_id)
        up_target_objects(1,_,_,_)
        #use farthest vil point to build house
        up_set_target_by_id(house_villager_id)
        villager_point = up_get_object_Point()
        build_at_point(villager_point, BuildingId.house)
        disable_self()

    if building_type_count_total(BuildingId.town_center) == 1 and building_type_count_total(BuildingId.house) == 1:
        #task to barracks
        house_point = Point()
        up_full_reset_search
        up_filter_status(ObjectStatus.status_pending, ObjectList.list_active)
        up_find_status_local(ObjectId.house,1)
        up_set_target_object(SearchSource.search_local,0)
        house_point = up_get_object_Point()
        up_set_target_point(house_point)
        up_full_reset_search()
        up_add_object_by_id(SearchSource.search_local, house_villager_id)
        up_target_objects(1,_,_,_)
        disable_self()

    ##==========Exploring==========#
    # move sheep to TC
    if building_type_count(BuildingId.town_center) > 0:
        up_full_reset_search()
        up_set_target_point(nomad_tc_location)
        up_filter_distance(5,100)
        up_find_local(ClassId.livestock_class, 5)
        up_target_point(nomad_tc_location)

    #==========Economy==========#
    if True: # setters
        DA_wood_needed = 85 #160 start with enought for a house, barrack, TC. need 160 for mulecart + 4 more hourses
        set_gather_percent(20,80,0,0)
        disable_self()

    if up_research_status(TechId.feudal_age) < ResearchState.research_pending:
        if building_type_count_total(BuildingId.house) >= 5:
            DA_wood_needed -= 25
            disable_self()

        if building_type_count_total(BuildingId.mule_cart) >= 1:
            DA_wood_needed -= 65
            disable_self()

        if DA_wood_needed != 0:
            if wood_amount() < DA_wood_needed:
                set_gather_percent(20,80,0,0)
            else:
                set_gather_percent(10,90,0,0)

    if up_research_status(TechId.feudal_age) == ResearchState.research_pending:
        set_gather_percent(10,40,50,0)
        
    

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

    ##==========Defensive==========#
    ##region ___decide where to build house for walling___
    ##endregion
    ##region ___bring malitia back if there is shinanigans___
    ##endregion
    #pass

#=============================#
#|        Feudal Age         |#
#=============================#
if current_age() == Age.feudal_age:
    #setters
    if True:
        villager_cap = 60
        disable_self()

    #__kill buildings__
    #1. train malitia on the way up
    
    try_research(TechId.ri_man_at_arms)
    try_research(TechId.ri_long_swordsman)
    try_research(TechId.ri_arson)

    if wood_amount() > 350 and building_type_count_total(BuildingId.blacksmith) < 1:
        try_build(BuildingId.blacksmith)

    #up_full_reset_search()
    #found_building = 0
    #if up_find_remote(BuildingId.dock,1) and found_building == 0:
    #    up_find_local(UnitId.militiaman,5)
    #    found_building = 1
    #    up_target_objects(0,DUCAction.action_attack_move,_,_)
    #if up_find_remote(BuildingId.archery_range,1) and found_building == 0:
    #    up_find_local(UnitId.militiaman,5)
    #    up_target_objects(0,DUCAction.action_attack_move,_,_)
    #    found_building = 1
    #if up_find_remote(BuildingId.stable,1) and found_building == 0:
    #    up_find_local(UnitId.militiaman,5)
    #    up_target_objects(0,DUCAction.action_attack_move,_,_)
    #    found_building = 1
    #found_building = 0
    
    #3. attack plan to kill dock, one guy to keep curcling
    #4. attack plan to kill other buildings. specificaly target archery ranges
    #
    #__Eco__
    try_research(TechId.ri_double_bit_axe)
    try_research(TechId.ri_gold_mining)
    if True: # setters
        set_gather_percent(30,50,20,0)
        disable_self()
    #1. mule cart to get farther away hunt (mule cart to block bores)(build houses with these viligers)(now that military is attacking)
    #2. mill far away berries if no hunt availible, or get gold/stone if i dont need more food
    #3. mule cart for more efective wood gathering
    #4. mule cart upgrades as fast as possible/both if i have 2 out at the same time
    #5. if no docks, build fishingships, if not build mill and farms last case canario
    #
    #__defence__
    #try_research(TechId.ri_pikeman)
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
    #setters
    if True:
        villager_cap = 100
        disable_self()

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
#|        Castle Age         |#
#=============================#
if current_age() == Age.imperial_age:
    if True:
        villager_cap = 130
        disable_self()

#=============================#
#|   Houseing & Villigers    |#
#=============================#

if (housing_headroom() < 3 
    and population_headroom() > 0 
    and building_type_count(BuildingId.town_center) > 0
): #to not build house while searching for TC on nomad
    success = Integer()
    success = build_around_tc(BuildingId.house, 10)
    if success != 1:
        try_build(BuildingId.house)

if building_type_count(BuildingId.barracks) < 1:
    try_build(BuildingId.barracks)

if wood_amount() > 300 and current_age() > Age.dark_age and building_type_count(BuildingId.barracks) < 8:
    try_build(BuildingId.barracks)

if building_type_count(BuildingId.mule_cart) < 1 and food_amount() > 300:
    SN.mule_cart_dropsite_placement = Resource.wood
    try_build(BuildingId.mule_cart)

if building_type_count(BuildingId.mill) < 1 and resource_found(Resource.food):
    try_build(BuildingId.mill)

if unit_type_count(UnitId.villager) < villager_cap:
    try_train(UnitId.villager)

#=============================#
#|   Military Prodection     |#
#=============================#
if (
    building_type_count(BuildingId.barracks) < 1
    or (wood_amount() > 300 and current_age() > Age.dark_age)
):
    try_build(BuildingId.barracks)

if food_amount() > 100:
    if (
        unit_type_count(UnitId.militiaman) < 5
        or up_research_status(TechId.feudal_age) >= ResearchState.research_pending
    ):
        try_train(UnitId.militiaman)

t_attack_timer = Timer()
if (
    current_age() >= Age.feudal_age
    and research_completed(TechId.ri_long_swordsman)
):
    if up_timer_status(t_attack_timer) != TimerState.timer_running and military_population() > 10:
        set_strategic_number(SN.special_attack_type2, BuildingId.lumber_camp) #SN.special_attack_type2 = BuildingId.lumber_camp
        set_strategic_number(110, 1) #SN.special_attack_influence2 = 1
        
        attack_now()
        chat_to_all("attack!")
        enable_timer(t_attack_timer, 60)
        SN.disable_attack_groups=0
        SN.number_attack_groups=1
    if strategic_number(SN.disable_attack_groups) == 0 and military_population() < 5:
        chat_to_all("Retreat!")
        SN.disable_attack_groups=1
        SN.number_attack_groups=0

#=============================#
#|     Econ Buildings        |#
#=============================#
if building_type_count(BuildingId.mule_cart) < 1 and food_amount() > 300:
    SN.mule_cart_dropsite_placement = Resource.wood
    try_build(BuildingId.mule_cart)

if building_type_count(BuildingId.mill) < 1 and resource_found(Resource.food):
    try_build(BuildingId.mill)

if current_age() > Age.dark_age and wood_amount() > 100 and idle_farm_count() == 0:
    try_build(BuildingId.farm)



#__________recruting for Jobs__________#
#----finding 1 melitia to circle the map---#
map_corner_explorer_id = J_get_unemployed_id(UnitId.militiaman)
if map_corner_explorer_id != -1:
    J_HIRE_explore_map(map_corner_explorer_id, EXPLORE_TYPE_CORNERS)
    disable_self()



#----finding deer and militia to Hire as Deer Pushers---#
#todo: move this to the deer push function
up_full_reset_search()
up_set_target_point(p_home)
up_filter_distance(8, LURE_DEER_DIST)
SN.focus_player_number = 0
up_find_remote(ClassId.prey_animal_class,40) #find 40 deer Max
up_remove_objects(SearchSource.search_remote, ObjectData.object_data_carry) < 70 #remove chickens
up_clean_search(SearchSource.search_remote, ObjectData.object_data_distance, SearchOrder.search_order_asc)
up_get_search_state(deer_search_state) #check how many deer were found

if deer_search_state.RemoteIndex > 0:
    deer_to_hunt = Integer()
    deer_already_hunted = Integer()
    deer_to_hunt = -1
    for i in range(deer_search_state.RemoteIndex): # get unhunted deer
        up_set_target_object(SearchSource.search_remote, i)
        up_get_object_data(ObjectData.object_data_id, deer_id)
        deer_already_hunted = FALSE
        for j in range(J_DEER_PUSH_ARRAY_LENGTH):
            array_deer_id = J_deer_push_pray[j]
            if deer_id == array_deer_id:
                deer_already_hunted = TRUE
                break
        if deer_already_hunted == FALSE:
            deer_to_hunt = deer_id
            break
    
    if deer_to_hunt != -1: #get milita to hunt the deer
        up_find_local(UnitId.militiaman, 10)
        up_get_search_state(deer_search_state)
        for j in range(deer_search_state.LocalList):
            up_set_target_object(SearchSource.search_local, j)
            up_get_object_data(ObjectData.object_data_id, hunter_id)
            is_employed = J_get_employment_status(hunter_id)
            if is_employed == UNEMPLOYED:
                J_HIRE_push_deer(hunter_id, deer_to_hunt)
                break