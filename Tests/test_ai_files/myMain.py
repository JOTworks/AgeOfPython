from AgeOfPython.src.scraper.aoe2scriptFunctions import *
from AgeOfPython.src.scraper.aoe2scriptEnums import *
from imported import *
#from test_strings import string_while_loop as swl, string_variable_asign as sva
#import test_functioen as tf

x = 12
x = 11
x = 15+x
if True:
    delete_unit(UnitId.archer)

x = Const(14)
x = Point(14)

if (can_research(TechId.ri_loom) 
    and building_type_count_total(BuildingId.house,'>',1) 
    and (food_amount('<',50) or (housing_headroom('<',1) and not can_build(BuildingId.house)))
   ):
  research(TechId.ri_loom)
  disable_self()
