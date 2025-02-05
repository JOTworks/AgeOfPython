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








