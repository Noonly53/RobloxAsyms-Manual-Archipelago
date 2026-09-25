# Object classes from AP core, to represent an entire MultiWorld and this individual World that's part of it
from typing import Any
from worlds.AutoWorld import World
from BaseClasses import MultiWorld, CollectionState, Item, ItemClassification
from Options import OptionError
import random

# Object classes from Manual -- extending AP core -- representing items and locations that are used in generation
from ..Items import ManualItem
from ..Locations import ManualLocation

# Raw JSON data from the Manual apworld, respectively:
#          data/game.json, data/items.json, data/locations.json, data/regions.json
#
from ..Data import game_table, item_table, location_table, region_table

# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value, format_state_prog_items_key, ProgItemsCat, remove_specific_item

# calling logging.info("message") anywhere below in this file will output the message to both console and log file
import logging

########################################################################################
## Order of method calls when the world generates:
##    1. create_regions - Creates regions and locations
##    2. create_items - Creates the item pool
##    3. set_rules - Creates rules for accessing regions and locations
##    4. generate_basic - Runs any post item pool options, like place item/category
##    5. pre_fill - Creates the victory location
##
## The create_item method is used by plando and start_inventory settings to create an item from an item name.
## The fill_slot_data method will be used to send data to the Manual client for later use, like deathlink.
########################################################################################



# Use this function to change the valid filler items to be created to replace item links or starting items.
# Default value is the `filler_item_name` from game.json
def hook_get_filler_item_name(world: World, multiworld: MultiWorld, player: int) -> str | bool:
    return False

def before_generate_early(world: World, multiworld: MultiWorld, player: int) -> None:
    """
    This is the earliest hook called during generation, before anything else is done.
    Use it to check or modify incompatible options, or to set up variables for later use.
    """
    if is_option_enabled(multiworld, player, "Auto_Balance_Starting_Amount") and (get_option_value(multiworld, player, "Override_Starting_Killers") != -1 or get_option_value(multiworld, player, "Override_Starting_Survivors") != -1):
        raise OptionError(
                f"{world.player_name}: AutoBalanceStartingCharacterAmount cannot be enabled together with "
                f"OverRideKillerStartingAmount or OverRideSurvivorStartingAmount. Disable one or the other."
        )
    pass

# Called before regions and locations are created. Not clear why you'd want this, but it's here. Victory location is included, but Victory event is not placed yet.
def before_create_regions(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after regions and locations are created, in case you want to see or modify that information. Victory location is included.
def after_create_regions(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to remove locations from the world
    locationNamesToRemove: list[str] = [] # List of location names

    # Add your code here to calculate which locations to remove

    category_map = {
        "noob": "Noob (Forsaken) Tasks",
        "007n7": "007n7 Tasks",
        "veeronica": "Veeronica Tasks",
        "elliot": "Elliot Tasks",
        "shedletsky": "Shedletsky Tasks",
        "chance": "Chance Tasks",
        "two time": "Two Time Tasks",
        "guest 1337": "Guest 1337 Tasks",
        "builderman": "Builderman Tasks",
        "taph": "Taph Tasks",
        "dusekkar": "Dusekkar Tasks",
        "jane doe": "Jane Doe Tasks",
        "slasher": "Slasher Tasks",
        "coolkidd": "Coolkidd Tasks",
        "john doe": "John Doe Tasks",
        "noli": "Noli Tasks",
        "1x1x1x1": "1x1x1x1 Tasks",
        "guest 666": "Guest 666 Tasks",
        "nosferatu": "Nosferatu Tasks",
        "azure": "Azure Tasks",
        "adrenaline": "Adrenaline Tasks",
        "banana peel": "Banana Peel Tasks",
        "bonuspad": "BonusPad Tasks",
        "block": "Block Tasks",
        "bugle": "Bugle Tasks",
        "caretaker": "Caretaker Tasks",
        "cloak": "Cloak Tasks",
        "dash": "Dash Tasks",
        "hotdog": "Hotdog Tasks",
        "pie": "Pie Tasks",
        "punch": "Punch Tasks",
        "revolver": "Revolver Tasks",
        "taunt": "Taunt Tasks",
        "reroll": "Reroll Tasks",
        "flashlight": "Flashlight Tasks",
        "pursuer": "Pursuer Tasks",
        "badware": "Badware Tasks",
        "artful": "Artful Tasks",
        "harken": "Harken Tasks",
        "killdroid": "Killdroid Tasks",
        "sonic": "Sonic Tasks",
        "tails": "Tails Tasks",
        "knuckles": "Knuckles Tasks",
        "eggman": "Eggman Tasks",
        "amy": "Amy Tasks",
        "cream": "Cream Tasks",
        "metal sonic": "Metal Sonic Tasks",
        "silver": "Silver Tasks",
        "blaze": "Blaze Tasks",
        "2011x": "2011X Tasks",
        "kolossos": "Kolossos Tasks",
        "tripwire": "Tripwire Tasks",
        "fleetway": "Fleetway Tasks",
        "dante": "Dante Tasks",
        "nyan": "Nyan Tasks",
        "mikaela": "Mikaela Tasks",
        "fukatsuki": "Fukatsuki Tasks",
        "vinnie": "Vinnie Tasks",
        "crafter": "Crafter Tasks",
        "tac9": "Tac9 Tasks",
        "roflpix": "Roflpix Tasks",
        "partypwny": "PartyPwny Tasks",
        "dotx": "DotX Tasks",
        "blankstare": "Blankstare Tasks",
        "sweep": "Sweep Tasks",
        "captain limewire": "Captain Limewire Tasks",
        "jack noir": "Jack Noir Tasks",
        "pancho": "Pancho Tasks",
        "bloxxer": "Bloxxer Tasks",
        "mrrobot": "MrRobot Tasks",
        "betty": "Betty Tasks",
        "calindra": "Calindra Tasks",
        "jimmy": "Jimmy Tasks",
        "clockwork": "Clockwork Tasks",
        "killerkyle": "KillerKyle Tasks",
        "fencer": "Fencer Tasks",
        "clawsguy": "ClawsGuy Tasks",
        "frapers": "Frapers Tasks",
        "stalker": "Stalker Tasks",
        "slacker": "Slacker Tasks",
        "trapper": "Trapper Tasks",
        "cubedhexa22": "CubedHexa22 Tasks",
        "observer": "Observer Tasks",
        "ashle": "Ashle Tasks"
    }

    excluded_characters = (list(world.options.Forsaken_Exclude.value) + list(world.options.DoD_Exclude.value) + list(world.options.SJ_Exclude.value) + list(world.options.OM_Exclude.value) + list(world.options.PS_Exclude.value) + list(world.options.BIAST_Exclude.value))

    for location in location_table:
        if any(
            category_map[character] in location["category"]
            for character in excluded_characters
        ):
            locationNamesToRemove.append(location["name"])
    
    #Editing Gen amount DOESN'T WORK YET, MAKE THIS WORK NOONLY
    genAmount = get_option_value(multiworld, player, "Gensanity_Amount")
    fullGenAmount = [str(genAmount), str(genAmount + 1), str(genAmount + 2)]
    
    for location in location_table:
        should_remove = False
        for number in fullGenAmount:
            if number in location["name"] and location["category"] == "Forsaken Gensanity Tasks":
                locationNamesToRemove.append(location["name"])
    
    for region in multiworld.regions:
        if region.player == player:
            for location in list(region.locations):
                if location.name in locationNamesToRemove:
                    region.locations.remove(location)

# This hook allows you to access the item names & counts before the items are created. Use this to increase/decrease the amount of a specific item in the pool
# Valid item_config key/values:
# {"Item Name": 5} <- This will create qty 5 items using all the default settings
# {"Item Name": {"useful": 7}} <- This will create qty 7 items and force them to be classified as useful
# {"Item Name": {"progression": 2, "useful": 1}} <- This will create 3 items, with 2 classified as progression and 1 as useful
# {"Item Name": {0b0110: 5}} <- If you know the special flag for the item classes, you can also define non-standard options. This setup
#       will create 5 items that are the "useful trap" class
# {"Item Name": {ItemClassification.useful: 5}} <- You can also use the classification directly
def before_create_items_all(item_config: dict[str, int|dict], world: World, multiworld: MultiWorld, player: int) -> dict[str, int|dict]:
    # Changes the Wintoken amount to the yaml Option or removes Wintokens if other goal is selected
    if world.options.goal.value == 0:
        item_config["Wintoken"] = world.options.Wintoken_Amount.value + world.options.Wintoken_Extra.value
    else:
        item_config["Wintoken"] = 0
    # Remove Moves if Move Sanity or Forsaken are disabled
    if world.options.Move_Sanity.value == False or world.options.Playing_Forsaken.value == False:
        items_to_remove = ["Bloxy Cola", "Slateskin Potion", "GhostBurger", "Slash", "Fried Chicken", "Pizza Toss", "Rush Hour", "Guest Block", "Charge", "Guest Punch", "Sacrificial Dagger", "Crouch", "Pray", "Ritual", "Clone", "C00LGUI", "Inject", "Coin Flip", "One Shot", "Chance Reroll", "Hat Fix", "Plasma Beam", "Spawn Protection", "Subspace Tripmine", "Taph Tripwire", "Sentry", "Dispenser", "Carry", "Vandalism", "Sk8", "Broadcast", "Activate Battery", "Crystal Pitch", "Hatchet"]
        for item in items_to_remove:
            item_config.pop(item, None)
    # Remove Regular Survivors if Movesanity and Forsaken are Enabled
    if world.options.Move_Sanity.value == True and world.options.Playing_Forsaken.value == True:
        items_to_remove = ["Noob (Forsaken)", "Shedletsky", "007n7", "Veeronica", "Guest 1337", "Taph", "Dusekkar", "Jane Doe", "Two Time", "Chance", "Elliot", "Builderman"]
        for item in items_to_remove:
            item_config.pop(item, None)
    # Remove Forsaken Survivors if Forsaken is Disabled
    if world.options.Playing_Forsaken.value == False:
        items_to_remove = ["Noob (Forsaken)", "Shedletsky", "007n7", "Veeronica", "Guest 1337", "Taph", "Dusekkar", "Jane Doe", "Two Time", "Chance", "Elliot", "Builderman"]
        for item in items_to_remove:
            item_config.pop(item, None)
    # Remove Moves if Move Sanity or Outcome Memories are disabled
    if world.options.Move_Sanity.value == False or world.options.Playing_Outcome_Memories.value == False:
        items_to_remove = ["Dropdash", "Peelout", "Glide", "Laser Cannon", "Switch", "Knuckles Punch", "Counter", "Hammer", "Hammer Throw", "Amy Reroll", "Heal", "Cream Dash", "Jetpack Boost", "Energy Shield", "Destructive Charge", "Self Repair", "Suspension", "Rock Throw", "Time Reversal", "Roundhouse Kick/Sol Dash/Sol Boost", "Burning Javelin/Sol Flame"]
        for item in items_to_remove:
            item_config.pop(item, None)
    # Remove Survivors if Outcome Memories is Disabled
    if world.options.Playing_Outcome_Memories == False:
        items_to_remove = ["Sonic", "Knuckles", "Amy", "Cream", "Tails", "Eggman", "Metal Sonic", "Blaze", "Silver"]
        for item in items_to_remove:
            item_config.pop(item, None)
    # Remove Regular Survivors if Movesanity and Outcome memories are Enabled
    if world.options.Move_Sanity.value == True and world.options.Playing_Outcome_Memories.value == True:
        items_to_remove = ["Sonic", "Knuckles", "Amy", "Cream", "Tails", "Eggman", "Metal Sonic", "Blaze", "Silver"]
        for item in items_to_remove:
            item_config.pop(item, None)
    #Removes Characters Being Excluded
    if world.options.Playing_Forsaken.value == True and world.options.Move_Sanity.value == False:
        for item_name in list(item_config):
            if item_name.lower() in world.options.Forsaken_Exclude.value:
                item_config.pop(item_name, None)
    if world.options.Playing_Forsaken.value == True and world.options.Move_Sanity.value == True:
        forsmoves = {
            "noob": ["bloxy cola", "slateskin potion", "ghostburger"],
            "shedletsky": ["slash", "fried chicken"],
            "elliot": ["pizza toss", "rush hour"],
            "007n7": ["clone", "c00lgui", "inject"],
            "veeronica": ["sk8", "broadcast", "activate battery"],
            "guest 1337": ["guest block", "charge", "guest punch"],
            "two time": ["sacrificial dagger", "crouch", "ritual"],
            "chance": ["coin flip", "one shot", "chance reroll", "hat fix"],
            "builderman": ["sentry", "dispenser"],
            "taph": ["taph tripwire", "subspace tripmine"],
            "dusekkar": ["plasma beam", "spawn protection"],
            "jane doe": ["crystal pitch", "hatchet"],
        }
        for character in world.options.Forsaken_Exclude.value:
            for move in forsmoves.get(character.lower(), []):
                for item_name in list(item_config):
                    if item_name.lower() == move:
                        item_config.pop(item_name, None)
                        
    if world.options.Playing_Die_of_Death.value == True:
        for item_name in list(item_config):
            if item_name.lower() in world.options.DoD_Exclude.value:
                item_config.pop(item_name, None)
    
    if world.options.Playing_Outcome_Memories.value == True and world.options.Move_Sanity.value == False:
        for item_name in list(item_config):
            if item_name.lower() in world.options.OM_Exclude.value:
                item_config.pop(item_name, None)
    if world.options.Playing_Outcome_Memories.value == True and world.options.Move_Sanity.value == True:
        ommoves = {
            "sonic": ["dropdash", "peelout"],
            "tails": ["laser cannon", "glide"],
            "knuckles": ["knuckles punch", "counter"],
            "amy": ["hammer", "hammer throw", "amy reroll"],
            "cream": ["heal", "cream dash", "glide"],
            "eggman": ["jetpack boost", "energy shield"],
            "metal sonic": ["destructive charge", "self repair"],
            "blaze": ["roundhouse kick/sol dash/sol boost", "burning javelin/sol flame"],
            "silver": ["suspension", "rock throw", "time reversal"],
        }
        for character in world.options.OM_Exclude.value:
            for move in ommoves.get(character.lower(), []):
                for item_name in list(item_config):
                    if item_name.lower() == move:
                        item_config.pop(item_name, None)
                       
    if world.options.Playing_Scream_Jam.value == True:
        for item_name in list(item_config):
            if item_name.lower() in world.options.SJ_Exclude.value:
                item_config.pop(item_name, None)
                
    if world.options.Playing_Pursuitcore.value == True:
        for item_name in list(item_config):
            if item_name.lower() in world.options.PS_Exclude.value:
                item_config.pop(item_name, None)
                
    if world.options.Playing_Break_in_and_Steal_Thingz.value == True:
        for item_name in list(item_config):
            if item_name.lower() in world.options.BIAST_Exclude.value:
                item_config.pop(item_name, None)
    return item_config
        
# The item pool before starting items are processed, in case you want to see the raw item pool at that stage
def before_create_items_starting(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    startingItems: list[str] = []
    
    Surv_Map = [
        # SJ
        "Pancho", "Bloxxer", "MrRobot", "Betty", "Calindra", "Jimmy", "Clockwork",
        # DoD
        "Punch", "Block", "Banana Peel", "Dash", "Caretaker", "Bonuspad", "Taunt",
        "Revolver", "Adrenaline", "Cloak", "Hotdog", "Reroll", "Pie", "Bugle", "Flashlight"
    ]

    Move_Map = [
        #Saken
        "Bloxy Cola", "Slateskin Potion", "GhostBurger", "Slash", "Fried Chicken", "Pizza Toss",
        "Rush Hour", "Guest Block", "Charge", "Guest Punch", "Sacrificial Dagger", "Crouch",
        "Pray", "Ritual", "Clone", "C00LGUI", "Inject", "Coin Flip", "One Shot", "Chance Reroll",
        "Hat Fix", "Plasma Beam", "Spawn Protection", "Subspace Tripmine", "Taph Tripwire",
        "Sentry", "Dispenser", "Carry", "Vandalism", "Sk8", "Broadcast", "Activate Battery",
        "Crystal Pitch", "Hatchet",

        # OM
        "Dropdash", "Peelout", "Glide", "Laser Cannon", "Switch",
        "Knuckles Punch", "Counter", "Hammer", "Hammer Throw", "Amy Reroll",
        "Heal", "Cream Dash", "Jetpack Boost", "Energy Shield", "Destructive Charge",
        "Self Repair", "Suspension", "Rock Throw", "Time Reversal",
        "Roundhouse Kick/Sol Dash/Sol Boost", "Burning Javelin/Sol Flame"
    ]

    Char_Map = [
        # OM
        "Sonic", "Knuckles", "Amy", "Cream", "Tails", "Eggman", "Metal Sonic", "Blaze", "Silver",
        # Forsaken characters
        "Noob (Forsaken)", "Shedletsky", "007n7", "Veeronica", "Guest 1337", "Taph", "Dusekkar",
        "Jane Doe", "Two Time", "Chance", "Elliot", "Builderman",
        # Pursuit
        "Dante", "Mikaela", "Nyan", "Fukatsuki", "Crafter", "Vinnie", "Tac9", "Roflpix", "The Kit"
    ]

    Kill_Map = [
        #OM
        "2011x", "Kolossos", "Tripwire", "Fleetway",
        #SJ
        "KillerKyle", "Fencer", "ClawsGuy", "Frapers", "Stalker",
        #DoD
        "Pursuer", "Badware", "Artful", "Harken", "Killdroid",
        #Saken
        "Slasher", "Coolkidd", "John Doe", "Noli", "1x1x1x1", "Guest 666", "Nosferatu", "Azure",
        #Pursuit
        "Partypwny", "DotX", "Blankstare", "Sweep", "Captain Limewire", "Jack Noir",
        #BIAST
        "Slacker", "Trapper", "CubedHexa22", "Observer", "Ashle", "Jeff the Killer"
    ]

    move_sanity = is_option_enabled(multiworld, player, "Move_Sanity")
    Surv_Map = Surv_Map + (Move_Map if move_sanity else Char_Map)

    def pick_unique(pool: list, count: int) -> list:
        # Pick up to `count` unique names from pool, without mutating pool or crashing on oversized counts.
        count = max(0, min(count, len(pool)))
        return world.random.sample(pool, count)

    override_survivors = get_option_value(multiworld, player, "Override_Starting_Survivors")
    override_killers = get_option_value(multiworld, player, "Override_Starting_Killers")
    auto_balance = is_option_enabled(multiworld, player, "Auto_Balance_Starting_Amount")

    # Explicit overrides always apply if set, regardless of auto-balance
    if override_survivors != -1:
        startingItems.extend(pick_unique(Surv_Map, override_survivors))

    if override_killers != -1:
        startingItems.extend(pick_unique(Kill_Map, override_killers))

    if auto_balance:
        survivorAmount = 0
        killerAmount = 0
        gamesPlayed = 0

        if is_option_enabled(multiworld, player, "Playing_Forsaken"):
            if move_sanity:
                survivorAmount += 2
            else:
                survivorAmount += 1
            killerAmount += 1
            gamesPlayed += 1
        if is_option_enabled(multiworld, player, "Playing_Die_Of_Death"):
            survivorAmount += 2
            killerAmount += 1
            gamesPlayed += 1
        if is_option_enabled(multiworld, player, "Playing_Outcome_Memories"):
            if move_sanity:
                survivorAmount += 2
            else:
                survivorAmount += 1
            killerAmount += 1
            gamesPlayed += 1
        if is_option_enabled(multiworld, player, "Playing_Scream_Jam"):
            survivorAmount += 1
            killerAmount += 1
            gamesPlayed += 1
        if is_option_enabled(multiworld, player, "Playing_Pursuitcore"):
            survivorAmount += 1
            killerAmount += 1
            gamesPlayed += 1
        if is_option_enabled(multiworld, player, "Playing_Break_in_and_Steal_Thingz"):
            survivorAmount += 0
            killerAmount += 1
            gamesPlayed += 1

        if survivorAmount > 3 and move_sanity:
            survivorAmount = 5
        else:
            survivorAmount = 3
        if killerAmount > 2:
            killerAmount = 2
        if gamesPlayed == 1:
            survivorAmount = 2
            killerAmount = 1

        # Only fill in amounts not already covered by an explicit override
        if override_survivors == -1:
            startingItems.extend(pick_unique(Surv_Map, survivorAmount))
        if override_killers == -1:
            startingItems.extend(pick_unique(Kill_Map, killerAmount))

    elif override_survivors == -1 and override_killers == -1:
        # Neither auto-balance nor any override set: use flat defaults
        startingItems.extend(pick_unique(Surv_Map, 2))
        startingItems.extend(pick_unique(Kill_Map, 1))

    else:
        # Auto-balance off, but one override was set and the other wasn't — default the unset one
        if override_survivors == -1:
            startingItems.extend(pick_unique(Surv_Map, 2))
        if override_killers == -1:
            startingItems.extend(pick_unique(Kill_Map, 1))
    
    #Don't mind the noonly code sneaking in here (This is for starting Skins)
    startingItems.extend(get_option_value(multiworld, player, "Starting_Skins"))
    
    for itemName in startingItems:
        item = next((i for i in item_pool if i.name == itemName), None)
        if item is None:
            continue
        remove_specific_item(item_pool, item)
        multiworld.push_precollected(item)

    #Edits the amount of Wintokens necessary to win
    for location in location_table:
        if location["name"] == "Win (Collect your necessary amount of Wintokens)":
            location["requires"] = f"|Wintoken: {world.options.Wintoken_Amount.value}|"
    # Edits the requirements of the goal location collect all Characters
    requirementssurvivors = []
    if is_option_enabled(multiworld, player, "Playing_Forsaken") and not is_option_enabled(multiworld, player, "Move_Sanity"):
        requiresforsaken = {
            "noob": "|Noob (Forsaken)|",
            "007n7": "|007n7|",
            "veeronica": "|Veeronica|",
            "shedletsky": "|Shedletsky|",
            "guest 1337": "|Guest 1337|",
            "taph": "|Taph|",
            "dusekkar": "|Dusekkar|",
            "jane doe": "|Jane Doe|",
            "two time": "|Two Time|",
            "chance": "|Chance|",
            "elliot": "|Elliot|",
            "builderman": "|Builderman|"
        }
        for character, requirement in requiresforsaken.items():
            if character not in world.options.Forsaken_Exclude.value:
                requirementssurvivors.append(requirement)
    if is_option_enabled(multiworld, player, "Playing_Forsaken") and is_option_enabled(multiworld, player, "Move_Sanity"):
        requiresforsaken = {
            "noob": "|Bloxy Cola| AND |Slateskin Potion| AND |GhostBurger|",
            "elliot": "|Pizza Toss| AND |Rush Hour|",
            "shedletsky": "|Slash| AND |Fried Chicken|",
            "007n7": "|Clone| AND |C00LGUI| AND |Inject|",
            "veeronica": "|Sk8| AND |Broadcast| AND |Activate Battery|",
            "guest 1337": "|Guest Block| AND |Charge| AND |Guest Punch|",
            "two time": "|Sacrificial Dagger| AND |Crouch| AND |Pray| AND |Ritual|",
            "chance": "|Coin Flip| AND |One Shot| AND |Chance Reroll| AND |Hat Fix|",
            "builderman": "|Sentry| AND |Dispenser| AND |Carry|",
            "taph": "|Taph Tripwire| AND |Subspace Tripmine|",
            "dusekkar": "|Plasma Beam| AND |Spawn Protection|",
            "jane doe": "|Crystal Pitch| AND |Hatchet|",
        }
        for character, requirement in requiresforsaken.items():
            if character not in world.options.Forsaken_Exclude.value:
                requirementssurvivors.append(requirement)
        
    if is_option_enabled(multiworld, player, "Playing_Die_Of_Death"):
        requiresdod = {
            "punch": "|Punch|",
            "block": "|Block|",
            "banana peel": "|Banana Peel|",
            "dash": "|Dash|",
            "caretaker": "|Caretaker|",
            "bonuspad": "|Bonuspad|",
            "taunt": "|Taunt|",
            "revolver": "|Revolver|",
            "adrenaline": "|Adrenaline|",
            "cloak": "|Cloak|",
            "hotdog": "|Hotdog|",
            "reroll": "|Reroll|",
            "pie": "|Pie|",
            "bugle": "|Bugle|",
            "flashlight": "|Flashlight|",
        }
        for character, requirement in requiresdod.items():
            if character not in world.options.DoD_Exclude.value:
                requirementssurvivors.append(requirement)
    if is_option_enabled(multiworld, player, "Playing_Outcome_Memories") and not is_option_enabled(multiworld, player, "Move_Sanity"):
        requiresom = {
            "sonic": "|Sonic|",
            "knuckles": "|Knuckles|",
            "amy": "|Amy|",
            "cream": "|Cream|",
            "tails": "|Tails|",
            "eggman": "|Eggman|",
            "metal sonic": "|Metal Sonic|",
            "blaze": "|Blaze|",
            "silver": "|Silver|",
        }
        for character, requirement in requiresom.items():
            if character not in world.options.OM_Exclude.value:
                requirementssurvivors.append(requirement)
    if is_option_enabled(multiworld, player, "Playing_Outcome_Memories") and is_option_enabled(multiworld, player, "Move_Sanity"):
        requiresom = {
            "sonic": "|Dropdash| AND |Peelout|",
            "tails": "|Laser Cannon| AND |Glide|",
            "knuckles": "|Knuckles Punch| AND |Counter|",
            "amy": "|Hammer| AND |Hammer Throw| AND |Amy Reroll|",
            "cream": "|Heal| AND |Cream Dash| AND |Glide|",
            "eggman": "|Jetpack Boost| AND |Energy Shield|",
            "metal sonic": "|Destructive Charge| AND |Self Repair|",
            "blaze": "|Roundhouse Kick/Sol Dash/Sol Boost| AND |Burning Javelin/Sol Flame|",
            "silver": "|Suspension| AND |Rock Throw| AND |Time Reversal|",
        }
        for character, requirement in requiresom.items():
            if character not in world.options.OM_Exclude.value:
                requirementssurvivors.append(requirement)
        
    if is_option_enabled(multiworld, player, "Playing_Scream_Jam"):
        requiressj = {
            "pancho": "|Pancho|",
            "bloxxer": "|Bloxxer|",
            "mrrobot": "|MrRobot|",
            "betty": "|Betty|",
            "calindra": "|Calindra|",
            "jimmy": "|Jimmy|",
            "clockwork": "|Clockwork|",
        }
        for character, requirement in requiressj.items():
            if character not in world.options.SJ_Exclude.value:
                requirementssurvivors.append(requirement)
    
    if is_option_enabled(multiworld, player, "Playing_Pursuitcore"):
        requiresps = {
            "dante": "|Dante|",
            "mikaela": "|Mikaela|",
            "nyan": "|Nyan|",
            "fukatsuki": "|Fukatsuki|",
            "crafter": "|Crafter|",
            "vinnie": "|Vinnie|",
            "tac9": "|Tac9|",
            "roflpix": "|Roflpix|"
        }
        for character, requirement in requiresps.items():
            if character not in world.options.PS_Exclude.value:
                requirementssurvivors.append(requirement)
                
    if is_option_enabled(multiworld, player, "Playing_Just_One_More_Asym"):
        requiresjoma = {
            "noob (joma)": "|Noob (JOMA)|",
            "doctor": "|Doctor|",
            "jester": "|Jester|",
            "assistant": "|Assistant|",
            "brawler": "|Brawler|",
            "firefighter": "|Firefighter|",
            "shielder": "|Shielder|",
            "knight": "|Knight|",
            "maniac": "|Maniac|",
            "wrecker": "|Wrecker|",
            "guest (joma)": "|Guest (JOMA)|",
            "hemomancer": "|Hemomancer|",
            "sniper": "|Sniper|",
            "vocalist": "|Vocalist|",
            "sherrif": "|Sherrif|"
        }
        for character, requirement in requiresjoma.items():
            if character not in world.options.JOMA_Exclude.value:
                requirementssurvivors.append(requirement)
    
        print(requirementssurvivors)
    for location in location_table:
        if location["name"] == "Win (Collect all Survivors)":
            location["requires"] = " AND ".join(requirementssurvivors)
            
    requirementskillers = []
    
    if is_option_enabled(multiworld, player, "Playing_Forsaken") and not is_option_enabled(multiworld, player, "Move_Sanity"):
        requiresforsaken = {
            "noob": "|Noob (Forsaken)|",
            "shedletsky": "|Shedletsky|",
            "007n7": "|007n7|",
            "veeronica": "|Veeronica|",
            "guest 1337": "|Guest 1337|",
            "taph": "|Taph|",
            "dusekkar": "|Dusekkar|",
            "jane doe": "|Jane Doe|",
            "two time": "|Two Time|",
            "chance": "|Chance|",
            "elliot": "|Elliot|",
            "builderman": "|Builderman|",
            "slasher": "|Slasher|",
            "coolkidd": "|Coolkidd|",
            "john doe": "|John Doe|",
            "noli": "|Noli|",
            "1x1x1x1": "|1x1x1x1|",
            "guest 666": "|Guest 666|",
            "nosferatu": "|Nosferatu|",
            "azure": "|Azure|",
        }
        for character, requirement in requiresforsaken.items():
            if character not in world.options.Forsaken_Exclude.value:
                requirementskillers.append(requirement)
    if is_option_enabled(multiworld, player, "Playing_Forsaken") and is_option_enabled(multiworld, player, "Move_Sanity"):
        requiresforsakenmoves = {
            "noob": "|Bloxy Cola| AND |Slateskin Potion| AND |GhostBurger|",
            "elliot": "|Pizza Toss| AND |Rush Hour|",
            "shedletsky": "|Slash| AND |Fried Chicken|",
            "007n7": "|Clone| AND |C00LGUI| AND |Inject|",
            "veeronica": "|Vandalism| AND |Sk8| AND |Broadcast| AND |Activate Battery|",
            "guest 1337": "|Guest Block| AND |Charge| AND |Guest Punch|",
            "two time": "|Sacrificial Dagger| AND |Crouch| AND |Ritual| AND |Pray|",
            "chance": "|Coin Flip| AND |One Shot| AND |Chance Reroll| AND |Hat Fix|",
            "builderman": "|Sentry| AND |Dispenser| AND |Carry|",
            "taph": "|Taph Tripwire| AND |Subspace Tripmine|",
            "dusekkar": "|Plasma Beam| AND |Spawn Protection|",
            "jane doe": "|Crystal Pitch| AND |Hatchet|",
            "slasher": "|Slasher|",
            "coolkidd": "|Coolkidd|",
            "john doe": "|John Doe|",
            "noli": "|Noli|",
            "1x1x1x1": "|1x1x1x1|",
            "guest 666": "|Guest 666|",
            "nosferatu": "|Nosferatu|",
            "azure": "|Azure|"
        }
        for character, requirement in requiresforsakenmoves.items():
            if character not in world.options.Forsaken_Exclude.value:
                requirementskillers.append(requirement)
    
    if is_option_enabled(multiworld, player, "Playing_Die_Of_Death"):
        requiresdod = {
            "punch": "|Punch|",
            "block": "|Block|",
            "banana peel": "|Banana Peel|",
            "dash": "|Dash|",
            "caretaker": "|Caretaker|",
            "bonuspad": "|Bonuspad|",
            "taunt": "|Taunt|",
            "revolver": "|Revolver|",
            "adrenaline": "|Adrenaline|",
            "cloak": "|Cloak|",
            "hotdog": "|Hotdog|",
            "reroll": "|Reroll|",
            "pie": "|Pie|",
            "bugle": "|Bugle|",
            "flashlight": "|Flashlight|",
            "pursuer": "|Pursuer|",
            "badware": "|Badware|",
            "artful": "|Artful|",
            "harken": "|Harken|",
            "killdroid": "|Killdroid|",
        }
        for character, requirement in requiresdod.items():
            if character not in world.options.DoD_Exclude.value:
                requirementskillers.append(requirement)
        
    if is_option_enabled(multiworld, player, "Playing_Outcome_Memories") and not is_option_enabled(multiworld, player, "Move_Sanity"):
        requiresom = {
            "sonic": "|Sonic|",
            "knuckles": "|Knuckles|",
            "amy": "|Amy|",
            "cream": "|Cream|",
            "tails": "|Tails|",
            "eggman": "|Eggman|",
            "metal sonic": "|Metal Sonic|",
            "blaze": "|Blaze|",
            "silver": "|Silver|",
            "2011x": "|2011x|",
            "kolossos": "|Kolossos|",
            "tripwire": "|Tripwire|",
            "fleetway": "|Fleetway|",
        }
        for character, requirement in requiresom.items():
            if character not in world.options.OM_Exclude.value:
                requirementskillers.append(requirement)
    if is_option_enabled(multiworld, player, "Playing_Outcome_Memories") and is_option_enabled(multiworld, player, "Move_Sanity"):
        requiresommoves = {
            "sonic": "|Dropdash| AND |Peelout|",
            "tails": "|Laser Cannon| AND |Glide|",
            "knuckles": "|Knuckles Punch| AND |Counter|",
            "amy": "|Hammer| AND |Hammer Throw| AND |Amy Reroll|",
            "cream": "|Heal| AND |Cream Dash| AND |Glide|",
            "eggman": "|Jetpack Boost| AND |Energy Shield|",
            "metal sonic": "|Destructive Charge| AND |Self Repair|",
            "blaze": "|Roundhouse Kick/Sol Dash/Sol Boost| AND |Burning Javelin/Sol Flame|",
            "silver": "|Suspension| AND |Rock Throw| AND |Time Reversal|",
            "2011x": "|2011x|",
            "kolossos": "|Kolossos|",
            "tripwire": "|Tripwire|",
            "fleetway": "|Fleetway|",
        }
        for character, requirement in requiresommoves.items():
            if character not in world.options.OM_Exclude.value:
                requirementskillers.append(requirement)
        
    if is_option_enabled(multiworld, player, "Playing_Scream_Jam"):
        requiressj = {
            "pancho": "|Pancho|",
            "bloxxer": "|Bloxxer|",
            "mrrobot": "|MrRobot|",
            "betty": "|Betty|",
            "calindra": "|Calindra|",
            "jimmy": "|Jimmy|",
            "clockwork": "|Clockwork|",
            "killerkyle": "|KillerKyle|",
            "fencer": "|Fencer|",
            "clawsguy": "|ClawsGuy|",
            "frapers": "|Frapers|",
            "stalker": "|Stalker|",
        }
        for character, requirement in requiressj.items():
            if character not in world.options.SJ_Exclude.value:
                requirementskillers.append(requirement)
        
    if is_option_enabled(multiworld, player, "Playing_Pursuitcore"):
        requiresps = {
            "dante": "|Dante|",
            "mikaela": "|Mikaela|",
            "nyan": "|Nyan|",
            "fukatsuki": "|Fukatsuki|",
            "crafter": "|Crafter|",
            "vinnie": "|Vinnie|",
            "tac9": "|Tac9|",
            "roflpix": "|Roflpix|",
            "partypwny": "|Partypwny|",
            "dotx": "|DotX|",
            "blankstare": "|Blankstare|",
            "sweep": "|Sweep|",
            "captain limewire": "|Captain Limewire|",
            "jack noir": "|Jack Noir|",
        }
        for character, requirement in requiresps.items():
            if character not in world.options.PS_Exclude.value:
                requirementskillers.append(requirement)
                
    if is_option_enabled(multiworld, player, "Playing_Break_in_and_Steal_Thingz"):
        requiresbiast = {
            "slacker": "|Slacker|",
            "trapper": "|Trapper|",
            "cubedhexa22": "|CubedHexa22|",
            "observer": "|Observer|",
            "ashle": "|Ashle|"
        }
        for character, requirement in requiresbiast.items():
            if character not in world.options.BIAST_Exclude.value:
                requirementskillers.append(requirement)
                
    if is_option_enabled(multiworld, player, "Playing_Just_One_More_Asym"):
        requiresjoma = {
            "noob (joma)": "|Noob (JOMA)|",
            "doctor": "|Doctor|",
            "jester": "|Jester|",
            "assistant": "|Assistant|",
            "brawler": "|Brawler|",
            "firefighter": "|Firefighter|",
            "shielder": "|Shielder|",
            "knight": "|Knight|",
            "maniac": "|Maniac|",
            "wrecker": "|Wrecker|",
            "guest (joma)": "|Guest (JOMA)|",
            "hemomancer": "|Hemomancer|",
            "sniper": "|Sniper|",
            "vocalist": "|Vocalist|",
            "sherrif": "|Sherrif|",
            "spotter": "|Spotter|",
            "dullahan": "|Dullahan|",
            "anarchist": "|Anarchist|",
            "executioner": "|Executioner|",
            "firework": "|Firework|",
            "chronos": "|Chronos|",
            "hunter": "|Hunter|",
            "chaser": "|Chaser|",
            "sin": "|Sin|",
            "apprentice": "|Apprentice|",
            "flarereaver": "|Flarereaver|",
            "custodian": "|Custodian|"
        }
        for character, requirement in requiresjoma.items():
            if character not in world.options.JOMA_Exclude.value:
                requirementskillers.append(requirement) 
        
    for location in location_table:
        if location["name"] == "Win (Collect all Survivors and Killers)":
            location["requires"] = " AND ".join(requirementskillers)
            
    #Collect Specified Amount of Survivors win con
    for location in location_table:
        if location["name"] == "Win (Collect Specified amount of Survivors)":
            location["requires"] = f'|@Survivors: {get_option_value(multiworld, player, "Survivors_Needed")}|'
            
    #Collect Specified Amount of Survivors and Killers win con
    for location in location_table:
        if location["name"] == "Win (Collect Specified amount of Survivors and Killers)":
            location["requires"] = (
            f'|@All Survivors: {get_option_value(multiworld, player, "Survivors_Needed")}| '
            f'AND |@All Killers: {get_option_value(multiworld, player, "Killers_Needed")}|'
            )
            
    return item_pool

# The item pool after starting items are processed but before filler is added, in case you want to see the raw item pool at that stage
def before_create_items_filler(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    # Use this hook to remove items from the item pool
    itemNamesToRemove: list[str] = [] # List of item names

    # Add your code here to calculate which items to remove.
    #
    # Because multiple copies of an item can exist, you need to add an item name
    # to the list multiple times if you want to remove multiple copies of it.
    for itemName in itemNamesToRemove:
        item = next(i for i in item_pool if i.name == itemName)
        remove_specific_item(item_pool, item)

    return item_pool

    # Some other useful hook options:

    ## Place an item at a specific location
    # location = next(l for l in multiworld.get_unfilled_locations(player=player) if l.name == "Location Name")
    # item_to_place = next(i for i in item_pool if i.name == "Item Name")
    # location.place_locked_item(item_to_place)
    # remove_specific_item(item_pool, item_to_place)

# The complete item pool prior to being set for generation is provided here, in case you want to make changes to it
def after_create_items(item_pool: list, world: World, multiworld: MultiWorld, player: int) -> list:
    skin_items = ["007n7 Skin - 118o8", "C00lkidd Skin - bluudud", "Two Time Skin - Ghoul", "1x1x1x1 Skin - Diva", "Shedletsky Skin - The Heartbroken", "1x1x1x1 Skin - Hacklord", "Noob Skin - Taunt", "Shedletsky Skin - Hot Dog", "Elliot Skin - Caretaker", "Builderman Skin - Carepad", "Guest 1337 Skin - Block", "Two Time Skin - Cloak", "Taph Skin - Banana", "Chance Skin - Revolver", "Chance Skin - Loveshot", "Slasher Skin - Pursuer", "Noli Skin - Artful", "Noli Skin - Devesto", "Guest 1337 Skin - Guard", "1x1x1x1 Skin - The Pestilence", "Noli Skin - The Possessed", "Dusekkar Skin - Golden", "Shedletsky Skin - Golden", "Chance Skin - Golden", "C00lkidd Skin - P4rtyPwny", "Elliot Skin - Friend", "John Doe Skin - Annihilation", "Slasher Skin - Vanity", "John Doe Skin - Gasharpoon"]
    if not (world.options.Playing_Forsaken.value == True and world.options.Include_Forsaken_Skin_LMS_Tasks.value == True and world.options.Include_Forsaken_LMS_Tasks.value == True):
        for item in item_pool:
            if item.name in skin_items:
                item.classification = ItemClassification.filler
    return item_pool

# Called before rules for accessing regions and locations are created. Not clear why you'd want this, but it's here.
def before_set_rules(world: World, multiworld: MultiWorld, player: int):
    pass

# Called after rules for accessing regions and locations are created, in case you want to see or modify that information.
def after_set_rules(world: World, multiworld: MultiWorld, player: int):
    # Use this hook to modify the access rules for a given location

    def Example_Rule(state: CollectionState) -> bool:
        # Calculated rules take a CollectionState object and return a boolean
        # True if the player can access the location
        # CollectionState is defined in BaseClasses
        return True

    ## Common functions:
    # location = world.get_location(location_name, player)
    # location.access_rule = Example_Rule

    ## Combine rules:
    # old_rule = location.access_rule
    # location.access_rule = lambda state: old_rule(state) and Example_Rule(state)
    # OR
    # location.access_rule = lambda state: old_rule(state) or Example_Rule(state)

# The item name to create is provided before the item is created, in case you want to make changes to it
def before_create_item(item_name: str, world: World, multiworld: MultiWorld, player: int) -> str:
    return item_name

# The item that was created is provided after creation, in case you want to modify the item
def after_create_item(item: ManualItem, world: World, multiworld: MultiWorld, player: int) -> ManualItem:
    return item

# This method is run towards the end of pre-generation, before the place_item options have been handled and before AP generation occurs
def before_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is run at the very end of pre-generation, once the place_item options have been handled and before AP generation occurs
def after_generate_basic(world: World, multiworld: MultiWorld, player: int):
    pass

# This method is run every time an item is added to the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be cancelled/undone in after_remove_item
def after_collect_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you add to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] += 1
    pass

# This method is run every time an item is removed from the state, can be used to modify the value of an item.
# IMPORTANT! Any changes made in this hook must be first done in after_collect_item
def after_remove_item(world: World, state: CollectionState, Changed: bool, item: Item):
    # the following let you undo the addition to the Potato Item Value count
    # if item.name == "Cooked Potato":
    #     state.prog_items[item.player][format_state_prog_items_key(ProgItemsCat.VALUE, "Potato")] -= 1
    pass


# This is called before slot data is set and provides an empty dict ({}), in case you want to modify it before Manual does
def before_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called after slot data is set and provides the slot data at the time, in case you want to check and modify it after Manual is done with it
def after_fill_slot_data(slot_data: dict, world: World, multiworld: MultiWorld, player: int) -> dict:
    return slot_data

# This is called right at the end, in case you want to write stuff to the spoiler log
def before_write_spoiler(world: World, multiworld: MultiWorld, spoiler_handle) -> None:
    pass

# This is called when you want to add information to the hint text
def before_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:

    ### Example way to use this hook:
    # if player not in hint_data:
    #     hint_data.update({player: {}})
    # for location in multiworld.get_locations(player):
    #     if not location.address:
    #         continue
    #
    #     use this section to calculate the hint string
    #
    #     hint_data[player][location.address] = hint_string

    pass

def after_extend_hint_information(hint_data: dict[int, dict[int, str]], world: World, multiworld: MultiWorld, player: int) -> None:
    pass

def hook_interpret_slot_data(world: World, player: int, slot_data: dict[str, Any]) -> dict[str, Any]:
    """
        Called when Universal Tracker wants to perform a fake generation
        Use this if you want to use or modify the slot_data for passed into re_gen_passthrough
    """
    return slot_data
