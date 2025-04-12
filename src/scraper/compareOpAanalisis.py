from aoe2scriptFunctions import *

up_compare_sn(GoalId: int,compareOp: compareOp,Value: int,)
strategic_number(SnId: int,compareOp: compareOp,Value: int,)
up_compare_const(Defconst: int,compareOp: compareOp,Value: int,)
up_compare_text(Defconst: int,compareOp: compareOp,Value: int,)
up_compare_goal(GoalId: int,compareOp: compareOp,Value: int,)


# attack_soldier_count() > 12
attack_soldier_count(compareOp: compareOp,Value: int,)
attack_warboat_count(compareOp: compareOp,Value: int,)
building_count(compareOp: compareOp,Value: int,)
building_count_total(compareOp: compareOp,Value: int,)
civilian_population(compareOp: compareOp,Value: int,)
current_age_time(compareOp: compareOp,Value: int,)
current_score(compareOp: compareOp,Value: int,)
defend_soldier_count(compareOp: compareOp,Value: int,)
defend_warboat_count(compareOp: compareOp,Value: int,)
food_amount(compareOp: compareOp,Value: int,)
game_time(compareOp: compareOp,Value: int,)
gold_amount(compareOp: compareOp,Value: int,)
housing_headroom(compareOp: compareOp,Value: int,)
idle_farm_count(compareOp: compareOp,Value: int,)
military_population(compareOp: compareOp,Value: int,)
population(compareOp: compareOp,Value: int,)
population_cap(compareOp: compareOp,Value: int,)
population_headroom(compareOp: compareOp,Value: int,)
random_number(compareOp: compareOp,Value: int,)
soldier_count(compareOp: compareOp,Value: int,)
stone_amount(compareOp: compareOp,Value: int,)
unit_count(compareOp: compareOp,Value: int,)
unit_count_total(compareOp: compareOp,Value: int,)
warboat_count(compareOp: compareOp,Value: int,)
wood_amount(compareOp: compareOp,Value: int,)
up_remaining_boar_amount(compareOp: compareOp,Value: int,)
up_defender_count(compareOp: compareOp,Value: int,)
up_enemy_buildings_in_town(compareOp: compareOp,Value: int,)
up_enemy_units_in_town(compareOp: compareOp,Value: int,)
up_enemy_villagers_in_town(compareOp: compareOp,Value: int,)
#these need type checking
current_age(compareOp: compareOp,Age: Age,)
difficulty(compareOp: compareOp,Difficulty: Difficulty,)
game_type(compareOp: compareOp,GameType: GameType,)
starting_age(compareOp: compareOp,Age: Age,)
starting_resources(compareOp: compareOp,StartingResources: StartingResources,)
up_attacker_class(compareOp: compareOp,ClassId: ClassId,)
fe_sub_game_type(compareOp: compareOp,SubGameType: SubGameType,)


# unit_type_count(UnitId.Archer) > 12
# up_allied_resource_amount(Player.1, Resource.wood) > 12
building_type_count(BuildingId: BuildingId,compareOp: compareOp,Value: int,)
building_type_count_total(BuildingId: BuildingId,compareOp: compareOp,Value: int,)
cc_players_building_count(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,)
cc_players_building_type_count(PlayerNumber: PlayerNumber,BuildingId: BuildingId,compareOp: compareOp,Value: int,)
cc_players_unit_count(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,)
cc_players_unit_type_count(PlayerNumber: PlayerNumber,UnitId: UnitId,compareOp: compareOp,Value: int,)
players_civilian_population(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,)
players_current_age(PlayerNumber: PlayerNumber,compareOp: compareOp,Age: Age,)
players_military_population(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,)
players_population(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,)
players_score(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,)
players_tribute(PlayerNumber: PlayerNumber,Resource: Resource,compareOp: compareOp,Value: int,)
players_tribute_memory(PlayerNumber: PlayerNumber,Resource: Resource,compareOp: compareOp,Value: int,)
players_unit_count(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,)
players_unit_type_count(PlayerNumber: PlayerNumber,UnitId: UnitId,compareOp: compareOp,Value: int,)
up_allied_goal(PlayerNumber: PlayerNumber,GoalId: int,compareOp: compareOp,Value: int,)
up_allied_resource_amount(PlayerNumber: PlayerNumber,ResourceType: ResourceType,compareOp: compareOp,Value: int,)
up_allied_resource_percent(PlayerNumber: PlayerNumber,ResourceType: ResourceType,compareOp: compareOp,Value: int,)
up_allied_sn(PlayerNumber: PlayerNumber,SnId: int,compareOp: compareOp,Value: int,)
unit_type_count(UnitId: UnitId,compareOp: compareOp,Value: int,)
unit_type_count_total(UnitId: UnitId,compareOp: compareOp,Value: int,)
up_building_type_in_town(BuildingId: BuildingId,compareOp: compareOp,Value: int,)
up_gaia_type_count(Resource: Resource,compareOp: compareOp,Value: int,)
up_gaia_type_count_total(Resource: Resource,compareOp: compareOp,Value: int,)
up_unit_type_in_town(UnitId: UnitId,compareOp: compareOp,Value: int,)
up_villager_type_in_town(UnitId: UnitId,compareOp: compareOp,Value: int,)
commodity_buying_price(Commodity: Commodity,compareOp: compareOp,Value: int,)
commodity_selling_price(Commodity: Commodity,compareOp: compareOp,Value: int,)
dropsite_min_distance(Resource: Resource,compareOp: compareOp,Value: int,)
escrow_amount(Resource: Resource,compareOp: compareOp,Value: int,)
up_resource_amount(ResourceType: ResourceType,compareOp: compareOp,Value: int,)
up_resource_percent(ResourceType: ResourceType,compareOp: compareOp,Value: int,)
gate_count(Perimeter: int,compareOp: compareOp,Value: int,)
wall_completed_percentage(Perimeter: int,compareOp: compareOp,Value: int,)
wall_invisible_percentage(Perimeter: int,compareOp: compareOp,Value: int,)


up_compare_flag(GoalId: int,compareOp: compareOp,Flag: int,)

up_group_size(GroupId: int,compareOp: compareOp,Value: int,)
up_idle_unit_count(IdleType: IdleType,compareOp: compareOp,Value: int,)
up_object_data(ObjectData: ObjectData,compareOp: compareOp,Value: int,)
up_object_target_data(ObjectData: ObjectData,compareOp: compareOp,Value: int,)
up_object_type_count(ObjectId: int,compareOp: compareOp,Value: int,)
up_object_type_count_total(ObjectId: int,compareOp: compareOp,Value: int,)
up_path_distance(Point: int,Option: int,compareOp: compareOp,Value: int,)
up_pending_objects(ObjectId: int,compareOp: compareOp,Value: int,)
up_player_distance(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,)
up_players_in_game(PlayerStance: PlayerStance,compareOp: compareOp,Value: int,)
up_point_distance(Point1:Point,Point2:Point,compareOp: compareOp,Value: int,)
up_point_elevation(Point: int,compareOp: compareOp,Value: int,)
up_point_explored(Point: int,compareOp: compareOp,ExploredState: ExploredState,)
up_point_terrain(Point: int,compareOp: compareOp,Terrain: Terrain,)
up_point_zone(Point: int,compareOp: compareOp,Value: int,)
up_projectile_detected(ProjectileType: ProjectileType,compareOp: compareOp,Value: int,)
up_projectile_target(ProjectileType: ProjectileType,compareOp: compareOp,ClassId: ClassId,)
up_remove_objects(SearchSource: SearchSource,ObjectData: ObjectData,compareOp: compareOp,Value: int,)
up_research_status(TechId: int,compareOp: compareOp,ResearchState: ResearchState,)

up_timer_status(TimerId: int,compareOp: compareOp,TimerState: TimerState,)

#ONLY ONE TO NOT HAVE IT AT THE END!
fe_break_point(Value: int,compareOp: compareOp,Value1: int,OptionGoalId: int,)

