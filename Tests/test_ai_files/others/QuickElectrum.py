from scraper.aoe2scriptFunctions import *
from scraper.aoe2scriptFunctions import (
    SN,
    unit_type_count,
    can_build,
    building_type_count,
    up_pending_objects,
    up_resource_amount,
    dropsite_min_distance,
    food_amount,
    can_research,
    research,
    can_train,
    train,
    building_type_count_total,
    up_set_timer,
    enable_timer,
    timer_triggered,
    disable_timer,
    game_time,
    up_drop_resources,
    up_modify_goal,
    up_remaining_boar_amount,
    up_compare_sn,
    up_timer_status,
    up_send_scout,
    chat_to_all,
    disable_self,
    housing_headroom,
    build,
    set_goal,
    unit_type_count_total,
    research_completed,
    can_sell_commodity,
    sell_commodity,
    wood_amount,
    idle_farm_count,
    military_population,
    attack_now,
    up_chat_data_to_all,
    up_clean_search,
    up_get_search_state,
    up_filter_status,
    up_send_flare,
    up_get_object_data,
    up_set_target_object,
    up_find_local,
    up_filter_distance,
    up_set_target_point,
    up_reset_filters,
    up_find_resource,
    up_get_fact,
    up_reset_search,
    up_build,
    up_find_status_local,
    up_can_research,


)
from scraper.aoe2scriptEnums import *
from scraper.aoe2scriptEnums import (
    UnitId,
    compareOp,
    ObjectId,
    BuildingId,
    Resource,
    TechId,
    ClassId,
    LineId,
    GroupType,
    ScoutMethod,
    ResourceType,
    Commodity,
    SearchOrder,
    SearchSource,
    ObjectData,
    ObjectList,
    ObjectStatus,
    FactId,
    Point,
    State,
    PlacementType,
)

#(load "Quicksilver/UserPatchFile")
#
##load-if-defined HUN-CIV
#    (load "Quicksilver/ConstantsHuns")
##else    
#    (load "Quicksilver/Constants")
##end-if

#(load "Quicksilver/HowOldAmI")
#;(load "Quicksilver/WallThemInFinal")
#(load "Quicksilver/WallThemInNoTimers")
#;(load "Quicksilver/SheepClaimandDeerLure")
#(load "Quicksilver/Operationpopulation")
#(load "Quicksilver/OneMoreMiningCampPlease")

#todo: while while_conditional: #doest work becuase test canot be a variable
#todo: while_conditional = True #doesnt work because its a boolean currently

#todo: make else work
#todo: make sure not, and, or, and nesting works for conditionals.
#todo: figure out comparators
#todo: figure out how to do defconst basically


g_current_age = 0
g_its_tower_time = 0
g_one_more_gold_mining_camp_please = 0
g_one_more_stone_mining_camp_please = 0
timer_running = 0

c_castle_age = 0
c_castle_age = 0
c_researching_castle_age = 0
c_feudal_age = 0
c_researching_feudal_age = 0
c_dark_age = 0
c_dark_age_pop_cap = 0
c_tower_timer = 0
c_imperial_age = 0
t_attack_timer = 0

#------------ONE MORE MINING CAMP PLEASE------------#
#set g-one-more-gold-mmining-camp-please to 1/yes to trigger the code and then set it to 2 again at the end of the code
#same with g-one-more-stone-mining-camp-please, then they won't interfere. Will need loops here too. Do I need separate loop names? I don't think so.
#can't choose location, would have to have parameters and be an actual function
def make_one_more_mining_camp(resource :Resource):
    #! making state adn point objects dosnt work in functions, it may not work outside of them as well
    #resource_state = State()
    #mining_camp_state = State()
    #mining_camp_state_pending = State()
    #resource_point = Point()
    resource_found_count = 0
    up_reset_search(0, 0, 1, 1) #full reset instead?
    up_reset_filters() #to hide the filters from other rules
    SN.focus_player_number = 0
    up_get_fact(FactId.gaia_type_count, resource, resource_found_count) #count resource found #! this may not work, was stone, but not sure if resource is the same int value
    up_filter_status(ObjectStatus.status_resource, ObjectList.list_active) #specify resource search
    up_find_resource(resource, resource_found_count) #find resource and store instances in remote list ;what remote list????
    up_get_search_state(resource_state) #is this seriously the line I've been missing?????
    up_clean_search(SearchSource.search_remote, ObjectData.object_data_distance, SearchOrder.search_order_asc)
    up_chat_data_to_all("I found %d piles of resource", resource_found_count) #report resource count

    #for each instance of resource, search for a nearby mining camp
    for i in range(resource_found_count):
        #--get resource location--#
        up_set_target_object(SearchSource.search_remote, i) #target first stored resource
        up_get_object_data(ObjectData.object_data_point_x, resource_point.x) #locate x of next resource
        up_get_object_data(ObjectData.object_data_point_y, resource_point.y) #locate y of next resource
        up_send_flare(resource_point) #flare resource ;this flared a single pile of resource 20 times...aah, because I didn't reset my filters
        chat_to_all("Flaring resource")

        #--get count of nearby mining camps--#
        up_reset_search(1, 1, 0, 0) #why am I resetting the search here? Oh, just local, the gaia resource is in remote
        up_reset_filters() #to hide the filters from other rules
        up_set_target_point(resource_point)
        up_filter_distance( -1, 10)
        up_find_local(ObjectId.mining_camp, 1)
        up_get_search_state(mining_camp_state)
        up_filter_status(ObjectStatus.status_pending, ObjectList.list_active)
        up_find_status_local(ObjectId.mining_camp, 1)
        up_get_search_state(mining_camp_state_pending)
        #untill we have c3 and not just c2, we can do this last one sadly and have to use 2 statments
        #g_nearby_mining_camp_count = mining_camp_state + mining_camp_state_pending
        g_nearby_mining_camp_count = mining_camp_state
        g_nearby_mining_camp_count += mining_camp_state_pending

        if ( g_nearby_mining_camp_count == 0 #if no mining camps were found
            and can_build(BuildingId.mining_camp)  
            and up_pending_objects(ObjectId.mining_camp) == 0 #if we are building no mining camps ;should probably be stated in the rule I call for it
        ): #! was the line before, does this make any sense having c:< ??? (up-pending-objects c:< mining-camp == 0)
            chat_to_all("Placing stone mining camp")  
            SN.placement_zone_size = 2
            up_set_target_point(resource_point)
            up_build(PlacementType.place_point, 0, BuildingId.mining_camp)
            return


def set_gatherer_percentages(wood, food, gold, stone):
    SN.wood_gatherer_percentage = wood
    SN.food_gatherer_percentage = food
    SN.gold_gatherer_percentage = gold
    SN.stone_gatherer_percentage = stone


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

#------------SHEEP CLAIM-------------#
SheepSearchDistance = 30
t_sheep_claim = Timer()
point = Point()
p_point = Point()
gl_sheep_blaim = 0
SPLIT = 0
search_state = State()
#;(defconst lt 254)
#;(defconst ll 255)
#;(defconst rt 256)
#;(defconst rl 257)

if current_age() == Age.dark_age and unit_type_count(LineId.scout_cavalry_line) == 1:
    up_full_reset_search()
    up_find_local(LineId.scout_cavalry_line, 1) #add scout to local list
    up_set_target_object(SearchSource.search_local, 0) #do this to get his position
    up_get_point(PositionType.position_object, p_point) #save position in point
    up_set_target_point(p_point)
    up_filter_distance(-1, SheepSearchDistance) #don't look too far from the scout
    SN.focus_player_number = 0 #to find gaia, need to focus player 0
    up_find_remote(958, 1) #try to add one sheep to the remote list #todo: livestock_class is 958
    up_get_search_state(search_state) #to set up the check

    searchSource = SearchSource.search_remote
    if search_state.RemoteIndex > 0: #found a sheep last rule
        up_full_reset_search()
        up_filter_distance(-1, SheepSearchDistance) #still uses last target point 
        up_find_remote(958, 5) #livestock_class
        up_clean_search(SearchSource.search_remote, ObjectData.object_data_distance, SearchOrder.search_order_asc) #use closest sheep
        up_set_target_object(SearchSource.search_remote, 0) #get the position as above
        up_get_point(PositionType.position_object, p_point)
        up_bound_point(p_point, p_point) #be sure the point is on the map
        up_find_local(LineId.scout_cavalry_line, 1) #add the scout to the local list
        up_target_point(p_point, DUCAction.action_move, -1, AttackStance.stance_no_attack) #target the position of the sheep
        chat_to_player(PlayerNumber.my_player_number, "Move") #todo: add my_plyaer_number
        enable_timer(t_sheep_claim, 4)
        g_sheep_claim = 1

    if g_sheep_claim == 1 and timer_triggered(t_sheep_claim): #reset the scout once the timer runs out (means the above rule hasn't fired, which means there are no more sheep nearby)
        chat_to_player(PlayerNumber.my_player_number, "Reset scout")
        disable_timer(t_sheep_claim)
        g_sheep_claim = 2
        up_reset_scouts() #reset everything

#------------DEER LURE-------------#
TimeBeforeDeerLuring = 270
TimeToStopDeerLuring = 550
DistanceToShootDeer = 5
VillsToShootDeer = 2
t_deer_lure = Timer()

s_deer = State()

deer_hp = 0
deer_id = 0
deer_lure_stage = 0
p_home = Point()
p_point = Point()
p_object = Point()
p_point2 = Point()

if building_type_count(BuildingId.town_center) > 0:
    up_full_reset_search()
    up_find_local(BuildingId.town_center, 1)
    up_set_target_object(SearchSource.search_local, 0)
    up_get_point(PositionType.position_object, p_home)
    disable_self()

if True:
    SN.home_exploration_time == TimeToStopDeerLuring
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
    if deer_lure_stage != 100: #allow for exploration first
        #search for deer around the town center and pick the closest one
        up_full_reset_search()
        up_set_target_point(p_home)
        up_filter_distance(-1, 17)
        SN.focus_player_number = 0
        up_find_remote(Resource.deer_hunting, 40) #search 40 times for deer
        up_clean_search(SearchSource.search_remote, ObjectData.object_data_distance, SearchOrder.search_order_asc)
        up_remove_objects(SearchSource.search_remote, ObjectData.object_data_index, compareOp.greater_than, 0) #only closest
        up_get_search_state(s_deer) #check how many deer were found
        
        if deer_lure_stage == -1 and s_deer.RemoteIndex >= 1 and up_set_target_object(SearchSource.search_remote, 0):
            up_get_object_data(ObjectData.object_data_id, deer_id) #get the id of the deer
            deer_lure_stage = 0 #start pushing the deer

        if up_set_target_by_id(deer_id): #update chosen deer's position and hp every pass
            up_full_reset_search()
            up_get_object_data(ObjectData.object_data_hitpoints, deer_hp)
            up_get_object_data(ObjectData.object_data_precise_x, p_object.x) #get the precise coordinates
            up_get_object_data(ObjectData.object_data_precise_y, p_object.y)
            up_copy_point(p_point2, p_home) #need to multiply by 100 for precise
            p_point2.x = p_point2.x * 100
            p_point2.y = p_point2.y * 100


        if deer_hp > 0 and up_set_target_by_id(deer_id): #if the deer is still alive
            chat_to_all("Push The Deer")
            up_copy_point(p_point, p_object) #copy deer position into a second point
            up_lerp_tiles(p_point, p_point2, -75) #move point one-quarter tile away from tc so the scout will be behind the deer
            up_full_reset_search()
            up_find_local(LineId.scout_cavalry_line, 1)
            SN.target_point_adjustment = 6 #set to enable precise targetting
            up_bound_precise_point(p_point, 1, 50) #Option unimplmented
            up_target_point(p_point, DUCAction.action_move, Formation._1, AttackStance.stance_no_attack)
            SN.target_point_adjustment = 0 #reset

    #shooting Deer
    up_full_reset_search()
    up_set_target_point(p_home)
    up_filter_distance(-1, DistanceToShootDeer)
    SN.focus_player_number = 0
    up_find_remote(Resource.deer_hunting, 5) #find up to 5 deer
    up_remove_objects(SearchSource.search_remote, ObjectData.object_data_carry, compareOp.less_than, 120) #only live deer
    up_get_search_state(s_deer) #see how many were found

    #shoot the deer if not hunting boar and one is near the tc
    if ( s_deer.RemoteIndex >= 1 #deer found near tc
        and up_timer_status(t_deer_lure) != timer_running #this is so the command doesnt loop continuously
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
        enable_timer(t_deer_lure, 15) #wait awhile before allowing this rule to fire again

        #reset the system once deer is shot
        if deer_hp < 2 and deer_lure_stage >= 0 and deer_lure_stage != 100:
            up_reset_unit(LineId.scout_cavalry_line)
            chat_to_all("Deer Shot--Reset")
            deer_lure_stage = -1
            deer_id = -1
            up_reset_scouts()

#==END======SHEEP CLAIM AND DEER LURE=======#


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

if unit_type_count(UnitId.villager) == 8:
    SN.food_gatherer_percentage = 75
    SN.wood_gatherer_percentage = 25
    disable_self()

#------building house, lumber camp, mill, mining camp, barracks------#
if can_build(BuildingId.house):
    if ( housing_headroom() < 2
        and up_pending_objects(ObjectId.house) < 1 #! does c:< make sense as a first arg of 4? (up-pending-objects c:< house < 1)
        and g_current_age <= c_researching_castle_age
        ):
        build(BuildingId.house)

    if ( housing_headroom() < 5
        and up_pending_objects(ObjectId.house) < 2
        and g_current_age > c_researching_castle_age
        ):
        build(BuildingId.house)

if can_build(BuildingId.lumber_camp):
    if ( unit_type_count(UnitId.villager) >= 7
        and building_type_count(BuildingId.lumber_camp) < 1
        and up_pending_objects(BuildingId.lumber_camp) < 1
        ):
        build(BuildingId.lumber_camp)

    if ( building_type_count_total(BuildingId.lumber_camp) > 0
        and dropsite_min_distance(Resource.wood) > 4
        and dropsite_min_distance(Resource.wood) < 255
        ):
        build(BuildingId.lumber_camp)

if ( can_build(BuildingId.mill)
    and unit_type_count(UnitId.villager, compareOp.greater_or_equal, 10)
    and building_type_count_total(BuildingId.mill, compareOp.less_than, 1)
    ):
    build(BuildingId.mill)

if ( can_build(BuildingId.mining_camp)
    and g_current_age == c_researching_castle_age
    and g_current_age == c_dark_age #! nichole these cant both be true? am i missing something
    and building_type_count_total(BuildingId.mining_camp, compareOp.equal, 0)
    ):
    build(BuildingId.mining_camp)

if ( can_build(BuildingId.barracks)
    and building_type_count(BuildingId.mill, compareOp.greater_or_equal, 1)
    and building_type_count(BuildingId.barracks, compareOp.less_than, 1)
    ):
    build(BuildingId.barracks)

if unit_type_count(UnitId.villager, compareOp.greater_or_equal, 17) and can_research(TechId.ri_loom):
    research(TechId.ri_loom)

if unit_type_count(UnitId.villager, compareOp.greater_or_equal, 12):
    if( dropsite_min_distance(Resource.live_boar, compareOp.less_than, 30)
    and dropsite_min_distance(Resource.live_boar, compareOp.greater_than, 0)
        ):
        SN.enable_boar_hunting = 2
        SN.minimum_number_hunters = 1
        SN.maximum_food_drop_distance = 15
        SN.maximum_hunt_drop_distance = 30
        disable_self()

    if ( dropsite_min_distance(Resource.live_boar, compareOp.less_than, 9)
    and dropsite_min_distance(Resource.live_boar, compareOp.greater_than, 0)
    and up_compare_sn(SN.minimum_number_hunters, compareOp.not_equal, 5) #does this work? SN.minimum_number_hunters != 5 
        ):    

        if up_remaining_boar_amount(compareOp.less_than, 25):
            SN.minimum_number_hunters = 1
        else: #!make else work
            SN.minimum_number_hunters = 5

if food_amount(compareOp.less_than, 50): #force-drop code
    up_drop_resources(Resource.food, 11)

#force-drop when idling code
if ( unit_type_count(UnitId.villager, compareOp.equal, c_dark_age_pop_cap)
    and g_current_age == c_dark_age
    and food_amount(compareOp.less_than, 500)
    ):
    up_drop_resources(Resource.food, 8)

if g_current_age == c_researching_feudal_age:
    set_gatherer_percentages(35, 40, 15, 10)
    up_set_timer(c_tower_timer, 400) #why is it c: both times? (up-set-timer c: c-tower-timer c: 400)
    enable_timer(c_tower_timer, 400)
    disable_self()

if g_current_age == c_feudal_age:
    set_gatherer_percentages(40, 35, 15, 10)
    disable_self()

if timer_triggered(c_tower_timer):
    set_goal(g_its_tower_time, 1)
    disable_timer(c_tower_timer)
    chat_to_all("It's tower time!")

#it would be nice to be able to conditionaly disable a lower level if statment
if game_time(compareOp.greater_than, 400): #would be great to make it game_time > 400
    up_send_scout(GroupType.group_type_land_explore, ScoutMethod.scout_enemy)
    disable_self()
if game_time(compareOp.greater_than, 460):
    up_send_scout(GroupType.group_type_land_explore, ScoutMethod.scout_enemy)
    disable_self()
if game_time(compareOp.greater_than, 480):
    up_send_scout(GroupType.group_type_land_explore, ScoutMethod.scout_enemy)
    disable_self()
if game_time(compareOp.greater_than, 500):
    up_send_scout(GroupType.group_type_land_explore, ScoutMethod.scout_enemy)
    disable_self()
if game_time(compareOp.greater_than, 550):
    up_send_scout(GroupType.group_type_land_explore, ScoutMethod.scout_enemy)
    disable_self()
if game_time(compareOp.greater_than, 600):
    up_send_scout(GroupType.group_type_land_explore, ScoutMethod.scout_flank)
    disable_self()
if game_time(compareOp.greater_than, 750):
    up_send_scout(GroupType.group_type_land_explore, ScoutMethod.scout_opposite)
    disable_self()
if game_time(compareOp.greater_than, 780):
    up_send_scout(GroupType.group_type_land_explore, ScoutMethod.scout_flank)
    disable_self()
if game_time(compareOp.greater_than, 900):
    up_send_scout(GroupType.group_type_land_explore, ScoutMethod.scout_enemy)
    disable_self()

if g_current_age >= c_feudal_age: #! figure out why >= does not work but == does work in test. but both work as a naked expr
    if can_research(TechId.ri_fletching):
        research(TechId.ri_fletching)

if g_current_age >= c_researching_castle_age:
    if can_build(BuildingId.lumber_camp) and building_type_count_total(BuildingId.lumber_camp, compareOp.less_than, 2):
        build(BuildingId.lumber_camp)

    if can_research(TechId.ri_double_bit_axe):
        research(TechId.ri_double_bit_axe)

if g_current_age >= c_castle_age:
    if True:
        set_gatherer_percentages(25, 40, 25, 10)
        disable_self()

    #Techs
    if unit_type_count_total(ClassId.villager_class, compareOp.greater_than, 40): #does ClassId.villager_class work or shoudl it be UnitId.villager?
        try_research(TechId.ri_wheel_barrow)
    if unit_type_count_total(ClassId.villager_class, compareOp.greater_than, 70):
        try_research(TechId.ri_hand_cart)
    try_research(TechId.ri_horse_collar)
    try_research(TechId.ri_bow_saw)
    try_research(TechId.ri_bodkin_arrow)
    try_research(TechId.ri_ballistics)
    try_research(TechId.ri_fortified_wall)
    try_research(TechId.ri_murder_holes)
    if can_research(TechId.ri_masonry) and building_type_count_total(BuildingId.castle, compareOp.greater_than, 0):
        try_research(TechId.ri_masonry)
    try_research(TechId.my_second_unique_research)
    try_research(TechId.ri_gold_mining)
    try_research(TechId.ri_stone_mining)
    try_research(TechId.ri_town_watch)
    
    #Eco Buildings
    if ( can_build(BuildingId.mining_camp)
        and building_type_count_total(BuildingId.mining_camp, compareOp.less_than, 2)
    ):
        build(BuildingId.mining_camp)

    if ( can_build(BuildingId.town_center)
        and up_resource_amount(ResourceType.amount_wood, compareOp.greater_than, 550) #todo: is amount_wood right? or is it Resource.wood
        and building_type_count_total(BuildingId.town_center, compareOp.less_than, 3)
    ):
        build(BuildingId.town_center)

    if can_build(BuildingId.university) and building_type_count(BuildingId.university, compareOp.equal, 0):
        build(BuildingId.university)

    #Military Buildings
    if ( can_build(BuildingId.barracks)
        and up_resource_amount(ResourceType.amount_wood, compareOp.greater_than, 400) #todo: is amount_wood right? or is it Resource.wood
        and building_type_count_total(BuildingId.town_center, compareOp.less_than, 1)
    ):
        build(BuildingId.barracks)

    if ( can_build(BuildingId.archery_range)
        and up_resource_amount(ResourceType.amount_wood, compareOp.greater_than, 400) #todo: is amount_wood right? or is it Resource.wood
        and building_type_count_total(BuildingId.town_center, compareOp.greater_or_equal, 3)
        and building_type_count_total(BuildingId.archery_range, compareOp.less_than, 8)
    ):
        build(BuildingId.archery_range)

if g_current_age >= c_imperial_age:
    if True:
        set_gatherer_percentages(20, 40, 20, 20)
        disable_self()

    #Techs
    try_research(TechId.ri_bracer)
    try_research(TechId.ri_arrowslits)
    try_research(TechId.ri_bracer)
    try_research(TechId.ri_chemistry)
    try_research(TechId.ri_architecture)
    try_research(TechId.ri_two_man_saw)
    try_research(TechId.ri_heavy_plow)
    try_research(TechId.ri_crop_rotation)
    try_research(TechId.ri_gold_shaft_mining)
    try_research(TechId.ri_stone_shaft_mining)
    try_research(TechId.ri_town_patrol)

if game_time(compareOp.greater_than, 180):
    up_modify_goal(g_one_more_gold_mining_camp_please, 1) #but why goal 1??? (up-modify-goal g-one-more-gold-mining-camp-please g:= 1) 
    disable_self()

if game_time() > 200:
    make_one_more_mining_camp(Resource.stone)
    make_one_more_mining_camp(Resource.gold)
    disable_self()

#techs (idk why they are not part of the age check)
    try_research(TechId.ri_thumb_ring)
    try_research(TechId.ri_crossbow)
    try_research(TechId.ri_arbalest)
    try_research(TechId.ri_arbalest)
    try_research(TechId.ri_elite_skirmisher)

#-------military units-------#
if g_current_age >= c_castle_age:
    if ( can_train(LineId.archer_line)
        and unit_type_count_total(LineId.archer_line, compareOp.less_than, 30)
        and up_resource_amount(ResourceType.amount_gold, compareOp.greater_than, 800)
    ):
        train(LineId.archer_line)

    if ( can_train(LineId.skirmisher_line)
        and unit_type_count_total(LineId.skirmisher_line, compareOp.less_than, 30)
        and up_resource_amount(ResourceType.amount_wood, compareOp.greater_than, 1000)
        and up_resource_amount(ResourceType.amount_food, compareOp.greater_than, 1000)
    ):
        train(LineId.skirmisher_line)

if ( can_train(UnitId.trebuchet)
    and research_completed(TechId.my_second_unique_research)
    and unit_type_count_total(UnitId.trebuchet) < 4
    and unit_type_count_total(LineId.my_unique_unit_line) >= 15
    and unit_type_count_total(LineId.my_unique_unit_line) < 40
    ):
    train(UnitId.trebuchet)

if can_train(LineId.my_unique_unit_line):
    if (not can_train(UnitId.trebuchet)
    and (research_completed(TechId.my_second_unique_research) or unit_type_count_total(LineId.my_unique_unit_line) <= 4)
    and unit_type_count_total(LineId.my_unique_unit_line) < 20
    ):
        train(LineId.my_unique_unit_line)

    if can_train(LineId.my_unique_unit_line) and unit_type_count_total(UnitId.trebuchet) >= 4:
        train(LineId.my_unique_unit_line)

#-----farms-----#
if can_build(BuildingId.farm) and idle_farm_count() == 0:    
    if g_current_age >= c_feudal_age and unit_type_count(UnitId.villager) >= 18:
        if building_type_count_total(BuildingId.farm) < 12:
            build(BuildingId.farm)

        if ( building_type_count_total(BuildingId.farm) < 15
            and building_type_count_total(BuildingId.blacksmith) >= 1
            and building_type_count_total(BuildingId.market) >= 1
        ):
            build(BuildingId.farm)

    if ( g_current_age >= c_castle_age
        and unit_type_count(UnitId.villager) >= 40
        and building_type_count_total(BuildingId.farm) < 18
    ):
        build(BuildingId.farm)
    
    if ( g_current_age >= c_imperial_age
        and unit_type_count(UnitId.villager) >= 40
        and building_type_count_total(BuildingId.farm) < 30
        and up_resource_amount(ResourceType.amount_wood) > 4000
    ):
        build(BuildingId.farm)

if building_type_count_total(BuildingId.farm) > 8:
    if can_build(BuildingId.blacksmith) and building_type_count_total(BuildingId.blacksmith) == 0:
        build(BuildingId.blacksmith)

    if can_build(BuildingId.market) and building_type_count_total(BuildingId.market) == 0:
        build(BuildingId.market)

if military_population() > 4:
    if True:
        attack_now()
        disable_self()

    if game_time() > 600:
        if up_timer_status(t_attack_timer) != timer_running:
            attack_now()
            chat_to_all("Attack!")
            enable_timer(t_attack_timer, 60)
            disable_self()

if (can_research(TechId.my_unique_unit_upgrade) and unit_type_count_total(LineId.my_unique_unit_line) >= 8):
    research(TechId.my_unique_unit_upgrade)

#market rules
if can_sell_commodity(Commodity.wood) and wood_amount() > 2500:
    sell_commodity(Commodity.wood)
if can_sell_commodity(Commodity.food) and wood_amount() > 1100:
    sell_commodity(Commodity.food)


