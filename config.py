import tkinter as tk

from models.classes import *

# Flags
bestiary_flag = None
clear_flag = None
regions_flag = None
button_flag = None
back_flag = None
party_flag = None
last_flag = None
parent_flag = None
nav_stack = ['Main']
nav_stack_context = [('Main', None)]

VALID_MAP = {
            "artificer": Artificer,
            "barbarian": Barbarian,
            "bard": Bard,
            "cleric": Cleric,
            "druid": Druid,
            "fighter": Fighter,
            "monk": Monk,
            "paladin": Paladin,
            "ranger": Ranger,
            "rogue": Rogue,
            "sorcerer": Sorcerer,
            "warlock": Warlock,
            "wizard": Wizard,
        }

# Button Labels
MAIN_PAGE_BUTTON_LABELS = [
    "Label: Campaign Info",
    "Party and NPCs",
    "Bestiary",
    "Regions",
    "Line Break",
    "Label: Navigation",
    "Generators",
    "Settings",
    "Close Program"
]
MANAGE_PARTY_BUTTON_LABELS = [
    "Label: Party Management",
    "Add Party Member",
    "Update Party Member",
    "Delete Party Member",
    "Line Break",
    "Label: Camp Management",
    "Move Member to Camp",
    "Move Active from Camp",
    "Line Break",
    "Label: Navigation",
    "Go Back"
]
MANAGE_BESTIARY_BUTTON_LABELS = [
    "Label: Monster Entry",
    "Add Monster",
    "Delete Monster",
    "Line Break",
    "Label: Move Monsters",
    "Move Monster to Required",
    "Move Monster to Random",
    "Move Monster to Archive",
    "Line Break",
    "Generate Encounter",
    "Label: Navigation",
    "Go Back"
]
SETTINGS_BUTTON_LABELS = [
    "Label: Settings",
    "Adjust Settings",
    "Reset Settings to Default",
    "Line Break",
    "Label: Clear Data",
    "Clear Party Data",
    "Clear Bestiary Data",
    "Clear Regions Data",
    "Clear All Data",
    "Label: Navigation",
    "Go Back"
]

GENERATORS_BUTTON_LABELS = [
    "Generate Encounter",
    "Generate Individual Loot",
    "Generate Treasure Hoard",
    "Label: Navigation",
    "Go Back"
]
REGIONS_BUTTON_LABELS = [
    "Label: Region Management",
    "Add New Region",
    "Remove Region",
    "Line Break",
    "Label: Navigation",
    "Party and NPCs",
    "Bestiary",
    "Go Back",
]
SPECIFIC_REGION_BUTTON_LABELS = [
    "Label: Region Management",
    "Update Description",
    "Add Note",
    "Update Note",
    "Remove Note",
    "Add City",
    "Remove City",
    "Add Point of Interest",
    "Remove Point of Interest",
    "Line Break",
    "Label: Navigation",
    "Party and NPCs",
    "Bestiary",
    "Regions",
    "Go Back",
    "Main Page"
]
CITY_BUTTON_LABELS = [
    "Label: City Management",
    "Update Description",
    "Add Note",
    "Update Note",
    "Remove Note",
    "Add Place",
    "Remove Place",
    "Add Shop",
    "Remove Shop",
    "Line Break",
    "Label: Navigation",
    "Party and NPCs",
    "Bestiary",
    "Regions",
    "Go Back",
    "Main Page"
]
POI_BUTTON_LABELS = [
    "Label: POI Management",
    "Update Description",
    "Add Note",
    "Update Note",
    "Remove Note",
    "Add Effect",
    "Update Effect",
    "Remove Effect",
    "Line Break",
    "Label: Navigation",
    "Party and NPCs",
    "Bestiary",
    "Regions",
    "Go Back",
    "Main Page"
]
SHOP_BUTTON_LABELS = [
    "Label: Shop Management",
    "Update Description",
    "Add Note",
    "Update Note",
    "Remove Note",
    "Add Inventory",
    "Update Inventory",
    "Remove Inventory",
    "Line Break",
    "Label: Navigation",
    "Party and NPCs",
    "Bestiary",
    "Regions",
    "Go Back",
    "Main Page"
]

# Constants
CONSTANT_LIST = load_json("settings.json")

WIDTH = str(CONSTANT_LIST["Width"])
HEIGHT = str(CONSTANT_LIST["Height"])

WINDOW_SIZE = f"{WIDTH}x{HEIGHT}"
BUTTON_PACK_OPTIONS = {"fill": tk.X, "pady": 5}

VALID_CLASSES = ["Artificer", "Barbarian", "Bard", "Cleric", "Druid",
                 "Fighter", "Monk", "Paladin", "Ranger", "Rogue",
                 "Sorcerer", "Warlock", "Wizard"]