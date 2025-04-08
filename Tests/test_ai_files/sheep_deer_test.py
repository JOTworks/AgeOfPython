from scraper.aoe2scriptFunctions import *
from scraper.aoe2scriptFunctions import (
    SN,unit_type_count,building_type_count,dropsite_min_distance,game_time,up_timer_status,chat_to_all,
    disable_self,up_clean_search,up_get_search_state,up_get_object_data,up_set_target_object,up_find_local,
    up_filter_distance,up_set_target_point,current_age,up_full_reset_search,up_get_point,up_find_remote,
    up_bound_point,chat_to_player,up_target_point,up_reset_scouts,up_reset_unit,up_remove_objects,
    up_set_target_by_id,up_copy_point,up_lerp_tiles,up_target_objects,up_bound_precise_point,up_set_timer,
    up_chat_data_to_all,
)
from scraper.aoe2scriptEnums import (
    compareOp,BuildingId,Resource,ClassId,LineId,SearchOrder,SearchSource,ObjectData,Point,State,
    PositionType,DUCAction,Formation,ActionId,AttackStance,TimerState
)
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
TimeToStopDeerLuring = 100
DistanceToShootDeer = 5
VillsToShootDeer = 2

#timers #todo: make timers alocate memory and pass into functions
t_sheep_claim = 1
t_deer_lure = 2
#Variables
deer_hp = 0
deer_id = 0
deer_lure_stage = 0
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
    up_chat_data_to_all("next to deer X:%d", point_next_to_deer.x)
    up_chat_data_to_all("next to deer Y:%d", point_next_to_deer.y)
    
    if deer_lure_stage != 100: #allow for exploration first
        #search for deer around the town center and pick the closest one
        up_full_reset_search()
        up_set_target_point(p_home)
        up_filter_distance(-1, 17)
        SN.focus_player_number = 0
        up_find_remote(Resource.deer_hunting, 40) #search 40 times for deer
        up_clean_search(SearchSource.search_remote, ObjectData.object_data_distance, SearchOrder.search_order_asc)
        up_remove_objects(SearchSource.search_remote, ObjectData.object_data_index, compareOp.greater_than, 0) #only closest
        up_get_search_state(search_state) #check how many deer were found
        
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
            up_bound_precise_point(point_next_to_deer, 1, 50) #Option unimplmented
            up_target_point(point_next_to_deer, DUCAction.action_move, Formation._1, AttackStance.stance_no_attack)
            SN.target_point_adjustment = 0 #reset

    #shooting Deer
    up_full_reset_search()
    up_set_target_point(p_home)
    up_filter_distance(-1, DistanceToShootDeer)
    SN.focus_player_number = 0
    up_find_remote(Resource.deer_hunting, 5) #find up to 5 deer
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
        up_find_remote(Resource.deer_hunting, 10)
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