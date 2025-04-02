from scraper.aoe2scriptFunctions import *
from scraper.aoe2scriptEnums import *
from scraper.aoe2scriptEnums import PlayerNumber
from scraper.aoe2scriptFunctions import chat_to_all, up_chat_data_to_all, disable_self

##asignment
#asi = 12
asi = asi+18
#if True:
#    up_chat_data_to_all("asi should be 30:%d", asi)
#    disable_self()
#
###if
#if True:
#    chat_to_all("in if")
#    disable_self()
#
#if True:
#    if True:
#        chat_to_all("in nested if")
#        disable_self()
#
##for
#if True:
#    for i in range(4):
#        chat_to_all("in for (4 times)")
#    disable_self()
#        
##while
##while_conditional = True #doesnt work because its a boolean currently
#while_conditional = 1
#if True:
#    #while while_conditional: #doest work becuase test canot be a variable
#    while while_conditional == 1:
#        chat_to_all("in while")
#        while_conditional = 0
#    disable_self()
#
##function # functions dont work because they need the retern block and commands
def foo(y):
    chat_to_all("in function")
    y = y + 3

foo(asi)

#!foo.y-44 and foo-0-43 need to pair up!
#for loop incomenter needs to default to 1, not 0