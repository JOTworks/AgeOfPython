conditionals_success = [
    'if x != 0: do_nothing()',
    'if True: do_nothing()',
    'if true(): do_nothing()',
    'if can_build(BuildingId.castle): do_nothing()',
    'if can_build(BuildingId.castle) and can_build(BuildingId.castle): do_nothing()',
]

conditionals_fail = [
    'if x: do_nothing()',
]

random_code_that_should_still_work = [
"""
if (can_build(BuildingId.archery_range) 
    and can_afford_building(BuildingId.castle) 
    and villager_count < 12
    ):
    disable_self()
""",
"""
iddle_villager_count = 6
iddle_villager_count = up_get_fact(FactId.idle_farm_count)
if True:
    up_assign_builders(BuildingId.barracks, iddle_villager_count)
if up_assign_builders(BuildingId.barracks, iddle_villager_count):
    pass
""",
]




