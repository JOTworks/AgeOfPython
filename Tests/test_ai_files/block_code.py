from scraper import *
from tests.test_ai_files.code_snipits_test import *

x = 4+2/1
y = x/2+1
"""

INPUT
y = 12 + 2 / 3 - 40

ASSEMBLY
t1 = 2 / 3
t2 = 12 + t1
y = t2 - 40

AOE2SCRIPT
y = 12
ti = 2
ti /= 3
y += t1
y -= 40

temp_id and 



"""