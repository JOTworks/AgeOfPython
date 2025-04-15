from scraper import *
'''
#-------Dark Age----------#

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

#------Feudal Age--------#

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

#--------Castle Age-------#

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
STARTING_VILL_COUNT = Constant(3)
CLOCKWIZE = Constant(0)
COUNTER_CLOCKWIZE = Constant(1)

def explore_terrain(terrain:Terrain, tiles_away, starting_point) -> (Integer, Integer):
  terrain_type_at_point = Integer()
  terrain_id_at_point = Integer()
  up_get_point_terrain(starting_point, terrain_type_at_point, terrain_id_at_point)

def explore_object(explorer_id, thing:ObjectId, tiles_away, starting_point, explore_duration = 50, explore_direction = CLOCKWIZE) -> (Integer, Integer):
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

def get_closest_unit_id(unit_type:UnitId, point:Point) -> Integer:
  temp_int = Integer()
  temp_state = State()
  up_full_reset_search()
  up_filter_status(ObjectStatus.status_ready, ObjectList.list_active)
  up_find_local(unit_type,1)
  up_get_search_state(temp_state)
  up_set_target_object(SearchSource.search_local, 0)
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

def up_get_object_point(point:Point) -> Point:
  up_get_object_data(ObjectData.object_data_point_x, point.x)
  up_get_object_data(ObjectData.object_data_point_y, point.y)
  return point



#_______find TC Location________#
#--walk twords middle of map for 5 seconds--#
if True:
  #select all villigers
  #walk twords middle of map
  disable_self()

#2. if find gold localy, walk around gold
if resource_found(Resource.gold):

  up_full_reset_search()
  up_find_local(ClassId.villager_class, 3)
  for i in range(STARTING_VILL_COUNT):
      up_set_target_object(SearchSource.search_local, i)
      villager_point = up_get_object_point(villager_point)
      closest_gold = get_closest_resource_point(Resource.gold, villager_point)
      if up_point_distance(villager_point, closest_gold) <= VILLAGER_LOS:
        villager_id = -1
        up_get_object_target_data(ObjectData.object_data_id, villager_id)
        explore_object(villager_id, Resource.gold, VILLAGER_LOS)

    
  


search_state = State()
  up_full_reset_search()
  up_filter_status(ObjectStatus.status_resource, ObjectList.list_active)
  up_find_resource(r, 20)
  up_get_search_state(search_state)
  total = 0
  temp = 0
  for i in range(search_state.RemoteIndex):
    up_set_target_object(SearchSource.search_remote, i)
    up_get_object_data(ObjectData.object_data_carry, temp)
    total += temp
  up_chat_data_to_all("Total:%d", total)
#3. After 5 seconds place TC next to wood line when found
#   (Gold+Hunt -> Gold -> Berry -> hunt -> stone)
#4. build barracks with one of the villagers build house with other villager
#5. send all villegers to TC to build and then collect food
