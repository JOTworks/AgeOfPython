from aoe2scriptEnums import *

class Point():
    def __init__(self, x, y):
        pass
class State():
    def __init__(self, one, two, three, four):
        pass
class Const():
    def __init__(self, num):
        pass

#todo: find out what uses this in the end and if we can move it there
class_constructers = {Point:2, State:4, int:1, list:8}

def acknowledge_event(EventType: EventType,EventId: int,):
    """
 Acknowledges a received event by resetting the associated flag. Scenario triggers that execute an AI Script Goal effect are the only events that AI scripts can detect. This command, along withevent-detected, is used to detect an AI Script Goal effect from a scenario trigger, often with the intention of changing the AI behavior after the scenario trigger has fired. The scenario designer chooses an AI Trigger number for the AI Script Goal effect in the scenario editor. Then, the event-detected command in the AI script will detect when this trigger effect happens. The event-detected command will remain true after the AI Script Goal trigger effect fires, so acknowledge-event is used to reset the event-detected flag so that event-detected will no longer be true, similar to how thedisable-timercommand clears a timer that has triggered or how theacknowledge-tauntcommand accepts the taunt message. 
:param EventType: Range: 0.
 The type of the event. Triggers are the only valid event types. 
:param EventId: Range: 0 to 255.
 The event ID. The only valid events are AI Script Goal effects and AI Signal conditions in scenario triggers. The ID matches the number of the chosen option from the trigger condition/effect. Note: the "AI Trigger 256" option in the AI Script Goal effect cannot be detected by AIs. 
"""
    pass
def acknowledge_taunt(PlayerNumber: PlayerNumber,TauntId: int,):
    """
 Acknowledges the taunt (resets the flag). Like other event systems in the AI, taunt detection requests explicit acknowledgement. In simple terms, whenever an AI receives a taunt message,taunt-detectedwill remain true for the given taunt until the taunt is acknowledged. If the taunt is not acknowledged, your AI's response to the taunt will happen repeatedly. The action allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows the use of rule variables forPlayerNumber, such as "this-any-ally" or "this-any-enemy". It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param TauntId: Range: 1 to 255.
 A valid taunt ID. Only taunts 1-42 will send an audio version of the taunt, but all taunts within the range below can be sent and detected by AIs. 
"""
    pass
def attack_now():
    """
 Forces attack with currently available attack units. Units are designated as attack units by usingsn-percent-attack-soldiersorsn-percent-attack-boats. Once the attack-now command is issued, all attack units will group up into formations, pick a building or unit to target, and march toward that location to attack, mostly ignoring enemy units and buildings along the way. Once the soldiers reach the target, they will attack the target and nearby units. Once the target is destroyed, a new target will be selected. This process will continue until all attack units from the attack-now command are killed. To stop an attack-now attack, useup-reset-attack-now. Three important notes:  
"""
    pass
def attack_soldier_count(compareOp: compareOp,Value: int,):
    """
 Compares the computer player's attack soldier count toValueusingcompareOpand returns true if the condition is met. Attack soldiers are those attacking with the attack groups method (settingsn-number-attack-groups> 0) or are attacking with theattack-nowcommand. Setting sn-number-attack-groups to 0 and usingup-disband-group-typeto disband land attack groups when attacking with attack groups will reset the soldiers, and they will no longer be considered attack soldiers. Likewise, usingup-reset-attack-nowwhen attacking with attack-now will reset the soldiers, and they will no longer be considered attack soldiers. Monks are included as land attack soldiers when attacking. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def attack_warboat_count(compareOp: compareOp,Value: int,):
    """
 Compares the computer player's attack warboat count toValueusingcompareOpand returns true if the condition is met. Attack warboats are those assigned to boat attack groups with theattack-nowcommand, not with thesn-number-boat-attack-groupsSN. If you stop callingattack-nowthen they are immediately no longer attack warboats - even without usingup-reset-attack-now. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def build(BuildingId: BuildingId,):
    """
 Builds the given building if the building is available to the player and the building can be constructed without escrowed resources. If you want to construct walls or gates, use the correspondingbuild-wall,build-gate, orup-build-linecommands instead. The Action allows the use of building line wildcard parameters forBuildingId. The only wildcard parameter available is watch-tower-line. However, it is better to use watch-tower instead of watch-tower-line, even after Guard Tower or Keep upgrades due to some bugs with watch-tower-line. Simply using (build watch-tower) will work regardless of tower upgrades. Building classes cannot be used with this command. Important Note:Always use acan-buildorup-can-buildcondition in every rule where you use the build command. Without this condition, the building queue for this building may get stuck for the rest of the game. When this command is issued, the AI engine will add the specified building to the building placement queue. Ifsn-enable-new-building-systemis set to 0, the engine will only add the building to the placement queue if there isn't already a building of the same type being constructed or waiting to be placed, but if the SN is set to 1 this check is removed, and an unlimited number of buildings of the same type are allowed to be queued for placement or be constructed at once. You can limit the number of buildings added to the placement queue with aup-pending-objectscondition. At the end of each script pass, the AI engine checks if the AI has explored the minimum percentage of the map required bysn-initial-exploration-required. If so, it will attempt to place each building that is currently in the placement queue. If the building was added to the queue with the (build) command, the AI will place most buildings at a random location withinsn-maximum-town-sizetiles from the main town center using whatever value sn-maximum-town-size is set to at the end of the script.sn-minimum-town-sizehas no effect on building placement except for towers. However, four tiles around the TC are reserved around every town center for farms, and all buildings are placed at least one tile apart. For a complete list on the min and max distances where each building can be built, see this list here:link. Buildings placed with this command will avoid the following locations: There are many other commands that you can use instead of this command that you more precise control over building placement, such asbuild-forward,up-build, andup-build-line. Several buildings have variations on how they are placed that are different from the description above: Town Centersare placed like most buildings whensn-town-center-placementis set to the default value of 0. However, if sn-town-center-placement is set to theBuildingIdof another building, such as "mill" or "lumber-camp", the town center will follow the placement rules of that building instead. MillsandFolwarksare not placed in a random location within sn-maximum-town-size, but instead are built by a food resource withinsn-mill-max-distance. The AI engine by default prefers to build mills and folwarks by forage, then by shore fish, then by deer. However, this preference can be changed withsn-preferred-mill-placement. Also, mills and folwarks are placed one tile away from food resource piles unlesssn-allow-adjacent-dropsitesis set to 1 by the end of the script pass, and they are placed a minimum number of tiles from all dropsites (not just mills and folwarks), as specified bysn-dropsite-separation-distance. Mining Campsare not placed in a random location within sn-maximum-town-size, but instead are built by a gold or stone resource withinsn-mining-camp-max-distance(orsn-camp-max-distanceif sn-mining-camp-max-distance is set to 0), and they are placed at least 7 tiles from the main town center. If the closest gold mine distance to a dropoff point is greater thansn-gold-dropsite-distance, then it will prefer to place the mining camp near gold mines. Then it checks if the closest stone mine distance to a dropoff point is greater thansn-stone-dropsite-distance, and if it is, it will prefer to place the mining camp near stone. If neither condition is met, it prefers neither gold nor stone, and the mining camp placement behavior is undefined. It's possible the mining camp isn't placed, but this is untested. Also, mining camps are placed one tile away from gold and stone resource piles unlesssn-allow-adjacent-dropsitesis set to 1 by the end of the script pass, and they are placed a minimum number of tiles from all dropsites (not just mining camps), as specified bysn-dropsite-separation-distance. Lumber Campsare not placed in a random location within sn-maximum-town-size, but instead are built by a tree withinsn-lumber-camp-max-distance(orsn-camp-max-distanceif sn-lumber-camp-max-distance is set to 0), and they are placed at least 7 tiles from the main town center. Also, lumber camps are placed one tile away from trees unlesssn-allow-adjacent-dropsitesis set to 1 by the end of the script pass, though even with the SN set to 1 the AI will sometimes fail to build the lumber camp adjacent to trees, and they are placed a minimum number of tiles from all dropsites (not just lumber camps), as specified bysn-dropsite-separation-distance. Usually the AI favors building lumber camps near forests rather than straggler trees, but the AI will build lumber camps near straggler trees if sn-lumber-camp-max-distance is to small for the AI to find an available forest to build the lumber camp by. Docksare of course only placed on water, and there are several SNs that can affect their placement, such assn-dock-avoidance-factor,sn-dock-placement-mode,sn-dock-proximity-factor, andsn-minimum-water-body-size-for-dock. Farmsare automatically placed near town centers, mills, and folwarks. The AI engine prefers to place farms around TCs instead of mills or folwarks, but it will place farms around mills or folwarks if all spaces immediately next to the town center are already filled with farms.  Fish Trapsshould not be placed with the build command. Instead, they should only be placed with up-build-line. It's possible they can be placed with the build command, but they often won't be placed in the right location. Also, make sure to use (up-assign-builders c: fish-trap c: -1) to make sure that villagers aren't sent to contruct them. Outposts, at least according to thisinfo, are placed outside the town, at a distance between sn-maximum-town-size and twice the distance of sn-maximum-town-size. They might also have a preference to be placed on hills like towers do (see the towers section below). If you choose to build outposts, make sure you test to make sure you like their placement location. You can build them in more precise locations or inside the town if you use the place-control or place-point options with up-build, or you can also place them with up-build-line. Towersare the only type of building that uses sn-minimum-town-size as the minimum distance they can be placed from the starting town center. By default they have a preference to be placed on hills, but you can remove this preference by settingsn-ignore-tower-elevationto 1. This preference for hills is not used for castles or kreposts.  Donjons. Everything from towers applies to donjons. To construct donjons with serjeants, setsn-allow-serjeant-buildingto 1. Gatescannot be placed with the build command. Construct them with thebuild-gateor up-build-line command. To build palisade gates, setsn-gate-type-for-wallto 1 before using the build-gate command. Trebuchets. Yes, (build trebuchet) actually works. Every scripter should try it once in their life. However, soon you'll see why it's considered cheating. 
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
"""
    pass
def build_forward(BuildingId: BuildingId,):
    """
 Builds the given building close to an enemy if the building is available to the player and the building can be constructed without escrowed resources. The Action allows the use of building line wildcard parameters forBuildingId. The only wildcard parameter available is watch-tower-line. However, it is better to use watch-tower instead of watch-tower-line, even after Guard Tower or Keep upgrades due to some bugs with watch-tower-line. Simply using (build watch-tower) will work regardless of tower upgrades. Building classes cannot be used with this command. Important Note:Always use acan-buildorup-can-buildcondition in every rule where you use the build-forward command. Without this condition, the building queue for this building may get stuck for the rest of the game. When this command is issued, the AI engine will add the specified building to the building placement queue. Ifsn-enable-new-building-systemis set to 0, the engine will only add the building to the placement queue if there isn't already a building of the same type being constructed or waiting to be placed, but if the SN is set to 1 this check is removed, and an unlimited number of buildings of the same type are allowed to be queued for placement or be constructed at once. At the end of each script pass, the AI engine checks if the AI has explored the minimum percentage of the map required bysn-initial-exploration-required. If so, it will attempt to place each building that is currently in the placement queue. If the building was added to the queue with the build-forward command, the AI will place the building near the enemy player specified bysn-target-player-numberor the player specified bysn-attack-winning-playerif sn-target-player-number is set to 0. build-forward will avoid placing the building on tiles where an enemy building already exists, and it will also avoid placing a building within any enemy building's line of sight, + 2 tiles. Buildings placed with build-forward will avoid placing the building on tiles where an enemy building already exists, and it will also avoid placing a building within any enemy building's line of sight, + 2 tiles. 
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
"""
    pass
def build_gate(Perimeter: int,):
    """
 Builds a gate as part of the given perimeter wall if the gate is available to the player and the gate can be constructed without escrowed resources. The given perimeter must first be enabled withenable-wall-placement. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. If wall placement is enabled at a particular perimeter with enable-wall-placement, the AI engine will attempt to plan a roughly circular wall pattern within the given perimeter distances when thebuild-wallcommand is issued. Once the AI finds an appropriate location to build a gate within the given perimeter and the build-gate command is issued, the AI will replace four wall segments with a gate foundation. This command cannot be used to build a gate within wall segments that existed at the start of the game, such as the starting walls in Arena or Fortress. In the DE version you can build palisade gates by settingsn-gate-type-for-wallto 1 before using this command. 
:param Perimeter: Range: 1 or 2.
 The distance to build a wall around the town. Allowed values are 1 and 2, with 1 being closer to the Town Center than 2. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. 
"""
    pass
def build_wall(Perimeter: int,WallId: WallId,):
    """
 Builds a wall line of the given wall type at the given perimeter if the wall type is available to the player and the wall can be constructed without escrowed resources. The given perimeter must first be enabled withenable-wall-placement. The Action allows the use of wall line wildcard parameters forWallId. The only wall line wildcard parameter is stone-wall-line. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. If wall placement is enabled at a particular perimeter with enable-wall-placement, the AI engine will attempt to plan a roughly circular wall pattern within the given perimeter distances and construct the wall according to this pattern. This command cannot be used to rebuild parts of wall segments that existed at the start of the game, such as the starting walls in Arena or Fortress. 
:param Perimeter: Range: 1 or 2.
 The distance to build a wall around the town. Allowed values are 1 and 2, with 1 being closer to the Town Center than 2. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. 
:param WallId: Range: A Wall type.
 TheBuildingIdof a wall type. 
"""
    pass
def building_available(BuildingId: BuildingId,):
    """
 Checks that the building is available to the computer player's civ and that the tech tree prerequisites are met. It does not check that there are enough resources to build the building. It allows the use of building line wildcard parameters forBuildingId. The only wildcard parameter available is watch-tower-line. However, it is better to use watch-tower instead of watch-tower-line, even after Guard Tower or Keep upgrades due to some bugs with watch-tower-line. Simply using (building-available watch-tower) will work regardless of tower upgrades. You cannot use building classes with this command. When the AI checks the tech tree prerequisites, this includes checking whether the prerequisite age has been researched. There isn't a way at the beginning of the game to check if the building will be available for the civilization in future ages. 
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
"""
    pass
def building_count(compareOp: compareOp,Value: int,):
    """
 Checks the computer player's building count. Only existing buildings are included, not buildings under construction. Buildings that existed from the start of the game, such as the starting town center, are not included. Also, farms are included, but walls and gates are not included. To check for the building-count of other players, including buildings under construction, useplayers-building-count. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def building_count_total(compareOp: compareOp,Value: int,):
    """
 Checks the computer player's total building count, either existing buildings or buildings under construction. Buildings that existed from the start of the game, such as the starting town center, are not included. Also, farms are included, but walls and gates are not included. To check for the building-count of other players, including buildings under construction, useplayers-building-count. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def building_type_count(BuildingId: BuildingId,compareOp: compareOp,Value: int,):
    """
 Checks the computer player's building count. Only existing buildings of the given type or class are included, not buildings under construction. To check the number of gates, usegate-countinstead. building-type-count allows the use of building line wildcard parameters forBuildingId. The only wildcard parameter available is watch-tower-line. However, it is better to use watch-tower instead of watch-tower-line, even after Guard Tower or Keep upgrades due to some bugs with watch-tower-line. Simply using (building-type-count watch-tower) will work regardless of tower upgrades. There are four ways you can specify the building "type":  To check for the building-type-count of other players, including buildings under construction, useplayers-building-type-count. 
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def building_type_count_total(BuildingId: BuildingId,compareOp: compareOp,Value: int,):
    """
 Checks the computer player's total building count. The total includes buildings of the given type class, both existing buildings and those under construction. To check the number of gates, usegate-countinstead. building-type-count-total allows the use of building line wildcard parameters forBuildingId. The only wildcard parameter available is watch-tower-line. However, it is better to use watch-tower instead of watch-tower-line, even after Guard Tower or Keep upgrades due to some bugs with watch-tower-line. Simply using (building-type-count-total watch-tower) will work regardless of tower upgrades. There are four ways you can specify the building "type":  To check for the building-type-count of other players, including buildings under construction, useplayers-building-type-count. 
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def buy_commodity(Commodity: Commodity,):
    """
 Buys one lot of the given commodity. The AI will buy 100 of the given commodity (wood, food, or stone) at the current trading price. 
:param Commodity: Range: 0 to 2.
 A resource that can be bought or sold. Gold is not a commodity. 
"""
    pass
def can_afford_building(BuildingId: BuildingId,):
    """
 Checks whether the computer player has enough resources to build the given building. It does not take into account resources in the escrow stockpiles. It does not check that the tech tree prerequisites are met or if the building is allowed for the civ. It allows the use of building line wildcard parameters forBuildingId. The only wildcard parameter available is watch-tower-line. However, it is better to use watch-tower instead of watch-tower-line, even after Guard Tower or Keep upgrades due to some bugs with watch-tower-line. Simply using (can-afford-building watch-tower) will work regardless of tower upgrades. You cannot use building classes with this command. 
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
"""
    pass
def can_afford_complete_wall(Perimeter: int,WallId: WallId,):
    """
 Checks whether the computer player has enough resources to finish the given wall type at thePerimeter. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. If wall placement is enabled at a particular perimeter with enable-wall-placement, the AI engine will attempt to plan a roughly circular wall pattern within the given perimeter distances and construct the wall according to this pattern when thebuild-wallcommand is issued. In particular, can-afford-complete-wall checks: It does not take into account escrowed resources. It does not check if wall area is explored or ifenable-wall-placementhas been used.Perimeteris either: '1' for a 10-20 tile radius aroung home TC or '2' for an 18-30 tile radius. 
:param Perimeter: Range: 1 or 2.
 The distance to build a wall around the town. Allowed values are 1 and 2, with 1 being closer to the Town Center than 2. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. 
:param WallId: Range: A Wall type.
 TheBuildingIdof a wall type. 
"""
    pass
def can_afford_research(TechId: int,):
    """
 Checks whether the computer player has enough resources to perform the given research. Also checks that the research is available for the civ, that its not already researched and that the computer player has reached the required age. Does not check if the required building is built. The fact does not take into account escrowed resources. You can also use my-unique-research, which will usually check the imperial age unique tech for the civilization, and you can also use my-second-unique-research, which will usually check the castle age unique tech for the civilization. The excepts are the Britons, Franks, Goths, and Saracens, whose my-unique-research and my-second-unique-research are switched. 
:param TechId: Range: A valid technology ID.
 The name of a technology or the ID number assigned to that technology. See the Technology table for details [to be added later]. Note that some technologies are given an AI name that is different from the in-game technology name. 
"""
    pass
def can_afford_unit(UnitId: UnitId,):
    """
 Checks whether the computer player has enough resources to train the given unit. Does not check anything else. The fact does not take into account escrowed resources. The fact allows the use of unit line wildcard parameters forUnitId. These wildcard parameters allow you to specify a unit line rather than an individual unit in the unit line. You cannot use unit classes with this command. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
"""
    pass
def can_build(BuildingId: BuildingId,):
    """
 This fact checks whether the computer player can build the given building. You cannot use building classes with this command. This command does not work with walls or gates. However, you can usecan-build-wall,can-build-gate,up-can-build-line, orup-can-buildto check if walls or gates can be built. In particular it checks: It does not check whether villagers exist to build it, or if there is adequate space for the building. The fact allows the use of building line wildcard parameters forBuildingId. The only wildcard parameter available is watch-tower-line. However, it is better to use watch-tower instead of watch-tower-line, even after Guard Tower or Keep upgrades due to some bugs with watch-tower-line. Simply using (can-build watch-tower) will work regardless of tower upgrades. Important Note:Always use a can-build,can-build-with-escrow, orup-can-buildcondition in every rule where you use thebuildorup-buildcommand. Without this condition, the building queue for this building may get stuck for the rest of the game. 
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
"""
    pass
def can_build_with_escrow(BuildingId: BuildingId,):
    """
 This fact checks whether the computer player can build the given building if escrowed resources are included. You cannot use building classes with this command. This command does not work with walls or gates. However, you can usecan-build-wall-with-escrow,can-build-gate-with-escrow,up-can-build-line, orup-can-buildto check if walls or gates can be built. In particular it checks: It does not check whether villagers exist to build it, or if there is adequate space for the building. The fact allows the use of building line wildcard parameters forBuildingId. The only wildcard parameter available is watch-tower-line. However, it is better to use watch-tower instead of watch-tower-line, even after Guard Tower or Keep upgrades due to some bugs with watch-tower-line. Simply using (can-build-with-escrow watch-tower) will work regardless of tower upgrades. Important Note:Always use acan-build,  can-build-with-escrow, orup-can-buildcondition in every rule where you use thebuildorup-buildcommand. Without this condition, the building queue for this building may get stuck for the rest of the game. 
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
"""
    pass
def can_build_gate(Perimeter: int,):
    """
 Checks whether construction of a gate as part of the given perimeter wall can start. In non-DE versions, this command will only check if you can build stone gates. In DE, this command will check if you can build the gate type specified bysn-gate-type-for-wall. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. If wall placement is enabled at a particular perimeter with enable-wall-placement, the AI engine will attempt to plan a roughly circular wall pattern within the given perimeter distances and construct the wall according to this pattern when thebuild-wallcommand is issued. Once the AI finds an appropriate location to build a gate within the given perimeter and thebuild-gatecommand is issued, the AI will replace four wall segments with a gate foundation. can-build-gate checks: It will return false if it cannot fit a gate 3 tiles away from existing gates. In the DE version, to check if the AI can build palisade gates, setsn-gate-type-for-wallto 1 before using this command. 
:param Perimeter: Range: 1 or 2.
 The distance to build a wall around the town. Allowed values are 1 and 2, with 1 being closer to the Town Center than 2. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. 
"""
    pass
def can_build_gate_with_escrow(Perimeter: int,):
    """
 Checks whether construction of a gate as part of the given perimeter wall can start. In non-DE versions, this command will only check if you can build stone gates. In DE, this command will check if you can build the gate type specified bysn-gate-type-for-wall. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. If wall placement is enabled at a particular perimeter with enable-wall-placement, the AI engine will attempt to plan a roughly circular wall pattern within the given perimeter distances and construct the wall according to this pattern when thebuild-wallcommand is issued. Once the AI finds an appropriate location to build a gate within the given perimeter and thebuild-gatecommand is issued, the AI will replace four wall segments with a gate foundation. can-build-gate-with-escrow checks: It will return false if it cannot fit a gate 3 tiles away from existing gates. In the DE version, to check if the AI can build palisade gates, setsn-gate-type-for-wallto 1 before using this command. 
:param Perimeter: Range: 1 or 2.
 The distance to build a wall around the town. Allowed values are 1 and 2, with 1 being closer to the Town Center than 2. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. 
"""
    pass
def can_build_wall(Perimeter: int,WallId: WallId,):
    """
 Checks whether a given wall type can be built at the given perimeter without escrowed resources. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. If wall placement is enabled at a particular perimeter with enable-wall-placement, the AI engine will attempt to plan a roughly circular wall pattern within the given perimeter distances and construct the wall according to this pattern when thebuild-wallcommand is issued. In particular, can-build-wall checks: This fact checks that there is enough stone for at least 5 wall pieces, whereascan-afford-complete-wallchecks if there is enough stone for the entire wall. The fact allows the use of wall line wildcard parameters forWallId. The only available wall line wildcard parameter is stone-wall-line. Note you are allowed to enable wall placement at both perimeters. 
:param Perimeter: Range: 1 or 2.
 The distance to build a wall around the town. Allowed values are 1 and 2, with 1 being closer to the Town Center than 2. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. 
:param WallId: Range: A Wall type.
 TheBuildingIdof a wall type. 
"""
    pass
def can_build_wall_with_escrow(Perimeter: int,WallId: WallId,):
    """
 Checks whether a given wall type can be built at the given perimeter, including with escrowed resources.Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. If wall placement is enabled at a particular perimeter with enable-wall-placement, the AI engine will attempt to plan a roughly circular wall pattern within the given perimeter distances and construct the wall according to this pattern when thebuild-wallcommand is issued. In particular, can-build-wall-with-escrow checks: This fact checks that there is enough stone for at least 5 wall pieces, whereascan-afford-complete-wallchecks if there is enough stone for the entire wall. The Fact allows the use of wall line wildcard parameters forWallId. The only available wall line wildcard parameter is stone-wall-line. Note you are allowed to enable wall placement at both perimeters. 
:param Perimeter: Range: 1 or 2.
 The distance to build a wall around the town. Allowed values are 1 and 2, with 1 being closer to the Town Center than 2. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. 
:param WallId: Range: A Wall type.
 TheBuildingIdof a wall type. 
"""
    pass
def can_buy_commodity(Commodity: Commodity,):
    """
 Checks whether the computer player can buy one lot (100 resources) of the given commodity (food, wood, or stone). The fact does not take into account escrowed resources. In other words, this checks if the AI has a market and enough gold at the current buying price for the specified commodity to be able to buy 100 of the specified commodity. 
:param Commodity: Range: 0 to 2.
 A resource that can be bought or sold. Gold is not a commodity. 
"""
    pass
def can_research(TechId: int,):
    """
 Checks if the given research can start. In particular it checks: Research names, except for ages, my-unique-research, my-second-unique-research, are prefixed with a "ri-" which might stand for "research item". You can also research by the research ID rather than the research name. You can see all technologies and their research IDs in theTechnologies table. You can also use my-unique-research, which will usually (always in DE) check the imperial age unique tech for the civilization, and you can also use my-second-unique-research, which will usually (always in DE) check the castle age unique tech for the civilization. In UP and WK, the exceptions are the Britons (in WK only) and Goths, whose my-unique-research and my-second-unique-research are switched. 
:param TechId: Range: A valid technology ID.
 The name of a technology or the ID number assigned to that technology. See the Technology table for details [to be added later]. Note that some technologies are given an AI name that is different from the in-game technology name. 
"""
    pass
def can_research_with_escrow(TechId: int,):
    """
 Checks if the given research can start. In particular it checks: Research names, except for ages, my-unique-research, my-second-unique-research, are prefixed with a "ri-" which might stand for "research item". You can also research by the research ID rather than the research name. You can see all technologies and their research IDs in theTechnologies table. You can also use my-unique-research, which will usually check the imperial age unique tech for the civilization, and you can also use my-second-unique-research, which will usually check the castle age unique tech for the civilization. The excepts are the Britons, Franks, Goths, and Saracens, whose my-unique-research and my-second-unique-research are switched. 
:param TechId: Range: A valid technology ID.
 The name of a technology or the ID number assigned to that technology. See the Technology table for details [to be added later]. Note that some technologies are given an AI name that is different from the in-game technology name. 
"""
    pass
def can_sell_commodity(Commodity: Commodity,):
    """
 Checks whether the computer player can sell one lot (100 resources) of the given commodity (food, wood, or stone). The fact does not take into account escrowed resources. In other words, this checks if the AI has a market and has at least 100 of the specified commodity that it can sell for gold. 
:param Commodity: Range: 0 to 2.
 A resource that can be bought or sold. Gold is not a commodity. 
"""
    pass
def can_spy():
    """
 Checks if the AI can research Treason without escrowed resources. Only works in Regicide games. The computer player does see the revealed area around the enemy kings as expected. This command does not check if the AI can research Spies like you might expect. 
"""
    pass
def can_spy_with_escrow():
    """
 Checks if the AI can research Treason, including escrowed resources. The computer player does see the revealed area around the enemy kings as expected. This command does not check if the AI can research Spies with escrow like you might expect. 
"""
    pass
def can_train(UnitId: UnitId,):
    """
 Checks that the training of a given unit can start. You cannot use unit classes with this command. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. In particular it checks: The fact allows the use of unit line wildcard parameters forUnitId, which means that you can use (can-train spearman-line), instead of (can-train spearman). Interestingly, you can safely use the base unit of a unit line with this command instead of the unit line version, and it will work regardless of any upgrades that have been researched. For example, you can safely use (can-train archer) even if Crossbowman has been researched. This capability is important if you are scripting for WololoKingdoms (WK) or any other mod where some unit lines aren't defined in the AI engine. Unique units can be trained dynamically by using my-unique-unit or my-unique-unit-line as long as your aren't scripting for a Userpatch modpack like WK. You can also train by the unit ID rather than the unit name. You can see all units and their unit IDs in theObjects table. In WK, there are two units that use a separate placeholder unit ID for training purposes, and you must use it for all can-train,can-train-with-escrow,train,up-can-train, andup-traincommands. These units are the condottiero and genitour. Use ID 184 for condottiero-placeholder and use ID 732 for genitour-placeholder. You cannot check for the ability to train units with unit classes (like infantry-class) or with sets (like huskarl-set, which includes castle huskarls and barracks huskarls). To check for units like huskarls or tarkans that can be trained at multiple buildings, you must each each unit type separately, such as (or (can-train huskarl) (can-train barracks-huskarl)). To check if mercenary kipchaks (elite kipchaks that allies can train after Cuman Mercenaries is researched) can be trained, use "mercenary-kipchak" rather than kipchak-line.  This fact will return false if the setting ofsn-dock-training-filtercurrently restricts the training of ships. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
"""
    pass
def can_train_with_escrow(UnitId: UnitId,):
    """
 Checks that the training of a given unit can start. You cannot use unit classes with this command. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. In particular it checks: The fact allows the use of unit line wildcard parameters forUnitId, which means that you can use (can-train-with-escrow spearman-line), instead of (can-train-with-escrow spearman). Interestingly, you can safely use the base unit of a unit line with this command instead of the unit line version, and it will work regardless of any upgrades that have been researched. For example, you can safely use (can-train-with-escrow archer) even if Crossbowman has been researched. This capability is important if you are scripting for WololoKingdoms (WK) or any other mod where some unit lines aren't defined in the AI engine. Unique units can be trained dynamically by using my-unique-unit or my-unique-unit-line as long as your aren't scripting for a Userpatch modpack like WK. You can also train by the unit ID rather than the unit name. You can see all units and their unit IDs in theObjects table. In WK, there are two units that use a separate placeholder unit ID for training purposes, and you must use it for all can-train,can-train-with-escrow,train,up-can-train, andup-traincommands. These units are the condottiero and genitour. Use ID 184 for condottiero-placeholder and use ID 732 for genitour-placeholder. You cannot check for the ability to train units with unit classes (like infantry-class) or with sets (like huskarl-set, which includes castle huskarls and barracks huskarls). To check for units like huskarls or tarkans that can be trained at multiple buildings, you must each each unit type separately, such as (or (can-train-with-escrow huskarl) (can-train-with-escrow barracks-huskarl)). To check if mercenary kipchaks (elite kipchaks that allies can train after Cuman Mercenaries is researched) can be trained, use "mercenary-kipchak" rather than kipchak-line. This fact will return false if the setting ofsn-dock-training-filtercurrently restricts the training of ships. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
"""
    pass
def cc_add_resource(Resource: Resource,Value: int,):
    """
 A cheating action that adds the given resource amount to the computer player. This command works even if cheats are disabled. It is to be used in scenarios to avoid late game oddities such as computer player villagers going all over the map while looking for the last pile of gold. Negative amounts can be used to remove resources from the computer player's stockpile. 
:param Resource: Range: 0 to 3, or theClassIdof the resource.
 A gatherable resource type. Note: using the ClassId is not valid for most (all?) of the 1.0c commands that use this parameter. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def cc_players_building_count(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,):
    """
 A cheating version ofplayers-building-count. This command works even if cheats are disabled. For use in scenarios only. The fact checks the given player's building count. Both existing buildings and buildings under construction are included regardless of whether they have been seen - fog is ignored. Unlike building-count, buildings that existed from the start of the game, such as the starting town center, are included. Also, farms are included, but walls and gates are not included. The Fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or a human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def cc_players_building_type_count(PlayerNumber: PlayerNumber,BuildingId: BuildingId,compareOp: compareOp,Value: int,):
    """
 A cheating version ofplayers-building-type-count. This command works even if cheats are disabled. For use in scenarios only. This fact checks the given player's building count for the given building. Both existing buildings and buildings under construction of the given type are included regardless of whether they have been seen - fog is ignored. The Fact allows "focus-player", "target-player", "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). It also allows the use of building line wildcard parameters forBuildingId. The only wildcard parameter available is watch-tower-line. However, it is better to use watch-tower instead of watch-tower-line, even after Guard Tower or Keep upgrades due to some bugs with watch-tower-line. Simply using (cc-players-building-type-count any-enemy watch-tower > 0) will work regardless of tower upgrades. There are four ways you can specify the building "type":  
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def cc_players_unit_count(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,):
    """
 A cheating version ofplayers-unit-count. This command works even if cheats are disabled. For use in scenarios only. This fact checks the given player's unit count. Only trained units are included and fog is ignored. The Fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def cc_players_unit_type_count(PlayerNumber: PlayerNumber,UnitId: UnitId,compareOp: compareOp,Value: int,):
    """
 A cheating version ofplayers-unit-type-count. This command works even if cheats are disabled. For use in scenarios only, though most AI tournaments allows its use to see if particular Gaia objects are on the map at the beginning of the game, for custom map detection purposes. For example, some scripts will check to see if fish are on the map to detect if the map is a water map. This fact checks the given player's unit count. Only trained units of the given type are included and fog is ignored. The Fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). Counting Gaia units (player number 0) is not considered cheating. There are four ways you can specify the unit "type":  
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def chat_local(String: str,):
    """
 Displays the given string (a message in quotation marks) as a local chat message to all players. Local chat messages display chat messages in white rather than with the AI's player color, making this command strictly inferior tochat-to-all. If the chat message string starts with numerals, that number will be sent as a taunt to all players and the starting numerals will be removed from the message. For example, "1 TC" will send taunt 1 to all players and send the message " TC" to all players. 
:param String: Range: A string (quoted text).
 Text inside double quotes. Used in chat messages. With some UP commands you can use %d or %s once in the message as a placeholder for a part of the chat message that should be replaced by a specified piece of data. 
"""
    pass
def chat_local_to_self(String: str,):
    """
 Displays a given string (a message in quotation marks) as local chat message. The message is displayed only if the user is the same player as the computer player sending the message. For debugging purposes only. Local chat messages display chat messages in white rather than with the AI's player color, making this command strictly inferior tochat-to-playerwith my-player-number as the player Id. If the chat message string starts with numerals, that number will be sent as a taunt to self and the starting numerals will be removed from the message. For example, "1 TC" will send taunt 1 to self and send the message " TC" to self. 
:param String: Range: A string (quoted text).
 Text inside double quotes. Used in chat messages. With some UP commands you can use %d or %s once in the message as a placeholder for a part of the chat message that should be replaced by a specified piece of data. 
"""
    pass
def chat_local_using_id(LanguageId: int,):
    """
 Displays a string, defined by a string id, as a local chat message to all players. For more info on String ids, see the description of theLanguageIdparameter. For example, string id 22322 in English is "No wonder thou wert victorious! I shalt abdicate." Local chat messages display chat messages in white rather than with the AI's player color, making this command strictly inferior tochat-to-all-using-id. 
:param LanguageId: Range: a valid LanguageId.
 The ID assigned to a string (quoted text) stored in one of the language.dll files or in a string text file. All words and phrases used by the game are stored in these files. If you have the DE version, you can easily find a list of all language IDs in your Steam installation, usually at "C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\en\strings\key-value\key-value-strings-utf8.txt". For example, language ID 22322 is "No wonder thou wert victorious! I shalt abdicate." 
"""
    pass
def chat_local_using_range(LanguageId: int,Value: int,):
    """
 Displays a random string from a given range as a local chat message to all players. The random string is defined by a string id randomly picked out of a given string id range. For more info on String ids, see the description of theLanguageIdparameter. For example, string ids from 22300 through 22321 include all of the possible random excuses the default AI can give for why it lost the game. Local chat messages display chat messages in white rather than with the AI's player color, making this command strictly inferior tochat-to-all-using-range. 
:param LanguageId: Range: a valid LanguageId.
 The ID assigned to a string (quoted text) stored in one of the language.dll files or in a string text file. All words and phrases used by the game are stored in these files. If you have the DE version, you can easily find a list of all language IDs in your Steam installation, usually at "C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\en\strings\key-value\key-value-strings-utf8.txt". For example, language ID 22322 is "No wonder thou wert victorious! I shalt abdicate." 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def chat_to_all(String: str,):
    """
 Sends a given string (a message in quotation marks) as a chat message to all players. If the chat message string starts with numerals, that number will be sent as a taunt to all players and the starting numerals will be removed from the message. For example, "1 TC" will send taunt 1 to all players and send the message " TC" to all players. 
:param String: Range: A string (quoted text).
 Text inside double quotes. Used in chat messages. With some UP commands you can use %d or %s once in the message as a placeholder for a part of the chat message that should be replaced by a specified piece of data. 
"""
    pass
def chat_to_all_using_id(LanguageId: int,):
    """
 Sends a string, defined by a string id, as a chat message to all players. For more info on String ids, see the description of theLanguageIdparameter. For example, string id 22322 in English is "No wonder thou wert victorious! I shalt abdicate." 
:param LanguageId: Range: a valid LanguageId.
 The ID assigned to a string (quoted text) stored in one of the language.dll files or in a string text file. All words and phrases used by the game are stored in these files. If you have the DE version, you can easily find a list of all language IDs in your Steam installation, usually at "C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\en\strings\key-value\key-value-strings-utf8.txt". For example, language ID 22322 is "No wonder thou wert victorious! I shalt abdicate." 
"""
    pass
def chat_to_all_using_range(LanguageId: int,Value: int,):
    """
 Sends a random string from a given range as a chat message to all players. The random string is defined by a string id randomly picked out of a given string id range. For more info on String ids, see the description of theLanguageIdparameter. For example, string ids from 22300 through 22321 include all of the possible random excuses the default AI can give for why it lost the game. 
:param LanguageId: Range: a valid LanguageId.
 The ID assigned to a string (quoted text) stored in one of the language.dll files or in a string text file. All words and phrases used by the game are stored in these files. If you have the DE version, you can easily find a list of all language IDs in your Steam installation, usually at "C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\en\strings\key-value\key-value-strings-utf8.txt". For example, language ID 22322 is "No wonder thou wert victorious! I shalt abdicate." 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def chat_to_allies(String: str,):
    """
 Sends a given string as a chat message to allies. If the chat message string starts with numerals, that number will be sent as a taunt to all allies and the starting numerals will be removed from the message. For example, "1 TC" will send taunt 1 to all allies and send the message " TC" to all allies. 
:param String: Range: A string (quoted text).
 Text inside double quotes. Used in chat messages. With some UP commands you can use %d or %s once in the message as a placeholder for a part of the chat message that should be replaced by a specified piece of data. 
"""
    pass
def chat_to_allies_using_id(LanguageId: int,):
    """
 Sends a string, defined by a string id, as a chat message to allied players. For more info on String ids, see the description of theLanguageIdparameter. For example, string id 22322 in English is "No wonder thou wert victorious! I shalt abdicate." 
:param LanguageId: Range: a valid LanguageId.
 The ID assigned to a string (quoted text) stored in one of the language.dll files or in a string text file. All words and phrases used by the game are stored in these files. If you have the DE version, you can easily find a list of all language IDs in your Steam installation, usually at "C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\en\strings\key-value\key-value-strings-utf8.txt". For example, language ID 22322 is "No wonder thou wert victorious! I shalt abdicate." 
"""
    pass
def chat_to_allies_using_range(LanguageId: int,Value: int,):
    """
 Sends a random string from a given range as a chat message to allies. The random string is defined by a string id randomly picked out of a given string id range. For more info on String ids, see the description of theLanguageIdparameter. For example, string ids from 22300 through 22321 include all of the possible random excuses the default AI can give for why it lost the game. 
:param LanguageId: Range: a valid LanguageId.
 The ID assigned to a string (quoted text) stored in one of the language.dll files or in a string text file. All words and phrases used by the game are stored in these files. If you have the DE version, you can easily find a list of all language IDs in your Steam installation, usually at "C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\en\strings\key-value\key-value-strings-utf8.txt". For example, language ID 22322 is "No wonder thou wert victorious! I shalt abdicate." 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def chat_to_enemies(String: str,):
    """
 Sends a given string as a chat message to enemies. If the chat message string starts with numerals, that number will be sent as a taunt to all enemies and the starting numerals will be removed from the message. For example, "1 TC" will send taunt 1 to all enemies and send the message " TC" to all enemies. 
:param String: Range: A string (quoted text).
 Text inside double quotes. Used in chat messages. With some UP commands you can use %d or %s once in the message as a placeholder for a part of the chat message that should be replaced by a specified piece of data. 
"""
    pass
def chat_to_enemies_using_id(LanguageId: int,):
    """
 sends a string, defined by a string id, as a chat message to enemy players. For more info on String ids, see the description of theLanguageIdparameter. For example, string id 22322 in English is "No wonder thou wert victorious! I shalt abdicate." 
:param LanguageId: Range: a valid LanguageId.
 The ID assigned to a string (quoted text) stored in one of the language.dll files or in a string text file. All words and phrases used by the game are stored in these files. If you have the DE version, you can easily find a list of all language IDs in your Steam installation, usually at "C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\en\strings\key-value\key-value-strings-utf8.txt". For example, language ID 22322 is "No wonder thou wert victorious! I shalt abdicate." 
"""
    pass
def chat_to_enemies_using_range(LanguageId: int,Value: int,):
    """
 Sends a random string from a given range as a chat message to enemies. The random string is defined by a string id randomly picked out of a given string id range. For more info on String ids, see the description of theLanguageIdparameter. For example, string ids from 22300 through 22321 include all of the possible random excuses the default AI can give for why it lost the game. 
:param LanguageId: Range: a valid LanguageId.
 The ID assigned to a string (quoted text) stored in one of the language.dll files or in a string text file. All words and phrases used by the game are stored in these files. If you have the DE version, you can easily find a list of all language IDs in your Steam installation, usually at "C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\en\strings\key-value\key-value-strings-utf8.txt". For example, language ID 22322 is "No wonder thou wert victorious! I shalt abdicate." 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def chat_to_player(PlayerNumber: PlayerNumber,String: str,):
    """
 Sends a given string as a chat message to a given player. If the chat message string starts with numerals, that number will be sent as a taunt to the specified player and the starting numerals will be removed from the message. For example, "1 TC" will send taunt 1 to the specified player and send the message " TC" to the specified player. The fact allows "my-player-number", "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). It also allows the use of rule variables forPlayerNumber, such as "this-any-ally" or "this-any-enemy". 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param String: Range: A string (quoted text).
 Text inside double quotes. Used in chat messages. With some UP commands you can use %d or %s once in the message as a placeholder for a part of the chat message that should be replaced by a specified piece of data. 
"""
    pass
def chat_to_player_using_id(PlayerNumber: PlayerNumber,LanguageId: int,):
    """
 sends a string, defined by a string id, as a chat message to a given player. For more info on String ids, see the description of theLanguageIdparameter. For example, string id 22322 in English is "No wonder thou wert victorious! I shalt abdicate." The action allows "my-player-number", "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). It also allows the use of rule variables forPlayerNumber, such as "this-any-ally" or "this-any-enemy". 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param LanguageId: Range: a valid LanguageId.
 The ID assigned to a string (quoted text) stored in one of the language.dll files or in a string text file. All words and phrases used by the game are stored in these files. If you have the DE version, you can easily find a list of all language IDs in your Steam installation, usually at "C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\en\strings\key-value\key-value-strings-utf8.txt". For example, language ID 22322 is "No wonder thou wert victorious! I shalt abdicate." 
"""
    pass
def chat_to_player_using_range(PlayerNumber: PlayerNumber,LanguageId: int,Value: int,):
    """
 Sends a random string from a given range as a chat message to a given player. The random string is defined by a string id randomly picked out of a given string id range. For more info on String ids, see the description of theLanguageIdparameter. For example, string ids from 22300 through 22321 include all of the possible random excuses the default AI can give for why it lost the game. The Action allows "my-player-number", "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows the use of rule variables forPlayerNumber, such as "this-any-ally" or "this-any-enemy". It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param LanguageId: Range: a valid LanguageId.
 The ID assigned to a string (quoted text) stored in one of the language.dll files or in a string text file. All words and phrases used by the game are stored in these files. If you have the DE version, you can easily find a list of all language IDs in your Steam installation, usually at "C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\en\strings\key-value\key-value-strings-utf8.txt". For example, language ID 22322 is "No wonder thou wert victorious! I shalt abdicate." 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def chat_trace(Value: int,):
    """
 Displays the given value to all players as a chat message, with "Trace " in front. Used purely for testing to check when a rule gets executed. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def cheats_enabled():
    """
 Checks whether the cheats have been enabled. Cheating commands that start with "cc-" can be used by AI scripts even if cheats are disabled. This command specifically checks whether players can enter cheat codes in the chat. 
"""
    pass
def civilian_population(compareOp: compareOp,Value: int,):
    """
 Checks the computer player's civilian population. The civilian population is villagers, trade units and fishing ships. To check for the civilian-population of other players, useplayers-civilian-population. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def civ_selected(Civ: Civ,):
    """
 Checks the computer player's civilization. You can use "my-civ," which will automatically detect the civilization the AI is playing as. Note that the civilization names used with this command for pre-DE civs are usually different than the civ's display name. They are like the #load-if civ names where they often use the adjective form of the civ name, not the plural name. SeeCivfor a list of correct civ names to use with this command. You can also enclose code in a #load-if-defined [CIV-NAME]-CIV block if it should only run when a particular civ is selected. To check for the civilization of other players, useplayers-civ. 
:param Civ: Range: 0 to the number of civs for the particular game version.
 The player's civilization. You may need to define some civilizations with a defconst. "my-civ" is also an option, which will detect the civilization that the AI is playing as. 
"""
    pass
def clear_tribute_memory(PlayerNumber: PlayerNumber,Resource: Resource,):
    """
 Clears the given player's tribute memory, the amount of a given resource received in tribute from the given player since the tribute memory was cleared. Only tribute memory for the given resource type is cleared. This command is used in conjunction withplayers-tribute-memory, which allows you to check the amount of tribute received from the specified player since clear-tribute-memory was issued. The action allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows the use of rule variables forPlayerNumber, such as "this-any-ally" or "this-any-enemy". It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param Resource: Range: 0 to 3, or theClassIdof the resource.
 A gatherable resource type. Note: using the ClassId is not valid for most (all?) of the 1.0c commands that use this parameter. 
"""
    pass
def commodity_buying_price(Commodity: Commodity,compareOp: compareOp,Value: int,):
    """
 Checks the current buying price for the given commodity. The current buying price is the amount of gold that will be deducted from the gold stockpile to buy 100 of the specified commodity (wood, food, or stone). This price can range between 26 and infinity without Guilds, between 25 and infinity with Guilds, and between 25 and infinity when playing Saracens. 
:param Commodity: Range: 0 to 2.
 A resource that can be bought or sold. Gold is not a commodity. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def commodity_selling_price(Commodity: Commodity,compareOp: compareOp,Value: int,):
    """
 Checks the current selling price for the given commodity. The current selling price is the amount of gold that will be added to the gold stockpile when 100 of the specified commodity (wood, food, or stone) is sold. This price can range between 14 and infinity without Guilds, between 17 and infinity with Guilds, and between 19 and infinity when playing Saracens. 
:param Commodity: Range: 0 to 2.
 A resource that can be bought or sold. Gold is not a commodity. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def current_age(compareOp: compareOp,Age: Age,):
    """
 Checks computer player's current age. In Post-Imperial Age Start games, the current age is imperial-age, not post-imperial-age. To check for Post-Imperial Age Start, use #load-if-defined POST-IMPERIAL-AGE-START orstarting-age. To check for the current-age of other players, useplayers-current-age. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Age: Range: 0 to 3, or 105.
 A valid age.starting-agefacts can also use post-imperial-age. 
"""
    pass
def current_age_time(compareOp: compareOp,Value: int,):
    """
 Checks the computer player's current age time (time spent in the current age). This time is measured in seconds. To check for the current-age-time of other players, useplayers-current-age-time. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def current_score(compareOp: compareOp,Value: int,):
    """
 Checks the computer player's current score. To check for the current-score of other players, useplayers-score. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def death_match_game():
    """
 Checks if the game is a Death Match game. You can also enclose code in a #load-if-defined DEATH-MATCH-GAME block if it should only run in a death match game. In DE, ultra high and infinite resource random map games are considered death match games, and this command will be true in those games. 
"""
    pass
def defend_soldier_count(compareOp: compareOp,Value: int,):
    """
 Checks the computer player's defend soldier count. A defend soldier is a land-based military unit not assigned to attack groups. This includes soldiers attacking with attack-now, with sn-number-attack-groups set > 0, or with TSA. Soldiers don't have to be actively defending the town against attacks to be considered defend soldiers. In other words, the defend-soldier-count is calculated by subtracting the attack-soldier-count from the total soldier-count. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def defend_warboat_count(compareOp: compareOp,Value: int,):
    """
 Checks the computer player's defend warboat count. A defend warboat is a boat capable of attacking that is not assigned to boat attack groups. This includes warboats attacking with attack-now or with sn-number-boat-attack-groups set > 0. Warboats don't have to be actively defending against enemy warship attacks to be considered defend warboats. In other words, the defend-warboat-count is calculated by subtracting the attack-warboat-count from the total warboat-count. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def delete_building(BuildingId: BuildingId,):
    """
 Deletes exactly one building of a given type. You cannot use building classes with this command. There are several other commands available to delete objects:   
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
"""
    pass
def delete_unit(UnitId: UnitId,):
    """
 Deletes exactly one unit of a given type. You cannot use unit classes with this command. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. There are several other commands available to delete objects:   
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
"""
    pass
def difficulty(compareOp: compareOp,Difficulty: Difficulty,):
    """
 Checks the difficulty setting. The ordering of difficulty settings is the opposite of what one would expect! Make sure that this is taken in account when using facts to compare difficulties. easiest > easy > moderate > hard > hardest (ie; treat easiest as a difficulty value of 4, easy as 3, moderate as 2, hard as 1, hardest as 0, and extreme as -1). For testing certain difficulty levels see the code examples. It is counter intuitive! Because of the counter-intuitive ordering of difficulties, you may find it helpful to use the #load-if symbols to check difficulty settings instead, such as #load-if-defined DIFFICULTY-HARD or #load-if-not-defined DIFFICULTY-HARDEST. Remember that easy is referred to as Standard in the game. This information about difficulty is from the CPSB about the hardcoded changes. Automatic changes to some sn values can be stopped withsn-do-not-scale-for-difficulty-level; see this SN for more information. Building construction appears to be unaffected. For non-DE game versions, Hardest difficulty adds a hardcoded 500 of each resource at the beginning of the game and on reaching each new age. This cannot be disabled, but you can remove these resources with a negativecc-add-resourceorup-cc-add-resourcecommand. Also note that starting the game in later ages adds these bonuses incrementally (so up to 2000 for starting in the Imperial Age or Post-Imperial Age). Each difficulty level will change certain SN values automatically (including when set manually) unless sn-do-not-scale-for-difficulty-level is set to 1. Seesn-do-not-scale-for-difficulty-levelfor these values. Small additional note is that Hard also still makes SN changes, so it is recommended for a non-cheating AI to use sn-do-not-scale-for-difficulty-level so it can perform well on Hard. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Difficulty: Range: 0 to 4. Range is -1 to 4 for DE.
 The current difficulty level. The ordering of difficulty settings is the opposite of what one would expect!: easiest > easy > moderate > hard > hardest. Make sure that this is taken in account when using facts to compare difficulties. 
"""
    pass
def disable_rule(Value: int,):
    """
 Disables the given rule id. (Not Fully Implemented! Do Not Use!) 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def disable_self():
    """
 Disables the rule that it is part of so that the rule is never run again. Since disabling takes effect in the next execution pass, other actions in the same rule are still executed once. Use this whenever you only want the rule to run once and never again. Rules disabled with a disable-self command are never read again, but they are still counted as rules by commands that jump over rules likeup-jump-ruleorup-jump-dynamic. 
"""
    pass
def disable_timer(TimerId: int,):
    """
 Disables the given timer. The given timer can be any valid timer number, which can range from 1 to 50. You can also substitute a defconst that is defined with a value between 1 and 50 if you want to give the timer a name. Timers have three possible states, and they cannot have multiple states at once: timer-running, timer-triggered, and timer-disabled. disable-timer orup-set-timerwith a -1 timer length puts the timer in the timer-disabled state.enable-timerorup-set-timerwith a timer length > 0 puts the timer in the timer-running state. disable-timer doesn't have to be used before using an enable-timer command. 
:param TimerId: Range: 1 to 50.
 The ID of a timer or a defconst representing a timer. 
"""
    pass
def doctrine(Value: int,):
    """
 Checks what the current doctrine is, similar to checking the value of a goal. The doctrine is always an integer value which is set with theset-doctrinecommand, and the doctrine command simply checks if the doctrine is currently equal to the given value. Unlike goals, there is only one doctrine that you can set, and you can only use the doctrine command to check if the doctrine is currently equal to the given value, not less than, or greater than, or any other type of comparison. In all cases, using goals instead of the doctrine will give you more flexibility, but if you run out of available goals then you can use the doctrine like an extra goal if you need it. The doctrine starts with the value of -1 at the beginning of the game, and it only changes if you use the set-doctrine command. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def do_nothing():
    """
 Does nothing. Used as a placeholder action if you don't want a rule to have any actions. Every rule must have at least one fact and one action. In rare cases where you don't want to include any actions in your rule, use do-nothing as a placeholder to fulfill the one action requirement. One of these rare cases is when you want to temporarily comment out all the actions in your rule for testing purposes but you want to keep the facts section of your rule. Unlikedisable-selfdo-nothing will not stop the rule from being checked each pass. 
"""
    pass
def dropsite_min_distance(Resource: Resource,compareOp: compareOp,Value: int,):
    """
 Checks computer player's minimum dropsite walking distance for a given resource type. The distance is the tile distance between the tile the resource is on and the center tile of the nearest dropsite. For example, if the dropsite is adjacent to the given resource, then dropsite-min-distance will be 1. Long walking distances indicate a need for a new dropsite. It is not recommended to use this fact for building of first dropsites necessary for age advancement. If, at the beginning, the resources happen to be close enough to the Town Center, building of the first dropsites will be delayed, resulting in slower age progression.  There are eight different types of resource dropsite distances you can check for:   
:param Resource: Range: 0 to 3, or theClassIdof the resource.
 A gatherable resource type. Note: using the ClassId is not valid for most (all?) of the 1.0c commands that use this parameter. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def enable_rule(Value: int,):
    """
 Enables the given rule id. (Not Fully Implemented! Do Not Use!) 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def enable_timer(TimerId: int,Value: int,):
    """
 Enables the given timer and sets it to the given time interval. The given timer can be any valid timer number, which can range from 1 to 50. You can also substitute a defconst that is defined with a value between 1 and 50 if you want to give the timer a name.  Time intervals are measured in game time seconds, so enabling a timer for 240 seconds would start a 4 minute timer. If played on 2.0 speed (Fast speed), this 4 minute timer would last 2 minutes in real time. Timers have three possible states, and they cannot have multiple states at once: timer-running, timer-triggered, and timer-disabled.disable-timerorup-set-timerwith a -1 timer length puts the timer in the timer-disabled state. enable-timer orup-set-timerwith a timer length > 0 puts the timer in the timer-running state. disable-timer doesn't have to be used before using an enable-timer command. 
:param TimerId: Range: 1 to 50.
 The ID of a timer or a defconst representing a timer. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def enable_wall_placement(Perimeter: int,):
    """
 Enables wall placement for the given perimeter, either perimeter 1 or perimeter 2. Walls cannot be built with thebuild-wallcommand at the given perimeter unless this command is used. Enabled wall placement causes the rest of the placement code to do some planning and place all structures at least one tile away from the future wall lines. If you are planning to build a wall, you have to explicitly define which perimeter wall you plan to use when the game starts. This is a one-time action and should be used during the initial setup. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. 
:param Perimeter: Range: 1 or 2.
 The distance to build a wall around the town. Allowed values are 1 and 2, with 1 being closer to the Town Center than 2. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. 
"""
    pass
def enemy_buildings_in_town():
    """
 Returns true if there are sighted enemy buildings less thansn-maximum-town-sizetiles of the computer player's home TC. For this fact, sn-maximum-town-size is a circle of sn-maximum-town-size tiles in a diagonal direction and sn-maximum-town-size * sqrt(2) tiles in any straight direction (it appears a perfect circle on the map rather than a square as for the building commands). Works with all buildings (including walls). Updates every few AOC seconds. 
"""
    pass
def enemy_captured_relics():
    """
 Checks if the enemy team has captured all relics. When this happens, tactical AI automatically starts targeting monasteries and monks. Use this fact to intensify attacks and combine it with theattack-nowaction to force attacks. You can also addsn-special-attack-type1to 1,sn-special-attack-influence1> 0, andup-set-offense-priorityfor monasteries to a high number to increase the likelyhood to target monasteries. 
"""
    pass
def escrow_amount(Resource: Resource,compareOp: compareOp,Value: int,):
    """
 Checks a computer player's escrow stockpile amount for a given resource type. AIs can store each of their four resource stockpiles in one of two stockpile types: normal and escrow. Resources in the normal stockpiles are free for the AI to use, while resources in the escrow stockpiles can only be used withup-build,up-train, orup-researchwhen the EscrowGoalId parameter in these commands is a goal set to the value "with-escrow". The user interface shows the sum of both the normal and escrow stockpile resources added together for each resource. By default, all resources are stored in the normal stockpiles. However,set-escrow-percentageandup-modify-escrowcan be used to store some or all of the AI's resources in the escrow stockpiles instead. Resources in the escrow stockpiles can transferred back into the normal stockpiles by usingrelease-escrow,up-release-escrow, orup-modify-escrow. Resources are usually placed in escrow stockpiles in order to save up for expensive technologies or important buildings or units, so that it isn't spent on lower priority things. 
:param Resource: Range: 0 to 3, or theClassIdof the resource.
 A gatherable resource type. Note: using the ClassId is not valid for most (all?) of the 1.0c commands that use this parameter. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def event_detected(EventType: EventType,EventId: int,):
    """
 Checks if the given event has been detected. Scenario triggers that execute an AI Script Goal effect are the only events that AI scripts can detect. The event-detected fact stays true until the event is explicitly disabled by theacknowledge-eventaction. This command, along withacknowledge-event, is used to detect an AI Script Goal effect from a scenario trigger, often with the intention of changing the AI behavior after the scenario trigger has fired. The scenario designer chooses an AI Trigger number for the AI Script Goal effect in the scenario editor. Then, the event-detected command in the AI script will detect when this trigger effect happens. The event-detected command will remain true after the AI Script Goal trigger effect fires, so acknowledge-event is used to reset the event-detected flag so that event-detected will no longer be true, similar to how thedisable-timercommand clears a timer that has triggered or how theacknowledge-tauntcommand accepts the taunt message. Trigger events are essentially the inverse of signals. To allow an AI script to send a signal which the AI Signal trigger condition can detect, useset-signal. 
:param EventType: Range: 0.
 The type of the event. Triggers are the only valid event types. 
:param EventId: Range: 0 to 255.
 The event ID. The only valid events are AI Script Goal effects and AI Signal conditions in scenario triggers. The ID matches the number of the chosen option from the trigger condition/effect. Note: the "AI Trigger 256" option in the AI Script Goal effect cannot be detected by AIs. 
"""
    pass
def false():
    """
 A Fact that is always false. A rule with this fact will never execute its actions. This command was likely added to the AI engine by Ensemble Studios early on to test logical operators, such as "or," "and," or "not." This command's usefulness is pretty limited, but scripters might be able to use it creatively. If you want to stop a rule from running, a more effective strategy is to comment out each of the lines in the rule with a semi-colon (;). 
"""
    pass
def food_amount(compareOp: compareOp,Value: int,):
    """
 Checks a computer player's food amount. This amount includes escrowed food. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def game_time(compareOp: compareOp,Value: int,):
    """
 Checks the game time, the amount of time elapsed since the start of the game, measured in game seconds. The fact can be used to make rules time-specific. For example, the computer can become more aggressive after 15 minutes of game time. Note: some scripters have reported that unlike other commands that have acompareOpoperator, the game-time command has a slight bug where you cannot use goal comparison operators like g:== or g:>, and only constant or strategic number comparison operators can be used for the compareOp operator. However, I, Leif Ericson, have used goal gomparison operators successfully. Test before using goal comparison operators with the game-time fact. game-time measures the game time in game seconds. The current game time can be found by using F11. Unless the game is being played on Slow speed (1.0 speed), the game time moves faster that real time. Casual speed (Normal speed in single player games in UP) is 1.5 times faster than real time, Normal speed (Normal speed in multiplayer games in UP) is 1.7 times faster than real time, and Fast speed is 2.0 times faster than real time. Even faster speeds are possible with DE launch options (see thisvideoor with the speedhack option in Cheat Engine, though AI behavior can diminish at faster game speeds. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def game_type(compareOp: compareOp,GameType: GameType,):
    """
 Checks the game type. Game types include settings like random-map, regicide, king-of-the-hill, or turbo-random-map. SeeGameTypefor the list of game types. Game types are not defined, so you must defconst them before using them. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param GameType: Range: 0 to 3, 5 to 8.
 The type of game being played. Each of the values in the value list must be defined with a defconst. Note that custom will be from 0 to 8 depending on what the source of the map / game was. 
"""
    pass
def gate_count(Perimeter: int,compareOp: compareOp,Value: int,):
    """
 Checks for the number of gates that are either being built or are completed at the given perimeter. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. This command likely only counts stone gates, but it is possible that you can count only palisade gates instead by settingsn-gate-type-for-wallto 1 before using gate-count. 
:param Perimeter: Range: 1 or 2.
 The distance to build a wall around the town. Allowed values are 1 and 2, with 1 being closer to the Town Center than 2. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def generate_random_number(Value: int,):
    """
 Generates a player-specific integer random number within given range (1 toValue). The number is stored internally and its value can be tested withrandom-number. Subsequent executions of this action generate new random numbers that replace existing ones. If you want to store the random number in a goal, useup-get-fact. Unfortunately, the numbers generated by this command are not truly random, and restarting the game can sometimes result in the same random numbers being generated. It's best to avoid generating random numbers in the first few seconds of the game since the results can be less reliable. If you want to generate a number that is more random, consider usingup-get-precise-timeto get a timestamp into a goal (such as gl-random-number) and then use (up-modify-goal gl-random-number c:mod X) where X is the range of values you want your random number to use. The mod operator (c:mod) divides the goal by the given value (X) and stores the remainder left over from the division. Thus, if X is 100, gl-random-number will range somewhere between 0 and 99. In addition to using up-get-precise-time, you can also do the same c:mod calculation with another number that is fairly random, like a player's score. Unfortunately, these alternative methods can only generate one random number per pass because game state information like up-get-precise-time and player scores are only updated between passes. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def goal(GoalId: int,Value: int,):
    """
 Checks the current value of the given goal. While their purpose may be unclear based on their name, goals are variables which can store an integer value which can be checked with this command or withup-compare-goal. Each goal is given an ID, and AIs have 16000 goals available (only 512 in UP and only 40 in 1.0c) that they can use to store different values, and they all store the value -1 at the beginning of the game. Goals are one of the most important concepts of AI scripting, so it's good to learn how to use them. In programming speak, goals are a 16000-length one-indexed 32-bit integer array, pre-initialized to -1, and a GoalId refers to a particular index of that array. Thegoalcommand checks if the value of the given GoalId is equal to the given value. New goals or variables cannot be defined, only constants (called defconsts by the AI engine), so AI scripters are limited to these 16000 goals, though unused strategic numbers can also be used like goals in a pinch. If the paragraph above makes absolutely no sense to you, you can imagine goals like a bank which holds 16000 bank accounts, numbered with IDs from 1 to 16000. These accounts can hold whole amounts (no cents or decimal amounts of money), and they can store either positive or negative amounts of money. These bank accounts are restricted to holding between -2,147,483,648 and 2,147,483,647 dollars, and they all start with -$1 (negative 1 dollars) stored inside them until they are used by a customer (the AI scripter). Theset-goalandup-modify-goalcommands can modify how much money is stored in a particular account. Following this bank metaphor, thegoalcommand checks if the given bank account number holds the given amount of money. For example, (goal 5 13) checks if goal ID #5 holds the value 13 (i.e. bank account #5 holds $13), and (goal 415 -3274) checks if goal ID #415 holds the value -3,274 (i.e. bank account #415 holds -$3,274). You can also useup-compare-goalto check the current value of a goal ID in a more powerful manner, such as checking if the goal stores greater or less than the given value. It is pretty common to use a defconst to refer to a goal ID number to make the AI more readable. See the second example below on what this looks like. 
:param GoalId: Range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE.
 A valid goal ID. A goal ID can either be a number within the range below or a defined constant set to a number within the range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def gold_amount(compareOp: compareOp,Value: int,):
    """
 Checks a computer player's gold amount. This amount includes escrowed gold. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def hold_koh_ruin():
    """
 Undocumented command that checks whether or not it (or its team) currently holds the monument in King of the Hill games. Koh stands for King of the Kill. 
"""
    pass
def hold_relics():
    """
 Undocumented command that checks whether or not it (or its team) has all of the relics. 
"""
    pass
def housing_headroom(compareOp: compareOp,Value: int,):
    """
 Checks computer player's housing headroom. Housing headroom is the difference between current housing capacity and trained unit capacity. For example, a computer player has a Town Center (capacity 5), a House (capacity 5) and 6 villagers. In this case, housing headroom is 4. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def idle_farm_count(compareOp: compareOp,Value: int,):
    """
 Checks a computer player's idle farm count - the number of farms with no farmers assigned to gather from it. It can be used before a new farm is built to make sure it is needed. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def log(String: str,):
    pass
def log_trace(Value: int,):
    """
 Writes the given value to a log file. Used purely for testing to check when a rule gets executed. Works only if logging is enabled (which it isn't). Useup-log-datainstead. You can also uselogto log a text string if you are scripting for DE. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def map_size(MapSize: MapSize,):
    """
 Checks the map size. The map sizes can be tiny, small, medium, normal, large, giant, or ludikris (DE only). To get the actual dimensions of the map, you can useup-get-pointwith position-map-size, which will store the coordinates of the rightmost point on the map. 
:param MapSize: Range: A valid map size.
 The size of the map. Before DE, Archipelago, Fortress, Island, Migration, and Team Islands are one size bigger than normal. For example, tiny maps will be 144x144 and giant maps will be 255x255 on those maps. In DE, the 240x240 size map name was changed from Giant to Huge. Also, DE introduced a Steam launch parameter "MORE_MAP_SIZES" which enables an expanded set of map sizes. For the standard map sizes there are two variations of the map size name that AIs can use. It's possible some AI features won't work on map sizes larger than 255 if they were originally coded with the assumption that the map dimensions would never exceed 255 tiles. These maps can often cause a lot of lag, so only script for them with care. 
"""
    pass
def map_type(MapType: MapType,):
    """
 Checks the map type. The map type is the map's name. SeeMapTypefor a complete list of maps. For custom random maps, the map type is "custom_map" (yes, with the underscore). The exception is if the custom random map script uses ai_info_map_type. For example, if the random map script hasai_info_map_type ARABIA 0 0 0, then (map-type arabia) will be true instead of (map-type custom_map). 
:param MapType: Range: -1, 9 to 23, or 25 to 44.
 The map the game is being played on. 
"""
    pass
def military_population(compareOp: compareOp,Value: int,):
    """
 Check's the player's military population. Military population includes any units that aren't civilian population (not villagers, trade units and fishing ships). It includes transport ships, but it does not count kings. To check for the military-population of other players, useplayers-military-population. This command counts Karambit Warriors as 1 population, rather than 0.5 population. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def player_computer(PlayerNumber: PlayerNumber,):
    """
 Checks if the given player is a computer player. The fact allows "my-player-number", "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
"""
    pass
def player_human(PlayerNumber: PlayerNumber,):
    """
 Checks if the given player is a human player. The fact allows "my-player-number", "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
"""
    pass
def player_in_game(PlayerNumber: PlayerNumber,):
    """
 Checks if the given player is a valid player and still playing (hasn't resigned or been defeated). The fact allows "my-player-number", "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
"""
    pass
def player_number(PlayerNumber: PlayerNumber,):
    """
 Checks computer player's player number. The player number is the player's slot order, not the number associated with the AI's player color. Only a number between 1 to 8 can be used. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
"""
    pass
def player_resigned(PlayerNumber: PlayerNumber,):
    """
 Checks if the given player has lost by resigning. Note that a player can lose without resigning, so this fact should not be used to check whether a player has lost a game. To check whether a player has lost a game (such as player 3) use:  
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
"""
    pass
def player_valid(PlayerNumber: PlayerNumber,):
    """
 Checks if the given player is a valid player, meaning the player slot was used during the game. In games with more than 2 players, players that lost before the game is over are still considered to be valid players. This is because although the player is not in the game, their units/buildings can still be in the game. To check whether the given player is still in the game use theplayer-in-gamefact. The fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
"""
    pass
def players_building_count(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,):
    """
 Checks the given player's building count. Both existing buildings and buildings under construction are included. The computer player relies only on what it has seen - no cheating. Ifsn-coop-share-informationis set to its default value of 1, any buildings seen by allies are also counted. A cheating version of this command,cc-players-building-count, can be used to count any building of this type, whether it has been scouted or not. The fact allows "focus-player", "target-player", "any"/"every" wildcard parameters forPlayerNumber, and the use of building line wildcard parameters forBuildingId. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def players_building_type_count(PlayerNumber: PlayerNumber,BuildingId: BuildingId,compareOp: compareOp,Value: int,):
    """
 Checks the given player's building count of the given type. Both existing buildings and buildings under construction of the given type are included. The computer player relies only on what it has seen - no cheating. Ifsn-coop-share-informationis set to its default value of 1, any buildings seen by allies are also counted. A cheating version of this command,cc-players-building-type-count, can be used to count any building, whether it has been scouted or not. The fact allows "focus-player", "target-player", "any"/"every" wildcard parameters forPlayerNumber, and the use of building line wildcard parameters forBuildingId. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def players_civ(PlayerNumber: PlayerNumber,Civ: Civ,):
    """
 Checks the given player's civilization. Note that the civilization names used with this command for pre-DE civs are usually different than the civ's display name. They are like the #load-if civ names where they often use the adjective form of the civ name, not the plural name. SeeCivfor a list of correct civ names to use with this command. The fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). You can use "my-civ" for the Civ parameter, which will automatically detect the civilization the AI is playing as.  
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param Civ: Range: 0 to the number of civs for the particular game version.
 The player's civilization. You may need to define some civilizations with a defconst. "my-civ" is also an option, which will detect the civilization that the AI is playing as. 
"""
    pass
def players_civilian_population(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,):
    """
 Checks a given player's civilian population, which includes villagers, fishing ships, and trade units. This fact includes seen and unseen civilians for the given player. The CPSB notes that this is equivalent to a human player checking the timeline, which was possible in-game in AoE1, and it was probably also possible during AoE2 development when the CPSB was written, hence why this isn't regarded as a cc- cheating command. However, since this command includes unseen civilian units, some consider this command to be cheating when it's used to check enemy civilian population, but the AI scripting community permits this command in AI tournaments for historical reasons. The fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def players_current_age(PlayerNumber: PlayerNumber,compareOp: compareOp,Age: Age,):
    """
 Checks the given player's current age. The CPSB notes that this is equivalent to a human player checking the timeline, which was possible in-game in AoE1, and it was probably also possible during AoE2 development when the CPSB was written. Of course, this information is available to all players in-game, even without the timeline. The fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Age: Range: 0 to 3, or 105.
 A valid age.starting-agefacts can also use post-imperial-age. 
"""
    pass
def players_current_age_time(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,):
    """
 Checks the given player's current age time -- time spent in the current age. The CPSB notes that this is equivalent to a human player checking the timeline, which was possible in-game in AoE1, and it was probably also possible during AoE2 development when the CPSB was written. Of course, this information could be calculated in-game even without using the timeline. The fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def players_military_population(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,):
    """
 Checks the given player's military population, which includes all units except for villagers, fishing ships, trade units, and kings. This fact includes seen and unseen military units for the given player. This command counts Karambit Warriors as 1 population, rather than 0.5 population. The CPSB notes that this is equivalent to a human player checking the timeline, which was possible in-game in AoE1, and it was probably also possible during AoE2 development when the CPSB was written, hence why this isn't regarded as a cc- cheating command. However, since this command includes unseen military units, some consider this command to be cheating when it's used to check enemy military population, but the AI scripting community permits this command in AI tournaments for historical reasons. The fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def players_population(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,):
    """
 Checks the given player's population. This fact includes seen and unseen units for the given player. This command counts Karambit Warriors as 1 population, rather than 0.5 population. The CPSB notes that this is equivalent to a human player checking the timeline, which was possible in-game in AoE1, and it was probably also possible during AoE2 development when the CPSB was written, hence why this isn't regarded as a cc- cheating command. However, since this command includes unseen units, some consider this command to be cheating when it's used to check enemy population, but the AI scripting community permits this command in AI tournaments for historical reasons. When checking for the population of an enemy player, consider usingplayers-unit-count. players-unit-count can overestimate enemy unit counts, but it doesn't count unseen units. The fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def players_score(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,):
    """
 Checks the given player's current score. The fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def players_stance(PlayerNumber: PlayerNumber,PlayerStance: PlayerStance,):
    """
 Checks if the given player's diplomatic stance toward the computer player matches the give stance, either ally, neutral, or enemy. To check our stance toward another player, usestance-toward. The fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param PlayerStance: Range: 0 to 3.
 A diplomatic stance, including ally, neutral, and enemy. Some UP commands also allow you to specify "any" stance instead of one of the three particular stances. 
"""
    pass
def players_tribute(PlayerNumber: PlayerNumber,Resource: Resource,compareOp: compareOp,Value: int,):
    """
 Checks the player's tribute given throughout the game. Only tribute for the given resource type is checked. The fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param Resource: Range: 0 to 3, or theClassIdof the resource.
 A gatherable resource type. Note: using the ClassId is not valid for most (all?) of the 1.0c commands that use this parameter. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def players_tribute_memory(PlayerNumber: PlayerNumber,Resource: Resource,compareOp: compareOp,Value: int,):
    """
 Checks a player's tribute given since the player's tribute memory for the given resource was cleared. Only tribute memory for the given resource type is checked. The tribute memory is cleared by usingclear-tribute-memory. The fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param Resource: Range: 0 to 3, or theClassIdof the resource.
 A gatherable resource type. Note: using the ClassId is not valid for most (all?) of the 1.0c commands that use this parameter. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def players_unit_count(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,):
    """
 Checks the given player's unit count. The computer player relies only on what it has seen - no cheating. For allies and self only trained units are included. To count the units of other players, each AI internally stores an explored objects list which is used by the players-unit-count,players-unit-type-count,players-building-count, andplayers-building-type-countcommands. Every time the AI sees an object owned by another player, that object is added to this list. However, while explored ally objects that have died are immediately removed from the explored objects list, the AI doesn't remove enemy objects from this list when they die because the object might have died in the fog of war without the AI's knowledge. Instead, the AI clears their explored objects list periodically, about every five minutes. Settingsn-coop-share-informationallows AIs to read the explored object lists of ally players. Researching Cartography, turning on the Shared Exploration game setting in DE, and researching Spies likely don't change how the explored object list system works. The possible presence of dead enemy objects in the explored object list means that players-unit-count may overcount the actual unit counts of enemy players. The fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def players_unit_type_count(PlayerNumber: PlayerNumber,UnitId: UnitId,compareOp: compareOp,Value: int,):
    """
 Checks the given player's unit count of the given type. The computer player relies only on what it has seen - no cheating. For allies and self only trained units of the given type are included. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used if you're counting the AI's own units, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. However, to count the AI's own units, consider usingunit-type-countorunit-type-count-totalinstead. Important Note:players-unit-type-count cannot use classes to count enemy units, such as (players-unit-type-count any-enemy cavalry-class > 5), though you can use classes to count allied units or the computer player's own units. To count the units of other players, each AI internally stores an explored objects list which is used by theplayers-unit-count, players-unit-type-count,players-building-count, andplayers-building-type-countcommands. Every time the AI sees an object owned by another player, that object is added to this list. However, while explored ally objects that have died are immediately removed from the explored objects list, the AI doesn't remove enemy objects from this list when they die because the object might have died in the fog of war without the AI's knowledge. Instead, the AI clears their explored objects list periodically, about every five minutes. Settingsn-coop-share-informationallows AIs to read the explored object lists of ally players. Researching Cartography, turning on the Shared Exploration game setting in DE, and researching Spies likely don't change how the explored object list system works. The possible presence of dead enemy objects in the explored object list means that players-unit-type-count may overcount the actual unit counts of enemy players. The fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def population(compareOp: compareOp,Value: int,):
    """
 Checks the computer player's population. To check for the population of other players, useplayers-population. This command counts Karambit Warriors as 1 population, rather than 0.5 population. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def population_cap(compareOp: compareOp,Value: int,):
    """
 Checks the population cap setting. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def population_headroom(compareOp: compareOp,Value: int,):
    """
 Checks the computer player's population headroom. Population headroom is the difference between the game's population cap and current housing capacity. For example, in a game with a population cap of 75, if the computer player has a town center (capacity 5) and a house (capacity 5), then the population headroom is 65. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def random_number(compareOp: compareOp,Value: int,):
    """
 Checks the value of the most recent random number value generated bygenerate-random-number. To store the random number in a goal, useup-get-factwith random-number as theFactId. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def regicide_game():
    """
 Checks if the game is a regicide game. You can also enclose code in a #load-if-defined REGICIDE block if it should only run in a regicide game. In DE, to check if the Regicide secondary game mode is active you can usefe-sub-game-type. 
"""
    pass
def release_escrow(Resource: Resource,):
    """
 Releases the computer player's escrow for a given resource type (transfers all of the given resource type from its escrow stockpile into its normal stockpile, setting the amount stored in that resource's escrow stockpile to 0). AIs can store each of their four resource stockpiles in one of two stockpile types: normal and escrow. Resources in the normal stockpiles are free for the AI to use, while resources in the escrow stockpiles can only be used withup-build,up-train, orup-researchif the EscrowGoalId parameter in these commands is a goal set to the value "with-escrow". The user interface shows the sum of both the normal and escrow stockpile resources added together for each resource. By default, all resources are stored in the normal stockpiles. However,set-escrow-percentageandup-modify-escrowcan be used to store some or all of the AI's resources in the escrow stockpiles instead. Resources in the escrow stockpiles can transferred back into the normal stockpiles by using release-escrow,up-release-escrow, orup-modify-escrow. Resources are usually placed in escrow stockpiles in order to save up for expensive technologies or important buildings or units, so that it isn't spent on lower priority things. 
:param Resource: Range: 0 to 3, or theClassIdof the resource.
 A gatherable resource type. Note: using the ClassId is not valid for most (all?) of the 1.0c commands that use this parameter. 
"""
    pass
def research(TechId: int,):
    """
 Researches the given item if the technology is available to the player and the technology can be researched without escrowed resources. Please usecan-research,can-research-with-escrow, orup-can-researchin any rule where you use the research command, in order to prevent possible crashes. To prevent cheating, this action will fail if the item currently cannot be researched (i.e. the tech prerequisites are not met, there is no available building, or the player cannot afford the item). Research names, except for ages, my-unique-research, my-second-unique-research, are prefixed with a "ri-" which might stand for "research item". You can also research by the research ID rather than the research name. You can see all technologies and their research IDs in theTechnologies table. You can also use my-unique-research, which will usually (always in DE) research the imperial age unique tech for the civilization, and you can also use my-second-unique-research, which will usually (always in DE) research the castle age unique tech for the civilization. In UP and WK, the exceptions are the Britons (in WK only) and Goths, whose my-unique-research and my-second-unique-research are switched. 
:param TechId: Range: A valid technology ID.
 The name of a technology or the ID number assigned to that technology. See the Technology table for details [to be added later]. Note that some technologies are given an AI name that is different from the in-game technology name. 
"""
    pass
def research_available(TechId: int,):
    """
 Checks that the given research is available to the computer player's civ, and that the research is available at this time (technology and tech tree prerequisites are met). The fact does not check that there are enough resources to start researching or if the player has built the building needed to research the technology. Unfortunately, because most technologies have an age as a prerequisite tech, research-available cannot be used at the beginning of the game to check if a technology is available in the civ's tech tree. There currently isn't a command that simply checks whether a technology is available in a civ's tech tree. Using this command is equivalent to usingup-research-statusto check if the technology's research status is equal to research-available. 
:param TechId: Range: A valid technology ID.
 The name of a technology or the ID number assigned to that technology. See the Technology table for details [to be added later]. Note that some technologies are given an AI name that is different from the in-game technology name. 
"""
    pass
def research_completed(TechId: int,):
    """
 Checks that the given research is completed. Using this command is equivalent to usingup-research-statusto check if the technology's research status is equal to research-complete. 
:param TechId: Range: A valid technology ID.
 The name of a technology or the ID number assigned to that technology. See the Technology table for details [to be added later]. Note that some technologies are given an AI name that is different from the in-game technology name. 
"""
    pass
def resign():
    """
 Causes the computer player to resign. 
"""
    pass
def resource_found(Resource: Resource,):
    """
 Checks whether the computer player has found the given resource. For food, gold, and stone (not wood), the given resource must be within the dropsite's max distance for this command to be true (sn-mill-max-distancefor food andsn-mining-camp-max-distanceorsn-camp-max-distancefor gold and stone). The fact should be used at the beginning period of the game. Once it becomes true for a certain resource it stays true for that resource. Only forests, not straggler trees, will make resource-found true for wood. Also, only forage bushes will make resource-found true for food. Usingup-gaia-type-count,up-gaia-type-count-total, ordropsite-min-distanceare often better commands to use than resource-found because they can count how many of the given resource have been found or determine how far away the resources are. 
:param Resource: Range: 0 to 3, or theClassIdof the resource.
 A gatherable resource type. Note: using the ClassId is not valid for most (all?) of the 1.0c commands that use this parameter. 
"""
    pass
def sell_commodity(Commodity: Commodity,):
    """
 Sells one lot of a given commodity. The AI will sell 100 of the given commodity (wood, food, or stone) in return for gold at the currentcommodity-selling-price. The commodity selling price is the amount of gold that will be added to the gold stockpile when 100 of the specified commodity (wood, food, or stone) is sold. This price can range between 14 and infinity without Guilds, between 17 and infinity with Guilds, and between 19 and infinity when playing Saracens. 
:param Commodity: Range: 0 to 2.
 A resource that can be bought or sold. Gold is not a commodity. 
"""
    pass
def set_author_email():
    """
 The game does not use it for anything. 
"""
    pass
def set_author_name():
    """
 The game does not use it for anything. 
"""
    pass
def set_author_version():
    """
 The game does not use it for anything. 
"""
    pass
def set_difficulty_parameter(DiffParameterId: DiffParameterId,Value: int,):
    """
 Sets a given difficulty parameter to a given value. Difficulty parameters are similar to strategic numbers. There are two difficulty parameters that can be set: ability-to-maintain-distance or ability-to-dodge-missiles. Both have a range from 0 to 100, and the values have the opposite effect from what you'd expect! Setting a difficulty parameter to 0 completely enables the difficulty parameter behavior, and setting a difficulty parameter to 100 disables it. It isn't possible to check the current value of each difficulty parameter. Descriptions of each difficulty parameter:  
:param DiffParameterId: Range: 0 to 1.
 A Difficulty Parameter ID. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def set_doctrine(Value: int,):
    """
 Sets the doctrine to the given value, similar to setting the value of a goal. The doctrine is always an integer value and you can check if the doctrine is set to a given value with thedoctrinecommand. Unlike goals, there is only one doctrine that you can set, and you can only use the set-doctrine command to set the doctrine to a specific value. You can't dynamically set the doctrine to equal the value of a goal or strategic number, like you can with goals. In all cases, using goals instead of the doctrine will give you more flexibility, but if you run out of available goals then you can use the doctrine like an extra goal if you need it. The doctrine starts with the value of -1 at the beginning of the game, and it only changes if you use the set-doctrine command. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def set_escrow_percentage(Resource: Resource,Value: int,):
    """
 Sets the computer player's escrow percentage for a given resource type. Given values have to be in the range 0-100. AIs can store each of their four resource stockpiles in one of two stockpile types: normal and escrow. Resources in the normal stockpiles are free for the AI to use, while resources in the escrow stockpiles can only be used withup-build,up-train, orup-researchif the EscrowGoalId parameter in these commands is a goal set to the value "with-escrow". The user interface shows the sum of both the normal and escrow stockpile resources added together for each resource. By default, all resources are stored in the normal stockpiles. However, set-escrow-percentage andup-modify-escrowcan be used to store some or all of the AI's resources in the escrow stockpiles instead. set-escrow-percentage sets the percentage of the resources a villager or fishing ship is carrying that will be stored in the escrow stockpile instead of the normal stockpile every time the villager or fishing ship drops off the resources they are carrying. For example, if a villager is dropping off 10 wood at the lumber camp and the wood escrow percentage is set to 30, then 3 of the 10 wood that is dropped off is stored in the wood escrow stockpile, while the remaining 7 wood is stored in the normal wood stockpile. set-escrow-percentage only applies to resources as they are dropped off. It does not immediately force a certain percentage of the total stockpile to be stored in escrow. For example, if the AI has 1000 gold, setting the gold escrow percentage to 20 does not mean that the AI will reallocate its gold stockpiles so that 200 gold will be in the gold escrow stockpile and 800 gold will be in the normal gold stockpile. If you want this behavior, you can useup-modify-escrowinstead (see the examples section on the up-modify-escrow page on how to do this). Resources in the escrow stockpiles can transferred back into the normal stockpiles by using release-escrow,up-release-escrow, orup-modify-escrow. Resources are usually placed in escrow stockpiles in order to save up for expensive technologies or important buildings or units, so that it isn't spent on lower priority things. There is no command that can check the current escrow percentage, so if you want to check the current escrow percentage, you'll need to store this percentage in a goal or an unused strategic number when you use set-escrow-percentage. 
:param Resource: Range: 0 to 3, or theClassIdof the resource.
 A gatherable resource type. Note: using the ClassId is not valid for most (all?) of the 1.0c commands that use this parameter. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def set_goal(GoalId: int,Value: int,):
    """
 Sets a given goal to a given value. While their purpose may be unclear based on their name, goals are variables which can store an integer value which can be checked with this command or withup-compare-goal. Each goal is given an ID, and AIs have 16000 goals available (only 512 in UP and only 40 in 1.0c) that they can use to store different values, and they all store the value -1 at the beginning of the game. Goals are one of the most important concepts of AI scripting, so it's good to learn how to use them. In programming speak, goals are a 16000-length one-indexed 32-bit integer array, pre-initialized to -1, and a GoalId refers to a particular index of that array. The set-goal command sets the value the given GoalId to the given integer value. New goals or variables cannot be defined, only constants (called defconsts by the AI engine), so AI scripters are limited to these 16000 goals, though unused strategic numbers can also be used like goals in a pinch. If the paragraph above makes absolutely no sense to you, you can imagine goals like a bank which holds 16000 bank accounts, numbered with IDs from 1 to 16000. These accounts can hold whole amounts (no cents or decimal amounts of money), and they can store either positive or negative amounts of money. These bank accounts are restricted to holding between -2,147,483,648 and 2,147,483,647 dollars, and they all start with -$1 (negative 1 dollars) stored inside them until they are used by a customer (the AI scripter). The set-goal andup-modify-goalcommands can modify how much money is stored in a particular account. Following this bank metaphor, thegoalcommand checks if the given bank account number holds the given amount of money. For example, (goal 5 13) checks if goal ID #5 holds the value 13 (i.e. bank account #5 holds $13), and (goal 415 -3274) checks if goal ID #415 holds the value -3,274 (i.e. bank account #415 holds -$3,274). You can also useup-compare-goalto check the current value of a goal ID in a more powerful manner, such as checking if the goal stores greater or less than the given value. It is pretty common to use a defconst to refer to a goal ID number to make the AI more readable. See the second example below on what this looks like. 
:param GoalId: Range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE.
 A valid goal ID. A goal ID can either be a number within the range below or a defined constant set to a number within the range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def set_shared_goal(SharedGoalId: int,Value: int,):
    """
 Sets a given shared goal (a goal that is shared among all computer players) to a given value. To be used only when all computer players are on the same team. Shared goals are a separate set of 256 goals, in addition to the regular 16000 normal goals, which are shared between all AIs in the game, even between AIs that are enemies. Any AI can modify them at any time with set-shared-goal orup-set-shared-goal, and all AIs can check their values withshared-goalorup-get-shared-goal. Otherwise, shared goals share the same characteristics of normal goals, which you can read about in theset-goaldescription. Because shared goals can change without the AI's knowledge and the fact than enemy AIs can check their values, it's often better to useup-allied-goal, which allows you to check the value of one of an allied AI's normal 16000 goals. 
:param SharedGoalId: Range: 1 to 256.
 A goal that is shared among computer players. It is to be used only when all computer players are on the same team. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def set_signal(SignalId: int,):
    """
 Sets a given signal value that can be checked by the AI Signal trigger condition in the scenario editor. To set a signal dynamically, useup-set-signal. To check if a signal was already set, useup-get-signal. There are 256 different signals that an AI can send to the scenario editor, from 0 to 255, which can trigger various events in the scenario. Signals are essentially on/off flags which are set to "off" at the beginning of the game, and are set to "on" whenever the set-signal action is used. This AI Signal trigger condition can be very useful to detect events that AIs can detect, but scenario triggers cannot easily detect, such as receiving tribute. Once the given signal is set, the scenario designer can create a trigger with the condition "AI Signal", and select the corresponding AI Signal value in the dropdown list. Once the signal is set in the AI script, the AI Signal condition for the given signal value will become true for the rest of the game, even after a trigger with an AI Signal condition is executed, unless you use theup-set-signalAI command to turn the signal off by setting the signal ID to the value 0, or the scenario designer uses the Acknowledge AI Signal trigger effect to turn the signal off (this trigger effect is only available in DE). Signals are essentially the inverse of AI Script Goal trigger effects. To allow an AI script to detect an AI Script Goal trigger effect from a scenario trigger, useevent-detected. This action only works with a single player scenario and "AI Signal" trigger condition. For a multiplayer scenario, use "Multiplayer AI Signal" andfe-set-signal. 
:param SignalId: Range: 0 to 255.
 The Id of a scenario trigger signal. This if effectively the same asEventIdsince the only types of events are trigger signals. 
"""
    pass
def set_stance(PlayerNumber: PlayerNumber,PlayerStance: PlayerStance,):
    """
 Sets the diplomatic stance toward a given player to the specified stance, either ally, neutral, or enemy. To check our stance toward a given player, usestance-toward. To check the stance another player has toward us, useplayers-stance. The action allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows the use of rule variables for Player, such as "this-any-ally" or "this-any-enemy". It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param PlayerStance: Range: 0 to 3.
 A diplomatic stance, including ally, neutral, and enemy. Some UP commands also allow you to specify "any" stance instead of one of the three particular stances. 
"""
    pass
def set_strategic_number(SnId: int,Value: int,):
    """
 Sets a given strategic number to a given value. See theStrategic Numberssection for more info on each strategic number. Each strategic number has a different default value, which you can also check on the SN Index page. Each SN is given an ID between 0 and 511. Currently, the SNs in the 313-511 range don't appear in the SN index and don't modify the behavior of your AI, but they are available for your AI to use. So, you can modify these SNs however you like, similar to goals, without changing the behavior of your AI. However, if you want to use a strategic number in this way like an extra custom goal, always check the SN index to make sure that the SN ID you are using is actually currently unused. A good practice is to start with using SN 510 (SN 511 might have some bugs in DE) and work your way backwards toward SNs in the 300 range. 
:param SnId: Range: 0 to 511.
 A strategic number. SeeStrategic Numbersfor a list of usable strategic numbers and their descriptions. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def shared_goal(SharedGoalId: int,Value: int,):
    """
 Checks a given shared goal (a goal that is shared among all computer players). It is to be used only when all computer players are on the same team. Shared goals are a separate set of 256 goals, in addition to the regular 16000 normal goals, which are shared between all AIs in the game, even between AIs that are enemies. Any AI can modify them at any time withset-shared-goalorup-set-shared-goal, and all AIs can check their values with shared-goal orup-get-shared-goal. Otherwise, shared goals share the same characteristics of normal goals, which you can read about in theset-goaldescription. Because shared goals can change without the AI's knowledge and the fact than enemy AIs can check their values, it's often better to useup-allied-goal, which allows you to check the value of one of an allied AI's normal 16000 goals. 
:param SharedGoalId: Range: 1 to 256.
 A goal that is shared among computer players. It is to be used only when all computer players are on the same team. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def sheep_and_forage_too_far():
    """
 Checks whether the computer player has any forage site(s) and/or sheep within 8 tiles of the drop-off location (Mill or Town Center). If not, this fact is true. To check if any resource is within a certain distance of a dropsite, you can usedropsite-min-distanceinstead, which is usually more flexible. You can check if the AI can currently see any particular resource withup-gaia-type-count. 
"""
    pass
def soldier_count(compareOp: compareOp,Value: int,):
    """
 Checks the computer player's soldier count. A soldier is a land-based military unit. Monks and siege weapons are included.attack-soldier-count+defend-soldier-countshould equal soldier-count. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def spy():
    """
 Executes a spy command. Only works in Regicide games to research the Treason effect. The computer player does see the revealed area around the enemy kings as expected. This command does not research Spies like you might expect. 
"""
    pass
def stance_toward(PlayerNumber: PlayerNumber,PlayerStance: PlayerStance,):
    """
 Checks if the computer player's diplomatic stance toward a given player matches the given stance, either ally, neutral, or enemy. To check another player's diplomatic stance toward the computer player, useplayers-stance. The fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1).  
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param PlayerStance: Range: 0 to 3.
 A diplomatic stance, including ally, neutral, and enemy. Some UP commands also allow you to specify "any" stance instead of one of the three particular stances. 
"""
    pass
def starting_age(compareOp: compareOp,Age: Age,):
    """
 Checks the game's starting age. In addition to the regular age parameters, post-imperial-age can be used. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Age: Range: 0 to 3, or 105.
 A valid age.starting-agefacts can also use post-imperial-age. 
"""
    pass
def starting_resources(compareOp: compareOp,StartingResources: StartingResources,):
    """
 Checks the starting resources level. The standard setting is Low resources. In games without a Starting Resources option, like Death Match, starting-resources will be equal to 1 (low resources), probably because 1 is the standard resource setting in random map games. DE added the option for Ultra High, Infinite, and Random resource starts. Before DE, AIs on hardest difficulty would get 500 of each resource at the beginning of each age, including at the beginning of the game, but DE no longer does this. Starting resources can be modified bysn-add-starting-resource-wood,sn-add-starting-resource-food,sn-add-starting-resource-gold, orsn-add-starting-resource-stone, though using these strategic numbers is considered cheating in AI tournaments. Starting resource amounts:  
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param StartingResources: Range: 1 to 6.
 The starting resources level of the game. 
"""
    pass
def stone_amount(compareOp: compareOp,Value: int,):
    """
 Checks a computer player's stone amount. This amount includes escrowed stone. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def strategic_number(SnId: int,compareOp: compareOp,Value: int,):
    """
 Checks a strategic number's value. Strategic numbers modify various built-in behaviors and settings that can modify the automatic behaviors of your AI. See theSN Indexfor details on what each strategic number does. Each strategic number has a different default value, which you can also check on the SN Index page. Each SN is given an ID between 0 and 511. Currently, the SNs in the 313-511 range don't appear in the SN index and don't modify the behavior of your AI, but they are available for your AI to use. So, you can modify these SNs however you like, similar to goals, without changing the behavior of your AI. However, if you want to use a strategic number in this way like an extra custom goal, always check the SN index to make sure that the SN ID you are using is actually currently unused. A good practice is to start with using SN 510 (SN 511 might have some bugs in DE) and work your way backwards toward SNs in the 300 range. 
:param SnId: Range: 0 to 511.
 A strategic number. SeeStrategic Numbersfor a list of usable strategic numbers and their descriptions. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def taunt(TauntId: int,):
    """
 Triggers the taunt associated with the given value. This taunt will only be sent to allies, and other AIs can detect this taunt with thetaunt-detectedcommand. To send a randomized taunt to allies between a range of taunt values, you can usetaunt-using-range. You can also use any of the chat commands, likechat-to-player, to send a taunt along with a chat message. To do this, put the taunt number at the very beginning of the message, followed by the rest of the chat message, like (chat-to-allies "/3Please send food!"). In DE, the forward slash "/" is currently required, but in UP it is not. This example will send taunt 3 to all allies, and they will see the message without the taunt number at the beginning, just like when a human player starts a chat message with a taunt number. 
:param TauntId: Range: 1 to 255.
 A valid taunt ID. Only taunts 1-42 will send an audio version of the taunt, but all taunts within the range below can be sent and detected by AIs. 
"""
    pass
def taunt_detected(PlayerNumber: PlayerNumber,TauntId: int,):
    """
 Detects a given taunt from the given player. The check can be performed any number of times until the taunt is explicitly acknowledged, meaning that if the given taunt is received from the given player, this fact with remain true until the AI uses theacknowledge-tauntcommand to acknowledge the taunt from that player. taunt-detected will detect taunts sent to the AI from another AI that uses thetauntcommand, and it will also detect taunts sent in a chat message if the message starts with a number between 1 and 255. The fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param TauntId: Range: 1 to 255.
 A valid taunt ID. Only taunts 1-42 will send an audio version of the taunt, but all taunts within the range below can be sent and detected by AIs. 
"""
    pass
def taunt_using_range(TauntId: int,Value: int,):
    """
 Triggers a random taunt that is picked from a given taunt range. This taunt will only be sent to allies, and other AIs can detect this taunt with thetaunt-detectedcommand. 
:param TauntId: Range: 1 to 255.
 A valid taunt ID. Only taunts 1-42 will send an audio version of the taunt, but all taunts within the range below can be sent and detected by AIs. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def timer_triggered(TimerId: int,):
    """
 Checks whether a given timer has triggered (the time on the timer has run out). For disabled or running timers this fact is always false. The check can be performed any number of times until the timer is explicitly disabled or enabled again (restarted). The given timer ID can be any valid timer ID, which can range from 1 to 50. You can also substitute a defconst that is defined with a value between 1 and 50 if you want to give the timer a name. Timers have three possible states, and they cannot have multiple states at once: timer-running, timer-triggered, and timer-disabled. All 50 timers start in the timer-disabled state, and timer-triggered command is only true when the timer is in the timer-triggered state. To disable a timer, usedisable-timeror useup-set-timerwith a -1 timer length. To enable a timer, useenable-timeror useup-set-timerwith a timer length > 0. 
:param TimerId: Range: 1 to 50.
 The ID of a timer or a defconst representing a timer. 
"""
    pass
def town_under_attack():
    """
 town-under-attack is triggered (i.e. returns true) if any unit/building belonging to the computer player that is insidesn-maximum-town-sizegets attacked. It lasts 1 to 10 in-game seconds after the attack. It is not triggered by attacks to buildings or villagers that are outside sn-maximum-town-size. This command detects ally attackers. Because town-under-attack detects any attack events within sn-maximum-town-size, it can sometimes trigger town-under-attack in conditions when a human player wouldn't consider the town under attack, such as if a wolf attacks a villager or an enemy scout attacks a villager while exploring. Most importantly, town-under-attack can trigger when the AI is using TSA to attack the enemy, since sn-maximum-town-size is large enough to detect attack events that occur in the enemy's town, so use town-under-attack with care. 
"""
    pass
def trace_fact():
    """
 Undocumented action that doesn't work. Probably only for debugging purposes originally. 
"""
    pass
def train(UnitId: UnitId,):
    """
 Trains the given unit if the unit is available to the player and the unit can be trained without escrowed resources. In order to use escrow resources, they must be released withrelease-escrow,up-release-escrow, orup-modify-escrow. To prevent cheating, this action uses the same criteria as thecan-trainfact to make sure the unit can be trained. It also checks When possible, use unit lines with this command. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. You can also train by the unit ID rather than the unit name. You can see all units and their unit IDs in theObjects table. You cannot use unit classes or unit sets, like huskarl-set. To train units which can be trained at multiple buildings, like huskarls, tarkans, konniks, and serjeants, you must use a separate unit type or unit line to train them from their non-castle building. Look up these units in the Objects Table for more information. To train mercenary kipchaks (elite kipchaks that allies can train after Cuman Mercenaries is researched), use "mercenary-kipchak" rather than kipchak-line. In WK, there are two units that use a separate placeholder unit ID for training purposes, and you must use it for alltrain,can-train-with-escrow, train,up-can-train, andup-traincommands. These units are the condottiero and genitour. Use ID 184 for condottiero-placeholder and use ID 732 for genitour-placeholder.   Interestingly, you can safely use the base unit of a unit line with this command instead of the unit line version, and it will work regardless of any upgrades that have been researched. For example, you can safely use (train archer) even if Crossbowman has been researched. This capability is important if you are scripting for WololoKingdoms (WK) or any other mod where some unit lines aren't defined in the AI engine. The setting ofsn-dock-training-filteraffects the ability for docks to train warships with this command. The fact allows the use of unit line wildcard parameters forUnitId. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
"""
    pass
def tribute_to_player(PlayerNumber: PlayerNumber,Resource: Resource,Value: int,):
    """
 Tributes the given amount of the given resource type to the player defined by the PlayerNumber parameter. If the computer player does not have a Market, no tribute is given. In the case when the value parameter specifies an amount larger than available, only the available resources of the given type are tributed. If, for example, there is only 60 food and the tribute action specifies 100 food, only 60 food will be tributed. The tribute action is ignored when there are no resources of the given type. Tribute fees are paid and deducted from the tribute amount (if applicable). The action allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows the use of rule variables for Player, such as "this-any-ally" or "this-any-enemy". It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param Resource: Range: 0 to 3, or theClassIdof the resource.
 A gatherable resource type. Note: using the ClassId is not valid for most (all?) of the 1.0c commands that use this parameter. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def true():
    """
 A Fact that is always true. Each rule has to have at least one fact/condition, so this command is often used as a placeholder for rules that should execute its actions without conditions. 
"""
    pass
def unit_available(UnitId: UnitId,):
    """
 Checks that the unit is available to the computer player's civ, and that the tech tree prerequisites for training the unit are met. The fact does not check whether the unit training can start, meaning this command does not check resource availability, housing headroom, or whether the building needed for training is currently used for research/training of another unit. The fact allows the use of unit line wildcard parameters forUnitId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. When the AI checks the tech tree prerequisites, this includes checking whether the prerequisite age has been researched. There isn't a way at the beginning of the game to check if the unit will be available for the civilization in future ages. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
"""
    pass
def unit_count(compareOp: compareOp,Value: int,):
    """
 Checks the computer player's unit count. Only trained units are included. To check for the unit-count of other players, useplayers-unit-count. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def unit_count_total(compareOp: compareOp,Value: int,):
    """
 Checks the computer player's total unit count. The total includes trained and queued units. To check for the unit-count of other players (not including queued units), useplayers-unit-type-count. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def unit_type_count(UnitId: UnitId,compareOp: compareOp,Value: int,):
    """
 Checks the computer player's unit count of the given type. Only trained units of the given type are included. The fact allows the use of unit line wildcard parameters forUnitId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. There are four ways you can specify the unit "type":  To check for the unit-type-count of other players, useplayers-unit-type-count. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def unit_type_count_total(UnitId: UnitId,compareOp: compareOp,Value: int,):
    """
 Checks the computer player's unit count of the given type, including queued units. The fact allows the use of unit line wildcard parameters forUnitId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. There are four ways you can specify the unit "type":  To check for the unit-type-count of other players, useplayers-unit-type-count. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def victory_condition(VictoryCondition: VictoryCondition,):
    """
 Checks the game victory condition. The victory conditions can be standard, conquest, time-limit, score, or custom. 
:param VictoryCondition: Range: 0 to 4.
 A victory condition. 
"""
    pass
def wall_completed_percentage(Perimeter: int,compareOp: compareOp,Value: int,):
    """
 Checks the completion percentage for a given perimeter wall. Trees and other destructible natural barriers are included and count as completed. On island maps if there is an entirely water based barrier between the AI and any enemies then this will return 100% completed. The given perimeter must have been enabled withenable-wall-placement, and you should not check the completed percentage until the pass after the given wall perimeter has been enabled. Allowed perimieter values are 1 and 2, with 1 being closer to the Town Center than 2. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. 
:param Perimeter: Range: 1 or 2.
 The distance to build a wall around the town. Allowed values are 1 and 2, with 1 being closer to the Town Center than 2. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def wall_invisible_percentage(Perimeter: int,compareOp: compareOp,Value: int,):
    """
 Checks what percentage of the potential wall placement is covered with fog. If the invisible percentage is not equal to 0 we do not know if there is a hole or not. This is because the hidden tile(s) might have a tree(s). The given perimeter must have been enabled withenable-wall-placement, and you should not check the invisible percentage until the pass after the given wall perimeter has been enabled. Allowed perimieter values are 1 and 2, with 1 being closer to the Town Center than 2. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. 
:param Perimeter: Range: 1 or 2.
 The distance to build a wall around the town. Allowed values are 1 and 2, with 1 being closer to the Town Center than 2. Perimeter 1 is usually between 10 and 20 tiles from the starting Town Center. Perimeter 2 is usually between 18 and 30 tiles from the starting Town Center. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def warboat_count(compareOp: compareOp,Value: int,):
    """
 Checks the computer player's warboat count. A warboat is a ship capable of attacking. Fishing ships, transport ships, and trade cogs aren't included. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def wood_amount(compareOp: compareOp,Value: int,):
    """
 Checks a computer player's wood amount. This amount includes escrowed wood. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_add_cost_data(GoalId: int,Value: int,):
    """
 Add or subtract another set of cost data to the current cost data. 
:param GoalId: Range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE.
 A valid goal ID. A goal ID can either be a number within the range below or a defined constant set to a number within the range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_add_object_by_id(SearchSource: SearchSource,Id: int,):
    """
 Add an object to the search results by id. This command can be used as either a Fact or an Action. 
:param SearchSource: Range: 1 or 2
 The desired search source. 
:param Id: Range: An ID of an object that is currently on the map.
 The object's ID on the map. All objects on the map will have a different map object ID in the order that the object appeared on the map. 
"""
    pass
def up_add_object_cost(ObjectId: int,Value: int,):
    """
 Add or subtract objects of a specific type to the current cost data. Note the special exception for town centers below. Gates likely also need to use foundation IDs instead. 
:param ObjectId: Range: A validUnitIdor a validBuildingId.
 AUnitIdor aBuildingId. See theObjects Tablefor details. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_add_point(Point1:Point,Point2:Point,Value: int,):
    """
 Add or subtract two point goal pairs together and store the result in Point1. The Value parameter indicates how many instances of Point2 to add to Point1. A negative Value will result in subtracting this number of instances of Point2 from Point1. Set Point2 to 0 to use the point that is stored by up-set-target-point. 
:param Point1: is a point object
:param Point2: is a point object
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_add_research_cost(TechId: int,Value: int,):
    """
 Add or subtract techs of a specific type to the current cost data. 
:param TechId: Range: A valid technology ID.
 The name of a technology or the ID number assigned to that technology. See the Technology table for details [to be added later]. Note that some technologies are given an AI name that is different from the in-game technology name. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_allied_goal(PlayerNumber: PlayerNumber,GoalId: int,compareOp: compareOp,Value: int,):
    """
 Perform a comparison with an allied AI's goal variable. The command cannot be used to check human players or computer players who are not allies. 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param GoalId: Range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE.
 A valid goal ID. A goal ID can either be a number within the range below or a defined constant set to a number within the range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_allied_resource_amount(PlayerNumber: PlayerNumber,ResourceType: ResourceType,compareOp: compareOp,Value: int,):
    """
 Perform a comparison with an ally's internal resource value. The command cannot be used to check the resources of players who are not allies. 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param ResourceType: Range: 0 to 224 (with some gaps for unused resources).
 A resource type. Includes over 200 more resource types beyond the four basic ones. Some resource types check the resource amount of a specified player number instead of the current player. Note: most of these are not thoroughly tested (by Leif Ericson). Please report your findings. Resources 205 through 210 are used by the post-Conquerors expansions, so they can be used with this parameter, but they aren't defined with UserPatch. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_allied_resource_percent(PlayerNumber: PlayerNumber,ResourceType: ResourceType,compareOp: compareOp,Value: int,):
    """
 Perform a comparison with an ally's internal resource value * 100. This command cannot be used with players who are not allies. 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param ResourceType: Range: 0 to 224 (with some gaps for unused resources).
 A resource type. Includes over 200 more resource types beyond the four basic ones. Some resource types check the resource amount of a specified player number instead of the current player. Note: most of these are not thoroughly tested (by Leif Ericson). Please report your findings. Resources 205 through 210 are used by the post-Conquerors expansions, so they can be used with this parameter, but they aren't defined with UserPatch. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_allied_sn(PlayerNumber: PlayerNumber,SnId: int,compareOp: compareOp,Value: int,):
    """
 Perform a comparison with an allied AI's strategic number. This command cannot be used on human players or players who aren't allies. 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param SnId: Range: 0 to 511.
 A strategic number. SeeStrategic Numbersfor a list of usable strategic numbers and their descriptions. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_assign_builders(BuildingId: BuildingId,Value: int,):
    """
 Assign a specific number of builders to a building type or class. This assignment lasts for all future buildings of the specified building type or class until a new up-assign-builders command is issued. If the current number of builders for the building type or class is less than the amount of villagers specified by up-assign-builders, the additional builders are immediately sent to help construct the building. If you want a certain number of assign builders to only last for the construction of one building, you must set up-assign-builders again after the building is constructed. Additionally, if you want to stop sending any builders to construct a building type or class, you must set up-assign-builders to -1, not 0. When using any build command besidesup-build-line, the game will automatically assign one builder to construct the building, regardless of what you have up-assign-builders set to. However, if the original builder is killed or restasked and up-assign-builders is set to -1 for the building, the AI will not send a replacement builder to finish the building. Assigning the number of builders by class is best for walls and gates. By default, like v1.0c, wonders have 250 (max) builders, and the wall class has 2. 
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_attacker_class(compareOp: compareOp,ClassId: ClassId,):
    """
 Check the class of the last enemy object to trigger town-under-attack. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param ClassId: Range: -1, 900 to 999.
 A class ID. Each object in the game is assigned a class that contains other similar objects. Class IDs can often be used in place of a unit ID. Classes with an asterisk (*) in the name must be defined with a defconst. All other classes are defined in the UserPatchConst.per file that comes with a UserPatch installation. See theObjects Tableto see which units belong to each class. 
"""
    pass
def up_bound_point(Point1:Point,Point2:Point,):
    """
 Copy a point goal pair (Point2), shift it into the map bounds, and store the bounded point in Point1. 
:param Point1: is a point object
:param Point2: is a point object
"""
    pass
def up_bound_precise_point(Point: int,Option: int,Value: int,):
    """
 Bound a point goal pair, either a normal point or a precise point, inside the map according to the number of tiles specified by the Value parameter, effectively acting as if the map has been shrunk on all sides by the number of tiles specified by the Value parameter. For example, the point (0,3) will be bounded to the point (5,5) if the Value parameter is 5. Please ensure that Value is a valid value and will not cause an overflow for the map size. If Option is set to 1, the command will treat the point goal pair as precise point and multiply the map size by 100 before bounding to account for the precise point coordinates, so the Value parameter should be adjusted accordingly by multiplying by 100. The bounded point will be stored back into the original point goal pair. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
:param Option: Range: varies
 A value that determines different ways the command will work. Here is a list:  
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_build(PlacementType: PlacementType,EscrowGoalId: int,BuildingId: BuildingId,):
    """
 Add a building to the construction queue with dynamic values. The AI will avoid placing the building in the following locations according to the placement type: System 1 (used by place-normal, place-control, and place-point): System 2 (used by place-forward):  
:param PlacementType: Range: 0 to 3.
 The type of building placement. Executeup-set-placement-databefore using place-control. 
:param EscrowGoalId: Range: 0 or a valid GoalId, ranging from 1 to 16000.
 A goal ID that controls whether escrow should be used. It can be set to the value "with-escrow" or the value "without-escrow". Alternatively, you can use 0 instead of a goal ID to specify that escrow should never be used for this item. Note that using the constants "with-escrow" or "without-escrow" themselves for EscrowGoalId is not valid because 0 or a valid goal ID is expected. 
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
"""
    pass
def up_build_line(Point1:Point,Point2:Point,BuildingId: BuildingId,):
    """
 Place a line of buildings between two point goal pairs. For town centers and gates, please use a FoundationId, such as town-center-foundation or gate-ascending. Do not use town-center or gate with this command. 
:param Point1: is a point object
:param Point2: is a point object
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
"""
    pass
def up_building_type_in_town(BuildingId: BuildingId,compareOp: compareOp,Value: int,):
    """
 Check the number of a specific enemy building type in town. 
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_buy_commodity(ResourceType: ResourceType,Value: int,):
    """
 Buy a variable amount of resources at the market. The actual amount you receive depends on available gold. 
:param ResourceType: Range: 0 to 224 (with some gaps for unused resources).
 A resource type. Includes over 200 more resource types beyond the four basic ones. Some resource types check the resource amount of a specified player number instead of the current player. Note: most of these are not thoroughly tested (by Leif Ericson). Please report your findings. Resources 205 through 210 are used by the post-Conquerors expansions, so they can be used with this parameter, but they aren't defined with UserPatch. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_can_build(EscrowGoalId: int,BuildingId: BuildingId,):
    """
 Check if a building can be constructed with dynamic values. 
:param EscrowGoalId: Range: 0 or a valid GoalId, ranging from 1 to 16000.
 A goal ID that controls whether escrow should be used. It can be set to the value "with-escrow" or the value "without-escrow". Alternatively, you can use 0 instead of a goal ID to specify that escrow should never be used for this item. Note that using the constants "with-escrow" or "without-escrow" themselves for EscrowGoalId is not valid because 0 or a valid goal ID is expected. 
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
"""
    pass
def up_can_build_line(EscrowGoalId: int,Point: int,BuildingId: BuildingId,):
    """
 Check if a building can be constructed at a point goal pair. For town centers and gates, please use a FoundationId, such as town-center-foundation or gate-ascending. Do not use town-center or gate with this command. 
:param EscrowGoalId: Range: 0 or a valid GoalId, ranging from 1 to 16000.
 A goal ID that controls whether escrow should be used. It can be set to the value "with-escrow" or the value "without-escrow". Alternatively, you can use 0 instead of a goal ID to specify that escrow should never be used for this item. Note that using the constants "with-escrow" or "without-escrow" themselves for EscrowGoalId is not valid because 0 or a valid goal ID is expected. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
"""
    pass
def up_can_research(EscrowGoalId: int,TechId: int,):
    """
 Check if a technology can be researched with dynamic values. 
:param EscrowGoalId: Range: 0 or a valid GoalId, ranging from 1 to 16000.
 A goal ID that controls whether escrow should be used. It can be set to the value "with-escrow" or the value "without-escrow". Alternatively, you can use 0 instead of a goal ID to specify that escrow should never be used for this item. Note that using the constants "with-escrow" or "without-escrow" themselves for EscrowGoalId is not valid because 0 or a valid goal ID is expected. 
:param TechId: Range: A valid technology ID.
 The name of a technology or the ID number assigned to that technology. See the Technology table for details [to be added later]. Note that some technologies are given an AI name that is different from the in-game technology name. 
"""
    pass
def up_can_search(SearchSource: SearchSource,):
    """
 Check the status for either the local or remote search. If the result list is full or the index offset is at the end of the player object list, this will return false. 
:param SearchSource: Range: 1 or 2
 The desired search source. 
"""
    pass
def up_can_train(EscrowGoalId: int,UnitId: UnitId,):
    """
 Check if a unit can be trained with dynamic values. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used for the Unit ID to check, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. This fact will return false if nhe setting ofsn-dock-training-filtercurrently restricts the training of ships. 
:param EscrowGoalId: Range: 0 or a valid GoalId, ranging from 1 to 16000.
 A goal ID that controls whether escrow should be used. It can be set to the value "with-escrow" or the value "without-escrow". Alternatively, you can use 0 instead of a goal ID to specify that escrow should never be used for this item. Note that using the constants "with-escrow" or "without-escrow" themselves for EscrowGoalId is not valid because 0 or a valid goal ID is expected. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
"""
    pass
def up_cc_add_resource(ResourceType: ResourceType,Value: int,):
    """
 Add resources dynamically to the player stockpile. This is considered a cheat command, but cheats do not have to be enabled. 
:param ResourceType: Range: 0 to 224 (with some gaps for unused resources).
 A resource type. Includes over 200 more resource types beyond the four basic ones. Some resource types check the resource amount of a specified player number instead of the current player. Note: most of these are not thoroughly tested (by Leif Ericson). Please report your findings. Resources 205 through 210 are used by the post-Conquerors expansions, so they can be used with this parameter, but they aren't defined with UserPatch. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_cc_send_cheat(String: str,):
    """
 Send a message in order to execute a cheat code. Cheats must be enabled for this to take effect. 
:param String: Range: A string (quoted text).
 Text inside double quotes. Used in chat messages. With some UP commands you can use %d or %s once in the message as a placeholder for a part of the chat message that should be replaced by a specified piece of data. 
"""
    pass
def up_change_name(String: str,):
    """
 Change the name of the AI during gameplay. When you use (up-change-name -1), the AI's name will be set to one of that civilization's first 8 built-in historical names in an semi-random manner, same as the names used in the default AI. The name is guaranteed to be unique among other AIs that use this command, but not necessarily with Petersen's selection. 
:param String: Range: A string (quoted text).
 Text inside double quotes. Used in chat messages. With some UP commands you can use %d or %s once in the message as a placeholder for a part of the chat message that should be replaced by a specified piece of data. 
"""
    pass
def up_chat_data_to_all(String: str,Value: int,):
    """
 Send a chat message with a formatted value to everyone. 
:param String: Range: A string (quoted text).
 Text inside double quotes. Used in chat messages. With some UP commands you can use %d or %s once in the message as a placeholder for a part of the chat message that should be replaced by a specified piece of data. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_chat_data_to_player(PlayerNumber: PlayerNumber,String: str,Value: int,):
    """
 Send a chat message with a formatted value to a player. The Action allows "my-player-number", "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows the use of rule variables forPlayerNumber, such as "this-any-ally" or "this-any-enemy". It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param String: Range: A string (quoted text).
 Text inside double quotes. Used in chat messages. With some UP commands you can use %d or %s once in the message as a placeholder for a part of the chat message that should be replaced by a specified piece of data. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_chat_data_to_self(String: str,Value: int,):
    """
 Send a chat message with a formatted value locally. 
:param String: Range: A string (quoted text).
 Text inside double quotes. Used in chat messages. With some UP commands you can use %d or %s once in the message as a placeholder for a part of the chat message that should be replaced by a specified piece of data. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_clean_search(SearchSource: SearchSource,ObjectData: ObjectData,SearchOrder: SearchOrder,):
    """
 Removes duplicate ids or sorts the search results. If ObjectData is set to -1, this will attempt to remove duplicates, lowering the result total. When removing duplicates, using search-order-none to preserve the existing order may perform slower than with asc/desc. If you wish to sort by ObjectData, it's best to remove duplicates first. Depending on the number of objects in the list, this command may be expensive, so please take care. 
:param SearchSource: Range: 1 or 2
 The desired search source. 
:param ObjectData: Range: a valid ObjectData ID. -1 can only be used with up-remove-objects.
 Data information about an object. This information is gathered from the unit's current stats, including any techs that have been researched or civ bonuses that affect the unit. Important Note:some object data is not available for units marching in formation when usingup-get-object-dataorup-object-data: object-data-action, object-data-order, object-data-target, and object-data-target-id. 
:param SearchOrder: Range: 0 to 2.
 Determines how the results should be sorted. 
"""
    pass
def up_compare_const(Defconst: int,compareOp: compareOp,Value: int,):
    """
 Perform a comparison with a constant value. A defconst that defines a string (quoted text) stores a string table index where the string is stored. Therefore, up-compare-const will compare against the string index of such a defconst, rather than the text itself. 
:param Defconst: Range: A defconst.
 A defconst.up-compare-constrequires a defconst defined with an integer value.up-compare-textrequires a defconst defined with a text string. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_compare_flag(GoalId: int,compareOp: compareOp,Flag: int,):
    """
 Perform a bitwise flag test with a goal variable. Flags allow multiple states to be stored in a single value by using powers of 2 (1, 2, 4, 8, 16, etc.). You can use [cgs]:== to see if a flag is stored or [cgs]:!= to see if it isn't stored. 
:param GoalId: Range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE.
 A valid goal ID. A goal ID can either be a number within the range below or a defined constant set to a number within the range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Flag: Range: A valid flag.
 A flag that belongs to the given goal. A flag has two states: appended or removed. See the list of commands that use this parameter for more info. 
"""
    pass
def up_compare_goal(GoalId: int,compareOp: compareOp,Value: int,):
    """
 Perform a comparison with a goal variable. 
:param GoalId: Range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE.
 A valid goal ID. A goal ID can either be a number within the range below or a defined constant set to a number within the range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_compare_sn(GoalId: int,compareOp: compareOp,Value: int,):
    """
 Perform a comparison with a strategic number. 
:param GoalId: Range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE.
 A valid goal ID. A goal ID can either be a number within the range below or a defined constant set to a number within the range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_compare_text(Defconst: int,compareOp: compareOp,Value: int,):
    """
 Perform a string comparison with the stored text. You must store text before using this command and the provided Defconst must be a text defconst. If the provided string cannot be found anywhere in the stored text, the value will be -1. Otherwise, the value will be the index of the match. 
:param Defconst: Range: A defconst.
 A defconst.up-compare-constrequires a defconst defined with an integer value.up-compare-textrequires a defconst defined with a text string. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_copy_point(Point1:Point,Point2:Point,):
    """
 Copy one point goal pair (Point2) into another pair of extended goals (Point1). 
:param Point1: is a point object
:param Point2: is a point object
"""
    pass
def up_create_group(IndexGoalId,CountGoalId,GroupId: int,):
    """
 Reset the group and create a search group from the local search results. The number of units put into the group will be capped by the number stored in CountGoalId. If 0 is used for the CountGoalId parameter, up to 40 objects will be put into the group instead (the highest amount). If there are no units available in the results list to create the specified group, the group will be cleared in the same way asup-reset-group. 
:param IndexGoalId: NOT_DEFINED
:param CountGoalId: NOT_DEFINED
:param GroupId: Range: 0 to 19.
 An ID assigned to a group of objects, similar to Ctrl groups human players can use. In UP, only GroupId's 0 through 9 could be used. However, in DE, GroupId's 0 through 19 work. 
"""
    pass
def up_cross_tiles(Point1:Point,Point2:Point,Value: int,):
    """
 Get a point perpendicular to two point goal pairs. The Value parameter specifies how many tiles away the new point will be from Point1, perpendicularly away in reference to Point2. A negative Value will result in the new point being located perpendicularly away in opposite direction. Set Point2 to 0 to use the point that is stored by up-set-target-point. The new point will be stored in Point1. 
:param Point1: is a point object
:param Point2: is a point object
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_defender_count(compareOp: compareOp,Value: int,):
    """
 Check the number of units actively defending in town. With this command you can check to see if your TSA attack is actually actively targeting anything or if it's just idling. If, after expecting your new town-size to initiate a defensive attack, the response from this command is far less than expected for several consecutive turns, your target may be unreachable by the defensive targeting system (target has been walled for protection by one of their allies, etc.) and you may need to switch targets. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_delete_distant_farms(Value: int,):
    """
 Delete all farms that exist outside the specified drop distance. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_delete_idle_units(IdleType: IdleType,):
    """
 Delete all idle units of the specified type. 
:param IdleType: Range: 0 to 3.
 The type of idle unit. 
"""
    pass
def up_delete_objects(UnitId: UnitId,Value: int,):
    """
 Delete all objects with less hitpoints than the specified Value. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_disband_group_type(GroupType: GroupType,):
    """
 Disband all internal groups of the specified type. To attack with groups with TSA, it is possible to collect units into large groups, disband with up-disband-group-type, and then send them with TSA. 
:param GroupType: Range: 100 to 109.
 The type of group. 
"""
    pass
def up_drop_resources(Resource: Resource,Value: int,):
    """
 Request a drop by gatherers carrying a specific number of a resource. This command works for both villagers and fishing ships. 
:param Resource: Range: 0 to 3, or theClassIdof the resource.
 A gatherable resource type. Note: using the ClassId is not valid for most (all?) of the 1.0c commands that use this parameter. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_enemy_buildings_in_town(compareOp: compareOp,Value: int,):
    """
 Check the number of targetable enemy buildings in town. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_enemy_units_in_town(compareOp: compareOp,Value: int,):
    """
 Check the number of targetable enemy units in town. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_enemy_villagers_in_town(compareOp: compareOp,Value: int,):
    """
 Check the number of targetable enemy villagers in town. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_filter_distance(MinDistance: int,MaxDistance: int,):
    """
 Set distance parameters for the direct targeting system. If any of these parameters is set to -1, then the associated condition will be ignored during search filtering. 
:param MinDistance: Range: -1 to 32767.
 The minimum acceptable distance from the point specified byup-set-target-point. If set to -1, no minimum distance for the filter is set. 
:param MaxDistance: Range: -1 to 32767.
 The maximum acceptable distance from the point specified byup-set-target-point. If set to -1, no maximum distance for the filter is set. 
"""
    pass
def up_filter_exclude(CmdId: CmdId,ActionId: ActionId,OrderId: OrderId,ClassId: ClassId,):
    """
 Set exclude parameters for the direct targeting system. If any of these parameters is set to -1, then the associated condition will be ignored during search filtering. 
:param CmdId: Range: -1 to 10.
 An object's command ID. The command ID (or interface type) determines the available actions for the object or which actions display in the bottom left corner when the object is selected. To determine an objects command ID, look up the object's Interface Type in the Advanced Genie Editor. 
:param ActionId: Range: -1, 600 to 699.
 The current action(s) of an object. Sometimes an object can have more than one current action. It's also often wise to check an object'sOrderIdsince orders last longer. 
:param OrderId: Range: -1, 700 to 799.
 The current order for the object. Sometimes an object can have more than one current order. 
:param ClassId: Range: -1, 900 to 999.
 A class ID. Each object in the game is assigned a class that contains other similar objects. Class IDs can often be used in place of a unit ID. Classes with an asterisk (*) in the name must be defined with a defconst. All other classes are defined in the UserPatchConst.per file that comes with a UserPatch installation. See theObjects Tableto see which units belong to each class. 
"""
    pass
def up_filter_garrison(MinGarrison: int,MaxGarrison: int,):
    """
 Set garrison parameters for the direct targeting system. If any of these parameters is set to -1, then the associated condition will be ignored during search filtering. 
:param MinGarrison: Range: -1 to 32767.
 The minimum acceptable value for objects garrisoned. If set to -1, no minimum garrison amount is set. 
:param MaxGarrison: Range: -1 to 32767.
 The maximum acceptable value for objects garrisoned. If set to -1, no maximum garrison amount is set. 
"""
    pass
def up_filter_include(CmdId: CmdId,ActionId: ActionId,OrderId: OrderId,OnMainland: int,):
    """
 Set include parameters for the direct targeting system. If any of these parameters is set to -1, then the associated condition will be ignored during search filtering. 
:param CmdId: Range: -1 to 10.
 An object's command ID. The command ID (or interface type) determines the available actions for the object or which actions display in the bottom left corner when the object is selected. To determine an objects command ID, look up the object's Interface Type in the Advanced Genie Editor. 
:param ActionId: Range: -1, 600 to 699.
 The current action(s) of an object. Sometimes an object can have more than one current action. It's also often wise to check an object'sOrderIdsince orders last longer. 
:param OrderId: Range: -1, 700 to 799.
 The current order for the object. Sometimes an object can have more than one current order. 
:param OnMainland: Range: -1, 0, or 1.
 If set to 1, select only objects on the mainland, the land that the AI started on. If set to 0, select those not on the mainland. If set to -1, this parameter will be ignored. 
"""
    pass
def up_filter_range(MinGarrison: int,MaxGarrison: int,MinDistance: int,MaxDistance: int,):
    """
 Set range parameters for the direct targeting system. If any of these parameters is set to -1, then the associated condition will be ignored during search filtering. 
:param MinGarrison: Range: -1 to 32767.
 The minimum acceptable value for objects garrisoned. If set to -1, no minimum garrison amount is set. 
:param MaxGarrison: Range: -1 to 32767.
 The maximum acceptable value for objects garrisoned. If set to -1, no maximum garrison amount is set. 
:param MinDistance: Range: -1 to 32767.
 The minimum acceptable distance from the point specified byup-set-target-point. If set to -1, no minimum distance for the filter is set. 
:param MaxDistance: Range: -1 to 32767.
 The maximum acceptable distance from the point specified byup-set-target-point. If set to -1, no maximum distance for the filter is set. 
"""
    pass
def up_filter_status(ObjectStatus: ObjectStatus,ObjectList: ObjectList,):
    """
 Set the object status value for use with up-find-status. The default (after up-reset-filters) is 2, which should match most active objects. Buildings that are incomplete have a status of 0, while certain resources have a status of 3. For remote search, up-find-remote can find objects with object status values 0 to 3 (status-pending, status-ready, and status-resource) if you search by object type id instead of class id. 
:param ObjectStatus: Range: 0, 2 to 5.
 Specifies the status of objects that should be filtered. Default is status-ready. 
:param ObjectList: Range: 0 or 1.
 Specifies whether the filter should apply to objects in the active list or the inactive list. Here's some background info from scripter64 in response to a question on why some custom flags in a mod weren't being animated: Custom building flags can't be animated due to the performance overhead of updating them. There can be many houses and wall segments (each one counts as a separate "building") on a map each game, so ES moved these objects into a separate [inactive] list that does not update per-turn to avoid excessive computational overhead. When attacked, they are moved into the main per-turn update list in order to animate their fire if necessary. Gates are always in the main list. The current flag fix only enables the palisade wall ends to animate by moving those specific objects into the main object list that can update per-turn for redrawing and animation. It would probably be bad for the general performance of the game if we were to undo the ES optimization entirely and allow all objects into the per-turn update list. 
"""
    pass
def up_find_flare(Point: int,):
    """
 Read the (x,y) position of an allied flare into an extended goal pair. This command writes to 2 consecutive goals and requires an extended goal pair between 41 and 15998. If it fails to get a valid position, it will return (-1,-1). This command is equivalent to up-find-player-flare with any-ally. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
"""
    pass
def up_find_local(UnitId: UnitId,Value: int,):
    """
 Find objects owned by the local player for direct targeting. If UnitId changes, the search index offset will be reset. Otherwise, it will continue from where it left off. This command can be used as either a Fact or an Action. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_find_next_player(PlayerStance: PlayerStance,FindPlayerMethod: FindPlayerMethod,OutputGoalId: int,):
    """
 Find the next active player based on the provided information. 
:param PlayerStance: Range: 0 to 3.
 A diplomatic stance, including ally, neutral, and enemy. Some UP commands also allow you to specify "any" stance instead of one of the three particular stances. 
:param FindPlayerMethod: Range: 0 to 3.
 The method used to find a player. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_find_player(PlayerStance: PlayerStance,FindPlayerMethod: FindPlayerMethod,OutputGoalId: int,):
    """
 Find the first active player based on the provided information. 
:param PlayerStance: Range: 0 to 3.
 A diplomatic stance, including ally, neutral, and enemy. Some UP commands also allow you to specify "any" stance instead of one of the three particular stances. 
:param FindPlayerMethod: Range: 0 to 3.
 The method used to find a player. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_find_player_flare(PlayerNumber: PlayerNumber,Point: int,):
    """
 Read the (x,y) position of any visible flare into an extended goal pair. This command writes to 2 consecutive goals and requires an extended goal pair between 41 and 15998. If it fails to get a valid position, it will return (-1,-1). Please note that it has never been designed to work with this-any-* or every-* wildcards, as flares belong to all recipient players, even when they aren't owned by them, so the stored player from this-* would not necessarily be the actual sender of the flare. If you search for players-unit-type-count any-* flare, do not expect this-* to be the sender player for any action commands (not limited to just the flare stuff). If you need to know the specific player number of the sender, you'll need to loop with focus-player checks. The action allows "my-player-number", "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
"""
    pass
def up_find_remote(UnitId: UnitId,Value: int,):
    """
 Find objects owned by the focus player for direct targeting. Set sn-focus-player-number before using this command. If the focus or UnitId changes, the search index offset will be reset. Otherwise, it will continue from where it left off. This command can be used as either a Fact or an Action. Normally, up-find-remote will only find status-ready objects, but up-find-remote can also find objects with object status values 0 to 3 (status-pending, status-ready, and status-resource) if you search by object type id instead of class id. For self/ally objects, it can find them directly at all times. For non-ally objects, if the object has been sighted and is either a building or has been seen/reseen within the past 5 seconds, it can be found. This should allow the AI to target units that are clearly visible without cheating, and target sighted enemy buildings in the fog. One other note: although the new targeting and find commands aren't as heavy as attack-now, like any command that directly manipulates units like retreat-now, guard-unit, etc., please try not to flood them. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_find_resource(Resource: Resource,Value: int,):
    """
 Find gatherable resource objects for direct targeting. This command stores data in the remote list and it will consider the status value set by up-filter-status. To find stone, gold, fallen trees, and other directly gatherable resources, status-resource is required. For standing trees and living objects, status-ready is required. Please ensure the proper status is set before searching. The remote index will reset automatically when switching between this command and other remote search commands like up-find-remote. If Resource changes, the search index offset will be reset. Otherwise, it will continue from where it left off. This command can be used as either a Fact or an Action. When searching with boar-class (class 910), this command will not include wolves in the search. 
:param Resource: Range: 0 to 3, or theClassIdof the resource.
 A gatherable resource type. Note: using the ClassId is not valid for most (all?) of the 1.0c commands that use this parameter. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_find_status_local(UnitId: UnitId,Value: int,):
    """
 Find objects owned by the local player filtered by status. This is identical to up-find-local, except it will consider the status value set by up-filter-status. If UnitId changes, the search index offset will be reset. Otherwise, it will continue from where it left off. This command can be used as either a Fact or an Action. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_find_status_remote(UnitId: UnitId,Value: int,):
    """
 Find objects owned by the focus player for direct targeting. Set sn-focus-player-number before using this command. This is identical to up-find-remote, except it will consider the status value set by up-filter-status. If the focus or UnitId changes, the search index offset will be reset. Otherwise, it will continue from where it left off. This command can be used as either a Fact or an Action. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_full_reset_search():
    """
 Reset all search and filter states for direct unit targeting. This command simply combines (up-reset-search 1 1 1 1) and (up-reset-filters) for rule size optimization. 
"""
    pass
def up_gaia_type_count(Resource: Resource,compareOp: compareOp,Value: int,):
    """
 Check the current sighted resource count from gaia. This command may be relatively slow, since it must check the status of all discovered resources within the requested subset (food, wood, stone, or gold). 
:param Resource: Range: 0 to 3, or theClassIdof the resource.
 A gatherable resource type. Note: using the ClassId is not valid for most (all?) of the 1.0c commands that use this parameter. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_gaia_type_count_total(Resource: Resource,compareOp: compareOp,Value: int,):
    """
 Check the total sighted resource count from gaia. When checking food, wood, stone, or gold, this command operates very quickly. However, the required data does not exist for specific food types, including deer and sheep. As a fallback, it will redirect to the slower up-gaia-type-count, and the result will only reflect resources that still exist. 
:param Resource: Range: 0 to 3, or theClassIdof the resource.
 A gatherable resource type. Note: using the ClassId is not valid for most (all?) of the 1.0c commands that use this parameter. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_garrison(ObjectId: int,UnitId: UnitId,):
    """
 Garrison all units of the specified type into another object. The first parameter cannot be a class or a unit-line. my-unique-unit and my-elite-unique-unit can be used though, which will automatically get the UnitId of the unique unit or elite unique unit that the AI's civ can train from the castle. It must be a valid root object type id that can accept a garrison (battering-ram instead of battering-ram-line). DE requires "feudal-battering-ram" (ID 1258) instead of battering-ram. Objects tasked to garrison are prioritized in the order from newest to oldest trained/built. 
:param ObjectId: Range: A validUnitIdor a validBuildingId.
 AUnitIdor aBuildingId. See theObjects Tablefor details. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
"""
    pass
def up_gather_inside(BuildingId: BuildingId,Option: int,):
    """
 Set all existing buildings of a specific type to hold units inside. If the Option parameter is set to 1, both trained and garrisoned units will be held inside the building. If set to -1, only garrisoned units will be held inside. Otherwise, if set to 0, all units will be released as usual. 
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
:param Option: Range: varies
 A value that determines different ways the command will work. Here is a list:  
"""
    pass
def up_get_attacker_class(ThreatSource: int,):
    """
 Get the class of the last enemy object to trigger town-under-attack. 
:param ThreatSource: Range: A goal ID between 1 and 16000 to store the source class.
 Stores the class of the enemy object that triggered the most recent attack threat event. 
"""
    pass
def up_get_cost_delta(OutputGoalId: int,):
    """
 Get the difference between player resources and the current cost data, and store this difference in four consecutive goals in the order of food, wood, stone, and gold. The calculation is the current stockpile minus the current amount stored in the four cost goals from the most recentup-setup-cost-datacommand. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_event(EventId: int,Value: int,):
    """
 Get the value of a scenario trigger event. 
:param EventId: Range: 0 to 255.
 The event ID. The only valid events are AI Script Goal effects and AI Signal conditions in scenario triggers. The ID matches the number of the chosen option from the trigger condition/effect. Note: the "AI Trigger 256" option in the AI Script Goal effect cannot be detected by AIs. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_get_fact(FactId: FactId,FactParameter: int,OutputGoalId: int,):
    """
 Read a fact for my-player-number into a goal. This command can be used as either a fact or an action. 
:param FactId: Range: 0 to 54.
 Selects the fact type to be checked and stored in a goal. Each FactId corresponds to a normal Fact except for cc-gaia-type-count. Several FactIds can only be used withup-get-factor with my-player-number as the player number in commands likeup-get-player-fact. See the values list below for information. Also, all commands that use FactId also includeFactParameter. See the values list below for the expected type of parameter. 
:param FactParameter: Range: An appropriate parameter for the fact, or 0 if not required.
 A parameter for the fact to be used in up-get-fact-* commands. This often matches the first parameter in a fact command, but if theFactIdcan be used with any player number, then this is usually a validFactParameterinstead. If no extra parameter is needed, this is usually 0. See the FactId page to determine what should be used for the FactParameter. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_fact_max(PlayerNumber: PlayerNumber,FactId: FactId,FactParameter: int,OutputGoalId: int,):
    """
 Read the maximum value of the facts for specific players into a goal. This command can be used as either a fact or an action. The matching player will be set to the this-any-* rule variable for use in the action section of the rule, even if up-get-fact-max is used as an action. The Action allows only the "any" wildcard parameters forPlayerNumber, such as any-ally or any-enemy. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param FactId: Range: 0 to 54.
 Selects the fact type to be checked and stored in a goal. Each FactId corresponds to a normal Fact except for cc-gaia-type-count. Several FactIds can only be used withup-get-factor with my-player-number as the player number in commands likeup-get-player-fact. See the values list below for information. Also, all commands that use FactId also includeFactParameter. See the values list below for the expected type of parameter. 
:param FactParameter: Range: An appropriate parameter for the fact, or 0 if not required.
 A parameter for the fact to be used in up-get-fact-* commands. This often matches the first parameter in a fact command, but if theFactIdcan be used with any player number, then this is usually a validFactParameterinstead. If no extra parameter is needed, this is usually 0. See the FactId page to determine what should be used for the FactParameter. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_fact_min(PlayerNumber: PlayerNumber,FactId: FactId,FactParameter: int,OutputGoalId: int,):
    """
 Read the minimum value of the facts for specific players into a goal. This command can be used as either a fact or an action. The matching player will be set to the this-any-* wildcard player id for use in the action section of the rule, even if up-get-fact-min is used as an action. The Action allows only the "any" wildcard parameters forPlayerNumber, such as any-ally or any-enemy. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param FactId: Range: 0 to 54.
 Selects the fact type to be checked and stored in a goal. Each FactId corresponds to a normal Fact except for cc-gaia-type-count. Several FactIds can only be used withup-get-factor with my-player-number as the player number in commands likeup-get-player-fact. See the values list below for information. Also, all commands that use FactId also includeFactParameter. See the values list below for the expected type of parameter. 
:param FactParameter: Range: An appropriate parameter for the fact, or 0 if not required.
 A parameter for the fact to be used in up-get-fact-* commands. This often matches the first parameter in a fact command, but if theFactIdcan be used with any player number, then this is usually a validFactParameterinstead. If no extra parameter is needed, this is usually 0. See the FactId page to determine what should be used for the FactParameter. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_fact_sum(PlayerNumber: PlayerNumber,FactId: FactId,FactParameter: int,OutputGoalId: int,):
    """
 Read the sum of facts for specific players into a goal. This command can be used as either a fact or an action. The action only allows the "any" wildcard parameters forPlayerNumber, such as any-ally or any-enemy. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param FactId: Range: 0 to 54.
 Selects the fact type to be checked and stored in a goal. Each FactId corresponds to a normal Fact except for cc-gaia-type-count. Several FactIds can only be used withup-get-factor with my-player-number as the player number in commands likeup-get-player-fact. See the values list below for information. Also, all commands that use FactId also includeFactParameter. See the values list below for the expected type of parameter. 
:param FactParameter: Range: An appropriate parameter for the fact, or 0 if not required.
 A parameter for the fact to be used in up-get-fact-* commands. This often matches the first parameter in a fact command, but if theFactIdcan be used with any player number, then this is usually a validFactParameterinstead. If no extra parameter is needed, this is usually 0. See the FactId page to determine what should be used for the FactParameter. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_focus_fact(FactId: FactId,FactParameter: int,OutputGoalId: int,):
    """
 Read a fact for the focus-player into a goal. This command can be used as either a fact or an action. 
:param FactId: Range: 0 to 54.
 Selects the fact type to be checked and stored in a goal. Each FactId corresponds to a normal Fact except for cc-gaia-type-count. Several FactIds can only be used withup-get-factor with my-player-number as the player number in commands likeup-get-player-fact. See the values list below for information. Also, all commands that use FactId also includeFactParameter. See the values list below for the expected type of parameter. 
:param FactParameter: Range: An appropriate parameter for the fact, or 0 if not required.
 A parameter for the fact to be used in up-get-fact-* commands. This often matches the first parameter in a fact command, but if theFactIdcan be used with any player number, then this is usually a validFactParameterinstead. If no extra parameter is needed, this is usually 0. See the FactId page to determine what should be used for the FactParameter. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_group_size(GroupId: int,OutputGoalId: int,):
    """
 Get the current number of units in a search group. 
:param GroupId: Range: 0 to 19.
 An ID assigned to a group of objects, similar to Ctrl groups human players can use. In UP, only GroupId's 0 through 9 could be used. However, in DE, GroupId's 0 through 19 work. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_guard_state(OutputGoalId: int,):
    """
 Get the guard state into 4 consecutive extended goals. The guard state is defined in custom random maps using the guard_state command, which enables a resource trickle and/or a defeat condition depending on whether a certain unit type is killed. The goals will be filled with data in the following order: TypeId, ResourceType, ResourceDelta, GuardFlags. Please use up-compare-flag to check the guard flags (seeGuardFlagfor a list of guard flags). If guard-flag-resource is set in GuardFlags, then ResourceDelta/100 will slowly be added to ResourceType as long as TypeId objects remain. If both guard-flag-resource and guard-flag-inverse are set, then the resources will be added only when there are no TypeId objects left. If the guard-flag-victory condition is set, the AI will be defeated if no TypeId objects remain. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_indirect_goal(GoalId: int,OutputGoalId: int,):
    """
 Get the value of a goal indirectly by reference. 
:param GoalId: Range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE.
 A valid goal ID. A goal ID can either be a number within the range below or a defined constant set to a number within the range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_object_data(ObjectData: ObjectData,OutputGoalId: int,):
    """
 Get specific information about the selected target object. This command can be used as either a Fact or an Action. 
:param ObjectData: Range: a valid ObjectData ID. -1 can only be used with up-remove-objects.
 Data information about an object. This information is gathered from the unit's current stats, including any techs that have been researched or civ bonuses that affect the unit. Important Note:some object data is not available for units marching in formation when usingup-get-object-dataorup-object-data: object-data-action, object-data-order, object-data-target, and object-data-target-id. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_object_target_data(ObjectData: ObjectData,OutputGoalId: int,):
    """
 Get specific information about the target object's target. This command can be used as either a Fact or an Action. 
:param ObjectData: Range: a valid ObjectData ID. -1 can only be used with up-remove-objects.
 Data information about an object. This information is gathered from the unit's current stats, including any techs that have been researched or civ bonuses that affect the unit. Important Note:some object data is not available for units marching in formation when usingup-get-object-dataorup-object-data: object-data-action, object-data-order, object-data-target, and object-data-target-id. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_object_type_data(TypeId: int,ObjectData: ObjectData,OutputGoalId: int,):
    """
 Get generic information about an object type. This can be expensive, so please consider performance. 
:param TypeId: Range: A validObjectIdor one of the object line wildcard parameters.
 The type of object. This can be either the object name or an object line ID. See theObjects Tablefor a list of object names and object line wildcard parameters. 
:param ObjectData: Range: a valid ObjectData ID. -1 can only be used with up-remove-objects.
 Data information about an object. This information is gathered from the unit's current stats, including any techs that have been researched or civ bonuses that affect the unit. Important Note:some object data is not available for units marching in formation when usingup-get-object-dataorup-object-data: object-data-action, object-data-order, object-data-target, and object-data-target-id. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_path_distance(Point: int,Option: int,OutputGoalId: int,):
    """
 Get the distance from the target object to a specified point goal pair. This will return 65535 if the point is unreachable. Set the Option parameter to 1 to require an open destination tile to find the path distance toward or 0 to allow for a few tiles of separation to find a reachable open tile. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
:param Option: Range: varies
 A value that determines different ways the command will work. Here is a list:  
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_player_color(PlayerNumber: PlayerNumber,ColorId: int,):
    """
 Get the color id and store the name in the internal butter. ColorId will range from 1 to 8. The buffer can be referenced by the chat-data commands using %s instead of %d with c: 7031232 (7031232 cannot be stored in a defconst). This buffer is shared by all AIs, so please store data before using it in a rule pass. The action only allows for exact player numbers, "my-player-number", or "this-any" rule variables forPlayerNumber, such as this-any-ally or this-any-enemy. It does not allow "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param ColorId: Range: 1 to 8.
 A color number ID. These colors correspond with the player number color where 1 = Blue, 2 = Red, etc. Each color will always return the same color ID, even if it doesn't match the player number. If player 4 is Blue, player 4's ColorId will still be 1. 
"""
    pass
def up_get_player_fact(PlayerNumber: PlayerNumber,FactId: FactId,FactParameter: int,OutputGoalId: int,):
    """
 Read a fact for a specific player into a goal. This command can be used as either a fact or an action. For better performance, please use one of the more direct commands from the up-get-fact series whenever possible. The action only allows for exact player numbers, "my-player-number", or "this-any" rule variables forPlayerNumber, such as this-any-ally or this-any-enemy. It does not allow "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param FactId: Range: 0 to 54.
 Selects the fact type to be checked and stored in a goal. Each FactId corresponds to a normal Fact except for cc-gaia-type-count. Several FactIds can only be used withup-get-factor with my-player-number as the player number in commands likeup-get-player-fact. See the values list below for information. Also, all commands that use FactId also includeFactParameter. See the values list below for the expected type of parameter. 
:param FactParameter: Range: An appropriate parameter for the fact, or 0 if not required.
 A parameter for the fact to be used in up-get-fact-* commands. This often matches the first parameter in a fact command, but if theFactIdcan be used with any player number, then this is usually a validFactParameterinstead. If no extra parameter is needed, this is usually 0. See the FactId page to determine what should be used for the FactParameter. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_point(PositionType: PositionType,Point: int,):
    """
 Read a specific (x,y) position into an extended goal pair. This command writes to 2 consecutive goals and requires an extended goal pair between 41 and 15998. If it fails to get a valid position, it will return (-1,-1). 
:param PositionType: Range: 0 to 13.
 The position type, a predefined position that can be stored in a point. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
"""
    pass
def up_get_point_contains(Point: int,OutputGoalId: int,ObjectId: int,):
    """
 Get the id if an object exists at a point goal pair position. Set Point to 0 to use the point that is stored by up-set-target-point. Please note that when used with all-units-class (-1), this may capture unexpected objects like birds flying over a tile, terrain plants, etc. This command can be used as either a Fact or an Action. Also, this action will work whether the point has been explored or not. Therefore, in AI tournamentsup-point-exploredmust be used as a condition in every rule where this command is used. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
:param ObjectId: Range: A validUnitIdor a validBuildingId.
 AUnitIdor aBuildingId. See theObjects Tablefor details. 
"""
    pass
def up_get_point_distance(Point1:Point,Point2:Point,OutputGoalId: int,):
    """
 Get the distance between two point goal pairs. Set Point2 to 0 to use the point that is stored by up-set-target-point. This command does not bound the points to the map, meaning you can use it for more general calculations. It simply calculates the distance formula. When calculating the distance between two precise points, it will calculate a precise distance, where the distance is 100 times larger than the actual distance. 
:param Point1: is a point object
:param Point2: is a point object
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_point_elevation(Point: int,OutputGoalId: int,):
    """
 Get the elevation for a tile with a point goal pair. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_point_terrain(Point: int,Terrain: Terrain,):
    """
 Get the terrain id at a specific point goal pair position. Set Point to 0 to use the point that is stored by up-set-target-point. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
:param Terrain: Range: 0 to 41.
 The name of a terrain or the ID number assigned to that terrain. Notes about terrain changes apply primarily to the WololoKingdoms version of the game. Terrain changes might be different in AoE2:DE and the HD expansions on Steam. 
"""
    pass
def up_get_point_zone(Point: int,OutputGoalId: int,):
    """
 Get the zone for a tile with a point goal pair. Zone ids may differ if you have no villagers. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_precise_time(OptionGoalId: int,OutputGoalId: int,):
    """
 Get a system timestamp or the elapsed time into a goal. The OptionGoalId parameter determines whether a system timestamp is retrieved or the elapsed time since a previous system timestamp is retrieved. To get a system timestamp, use 0 for the OptionGoalId parameter. To get the elapsed time since a timestamp, use aGoalIdthat is currently storing a system timestamp for the OptionGoalId parameter. The system timestamp or elapsed time will be stored in the OutputGoal. 
:param OptionGoalId: Range: a goal ID to control how the command works
 A goal ID, whose values controls how a command works. Here's how it affects each command:  
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_projectile_player(ProjectileType: ProjectileType,OutputGoalId: int,):
    """
 Get the enemy player that last attacked with a specific type of projectile. 
:param ProjectileType: Range: 0 to 7.
 The source of the projectile to check. Note that the actualObjectIdof the projectile does not work. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_rule_id(GoalId: int,):
    """
 Get the zero-based id for the current rule within the rule set. This id can be used with up-jump-direct to precisely control jump destinations. 
:param GoalId: Range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE.
 A valid goal ID. A goal ID can either be a number within the range below or a defined constant set to a number within the range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE. 
"""
    pass
def up_get_search_state(OutputGoalId: int,):
    """
 Get the search state into 4 consecutive extended goals. The goals will be filled with data in the following order: current local search total, last local search count, current remote search total, last remote search count. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_shared_goal(SharedGoalId: int,Value: int,):
    """
 Get the value of a shared goal. 
:param SharedGoalId: Range: 1 to 256.
 A goal that is shared among computer players. It is to be used only when all computer players are on the same team. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_get_signal(SignalId: int,Value: int,):
    """
 Get the value of a scenario trigger signal. 
:param SignalId: Range: 0 to 255.
 The Id of a scenario trigger signal. This if effectively the same asEventIdsince the only types of events are trigger signals. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_get_target_fact(FactId: FactId,FactParameter: int,OutputGoalId: int,):
    """
 Read a fact for the target-player into a goal. This command can be used as either a fact or an action. 
:param FactId: Range: 0 to 54.
 Selects the fact type to be checked and stored in a goal. Each FactId corresponds to a normal Fact except for cc-gaia-type-count. Several FactIds can only be used withup-get-factor with my-player-number as the player number in commands likeup-get-player-fact. See the values list below for information. Also, all commands that use FactId also includeFactParameter. See the values list below for the expected type of parameter. 
:param FactParameter: Range: An appropriate parameter for the fact, or 0 if not required.
 A parameter for the fact to be used in up-get-fact-* commands. This often matches the first parameter in a fact command, but if theFactIdcan be used with any player number, then this is usually a validFactParameterinstead. If no extra parameter is needed, this is usually 0. See the FactId page to determine what should be used for the FactParameter. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_threat_data(ThreatTime: int,ThreatPlayer: int,ThreatSource: int,ThreatTarget: int,):
    """
 Get the elapsed time, player, source, and target of the last threat and store them in the four specified goals. This command returns the absolute, most recent attack information before the rule pass begins. If the last attack event was from a p2 archer against one of your villagers, you'll get "time, 2, 900, 904" in return (900 = archery-class, 904 = villager-class). In an epic battle, it would become relatively useless in determining what is going on. 
:param ThreatTime: Range: A goal ID between 1 and 16000 to store the elapsed time.
 Stores the elapsed time in milliseconds since the most recent attack threat event. 
:param ThreatPlayer: Range: A goal ID between 1 and 16000 to store the player number.
 Stores the enemy player who triggered the most recent attack threat event. 
:param ThreatSource: Range: A goal ID between 1 and 16000 to store the source class.
 Stores the class of the enemy object that triggered the most recent attack threat event. 
:param ThreatTarget: Range: A goal ID between 1 and 16000 to store the elapsed time.
 Stores the class of the object that the enemy attacked in the most recent attack threat event. 
"""
    pass
def up_get_timer(TimerId: int,OutputGoalId: int,):
    """
 Get the trigger time for a timer in milliseconds. 
:param TimerId: Range: 1 to 50.
 The ID of a timer or a defconst representing a timer. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_treaty_data(OutputGoalId: int,):
    """
 DE only. Stores the remaining treaty time in seconds into a goal. Treaty time is the amount of time left in treaty games where players cannot attack each other. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_upgrade_id(PlayerNumber: PlayerNumber,Option: int,TypeGoalId,OutputGoalId: int,):
    """
 Get the upgrade type id for an object into a goal. Set the Option parameter to 1 to get the current type id for counting, otherwise 0. The action only allows for exact player numbers, "my-player-number", or "this-any" rule variables forPlayerNumber, such as this-any-ally or this-any-enemy. It does not allow "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param Option: Range: varies
 A value that determines different ways the command will work. Here is a list:  
:param TypeGoalId: NOT_DEFINED
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_get_victory_data(VictoryPlayer: int,VictoryType: int,VictoryTime: int,):
    """
 Get standard victory status information into the provided goals. 
:param VictoryPlayer: Range: AGoalId.
 AGoalIdto store the player number of the player approaching victory, or 0 if invalid. 
:param VictoryType: Range: AGoalId. These range from 1 to 16000.
 AGoalIdthat stores the type of victory approaching. Stores one of the following: relic, wonder, monument, or 0 if invalid. 
:param VictoryTime: Range: AGoalId.
 AGoalIdto store the time remaining until victory. The stored value is 10 * the number of game years remaining until victory from relics, wonders, or captured monuments. 
"""
    pass
def up_get_victory_limit(OutputGoalId: int,):
    """
 Get the time or score victory limit into the provided goal. 
:param OutputGoalId: Range: a valid GoalId, max range of GoalId is 1 to 16000.
 A goal to store the data output of a command. Forup-get-cost-delta,up-get-guard-state, andup-get-search-stateonly, this goal is the first of four consecutive goals that will store the data output, and only goal IDs 41 through 15997 can be used with the OutputGoalId parameter. 
"""
    pass
def up_group_size(GroupId: int,compareOp: compareOp,Value: int,):
    """
 Check the current number of units in a search group. 
:param GroupId: Range: 0 to 19.
 An ID assigned to a group of objects, similar to Ctrl groups human players can use. In UP, only GroupId's 0 through 9 could be used. However, in DE, GroupId's 0 through 19 work. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_guard_unit(ObjectId: int,UnitId: UnitId,):
    """
 Set a single unit of a specific type to protect a random instance of another, as long as they are on the same continent. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can be used for the UnitId, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. 
:param ObjectId: Range: A validUnitIdor a validBuildingId.
 AUnitIdor aBuildingId. See theObjects Tablefor details. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
"""
    pass
def up_idle_unit_count(IdleType: IdleType,compareOp: compareOp,Value: int,):
    """
 Check the number of idle units for the specified type. 
:param IdleType: Range: 0 to 3.
 The type of idle unit. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_jump_direct(RuleId: int,):
    """
 Jump directly within the current rule set. Please ensure that the rule you are jumping to actually exists. You can use up-get-rule-id to get a valid rule id to jump to. With this action, you can either decrease rules per pass with intelligent skips, or greatly increase it with loops. Please consider game performance. 
:param RuleId: Range: A valid zero-based rule id, theoretically has a range of 0 to 32767.
 The rule number id to jump to. Please do not attempt to jump to a negative rule id. 
"""
    pass
def up_jump_dynamic(RuleDelta: int,):
    """
 Jump dynamically within the current rule set. Never use this command where #load blocks may make your jump target unreliable. Please ensure that the rule you are jumping to actually exists. With this action, you can either decrease rules per pass with intelligent skips, or greatly increase it with loops. Please consider game performance. 
:param RuleDelta: Range: The number of rules to jump, theoretically will likely have a range of -32768 to 32767.
 The number of rules to jump. Positive values will jump forward, while negative values will jump backward. 
"""
    pass
def up_jump_rule(RuleDelta: int,):
    """
 Jump forward or backward within the current rule set. Never use this command where #load blocks may make your jump target unreliable. Please ensure that the rule you are jumping to actually exists. With this action, you can either decrease rules per pass with intelligent skips, or greatly increase it with loops. Please consider game performance. 
:param RuleDelta: Range: The number of rules to jump, theoretically will likely have a range of -32768 to 32767.
 The number of rules to jump. Positive values will jump forward, while negative values will jump backward. 
"""
    pass
def up_lerp_percent(Point1:Point,Point2:Point,Percent: int,):
    """
 Interpolate a point by percentage between two point goal pairs and store the new point in Point1. The Percent parameter specifies the percentage of the distance between the two points that the new point will move toward or away from Point1 to Point2. If Value is positive, the new point will move closer to Point2. If Value is negative, the new point will move further away from Point2. Set Point2 to 0 to use the point that is stored by up-set-target-point. 
:param Point1: is a point object
:param Point2: is a point object
:param Percent: Range: -32768 to 32767.
 A percentage, i.e. a decimal multiplied by 100 
"""
    pass
def up_lerp_tiles(Point1:Point,Point2:Point,Value: int,):
    """
 Interpolate a point by tiles between two point goal pairs and store the new point in Point1. The Value parameter specifies how many tiles the new point will move toward or away from Point1 to Point2. If Value is positive, the new point will move closer to Point2. If Value is negative, the new point will move further away from Point2. Set Point2 to 0 to use the point that is stored by up-set-target-point. Note: It is possible for the new point to be outside the bounds of the map which can cause several issues. Therefore, it is wise to useup-bound-pointafterward to ensure that you always have a valid point location. 
:param Point1: is a point object
:param Point2: is a point object
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_log_data(Option: int,String: str,Value: int,):
    pass
def up_modify_escrow(Resource: Resource,mathOp: mathOp,Value: int,):
    """
 Perform math operations to adjust escrowed resources. 
:param Resource: Range: 0 to 3, or theClassIdof the resource.
 A gatherable resource type. Note: using the ClassId is not valid for most (all?) of the 1.0c commands that use this parameter. 
:param mathOp: Range: 0 to 35.
 Performs a math operation between two parameters in the command. These two parameters will be called operands in the descriptions in the Operator Types section below, after the Examples section. The prefix (c:, g:, or s:) determines the expected type of parameter for the second operand. The following examples show how each math operation works with actual numbers. There are identical versions of each operation for constants (c:), goals (g:), and strategic numbers (s:). c:=, g:=, and s:= The value of gl-example will be set to 7. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)) c:+, g:+, and s:+ Calculation: 7 + 2 = 9The value of gl-example will be increased by 2. The end result is that gl-example in both examples will equal 9. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:+ 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:+ gl-temp)) c:-, g:-, and s:- Calculation: 7 - 2 = 5The value of gl-example will be decreased by 2. The end result is that gl-example in both examples will equal 5. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:- 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:- gl-temp)) c:*, g:*, and s:* Calculation: 7 * 2 = 14The value of gl-example will be multiplied by 2. The end result is that gl-example in both examples will equal 14. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:* 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:* gl-temp)) c:/, g:/, and s:/ Calculation: 7 / 2 = 4 (rounded because AI engine doesn't use decimals)The value of gl-example will be divided by 2 (and rounded to the nearest integer). The end result is that gl-example in both examples will equal 4. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:/ 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:/ gl-temp)) c:z/, g:z/, and s:z/ Calculation: 7 z/ 2 = 3 (7 divided by 2 and truncated (rounded down) using integer division rules, where the remainder is truncated instead of rounded).The value of gl-example will be divided by 2, rounded down. The end result is that gl-example in both examples will equal 3. This operation is sometimes referred to as integer division, hence the use of "z," a letter which mathematicians sometimes use to refer to the set of all integer numbers. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:z/ 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:z/ gl-temp)) c:mod, g:mod, and s:mod Calculation: 7 % 2 = 1The value of gl-example in both examples will equal 1. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:mod 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:mod gl-temp)) c:min, g:min, and s:min Calculation: min(7, 2) = 2If the given value is smaller than the value currently stored in gl-example, then gl-example will be set to that smaller value. Otherwise, gl-example will remain unchanged. The end result is that gl-example in both examples will equal 2. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:min 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:min gl-temp)) c:max, g:max, and s:max Calculation: max(7, 2) = 7If the given value is larger than the value currently stored in gl-example, then gl-example will be set to that larger value. Otherwise, gl-example will remain unchanged. The end result is that gl-example in both examples will equal 7. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:max 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:max gl-temp)) c:neg, g:neg, and s:neg Calculation: 7 * -1 = -7Two examples are given since the example with c:neg is rather trivial. The given number will be stored in gl-example with the opposite positive/negative sign. The end result is that gl-example in both examples will equal -7. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:neg 7))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-temp c:= 7)(up-modify-goal gl-example g:neg gl-temp)) c:%*, g:%*, and s:%* Calculation: 29% of 10 = 2 or 10 * 29 / 100 = 2.9, truncated to 2.The given percent of gl-example will be stored in gl-example. In other words, gl-example is multiplied by the given value and divided by 100. The result is truncated (rounded down) if there is a remainder. The end result is that gl-example in both examples will equal 2. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 10)(up-modify-goal gl-example c:%* 29))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 10)(up-modify-goal gl-temp c:= 29)(up-modify-goal gl-example g:%* gl-temp)) If you want your result rounded, rather than truncated, you can accomplish this in two operations using the multiplication and division operators. The end result is that gl-example in both examples will equal 3. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 10)(up-modify-goal gl-example c:* 29)(up-modify-goal gl-example c:/ 100))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 10)(up-modify-goal gl-temp c:= 29)(up-modify-goal gl-example g:* gl-temp)(up-modify-goal gl-example c:/ 100)) c:%/, g:%/, and s:%/ Calculation: 7 out of 9 = 77% or 7 * 100 / 9 = 77.777777, truncated to 77.The value currently stored in gl-example will be multiplied by 100 before dividing by the given value, effectively converting the result to a percent, with any decimal result truncated (rounded down) rather than rounded. The end result is that gl-example in both examples will equal 77. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:%/ 9))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 9)(up-modify-goal gl-example g:%/ gl-temp)) If you want your result rounded, rather than truncated, you can accomplish this in two operations using the multiplication and division operators. The end result is that gl-example in both examples will equal 78. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:* 100)(up-modify-goal gl-example c:/ 9))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:* 100)(up-modify-goal gl-temp c:= 9)(up-modify-goal gl-example g:/ gl-temp))  
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_modify_flag(GoalId: int,mathOp: mathOp,Flag: int,):
    """
 Modify a bitwise flag on the value stored in a goal variable. Flags allow multiple states to be stored in a single value by using powers of 2 (1, 2, 4, 8, 16, etc.). The only ops allowed are [cgs]:+ to append a flag and [cgs]:- to remove a flag. 
:param GoalId: Range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE.
 A valid goal ID. A goal ID can either be a number within the range below or a defined constant set to a number within the range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE. 
:param mathOp: Range: 0 to 35.
 Performs a math operation between two parameters in the command. These two parameters will be called operands in the descriptions in the Operator Types section below, after the Examples section. The prefix (c:, g:, or s:) determines the expected type of parameter for the second operand. The following examples show how each math operation works with actual numbers. There are identical versions of each operation for constants (c:), goals (g:), and strategic numbers (s:). c:=, g:=, and s:= The value of gl-example will be set to 7. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)) c:+, g:+, and s:+ Calculation: 7 + 2 = 9The value of gl-example will be increased by 2. The end result is that gl-example in both examples will equal 9. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:+ 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:+ gl-temp)) c:-, g:-, and s:- Calculation: 7 - 2 = 5The value of gl-example will be decreased by 2. The end result is that gl-example in both examples will equal 5. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:- 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:- gl-temp)) c:*, g:*, and s:* Calculation: 7 * 2 = 14The value of gl-example will be multiplied by 2. The end result is that gl-example in both examples will equal 14. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:* 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:* gl-temp)) c:/, g:/, and s:/ Calculation: 7 / 2 = 4 (rounded because AI engine doesn't use decimals)The value of gl-example will be divided by 2 (and rounded to the nearest integer). The end result is that gl-example in both examples will equal 4. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:/ 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:/ gl-temp)) c:z/, g:z/, and s:z/ Calculation: 7 z/ 2 = 3 (7 divided by 2 and truncated (rounded down) using integer division rules, where the remainder is truncated instead of rounded).The value of gl-example will be divided by 2, rounded down. The end result is that gl-example in both examples will equal 3. This operation is sometimes referred to as integer division, hence the use of "z," a letter which mathematicians sometimes use to refer to the set of all integer numbers. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:z/ 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:z/ gl-temp)) c:mod, g:mod, and s:mod Calculation: 7 % 2 = 1The value of gl-example in both examples will equal 1. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:mod 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:mod gl-temp)) c:min, g:min, and s:min Calculation: min(7, 2) = 2If the given value is smaller than the value currently stored in gl-example, then gl-example will be set to that smaller value. Otherwise, gl-example will remain unchanged. The end result is that gl-example in both examples will equal 2. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:min 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:min gl-temp)) c:max, g:max, and s:max Calculation: max(7, 2) = 7If the given value is larger than the value currently stored in gl-example, then gl-example will be set to that larger value. Otherwise, gl-example will remain unchanged. The end result is that gl-example in both examples will equal 7. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:max 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:max gl-temp)) c:neg, g:neg, and s:neg Calculation: 7 * -1 = -7Two examples are given since the example with c:neg is rather trivial. The given number will be stored in gl-example with the opposite positive/negative sign. The end result is that gl-example in both examples will equal -7. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:neg 7))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-temp c:= 7)(up-modify-goal gl-example g:neg gl-temp)) c:%*, g:%*, and s:%* Calculation: 29% of 10 = 2 or 10 * 29 / 100 = 2.9, truncated to 2.The given percent of gl-example will be stored in gl-example. In other words, gl-example is multiplied by the given value and divided by 100. The result is truncated (rounded down) if there is a remainder. The end result is that gl-example in both examples will equal 2. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 10)(up-modify-goal gl-example c:%* 29))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 10)(up-modify-goal gl-temp c:= 29)(up-modify-goal gl-example g:%* gl-temp)) If you want your result rounded, rather than truncated, you can accomplish this in two operations using the multiplication and division operators. The end result is that gl-example in both examples will equal 3. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 10)(up-modify-goal gl-example c:* 29)(up-modify-goal gl-example c:/ 100))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 10)(up-modify-goal gl-temp c:= 29)(up-modify-goal gl-example g:* gl-temp)(up-modify-goal gl-example c:/ 100)) c:%/, g:%/, and s:%/ Calculation: 7 out of 9 = 77% or 7 * 100 / 9 = 77.777777, truncated to 77.The value currently stored in gl-example will be multiplied by 100 before dividing by the given value, effectively converting the result to a percent, with any decimal result truncated (rounded down) rather than rounded. The end result is that gl-example in both examples will equal 77. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:%/ 9))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 9)(up-modify-goal gl-example g:%/ gl-temp)) If you want your result rounded, rather than truncated, you can accomplish this in two operations using the multiplication and division operators. The end result is that gl-example in both examples will equal 78. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:* 100)(up-modify-goal gl-example c:/ 9))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:* 100)(up-modify-goal gl-temp c:= 9)(up-modify-goal gl-example g:/ gl-temp))  
:param Flag: Range: A valid flag.
 A flag that belongs to the given goal. A flag has two states: appended or removed. See the list of commands that use this parameter for more info. 
"""
    pass
def up_modify_goal(GoalId: int,mathOp: mathOp,Value: int,):
    """
 Perform math operations on the value stored in a goal variable. This command can be used as either a Fact or an Action, meaning the command can appear before the "=>" in the rule or after it. The behavior of the command is identical, regardless of whether it is used as a Fact or as an Action. This command is a much more flexible version of theset-goalcommand, which only allows you to set a goal to a specific value. up-modify-goal allows you to add, subtract, multiply, divide, find remainders, find percentages, find min and max values, and do other mathematical operations, either with specific numbers or with the values currently stored in a goal or strategic number. See themathOppage for a full list of all the operations available, along with in-depth examples of each operation. 
:param GoalId: Range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE.
 A valid goal ID. A goal ID can either be a number within the range below or a defined constant set to a number within the range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE. 
:param mathOp: Range: 0 to 35.
 Performs a math operation between two parameters in the command. These two parameters will be called operands in the descriptions in the Operator Types section below, after the Examples section. The prefix (c:, g:, or s:) determines the expected type of parameter for the second operand. The following examples show how each math operation works with actual numbers. There are identical versions of each operation for constants (c:), goals (g:), and strategic numbers (s:). c:=, g:=, and s:= The value of gl-example will be set to 7. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)) c:+, g:+, and s:+ Calculation: 7 + 2 = 9The value of gl-example will be increased by 2. The end result is that gl-example in both examples will equal 9. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:+ 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:+ gl-temp)) c:-, g:-, and s:- Calculation: 7 - 2 = 5The value of gl-example will be decreased by 2. The end result is that gl-example in both examples will equal 5. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:- 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:- gl-temp)) c:*, g:*, and s:* Calculation: 7 * 2 = 14The value of gl-example will be multiplied by 2. The end result is that gl-example in both examples will equal 14. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:* 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:* gl-temp)) c:/, g:/, and s:/ Calculation: 7 / 2 = 4 (rounded because AI engine doesn't use decimals)The value of gl-example will be divided by 2 (and rounded to the nearest integer). The end result is that gl-example in both examples will equal 4. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:/ 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:/ gl-temp)) c:z/, g:z/, and s:z/ Calculation: 7 z/ 2 = 3 (7 divided by 2 and truncated (rounded down) using integer division rules, where the remainder is truncated instead of rounded).The value of gl-example will be divided by 2, rounded down. The end result is that gl-example in both examples will equal 3. This operation is sometimes referred to as integer division, hence the use of "z," a letter which mathematicians sometimes use to refer to the set of all integer numbers. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:z/ 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:z/ gl-temp)) c:mod, g:mod, and s:mod Calculation: 7 % 2 = 1The value of gl-example in both examples will equal 1. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:mod 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:mod gl-temp)) c:min, g:min, and s:min Calculation: min(7, 2) = 2If the given value is smaller than the value currently stored in gl-example, then gl-example will be set to that smaller value. Otherwise, gl-example will remain unchanged. The end result is that gl-example in both examples will equal 2. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:min 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:min gl-temp)) c:max, g:max, and s:max Calculation: max(7, 2) = 7If the given value is larger than the value currently stored in gl-example, then gl-example will be set to that larger value. Otherwise, gl-example will remain unchanged. The end result is that gl-example in both examples will equal 7. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:max 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:max gl-temp)) c:neg, g:neg, and s:neg Calculation: 7 * -1 = -7Two examples are given since the example with c:neg is rather trivial. The given number will be stored in gl-example with the opposite positive/negative sign. The end result is that gl-example in both examples will equal -7. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:neg 7))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-temp c:= 7)(up-modify-goal gl-example g:neg gl-temp)) c:%*, g:%*, and s:%* Calculation: 29% of 10 = 2 or 10 * 29 / 100 = 2.9, truncated to 2.The given percent of gl-example will be stored in gl-example. In other words, gl-example is multiplied by the given value and divided by 100. The result is truncated (rounded down) if there is a remainder. The end result is that gl-example in both examples will equal 2. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 10)(up-modify-goal gl-example c:%* 29))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 10)(up-modify-goal gl-temp c:= 29)(up-modify-goal gl-example g:%* gl-temp)) If you want your result rounded, rather than truncated, you can accomplish this in two operations using the multiplication and division operators. The end result is that gl-example in both examples will equal 3. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 10)(up-modify-goal gl-example c:* 29)(up-modify-goal gl-example c:/ 100))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 10)(up-modify-goal gl-temp c:= 29)(up-modify-goal gl-example g:* gl-temp)(up-modify-goal gl-example c:/ 100)) c:%/, g:%/, and s:%/ Calculation: 7 out of 9 = 77% or 7 * 100 / 9 = 77.777777, truncated to 77.The value currently stored in gl-example will be multiplied by 100 before dividing by the given value, effectively converting the result to a percent, with any decimal result truncated (rounded down) rather than rounded. The end result is that gl-example in both examples will equal 77. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:%/ 9))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 9)(up-modify-goal gl-example g:%/ gl-temp)) If you want your result rounded, rather than truncated, you can accomplish this in two operations using the multiplication and division operators. The end result is that gl-example in both examples will equal 78. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:* 100)(up-modify-goal gl-example c:/ 9))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:* 100)(up-modify-goal gl-temp c:= 9)(up-modify-goal gl-example g:/ gl-temp))  
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_modify_group_flag(Option: int,GroupId: int,):
    """
 Modify the ctrl group flag for units in a search group. You must manage the group flag carefully in order to avoid unexpected situations. Please remove the group flag before modifying a flagged search group. You can find units from a flagged search group using object-data-group-flag, which is set to the group id. Do not modify the group flag of control groups owned by another player, because this will clear any control group settings that player has set, because up-modify-group-flag changes the object-data-group-flag data for that unit. When managing search groups that contain objects from other players, only useup-create-grouporup-set-group. 
:param Option: Range: varies
 A value that determines different ways the command will work. Here is a list:  
:param GroupId: Range: 0 to 19.
 An ID assigned to a group of objects, similar to Ctrl groups human players can use. In UP, only GroupId's 0 through 9 could be used. However, in DE, GroupId's 0 through 19 work. 
"""
    pass
def up_modify_sn(SnId: int,mathOp: mathOp,Value: int,):
    """
 Perform math operations on a strategic number. In DE, this command can be used as either a fact or an action, but it can only be used as an action in UP and WK. When used as a fact, it will modify the strategic number just like it would if it was used in the actions section of the rule. The only difference when up-modify-sn is used as a fact is that if it to modify the strategic number (because of an invalid strategic number ID or an invalid value), then the rest of the rule won't execute. 
:param SnId: Range: 0 to 511.
 A strategic number. SeeStrategic Numbersfor a list of usable strategic numbers and their descriptions. 
:param mathOp: Range: 0 to 35.
 Performs a math operation between two parameters in the command. These two parameters will be called operands in the descriptions in the Operator Types section below, after the Examples section. The prefix (c:, g:, or s:) determines the expected type of parameter for the second operand. The following examples show how each math operation works with actual numbers. There are identical versions of each operation for constants (c:), goals (g:), and strategic numbers (s:). c:=, g:=, and s:= The value of gl-example will be set to 7. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)) c:+, g:+, and s:+ Calculation: 7 + 2 = 9The value of gl-example will be increased by 2. The end result is that gl-example in both examples will equal 9. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:+ 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:+ gl-temp)) c:-, g:-, and s:- Calculation: 7 - 2 = 5The value of gl-example will be decreased by 2. The end result is that gl-example in both examples will equal 5. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:- 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:- gl-temp)) c:*, g:*, and s:* Calculation: 7 * 2 = 14The value of gl-example will be multiplied by 2. The end result is that gl-example in both examples will equal 14. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:* 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:* gl-temp)) c:/, g:/, and s:/ Calculation: 7 / 2 = 4 (rounded because AI engine doesn't use decimals)The value of gl-example will be divided by 2 (and rounded to the nearest integer). The end result is that gl-example in both examples will equal 4. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:/ 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:/ gl-temp)) c:z/, g:z/, and s:z/ Calculation: 7 z/ 2 = 3 (7 divided by 2 and truncated (rounded down) using integer division rules, where the remainder is truncated instead of rounded).The value of gl-example will be divided by 2, rounded down. The end result is that gl-example in both examples will equal 3. This operation is sometimes referred to as integer division, hence the use of "z," a letter which mathematicians sometimes use to refer to the set of all integer numbers. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:z/ 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:z/ gl-temp)) c:mod, g:mod, and s:mod Calculation: 7 % 2 = 1The value of gl-example in both examples will equal 1. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:mod 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:mod gl-temp)) c:min, g:min, and s:min Calculation: min(7, 2) = 2If the given value is smaller than the value currently stored in gl-example, then gl-example will be set to that smaller value. Otherwise, gl-example will remain unchanged. The end result is that gl-example in both examples will equal 2. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:min 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:min gl-temp)) c:max, g:max, and s:max Calculation: max(7, 2) = 7If the given value is larger than the value currently stored in gl-example, then gl-example will be set to that larger value. Otherwise, gl-example will remain unchanged. The end result is that gl-example in both examples will equal 7. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:max 2))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 2)(up-modify-goal gl-example g:max gl-temp)) c:neg, g:neg, and s:neg Calculation: 7 * -1 = -7Two examples are given since the example with c:neg is rather trivial. The given number will be stored in gl-example with the opposite positive/negative sign. The end result is that gl-example in both examples will equal -7. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:neg 7))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-temp c:= 7)(up-modify-goal gl-example g:neg gl-temp)) c:%*, g:%*, and s:%* Calculation: 29% of 10 = 2 or 10 * 29 / 100 = 2.9, truncated to 2.The given percent of gl-example will be stored in gl-example. In other words, gl-example is multiplied by the given value and divided by 100. The result is truncated (rounded down) if there is a remainder. The end result is that gl-example in both examples will equal 2. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 10)(up-modify-goal gl-example c:%* 29))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 10)(up-modify-goal gl-temp c:= 29)(up-modify-goal gl-example g:%* gl-temp)) If you want your result rounded, rather than truncated, you can accomplish this in two operations using the multiplication and division operators. The end result is that gl-example in both examples will equal 3. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 10)(up-modify-goal gl-example c:* 29)(up-modify-goal gl-example c:/ 100))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 10)(up-modify-goal gl-temp c:= 29)(up-modify-goal gl-example g:* gl-temp)(up-modify-goal gl-example c:/ 100)) c:%/, g:%/, and s:%/ Calculation: 7 out of 9 = 77% or 7 * 100 / 9 = 77.777777, truncated to 77.The value currently stored in gl-example will be multiplied by 100 before dividing by the given value, effectively converting the result to a percent, with any decimal result truncated (rounded down) rather than rounded. The end result is that gl-example in both examples will equal 77. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:%/ 9))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-temp c:= 9)(up-modify-goal gl-example g:%/ gl-temp)) If you want your result rounded, rather than truncated, you can accomplish this in two operations using the multiplication and division operators. The end result is that gl-example in both examples will equal 78. (defconst gl-example 101)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:* 100)(up-modify-goal gl-example c:/ 9))(defconst gl-example 101)(defconst gl-temp 102)(defrule(true)=>(up-modify-goal gl-example c:= 7)(up-modify-goal gl-example c:* 100)(up-modify-goal gl-temp c:= 9)(up-modify-goal gl-example g:/ gl-temp))  
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_object_data(ObjectData: ObjectData,compareOp: compareOp,Value: int,):
    """
 Check specific information about the selected target object. 
:param ObjectData: Range: a valid ObjectData ID. -1 can only be used with up-remove-objects.
 Data information about an object. This information is gathered from the unit's current stats, including any techs that have been researched or civ bonuses that affect the unit. Important Note:some object data is not available for units marching in formation when usingup-get-object-dataorup-object-data: object-data-action, object-data-order, object-data-target, and object-data-target-id. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_object_target_data(ObjectData: ObjectData,compareOp: compareOp,Value: int,):
    """
 Check specific information about the target object's target. 
:param ObjectData: Range: a valid ObjectData ID. -1 can only be used with up-remove-objects.
 Data information about an object. This information is gathered from the unit's current stats, including any techs that have been researched or civ bonuses that affect the unit. Important Note:some object data is not available for units marching in formation when usingup-get-object-dataorup-object-data: object-data-action, object-data-order, object-data-target, and object-data-target-id. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_object_type_count(ObjectId: int,compareOp: compareOp,Value: int,):
    """
 Combine unit-type-count and building-type-count checks. 
:param ObjectId: Range: A validUnitIdor a validBuildingId.
 AUnitIdor aBuildingId. See theObjects Tablefor details. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_object_type_count_total(ObjectId: int,compareOp: compareOp,Value: int,):
    """
 Combine unit-type-count-total and building-type-count-total checks. 
:param ObjectId: Range: A validUnitIdor a validBuildingId.
 AUnitIdor aBuildingId. See theObjects Tablefor details. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_path_distance(Point: int,Option: int,compareOp: compareOp,Value: int,):
    """
 Check the distance from the target object to a specified point goal pair. The distance will be 65535 if the point is unreachable. Set the Option parameter to 1 to require an open destination tile to find the path distance toward or 0 to allow for a few tiles of separation to find a reachable open tile. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
:param Option: Range: varies
 A value that determines different ways the command will work. Here is a list:  
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_pending_objects(ObjectId: int,compareOp: compareOp,Value: int,):
    """
 Perform a comparison with the pending count of an object. 
:param ObjectId: Range: A validUnitIdor a validBuildingId.
 AUnitIdor aBuildingId. See theObjects Tablefor details. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_pending_placement(BuildingId: BuildingId,):
    """
 Check if a specific type of building is waiting for placement. 
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
"""
    pass
def up_player_distance(PlayerNumber: PlayerNumber,compareOp: compareOp,Value: int,):
    """
 Check the distance in tiles to the nearest building of another player. The action allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It cannot be used with players who aren't allies. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_players_in_game(PlayerStance: PlayerStance,compareOp: compareOp,Value: int,):
    """
 Check the number of active players in the game of the specified stance. Players are considered allied with themselves, so "ally" will include the AI player itself. 
:param PlayerStance: Range: 0 to 3.
 A diplomatic stance, including ally, neutral, and enemy. Some UP commands also allow you to specify "any" stance instead of one of the three particular stances. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_point_contains(Point: int,ObjectId: int,):
    """
 Check if an object exists at a point goal pair position. Set Point to 0 to use the point that is stored by up-set-target-point. Please note that when used with all-units-class (-1), this may capture unexpected objects like birds flying over a tile, terrain plants, etc. Also, this action will work whether the point has been explored or not. Therefore, in AI tournamentsup-point-exploredmust be used as a condition in every rule where this command is used. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
:param ObjectId: Range: A validUnitIdor a validBuildingId.
 AUnitIdor aBuildingId. See theObjects Tablefor details. 
"""
    pass
def up_point_distance(Point1:Point,Point2:Point,compareOp: compareOp,Value: int,):
    """
 Perform a distance check between two point goal pairs. Set Point2 to 0 to use the point that is stored by up-set-target-point. 
:param Point1: is a point object
:param Point2: is a point object
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_point_elevation(Point: int,compareOp: compareOp,Value: int,):
    """
 Check the elevation for a tile with a point goal pair. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_point_explored(Point: int,compareOp: compareOp,ExploredState: ExploredState,):
    """
 Check if a point on the map has been explored. Set Point to 0 to use the point that is stored by up-set-target-point. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param ExploredState: Range: 0, 15, 128 (see Defined Values List).
 The exploration state of the point. 
"""
    pass
def up_point_terrain(Point: int,compareOp: compareOp,Terrain: Terrain,):
    """
 Perform a terrain id at a point goal pair position. Set Point to 0 to use the point that is stored by up-set-target-point. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Terrain: Range: 0 to 41.
 The name of a terrain or the ID number assigned to that terrain. Notes about terrain changes apply primarily to the WololoKingdoms version of the game. Terrain changes might be different in AoE2:DE and the HD expansions on Steam. 
"""
    pass
def up_point_zone(Point: int,compareOp: compareOp,Value: int,):
    """
 Check the zone for a tile with a point goal pair. Zone ids may differ if you have no villagers. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_projectile_detected(ProjectileType: ProjectileType,compareOp: compareOp,Value: int,):
    """
 Check the elapsed time in milliseconds since a type of projectile was fired at the AI. 
:param ProjectileType: Range: 0 to 7.
 The source of the projectile to check. Note that the actualObjectIdof the projectile does not work. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_projectile_target(ProjectileType: ProjectileType,compareOp: compareOp,ClassId: ClassId,):
    """
 Check the class of the target of a projectile that was fired at the AI. 
:param ProjectileType: Range: 0 to 7.
 The source of the projectile to check. Note that the actualObjectIdof the projectile does not work. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param ClassId: Range: -1, 900 to 999.
 A class ID. Each object in the game is assigned a class that contains other similar objects. Class IDs can often be used in place of a unit ID. Classes with an asterisk (*) in the name must be defined with a defconst. All other classes are defined in the UserPatchConst.per file that comes with a UserPatch installation. See theObjects Tableto see which units belong to each class. 
"""
    pass
def up_release_escrow():
    """
 Set all escrow amounts to 0 with a single command. 
"""
    pass
def up_remaining_boar_amount(compareOp: compareOp,Value: int,):
    """
 Check the amount of food remaining on the current boar. This data is only valid if the boar is lured with strategic numbers (not Direct Unit Control), while another boar is targetable and available to hunt. If this is not the case, it remains invalid (65535) to signify that this is the final boar. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_remove_objects(SearchSource: SearchSource,ObjectData: ObjectData,compareOp: compareOp,Value: int,):
    """
 Removes objects from the search results based on specific data. If ObjectData is set to -1, the object index in the search results will be used for data comparison when performing removal. 
:param SearchSource: Range: 1 or 2
 The desired search source. 
:param ObjectData: Range: a valid ObjectData ID. -1 can only be used with up-remove-objects.
 Data information about an object. This information is gathered from the unit's current stats, including any techs that have been researched or civ bonuses that affect the unit. Important Note:some object data is not available for units marching in formation when usingup-get-object-dataorup-object-data: object-data-action, object-data-order, object-data-target, and object-data-target-id. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_request_hunters(Value: int,):
    """
 Attempt to request support hunters for the active boar lure. This only applies to boars that are lured with strategic numbers (not Direct Unit Control). It is not guaranteed to reach the total number of requested hunters. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_research(EscrowGoalId: int,TechId: int,):
    """
 Add a technology to the research queue with dynamic values. 
:param EscrowGoalId: Range: 0 or a valid GoalId, ranging from 1 to 16000.
 A goal ID that controls whether escrow should be used. It can be set to the value "with-escrow" or the value "without-escrow". Alternatively, you can use 0 instead of a goal ID to specify that escrow should never be used for this item. Note that using the constants "with-escrow" or "without-escrow" themselves for EscrowGoalId is not valid because 0 or a valid goal ID is expected. 
:param TechId: Range: A valid technology ID.
 The name of a technology or the ID number assigned to that technology. See the Technology table for details [to be added later]. Note that some technologies are given an AI name that is different from the in-game technology name. 
"""
    pass
def up_research_status(TechId: int,compareOp: compareOp,ResearchState: ResearchState,):
    """
 Check the research status of a specific technology. 
:param TechId: Range: A valid technology ID.
 The name of a technology or the ID number assigned to that technology. See the Technology table for details [to be added later]. Note that some technologies are given an AI name that is different from the in-game technology name. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param ResearchState: Range: UP: 0 to 3, DE: -1 to 4.
 The status of the research. 
"""
    pass
def up_reset_attack_now():
    """
 Reset the infinite targeting loop flag set by attack-now. 
"""
    pass
def up_reset_building(Option: int,BuildingId: BuildingId,):
    """
 Halt the activity and research of all buildings of a specific type. If the Option parameter is set to 1, buildings performing research will not be reset. 
:param Option: Range: varies
 A value that determines different ways the command will work. Here is a list:  
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
"""
    pass
def up_reset_cost_data(GoalId: int,):
    """
 Reset 4 consecutive goals storing cost data to 0. 
:param GoalId: Range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE.
 A valid goal ID. A goal ID can either be a number within the range below or a defined constant set to a number within the range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE. 
"""
    pass
def up_reset_filters():
    """
 Reset search indices and filter states for direct unit targeting. All filter states will be set to -1. Use up-reset-search to clear search results. 
"""
    pass
def up_reset_group(GroupId: int,):
    """
 Clear all units in a search group. 
:param GroupId: Range: 0 to 19.
 An ID assigned to a group of objects, similar to Ctrl groups human players can use. In UP, only GroupId's 0 through 9 could be used. However, in DE, GroupId's 0 through 19 work. 
"""
    pass
def up_reset_placement(BuildingId: BuildingId,):
    """
 Clear the placement list for the specified building type when blocked. Please use with caution. 
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
"""
    pass
def up_reset_scouts():
    """
 Halt and disband all soldier explore groups on land. 
"""
    pass
def up_reset_search(LocalIndex: int,LocalList: int,RemoteIndex: int,RemoteList: int,):
    """
 Reset the search state for the direct unit targeting system. Each of the four parameters can be 0 or 1:  
:param LocalIndex: Range: 0 or 1.
 Set to 1 to clear the offset into the list of local objects to search. Explanation: The local list only contains units found for the current player. Whenever you find something with search-local, it'll be removed from searchable local object list and added to found local object list. Setting LocalIndex to 1 would clear searchable local object list and allow finding same objects again. 
:param LocalList: Range: 0 or 1.
 Set to 1 to clear the local object list from previous searches. Explanation: The local list only contains units found for the current player. Whenever you find something with search-local, it'll be removed from searchable local object list and added to found local object list. Setting LocalList to 1 will remove everything from the found local object list. 
:param RemoteIndex: Range: 0 or 1.
 Set to 1 to clear the offset into the list of remote objects to search. Explanation: The remote list only contains units found for the focus player. Whenever you find something with search-remote, it'll be removed from searchable remote object list and added to found remote object list. Setting RemoteIndex to 1 would clear searchable remote object list and allow finding same objects again. 
:param RemoteList: Range: 0 or 1.
 Set to 1 to clear the remote object list from previous searches. Explanation: The remote list only contains units found for the focus player. Whenever you find something with search-remote, it'll be removed from searchable remote object list and added to found remote object list. Setting RemoteList to 1 will remove everything from the found remote object list. 
"""
    pass
def up_reset_target_priorities(PriorityType: PriorityType,Option: int,):
    """
 Reset or clear offensive or defensive targeting priorities. Restore default priorities with 0. For defensive priorities, setting the Option parameter to 1 will reset all to -1. For offensive priorities, unit types will be reset to 0, while classes will be -1. Target units on -1 offensive priority will not hold the attention of attackers if a higher priority unit appears, and you may notice attack behavior that is a bit similar to how patrol selects its targets. If the target unit is not -1 priority, the attacker may retarget, but primarily to other units with the same offensive priority. Battering rams and cannon galleons prefer to attack non-moving targets, while all other units prefer moving targets. 
:param PriorityType: Range: 0 or 1.
 The targeting priority type to modify. 
:param Option: Range: varies
 A value that determines different ways the command will work. Here is a list:  
"""
    pass
def up_reset_unit(UnitId: UnitId,):
    """
 Halt the activity of all units of a specific type. This is equivalent to clicking the "stop" button. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can be used for the UnitId, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
"""
    pass
def up_resource_amount(ResourceType: ResourceType,compareOp: compareOp,Value: int,):
    """
 Perform a comparison with an internal resource value. 
:param ResourceType: Range: 0 to 224 (with some gaps for unused resources).
 A resource type. Includes over 200 more resource types beyond the four basic ones. Some resource types check the resource amount of a specified player number instead of the current player. Note: most of these are not thoroughly tested (by Leif Ericson). Please report your findings. Resources 205 through 210 are used by the post-Conquerors expansions, so they can be used with this parameter, but they aren't defined with UserPatch. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_resource_percent(ResourceType: ResourceType,compareOp: compareOp,Value: int,):
    """
 Perform a comparison with an internal resource value * 100. 
:param ResourceType: Range: 0 to 224 (with some gaps for unused resources).
 A resource type. Includes over 200 more resource types beyond the four basic ones. Some resource types check the resource amount of a specified player number instead of the current player. Note: most of these are not thoroughly tested (by Leif Ericson). Please report your findings. Resources 205 through 210 are used by the post-Conquerors expansions, so they can be used with this parameter, but they aren't defined with UserPatch. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_retask_gatherers(Resource: Resource,Value: int,):
    """
 Retask a specific number of villagers gathering from a resource. This command will attempt to retask villagers to preferred resources after dropping the resources, and it also works with fishing ships. 
:param Resource: Range: 0 to 3, or theClassIdof the resource.
 A gatherable resource type. Note: using the ClassId is not valid for most (all?) of the 1.0c commands that use this parameter. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_retreat_now():
    """
 Retreat all military units to the home town center. Military units within 6 range of the home town center will not be told to retreat. Active explorers will not retreat. If explorers need to retreat, useup-reset-scoutsbefore using this command. It should work with groups and idle units. There's a chance that you may need to disband attack groups before using it, though, by setting the attack group sns to 0 (sn-number-attack-groups, min, and max). It will also work with TSA units, unless an enemy building exists in max-town-size. In that case, TSA overrides the retreat, I think, and resends them to the target. It should also work with attack-now if you useup-reset-attack-nowbefore using up-retreat-now. 
"""
    pass
def up_retreat_to(ObjectId: int,UnitId: UnitId,):
    """
 Retreat all units of a specific type to a random instance of another. Military units within 6 range of the retreat target object (the object in the first parameter) will not be told to retreat, to allow better defense of the retreat object, such as an offensive trebuchet or a castle. Active explorers will not retreat. If explorers need to retreat, useup-reset-scoutsbefore using this command. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can be used for the UnitId, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. 
:param ObjectId: Range: A validUnitIdor a validBuildingId.
 AUnitIdor aBuildingId. See theObjects Tablefor details. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
"""
    pass
def up_sell_commodity(ResourceType: ResourceType,Value: int,):
    """
 Sell a variable amount of resources at the market. The actual amount you sell depends on available resources. 
:param ResourceType: Range: 0 to 224 (with some gaps for unused resources).
 A resource type. Includes over 200 more resource types beyond the four basic ones. Some resource types check the resource amount of a specified player number instead of the current player. Note: most of these are not thoroughly tested (by Leif Ericson). Please report your findings. Resources 205 through 210 are used by the post-Conquerors expansions, so they can be used with this parameter, but they aren't defined with UserPatch. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_send_flare(Point: int,):
    """
 Send a flare to allies from a point goal pair. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
"""
    pass
def up_send_scout(GroupType: GroupType,ScoutMethod: ScoutMethod,):
    """
 Send a land or water scout to a specific location. 
:param GroupType: Range: 100 to 109.
 The type of group. 
:param ScoutMethod: Range: 0 to 6.
 The scouting method. These are the same as IDs 0 to 6 forPositionType. 
"""
    pass
def up_set_attack_stance(UnitId: UnitId,AttackStance: AttackStance,):
    """
 Set the attack stance for all units of a specific type. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
:param AttackStance: Range: -1 to 3 (-1 is invalid forup-set-attack-stance).
 Controls the attack stance of military units. 
"""
    pass
def up_set_defense_priority(BuildingId: BuildingId,Value: int,):
    """
 Set the defensive (TSA) targeting priority for a building. This has no effect against units. Also, unit lines do not work here, so just set the base unit type id (spearman for the entire spearman-line, etc.). Classes may be used, as well. For walls, use class 927; for gates, use class 939. Default priorities by building:  
:param BuildingId: Range: A valid building ID.
 A building object, either the defined building type name, the object ID assigned to it, or the building's class. Sometimes can also be a building line. See theObjects Tablefor reference. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_set_event(EventId: int,Value: int,):
    """
 Set the value of a scenario trigger event. 
:param EventId: Range: 0 to 255.
 The event ID. The only valid events are AI Script Goal effects and AI Signal conditions in scenario triggers. The ID matches the number of the chosen option from the trigger condition/effect. Note: the "AI Trigger 256" option in the AI Script Goal effect cannot be detected by AIs. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_set_group(SearchSource: SearchSource,GroupId: int,):
    """
 Set the local or remote search results to a search group. 
:param SearchSource: Range: 1 or 2
 The desired search source. 
:param GroupId: Range: 0 to 19.
 An ID assigned to a group of objects, similar to Ctrl groups human players can use. In UP, only GroupId's 0 through 9 could be used. However, in DE, GroupId's 0 through 19 work. 
"""
    pass
def up_set_indirect_goal(GoalId: int,Value: int,):
    """
 Set the value of a goal indirectly by reference. 
:param GoalId: Range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE.
 A valid goal ID. A goal ID can either be a number within the range below or a defined constant set to a number within the range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_set_offense_priority(ObjectId: int,Value: int,):
    """
 Set the offensive targeting priority for an object. This is used when attacking withsn-number-attack-groupsorattack-now.sn-enable-offensive-prioritymust be set to 1 for these priorities to take effect. Note: offensive priorities have a very small range. You can turn the priorities up to 11 (highest), but no more. Also, unit lines do not work here, so just set the base unit type id (spearman for the entire spearman-line, etc.). Classes may be used, as well. If a unit has its type priority set, that will override its class priority. Target units on -1 offensive priority will not hold the attention of attackers if a higher priority unit appears. If the target unit is not -1 priority, the attacker may retarget to other units nearby, but primarily to other units with the same offensive priority. Battering rams and cannon galleons prefer to attack non-moving targets, while all other units prefer moving targets. If you clear offensive priorities withup-reset-target-priorities, you may notice attack behavior that is a bit similar to patrol. Default offensive priorities by class/type id: (classes that are not actually used in the game are marked with an asterisk)   
:param ObjectId: Range: A validUnitIdor a validBuildingId.
 AUnitIdor aBuildingId. See theObjects Tablefor details. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_set_placement_data(PlayerNumber: PlayerNumber,ObjectId: int,Value: int,):
    """
 Specify placement information for managed construction. Please ensure Player has at least a town-center to use for reference, if they don't have ObjectId. If Player has no objects left, placement will not work as expected. The properties assigned by up-set-placement-data that are in effect when a build command is executed are stored with them, so you can change properties immediately afterward and it won't break your previous settings. The action only allows exact player numbers, "my-player-number", or "this-any" rule variables forPlayerNumber, such as "this-any-ally" or "this-any-computer-ally". It does not allow "any"/"every" wildcard parameters forPlayerNumber. It cannot be used with players who aren't allies. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param ObjectId: Range: A validUnitIdor a validBuildingId.
 AUnitIdor aBuildingId. See theObjects Tablefor details. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_set_precise_target_point(Point: int,):
    """
 Set the target point with an unchecked extended goal pair. This command is identical to up-set-target-point, except it will not bound the point inside the map. Please ensure the point is valid with up-bound-precise-point. A precise point is expected to be a normal point x100 for 2 places of decimal precision. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
"""
    pass
def up_set_shared_goal(SharedGoalId: int,Value: int,):
    """
 Set the value of a shared goal. 
:param SharedGoalId: Range: 1 to 256.
 A goal that is shared among computer players. It is to be used only when all computer players are on the same team. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_set_signal(SignalId: int,Value: int,):
    """
 Set the value of a scenario trigger signal. This action only works with a single player scenario and "AI Signal" trigger condition. For a multiplayer scenario, use "Multiplayer AI Signal" andfe-set-signal. 
:param SignalId: Range: 0 to 255.
 The Id of a scenario trigger signal. This if effectively the same asEventIdsince the only types of events are trigger signals. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_set_target_by_id(Id: int,):
    """
 Set the target object for other commands by id. Reference it with up-get-point and position-object. If the Id is invalid, the current target object will remain unchanged. This command can be used as either a Fact or an Action. 
:param Id: Range: An ID of an object that is currently on the map.
 The object's ID on the map. All objects on the map will have a different map object ID in the order that the object appeared on the map. 
"""
    pass
def up_set_target_object(SearchSource: SearchSource,Index: int,):
    """
 Set the target object for other commands from your search. Reference it with up-get-point and position-object. If the Index is invalid, the current target object will remain unchanged. This command can be used as either a Fact or an Action. 
:param SearchSource: Range: 1 or 2
 The desired search source. 
:param Index: Range: 0 to 239 for the search-local list. 0 to 39 for the search-remote list.
 The zero-based index of an object in the search-local or search-remote lists. 
"""
    pass
def up_set_target_point(Point: int,):
    """
 Set the target point for other commands with an extended goal pair. This command will also safely bound the point inside the map. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
"""
    pass
def up_set_timer(TimerId: int,Value: int,):
    """
 Disable or enable a timer by interval. Set Value to -1 to disable the timer. If Value is positive, this will perform like the enable-timer action. 
:param TimerId: Range: 1 to 50.
 The ID of a timer or a defconst representing a timer. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_setup_cost_data(Option: int,GoalId: int,):
    """
 Set the goals to store cost data for food, wood, stone, and gold. If the Option parameter is set to 1 the values of the provided cost goal set will be reset to 0. 
:param Option: Range: varies
 A value that determines different ways the command will work. Here is a list:  
:param GoalId: Range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE.
 A valid goal ID. A goal ID can either be a number within the range below or a defined constant set to a number within the range: 1 to 40 for 1.0c. 1 to 512 for UP. 1 to 16000 for DE. 
"""
    pass
def up_store_map_name(Option: int,):
    """
 Store the current map name in the internal buffer. For rms, this is the filename of the map. However, if the map is a dynamic loader, such as Full Random, Random Land Map, or Blind Random, this will be the loader name instead of the actual map name. For scenarios, this will be the original save filename instead of the current filename. The buffer can be referenced by the chat-data commands using %s instead of %d with c: 7031232 (7031232 cannot be stored in a defconst). This buffer is shared by all AIs, so please store data before using it in a rule pass. If the Option parameter is set to 1, the map name will be stored with the file extension in the name. If the Option parameter is set to 0, the map name will be stored without the file extension in the name. 
:param Option: Range: varies
 A value that determines different ways the command will work. Here is a list:  
"""
    pass
def up_store_object_name():
    """
 Store the target object's type name in the internal buffer. The buffer can be referenced by the chat-data commands using %s instead of %d with c: 7031232 (7031232 cannot be stored in a defconst). This buffer is shared by all AIs, so please store data before using it in a rule pass. 
"""
    pass
def up_store_player_chat(PlayerNumber: PlayerNumber,):
    """
 Store a player chat message in the internal buffer. Note that only the last word of a chat message will be stored in the buffer and the message must be present in the host's chat history log (the PageUp key can find it). The buffer can be referenced by the chat-data commands using %s instead of %d with c: 7031232 (7031232 cannot be stored in a defconst). This buffer is shared by all AIs, so please store data before using it in a rule pass. The action only allows for exact player numbers, "my-player-number", or "this-any" rule variables forPlayerNumber, such as "this-any-ally" or "this-any-enemy". It does not allow "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
"""
    pass
def up_store_player_name(PlayerNumber: PlayerNumber,):
    """
 Store a player name in the internal buffer. The buffer can be referenced by the chat-data commands using %s instead of %d with c: 7031232 (7031232 cannot be stored in a defconst). This buffer is shared by all AIs, so please store data before using it in a rule pass. The action only allows for exact player numbers, "my-player-number", or "this-any" rule variables forPlayerNumber, such as "this-any-ally" or "this-any-enemy". It does not allow "any"/"every" wildcard parameters forPlayerNumber. It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
"""
    pass
def up_store_tech_name(TechId: int,):
    """
 Store a research tech name in the internal buffer. The buffer can be referenced by the chat-data commands using %s instead of %d with c: 7031232 (7031232 cannot be stored in a defconst). This buffer is shared by all AIs, so please store data before using it in a rule pass. You can also use my-unique-research, which will usually get the imperial age unique tech for the civilization, and you can also use my-second-unique-research, which will usually get the castle age unique tech for the civilization. The excepts are the Britons, Franks, Goths, and Saracens, whose my-unique-research and my-second-unique-research are switched. 
:param TechId: Range: A valid technology ID.
 The name of a technology or the ID number assigned to that technology. See the Technology table for details [to be added later]. Note that some technologies are given an AI name that is different from the in-game technology name. 
"""
    pass
def up_store_text(LanguageId: int,):
    """
 Store a language string in the internal buffer. The buffer can be referenced by the chat-data commands using %s instead of %d with c: 7031232 (7031232 cannot be stored in a defconst). This buffer is shared by all AIs, so please store data before using it in a rule pass. 
:param LanguageId: Range: a valid LanguageId.
 The ID assigned to a string (quoted text) stored in one of the language.dll files or in a string text file. All words and phrases used by the game are stored in these files. If you have the DE version, you can easily find a list of all language IDs in your Steam installation, usually at "C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\en\strings\key-value\key-value-strings-utf8.txt". For example, language ID 22322 is "No wonder thou wert victorious! I shalt abdicate." 
"""
    pass
def up_store_type_name(TypeId: int,):
    """
 Store an object type name in the internal buffer. The buffer can be referenced by the chat-data commands using %s instead of %d with c: 7031232 (7031232 cannot be stored in a defconst). This buffer is shared by all AIs, so please store data before using it in a rule pass. 
:param TypeId: Range: A validObjectIdor one of the object line wildcard parameters.
 The type of object. This can be either the object name or an object line ID. See theObjects Tablefor a list of object names and object line wildcard parameters. 
"""
    pass
def up_target_objects(Option: int,DUCAction: DUCAction,Formation: Formation,AttackStance: AttackStance,):
    """
 Direct local search results against remote search results. The action-default command is equivalent to a right-click. This command can only perform the following actions: action-default, action-move, action-patrol, action-guard, action-follow, action-stop, action-ground, action-garrison, action-delete, action-gather, and action-none. The otherDUCActionoptions available forup-target-pointwill not work. Set the Option parameter to 1 to target only the object set by up-set-target-object. If set to 0, the objects in the local list will evenly target all objects in the remote list. This command will aim to separate the units selected with up-find-local into groups of 20 units or less before sending them against the remote target(s). Do not use the action-default or action-move commands if the defensive targeting system (TSA) is locked on a target, or units will become "confused" and not respond for a few moments. Either bring the town size so thatenemy-buildings-in-townis no longer true or setsn-disable-defend-groupson. The action-patrol command seems to work regardless. 
:param Option: Range: varies
 A value that determines different ways the command will work. Here is a list:  
:param DUCAction: Range: 0 to 18.
 The action to perform with the selected units. Some DUC Actions cannot be taken withup-target-objects. 
:param Formation: Range: -1, 2, 4, 7, or 8.
 The formation that the units will be set to. 
:param AttackStance: Range: -1 to 3 (-1 is invalid forup-set-attack-stance).
 Controls the attack stance of military units. 
"""
    pass
def up_target_point(Point: int,DUCAction: DUCAction,Formation: Formation,AttackStance: AttackStance,):
    """
 Direct local search results to a specific point on the map. This command can perform all actions from the DUCAction list. However, action-default, action-guard, action-follow, and action-garrison will perform as action-move. If you wish to action-move back into formation nearby after attacking, please action-move to the point (-1,-1) first to reset distance. This command will aim to separate the units selected with up-find-local into groups of 20 units or less before sending them against the remote target(s). Do not use the action-default or action-move commands if the defensive targeting system (TSA) is locked on a target, or units will become "confused" and not respond for a few moments. Either bring the town size so thatenemy-buildings-in-townis no longer true or setsn-disable-defend-groupson. The action-patrol command seems to work regardless. 
:param Point: Range: 41 to 15998.
 The first of 2 consecutive goals to store the x and y coordinates of the point. These goals must be extended goals (goal IDs 41-15998), which have a signed 32-bit range (-2,147,483,648 to 2,147,483,647). 
:param DUCAction: Range: 0 to 18.
 The action to perform with the selected units. Some DUC Actions cannot be taken withup-target-objects. 
:param Formation: Range: -1, 2, 4, 7, or 8.
 The formation that the units will be set to. 
:param AttackStance: Range: -1 to 3 (-1 is invalid forup-set-attack-stance).
 Controls the attack stance of military units. 
"""
    pass
def up_timer_status(TimerId: int,compareOp: compareOp,TimerState: TimerState,):
    """
 Check whether a timer is disabled, triggered, running, or a combination. 
:param TimerId: Range: 1 to 50.
 The ID of a timer or a defconst representing a timer. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param TimerState: Range: 0 to 2.
 The current state of a timer. 
"""
    pass
def up_train(EscrowGoalId: int,UnitId: UnitId,):
    """
 Add a unit to the training queue with dynamic values. You can also train unique units by using my-unique-unit, my-elite-unique-unit, and my-unique-unit-line, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. The setting ofsn-dock-training-filteraffects the ability for docks to train warships with this command. 
:param EscrowGoalId: Range: 0 or a valid GoalId, ranging from 1 to 16000.
 A goal ID that controls whether escrow should be used. It can be set to the value "with-escrow" or the value "without-escrow". Alternatively, you can use 0 instead of a goal ID to specify that escrow should never be used for this item. Note that using the constants "with-escrow" or "without-escrow" themselves for EscrowGoalId is not valid because 0 or a valid goal ID is expected. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
"""
    pass
def up_train_site_ready(UnitId: UnitId,):
    """
 Check if a unit's training site is ready and available. You can also check the train site of my-unique-unit, which will automatically check the train site of the UnitId of the unique unit that the AI's civ can train from the castle. Important Note:Unit lines, negative unit IDs, or invalid unit Ids may result in a crash. Do not use unit lines or unit classes with this command. Please use the root unit type instead, such as using archer instead of archer-line, even if Crossbowman has been researched. In most cases, the unit you use to test whether a train site is ready doesn't matter. However, for docks, the unit you choose to test is important. Trade cogs may be rejected by the dock if you usesn-dock-training-filterand it hasn't found an allied dock. On the other hand, a military ship (galley works to test all of these) uses enemy ships/docks to determine if it is acceptable when that sn is in use. Fishing ships may also provide a different result sooner or later. An alternative to this command is finding a building you want to check, setting it as the target object withup-set-target-objectorup-set-target-by-idand usingup-get-object-datalike this: If 0 is stored in gl-data, then the building is not training or researching, and it is ready to train units. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
"""
    pass
def up_tribute_to_player(PlayerNumber: PlayerNumber,ResourceType: ResourceType,Value: int,):
    """
 Tribute a variable amount of resources to other players. The fact allows "focus-player", "target-player", and "any"/"every" wildcard parameters forPlayerNumber. It also allows the use of rule variables for PlayerNumber, such as "this-any-ally" or "this-any-enemy". It also allows for scenario-player-# and lobby-player-#, where # is between 1 and 8. scenario-player-# refers to the player color (where red = scenario-player-2), and lobby-player-# refers to the player slot (where the lobby host or human player playing a single player campaign is always lobby-player-1). 
:param PlayerNumber: Range: A valid player number.
 A valid player number. Here is a list with the possible PlayerNumber types which all commands with a PlayerNumber parameter can use. target-player, focus-player, lobby-player-#, scenario-player-#, and the any/every/this-any PlayerNumber types can only be used in commands where a PlayerNumber parameter is expected. If a fact command that uses an any-* wildcard parameter returns true, it will set the corresponding this-any-* rule variable for the rest of the rule, which can be used by any action command below that can use this-any-* rule variables. For example, if (players-building-count any-enemy >= 1) returns true, this-any-enemy will be set to the first enemy player that the AI knows has at least 1 building, and the AI can send a chat to this player with (chat-to-player this-any-enemy "I found you!"). However, once the rule has finished the this-any-* rule variables are reset. Several commands with the PlayerNumber parameter can also use any/enemy wildcard parameters and/or this-any-* rule variables from the lists at the bottom of the page. Here is a chart of which commands can use any/every wildcard parameters and/or this-any-* rule variables. Any command that isn't on this list cannot use any of them. Use these wildcard parameters and rule variables carefully, because the game likely won't generate an error if you use them with commands which don't support them.  
:param ResourceType: Range: 0 to 224 (with some gaps for unused resources).
 A resource type. Includes over 200 more resource types beyond the four basic ones. Some resource types check the resource amount of a specified player number instead of the current player. Note: most of these are not thoroughly tested (by Leif Ericson). Please report your findings. Resources 205 through 210 are used by the post-Conquerors expansions, so they can be used with this parameter, but they aren't defined with UserPatch. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_ungarrison(ObjectId: int,):
    """
 Request all objects of the specified type to ungarrison units. 
:param ObjectId: Range: A validUnitIdor a validBuildingId.
 AUnitIdor aBuildingId. See theObjects Tablefor details. 
"""
    pass
def up_unit_type_in_town(UnitId: UnitId,compareOp: compareOp,Value: int,):
    """
 Check the number of a specific enemy unit type in town. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def up_update_targets():
    """
 Perform an immediate update for objects in town size. This command is important when using TSA. If you expand town size, new targets inside sn-maximum-town-size are quickly added into the target list (the list of enemy objects within sn-maximum-town-size). However, if you reduce sn-maximum-town-size, you have to wait until the target refresh for these objects to be removed from the target list, which happens every 15 seconds. This can cause issues with retreating, for example. Using up-update-targets will immediately update the target list, resolving the issue. 
"""
    pass
def up_villager_type_in_town(UnitId: UnitId,compareOp: compareOp,Value: int,):
    """
 Check the number of a specific enemy villager type in town. 
:param UnitId: Range: A valid UnitId.
 The object ID of a unit, the unit type name, a unit line (see wildcard parameters below), or a unit'sClassId. my-unique-unit, my-elite-unique-unit, and my-unique-unit-line can also be used, which will automatically get the UnitId of the unique unit, elite unique unit, or unique unit line that the AI's civ can train from the castle. Some commands cannot use unit lines or classes. Please see the command page for each individual command to confirm what type of UnitId can be used. See theObjects Tablefor a list of unit IDs and unit type names. Note:The unit lines IDs for UP and DE don't always match. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def fe_break_point(Value: int,compareOp: compareOp,Value1: int,OptionGoalId: int,):
    """
 DE only. Add a break point to force the AI debugger interface to display if the break point conditions are met. The break point conditions are met if the comparison between the first and second values is true and either the last parameter is -1 or the goal specified in the last parameter is set to a value >= 1. The debugger shows you various information about the AI's current state, such as the current value of each goal and the object IDs stored in the local and remote lists. Once the debugger is opened, you'll be able to step through your rules. To enable the debugger you must first enable AI debugging for the game in the Steam launch options. Before launching the game, go to Steam => Right click game => Properties => in bottom box type AIDEBUGGING. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param Value1: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
:param OptionGoalId: Range: a goal ID to control how the command works
 A goal ID, whose values controls how a command works. Here's how it affects each command:  
"""
    pass
def fe_cc_effect_amount(EffectId: EffectId,ItemId: int,AttrId: AttrId,Value: int,):
    """
 DE only. Apply a research-style effect with an integer value for the AI player. This is considered a cheat command, but cheats do not have to be enabled. When modifying objects, you may need to target ALL hidden variations, one-by-one, as well. Please consider in-game object upgrades, so that an upgrade will not push a unit's max hitpoints over 32768 or the object will be destroyed. If you disable an object with this command, in-game techs/ages (unless disabled) may re-enable them. The civ tech tree may also override changes. This command can only use integer values. If you need to make an effect with a decimal value, usefe-cc-effect-percent. 
:param EffectId: Range: 0 to 9.
 The id of an Effect such as effect_set_attribute. This parameter determines how theAttrIdshould be affected. Since thefe-cc-effect-amountandfe-cc-effect-percentare similar to researching a custom technology for free, you can think of the EffectId as specifying the type of technology the command will execute, such as upgrading a new unit or adding hit points to a building. The available EffectIds are very similar to the Command Types dropdown on the Effects tab of the Advanced Genie Editor when a tech effect is selected. Please note that I (Leif Ericson) have not tested the effects below, and they are just educated guesses at the moment. 
:param ItemId: Range: an Object ID or Tech ID
 The type of object that will be affected, such as villager-class, or the research name or ID. 
:param AttrId: Range: 0 to 109.
 The id of an attribute to modify, such as attribute-hp. Since thefe-cc-effect-amountandfe-cc-effect-percentare similar to researching a custom technology for free, you can think of the AttrId as specifying what the technology will change or modify. Please note that all of the attribute descriptions below are my (Leif Ericson's) educated guess, and I have done no testing on these attributes (yet). 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def fe_cc_effect_percent(EffectId: EffectId,ItemId: int,AttrId: AttrId,Percent: int,):
    """
 DE only. Apply a research-style effect as a percentage for the AI player. This command is identical tofe-cc-effect-amount, except the value is divided by 100 to provide decimal precision. This is considered a cheat command, but cheats do not have to be enabled. When modifying objects, you may need to target ALL hidden variations, one-by-one, as well. Please consider in-game object upgrades, so that an upgrade will not push a unit's max hitpoints over 32768 or the object will be destroyed. If you disable an object with this command, in-game techs/ages (unless disabled) may re-enable them. The civ tech tree may also override changes. This command can only use integer values. 
:param EffectId: Range: 0 to 9.
 The id of an Effect such as effect_set_attribute. This parameter determines how theAttrIdshould be affected. Since thefe-cc-effect-amountandfe-cc-effect-percentare similar to researching a custom technology for free, you can think of the EffectId as specifying the type of technology the command will execute, such as upgrading a new unit or adding hit points to a building. The available EffectIds are very similar to the Command Types dropdown on the Effects tab of the Advanced Genie Editor when a tech effect is selected. Please note that I (Leif Ericson) have not tested the effects below, and they are just educated guesses at the moment. 
:param ItemId: Range: an Object ID or Tech ID
 The type of object that will be affected, such as villager-class, or the research name or ID. 
:param AttrId: Range: 0 to 109.
 The id of an attribute to modify, such as attribute-hp. Since thefe-cc-effect-amountandfe-cc-effect-percentare similar to researching a custom technology for free, you can think of the AttrId as specifying what the technology will change or modify. Please note that all of the attribute descriptions below are my (Leif Ericson's) educated guess, and I have done no testing on these attributes (yet). 
:param Percent: Range: -32768 to 32767.
 A percentage, i.e. a decimal multiplied by 100 
"""
    pass
def fe_filter_garrisoned(Option: int,):
    """
 DE only. Filters whether garrisoned and/or ungarrisoned units are found in DUC searches. Set to 0 before a DUC search to exclude objects that are garrisoned in a building, ram, or transport ship from future DUC searches, but allow units that aren't garrisoned to be found (the default setting). Set to 1 before a DUC search to allow both garrisoned and ungarrisoned units to be found. Set to 2 before a DUC search to exclude ungarrisoned units. Usingup-full-reset-searchorup-reset-filterswill reset the filter back to its default setting (0). 
:param Option: Range: varies
 A value that determines different ways the command will work. Here is a list:  
"""
    pass
def fe_set_signal(SignalId: int,Value: int,):
    """
 DE only. Set the value of a multiplayer scenario trigger signal. This action only works with a "Multiplayer AI Signal" trigger condition in a single and multiplayer scenario. For the "AI Signal" condition useup-set-signal(only works in a single player scenario).  
:param SignalId: Range: 0 to 255.
 The Id of a scenario trigger signal. This if effectively the same asEventIdsince the only types of events are trigger signals. 
:param Value: Range: A 16-bit signed integer (-32768 to 32767). Values for goals and extended strategic numbers (SNs 242-511) have a 32-bit signed integer range instead (-2,147,483,648 to 2,147,483,647).
 An integer value. Used for many different purposes. 
"""
    pass
def fe_sub_game_type(compareOp: compareOp,SubGameType: SubGameType,):
    """
 DE only. Checks if game matches the specified sub-game type. There are four sub-game types: sub-game-type-empire-wars, sub-game-type-sudden-death, sub-game-type-regicide, and sub-game-type-king-of-the-hill. Sub-games are loaded whenever the checkbox for these sub-game modes are checked in the lobby screen, rather than being selected from the game type dropdown. Multiple sub-games modes can be true at once in a game. 
:param compareOp: Range: 0 to 5, 7 to 12, 14 to 19.
 Performs a comparison between two parameters in a command. The prefix determines the expected type of parameter for the second parameter to be compared. There are three possible versions you can use for each operator. 
:param SubGameType: Range: 1, 2, 4, 8
 A sub-game type. Sub-games are loaded whenever the checkbox for these sub-game modes are checked in the lobby screen, rather than being selected from the game type dropdown. Multiple sub-games modes can be true at once in a game. 
"""
    pass
def xs_script_call(String: str,):
    pass