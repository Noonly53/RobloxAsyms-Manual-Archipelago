# Object classes from AP that represent different types of options that you can create
from Options import Option, FreeText, NumericOption, Toggle, DefaultOnToggle, Choice, TextChoice, Range, NamedRange, OptionGroup, PerGameCommonOptions, OptionSet
# These helper methods allow you to determine if an option has been set, or what its value is, for any player in the multiworld
from ..Helpers import is_option_enabled, get_option_value
from typing import Type, Any


####################################################################
# NOTE: At the time that options are created, Manual has no concept of the multiworld or its own world.
#       Options are defined before the world is even created.
#
# Example of creating your own option:
#
#   class MakeThePlayerOP(Toggle):
#       """Should the player be overpowered? Probably not, but you can choose for this to do... something!"""
#       display_name = "Make me OP"
#
#   options["make_op"] = MakeThePlayerOP
#
#
# Then, to see if the option is set, you can call is_option_enabled or get_option_value.
#####################################################################


# To add an option, use the before_options_defined hook below and something like this:
#   options["total_characters_to_win_with"] = TotalCharactersToWinWith
#
class MoveSanity(Toggle):
    """Replaces survivors with their individual moves. Currently only supports Forsaken and Outcome Memories"""
    display_name = "Move Sanity"
    
class WintokenAmount(Range):
    """The amount of Wintokens needed to win the game. Leads to faster or slower completion
    Only contributes to the goal if your goal is: Win (Collect your necessary amount of Wintokens)"""
    display_name = "Wintoken Amount"
    range_start = 5
    range_end = 40
    default = 15

class SurvivorsNeeded(Range):
    """The amount of Survivors needed to win the game. Leads to faster or slower completion
    Only contributes to the goal if your goal is: Win (Collect Specified amount of Survivors) OR: Win (Collect Specified amount of Survivors and Killers)
    THIS NUMBER MUST BE WITHIN THE TOTAL AMOUNT OF SURVIVORS GIVEN WHAT GAMES YOU HAVE ACTIVE, AND WHAT SURVIVORS ARE EXCLUDED PLEASE EXCERCIZE CAUTION"""
    display_name = "Survivors Needed"
    range_start = 1
    range_end = 50
    default = 12
    
class KillersNeeded(Range):
    """The amount of Killers needed to win the game. Leads to faster or slower completion
    Only contributes to the goal if your goal is: Win (Collect Specified amount of Survivors and Killers)
    THIS NUMBER MUST BE WITHIN THE TOTAL AMOUNT OF KILLERS GIVEN WHAT GAMES YOU HAVE ACTIVE, AND WHAT KILLERS ARE EXCLUDED PLEASE EXCERCIZE CAUTION"""
    display_name = "Killers Needed"
    range_start = 1
    range_end = 29
    default = 8

class AutoBalanceStartingCharacterAmount(Toggle):
    """Automatically starts the player with an amount of Killers and Survivors based on the amount of selected games."""
    display_name = "Auto Balance Starting Character Amount"
    default = 1

class OverRideKillerStartingAmount(NamedRange):
    """Overrides the amount of killers the player starts with. Default (-1) Disables the setting"""
    display_name = "Override Starting Killer Amount"
    default = -1
    range_start = 0
    range_end = 10
    special_range_names = {"off": -1}

class OverRideSurvivorStartingAmount(NamedRange):
    """Overrides the amount of survivors the player starts with. Default (-1) Disables the setting"""
    display_name = "Override Starting Survivor Amount"
    default = -1
    range_start = 0
    range_end = 10
    special_range_names = {"off": -1}

class PlayingForsaken(Toggle):
    """Enables Forsaken in generation"""
    display_name = "Playing Forsaken"
    
class ForsakenGens(Toggle):
    """Adds Maps as Items and Generator Spawns as locations. Highly recommend using the Poptracker for this. You do not need maps to play on them (Unless you want to do that)"""
    display_name = "Forsaken Gensanity"
    
class KillerDoors(Toggle):
    """Adds an item that dictates how many times you may use a killer door in each killer round"""
    display_name = "Include Killer Doors"
    
class KillerDoorsAmount(Range):
    """Determines the amount of Killer Door items that are included with the last option enabled"""
    display_name = "Killer Door Amount"
    default = 10
    range_start = 5
    range_end = 30
    
class ForsakenMisc(Toggle):
    """Include many random extra tasks that may take longer to complete. Includes winning on each map"""
    display_name = "Include Forsaken Misc Tasks"
    
class ForsakenLMS(Toggle):
    """Include locations that require you to win on either side of a special Last Man Standing in Forsaken"""
    display_name = "Include Forsaken LMS Tasks"
    
class ForsakenSkinLMS(Toggle):
    """Ditto for the last option, except skins that have a special LMS are added and checks for their LMS are added (DOES NOT INCLUDE BADGE SKINS FROM OTHER GAMES)"""
    display_name = "Include Forsaken Skin LMS Tasks"
    
class Trickstabs(Toggle):
    """Includes two extra locations if you are able to trickstab as Two Time"""
    display_name = "Harder Two Time Tasks"
    
class ReactBlocks(Toggle):
    """Includes two extra locations if you are able to react block as Guest 1337"""
    display_name = "Harder Guest 1337 Tasks"
    
class ForsakenExclude(OptionSet):
    """Exclude chosen characters in Forsaken"""
    display_name = "Forsaken Characters Excluded"
    valid_keys = frozenset([
        "noob",
        "elliot",
        "shedletsky",
        "007n7",
        "veeronica",
        "guest 1337",
        "two time",
        "chance",
        "builderman",
        "taph",
        "dusekkar",
        "slasher",
        "c00lkidd",
        "john doe",
        "noli",
        "1x1x1x1",
        "guest 666",
        "nosferatu",
        "azure",
    ])
    default = frozenset([])
    
class PlayingDoD(Toggle):
    """Enables Die of Death in generation"""
    display_name = "Playing Die of Death"
    
class DoDMisc(Toggle):
    """Include many random extra tasks that may take longer to complete. Includes winning on each map"""
    display_name = "Include Die of Death Misc Tasks"
    
class DoDLMS(Toggle):
    """Include locations that require you to win on either side of a special Last Man Standing in Die of Death"""
    display_name = "Include Die of Death LMS Tasks"
    
class DoDSynergies(Toggle):
    """Include special movesets as items in Die of Death such as Loveshot, Carepad, Noisemaker, and SweetTooth"""
    display_name = "Include Die of Death Synergies"
    
class DoDExclude(OptionSet):
    """Exclude chosen characters in DoD"""
    display_name = "Die of Death Characters Excluded"
    valid_keys = frozenset([
        "adrenaline",
        "banana peel",
        "bonuspad",
        "block",
        "bugle",
        "caretaker",
        "cloak",
        "dash",
        "hotdog",
        "pie",
        "punch",
        "revolver",
        "taunt",
        "flashlight",
        "reroll",
        "pursuer",
        "badware",
        "killdroid",
        "harken",
        "artful"
    ])
    default = frozenset([])
    
class PlayingOM(Toggle):
    """Enables Outcome Memories in generation"""
    display_name = "Playing Outcome Memories"
    
class OMMap(Toggle):
    """Includes surviving on each map as a location in outcome memories"""
    display_name = "Include Outcome Memories Map Tasks"
    
class OMExclude(OptionSet):
    """Exclude chosen characters in Outcome Memories"""
    display_name = "Outcome Memories Characters Excluded"
    valid_keys = frozenset([
        "sonic",
        "tails",
        "knuckles",
        "eggman",
        "amy",
        "cream",
        "metal sonic",
        "silver",
        "blaze",
        "2011x",
        "kolossos",
        "tripwire",
        "fleetway"
    ])
    default = frozenset([])
    
class PlayingSJ(Toggle):
    """Enables Scream Jam in generation"""
    display_name = "Playing Scream Jam"
    
class SJExclude(OptionSet):
    """Exclude chosen characters in Scream Jam"""
    display_name = "Scream Jam Characters Excluded"
    valid_keys = frozenset([
        "pancho",
        "bloxxer",
        "mrrobot",
        "betty",
        "calindra",
        "jimmy",
        "clockwork",
        "killerkyle",
        "fencer",
        "clawsguy",
        "frapers",
        "stalker"
    ])
    default = frozenset([])

class PlayingPS(Toggle):
    """Enables Pursuitcore in generation"""
    display_name = "Playing Pursuitcore"

class TheKit(Toggle):
    """Includes The Kit as a recievable User in Pursuitcore, a character earned by winning IWBTU as the User"""
    display_name = "Include The Kit"
    
class PSMisc(Toggle):
    """Include many random extra tasks that may take longer to complete. Includes winning on each map, Special Rounds and Zombie Tasks"""
    display_name = "Include Pursuitcore Misc Tasks"

class PSExclude(OptionSet):
    """Exclude chosen characters in PursuitCore"""
    display_name = "Pursuitcore Characters Excluded"
    valid_keys = frozenset([
        "dante",
        "nyan",
        "mikaela",
        "fukatsuki",
        "vinnie",
        "crafter",
        "tac9",
        "roflpix",
        "kit",
        "partypwny",
        "dotx",
        "blankstare",
        "sweep",
        "captain lime",
        "jack noir"
    ])
    default = frozenset([])
    
class PlayingBIAST(Toggle):
    """Enables Break in and Steal Thingz in generation
    Disclaimer: Since BIAST Does not have any set survivors. The following win condition is unviable to use: (Collect all Survivors)"""
    display_name = "Playing Break in and Steal Thingz"
    
class BIASTVIP(Toggle):
    """Includes Killers or Characters that need VIP to use. Currently just Jeff the Killer"""
    display_name = "Include Early Access Killer"
    
class BIASTMap(Toggle):
    """Include checks that are relative to each map"""
    display_name = "Include Map Tasks"
    
class BIASTExclude(OptionSet):
    """Exclude chosen killers in Break in and Steal Thingz"""
    display_name = "Break in and Steal Thingz Killers Excluded"
    valid_keys = frozenset([
        "slacker",
        "trapper",
        "cubedhexa22",
        "observer",
        "ashle"
    ])
    default = frozenset([])

# This is called before any manual options are defined, in case you want to define your own with a clean slate or let Manual define over them
def before_options_defined(options: dict[str, Type[Option[Any]]]) -> dict[str, Type[Option[Any]]]:
    options["Move_Sanity"] = MoveSanity
    options["Wintoken_Amount"] = WintokenAmount
    options["Survivors_Needed"] = SurvivorsNeeded
    options["Killers_Needed"] = KillersNeeded
    options["Include_Killer_Doors"] = KillerDoors
    options["Killer_Door_Amount"] = KillerDoorsAmount
    options["Playing_Forsaken"] = PlayingForsaken
    options["Gensanity"] = ForsakenGens
    options["Include_Forsaken_Misc_Tasks"] = ForsakenMisc
    options["Include_Forsaken_LMS_Tasks"] = ForsakenLMS
    options["Include_Forsaken_Skin_LMS_Tasks"] = ForsakenSkinLMS
    options["Can_Trickstab_as_Two_Time"] = Trickstabs
    options["Can_React_Block_as_Guest_1337"] = ReactBlocks
    options["Forsaken_Exclude"] = ForsakenExclude
    options["Playing_Die_of_Death"] = PlayingDoD
    options["Include_DoD_Misc_Tasks"] = DoDMisc
    options["DoD_LMS_Tasks"] = DoDLMS
    options["Include_DoD_Synergies"] = DoDSynergies
    options["DoD_Exclude"] = DoDExclude
    options["Playing_Outcome_Memories"] = PlayingOM
    options["Include_Outcome_Memories_Map_Tasks"] = OMMap
    options["OM_Exclude"] = OMExclude
    options["Playing_Scream_Jam"] = PlayingSJ
    options["SJ_Exclude"] = SJExclude
    options["Playing_Pursuitcore"] = PlayingPS
    options["Include_The_Kit"] = TheKit
    options["Include_Pursuitcore_Misc_Tasks"] = PSMisc
    options["PS_Exclude"] = PSExclude
    options["Playing_Break_in_and_Steal_Thingz"] = PlayingBIAST
    options["Include_Early_Access_Killer"] = BIASTVIP
    options["Include_Map_Tasks"] = BIASTMap
    options["BIAST_Exclude"] = BIASTExclude
    
    #Options Added By StudMuffin, put a # in front of these if you need to push an update and it breaks these, and someone isnt able to fix them.
    options["Auto_Balance_Starting_Amount"] = AutoBalanceStartingCharacterAmount
    options["Override_Starting_Killers"] = OverRideKillerStartingAmount
    options["Override_Starting_Survivors"] = OverRideSurvivorStartingAmount
    return options

# This is called after any manual options are defined, in case you want to see what options are defined or want to modify the defined options
def after_options_defined(options: Type[PerGameCommonOptions]):
    # To access a modifiable version of options check the dict in options.type_hints
    # For example if you want to change DLC_enabled's display name you would do:
    # options.type_hints["DLC_enabled"].display_name = "New Display Name"

    #  Here's an example on how to add your aliases to the generated goal
    # options.type_hints['goal'].aliases.update({"example": 0, "second_alias": 1})
    # options.type_hints['goal'].options.update({"example": 0, "second_alias": 1})  #for an alias to be valid it must also be in options

    pass

# Use this Hook if you want to add your Option to an Option group (existing or not)
def before_option_groups_created(groups: dict[str, list[Type[Option[Any]]]]) -> dict[str, list[Type[Option[Any]]]]:
    # Uses the format groups['GroupName'] = [TotalCharactersToWinWith]
    groups['Global Things'] = [MoveSanity, WintokenAmount, SurvivorsNeeded, KillersNeeded, KillerDoors, KillerDoorsAmount, AutoBalanceStartingCharacterAmount, OverRideKillerStartingAmount, OverRideSurvivorStartingAmount]
    groups['Forsaken'] = [PlayingForsaken, ForsakenGens, ForsakenMisc, ForsakenLMS, ForsakenSkinLMS, Trickstabs, ReactBlocks]
    groups['Die of Death'] = [PlayingDoD, DoDMisc, DoDLMS, DoDSynergies]
    groups['Outcome Memories'] = [PlayingOM, OMMap]
    groups['Scream Jam'] = [PlayingSJ]
    groups['Pursuitcore'] = [PlayingPS, TheKit, PSMisc]
    groups['Break in and Steal Thingz'] = [PlayingBIAST, BIASTVIP, BIASTMap]
    groups['Character Exclusion'] = [ForsakenExclude, DoDExclude, OMExclude, SJExclude, PSExclude, BIASTExclude]
    return groups

def after_option_groups_created(groups: list[OptionGroup]) -> list[OptionGroup]:
    return groups
