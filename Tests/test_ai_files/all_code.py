#all_code
#todo: while while_conditional: #doest work becuase test canot be a variable
#todo: while_conditional = True #doesnt work because its a boolean currently
from scraper.aoe2scriptFunctions import *
from scraper.aoe2scriptFunctions import (
    can_build,
    idle_farm_count,
    building_type_count_total,
    unit_type_count,
    build,
    
)
from scraper.aoe2scriptEnums import *
from scraper.aoe2scriptEnums import (
    compareOp,
    BuildingId,
    UnitId,
)
g_current_age = 0
c_feudal_age = 0
c_castle_age = 0



if can_build(BuildingId.farm) and idle_farm_count() == 0:    
    if g_current_age >= c_feudal_age and unit_type_count(UnitId.villager) >= 18:
        if building_type_count_total(BuildingId.farm) < 12:
            build(BuildingId.farm)

        if ( building_type_count_total(BuildingId.farm) < 15
            and building_type_count_total(BuildingId.blacksmith) 
            and building_type_count_total(BuildingId.market)
        ):
            build(BuildingId.farm)

    if ( g_current_age >= c_castle_age
        and unit_type_count(UnitId.villager) >= 40
        and building_type_count_total(BuildingId.farm) < 18
    ):
        build(BuildingId.farm)


#DefRule(
#    test=aoeOp(
#        op=And(),
#        values=[
#            Command(
#                func=Name(id=<AOE2FUNC.up_compare_goal: 203>, ctx=Load()),
#                args=[
#                    Variable(id='g_current_age', ctx=Load()),
#                    <compareOp.greater_or_equal: (21, '>=')>,
#                    Variable(id='c_feudal_age', ctx=Load())]),
#            Command(
#                func=Name(id=<AOE2FUNC.unit_type_count: 170>, ctx=Load()),
#                args=[
#                    <UnitId.villager: 83>,
#                    <compareOp.greater_or_equal: (21, '>=')>,
#                    Constant(value=18)])]),
#    body=[
#        Command(
#            func=Name(id=<AOE2FUNC.up_jump_direct: 277>, ctx=Load()),
#            args=[
#                <typeOp.constant: (6, 'c:')>,
#                Constant(value=8)])]),

#DefRule(
#    test=aoeOp(
#        op=And(),
#        values=[
#            Command(
#                func=Name(id=<AOE2FUNC.building_type_count_total: 13>, ctx=Load()),
#                args=[
#                    <BuildingId.farm: 50>,
#                    <compareOp.less_than: (18, '<')>,
#                    Constant(value=18)]),
#            aoeOp(
#                op=And(),
#                values=[
#                    Command(
#                        func=Name(id=<AOE2FUNC.unit_type_count: 170>, ctx=Load()),
#                        args=[
#                            <UnitId.villager: 83>,
#                            <compareOp.greater_or_equal: (21, '>=')>,
#                            Constant(value=40)]),
#                    Compare(
#                        left=Variable(id='g_current_age', ctx=Load()),
#                        ops=[
#                            GtE()],
#                        comparators=[
#                            Variable(id='c_castle_age', ctx=Load())])])]),
#    body=[
#        Command(
#            func=Name(id=<AOE2FUNC.up_jump_direct: 277>, ctx=Load()),
#            args=[
#                <typeOp.constant: (6, 'c:')>,
#                Constant(value=16)])]),