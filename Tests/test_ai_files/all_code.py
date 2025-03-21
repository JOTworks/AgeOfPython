from scraper.aoe2scriptFunctions import *
from scraper.aoe2scriptEnums import *
from scraper.aoe2scriptEnums import PlayerNumber
from scraper.aoe2scriptFunctions import chat_to_all, up_chat_data_to_player, disable_self

#asignment
asi = 12
asi = asi+18
up_chat_data_to_player(PlayerNumber.my_player_number, "asi should be 30:%d", asi)

#if
if True:
    chat_to_all("in if")
    disable_self()

if True:
    if True:
        chat_to_all("in nested if")
        disable_self()

#for
if True:
    for i in range(4):
        chat_to_all("in for (4 times)")
    disable_self()
        
#while
#while_conditional = True #doesnt work because its a boolean currently
while_conditional = 1
if True:
    #while while_conditional: #doest work becuase test canot be a variable
    while while_conditional == 1:
        chat_to_all("in while")
        while_conditional = 0
    disable_self()

#function
def foo():
    chat_to_all("in function")

if True:
    foo()
    disable_self()
