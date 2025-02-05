from scraper.aoe2scriptFunctions import *
from scraper.aoe2scriptEnums import *
#if x + True and True:
#    pass
#
#if x > (False or True):
#    pass
#
#if (True and True) > (False or False):
#    pass
"""
test: (t1=False)(True)(True)
result: t1 = True

test: (t2=False)(Or(False)(False))
result: t2 = True

test: (compare t1 > t2)
result:

"""

if (can_build(BuildingId.archery_range) 
    and can_afford_building(BuildingId.castle) 
    and villager_count < 12
    ):
    disable_self()
"""
Same as if (x<y) and (y<z) and (z<(True and True))

boolOp()

bool(x<y
    bool(y<z
        z<(True and True)
    )
)

"""


